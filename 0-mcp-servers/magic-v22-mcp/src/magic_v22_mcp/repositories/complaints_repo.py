"""Complaints repository — all DB access for the complaints table."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from magic_v22_mcp.db import get_conn
from magic_v22_mcp.enums import ComplaintPriority, ComplaintStatus, ResolverTeam
from magic_v22_mcp.models import Complaint


def _row_to_complaint(row) -> Complaint:
    return Complaint(
        complaint_id=row["complaint_id"],
        complaint_date=datetime.fromisoformat(row["complaint_date"]),
        order_id=row["order_id"],
        registered_by=row["registered_by"],
        complaint_description=row["complaint_description"],
        priority=ComplaintPriority(row["priority"]),
        status=ComplaintStatus(row["status"]),
        resolved_by=ResolverTeam(row["resolved_by"]) if row["resolved_by"] else None,
        resolution_remarks=row["resolution_remarks"],
    )


def insert_complaint(
    complaint_date: datetime,
    order_id: int,
    registered_by: str,
    complaint_description: str,
    priority: ComplaintPriority,
    status: ComplaintStatus = ComplaintStatus.OPEN,
) -> Complaint:
    with get_conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO complaints
                (complaint_date, order_id, registered_by, complaint_description, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                complaint_date.isoformat(),
                order_id,
                registered_by,
                complaint_description,
                priority.value,
                status.value,
            ),
        )
        conn.commit()
        complaint_id = cursor.lastrowid
    return get_by_id(complaint_id)


def get_by_id(complaint_id: int) -> Optional[Complaint]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM complaints WHERE complaint_id=?", (complaint_id,)
        ).fetchone()
    return _row_to_complaint(row) if row else None


def search(
    order_id: Optional[int] = None,
    customer_substr: Optional[str] = None,
    registered_by_substr: Optional[str] = None,
    priority: Optional[ComplaintPriority] = None,
    status: Optional[ComplaintStatus] = None,
    resolved_by: Optional[ResolverTeam] = None,
    description_substr: Optional[str] = None,
) -> list[Complaint]:
    clauses: list[str] = []
    params: list = []

    if order_id is not None:
        clauses.append("c.order_id = ?")
        params.append(order_id)
    if customer_substr:
        clauses.append("LOWER(o.customer_name) LIKE ?")
        params.append(f"%{customer_substr.lower()}%")
    if registered_by_substr:
        clauses.append("LOWER(c.registered_by) LIKE ?")
        params.append(f"%{registered_by_substr.lower()}%")
    if priority:
        clauses.append("c.priority = ?")
        params.append(priority.value)
    if status:
        clauses.append("c.status = ?")
        params.append(status.value)
    if resolved_by:
        clauses.append("c.resolved_by = ?")
        params.append(resolved_by.value)
    if description_substr:
        clauses.append("LOWER(c.complaint_description) LIKE ?")
        params.append(f"%{description_substr.lower()}%")

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    sql = f"""
        SELECT c.*
        FROM complaints c
        JOIN orders o ON o.order_id = c.order_id
        {where}
        ORDER BY c.complaint_id
    """
    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_row_to_complaint(r) for r in rows]


def update_status_resolve(
    complaint_id: int,
    resolved_by: ResolverTeam,
    resolution_remarks: str,
) -> Optional[Complaint]:
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE complaints
            SET status=?, resolved_by=?, resolution_remarks=?
            WHERE complaint_id=?
            """,
            (ComplaintStatus.RESOLVED.value, resolved_by.value, resolution_remarks, complaint_id),
        )
        conn.commit()
    return get_by_id(complaint_id)


def update_status_close(complaint_id: int) -> Optional[Complaint]:
    with get_conn() as conn:
        conn.execute(
            "UPDATE complaints SET status=? WHERE complaint_id=?",
            (ComplaintStatus.CLOSED.value, complaint_id),
        )
        conn.commit()
    return get_by_id(complaint_id)


def complaint_stats() -> dict:
    """Return counts by status, priority, and resolved_by team."""
    with get_conn() as conn:
        by_status = {
            r["status"]: r["cnt"]
            for r in conn.execute(
                "SELECT status, COUNT(*) as cnt FROM complaints GROUP BY status"
            ).fetchall()
        }
        by_priority = {
            r["priority"]: r["cnt"]
            for r in conn.execute(
                "SELECT priority, COUNT(*) as cnt FROM complaints GROUP BY priority"
            ).fetchall()
        }
        by_team = {
            r["resolved_by"]: r["cnt"]
            for r in conn.execute(
                "SELECT resolved_by, COUNT(*) as cnt FROM complaints WHERE resolved_by IS NOT NULL GROUP BY resolved_by"
            ).fetchall()
        }
        total = conn.execute("SELECT COUNT(*) as cnt FROM complaints").fetchone()["cnt"]
    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority,
        "by_resolver_team": by_team,
    }


def get_open_complaints() -> list[Complaint]:
    """Return all OPEN, IN_PROGRESS, and REOPENED complaints."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM complaints WHERE status IN ('OPEN','IN_PROGRESS','REOPENED') ORDER BY complaint_id"
        ).fetchall()
    return [_row_to_complaint(r) for r in rows]
