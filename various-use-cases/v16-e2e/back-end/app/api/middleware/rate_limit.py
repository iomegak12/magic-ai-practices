"""
Rate Limiting Middleware

Sliding window rate limiter with per-IP tracking.
"""
import time
from typing import Dict, Tuple
from collections import defaultdict
from threading import Lock
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from ...config import get_settings
from ...utils.logger import get_logger

logger = get_logger(__name__)


class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter implementation.
    
    Tracks requests per IP address with a sliding time window.
    """
    
    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests allowed per minute
        """
        self.requests_per_minute = requests_per_minute
        self.window_size = 60.0  # 60 seconds
        self._requests: Dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()
    
    def _clean_old_requests(self, ip_address: str, current_time: float):
        """Remove requests older than the window."""
        cutoff_time = current_time - self.window_size
        self._requests[ip_address] = [
            req_time for req_time in self._requests[ip_address]
            if req_time > cutoff_time
        ]
    
    def is_allowed(self, ip_address: str) -> Tuple[bool, dict]:
        """
        Check if request from IP is allowed.
        
        Args:
            ip_address: Client IP address
        
        Returns:
            Tuple of (allowed: bool, metadata: dict)
        """
        current_time = time.time()
        
        with self._lock:
            # Clean old requests
            self._clean_old_requests(ip_address, current_time)
            
            # Get current count
            request_count = len(self._requests[ip_address])
            
            # Check limit
            if request_count >= self.requests_per_minute:
                # Calculate retry after
                oldest_request = self._requests[ip_address][0]
                retry_after = int(self.window_size - (current_time - oldest_request)) + 1
                
                return False, {
                    "limit": self.requests_per_minute,
                    "remaining": 0,
                    "reset": int(oldest_request + self.window_size),
                    "retry_after": retry_after
                }
            
            # Add current request
            self._requests[ip_address].append(current_time)
            
            # Calculate reset time (when oldest request expires)
            reset_time = int(current_time + self.window_size)
            if self._requests[ip_address]:
                reset_time = int(self._requests[ip_address][0] + self.window_size)
            
            return True, {
                "limit": self.requests_per_minute,
                "remaining": self.requests_per_minute - request_count - 1,
                "reset": reset_time,
                "retry_after": 0
            }
    
    def get_stats(self) -> dict:
        """Get rate limiter statistics."""
        with self._lock:
            return {
                "tracked_ips": len(self._requests),
                "total_requests_tracked": sum(len(reqs) for reqs in self._requests.values()),
                "requests_per_minute_limit": self.requests_per_minute
            }


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for FastAPI.
    
    Enforces rate limits per IP address with configurable exclusions.
    """
    
    # Paths that bypass rate limiting
    EXCLUDED_PATHS = [
        "/health",
        "/health/readiness",
        "/health/liveness",
        "/docs",
        "/redoc",
        "/openapi.json"
    ]
    
    def __init__(self, app, rate_limiter: SlidingWindowRateLimiter):
        """
        Initialize rate limit middleware.
        
        Args:
            app: FastAPI application
            rate_limiter: Rate limiter instance
        """
        super().__init__(app)
        self.rate_limiter = rate_limiter
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        # Skip rate limiting for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Get client IP
        ip_address = request.client.host if request.client else "unknown"
        
        # Check rate limit
        allowed, metadata = self.rate_limiter.is_allowed(ip_address)
        
        if not allowed:
            logger.warning(
                f"Rate limit exceeded for IP: {ip_address}",
                extra={
                    "ip": ip_address,
                    "path": request.url.path,
                    "retry_after": metadata["retry_after"]
                }
            )
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Please try again in {metadata['retry_after']} seconds.",
                    "limit": metadata["limit"],
                    "retry_after": metadata["retry_after"]
                },
                headers={
                    "X-RateLimit-Limit": str(metadata["limit"]),
                    "X-RateLimit-Remaining": str(metadata["remaining"]),
                    "X-RateLimit-Reset": str(metadata["reset"]),
                    "Retry-After": str(metadata["retry_after"])
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(metadata["limit"])
        response.headers["X-RateLimit-Remaining"] = str(metadata["remaining"])
        response.headers["X-RateLimit-Reset"] = str(metadata["reset"])
        
        return response


def create_rate_limiter() -> SlidingWindowRateLimiter:
    """
    Create rate limiter instance from settings.
    
    Returns:
        SlidingWindowRateLimiter instance
    """
    settings = get_settings()
    return SlidingWindowRateLimiter(
        requests_per_minute=settings.rate_limit_per_minute
    )


# Global rate limiter instance
_rate_limiter: SlidingWindowRateLimiter = None


def get_rate_limiter() -> SlidingWindowRateLimiter:
    """Get or create global rate limiter."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = create_rate_limiter()
    return _rate_limiter
