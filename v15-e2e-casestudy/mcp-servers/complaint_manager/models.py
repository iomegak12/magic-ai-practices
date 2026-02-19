"""
SQLAlchemy ORM Models for Complaint Management
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Complaint(Base):
    """Complaint model representing customer complaints"""
    
    __tablename__ = 'complaints'
    
    complaint_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    customer_name = Column(String(255), nullable=False)
    order_id = Column(String(100), nullable=False)
    complaint_registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    remarks = Column(Text, nullable=True)
    priority = Column(String(50), nullable=False, default="Medium")
    status = Column(String(50), nullable=False, default="New")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert complaint object to dictionary"""
        return {
            "complaint_id": self.complaint_id,
            "description": self.description,
            "customer_name": self.customer_name,
            "order_id": self.order_id,
            "complaint_registration_date": self.complaint_registration_date.isoformat() if self.complaint_registration_date else None,
            "remarks": self.remarks,
            "priority": self.priority,
            "status": self.status,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<Complaint(id={self.complaint_id}, customer='{self.customer_name}', order='{self.order_id}', status='{self.status}')>"
