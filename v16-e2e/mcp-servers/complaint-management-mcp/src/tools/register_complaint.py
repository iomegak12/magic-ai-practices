"""
Tool: register_complaint

Registers a new complaint for a customer order.
"""

from datetime import datetime, timezone

from src.database import get_db
from src.enums import Priority, Status
from src.models import Complaint
from src.schemas import ErrorResponse
from src.utils.logger import get_logger
from src.utils.validators import (
    validate_customer_name,
    validate_description,
    validate_order_number,
    validate_title,
)

logger = get_logger(__name__)


async def register_complaint(
    title: str,
    description: str,
    customer_name: str,
    order_number: str,
    priority: str = "MEDIUM",
    remarks: str = "",
) -> dict:
    """
    Register a new customer complaint for a specific order.

    Args:
        title:         Short summary of the issue (5–200 chars).
        description:   Full description of the problem (10–2000 chars).
        customer_name: Full name of the customer (letters and spaces only).
        order_number:  Order reference in the format ORD-NNNNN (e.g. ORD-10001).
        priority:      Severity level — LOW | MEDIUM | HIGH | CRITICAL (default: MEDIUM).
        remarks:       Optional additional notes (leave blank if none).

    Returns:
        dict with ``success`` flag and the created complaint data, or an error dict.
    """
    logger.info(
        "register_complaint called | order=%s customer=%s priority=%s",
        order_number, customer_name, priority,
    )

    # --- Input validation ---
    try:
        title = validate_title(title)
        description = validate_description(description)
        customer_name = validate_customer_name(customer_name)
        order_number = validate_order_number(order_number)
    except ValueError as exc:
        logger.warning("register_complaint validation error: %s", exc)
        return ErrorResponse.create(
            code="VALIDATION_ERROR",
            message=str(exc),
        )

    try:
        priority_enum = Priority(priority.upper())
    except (ValueError, AttributeError):
        return ErrorResponse.create(
            code="INVALID_PRIORITY",
            message=f"Invalid priority '{priority}'. Must be one of: LOW, MEDIUM, HIGH, CRITICAL.",
        )

    # --- Persist ---
    try:
        with get_db() as session:
            now = datetime.now(timezone.utc)
            complaint = Complaint(
                title=title,
                description=description,
                customer_name=customer_name,
                order_number=order_number,
                priority=priority_enum,
                status=Status.OPEN,
                remarks=remarks.strip() if remarks else None,
                is_archived=False,
                created_at=now,
                updated_at=now,
            )
            session.add(complaint)
            session.commit()
            session.refresh(complaint)
            data = complaint.to_dict()

        logger.info("Complaint registered | id=%s order=%s", data["complaint_id"], order_number)
        return {
            "success": True,
            "message": f"Complaint #{data['complaint_id']} registered successfully.",
            "data": data,
        }

    except Exception as exc:
        logger.exception("register_complaint DB error: %s", exc)
        return ErrorResponse.create(
            code="DATABASE_ERROR",
            message="Failed to register complaint due to a database error.",
            details={"error": str(exc)},
        )
