"""
Tool: search_complaints

Searches complaints using OR-logic across multiple optional filters.
"""

from sqlalchemy import or_

from src.database import get_db
from src.enums import Status
from src.models import Complaint
from src.schemas import ErrorResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def search_complaints(
    customer_name: str = "",
    order_number: str = "",
    title: str = "",
    status: str = "",
    include_archived: bool = False,
) -> dict:
    """
    Search for complaints using OR-logic across text fields.

    At least one search criterion is required (status alone is also accepted).
    Text fields are matched with a case-insensitive partial (LIKE) match.
    Multiple text fields are combined with OR — a complaint is returned if it
    matches *any* of the provided text filters.

    Args:
        customer_name:    Partial customer name to search for.
        order_number:     Partial order number to search for.
        title:            Partial title to search for.
        status:           Exact status match — OPEN | IN_PROGRESS | RESOLVED | CLOSED.
        include_archived: When True, includes soft-deleted (archived) complaints
                          in results (default: False).

    Returns:
        dict with ``success`` flag and a ``data`` list of matching complaints,
        or an error dict.
    """
    logger.info(
        "search_complaints called | customer=%r order=%r title=%r status=%r archived=%s",
        customer_name, order_number, title, status, include_archived,
    )

    # Normalise inputs
    customer_name = (customer_name or "").strip()
    order_number = (order_number or "").strip()
    title = (title or "").strip()
    status = (status or "").strip().upper()

    # At least one criterion required
    if not any([customer_name, order_number, title, status]):
        return ErrorResponse.create(
            code="NO_CRITERIA",
            message=(
                "At least one search criterion is required: "
                "customer_name, order_number, title, or status."
            ),
        )

    # Validate status if provided
    status_enum: Status | None = None
    if status:
        try:
            status_enum = Status(status)
        except ValueError:
            return ErrorResponse.create(
                code="INVALID_STATUS",
                message=f"Invalid status '{status}'. Must be one of: OPEN, IN_PROGRESS, RESOLVED, CLOSED.",
            )

    try:
        with get_db() as session:
            query = session.query(Complaint)

            # Archived filter
            if not include_archived:
                query = query.filter(Complaint.is_archived == False)  # noqa: E712

            # Build OR conditions for text fields
            or_conditions = []
            if customer_name:
                or_conditions.append(
                    Complaint.customer_name.ilike(f"%{customer_name}%")
                )
            if order_number:
                or_conditions.append(
                    Complaint.order_number.ilike(f"%{order_number}%")
                )
            if title:
                or_conditions.append(
                    Complaint.title.ilike(f"%{title}%")
                )

            if or_conditions:
                query = query.filter(or_(*or_conditions))

            # Exact status filter applied on top of OR results
            if status_enum is not None:
                query = query.filter(Complaint.status == status_enum)

            # Order by most recently updated first
            query = query.order_by(Complaint.updated_at.desc())

            complaints = query.all()
            results = [c.to_dict() for c in complaints]

            # -----------------------------------------------------------------
            # Zero-result diagnostics
            # When nothing is found, check what filters are hiding results and
            # surface an actionable hint in the response message.
            # -----------------------------------------------------------------
            hint: str = ""
            if not results:
                # 1. Check if the OR text filters alone (ignoring status) would
                #    have matched — tells us the status filter is the culprit.
                if status_enum is not None and or_conditions:
                    base_q = session.query(Complaint)
                    if not include_archived:
                        base_q = base_q.filter(Complaint.is_archived == False)  # noqa: E712
                    base_q = base_q.filter(or_(*or_conditions))
                    matches_without_status = base_q.count()
                    if matches_without_status:
                        hint = (
                            f" {matches_without_status} matching record(s) exist "
                            f"but have a different status than '{status_enum.value}'. "
                            "Try omitting the status filter or use a different value."
                        )

                # 2. Check if the same query against the archived pool would
                #    have matched — tells us is_archived is the culprit.
                if not hint and not include_archived:
                    archived_q = session.query(Complaint).filter(
                        Complaint.is_archived == True  # noqa: E712
                    )
                    if or_conditions:
                        archived_q = archived_q.filter(or_(*or_conditions))
                    if status_enum is not None:
                        archived_q = archived_q.filter(
                            Complaint.status == status_enum
                        )
                    archived_matches = archived_q.count()
                    if archived_matches:
                        hint = (
                            f" {archived_matches} matching record(s) exist but "
                            "are archived. Re-run with include_archived=true to "
                            "see them."
                        )

        logger.info("search_complaints | %d result(s) found", len(results))
        return {
            "success": True,
            "message": f"{len(results)} complaint(s) found.{hint}",
            "data": results,
            "count": len(results),
        }

    except Exception as exc:
        logger.exception("search_complaints DB error: %s", exc)
        return ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Failed to search complaints due to a database error.",
            details={"error": str(exc)},
        )
