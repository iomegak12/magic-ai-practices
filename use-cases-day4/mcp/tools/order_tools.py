"""Order query tools for the MCP server."""

import logging
from typing import Any

from sqlalchemy import func

from database.connection import db
from models.order import Order
from config.settings import settings

logger = logging.getLogger(__name__)


def get_orders_by_customer(customer_name: str) -> dict[str, Any]:
    """Get all orders for a customer name (partial, case-insensitive match)."""
    with db.get_session() as session:
        orders = (
            session.query(Order)
            .filter(func.lower(Order.customer_name).contains(customer_name.lower()))
            .order_by(Order.order_date.desc())
            .all()
        )
        results = [o.to_dict() for o in orders]

    return {
        "operation": "get_orders_by_customer",
        "success": True,
        "message": f"Found {len(results)} order(s) matching customer '{customer_name}'.",
        "result": results,
        "count": len(results),
    }


def search_orders_by_sku(product_sku: str) -> dict[str, Any]:
    """Search orders by exact product SKU."""
    with db.get_session() as session:
        orders = (
            session.query(Order)
            .filter(Order.product_sku == product_sku)
            .order_by(Order.order_date.desc())
            .all()
        )
        results = [o.to_dict() for o in orders]

    return {
        "operation": "search_orders_by_sku",
        "success": True,
        "message": f"Found {len(results)} order(s) for SKU '{product_sku}'.",
        "result": results,
        "count": len(results),
    }


def search_orders_by_status(order_status: str) -> dict[str, Any]:
    """Search orders filtered by order status."""
    if order_status not in settings.VALID_ORDER_STATUSES:
        return {
            "operation": "search_orders_by_status",
            "success": False,
            "error": f"Invalid status '{order_status}'. Valid statuses: {settings.VALID_ORDER_STATUSES}",
            "result": [],
            "count": 0,
        }

    with db.get_session() as session:
        orders = (
            session.query(Order)
            .filter(Order.order_status == order_status)
            .order_by(Order.order_date.desc())
            .all()
        )
        results = [o.to_dict() for o in orders]

    return {
        "operation": "search_orders_by_status",
        "success": True,
        "message": f"Found {len(results)} order(s) with status '{order_status}'.",
        "result": results,
        "count": len(results),
    }
