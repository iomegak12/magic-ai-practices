"""
CRUD operations for order management system.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from .database import get_db_session
from .models import Order
from .validations import validate_order_data, validate_order_status, VALID_ORDER_STATUSES
from .exceptions import ValidationError, OrderNotFoundError, DatabaseError


def create_order(
    customer_name: str,
    billing_address: str,
    product_sku: str,
    quantity: int,
    order_amount: float,
    remarks: Optional[str] = None,
    order_status: str = "PENDING",
    order_date: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Create a new order.
    
    Args:
        customer_name: Name of the customer
        billing_address: Billing address
        product_sku: Product SKU/code
        quantity: Quantity ordered
        order_amount: Total order amount
        remarks: Additional remarks (optional)
        order_status: Order status (default: PENDING)
        order_date: Order date (default: current timestamp)
        
    Returns:
        dict: Created order data
        
    Raises:
        ValidationError: If validation fails
        DatabaseError: If database operation fails
    """
    # Prepare order data
    order_data = {
        "customer_name": customer_name,
        "billing_address": billing_address,
        "product_sku": product_sku,
        "quantity": quantity,
        "order_amount": order_amount,
        "remarks": remarks,
        "order_status": order_status.upper() if order_status else "PENDING",
        "order_date": order_date
    }
    
    # Validate order data
    validate_order_data(order_data, is_update=False)
    
    # Create order
    session = get_db_session()
    try:
        new_order = Order(
            customer_name=order_data["customer_name"],
            billing_address=order_data["billing_address"],
            product_sku=order_data["product_sku"],
            quantity=order_data["quantity"],
            order_amount=order_data["order_amount"],
            remarks=order_data["remarks"],
            order_status=order_data["order_status"],
            order_date=order_data["order_date"] or datetime.utcnow()
        )
        
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        
        result = new_order.to_dict()
        return result
        
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Failed to create order: {str(e)}")
    finally:
        session.close()


def get_order_by_id(order_id: int) -> Dict[str, Any]:
    """
    Get order details by order ID.
    
    Args:
        order_id: Order ID to retrieve
        
    Returns:
        dict: Order data
        
    Raises:
        OrderNotFoundError: If order is not found
        DatabaseError: If database operation fails
    """
    session = get_db_session()
    try:
        order = session.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        
        return order.to_dict()
        
    except OrderNotFoundError:
        raise
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to retrieve order: {str(e)}")
    finally:
        session.close()


def get_orders_by_customer(customer_name: str) -> List[Dict[str, Any]]:
    """
    Get all orders for a specific customer.
    
    Args:
        customer_name: Name of the customer
        
    Returns:
        list: List of order dictionaries
        
    Raises:
        DatabaseError: If database operation fails
    """
    session = get_db_session()
    try:
        orders = session.query(Order).filter(
            Order.customer_name == customer_name
        ).order_by(Order.order_date.desc()).all()
        
        return [order.to_dict() for order in orders]
        
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to retrieve orders: {str(e)}")
    finally:
        session.close()


def search_orders(
    product_sku: Optional[str] = None,
    billing_address: Optional[str] = None,
    order_status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search orders by product SKU, billing address, or order status.
    Supports partial matching and case-insensitive search for product_sku and billing_address.
    
    Args:
        product_sku: Product SKU to search (partial match, case-insensitive)
        billing_address: Billing address to search (partial match, case-insensitive)
        order_status: Order status to filter by (exact match, case-insensitive)
        
    Returns:
        list: List of matching order dictionaries
        
    Raises:
        ValidationError: If validation fails
        DatabaseError: If database operation fails
    """
    # Validate order_status if provided
    if order_status:
        validate_order_status(order_status)
    
    session = get_db_session()
    try:
        query = session.query(Order)
        
        # Build filter conditions
        filters = []
        
        if product_sku:
            filters.append(Order.product_sku.ilike(f"%{product_sku}%"))
        
        if billing_address:
            filters.append(Order.billing_address.ilike(f"%{billing_address}%"))
        
        if order_status:
            filters.append(Order.order_status == order_status.upper())
        
        # Apply filters
        if filters:
            query = query.filter(or_(*filters))
        
        orders = query.order_by(Order.order_date.desc()).all()
        
        return [order.to_dict() for order in orders]
        
    except ValidationError:
        raise
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to search orders: {str(e)}")
    finally:
        session.close()


def update_order_status(order_id: int, new_status: str) -> Dict[str, Any]:
    """
    Update the status of an order.
    
    Args:
        order_id: Order ID to update
        new_status: New order status
        
    Returns:
        dict: Updated order data
        
    Raises:
        ValidationError: If validation fails
        OrderNotFoundError: If order is not found
        DatabaseError: If database operation fails
    """
    # Validate status
    validate_order_status(new_status)
    
    session = get_db_session()
    try:
        order = session.query(Order).filter(Order.order_id == order_id).first()
        
        if not order:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        
        order.order_status = new_status.upper()
        session.commit()
        session.refresh(order)
        
        return order.to_dict()
        
    except (ValidationError, OrderNotFoundError):
        raise
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseError(f"Failed to update order status: {str(e)}")
    finally:
        session.close()


def get_all_orders(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get all orders.
    
    Args:
        limit: Optional limit on number of orders to return
        
    Returns:
        list: List of all order dictionaries
        
    Raises:
        DatabaseError: If database operation fails
    """
    session = get_db_session()
    try:
        query = session.query(Order).order_by(Order.order_date.desc())
        
        if limit:
            query = query.limit(limit)
        
        orders = query.all()
        
        return [order.to_dict() for order in orders]
        
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to retrieve orders: {str(e)}")
    finally:
        session.close()
