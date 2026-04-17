"""
SQLAlchemy ORM models for the Order Manager library.

This module defines the database models for customer orders.
"""

from datetime import datetime
from typing import Dict, Any
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, CheckConstraint
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Order(Base):
    """
    SQLAlchemy model for customer orders.
    
    Attributes:
        order_id: Unique order identifier (auto-increment)
        order_date: Date and time when order was placed
        customer_name: Full name of the customer
        billing_address: Customer billing address
        product_sku: Product SKU/code
        quantity: Order quantity
        order_amount: Total order amount in cents
        remarks: Optional notes or comments
        order_status: Current order status
        created_at: Record creation timestamp
        updated_at: Last modification timestamp
    """
    
    __tablename__ = 'orders'
    
    # Primary key
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Order details
    order_date = Column(DateTime, nullable=False)
    customer_name = Column(String(255), nullable=False, index=True)
    billing_address = Column(Text, nullable=False)
    product_sku = Column(String(100), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    order_amount = Column(Integer, nullable=False)
    remarks = Column(Text, nullable=True)
    order_status = Column(String(50), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('order_amount > 0', name='check_order_amount_positive'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Order object to a dictionary.
        
        Returns:
            Dictionary representation of the order with serialized datetime values.
        """
        return {
            'order_id': self.order_id,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'customer_name': self.customer_name,
            'billing_address': self.billing_address,
            'product_sku': self.product_sku,
            'quantity': self.quantity,
            'order_amount': self.order_amount,
            'remarks': self.remarks,
            'order_status': self.order_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self) -> str:
        """String representation of the Order object."""
        return (
            f"<Order(order_id={self.order_id}, "
            f"customer_name='{self.customer_name}', "
            f"product_sku='{self.product_sku}', "
            f"order_status='{self.order_status}')>"
        )
