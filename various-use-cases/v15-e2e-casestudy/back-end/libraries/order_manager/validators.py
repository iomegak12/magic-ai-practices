"""
Validation functions for the Order Manager library.

This module provides validation and sanitization functions for order data.
"""

from datetime import datetime
from typing import Any
from .config import Config
from .exceptions import ValidationException


def validate_quantity(quantity: int) -> bool:
    """
    Validate order quantity.
    
    Args:
        quantity: The quantity to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If quantity is invalid
    """
    if not isinstance(quantity, int):
        raise ValidationException("quantity", "Quantity must be an integer")
    
    if quantity < Config.MIN_QUANTITY:
        raise ValidationException("quantity", "Quantity must be a positive integer")
    
    return True


def validate_order_amount(amount: int) -> bool:
    """
    Validate order amount.
    
    Args:
        amount: The amount to validate (in cents)
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If amount is invalid
    """
    if not isinstance(amount, int):
        raise ValidationException("order_amount", "Order amount must be an integer")
    
    if amount < Config.MIN_ORDER_AMOUNT:
        raise ValidationException("order_amount", "Order amount must be a positive integer")
    
    return True


def validate_order_status(status: str) -> bool:
    """
    Validate order status.
    
    Args:
        status: The status to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If status is invalid
    """
    if not isinstance(status, str):
        raise ValidationException("order_status", "Order status must be a string")
    
    if status not in Config.VALID_STATUSES:
        valid_statuses = ", ".join(Config.VALID_STATUSES)
        raise ValidationException(
            "order_status",
            f"Invalid order status. Must be one of: {valid_statuses}"
        )
    
    return True


def validate_customer_name(name: str) -> bool:
    """
    Validate customer name.
    
    Args:
        name: The customer name to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If name is invalid
    """
    if not isinstance(name, str):
        raise ValidationException("customer_name", "Customer name must be a string")
    
    if not name or not name.strip():
        raise ValidationException("customer_name", "Customer name is required")
    
    if len(name) > Config.MAX_CUSTOMER_NAME_LENGTH:
        raise ValidationException(
            "customer_name",
            f"Customer name must be <= {Config.MAX_CUSTOMER_NAME_LENGTH} characters"
        )
    
    return True


def validate_product_sku(sku: str) -> bool:
    """
    Validate product SKU.
    
    Args:
        sku: The product SKU to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If SKU is invalid
    """
    if not isinstance(sku, str):
        raise ValidationException("product_sku", "Product SKU must be a string")
    
    if not sku or not sku.strip():
        raise ValidationException("product_sku", "Product SKU is required")
    
    if len(sku) > Config.MAX_PRODUCT_SKU_LENGTH:
        raise ValidationException(
            "product_sku",
            f"Product SKU must be <= {Config.MAX_PRODUCT_SKU_LENGTH} characters"
        )
    
    return True


def validate_billing_address(address: str) -> bool:
    """
    Validate billing address.
    
    Args:
        address: The billing address to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If address is invalid
    """
    if not isinstance(address, str):
        raise ValidationException("billing_address", "Billing address must be a string")
    
    if not address or not address.strip():
        raise ValidationException("billing_address", "Billing address is required")
    
    return True


def validate_order_date(order_date: datetime) -> bool:
    """
    Validate order date.
    
    Args:
        order_date: The order date to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationException: If date is invalid
    """
    if not isinstance(order_date, datetime):
        raise ValidationException("order_date", "Order date must be a valid datetime object")
    
    # Check if date is not more than 1 year in the future
    from datetime import timedelta
    max_future_date = datetime.now() + timedelta(days=365)
    if order_date > max_future_date:
        raise ValidationException(
            "order_date",
            "Order date cannot be more than 1 year in the future"
        )
    
    return True


def validate_required_fields(**kwargs: Any) -> bool:
    """
    Validate that all required fields are present.
    
    Args:
        **kwargs: Field name and value pairs
        
    Returns:
        True if all required fields are valid
        
    Raises:
        ValidationException: If any required field is missing or invalid
    """
    required_fields = [
        'order_date', 'customer_name', 'billing_address',
        'product_sku', 'quantity', 'order_amount', 'order_status'
    ]
    
    for field in required_fields:
        if field not in kwargs:
            raise ValidationException(field, f"{field} is required")
        
        value = kwargs[field]
        if value is None:
            raise ValidationException(field, f"{field} cannot be None")
    
    return True


def sanitize_customer_name(name: str) -> str:
    """
    Sanitize customer name by trimming whitespace.
    
    Args:
        name: The customer name to sanitize
        
    Returns:
        Sanitized customer name
    """
    if isinstance(name, str):
        return name.strip()
    return name


def sanitize_product_sku(sku: str) -> str:
    """
    Sanitize product SKU by trimming whitespace and converting to uppercase.
    
    Args:
        sku: The product SKU to sanitize
        
    Returns:
        Sanitized product SKU
    """
    if isinstance(sku, str):
        return sku.strip().upper()
    return sku
