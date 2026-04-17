"""Complaint management tools."""

import json
from datetime import datetime
from typing import Annotated, Optional

from agent_framework import tool
from pydantic import Field

from .database import get_session
from .models import Complaint, Customer, CustomerProfilePreference


def _next_complaint_id() -> str:
    """Generate the next complaint ID (COMP10001, COMP10002, ...)."""
    with get_session() as session:
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


@tool(approval_mode="never_require")
def get_complaints_by_customer(
    customer_id: Annotated[str, Field(description="The customer ID to retrieve complaints for, e.g. CUST10001.")]
) -> str:
    """Get all complaint records for a specific customer."""
    with get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Error: Customer with ID {customer_id} not found."

        complaints = (
            session.query(Complaint)
            .filter(Complaint.customer_id == customer_id)
            .order_by(Complaint.complaint_date.desc())
            .all()
        )

        if not complaints:
            return f"No complaints found for customer {customer_id}."

        records = [c.to_dict() for c in complaints]
        return f"Found {len(records)} complaint(s) for customer {customer_id}: {json.dumps(records, indent=2)}"


@tool(approval_mode="never_require")
def get_complaints_by_status(
    status: Annotated[
        str,
        Field(description="Complaint status to filter by: Open, In Progress, Resolved, Closed, or Reopened."),
    ]
) -> str:
    """Get all complaint records filtered by status."""
    valid_statuses = {"Open", "In Progress", "Resolved", "Closed", "Reopened"}
    if status not in valid_statuses:
        return f"Error: Invalid status '{status}'. Must be one of: {', '.join(sorted(valid_statuses))}."

    with get_session() as session:
        complaints = (
            session.query(Complaint)
            .filter(Complaint.status == status)
            .order_by(Complaint.complaint_date.desc())
            .all()
        )

        if not complaints:
            return f"No complaints found with status '{status}'."

        records = [c.to_dict() for c in complaints]
        return f"Found {len(records)} complaint(s) with status '{status}': {json.dumps(records, indent=2)}"


@tool(approval_mode="never_require")
def register_complaint(
    customer_id: Annotated[str, Field(description="The customer ID to register a complaint for, e.g. CUST10001.")],
    complaint_description: Annotated[str, Field(description="Free-text description of the IT complaint.")],
    priority: Annotated[
        Optional[str],
        Field(description="Complaint priority: Critical, High, Medium, or Low. Auto-set to High for platinum customers if not specified."),
    ] = None,
    status: Annotated[
        Optional[str],
        Field(description="Initial complaint status (default: Open)."),
    ] = "Open",
) -> str:
    """Register a new IT complaint for a customer. If the customer has a platinum profile and no priority is specified, it defaults to High."""
    valid_priorities = {"Critical", "High", "Medium", "Low"}
    valid_statuses = {"Open", "In Progress", "Resolved", "Closed", "Reopened"}

    if priority and priority not in valid_priorities:
        return f"Error: Invalid priority '{priority}'. Must be one of: {', '.join(sorted(valid_priorities))}."
    if status not in valid_statuses:
        return f"Error: Invalid status '{status}'. Must be one of: {', '.join(sorted(valid_statuses))}."

    with get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Error: Customer with ID {customer_id} not found."

        # Auto-set priority for platinum customers
        if priority is None:
            profile = (
                session.query(CustomerProfilePreference)
                .filter(CustomerProfilePreference.customer_id == customer_id)
                .first()
            )
            if profile and profile.customer_type == "platinum":
                priority = "High"
            else:
                priority = "Medium"

        complaint_id = _next_complaint_id()
        complaint = Complaint(
            complaint_id=complaint_id,
            complaint_date=datetime.now(),
            customer_id=customer_id,
            complaint_description=complaint_description,
            priority=priority,
            status=status,
        )
        session.add(complaint)
        session.commit()

        return f"Complaint registered successfully: {json.dumps(complaint.to_dict(), indent=2)}"
