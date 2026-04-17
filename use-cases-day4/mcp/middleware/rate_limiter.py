"""Per-client-IP rate limiting ASGI middleware."""

import time
import json
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class RateLimiterMiddleware:
    """
    ASGI middleware that enforces per-client-IP rate limits.

    Disabled by default; controlled via RATE_LIMIT_ENABLED in settings.
    When a client exceeds the allowed number of requests within the
    configured window, the middleware returns HTTP 429 with a Retry-After header.
    """

    def __init__(self, app, *, enabled: bool, max_requests: int, window_seconds: int):
        self.app = app
        self.enabled = enabled
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # {ip: [timestamp, ...]}
        self._requests: dict[str, list[float]] = defaultdict(list)

    def _client_ip(self, scope) -> str:
        """Extract client IP from the ASGI scope."""
        client = scope.get("client")
        if client:
            return client[0]
        return "unknown"

    def _is_rate_limited(self, ip: str) -> tuple[bool, int]:
        """Check whether the IP has exceeded the limit. Returns (limited, retry_after)."""
        now = time.monotonic()
        cutoff = now - self.window_seconds

        # Prune old entries
        timestamps = self._requests[ip]
        self._requests[ip] = [t for t in timestamps if t > cutoff]

        if len(self._requests[ip]) >= self.max_requests:
            oldest = self._requests[ip][0]
            retry_after = int(oldest + self.window_seconds - now) + 1
            return True, max(retry_after, 1)

        self._requests[ip].append(now)
        return False, 0

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket") or not self.enabled:
            return await self.app(scope, receive, send)

        ip = self._client_ip(scope)
        limited, retry_after = self._is_rate_limited(ip)

        if limited:
            logger.warning(f"Rate limit exceeded for {ip}")
            body = json.dumps({"error": "Rate limit exceeded. Please try again later."}).encode()
            await send({
                "type": "http.response.start",
                "status": 429,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"retry-after", str(retry_after).encode()],
                ],
            })
            await send({"type": "http.response.body", "body": body})
            return

        return await self.app(scope, receive, send)
