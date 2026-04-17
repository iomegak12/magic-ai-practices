"""
Custom exceptions for order management system.
"""


class OrderManagementError(Exception):
    """Base exception for order management system."""
    pass


class ValidationError(OrderManagementError):
    """Raised when validation fails."""
    pass


class OrderNotFoundError(OrderManagementError):
    """Raised when an order is not found."""
    pass


class DatabaseError(OrderManagementError):
    """Raised when a database operation fails."""
    pass
