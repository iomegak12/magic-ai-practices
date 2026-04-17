"""Custom exception classes and FastAPI exception handler registration."""

import logging
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.api.models import ErrorDetail, ErrorResponse

logger = logging.getLogger("api")


# ──────────────────────────────────────────────────────────────
# Custom Exceptions
# ──────────────────────────────────────────────────────────────

class AppException(Exception):
    """Base for all application-level exceptions."""

    status_code: int = 500
    error: str = "internal_error"

    def __init__(self, message: str = "An unexpected error occurred."):
        self.message = message
        super().__init__(message)


class AgentNotInitializedError(AppException):
    status_code = 503
    error = "agent_not_initialized"

    def __init__(self):
        super().__init__("The agent has not been initialized yet. Please try again shortly.")


class AgentExecutionError(AppException):
    status_code = 502
    error = "agent_execution_error"

    def __init__(self, message: str = "The agent encountered an error while processing your request."):
        super().__init__(message)


class SessionNotFoundError(AppException):
    status_code = 404
    error = "session_not_found"

    def __init__(self, session_id: str):
        super().__init__(f"Session '{session_id}' not found.")


class RateLimitExceededError(AppException):
    status_code = 429
    error = "rate_limit_exceeded"

    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")


# ──────────────────────────────────────────────────────────────
# Handler helpers
# ──────────────────────────────────────────────────────────────

def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None) if hasattr(request, "state") else None


def _error_json(
    status_code: int,
    error: str,
    message: str,
    request: Request,
    details: list[ErrorDetail] | None = None,
) -> JSONResponse:
    body = ErrorResponse(
        error=error,
        message=message,
        status_code=status_code,
        timestamp=datetime.now(timezone.utc).isoformat(),
        request_id=_request_id(request),
        details=details,
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())


# ──────────────────────────────────────────────────────────────
# Registration
# ──────────────────────────────────────────────────────────────

def setup_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI application."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        details = [
            ErrorDetail(
                code="validation_error",
                message=err.get("msg", ""),
                field=".".join(str(loc) for loc in err.get("loc", [])),
            )
            for err in exc.errors()
        ]
        logger.warning("Validation error: %s", exc.errors())
        return _error_json(422, "validation_error", "Request validation failed.", request, details)

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.error("%s: %s", exc.error, exc.message)
        response = _error_json(exc.status_code, exc.error, exc.message, request)
        if isinstance(exc, RateLimitExceededError):
            response.headers["Retry-After"] = str(exc.retry_after)
        return response

    @app.exception_handler(Exception)
    async def catch_all_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception: %s: %s", type(exc).__name__, exc, exc_info=True)
        return _error_json(
            500,
            "internal_error",
            "An unexpected error occurred. Please try again later.",
            request,
        )
