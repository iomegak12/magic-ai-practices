"""
Configuration constants for the Order Manager library.

This module contains only constants and default values.
Environment configuration is managed by the consuming application.
"""

from typing import List


class Config:
    """Configuration constants for the library."""
    
    # Valid order status values
    VALID_STATUSES: List[str] = [
        "Pending",
        "Processing",
        "Confirmed",
        "Shipped",
        "Delivered",
        "Cancelled",
        "Returned"
    ]
    
    # Default database path (can be overridden by application)
    DEFAULT_DB_PATH: str = "orders.db"
    
    # Validation constraints
    MAX_CUSTOMER_NAME_LENGTH: int = 255
    MAX_PRODUCT_SKU_LENGTH: int = 100
    MIN_QUANTITY: int = 1
    MIN_ORDER_AMOUNT: int = 1
