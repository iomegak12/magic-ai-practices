"""
Order Management Library

A Python library for managing customer orders with SQLAlchemy ORM and SQLite.

Features:
- Create, retrieve, search, and update customer orders
- SQLAlchemy ORM with SQLite database
- Configurable database path via .env
- Comprehensive validation
- Case-insensitive partial matching for searches

Usage:
    from order_management import (
        init_db,
        create_order,
        get_order_by_id,
        get_orders_by_customer,
        search_orders,
        update_order_status
    )
    
    # Initialize the database
    init_db()
    
    # Create an order
    order = create_order(
        customer_name="John Doe",
        billing_address="123 Main St, City, State",
        product_sku="SKU-001",
        quantity=2,
        order_amount=99.99,
        remarks="Express delivery"
    )
"""

__version__ = "1.0.0"

# Database initialization and configuration
from .database import (
    init_db,
    get_db_session,
    get_database_path
)

# Operations
from .operations import (
    create_order,
    get_order_by_id,
    get_orders_by_customer,
    search_orders,
    update_order_status,
    get_all_orders
)

# Models
from .models import Order

# Exceptions
from .exceptions import (
    OrderManagementError,
    ValidationError,
    OrderNotFoundError,
    DatabaseError
)

# Validation constants
from .validations import VALID_ORDER_STATUSES

# Public API
__all__ = [
    # Database
    "init_db",
    "get_db_session",
    "get_database_path",
    
    # Operations
    "create_order",
    "get_order_by_id",
    "get_orders_by_customer",
    "search_orders",
    "update_order_status",
    "get_all_orders",
    
    # Models
    "Order",
    
    # Exceptions
    "OrderManagementError",
    "ValidationError",
    "OrderNotFoundError",
    "DatabaseError",
    
    # Constants
    "VALID_ORDER_STATUSES",
]
