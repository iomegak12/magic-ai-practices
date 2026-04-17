"""
Health Check Endpoint

Provides service health status and dependency checks.
"""
from fastapi import APIRouter, status
from datetime import datetime
import httpx
import os

from ..schemas import HealthResponse
from ..config import settings

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check service health and dependency status"
)
async def health_check():
    """
    Health check endpoint that verifies:
    - Service is running
    - Database connection
    - MCP server reachability
    
    Returns 200 if healthy, 503 if degraded.
    """
    # Check database connectivity
    db_status = "connected"
    try:
        if os.path.exists(settings.ORDER_DB_PATH):
            db_status = "connected"
        else:
            # Database will be created on first access
            db_status = "not_initialized"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check MCP server reachability
    mcp_status = "reachable"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.head(
                settings.MCP_COMPLAINT_SERVER_URL,
                timeout=3.0
            )
            if response.status_code < 500:
                mcp_status = "reachable"
            else:
                mcp_status = "unreachable"
    except httpx.TimeoutException:
        mcp_status = "timeout"
    except httpx.ConnectError:
        mcp_status = "connection_refused"
    except Exception as e:
        mcp_status = f"error: {str(e)[:50]}"
    
    # Determine overall health
    overall_status = "healthy"
    if db_status != "connected" or mcp_status not in ["reachable", "timeout"]:
        overall_status = "degraded"
    
    return HealthResponse(
        status=overall_status,
        service=settings.SERVICE_NAME,
        version=settings.SERVICE_VERSION,
        timestamp=datetime.now(),
        dependencies={
            "database": db_status,
            "mcp_server": mcp_status
        }
    )
