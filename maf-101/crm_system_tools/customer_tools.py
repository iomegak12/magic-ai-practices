"""Customer management tools for CRM system."""

import random
from datetime import datetime
from typing import Annotated, Literal, Optional

from agent_framework import tool
from pydantic import Field

# In-memory customer database
CUSTOMERS = {}
CUSTOMER_ID_COUNTER = {"current": 1}


def _initialize_customers():
    """Initialize 10 sample customers from Europe, India, and Australia."""
    if len(CUSTOMERS) > 0:
        return  # Already initialized

    sample_customers = [
        # European customers
        {
            "name": "Hans Mueller",
            "city": "Berlin",
            "email": "hans.mueller@email.de",
            "phone": "+49-30-12345678",
            "active_status": "active",
            "credit_limit": 5000,
        },
        {
            "name": "Sophie Dubois",
            "city": "Paris",
            "email": "sophie.dubois@email.fr",
            "phone": "+33-1-98765432",
            "active_status": "active",
            "credit_limit": 7500,
        },
        {
            "name": "Marco Rossi",
            "city": "Rome",
            "email": "marco.rossi@email.it",
            "phone": "+39-06-55512345",
            "active_status": "inactive",
            "credit_limit": 3000,
        },
        # Indian customers
        {
            "name": "Priya Sharma",
            "city": "Mumbai",
            "email": "priya.sharma@email.in",
            "phone": "+91-22-98765432",
            "active_status": "active",
            "credit_limit": 8000,
        },
        {
            "name": "Rajesh Kumar",
            "city": "Bangalore",
            "email": "rajesh.kumar@email.in",
            "phone": "+91-80-12345678",
            "active_status": "active",
            "credit_limit": 6500,
        },
        {
            "name": "Anjali Patel",
            "city": "Delhi",
            "email": "anjali.patel@email.in",
            "phone": "+91-11-87654321",
            "active_status": "active",
            "credit_limit": 10000,
        },
        {
            "name": "Vikram Singh",
            "city": "Chennai",
            "email": "vikram.singh@email.in",
            "phone": "+91-44-23456789",
            "active_status": "inactive",
            "credit_limit": 4000,
        },
        # Australian customers
        {
            "name": "James Wilson",
            "city": "Sydney",
            "email": "james.wilson@email.au",
            "phone": "+61-2-98765432",
            "active_status": "active",
            "credit_limit": 9000,
        },
        {
            "name": "Emma Thompson",
            "city": "Melbourne",
            "email": "emma.thompson@email.au",
            "phone": "+61-3-12345678",
            "active_status": "active",
            "credit_limit": 7000,
        },
        {
            "name": "Oliver Brown",
            "city": "Brisbane",
            "email": "oliver.brown@email.au",
            "phone": "+61-7-87654321",
            "active_status": "active",
            "credit_limit": 5500,
        },
    ]

    for customer_data in sample_customers:
        customer_id = CUSTOMER_ID_COUNTER["current"]
        CUSTOMERS[customer_id] = {
            "customer_id": customer_id,
            **customer_data,
        }
        CUSTOMER_ID_COUNTER["current"] += 1


# Initialize customers on module load
_initialize_customers()


@tool(approval_mode="never_require")
def create_customer(
    name: Annotated[str, Field(description="Customer name (required).")],
    city: Annotated[str, Field(description="Customer city (required).")],
    email: Annotated[
        Optional[str], Field(description="Customer email address (optional).")
    ] = None,
    phone: Annotated[
        Optional[str], Field(description="Customer phone number (optional).")
    ] = None,
    active_status: Annotated[
        Literal["active", "inactive"],
        Field(description="Customer active status (optional, default: active)."),
    ] = "active",
    credit_limit: Annotated[
        Optional[int],
        Field(
            description="Customer credit limit between $100-$10000 (optional, default: random)."
        ),
    ] = None,
) -> str:
    """Create a new customer record. Name and city are required fields."""
    # Validate credit_limit if provided
    if credit_limit is not None:
        if credit_limit < 100 or credit_limit > 10000:
            return "Error: Credit limit must be between $100 and $10,000."
    else:
        credit_limit = random.randint(100, 10000)

    customer_id = CUSTOMER_ID_COUNTER["current"]
    CUSTOMERS[customer_id] = {
        "customer_id": customer_id,
        "name": name,
        "city": city,
        "email": email,
        "phone": phone,
        "active_status": active_status,
        "credit_limit": credit_limit,
    }
    CUSTOMER_ID_COUNTER["current"] += 1

    return f"Customer created successfully with ID: {customer_id}. Details: {CUSTOMERS[customer_id]}"


@tool(approval_mode="never_require")
def get_customer_by_id(
    customer_id: Annotated[int, Field(description="The customer ID to retrieve.")]
) -> str:
    """Get a customer record by customer ID."""
    if customer_id not in CUSTOMERS:
        return f"Error: Customer with ID {customer_id} not found."

    customer = CUSTOMERS[customer_id]
    return f"Customer found: {customer}"


@tool(approval_mode="never_require")
def get_all_customers() -> str:
    """Get all customer records in the system."""
    if not CUSTOMERS:
        return "No customers found in the system."

    customer_list = []
    for customer in CUSTOMERS.values():
        customer_list.append(customer)

    return f"Total customers: {len(customer_list)}. Records: {customer_list}"


@tool(approval_mode="never_require")
def search_customers(
    name: Annotated[
        Optional[str], Field(description="Search by customer name (partial match).")
    ] = None,
    email: Annotated[
        Optional[str], Field(description="Search by email (partial match).")
    ] = None,
    city: Annotated[
        Optional[str], Field(description="Search by city (partial match).")
    ] = None,
) -> str:
    """Search customer records by name, email, or city using partial case-insensitive matching."""
    if not name and not email and not city:
        return "Error: At least one search parameter (name, email, or city) must be provided."

    results = []
    for customer in CUSTOMERS.values():
        match = True

        if name:
            if name.lower() not in (customer.get("name") or "").lower():
                match = False

        if email:
            if email.lower() not in (customer.get("email") or "").lower():
                match = False

        if city:
            if city.lower() not in (customer.get("city") or "").lower():
                match = False

        if match:
            results.append(customer)

    if not results:
        return "No customers found matching the search criteria."

    return f"Found {len(results)} customer(s): {results}"


@tool(approval_mode="never_require")
def get_customer_statistics() -> str:
    """Get overall customer statistics including total customers, active/inactive counts, total credit limits, and total revenue."""
    from .order_tools import ORDERS

    if not CUSTOMERS:
        return "No customer data available."

    total_customers = len(CUSTOMERS)
    active_count = sum(
        1 for c in CUSTOMERS.values() if c.get("active_status") == "active"
    )
    inactive_count = total_customers - active_count
    total_credit_limit = sum(c.get("credit_limit", 0) for c in CUSTOMERS.values())
    avg_credit_limit = total_credit_limit / total_customers if total_customers > 0 else 0

    # Calculate total revenue from all orders
    total_revenue = sum(order.get("order_amount", 0) for order in ORDERS.values())

    stats = {
        "total_customers": total_customers,
        "active_customers": active_count,
        "inactive_customers": inactive_count,
        "total_credit_limit": f"${total_credit_limit:,}",
        "average_credit_limit": f"${avg_credit_limit:,.2f}",
        "total_revenue": f"${total_revenue:,}",
    }

    return f"Customer Statistics: {stats}"
