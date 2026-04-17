"""Complaint ORM model."""

from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Complaint(Base):
    """Represents a customer complaint linked to an order."""

    __tablename__ = "complaints"

    complaint_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    complaint_reg_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    order_id: Mapped[str] = mapped_column(String(20), ForeignKey("orders.order_id"), nullable=False)
    complaint_description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False, default="Medium")
    assigned_to: Mapped[str] = mapped_column(String(255), nullable=False, default="Unassigned")
    complaint_status: Mapped[str] = mapped_column(String(50), nullable=False, default="Open")
    resolution_note: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationship back to order
    order = relationship("Order", back_populates="complaints", lazy="select")

    def to_dict(self) -> dict:
        return {
            "complaint_id": self.complaint_id,
            "complaint_reg_date": self.complaint_reg_date.isoformat() if self.complaint_reg_date else None,
            "order_id": self.order_id,
            "complaint_description": self.complaint_description,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "complaint_status": self.complaint_status,
            "resolution_note": self.resolution_note,
        }

    def __repr__(self) -> str:
        return f"<Complaint(id={self.complaint_id}, order='{self.order_id}', status='{self.complaint_status}', priority='{self.priority}')>"
