"""
Order Management Tools for MAF Agent

Wraps the order_manager library into MAF-compatible tools.
These tools provide the agent with order management capabilities.
"""
from agent_framework import tool
from typing import Annotated, Optional
from pydantic import Field
from datetime import datetime

# Import order_manager from local libraries
from app.libraries.order_manager import (
    OrderManager,
    OrderNotFoundException,
    InvalidOrderDataException,
    ValidationException
)

# Global OrderManager instance
_order_manager: Optional[OrderManager] = None


def initialize_order_manager(db_path: str):
    """
    Initialize the OrderManager with the specified database path.
    Must be called before using any tools.
    """
    global _order_manager
    _order_manager = OrderManager(db_path=db_path)
    print(f"✅ OrderManager initialized with database: {db_path}")


@tool(approval_mode="never_require")
def create_customer_order(
    customer_name: Annotated[str, Field(description="Full name of the customer")],
    billing_address: Annotated[str, Field(description="Customer's billing address")],
    product_sku: Annotated[str, Field(description="Product SKU/code")],
    quantity: Annotated[int, Field(description="Order quantity, must be positive")],
    order_amount: Annotated[int, Field(description="Total order amount in cents (e.g., 299900 for $2999.00)")],
    remarks: Annotated[Optional[str], Field(description="Optional notes or comments")] = None
) -> str:
    """
    Create a new customer order in the order management system.
    This tool creates orders with 'Pending' status by default.
    """
    try:
        order = _order_manager.create_order(
            order_date=datetime.now(),
            customer_name=customer_name,
            billing_address=billing_address,
            product_sku=product_sku,
            quantity=quantity,
            order_amount=order_amount,
            order_status="Pending",
            remarks=remarks
        )
        return f"✅ Order created successfully.\n\nOrder Details:\n- Order ID: {order.order_id}\n- Customer: {order.customer_name}\n- Product: {order.product_sku}\n- Quantity: {order.quantity}\n- Amount: ${order.order_amount / 100:.2f}\n- Status: {order.order_status}\n- Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}"
    except (InvalidOrderDataException, ValidationException) as e:
        return f"❌ Order creation failed: {str(e)}"
    except Exception as e:
        return f"❌ An unexpected error occurred: {str(e)}"


@tool(approval_mode="never_require")
def get_customer_orders(
    customer_name: Annotated[str, Field(description="Exact customer name to search for")]
) -> str:
    """
    Retrieve all orders for a specific customer (exact name match).
    Returns complete order history for the customer.
    """
    try:
        orders = _order_manager.get_orders_by_customer(customer_name)
        
        if not orders:
            return f"No orders found for customer: {customer_name}"
        
        result = f"📦 Found {len(orders)} order(s) for {customer_name}:\n\n"
        for order in orders:
            result += f"Order ID: {order.order_id}\n"
            result += f"  Product: {order.product_sku}\n"
            result += f"  Quantity: {order.quantity}\n"
            result += f"  Amount: ${order.order_amount / 100:.2f}\n"
            result += f"  Status: {order.order_status}\n"
            result += f"  Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            if order.remarks:
                result += f"  Remarks: {order.remarks}\n"
            result += "\n"
        
        return result
    except Exception as e:
        return f"❌ Error retrieving orders: {str(e)}"


@tool(approval_mode="never_require")
def get_order_details(
    order_id: Annotated[int, Field(description="The order ID to retrieve")]
) -> str:
    """
    Get detailed information about a specific order by its ID.
    """
    try:
        order = _order_manager.get_order_by_id(order_id)
        
        result = f"📋 Order Details (ID: {order.order_id}):\n\n"
        result += f"Customer: {order.customer_name}\n"
        result += f"Billing Address: {order.billing_address}\n"
        result += f"Product SKU: {order.product_sku}\n"
        result += f"Quantity: {order.quantity}\n"
        result += f"Amount: ${order.order_amount / 100:.2f}\n"
        result += f"Status: {order.order_status}\n"
        result += f"Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if order.remarks:
            result += f"Remarks: {order.remarks}\n"
        result += f"\nCreated: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Last Updated: {order.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        
        return result
    except OrderNotFoundException as e:
        return f"❌ {str(e)}"
    except Exception as e:
        return f"❌ Error retrieving order: {str(e)}"


@tool(approval_mode="never_require")
def search_orders_by_customer_name(
    customer_name_partial: Annotated[str, Field(description="Partial customer name to search (case-insensitive)")]
) -> str:
    """
    Search for orders using partial customer name match.
    This is useful when you don't know the exact customer name.
    """
    try:
        orders = _order_manager.search_orders_by_customer(customer_name_partial)
        
        if not orders:
            return f"No orders found matching: {customer_name_partial}"
        
        result = f"🔍 Found {len(orders)} order(s) matching '{customer_name_partial}':\n\n"
        for order in orders:
            result += f"Order ID: {order.order_id} | Customer: {order.customer_name} | Product: {order.product_sku} | Status: {order.order_status}\n"
        
        return result
    except Exception as e:
        return f"❌ Error searching orders: {str(e)}"


@tool(approval_mode="never_require")
def update_order_status(
    order_id: Annotated[int, Field(description="The order ID to update")],
    new_status: Annotated[str, Field(description="New status - must be one of: Pending, Processing, Confirmed, Shipped, Delivered, Cancelled, Returned")]
) -> str:
    """
    Update the status of an existing order.
    Valid statuses: Pending, Processing, Confirmed, Shipped, Delivered, Cancelled, Returned
    """
    try:
        order = _order_manager.update_order_status(order_id, new_status)
        return f"✅ Order {order_id} status updated to: {order.order_status}\n\nUpdated at: {order.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
    except OrderNotFoundException as e:
        return f"❌ {str(e)}"
    except ValidationException as e:
        from order_manager import Config
        return f"❌ {str(e)}\n\nValid statuses: {', '.join(Config.VALID_STATUSES)}"
    except Exception as e:
        return f"❌ Error updating order: {str(e)}"


@tool(approval_mode="never_require")
def search_orders_advanced(
    order_status: Annotated[Optional[str], Field(description="Filter by order status")] = None,
    product_sku: Annotated[Optional[str], Field(description="Filter by product SKU")] = None,
    billing_address_partial: Annotated[Optional[str], Field(description="Filter by partial billing address")] = None
) -> str:
    """
    Advanced search for orders with multiple filter options.
    You can filter by status, product SKU, or billing address (partial match).
    Multiple filters are combined with AND logic.
    """
    try:
        orders = _order_manager.search_orders(
            order_status=order_status,
            product_sku=product_sku,
            billing_address_partial=billing_address_partial
        )
        
        if not orders:
            return "No orders found matching the search criteria."
        
        filters = []
        if order_status:
            filters.append(f"Status: {order_status}")
        if product_sku:
            filters.append(f"SKU: {product_sku}")
        if billing_address_partial:
            filters.append(f"Address contains: {billing_address_partial}")
        
        result = f"🔍 Found {len(orders)} order(s) matching criteria ({', '.join(filters)}):\n\n"
        for order in orders:
            result += f"Order ID: {order.order_id} | Customer: {order.customer_name} | Product: {order.product_sku} | Status: {order.order_status} | Amount: ${order.order_amount / 100:.2f}\n"
        
        return result
    except Exception as e:
        return f"❌ Error searching orders: {str(e)}"


def get_all_order_tools():
    """
    Returns a list of all order management tools.
    Used when creating the MAF agent.
    """
    return [
        create_customer_order,
        get_customer_orders,
        get_order_details,
        search_orders_by_customer_name,
        update_order_status,
        search_orders_advanced
    ]
