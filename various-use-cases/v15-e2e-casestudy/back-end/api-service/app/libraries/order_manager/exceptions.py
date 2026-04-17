"""
Custom exceptions for the Order Manager library.

This module defines specific exceptions for different error scenarios
in order management operations.
"""


class OrderManagerException(Exception):
    """Base exception for all Order Manager related errors."""
    pass


class OrderNotFoundException(OrderManagerException):
    """Raised when an order with the specified ID is not found."""
    
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} not found")


class InvalidOrderDataException(OrderManagerException):
    """Raised when order data fails validation."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DatabaseException(OrderManagerException):
    """Raised when a database operation fails."""
    
    def __init__(self, message: str, original_exception: Exception = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(message)


class ValidationException(OrderManagerException):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")
