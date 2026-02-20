"""
API Request and Response Models

Pydantic models for API request validation and response serialization.
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


# ====================
# Agent Request Models
# ====================

class CreateSessionRequest(BaseModel):
    """Request model for creating a new conversation session."""
    session_id: Optional[str] = Field(
        None,
        description="Optional custom session ID (auto-generated if not provided)",
        min_length=1,
        max_length=100
    )
    tenant_id: Optional[str] = Field(
        None,
        description="Optional tenant identifier for multi-tenancy",
        min_length=1,
        max_length=100
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata to attach to the session"
    )


class SendMessageRequest(BaseModel):
    """Request model for sending a message to the agent."""
    message: str = Field(
        ...,
        description="User message to send to the agent",
        min_length=1,
        max_length=10000
    )
    session_id: str = Field(
        ...,
        description="Session ID for the conversation",
        min_length=1,
        max_length=100
    )
    tenant_id: Optional[str] = Field(
        None,
        description="Optional tenant identifier",
        min_length=1,
        max_length=100
    )
    stream: bool = Field(
        False,
        description="Whether to stream the response (not yet implemented)"
    )


class DeleteSessionRequest(BaseModel):
    """Request model for deleting a session."""
    session_id: str = Field(
        ...,
        description="Session ID to delete",
        min_length=1,
        max_length=100
    )
    tenant_id: Optional[str] = Field(
        None,
        description="Optional tenant identifier"
    )


# ====================
# Agent Response Models
# ====================

class CreateSessionResponse(BaseModel):
    """Response model for session creation."""
    session_id: str = Field(..., description="Unique session identifier")
    status: str = Field(..., description="Operation status")
    message: str = Field(..., description="Human-readable message")
    created_at: str = Field(..., description="Session creation timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Session metadata")


class SendMessageResponse(BaseModel):
    """Response model for agent message."""
    session_id: str = Field(..., description="Session identifier")
    response: str = Field(..., description="Agent's response message")
    status: str = Field(..., description="Operation status")
    timestamp: str = Field(..., description="Response timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Response metadata")


class SessionInfo(BaseModel):
    """Model for session information."""
    session_id: str = Field(..., description="Session identifier")
    created_at: str = Field(..., description="Creation timestamp")
    message_count: int = Field(..., description="Number of messages in session")
    last_activity: str = Field(..., description="Last activity timestamp")


class ListSessionsResponse(BaseModel):
    """Response model for listing sessions."""
    sessions: List[SessionInfo] = Field(..., description="List of active sessions")
    total_count: int = Field(..., description="Total number of sessions")
    status: str = Field(..., description="Operation status")


class DeleteSessionResponse(BaseModel):
    """Response model for session deletion."""
    session_id: str = Field(..., description="Deleted session identifier")
    status: str = Field(..., description="Operation status")
    message: str = Field(..., description="Human-readable message")


# ====================
# Health Check Models
# ====================

class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Overall health status: healthy, degraded, unhealthy")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    uptime_seconds: float = Field(..., description="Server uptime in seconds")
    checks: Dict[str, Any] = Field(..., description="Individual component health checks")


class ReadinessCheckResponse(BaseModel):
    """Response model for readiness check."""
    ready: bool = Field(..., description="Whether the service is ready to accept requests")
    status: str = Field(..., description="Readiness status")
    timestamp: str = Field(..., description="Check timestamp")
    components: Dict[str, bool] = Field(..., description="Component readiness status")


# ====================
# Error Response Models
# ====================

class ErrorDetail(BaseModel):
    """Detailed error information."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    field: Optional[str] = Field(None, description="Field name if validation error")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: str = Field(..., description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")


# ====================
# Utility Models
# ====================

class SuccessResponse(BaseModel):
    """Generic success response."""
    status: str = Field("success", description="Operation status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number (1-based)")
    page_size: int = Field(50, ge=1, le=1000, description="Number of items per page")
    
    @validator('page_size')
    def validate_page_size(cls, v):
        """Ensure page size is within reasonable limits."""
        if v > 1000:
            raise ValueError("Page size cannot exceed 1000")
        return v


# ====================
# API Info Models
# ====================

class APIInfo(BaseModel):
    """API information."""
    name: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    description: str = Field(..., description="API description")
    documentation_url: str = Field(..., description="Documentation URL")
    contact: Dict[str, str] = Field(..., description="Contact information")


class ToolInfo(BaseModel):
    """Information about available tools."""
    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    category: str = Field(..., description="Tool category: order, email, complaint")
    available: bool = Field(..., description="Whether the tool is currently available")


class ListToolsResponse(BaseModel):
    """Response model for listing available tools."""
    tools: List[ToolInfo] = Field(..., description="List of available tools")
    total_count: int = Field(..., description="Total number of tools")
    categories: List[str] = Field(..., description="Available tool categories")


# ====================
# Validation Helpers
# ====================

def validate_session_id(session_id: str) -> str:
    """
    Validate and sanitize session ID.
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        str: Validated session ID
        
    Raises:
        ValueError: If session ID is invalid
    """
    if not session_id or not isinstance(session_id, str):
        raise ValueError("Session ID must be a non-empty string")
    
    session_id = session_id.strip()
    
    if len(session_id) < 1 or len(session_id) > 100:
        raise ValueError("Session ID must be between 1 and 100 characters")
    
    # Check for invalid characters
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', session_id):
        raise ValueError("Session ID can only contain alphanumeric characters, hyphens, and underscores")
    
    return session_id


def validate_message(message: str) -> str:
    """
    Validate and sanitize user message.
    
    Args:
        message: User message to validate
        
    Returns:
        str: Validated message
        
    Raises:
        ValueError: If message is invalid
    """
    if not message or not isinstance(message, str):
        raise ValueError("Message must be a non-empty string")
    
    message = message.strip()
    
    if len(message) < 1:
        raise ValueError("Message cannot be empty")
    
    if len(message) > 10000:
        raise ValueError("Message cannot exceed 10,000 characters")
    
    return message


# Export all models
__all__ = [
    # Request models
    "CreateSessionRequest",
    "SendMessageRequest",
    "DeleteSessionRequest",
    
    # Response models
    "CreateSessionResponse",
    "SendMessageResponse",
    "SessionInfo",
    "ListSessionsResponse",
    "DeleteSessionResponse",
    "HealthCheckResponse",
    "ReadinessCheckResponse",
    "ErrorDetail",
    "ErrorResponse",
    "SuccessResponse",
    "APIInfo",
    "ToolInfo",
    "ListToolsResponse",
    
    # Utility models
    "PaginationParams",
    
    # Validation helpers
    "validate_session_id",
    "validate_message",
]
