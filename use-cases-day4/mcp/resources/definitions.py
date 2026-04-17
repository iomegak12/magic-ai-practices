"""Resource definitions for the MCP server."""

import json
from sqlalchemy import func

from database.connection import db
from models.order import Order
from models.complaint import Complaint
from config.settings import settings


def _orders_summary() -> str:
    """Total orders with breakdown by status."""
    with db.get_session() as session:
        total = session.query(func.count(Order.order_id)).scalar()
        rows = (
            session.query(Order.order_status, func.count(Order.order_id))
            .group_by(Order.order_status)
            .all()
        )
    by_status = {status: count for status, count in rows}
    return json.dumps({"total_orders": total, "by_status": by_status}, indent=2)


def _complaints_summary() -> str:
    """Total complaints with breakdown by status and priority."""
    with db.get_session() as session:
        total = session.query(func.count(Complaint.complaint_id)).scalar()
        status_rows = (
            session.query(Complaint.complaint_status, func.count(Complaint.complaint_id))
            .group_by(Complaint.complaint_status)
            .all()
        )
        priority_rows = (
            session.query(Complaint.priority, func.count(Complaint.complaint_id))
            .group_by(Complaint.priority)
            .all()
        )
    return json.dumps(
        {
            "total_complaints": total,
            "by_status": {s: c for s, c in status_rows},
            "by_priority": {p: c for p, c in priority_rows},
        },
        indent=2,
    )


def _config_statuses() -> str:
    """All valid enums used in the system."""
    return json.dumps(
        {
            "order_statuses": settings.VALID_ORDER_STATUSES,
            "complaint_priorities": settings.VALID_COMPLAINT_PRIORITIES,
            "complaint_statuses": settings.VALID_COMPLAINT_STATUSES,
        },
        indent=2,
    )


def _recent_orders() -> str:
    """Last 10 orders by date."""
    with db.get_session() as session:
        orders = (
            session.query(Order)
            .order_by(Order.order_date.desc())
            .limit(10)
            .all()
        )
        results = [o.to_dict() for o in orders]
    return json.dumps(results, indent=2)


def _unresolved_complaints() -> str:
    """All complaints with status Open or In Progress."""
    with db.get_session() as session:
        complaints = (
            session.query(Complaint)
            .filter(Complaint.complaint_status.in_(["Open", "In Progress"]))
            .order_by(Complaint.complaint_reg_date.desc())
            .all()
        )
        results = [c.to_dict() for c in complaints]
    return json.dumps(results, indent=2)
