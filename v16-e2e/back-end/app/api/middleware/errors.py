"""
Error Handling Middleware

Global exception handling and standardized error responses.
"""
from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ...utils.exceptions import (
    APIException,
    ValidationError,
    RateLimitError,
    ResourceNotFoundError,
    AuthenticationError,
    AuthorizationError,
    AgentException,
    ToolException,
    SessionException,
    SessionNotFoundError,
    SessionExpiredError
)
from ...utils.logger import get_logger

logger = get_logger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for global exception handling.
    
    Catches all exceptions and returns standardized JSON error responses.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Handle exceptions during request processing."""
        try:
            response = await call_next(request)
            return response
        
        except Exception as exc:
            return await self.handle_exception(request, exc)
    
    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """
        Handle exception and return appropriate JSON response.
        
        Args:
            request: The request that caused the exception
            exc: The exception that was raised
        
        Returns:
            JSONResponse with error details
        """
        request_id = getattr(request.state, "request_id", None)
        path = request.url.path
        
        # Get exception details
        error_type = type(exc).__name__
        error_message = str(exc)
        
        # Determine status code and response based on exception type
        if isinstance(exc, ValidationError):
            status_code = 400
            error = "Validation Error"
            detail = error_message
            log_level = "warning"
        
        elif isinstance(exc, SessionNotFoundError):
            status_code = 404
            error = "Session Not Found"
            detail = error_message
            log_level = "warning"
        
        elif isinstance(exc, SessionExpiredError):
            status_code = 410
            error = "Session Expired"
            detail = error_message
            log_level = "info"
        
        elif isinstance(exc, ResourceNotFoundError):
            status_code = 404
            error = "Resource Not Found"
            detail = error_message
            log_level = "warning"
        
        elif isinstance(exc, AuthenticationError):
            status_code = 401
            error = "Authentication Failed"
            detail = error_message
            log_level = "warning"
        
        elif isinstance(exc, AuthorizationError):
            status_code = 403
            error = "Access Denied"
            detail = error_message
            log_level = "warning"
        
        elif isinstance(exc, RateLimitError):
            status_code = 429
            error = "Rate Limit Exceeded"
            detail = error_message
            log_level = "warning"
        
        elif isinstance(exc, APIException):
            status_code = getattr(exc, "status_code", 500)
            error = "API Error"
            detail = error_message
            log_level = "error" if status_code >= 500 else "warning"
        
        elif isinstance(exc, (AgentException, ToolException, SessionException)):
            status_code = 500
            error = "Service Error"
            detail = "An error occurred while processing your request"
            log_level = "error"
        
        else:
            # Unknown exception
            status_code = 500
            error = "Internal Server Error"
            detail = "An unexpected error occurred"
            log_level = "error"
        
        # Log the error
        log_func = getattr(logger, log_level)
        log_func(
            f"Error handling request: {error_type}",
            extra={
                "request_id": request_id,
                "path": path,
                "error_type": error_type,
                "error_message": error_message,
                "status_code": status_code
            },
            exc_info=(log_level == "error")  # Include traceback for errors
        )
        
        # Build error response
        error_response = {
            "error": error,
            "detail": detail,
            "timestamp": datetime.utcnow().isoformat(),
            "path": path
        }
        
        # Add request ID if available
        if request_id:
            error_response["request_id"] = request_id
        
        # Add error type in development/debug mode
        if log_level == "error":
            error_response["error_type"] = error_type
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )
