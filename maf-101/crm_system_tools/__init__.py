"""CRM System Tools for Customer and Order Management."""

from .customer_tools import (
    create_customer,
    get_customer_by_id,
    get_all_customers,
    search_customers,
    get_customer_statistics,
)
from .order_tools import (
    create_order,
    get_orders_by_customer,
    get_order_statistics,
)

__all__ = [
    "create_customer",
    "get_customer_by_id",
    "get_all_customers",
    "search_customers",
    "get_customer_statistics",
    "create_order",
    "get_orders_by_customer",
    "get_order_statistics",
]
