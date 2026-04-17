"""
Tool wrappers for AI agent.

This package exports all tool wrappers that wrap library operations
and expose them to the agent framework.
"""

from .order_tools import (
    create_new_order,
    get_order,
    get_customer_orders,
    find_orders,
    update_order,
    list_all_orders
)

from .email_tools import (
    send_simple_email,
    send_formatted_email,
    send_email_with_files,
    send_complete_email,
    test_email_connection
)

# Export all tools
__all__ = [
    # Order tools (6)
    "create_new_order",
    "get_order",
    "get_customer_orders",
    "find_orders",
    "update_order",
    "list_all_orders",
    
    # Email tools (5)
    "send_simple_email",
    "send_formatted_email",
    "send_email_with_files",
    "send_complete_email",
    "test_email_connection",
]
