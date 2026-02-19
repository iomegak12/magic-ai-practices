"""
Validation logic for order management system.
"""
from datetime import datetime
from .exceptions import ValidationError

# Valid order statuses
VALID_ORDER_STATUSES = [
    "PENDING",
    "CONFIRMED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED"
]


def validate_order_data(order_data, is_update=False):
    """
    Validate order data before creating or updating an order.
    
    Args:
        order_data: Dictionary containing order data
        is_update: Boolean indicating if this is an update operation
        
    Raises:
        ValidationError: If validation fails
    """
    errors = []
    
    # Required fields for creation
    if not is_update:
        required_fields = ["customer_name", "product_sku", "quantity"]
        for field in required_fields:
            if field not in order_data or not order_data[field]:
                errors.append(f"{field} is required")
    
    # Validate customer_name if provided
    if "customer_name" in order_data:
        if not isinstance(order_data["customer_name"], str):
            errors.append("customer_name must be a string")
        elif not order_data["customer_name"].strip():
            errors.append("customer_name cannot be empty")
        elif len(order_data["customer_name"]) > 255:
            errors.append("customer_name cannot exceed 255 characters")
    
    # Validate billing_address if provided
    if "billing_address" in order_data:
        if not isinstance(order_data["billing_address"], str):
            errors.append("billing_address must be a string")
        elif len(order_data["billing_address"]) > 500:
            errors.append("billing_address cannot exceed 500 characters")
    
    # Validate product_sku if provided
    if "product_sku" in order_data:
        if not isinstance(order_data["product_sku"], str):
            errors.append("product_sku must be a string")
        elif not order_data["product_sku"].strip():
            errors.append("product_sku cannot be empty")
        elif len(order_data["product_sku"]) > 100:
            errors.append("product_sku cannot exceed 100 characters")
    
    # Validate quantity if provided
    if "quantity" in order_data:
        if not isinstance(order_data["quantity"], (int, float)):
            errors.append("quantity must be a number")
        elif order_data["quantity"] <= 0:
            errors.append("quantity must be positive")
    
    # Validate order_amount if provided
    if "order_amount" in order_data:
        if not isinstance(order_data["order_amount"], (int, float)):
            errors.append("order_amount must be a number")
        elif order_data["order_amount"] <= 0:
            errors.append("order_amount must be positive")
    
    # Validate remarks if provided
    if "remarks" in order_data and order_data["remarks"] is not None:
        if not isinstance(order_data["remarks"], str):
            errors.append("remarks must be a string")
        elif len(order_data["remarks"]) > 1000:
            errors.append("remarks cannot exceed 1000 characters")
    
    # Validate order_status if provided
    if "order_status" in order_data:
        if not isinstance(order_data["order_status"], str):
            errors.append("order_status must be a string")
        elif order_data["order_status"].upper() not in VALID_ORDER_STATUSES:
            errors.append(f"order_status must be one of: {', '.join(VALID_ORDER_STATUSES)}")
    
    # Validate order_date if provided
    if "order_date" in order_data and order_data["order_date"] is not None:
        if isinstance(order_data["order_date"], str):
            try:
                datetime.fromisoformat(order_data["order_date"])
            except ValueError:
                errors.append("order_date must be in valid ISO format")
        elif not isinstance(order_data["order_date"], datetime):
            errors.append("order_date must be a datetime object or ISO format string")
    
    if errors:
        raise ValidationError("; ".join(errors))


def validate_order_status(status):
    """
    Validate an order status value.
    
    Args:
        status: Status string to validate
        
    Raises:
        ValidationError: If status is invalid
    """
    if not isinstance(status, str):
        raise ValidationError("order_status must be a string")
    
    if status.upper() not in VALID_ORDER_STATUSES:
        raise ValidationError(f"order_status must be one of: {', '.join(VALID_ORDER_STATUSES)}")
