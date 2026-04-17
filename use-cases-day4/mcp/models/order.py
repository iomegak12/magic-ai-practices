"""Order ORM model."""

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Order(Base):
    """Represents a customer eCommerce order."""

    __tablename__ = "orders"

    order_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_sku: Mapped[str] = mapped_column(String(8), nullable=False)
    billing_address: Mapped[str] = mapped_column(Text, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)
    order_status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    remarks: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationship to complaints
    complaints = relationship("Complaint", back_populates="order", lazy="select")

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "customer_name": self.customer_name,
            "product_sku": self.product_sku,
            "billing_address": self.billing_address,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "order_status": self.order_status,
            "remarks": self.remarks,
        }

    def __repr__(self) -> str:
        return f"<Order(id={self.order_id}, customer='{self.customer_name}', sku='{self.product_sku}', status='{self.order_status}')>"
