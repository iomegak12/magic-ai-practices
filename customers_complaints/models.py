"""SQLAlchemy ORM models for customers, complaints, and profile preferences."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    active_status: Mapped[str] = mapped_column(String(10), default="active")
    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)

    complaints: Mapped[list["Complaint"]] = relationship(back_populates="customer")
    profile_preference: Mapped["CustomerProfilePreference | None"] = relationship(
        back_populates="customer", uselist=False
    )

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "address": self.address,
            "email": self.email,
            "phone": self.phone,
            "active_status": self.active_status,
            "remarks": self.remarks,
        }


class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    complaint_date: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    customer_id: Mapped[str] = mapped_column(
        String(12), ForeignKey("customers.customer_id"), nullable=False
    )
    complaint_description: Mapped[str] = mapped_column(String(2000), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Open", nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="complaints")

    def to_dict(self) -> dict:
        return {
            "complaint_id": self.complaint_id,
            "complaint_date": self.complaint_date.isoformat(),
            "customer_id": self.customer_id,
            "complaint_description": self.complaint_description,
            "priority": self.priority,
            "status": self.status,
        }


class CustomerProfilePreference(Base):
    __tablename__ = "customer_profile_preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[str] = mapped_column(
        String(12), ForeignKey("customers.customer_id"), unique=True, nullable=False
    )
    customer_type: Mapped[str] = mapped_column(String(20), nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="profile_preference")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_type": self.customer_type,
        }
