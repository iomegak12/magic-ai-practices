"""Idempotent seeder — runs only when both tables are empty."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from magic_v22_mcp.db import get_conn, next_order_number
from magic_v22_mcp.enums import ComplaintPriority, ComplaintStatus, OrderStatus, ResolverTeam
from magic_v22_mcp.repositories import complaints_repo, orders_repo

logger = logging.getLogger(__name__)

_SEED_ORDERS = [
    # (customer_name, product_sku, units, order_amount, remarks, status, days_ago)
    ("James Mitchell", "SKU-LAPTOP-001", 1, 1299, "Gift wrap please", OrderStatus.DELIVERED, 30),
    ("Priya Krishnamurthy", "SKU-PHONE-002", 2, 1598, "", OrderStatus.SHIPPED, 10),
    ("Liam O'Brien", "SKU-HEADPHONE-003", 1, 249, "Express shipping", OrderStatus.PROCESSING, 3),
    ("Ananya Sharma", "SKU-TABLET-004", 1, 849, "", OrderStatus.PENDING, 1),
    ("Emily Chen", "SKU-MONITOR-005", 2, 1100, "Office use", OrderStatus.DELIVERED, 60),
    ("Rajesh Patel", "SKU-KEYBOARD-006", 3, 210, "", OrderStatus.CANCELLED, 20),
    ("Sophie Williams", "SKU-MOUSE-007", 5, 175, "Bulk order", OrderStatus.DELIVERED, 45),
    ("Arjun Nair", "SKU-WEBCAM-008", 1, 129, "", OrderStatus.SHIPPED, 7),
    ("Olivia Thompson", "SKU-CHARGER-009", 4, 180, "", OrderStatus.PROCESSING, 2),
    ("Karthik Subramanian", "SKU-SPEAKER-010", 1, 399, "Birthday gift", OrderStatus.DELIVERED, 90),
]

_SEED_COMPLAINTS = [
    # (order_index, registered_by, description, priority, status, resolved_by, resolution_remarks)
    (
        0, "James Mitchell",
        "Product arrived damaged. Screen cracked on delivery.",
        ComplaintPriority.HIGH, ComplaintStatus.RESOLVED,
        ResolverTeam.RETURNS_AND_REFUNDS,
        "Replacement unit dispatched. Customer confirmed receipt.",
    ),
    (
        1, "Priya Krishnamurthy",
        "Wrong color variant shipped. Ordered black, received white.",
        ComplaintPriority.MEDIUM, ComplaintStatus.IN_PROGRESS,
        None, None,
    ),
    (
        2, "Liam O'Brien",
        "Shipment delayed beyond estimated delivery date.",
        ComplaintPriority.LOW, ComplaintStatus.OPEN,
        None, None,
    ),
    (
        4, "Emily Chen",
        "Monitor has dead pixels on the lower right corner.",
        ComplaintPriority.CRITICAL, ComplaintStatus.RESOLVED,
        ResolverTeam.QUALITY_ASSURANCE,
        "Unit recalled. Full refund issued to customer's payment method.",
    ),
    (
        7, "Arjun Nair",
        "Webcam not detected by Windows 11. Driver issue suspected.",
        ComplaintPriority.HIGH, ComplaintStatus.OPEN,
        None, None,
    ),
]


def _days_ago(n: int) -> datetime:
    from datetime import timedelta
    return datetime.now(timezone.utc) - timedelta(days=n)


def run_seed() -> None:
    """Seed the DB with sample data if both tables are empty."""
    with get_conn() as conn:
        order_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        complaint_count = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]

    if order_count > 0 or complaint_count > 0:
        logger.debug("Seed skipped — data already present (%d orders, %d complaints).", order_count, complaint_count)
        return

    logger.info("Seeding database with sample orders and complaints …")
    inserted_orders = []
    for name, sku, units, amount, remarks, status, days in _SEED_ORDERS:
        order_num = next_order_number()
        order = orders_repo.insert_order(
            order_date=_days_ago(days),
            customer_name=name,
            order_number=order_num,
            product_sku=sku,
            units=units,
            order_amount=amount,
            remarks=remarks,
            status=status,
        )
        inserted_orders.append(order)
        logger.debug("  Seeded order %s for %s", order.order_number, name)

    for idx, reg_by, desc, priority, status, resolved_by, res_remarks in _SEED_COMPLAINTS:
        order = inserted_orders[idx]
        complaint = complaints_repo.insert_complaint(
            complaint_date=_days_ago(1),
            order_id=order.order_id,
            registered_by=reg_by,
            complaint_description=desc,
            priority=priority,
            status=status,
        )
        if resolved_by:
            complaints_repo.update_status_resolve(
                complaint.complaint_id, resolved_by, res_remarks
            )
        logger.debug("  Seeded complaint #%d for order %s", complaint.complaint_id, order.order_number)

    logger.info("Seed complete: %d orders, %d complaints.", len(_SEED_ORDERS), len(_SEED_COMPLAINTS))
