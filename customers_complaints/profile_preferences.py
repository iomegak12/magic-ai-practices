"""Customer profile preference management."""

import json
from typing import Annotated

from agent_framework import tool
from pydantic import Field

from .database import get_session
from .models import Customer, CustomerProfilePreference


@tool(approval_mode="never_require")
def get_customer_profile(
    customer_id: Annotated[str, Field(description="The customer ID to get profile preferences for, e.g. CUST10001.")]
) -> str:
    """Get the profile preference (platinum/gold/silver/general) for a customer."""
    with get_session() as session:
        customer = session.get(Customer, customer_id)
        if not customer:
            return f"Error: Customer with ID {customer_id} not found."

        profile = (
            session.query(CustomerProfilePreference)
            .filter(CustomerProfilePreference.customer_id == customer_id)
            .first()
        )

        if not profile:
            return f"No profile preference found for customer {customer_id}."

        result = {
            **customer.to_dict(),
            "customer_type": profile.customer_type,
        }
        return json.dumps(result, indent=2)
