"""
API Module

This module provides the REST API layer including:
- Request/response models
- API routes
- Middleware
- Error handlers
"""

from .models import (
    CreateSessionRequest,
    CreateSessionResponse,
    SendMessageRequest,
    SendMessageResponse,
    ListSessionsResponse,
    DeleteSessionResponse,
    HealthCheckResponse,
    ReadinessCheckResponse,
    ErrorResponse,
    APIInfo,
    ListToolsResponse
)

from .routes import (
    agent_router,
    health_router,
    info_router,
    sessions_router
)

from .middleware import (
    setup_cors_middleware,
    setup_custom_middleware
)

from .error_handlers import (
    setup_exception_handlers
)

__all__ = [
    # Models
    "CreateSessionRequest",
    "CreateSessionResponse",
    "SendMessageRequest",
    "SendMessageResponse",
    "ListSessionsResponse",
    "DeleteSessionResponse",
    "HealthCheckResponse",
    "ReadinessCheckResponse",
    "ErrorResponse",
    "APIInfo",
    "ListToolsResponse",
    
    # Routers
    "agent_router",
    "health_router",
    "info_router",
    "sessions_router",
    
    # Setup functions
    "setup_cors_middleware",
    "setup_custom_middleware",
    "setup_exception_handlers",
]
