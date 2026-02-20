"""
Main Order Manager class for managing customer orders.

This module provides the primary interface for all order management operations.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import or_
from .config import Config
from .database import Database
from .models import Order
from .exceptions import (
    OrderNotFoundException,
    InvalidOrderDataException,
    DatabaseException,
    ValidationException
)
from .validators import (
    validate_required_fields,
    validate_customer_name,
    validate_billing_address,
    validate_product_sku,
    validate_quantity,
    validate_order_amount,
    validate_order_status,
    validate_order_date,
    sanitize_customer_name,
    sanitize_product_sku
)


class OrderManager:
    """
    Main class for order management operations.
    
    Provides methods for creating, retrieving, searching, and updating orders.
    """
    
    def __init__(self, db_path: str = Config.DEFAULT_DB_PATH):
        """
        Initialize the Order Manager.
        
        Args:
            db_path: Path to the SQLite database file. Default: "orders.db"
        """
        self.db = Database(db_path)
    
    def create_order(
        self,
        order_date: datetime,
        customer_name: str,
        billing_address: str,
        product_sku: str,
        quantity: int,
        order_amount: int,
        order_status: str = "Pending",
        remarks: Optional[str] = None
    ) -> Order:
        """
        Create a new customer order (Feature F-001).
        
        Args:
            order_date: Date and time when order was placed
            customer_name: Full name of the customer
            billing_address: Customer billing address
            product_sku: Product SKU/code
            quantity: Order quantity (must be > 0)
            order_amount: Total order amount in cents (must be > 0)
            order_status: Order status (default: "Pending")
            remarks: Optional notes or comments
            
        Returns:
            The created Order object
            
        Raises:
            InvalidOrderDataException: If validation fails
            DatabaseException: If database operation fails
        """
        try:
            # Validate all required fields
            validate_required_fields(
                order_date=order_date,
                customer_name=customer_name,
                billing_address=billing_address,
                product_sku=product_sku,
                quantity=quantity,
                order_amount=order_amount,
                order_status=order_status
            )
            
            # Validate individual fields
            validate_order_date(order_date)
            validate_customer_name(customer_name)
            validate_billing_address(billing_address)
            validate_product_sku(product_sku)
            validate_quantity(quantity)
            validate_order_amount(order_amount)
            validate_order_status(order_status)
            
            # Sanitize inputs
            customer_name = sanitize_customer_name(customer_name)
            product_sku = sanitize_product_sku(product_sku)
            
            # Create order
            with self.db.get_session() as session:
                order = Order(
                    order_date=order_date,
                    customer_name=customer_name,
                    billing_address=billing_address,
                    product_sku=product_sku,
                    quantity=quantity,
                    order_amount=order_amount,
                    order_status=order_status,
                    remarks=remarks
                )
                session.add(order)
                session.flush()
                session.refresh(order)
                return order
                
        except (InvalidOrderDataException, DatabaseException, ValidationException):
            raise
        except Exception as e:
            raise InvalidOrderDataException(f"Failed to create order: {str(e)}")
    
    def get_orders_by_customer(self, customer_name: str) -> List[Order]:
        """
        Retrieve all orders for a specific customer (Feature F-002).
        
        Performs exact name match.
        
        Args:
            customer_name: Exact customer name to search
            
        Returns:
            List of Order objects (empty list if none found)
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            customer_name = sanitize_customer_name(customer_name)
            
            with self.db.get_session() as session:
                orders = session.query(Order).filter(
                    Order.customer_name == customer_name
                ).order_by(Order.order_date.desc()).all()
                
                # Detach from session
                return list(orders)
                
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve orders: {str(e)}", e)
    
    def get_order_by_id(self, order_id: int) -> Order:
        """
        Retrieve a specific order by its ID (Feature F-003).
        
        Args:
            order_id: The order ID to retrieve
            
        Returns:
            The Order object
            
        Raises:
            OrderNotFoundException: If order doesn't exist
            DatabaseException: If database operation fails
        """
        try:
            with self.db.get_session() as session:
                order = session.query(Order).filter(
                    Order.order_id == order_id
                ).first()
                
                if not order:
                    raise OrderNotFoundException(order_id)
                
                return order
                
        except OrderNotFoundException:
            raise
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve order: {str(e)}", e)
    
    def search_orders_by_customer(self, customer_name_partial: str) -> List[Order]:
        """
        Search orders by partial customer name match (Feature F-004).
        
        Performs case-insensitive partial match.
        
        Args:
            customer_name_partial: Partial customer name to search
            
        Returns:
            List of matching Order objects (empty list if none found)
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            search_pattern = f"%{customer_name_partial}%"
            
            with self.db.get_session() as session:
                orders = session.query(Order).filter(
                    Order.customer_name.ilike(search_pattern)
                ).order_by(Order.order_date.desc()).all()
                
                return list(orders)
                
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to search orders: {str(e)}", e)
    
    def search_orders(
        self,
        order_status: Optional[str] = None,
        product_sku: Optional[str] = None,
        billing_address_partial: Optional[str] = None
    ) -> List[Order]:
        """
        Advanced search for orders (Feature F-005).
        
        Search by order status, product SKU, or billing address.
        Multiple filters are combined with AND logic.
        
        Args:
            order_status: Filter by exact order status
            product_sku: Filter by exact product SKU
            billing_address_partial: Filter by partial address match (case-insensitive)
            
        Returns:
            List of matching Order objects (empty list if none found)
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            with self.db.get_session() as session:
                query = session.query(Order)
                
                # Apply filters
                if order_status:
                    validate_order_status(order_status)
                    query = query.filter(Order.order_status == order_status)
                
                if product_sku:
                    product_sku = sanitize_product_sku(product_sku)
                    query = query.filter(Order.product_sku == product_sku)
                
                if billing_address_partial:
                    search_pattern = f"%{billing_address_partial}%"
                    query = query.filter(Order.billing_address.ilike(search_pattern))
                
                # Execute query
                orders = query.order_by(Order.order_date.desc()).all()
                return list(orders)
                
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to search orders: {str(e)}", e)
    
    def update_order_status(self, order_id: int, new_status: str) -> Order:
        """
        Update the status of an existing order (Feature F-006).
        
        Args:
            order_id: The order ID to update
            new_status: New status value (must be valid status)
            
        Returns:
            The updated Order object
            
        Raises:
            OrderNotFoundException: If order doesn't exist
            InvalidOrderDataException: If status is invalid
            DatabaseException: If database operation fails
        """
        try:
            # Validate status
            validate_order_status(new_status)
            
            with self.db.get_session() as session:
                order = session.query(Order).filter(
                    Order.order_id == order_id
                ).first()
                
                if not order:
                    raise OrderNotFoundException(order_id)
                
                # Update status
                order.order_status = new_status
                session.flush()
                session.refresh(order)
                
                return order
                
        except (OrderNotFoundException, InvalidOrderDataException, ValidationException):
            raise
        except DatabaseException:
            raise
        except Exception as e:
            raise DatabaseException(f"Failed to update order status: {str(e)}", e)
    
    def close(self) -> None:
        """
        Close the database connection.
        
        Should be called when the OrderManager is no longer needed.
        """
        self.db.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes database connection."""
        self.close()
