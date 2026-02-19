"""
SQLAlchemy Database Models

This module defines the database models for the complaint management system.

Models:
    - Complaint: Customer complaint entity
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from .enums import Priority, Status

# Create declarative base
Base = declarative_base()


class Complaint(Base):
    """
    Complaint database model.
    
    Represents a customer complaint associated with an order.
    
    Attributes:
        complaint_id: Unique identifier (primary key)
        title: Complaint title
        description: Detailed complaint description
        customer_name: Customer name
        order_number: Associated order number (format: ORD-XXXXX)
        created_at: Timestamp when complaint was created (UTC)
        updated_at: Timestamp when complaint was last updated (UTC)
        priority: Complaint priority level (enum)
        status: Current complaint status (enum)
        remarks: Additional notes or remarks
        is_archived: Soft-delete flag
        resolution_date: Timestamp when complaint was resolved (UTC)
    """
    
    __tablename__ = 'complaints'
    
    # Primary Key
    complaint_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Required Fields
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    customer_name = Column(String(100), nullable=False, index=True)
    order_number = Column(String(50), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Status Fields
    priority = Column(
        SQLEnum(Priority),
        nullable=False,
        default=Priority.MEDIUM
    )
    status = Column(
        SQLEnum(Status),
        nullable=False,
        default=Status.OPEN,
        index=True
    )
    
    # Optional Fields
    remarks = Column(Text, nullable=True)
    is_archived = Column(Boolean, nullable=False, default=False, index=True)
    resolution_date = Column(DateTime, nullable=True)
    
    def to_dict(self) -> dict:
        """
        Convert complaint to dictionary.
        
        Returns:
            Dictionary representation of complaint
        """
        return {
            'complaint_id': self.complaint_id,
            'title': self.title,
            'description': self.description,
            'customer_name': self.customer_name,
            'order_number': self.order_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'remarks': self.remarks,
            'is_archived': self.is_archived,
            'resolution_date': self.resolution_date.isoformat() if self.resolution_date else None
        }
    
    def __repr__(self) -> str:
        """String representation of complaint."""
        return (
            f"<Complaint(id={self.complaint_id}, "
            f"title='{self.title[:30]}...', "
            f"customer='{self.customer_name}', "
            f"order='{self.order_number}', "
            f"status={self.status.value if self.status else None})>"
        )
