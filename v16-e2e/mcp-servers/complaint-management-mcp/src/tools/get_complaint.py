"""
Tool: get_complaint

Retrieves a single complaint by its numeric ID.
"""

from src.database import get_db
from src.models import Complaint
from src.schemas import ErrorResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def get_complaint(complaint_id: int) -> dict:
    """
    Retrieve a complaint by its ID.

    Args:
        complaint_id: The numeric ID of the complaint to retrieve.

    Returns:
        dict with ``success`` flag and complaint data, or an error dict if not found.
    """
    logger.info("get_complaint called | id=%s", complaint_id)

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
                logger.warning("get_complaint | id=%s not found", complaint_id)
                return ErrorResponse.create(
                    code="NOT_FOUND",
                    message=f"Complaint #{complaint_id} does not exist.",
                )

            data = complaint.to_dict()

        logger.info("get_complaint | id=%s found (archived=%s)", complaint_id, data["is_archived"])
        return {
            "success": True,
            "message": f"Complaint #{complaint_id} retrieved successfully.",
            "data": data,
        }

    except Exception as exc:
        logger.exception("get_complaint DB error: %s", exc)
        return ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Failed to retrieve complaint due to a database error.",
            details={"error": str(exc)},
        )
