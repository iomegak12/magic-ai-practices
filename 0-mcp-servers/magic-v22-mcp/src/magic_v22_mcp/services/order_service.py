"""Order service — business logic layer for order operations."""

from __future__ import annotations

import re
import logging
from datetime import datetime, timezone
from typing import Optional

from magic_v22_mcp.db import next_order_number
from magic_v22_mcp.enums import OrderStatus
from magic_v22_mcp.models import Order
from magic_v22_mcp.repositories import orders_repo

logger = logging.getLogger(__name__)

ORDER_NUMBER_RE = re.compile(r"^ORD\d{5,}$")


class OrderServiceError(Exception):
    """Domain error for order operations."""


def make_order(
    customer_name: str,
    product_sku: str,
    units: int,
    order_amount: int,
    remarks: str = "",
    order_number: Optional[str] = None,
) -> Order:
    """Create a new order. Auto-generates order_number if not provided."""
    if order_number:
        if not ORDER_NUMBER_RE.match(order_number):
            raise OrderServiceError(
                f"Invalid order_number '{order_number}'. Must match ORD followed by 5+ digits, e.g. ORD10001."
            )
        if orders_repo.exists_order_number(order_number):
            raise OrderServiceError(f"order_number '{order_number}' already exists.")
    else:
        order_number = next_order_number()

    order = orders_repo.insert_order(
        order_date=datetime.now(timezone.utc),
        customer_name=customer_name,
        order_number=order_number,
        product_sku=product_sku,
        units=units,
        order_amount=order_amount,
        remarks=remarks,
        status=OrderStatus.PENDING,
    )
    logger.info("Order created: %s (id=%d) for customer '%s'", order.order_number, order.order_id, customer_name)
    return order


def query_orders(
    customer_name: Optional[str] = None,
    product_sku: Optional[str] = None,
) -> list[Order]:
    """Return orders matching partial customer name and/or product SKU."""
    return orders_repo.search(customer_substr=customer_name, sku_substr=product_sku)


def get_order_details(order_id: int) -> Order:
    """Return a single order by ID or raise if not found."""
    order = orders_repo.get_by_id(order_id)
    if order is None:
        raise OrderServiceError(f"Order with id={order_id} not found.")
    return order
