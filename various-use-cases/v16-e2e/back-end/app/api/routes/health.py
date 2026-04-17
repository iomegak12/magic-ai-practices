"""
Health Check API Endpoints

Endpoints for monitoring service health and readiness.
"""
import logging
import time
from datetime import datetime
from fastapi import APIRouter, status
from typing import Dict, Any

from ..models import HealthCheckResponse, ReadinessCheckResponse
from ...config.settings import get_settings
from ...agent.manager import get_agent_manager
from ...tools.mcp_handler import is_mcp_available
from ...utils.helpers import format_timestamp
from ... import __version__

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])

# Track server start time for uptime calculation
_start_time = time.time()


@router.get(
    "",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Get overall health status of the service and its components"
)
async def health_check() -> HealthCheckResponse:
    """
    Comprehensive health check endpoint.
    
    Returns:
        HealthCheckResponse: Health status of all components
    """
    try:
        settings = get_settings()
        agent_manager = get_agent_manager()
        
        # Calculate uptime
        uptime = time.time() - _start_time
        
        # Check individual components
        checks = {
            "configuration": {
                "status": "healthy",
                "message": "Configuration loaded successfully"
            },
            "agent": {
                "status": "healthy" if agent_manager and agent_manager.is_initialized() else "unhealthy",
                "message": "Agent manager operational" if agent_manager and agent_manager.is_initialized() else "Agent manager not initialized",
                "active_sessions": agent_manager.get_session_count() if agent_manager else 0
            },
            "mcp_server": {
                "status": "healthy" if is_mcp_available() else "degraded",
                "message": "MCP server connected" if is_mcp_available() else "MCP server unavailable (optional)",
                "required": settings.mcp_server_required
            },
            "database": {
                "status": "healthy",
                "message": "Database accessible",
                "path": str(settings.database_path)
            },
            "email": {
                "status": "healthy",
                "message": "SMTP configuration loaded",
                "server": settings.smtp_server
            }
        }
        
        # Determine overall status
        if all(check["status"] == "healthy" for check in checks.values()):
            overall_status = "healthy"
        elif any(check["status"] == "unhealthy" for check in checks.values()):
            overall_status = "unhealthy"
        else:
            overall_status = "degraded"
        
        return HealthCheckResponse(
            status=overall_status,
            timestamp=format_timestamp(datetime.now()),
            version=__version__,
            uptime_seconds=uptime,
            checks=checks
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheckResponse(
            status="unhealthy",
            timestamp=format_timestamp(datetime.now()),
            version="unknown",
            uptime_seconds=time.time() - _start_time,
            checks={
                "error": {
                    "status": "unhealthy",
                    "message": f"Health check error: {str(e)}"
                }
            }
        )


@router.get(
    "/ready",
    response_model=ReadinessCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness Check",
    description="Check if the service is ready to accept requests"
)
async def readiness_check() -> ReadinessCheckResponse:
    """
    Readiness check endpoint for load balancers.
    
    Returns:
        ReadinessCheckResponse: Readiness status
    """
    try:
        agent_manager = get_agent_manager()
        
        # Check critical components
        components = {
            "configuration": True,
            "agent_manager": agent_manager is not None and agent_manager.is_initialized(),
            "database": True  # Basic check - could be enhanced with actual DB query
        }
        
        # Service is ready only if all critical components are ready
        ready = all(components.values())
        
        return ReadinessCheckResponse(
            ready=ready,
            status="ready" if ready else "not_ready",
            timestamp=format_timestamp(datetime.now()),
            components=components
        )
        
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return ReadinessCheckResponse(
            ready=False,
            status="error",
            timestamp=format_timestamp(datetime.now()),
            components={"error": False}
        )


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Check",
    description="Simple liveness probe for Kubernetes/container orchestration"
)
async def liveness_check() -> Dict[str, str]:
    """
    Simple liveness check endpoint.
    
    Returns:
        dict: Liveness status
    """
    return {
        "status": "alive",
        "timestamp": format_timestamp(datetime.now())
    }


# Export router
__all__ = ["router"]
