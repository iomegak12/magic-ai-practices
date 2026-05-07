"""Complaint service — business logic layer for complaint operations."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from magic_v22_mcp.enums import ComplaintPriority, ComplaintStatus, ResolverTeam
from magic_v22_mcp.models import Complaint
from magic_v22_mcp.repositories import complaints_repo, orders_repo

logger = logging.getLogger(__name__)

# States from which a complaint can be resolved
_RESOLVABLE_STATUSES = {ComplaintStatus.OPEN, ComplaintStatus.IN_PROGRESS, ComplaintStatus.REOPENED}


class ComplaintServiceError(Exception):
    """Domain error for complaint operations."""


def register_complaint(
    order_id: int,
    registered_by: str,
    complaint_description: str,
    priority: ComplaintPriority,
) -> Complaint:
    """Register a new complaint against an existing order."""
    if orders_repo.get_by_id(order_id) is None:
        raise ComplaintServiceError(f"Order with id={order_id} does not exist.")

    complaint = complaints_repo.insert_complaint(
        complaint_date=datetime.now(timezone.utc),
        order_id=order_id,
        registered_by=registered_by,
        complaint_description=complaint_description,
        priority=priority,
    )
    logger.info(
        "Complaint #%d registered for order_id=%d by '%s' [%s]",
        complaint.complaint_id, order_id, registered_by, priority,
    )
    return complaint


def get_complaint_details(complaint_id: int) -> Complaint:
    """Return a single complaint by ID or raise if not found."""
    complaint = complaints_repo.get_by_id(complaint_id)
    if complaint is None:
        raise ComplaintServiceError(f"Complaint with id={complaint_id} not found.")
    return complaint


def search_complaints(
    order_id: Optional[int] = None,
    customer_name: Optional[str] = None,
    registered_by: Optional[str] = None,
    priority: Optional[ComplaintPriority] = None,
    status: Optional[ComplaintStatus] = None,
    resolved_by: Optional[ResolverTeam] = None,
    description: Optional[str] = None,
) -> list[Complaint]:
    """Search complaints with any combination of optional filters (all partial/case-insensitive)."""
    return complaints_repo.search(
        order_id=order_id,
        customer_substr=customer_name,
        registered_by_substr=registered_by,
        priority=priority,
        status=status,
        resolved_by=resolved_by,
        description_substr=description,
    )


def resolve_complaint(
    complaint_id: int,
    resolved_by_team: ResolverTeam,
    resolution_remarks: str,
) -> Complaint:
    """Resolve a complaint — only allowed from OPEN, IN_PROGRESS, or REOPENED."""
    complaint = get_complaint_details(complaint_id)
    if complaint.status not in _RESOLVABLE_STATUSES:
        raise ComplaintServiceError(
            f"Cannot resolve complaint #{complaint_id}: current status is '{complaint.status}'. "
            f"Must be one of {[s.value for s in _RESOLVABLE_STATUSES]}."
        )
    updated = complaints_repo.update_status_resolve(complaint_id, resolved_by_team, resolution_remarks)
    logger.info(
        "Complaint #%d resolved by team '%s'", complaint_id, resolved_by_team
    )
    return updated


def close_complaint(complaint_id: int) -> Complaint:
    """Close a complaint — only allowed when status is RESOLVED."""
    complaint = get_complaint_details(complaint_id)
    if complaint.status != ComplaintStatus.RESOLVED:
        raise ComplaintServiceError(
            f"Cannot close complaint #{complaint_id}: current status is '{complaint.status}'. "
            "Only RESOLVED complaints can be closed."
        )
    updated = complaints_repo.update_status_close(complaint_id)
    logger.info("Complaint #%d closed.", complaint_id)
    return updated
