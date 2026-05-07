"""Orders repository — all DB access for the orders table."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from magic_v22_mcp.db import get_conn
from magic_v22_mcp.enums import OrderStatus
from magic_v22_mcp.models import Order


def _row_to_order(row) -> Order:
    return Order(
        order_id=row["order_id"],
        order_date=datetime.fromisoformat(row["order_date"]),
        customer_name=row["customer_name"],
        order_number=row["order_number"],
        product_sku=row["product_sku"],
        units=row["units"],
        order_amount=row["order_amount"],
        remarks=row["remarks"],
        status=OrderStatus(row["status"]),
    )


def insert_order(
    order_date: datetime,
    customer_name: str,
    order_number: str,
    product_sku: str,
    units: int,
    order_amount: int,
    remarks: str,
    status: OrderStatus = OrderStatus.PENDING,
) -> Order:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO orders
                (order_date, customer_name, order_number, product_sku, units, order_amount, remarks, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order_date.isoformat(),
                customer_name,
                order_number,
                product_sku,
                units,
                order_amount,
                remarks,
                status.value,
            ),
        )
        conn.commit()
        order_id = cursor.lastrowid
    return get_by_id(order_id)


def get_by_id(order_id: int) -> Optional[Order]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM orders WHERE order_id=?", (order_id,)).fetchone()
    return _row_to_order(row) if row else None


def exists_order_number(order_number: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM orders WHERE order_number=?", (order_number,)
        ).fetchone()
    return row is not None


def search(
    customer_substr: Optional[str] = None,
    sku_substr: Optional[str] = None,
) -> list[Order]:
    clauses: list[str] = []
    params: list = []

    if customer_substr:
        clauses.append("LOWER(customer_name) LIKE ?")
        params.append(f"%{customer_substr.lower()}%")
    if sku_substr:
        clauses.append("LOWER(product_sku) LIKE ?")
        params.append(f"%{sku_substr.lower()}%")

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with get_conn() as conn:
        rows = conn.execute(f"SELECT * FROM orders {where} ORDER BY order_id", params).fetchall()
    return [_row_to_order(r) for r in rows]


def order_number_stats() -> dict:
    """Return counts per status and total revenue."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT status, COUNT(*) as cnt, SUM(order_amount) as rev FROM orders GROUP BY status"
        ).fetchall()
        total_row = conn.execute(
            "SELECT COUNT(*) as total, SUM(order_amount) as total_rev FROM orders"
        ).fetchone()
    by_status = {r["status"]: r["cnt"] for r in rows}
    return {
        "total": total_row["total"],
        "total_revenue": total_row["total_rev"] or 0,
        "by_status": by_status,
    }
