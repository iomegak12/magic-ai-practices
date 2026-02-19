"""
Tool: update_complaint

Updates editable fields of an existing complaint.
"""

from datetime import datetime, timezone

from src.database import get_db
from src.models import Complaint
from src.schemas import ErrorResponse
from src.utils.logger import get_logger
from src.utils.validators import validate_description, validate_title

logger = get_logger(__name__)


async def update_complaint(
    complaint_id: int,
    title: str = "",
    description: str = "",
    remarks: str = "",
) -> dict:
    """
    Update the editable fields of an existing complaint.

    Only the fields you supply (non-empty strings) will be updated. Fields left
    blank are left unchanged.

    Updatable fields:
    - ``title``       — must pass title validation if provided.
    - ``description`` — must pass description validation if provided.
    - ``remarks``     — free-form notes; pass a non-empty string to overwrite.

    Rules:
    - Archived complaints cannot be updated.
    - At least one field must be provided.

    Args:
        complaint_id: The numeric ID of the complaint to update.
        title:        New title (optional; leave blank to keep current).
        description:  New description (optional; leave blank to keep current).
        remarks:      New remarks (optional; leave blank to keep current).

    Returns:
        dict with ``success`` flag and updated complaint data, or an error dict.
    """
    logger.info("update_complaint called | id=%s", complaint_id)

    if not isinstance(complaint_id, int) or complaint_id < 1:
        return ErrorResponse.create(
            code="INVALID_ID",
            message="complaint_id must be a positive integer.",
        )

    # Normalise
    title = (title or "").strip()
    description = (description or "").strip()
    remarks = (remarks or "").strip()

    if not any([title, description, remarks]):
        return ErrorResponse.create(
            code="NO_UPDATES",
            message="At least one field must be provided: title, description, or remarks.",
        )

    # Validate before touching the DB
    if title:
        try:
            title = validate_title(title)
        except ValueError as exc:
            return ErrorResponse.create(code="VALIDATION_ERROR", message=str(exc))

    if description:
        try:
            description = validate_description(description)
        except ValueError as exc:
            return ErrorResponse.create(code="VALIDATION_ERROR", message=str(exc))

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

            updated_fields: list[str] = []

            if title:
                complaint.title = title
                updated_fields.append("title")

            if description:
                complaint.description = description
                updated_fields.append("description")

            if remarks:
                complaint.remarks = remarks
                updated_fields.append("remarks")

            complaint.updated_at = datetime.now(timezone.utc)

            session.commit()
            session.refresh(complaint)
            data = complaint.to_dict()

        logger.info(
            "Complaint #%s updated | fields=%s", complaint_id, updated_fields
        )
        return {
            "success": True,
            "message": (
                f"Complaint #{complaint_id} updated successfully. "
                f"Fields changed: {', '.join(updated_fields)}."
            ),
            "data": data,
        }

    except Exception as exc:
        logger.exception("update_complaint DB error: %s", exc)
        return ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Failed to update complaint due to a database error.",
            details={"error": str(exc)},
        )
