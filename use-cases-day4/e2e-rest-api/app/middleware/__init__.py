"""HTTP middleware wiring — CORS, rate limiting, and request logging."""

import logging
import time
import uuid

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.config import Settings
from app.middleware.rate_limit import RateLimitMiddleware

logger = logging.getLogger("api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Adds X-Request-ID and X-Response-Time headers, logs each request."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()
        response: Response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration_ms}ms"

        logger.info(
            "%s %s %s %.0fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


def setup_middleware(app: FastAPI, settings: Settings) -> None:
    """Register all HTTP-level middleware on the FastAPI application."""

    # CORS (outermost — must be added first so Starlette wraps it last)
    if settings.ENABLE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=[
                "X-Request-ID",
                "X-Response-Time",
                "X-RateLimit-Limit",
                "X-RateLimit-Remaining",
                "X-RateLimit-Reset",
            ],
        )

    # Rate limiting (disabled by default)
    if settings.ENABLE_RATE_LIMITING:
        app.add_middleware(
            RateLimitMiddleware,
            max_requests=settings.RATE_LIMIT_PER_MINUTE,
            window_seconds=60,
        )

    # Request logging (innermost — runs closest to the route handler)
    app.add_middleware(RequestLoggingMiddleware)
