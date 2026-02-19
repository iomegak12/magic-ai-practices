"""
Tool: resolve_complaint

Marks a complaint as RESOLVED and records the resolution timestamp.
"""

from datetime import datetime, timezone

from src.database import get_db
from src.enums import Status
from src.models import Complaint
from src.schemas import ErrorResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def resolve_complaint(complaint_id: int, remarks: str = "") -> dict:
    """
    Mark a complaint as resolved.

    Sets the complaint status to RESOLVED and records the current UTC timestamp
    as the resolution date. Optionally appends resolution notes to the remarks
    field.

    Rules:
    - Cannot resolve an already RESOLVED or CLOSED complaint.
    - Cannot resolve an archived complaint.

    Args:
        complaint_id: The numeric ID of the complaint to resolve.
        remarks:      Optional resolution notes to append to the complaint.

    Returns:
        dict with ``success`` flag and updated complaint data, or an error dict.
    """
    logger.info("resolve_complaint called | id=%s", complaint_id)

    if not isinstance(complaint_id, int) or complaint_id < 1:
        return ErrorResponse.create(
            code="INVALID_ID",
            message="complaint_id must be a positive integer.",
        )

    try:
        with get_db() as session:
            complaint = (
                session.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id)
                .first()
            )

            if complaint is None:
                return ErrorResponse.create(
                    code="NOT_FOUND",
                    message=f"Complaint #{complaint_id} does not exist.",
                )

            if complaint.is_archived:
                return ErrorResponse.create(
                    code="COMPLAINT_ARCHIVED",
                    message=f"Complaint #{complaint_id} is archived and cannot be modified.",
                )

            if complaint.status in (Status.RESOLVED, Status.CLOSED):
                return ErrorResponse.create(
                    code="ALREADY_RESOLVED",
                    message=(
                        f"Complaint #{complaint_id} is already {complaint.status.value} "
                        "and cannot be resolved again."
                    ),
                )

            now = datetime.now(timezone.utc)
            complaint.status = Status.RESOLVED
            complaint.resolution_date = now
            complaint.updated_at = now

            if remarks and remarks.strip():
                complaint.remarks = remarks.strip()

            session.commit()
            session.refresh(complaint)
            data = complaint.to_dict()

        logger.info("Complaint #%s resolved at %s", complaint_id, data["resolution_date"])
        return {
            "success": True,
            "message": f"Complaint #{complaint_id} has been resolved.",
            "data": data,
        }

    except Exception as exc:
        logger.exception("resolve_complaint DB error: %s", exc)
        return ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Failed to resolve complaint due to a database error.",
            details={"error": str(exc)},
        )
