"""
Session Data Models

Pydantic models for session management.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field


class SessionMessage(BaseModel):
    """Single message in a conversation."""
    
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionData(BaseModel):
    """Complete session data including conversation history."""
    
    session_id: str = Field(..., min_length=1, max_length=255)
    tenant_id: str = Field(default="default", max_length=255)
    messages: List[SessionMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def add_message(self, role: str, content: str, tool_calls: Optional[List[Dict]] = None):
        """Add a message to the session."""
        message = SessionMessage(
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            tool_calls=tool_calls
        )
        self.messages.append(message)
        self.last_activity = datetime.utcnow()
    
    def get_context(self) -> List[Dict[str, str]]:
        """Get conversation context for agent."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.messages
        ]


class SessionSummary(BaseModel):
    """Summary information about a session."""
    
    session_id: str
    tenant_id: str
    message_count: int
    created_at: datetime
    last_activity: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SessionHistoryResponse(BaseModel):
    """Response model for session history endpoint."""
    
    session_id: str
    tenant_id: str
    message_count: int
    created_at: datetime
    last_activity: datetime
    messages: List[SessionMessage]


class SessionListResponse(BaseModel):
    """Response model for listing sessions."""
    
    tenant_id: str
    total: int
    limit: int
    offset: int
    sessions: List[SessionSummary]
