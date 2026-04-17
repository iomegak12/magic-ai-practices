"""Customer management tools."""

import json
from typing import Annotated, Optional

from agent_framework import tool
from pydantic import Field
from sqlalchemy import func

from .database import get_session
from .models import Customer


def _next_customer_id() -> str:
    """Generate the next customer ID (CUST10001, CUST10002, ...)."""
    with get_session() as session:
        last = (
            session.query(Customer.customer_id)
            .order_by(Customer.customer_id.desc())
            .first()
        )
        if last:
            num = int(last[0].replace("CUST", "")) + 1
        else:
            num = 10001
        return f"CUST{num}"


@tool(approval_mode="never_require")
def get_customer_by_id(
    customer_id: Annotated[str, Field(description="The customer ID to retrieve, e.g. CUST10001.")]
) -> str:
    """Get a customer record by customer ID."""
    with get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Error: Customer with ID {customer_id} not found."
        return json.dumps(customer.to_dict(), indent=2)


@tool(approval_mode="never_require")
def search_customers(
    name: Annotated[
        Optional[str], Field(description="Search by customer name (partial match, case insensitive).")
    ] = None,
    address: Annotated[
        Optional[str], Field(description="Search by address (partial match, case insensitive).")
    ] = None,
    email: Annotated[
        Optional[str], Field(description="Search by email (partial match, case insensitive).")
    ] = None,
) -> str:
    """Search customer records by name, address, or email using partial case-insensitive matching."""
    if not name and not address and not email:
        return "Error: At least one search parameter (name, address, or email) must be provided."

    with get_session() as session:
        query = session.query(Customer)

        if name:
            query = query.filter(Customer.customer_name.ilike(f"%{name}%"))
        if address:
            query = query.filter(Customer.address.ilike(f"%{address}%"))
        if email:
            query = query.filter(Customer.email.ilike(f"%{email}%"))

        results = query.all()

        if not results:
            return "No customers found matching the search criteria."

        records = [c.to_dict() for c in results]
        return f"Found {len(records)} customer(s): {json.dumps(records, indent=2)}"
