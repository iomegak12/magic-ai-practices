"""
API Error Handlers

Global exception handlers for consistent error responses.
"""
import logging
from datetime import datetime
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .models import ErrorResponse, ErrorDetail
from ..utils.exceptions import (
    APIException,
    ValidationError,
    RateLimitError,
    ResourceNotFoundError,
    AuthenticationError,
    AuthorizationError,
    AgentException,
    ToolException,
    SessionException
)
from ..utils.helpers import format_timestamp, generate_request_id

logger = logging.getLogger(__name__)


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """
    Handle custom API exceptions.
    
    Args:
        request: Request that caused the exception
        exc: API exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.warning(
        f"[{request_id}] API Exception: {exc.__class__.__name__} - {str(exc)}"
    )
    
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=str(exc),
        status_code=exc.status_code,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    
    Args:
        request: Request that caused the error
        exc: Validation error
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.warning(f"[{request_id}] Validation error: {exc.errors()}")
    
    # Format error details
    details = [
        ErrorDetail(
            code="validation_error",
            message=error["msg"],
            field=".".join(str(loc) for loc in error["loc"]),
            details={"type": error["type"]}
        )
        for error in exc.errors()
    ]
    
    error_response = ErrorResponse(
        error="ValidationError",
        message="Request validation failed",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id,
        details=details
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.dict()
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """
    Handle standard HTTP exceptions.
    
    Args:
        request: Request that caused the exception
        exc: HTTP exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.warning(
        f"[{request_id}] HTTP Exception: {exc.status_code} - {exc.detail}"
    )
    
    error_response = ErrorResponse(
        error="HTTPException",
        message=str(exc.detail),
        status_code=exc.status_code,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


async def agent_exception_handler(request: Request, exc: AgentException) -> JSONResponse:
    """
    Handle agent-related exceptions.
    
    Args:
        request: Request that caused the exception
        exc: Agent exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.error(
        f"[{request_id}] Agent Exception: {exc.__class__.__name__} - {str(exc)}"
    )
    
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


async def session_exception_handler(request: Request, exc: SessionException) -> JSONResponse:
    """
    Handle session-related exceptions.
    
    Args:
        request: Request that caused the exception
        exc: Session exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.warning(
        f"[{request_id}] Session Exception: {exc.__class__.__name__} - {str(exc)}"
    )
    
    # Determine status code based on exception type
    from ..utils.exceptions import SessionNotFoundError, SessionExpiredError
    
    if isinstance(exc, SessionNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, SessionExpiredError):
        status_code = status.HTTP_410_GONE
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=str(exc),
        status_code=status_code,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict()
    )


async def tool_exception_handler(request: Request, exc: ToolException) -> JSONResponse:
    """
    Handle tool-related exceptions.
    
    Args:
        request: Request that caused the exception
        exc: Tool exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.error(
        f"[{request_id}] Tool Exception: {exc.__class__.__name__} - {str(exc)}"
    )
    
    error_response = ErrorResponse(
        error=exc.__class__.__name__,
        message=str(exc),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all other unhandled exceptions.
    
    Args:
        request: Request that caused the exception
        exc: Unhandled exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    request_id = getattr(request.state, "request_id", generate_request_id())
    
    logger.error(
        f"[{request_id}] Unhandled Exception: {exc.__class__.__name__} - {str(exc)}",
        exc_info=True
    )
    
    error_response = ErrorResponse(
        error="InternalServerError",
        message="An unexpected error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        timestamp=format_timestamp(datetime.now()),
        request_id=request_id
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.dict()
    )


def setup_exception_handlers(app):
    """
    Setup global exception handlers for the application.
    
    Args:
        app: FastAPI application
    """
    # Custom API exceptions
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(ValidationError, api_exception_handler)
    app.add_exception_handler(RateLimitError, api_exception_handler)
    app.add_exception_handler(ResourceNotFoundError, api_exception_handler)
    app.add_exception_handler(AuthenticationError, api_exception_handler)
    app.add_exception_handler(AuthorizationError, api_exception_handler)
    
    # Agent exceptions
    app.add_exception_handler(AgentException, agent_exception_handler)
    
    # Session exceptions
    app.add_exception_handler(SessionException, session_exception_handler)
    
    # Tool exceptions
    app.add_exception_handler(ToolException, tool_exception_handler)
    
    # Standard exceptions
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    
    # Catch-all for unhandled exceptions
    app.add_exception_handler(Exception, generic_exception_handler)
    
    logger.info("Global exception handlers configured")


# Export exception handler setup function
__all__ = [
    "setup_exception_handlers",
]
