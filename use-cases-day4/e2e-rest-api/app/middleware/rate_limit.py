"""Sliding-window per-IP rate limiter (ASGI middleware)."""

import logging
import time
import threading
from collections import defaultdict
from datetime import datetime, timezone

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger("rate_limit")

_EXCLUDED_PATHS = frozenset({
    "/health",
    "/health/readiness",
    "/docs",
    "/redoc",
    "/openapi.json",
})


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Per-client-IP sliding window rate limiter."""

    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def _clean_window(self, client_ip: str, now: float) -> list[float]:
        cutoff = now - self.window_seconds
        timestamps = self._requests[client_ip]
        timestamps[:] = [t for t in timestamps if t > cutoff]
        return timestamps

    async def dispatch(self, request: Request, call_next):
        if request.url.path in _EXCLUDED_PATHS:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        with self._lock:
            timestamps = self._clean_window(client_ip, now)
            remaining = max(0, self.max_requests - len(timestamps))
            reset_at = int(now + self.window_seconds)

            if len(timestamps) >= self.max_requests:
                retry_after = self.window_seconds
                logger.warning(
                    "Rate limit exceeded for %s (%d/%d)",
                    client_ip,
                    len(timestamps),
                    self.max_requests,
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "rate_limit_exceeded",
                        "message": f"Rate limit exceeded. Retry after {retry_after} seconds.",
                        "status_code": 429,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "limit": self.max_requests,
                        "retry_after": retry_after,
                    },
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(self.max_requests),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(reset_at),
                    },
                )

            timestamps.append(now)
            remaining = max(0, self.max_requests - len(timestamps))

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_at)
        return response
