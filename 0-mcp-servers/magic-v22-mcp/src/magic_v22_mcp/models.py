"""Pydantic domain models for orders and complaints."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from magic_v22_mcp.enums import ComplaintPriority, ComplaintStatus, OrderStatus, ResolverTeam

ORDER_NUMBER_RE = re.compile(r"^ORD\d{5,}$")


class Order(BaseModel):
    order_id: int
    order_date: datetime
    customer_name: str = Field(min_length=1)
    order_number: str
    product_sku: str = Field(min_length=1)
    units: int = Field(gt=0)
    order_amount: int = Field(ge=0)
    remarks: str = ""
    status: OrderStatus = OrderStatus.PENDING

    @field_validator("order_number")
    @classmethod
    def validate_order_number(cls, v: str) -> str:
        if not ORDER_NUMBER_RE.match(v):
            raise ValueError("order_number must match pattern ORD followed by 5+ digits, e.g. ORD10001")
        return v


class Complaint(BaseModel):
    complaint_id: int
    complaint_date: datetime
    order_id: int
    registered_by: str = Field(min_length=1)
    complaint_description: str = Field(min_length=1)
    priority: ComplaintPriority
    status: ComplaintStatus = ComplaintStatus.OPEN
    resolved_by: Optional[ResolverTeam] = None
    resolution_remarks: Optional[str] = None
