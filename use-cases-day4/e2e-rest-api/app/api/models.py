"""Pydantic request / response models for all API endpoints."""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────
# Chat
# ──────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Request body for chat endpoints."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=10_000,
        description="The user message to send to the agent.",
        examples=["Get all orders for Priya Sharma"],
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session ID to resume an existing conversation. "
        "If omitted a new session is created automatically.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )


class ToolCallInfo(BaseModel):
    """Metadata about a single tool invocation during the agent run."""

    name: str = Field(description="Name of the tool that was called.")
    arguments: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments passed to the tool.",
    )
    duration_seconds: float = Field(description="Wall-clock execution time in seconds.")
    result_preview: str | None = Field(
        default=None,
        description="Truncated preview of the tool result (max 200 chars).",
    )


class ChatResponse(BaseModel):
    """Response body for the non-streaming chat endpoint."""

    session_id: str = Field(description="Session ID for this conversation.")
    response: str = Field(description="The agent's response text.")
    tools_used: list[ToolCallInfo] = Field(
        default_factory=list,
        description="Tools invoked during this agent run.",
    )
    duration_seconds: float = Field(description="Total wall-clock time for the agent run.")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO-8601 UTC timestamp of the response.",
    )
    status: str = Field(default="success")


# ──────────────────────────────────────────────────────────────
# Health
# ──────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Liveness probe response."""

    status: str = "healthy"
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    version: str = ""
    uptime_seconds: float = 0.0


class ReadinessCheck(BaseModel):
    """Status of an individual component."""

    status: str
    detail: str | None = None


class ReadinessResponse(BaseModel):
    """Readiness probe response."""

    ready: bool
    status: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    checks: dict[str, ReadinessCheck] = Field(default_factory=dict)


# ──────────────────────────────────────────────────────────────
# Errors
# ──────────────────────────────────────────────────────────────

class ErrorDetail(BaseModel):
    """One field-level or sub-error detail."""

    code: str
    message: str
    field: str | None = None
    details: str | None = None


class ErrorResponse(BaseModel):
    """Standardised error envelope returned by all error handlers."""

    error: str = Field(description="Short error type identifier.")
    message: str = Field(description="Human-readable error description.")
    status_code: int = Field(description="HTTP status code.")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    request_id: str | None = Field(
        default=None,
        description="Correlation ID from the X-Request-ID header.",
    )
    details: list[ErrorDetail] | None = None
