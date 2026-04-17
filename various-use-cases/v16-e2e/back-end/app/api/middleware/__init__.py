"""
API Middleware Components

Middleware for rate limiting, logging, error handling, and request processing.
"""
import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ...config import get_settings
from .rate_limit import (
    SlidingWindowRateLimiter,
    RateLimitMiddleware,
    create_rate_limiter,
    get_rate_limiter
)
from .request_logging import (
    RequestLoggingMiddleware,
    ContextInjectionMiddleware
)
from .errors import ErrorHandlingMiddleware

logger = logging.getLogger(__name__)


def setup_cors_middleware(app: FastAPI) -> None:
    """
    Setup CORS middleware for the application.
    
    Args:
        app: FastAPI application
    """
    settings = get_settings()
    
    if settings.ENABLE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, specify allowed origins
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=[
                "X-Request-ID",
                "X-Request-Timestamp",
                "X-Response-Time",
                "X-RateLimit-Limit",
                "X-RateLimit-Remaining",
                "X-RateLimit-Reset"
            ]
        )
        logger.info("CORS middleware configured")
    else:
        logger.info("CORS middleware disabled")


def setup_custom_middleware(app: FastAPI) -> None:
    """
    Setup custom middleware for the application.
    
    Middleware order is IMPORTANT - they execute in reverse order of registration:
    1. Error handling (innermost - catches all exceptions)
    2. Request logging (logs requests/responses)
    3. Context injection (adds request context)
    4. Rate limiting (outermost - rejects excessive requests early)
    
    Args:
        app: FastAPI application
    """
    settings = get_settings()
    
    # 1. Error handling middleware (catches all exceptions)
    app.add_middleware(ErrorHandlingMiddleware)
    logger.info("✓ Error handling middleware added")
    
    # 2. Request logging middleware (logs all requests/responses)
    app.add_middleware(RequestLoggingMiddleware)
    logger.info("✓ Request logging middleware added")
    
    # 3. Context injection middleware (populates request.state)
    app.add_middleware(ContextInjectionMiddleware)
    logger.info("✓ Context injection middleware added")
    
    # 4. Rate limiting middleware (optional, rejects excessive requests)
    if settings.ENABLE_RATE_LIMITING:
        rate_limiter = get_rate_limiter()
        app.add_middleware(RateLimitMiddleware, rate_limiter=rate_limiter)
        logger.info(f"✓ Rate limiting middleware added ({settings.RATE_LIMIT_PER_MINUTE} req/min)")
    else:
        logger.info("✗ Rate limiting middleware disabled")


__all__ = [
    # Rate Limiting
    "SlidingWindowRateLimiter",
    "RateLimitMiddleware",
    "create_rate_limiter",
    "get_rate_limiter",
    
    # Logging
    "RequestLoggingMiddleware",
    "ContextInjectionMiddleware",
    
    # Error Handling
    "ErrorHandlingMiddleware",
    
    # Setup functions
    "setup_cors_middleware",
    "setup_custom_middleware",
]

