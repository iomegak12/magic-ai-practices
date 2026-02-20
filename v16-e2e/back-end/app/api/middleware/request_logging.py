"""
Request Logging Middleware

Comprehensive request and response logging with performance timing.
"""
import time
import uuid
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from ...utils.logger import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses.
    
    Features:
    - Assigns unique request ID
    - Logs request details (method, path, IP, user agent)
    - Logs response details (status code, duration)
    - Injects request ID into response headers
    """
    
    # Paths to exclude from detailed logging
    MINIMAL_LOG_PATHS = ["/health", "/health/liveness"]
    
    async def dispatch(self, request: Request, call_next):
        """Process request with logging."""
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Get request details
        method = request.method
        path = request.url.path
        ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Minimal logging for health checks
        is_minimal = path in self.MINIMAL_LOG_PATHS
        
        # Log request start
        if not is_minimal:
            logger.info(
                f"→ Request started: {method} {path}",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "ip": ip,
                    "user_agent": user_agent,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        else:
            logger.debug(
                f"→ {method} {path}",
                extra={"request_id": request_id}
            )
        
        # Start timer
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log response
            if not is_minimal:
                log_level = "info" if response.status_code < 400 else "warning" if response.status_code < 500 else "error"
                log_func = getattr(logger, log_level)
                
                log_func(
                    f"← Response: {response.status_code} ({duration_ms:.2f}ms)",
                    extra={
                        "request_id": request_id,
                        "status_code": response.status_code,
                        "duration_ms": round(duration_ms, 2),
                        "path": path,
                        "method": method
                    }
                )
            else:
                logger.debug(
                    f"← {response.status_code}",
                    extra={"request_id": request_id, "duration_ms": round(duration_ms, 2)}
                )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
            
            return response
        
        except Exception as e:
            # Log error
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error(
                f"← Request failed: {str(e)} ({duration_ms:.2f}ms)",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration_ms": round(duration_ms, 2),
                    "path": path,
                    "method": method
                },
                exc_info=True
            )
            
            # Re-raise to let error handlers deal with it
            raise


class ContextInjectionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject context into request state.
    
    Makes request ID and other context available to route handlers.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Inject context into request."""
        # Ensure request has request_id (in case logging middleware is disabled)
        if not hasattr(request.state, "request_id"):
            request.state.request_id = str(uuid.uuid4())
        
        # Add timestamp
        request.state.timestamp = datetime.utcnow()
        
        # Add client info
        request.state.client_ip = request.client.host if request.client else "unknown"
        
        # Process request
        response = await call_next(request)
        
        return response
