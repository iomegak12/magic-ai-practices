"""
Pydantic schemas for API request and response models.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    session_id: Optional[str] = Field(
        None, 
        description="Session ID for multi-turn conversation. Auto-generated if not provided."
    )
    message: str = Field(
        ..., 
        description="User message to send to the customer service agent",
        min_length=1
    )
    stream: bool = Field(
        False, 
        description="Enable streaming response using Server-Sent Events"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "session_id": "customer-123",
                    "message": "I want to place an order for a laptop",
                    "stream": False
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint (non-streaming)."""
    session_id: str = Field(..., description="Session ID for this conversation")
    response: str = Field(..., description="Agent's response message")
    timestamp: datetime = Field(..., description="Response timestamp")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (turn count, tools used, etc.)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "session_id": "uuid-string",
                    "response": "Order created successfully with ID: 1",
                    "timestamp": "2026-02-19T10:30:00Z",
                    "metadata": {
                        "turn_count": 1,
                        "tools_used": ["create_customer_order"],
                        "tokens_used": 450
                    }
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""
    status: str = Field(..., description="Overall service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(..., description="Health check timestamp")
    dependencies: Dict[str, str] = Field(
        ..., 
        description="Status of external dependencies (database, MCP server, etc.)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "service": "MSAv15Service",
                    "version": "0.1.0",
                    "timestamp": "2026-02-19T10:30:00Z",
                    "dependencies": {
                        "database": "connected",
                        "mcp_server": "reachable"
                    }
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)
