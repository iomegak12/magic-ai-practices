"""Order management tools for CRM system."""

import random
import string
from datetime import datetime, timedelta
from typing import Annotated, Optional

from agent_framework import tool
from pydantic import Field

# In-memory order database
ORDERS = {}
ORDER_ID_COUNTER = {"current": 1}


def _generate_product_sku() -> str:
    """Generate a random 10-character alphanumeric SKU."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


def _initialize_orders():
    """Initialize 5 sample orders for each of the 10 customers (50 total orders)."""
    from .customer_tools import CUSTOMERS

    if len(ORDERS) > 0:
        return  # Already initialized

    # Date range: last 2 months (Dec 17, 2025 to Feb 17, 2026)
    end_date = datetime(2026, 2, 17)
    start_date = end_date - timedelta(days=60)

    cities = ["Berlin", "Paris", "Rome", "Mumbai", "Bangalore", "Delhi", "Chennai", "Sydney", "Melbourne", "Brisbane"]
    remarks_options = [
        "Standard order",
        "Rush delivery requested",
        "Gift wrapping required",
        "Bulk order discount applied",
        "Regular customer",
        "First-time customer",
        "Seasonal promotion",
        "Corporate order",
        "Express shipping",
        "Customer requested specific delivery date",
    ]

    for customer_id in CUSTOMERS.keys():
        # Generate 5 orders per customer
        for _ in range(5):
            order_id = ORDER_ID_COUNTER["current"]
            # Random date within the last 2 months
            random_days = random.randint(0, 60)
            order_date = start_date + timedelta(days=random_days)

            ORDERS[order_id] = {
                "order_id": order_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "customer_id": customer_id,
                "billing_address": random.choice(cities),
                "product_sku": _generate_product_sku(),
                "quantity": random.randint(1, 100),
                "order_amount": random.randint(50, 5000),
                "remarks": random.choice(remarks_options),
            }
            ORDER_ID_COUNTER["current"] += 1


# Initialize orders on module load
_initialize_orders()


@tool(approval_mode="never_require")
def create_order(
    customer_id: Annotated[int, Field(description="Customer ID for the order.")],
    billing_address: Annotated[str, Field(description="Billing address (city name).")],
    product_sku: Annotated[
        Optional[str],
        Field(description="Product SKU (optional, auto-generated if not provided)."),
    ] = None,
    quantity: Annotated[int, Field(description="Order quantity.")] = 1,
    order_amount: Annotated[int, Field(description="Order amount in dollars.")] = 0,
    remarks: Annotated[Optional[str], Field(description="Order remarks (optional).")] = None,
) -> str:
    """Create a new order record for a customer. Validates customer existence."""
    from .customer_tools import CUSTOMERS

    # Validate customer exists
    if customer_id not in CUSTOMERS:
        return f"Error: Customer with ID {customer_id} does not exist. Please create the customer first."

    order_id = ORDER_ID_COUNTER["current"]
    order_date = datetime.now().strftime("%Y-%m-%d")

    # Auto-generate SKU if not provided
    if product_sku is None:
        product_sku = _generate_product_sku()

    ORDERS[order_id] = {
        "order_id": order_id,
        "order_date": order_date,
        "customer_id": customer_id,
        "billing_address": billing_address,
        "product_sku": product_sku,
        "quantity": quantity,
        "order_amount": order_amount,
        "remarks": remarks,
    }
    ORDER_ID_COUNTER["current"] += 1

    return f"Order created successfully with ID: {order_id}. Details: {ORDERS[order_id]}"


@tool(approval_mode="never_require")
def get_orders_by_customer(
    customer_id: Annotated[int, Field(description="Customer ID to get orders for.")]
) -> str:
    """Get all orders for a specific customer."""
    from .customer_tools import CUSTOMERS

    # Validate customer exists
    if customer_id not in CUSTOMERS:
        return f"Error: Customer with ID {customer_id} does not exist."

    customer_orders = [
        order for order in ORDERS.values() if order.get("customer_id") == customer_id
    ]

    if not customer_orders:
        return f"No orders found for customer ID {customer_id}."

    return f"Found {len(customer_orders)} order(s) for customer {customer_id}: {customer_orders}"


@tool(approval_mode="never_require")
def get_order_statistics(
    customer_id: Annotated[int, Field(description="Customer ID to get order statistics for.")]
) -> str:
    """Get order statistics for a specific customer including total orders, total amount spent, average order value, and date range."""
    from .customer_tools import CUSTOMERS

    # Validate customer exists
    if customer_id not in CUSTOMERS:
        return f"Error: Customer with ID {customer_id} does not exist."

    customer_orders = [
        order for order in ORDERS.values() if order.get("customer_id") == customer_id
    ]

    if not customer_orders:
        return f"No orders found for customer ID {customer_id}."

    total_orders = len(customer_orders)
    total_amount = sum(order.get("order_amount", 0) for order in customer_orders)
    avg_order_value = total_amount / total_orders if total_orders > 0 else 0
    total_quantity = sum(order.get("quantity", 0) for order in customer_orders)

    # Get date range
    order_dates = [
        datetime.strptime(order.get("order_date"), "%Y-%m-%d")
        for order in customer_orders
    ]
    first_order_date = min(order_dates).strftime("%Y-%m-%d")
    last_order_date = max(order_dates).strftime("%Y-%m-%d")

    customer_name = CUSTOMERS[customer_id].get("name")

    stats = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "total_orders": total_orders,
        "total_amount_spent": f"${total_amount:,}",
        "average_order_value": f"${avg_order_value:,.2f}",
        "total_quantity_ordered": total_quantity,
        "first_order_date": first_order_date,
        "last_order_date": last_order_date,
    }

    return f"Order Statistics for {customer_name} (ID: {customer_id}): {stats}"
