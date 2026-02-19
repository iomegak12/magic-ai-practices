"""
Tool: archive_complaint

Soft-deletes a complaint by setting is_archived = True.
"""

from datetime import datetime, timezone

from src.database import get_db
from src.models import Complaint
from src.schemas import ErrorResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def archive_complaint(complaint_id: int) -> dict:
    """
    Archive (soft-delete) a complaint.

    Sets ``is_archived = True`` on the record. Archived complaints are excluded
    from default search results but remain in the database and can be retrieved
    via ``get_complaint`` or ``search_complaints`` with ``include_archived=True``.

    Rules:
    - A complaint that is already archived cannot be archived again.

    Args:
        complaint_id: The numeric ID of the complaint to archive.

    Returns:
        dict with ``success`` flag and the archived complaint data, or an error dict.
    """
    logger.info("archive_complaint called | id=%s", complaint_id)

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
                    code="ALREADY_ARCHIVED",
                    message=f"Complaint #{complaint_id} is already archived.",
                )

            complaint.is_archived = True
            complaint.updated_at = datetime.now(timezone.utc)

            session.commit()
            session.refresh(complaint)
            data = complaint.to_dict()

        logger.info("Complaint #%s archived.", complaint_id)
        return {
            "success": True,
            "message": f"Complaint #{complaint_id} has been archived.",
            "data": data,
        }

    except Exception as exc:
        logger.exception("archive_complaint DB error: %s", exc)
        return ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Failed to archive complaint due to a database error.",
            details={"error": str(exc)},
        )
