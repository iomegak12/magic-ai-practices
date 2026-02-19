"""
Pydantic Validation Schemas

This module defines Pydantic schemas for request/response validation.

Schemas:
    - ComplaintCreate: Schema for creating a new complaint
    - ComplaintUpdate: Schema for updating a complaint
    - ComplaintResponse: Schema for complaint response
    - ComplaintSearchParams: Schema for search parameters
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from .enums import Priority, Status
import re


class ComplaintCreate(BaseModel):
    """
    Schema for creating a new complaint.
    
    Attributes:
        title: Complaint title (5-200 characters)
        description: Detailed description (minimum 10 characters)
        customer_name: Customer name (2-100 characters)
        order_number: Order number (format: ORD-XXXXX)
        priority: Priority level (default: MEDIUM)
        remarks: Optional additional remarks
    """
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    customer_name: str = Field(..., min_length=2, max_length=100)
    order_number: str = Field(..., pattern=r'^ORD-\d{5,}$')
    priority: Priority = Priority.MEDIUM
    remarks: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title contains only allowed characters."""
        if not re.match(r'^[a-zA-Z0-9\s\-_,.]+$', v):
            raise ValueError('Title can only contain letters, numbers, spaces, and -_,.')
        return v
    
    @field_validator('customer_name')
    @classmethod
    def validate_customer_name(cls, v: str) -> str:
        """Validate customer name contains only letters and spaces."""
        if not re.match(r'^[a-zA-Z\s]+$', v):
            raise ValueError('Customer name can only contain letters and spaces')
        return v


class ComplaintUpdate(BaseModel):
    """
    Schema for updating a complaint.
    
    Attributes:
        title: New title (optional)
        description: New description (optional)
        remarks: New remarks (optional)
    """
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    remarks: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title if provided."""
        if v is not None and not re.match(r'^[a-zA-Z0-9\s\-_,.]+$', v):
            raise ValueError('Title can only contain letters, numbers, spaces, and -_,.')
        return v


class ComplaintResponse(BaseModel):
    """
    Schema for complaint response.
    
    Attributes:
        complaint_id: Unique identifier
        title: Complaint title
        description: Detailed description
        customer_name: Customer name
        order_number: Order number
        created_at: Creation timestamp
        updated_at: Last update timestamp
        priority: Priority level
        status: Current status
        remarks: Additional remarks
        is_archived: Archive flag
        resolution_date: Resolution timestamp
    """
    complaint_id: int
    title: str
    description: str
    customer_name: str
    order_number: str
    created_at: datetime
    updated_at: datetime
    priority: Priority
    status: Status
    remarks: Optional[str] = None
    is_archived: bool
    resolution_date: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


class ComplaintSearchParams(BaseModel):
    """
    Schema for search parameters.
    
    Attributes:
        customer_name: Filter by customer name (partial match)
        order_number: Filter by order number (partial match)
        title: Filter by title (partial match)
        status: Filter by status (exact match)
        include_archived: Include archived complaints
    """
    customer_name: Optional[str] = None
    order_number: Optional[str] = None
    title: Optional[str] = None
    status: Optional[Status] = None
    include_archived: bool = False


class SuccessResponse(BaseModel):
    """
    Schema for success response.
    
    Attributes:
        success: Success flag (always True)
        message: Success message
        data: Response data
    """
    success: bool = True
    message: str
    data: dict


class ErrorResponse(BaseModel):
    """
    Schema for error response.
    
    Attributes:
        success: Success flag (always False)
        error: Error details
    """
    success: bool = False
    error: dict
    
    @staticmethod
    def create(code: str, message: str, details: Optional[dict] = None) -> dict:
        """
        Create an error response.
        
        Args:
            code: Error code
            message: Error message
            details: Additional error details
            
        Returns:
            Error response dictionary
        """
        return {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or {}
            }
        }
