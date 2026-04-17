"""
SQLAlchemy models for order management system.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base


class Order(Base):
    """
    Order model representing a customer order.
    
    Attributes:
        order_id: Unique identifier for the order (auto-incremented)
        order_date: Date when the order was placed (ISO format)
        customer_name: Name of the customer
        billing_address: Billing address for the order
        product_sku: Product SKU/code
        quantity: Quantity ordered
        order_amount: Total amount for the order
        remarks: Additional remarks or notes
        order_status: Current status of the order
    """
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    customer_name = Column(String(255), nullable=False, index=True)
    billing_address = Column(String(500), nullable=False)
    product_sku = Column(String(100), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    order_amount = Column(Float, nullable=False)
    remarks = Column(String(1000), nullable=True)
    order_status = Column(String(50), nullable=False, index=True)
    
    def to_dict(self):
        """
        Convert order to dictionary representation.
        
        Returns:
            dict: Dictionary containing order data
        """
        return {
            "order_id": self.order_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "customer_name": self.customer_name,
            "billing_address": self.billing_address,
            "product_sku": self.product_sku,
            "quantity": self.quantity,
            "order_amount": self.order_amount,
            "remarks": self.remarks,
            "order_status": self.order_status
        }
    
    def __repr__(self):
        return f"<Order(order_id={self.order_id}, customer={self.customer_name}, status={self.order_status})>"
