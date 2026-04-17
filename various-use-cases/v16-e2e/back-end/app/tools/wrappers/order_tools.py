"""
Order management tools for AI agent.

These tools wrap the order_management library operations
and expose them to the agent framework using the @tool decorator.
"""
from agent_framework import tool
from typing import Optional
from datetime import datetime

# Import order management operations
from ..order_management import (
    create_order,
    get_order_by_id,
    get_orders_by_customer,
    search_orders,
    update_order_status,
    get_all_orders,
    OrderNotFoundError,
    ValidationError,
    DatabaseError
)


@tool
def create_new_order(
    order_date: str,
    customer_name: str,
    billing_address: str,
    product_sku: str,
    quantity: int,
    order_amount: float,
    remarks: Optional[str] = None
) -> dict:
    """
    Create a new order in the system.
    
    Args:
        order_date: Order date in YYYY-MM-DD format (e.g., "2024-01-15")
        customer_name: Customer's full name
        billing_address: Customer's billing address
        product_sku: Product SKU/code
        quantity: Order quantity (must be positive)
        order_amount: Total order amount (must be non-negative)
        remarks: Optional order remarks or notes
        
    Returns:
        dict: Created order details including order_id and order_status
        
    Example:
        ```
        result = create_new_order(
            order_date="2024-01-15",
            customer_name="John Doe",
            billing_address="123 Main St, City, State, ZIP",
            product_sku="PROD-001",
            quantity=2,
            order_amount=99.99,
            remarks="Express delivery requested"
        )
        ```
    """
    try:
        # Parse order_date string to datetime object
        order_date_obj = None
        if order_date:
            try:
                order_date_obj = datetime.strptime(order_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "status": "error",
                    "error": f"Invalid date format: {order_date}. Expected YYYY-MM-DD format.",
                    "error_type": "ValidationError"
                }
        
        return create_order(
            customer_name=customer_name,
            billing_address=billing_address,
            product_sku=product_sku,
            quantity=quantity,
            order_amount=order_amount,
            remarks=remarks,
            order_date=order_date_obj
        )
    except (ValidationError, DatabaseError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def get_order(order_id: str) -> dict:
    """
    Retrieve a specific order by its ID.
    
    Args:
        order_id: Unique order identifier
        
    Returns:
        dict: Order details if found
        
    Example:
        ```
        result = get_order(order_id="ORD-20240115-ABC123")
        ```
    """
    try:
        return get_order_by_id(order_id)
    except OrderNotFoundError as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": "OrderNotFoundError"
        }
    except DatabaseError as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": "DatabaseError"
        }


@tool
def get_customer_orders(customer_name: str) -> dict:
    """
    Retrieve all orders for a specific customer.
    Orders are returned sorted by order date (newest first).
    
    Args:
        customer_name: Customer's name (case-insensitive, partial match)
        
    Returns:
        dict: List of orders for the customer
        
    Example:
        ```
        result = get_customer_orders(customer_name="John Doe")
        ```
    """
    try:
        orders = get_orders_by_customer(customer_name)
        return {
            "status": "success",
            "customer_name": customer_name,
            "order_count": len(orders),
            "orders": orders
        }
    except DatabaseError as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": "DatabaseError"
        }


@tool
def find_orders(
    product_sku: Optional[str] = None,
    billing_address: Optional[str] = None,
    order_status: Optional[str] = None
) -> dict:
    """
    Search for orders using multiple criteria.
    All criteria are optional - use at least one for meaningful results.
    
    Args:
        product_sku: Product SKU to search for (partial match, case-insensitive)
        billing_address: Billing address to search for (partial match, case-insensitive)
        order_status: Exact order status (PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED)
        
    Returns:
        dict: List of matching orders
        
    Example:
        ```
        # Find all pending orders
        result = find_orders(order_status="PENDING")
        
        # Find orders for a specific product
        result = find_orders(product_sku="PROD-001")
        
        # Find shipped orders in California
        result = find_orders(billing_address="California", order_status="SHIPPED")
        ```
    """
    try:
        orders = search_orders(
            product_sku=product_sku,
            billing_address=billing_address,
            order_status=order_status
        )
        return {
            "status": "success",
            "match_count": len(orders),
            "search_criteria": {
                "product_sku": product_sku,
                "billing_address": billing_address,
                "order_status": order_status
            },
            "orders": orders
        }
    except (ValidationError, DatabaseError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def update_order(order_id: str, new_status: str) -> dict:
    """
    Update the status of an existing order.
    
    Args:
        order_id: Unique order identifier
        new_status: New order status (must be: PENDING, CONFIRMED, SHIPPED, DELIVERED, or CANCELLED)
        
    Returns:
        dict: Updated order details
        
    Example:
        ```
        result = update_order(
            order_id="ORD-20240115-ABC123",
            new_status="SHIPPED"
        )
        ```
    """
    try:
        return update_order_status(order_id, new_status)
    except (OrderNotFoundError, ValidationError, DatabaseError) as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }


@tool
def list_all_orders(limit: Optional[int] = None) -> dict:
    """
    Retrieve all orders from the system.
    Orders are returned sorted by order date (newest first).
    
    Args:
        limit: Optional maximum number of orders to return (default: all orders)
        
    Returns:
        dict: List of all orders
        
    Example:
        ```
        # Get all orders
        result = list_all_orders()
        
        # Get 10 most recent orders
        result = list_all_orders(limit=10)
        ```
    """
    try:
        orders = get_all_orders(limit=limit)
        return {
            "status": "success",
            "order_count": len(orders),
            "limit_applied": limit if limit else "none",
            "orders": orders
        }
    except DatabaseError as e:
        return {
            "status": "error",
            "error": str(e),
            "error_type": "DatabaseError"
        }


# Export all tools
__all__ = [
    "create_new_order",
    "get_order",
    "get_customer_orders",
    "find_orders",
    "update_order",
    "list_all_orders"
]
