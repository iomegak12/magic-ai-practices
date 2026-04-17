"""Complaint management tools for the MCP server."""

import logging
from typing import Any
from datetime import datetime

from sqlalchemy import func

from database.connection import db
from models.order import Order
from models.complaint import Complaint
from config.settings import settings

logger = logging.getLogger(__name__)


def _next_complaint_id(session) -> str:
    """Generate the next COMP ID by finding the current max."""
    last = (
        session.query(Complaint.complaint_id)
        .order_by(Complaint.complaint_id.desc())
        .first()
    )
    if last:
        num = int(last[0].replace("COMP", "")) + 1
    else:
        num = 10001
    return f"COMP{num}"


def get_complaints_by_order(order_id: str) -> dict[str, Any]:
    """Get all complaints for a specific order ID."""
    with db.get_session() as session:
        complaints = (
            session.query(Complaint)
            .filter(Complaint.order_id == order_id)
            .order_by(Complaint.complaint_reg_date.desc())
            .all()
        )
        results = [c.to_dict() for c in complaints]

    return {
        "operation": "get_complaints_by_order",
        "success": True,
        "message": f"Found {len(results)} complaint(s) for order '{order_id}'.",
        "result": results,
        "count": len(results),
    }


def get_complaints_by_customer(customer_name: str) -> dict[str, Any]:
    """Get all complaints for a customer (partial, case-insensitive match via order join)."""
    with db.get_session() as session:
        complaints = (
            session.query(Complaint)
            .join(Order, Complaint.order_id == Order.order_id)
            .filter(func.lower(Order.customer_name).contains(customer_name.lower()))
            .order_by(Complaint.complaint_reg_date.desc())
            .all()
        )
        results = [c.to_dict() for c in complaints]

    return {
        "operation": "get_complaints_by_customer",
        "success": True,
        "message": f"Found {len(results)} complaint(s) for customer matching '{customer_name}'.",
        "result": results,
        "count": len(results),
    }


def register_complaint(
    order_id: str,
    complaint_description: str,
    priority: str | None = None,
) -> dict[str, Any]:
    """Register a new complaint against an existing order."""
    with db.get_session() as session:
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            return {
                "operation": "register_complaint",
                "success": False,
                "error": f"Order '{order_id}' not found. Cannot register complaint.",
                "result": None,
                "count": 0,
            }

        effective_priority = priority or settings.DEFAULT_COMPLAINT_PRIORITY
        if effective_priority not in settings.VALID_COMPLAINT_PRIORITIES:
            return {
                "operation": "register_complaint",
                "success": False,
                "error": f"Invalid priority '{effective_priority}'. Valid: {settings.VALID_COMPLAINT_PRIORITIES}",
                "result": None,
                "count": 0,
            }

        complaint = Complaint(
            complaint_id=_next_complaint_id(session),
            complaint_reg_date=datetime.utcnow(),
            order_id=order_id,
            complaint_description=complaint_description,
            priority=effective_priority,
            assigned_to=settings.DEFAULT_ASSIGNED_TO,
            complaint_status=settings.DEFAULT_COMPLAINT_STATUS,
        )
        session.add(complaint)
        session.flush()
        result = complaint.to_dict()

    return {
        "operation": "register_complaint",
        "success": True,
        "message": f"Complaint '{result['complaint_id']}' registered for order '{order_id}'.",
        "result": result,
        "count": 1,
    }


def resolve_complaint(
    complaint_id: str,
    resolution_note: str,
) -> dict[str, Any]:
    """Resolve an existing complaint with a resolution note."""
    with db.get_session() as session:
        complaint = (
            session.query(Complaint)
            .filter(Complaint.complaint_id == complaint_id)
            .first()
        )
        if not complaint:
            return {
                "operation": "resolve_complaint",
                "success": False,
                "error": f"Complaint '{complaint_id}' not found.",
                "result": None,
                "count": 0,
            }

        if complaint.complaint_status == "Resolved":
            return {
                "operation": "resolve_complaint",
                "success": False,
                "error": f"Complaint '{complaint_id}' is already resolved.",
                "result": complaint.to_dict(),
                "count": 0,
            }

        complaint.complaint_status = "Resolved"
        complaint.resolution_note = resolution_note
        session.flush()
        result = complaint.to_dict()

    return {
        "operation": "resolve_complaint",
        "success": True,
        "message": f"Complaint '{complaint_id}' has been resolved.",
        "result": result,
        "count": 1,
    }
