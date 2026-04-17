"""
Order Manager Library

A Python library for managing customer orders with SQLite database backend.

Example:
    from order_manager import OrderManager
    
    manager = OrderManager(db_path="data/orders.db")
    order = manager.create_order(
        order_date=datetime.now(),
        customer_name="John Smith",
        billing_address="123 Main St, Sydney, NSW",
        product_sku="LAPTOP-001",
        quantity=2,
        order_amount=299900
    )
"""

__version__ = "1.0.0"
__author__ = "Your Team"
__description__ = "Python library for managing customer orders"

# Import main classes and exceptions for public API
from .manager import OrderManager
from .models import Order
from .config import Config
from .exceptions import (
    OrderManagerException,
    OrderNotFoundException,
    InvalidOrderDataException,
    DatabaseException,
    ValidationException
)

# Define public API
__all__ = [
    # Main class
    "OrderManager",
    
    # Models
    "Order",
    
    # Configuration
    "Config",
    
    # Exceptions
    "OrderManagerException",
    "OrderNotFoundException",
    "InvalidOrderDataException",
    "DatabaseException",
    "ValidationException",
    
    # Version info
    "__version__",
]
