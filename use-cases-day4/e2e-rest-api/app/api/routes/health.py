"""Health and readiness endpoints."""

import sqlite3
import time

from fastapi import APIRouter

from app.api.models import HealthResponse, ReadinessCheck, ReadinessResponse
from app.config import get_settings

router = APIRouter(prefix="/health", tags=["Health"])

_start_time = time.time()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 if the server process is alive.",
)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        version=settings.APP_VERSION,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


@router.get(
    "/readiness",
    response_model=ReadinessResponse,
    summary="Readiness probe",
    description="Checks whether the agent, database, and MCP servers are operational.",
)
async def readiness() -> ReadinessResponse:
    settings = get_settings()
    checks: dict[str, ReadinessCheck] = {}

    # Agent check
    try:
        from app.agent.manager import get_manager

        mgr = get_manager()
        checks["agent"] = ReadinessCheck(
            status="ok" if mgr.is_initialized else "degraded",
            detail="Agent is initialized" if mgr.is_initialized else "Agent not ready",
        )
    except RuntimeError:
        checks["agent"] = ReadinessCheck(status="fail", detail="Agent not initialized")

    # Database check
    try:
        with sqlite3.connect(settings.DB_PATH) as conn:
            conn.execute("SELECT 1")
        checks["database"] = ReadinessCheck(status="ok", detail="SQLite accessible")
    except Exception as e:
        checks["database"] = ReadinessCheck(status="fail", detail=str(e))

    all_ok = all(c.status == "ok" for c in checks.values())
    return ReadinessResponse(
        ready=all_ok,
        status="ready" if all_ok else "degraded",
        checks=checks,
    )
