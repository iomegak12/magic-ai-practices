"""
Session Management API Endpoints

Routes for managing conversation sessions.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from datetime import datetime

from ...session.manager import SessionManager, get_session_manager
from ...session.models import SessionHistoryResponse, SessionListResponse, SessionSummary
from ...utils.exceptions import SessionNotFoundError, SessionExpiredError
from ...utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/sessions", tags=["Sessions"])


@router.get("/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(
    session_id: str,
    tenant_id: str = Query(default="default", description="Tenant identifier"),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Get conversation history for a session.
    
    **Parameters:**
    - `session_id`: Session identifier
    - `tenant_id`: Tenant identifier (default: "default")
    
    **Returns:**
    - Session history including all messages
    
    **Errors:**
    - `404`: Session not found
    - `410`: Session expired
    """
    try:
        session = await session_manager.get_session(session_id, tenant_id)
        
        return SessionHistoryResponse(
            session_id=session.session_id,
            tenant_id=session.tenant_id,
            message_count=len(session.messages),
            created_at=session.created_at,
            last_activity=session.last_activity,
            messages=session.messages
        )
    
    except SessionNotFoundError as e:
        logger.warning(f"Session not found: {session_id}", extra={"session_id": session_id, "tenant_id": tenant_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Session not found",
                "session_id": session_id,
                "tenant_id": tenant_id
            }
        )
    
    except SessionExpiredError as e:
        logger.info(f"Session expired: {session_id}", extra={"session_id": session_id, "tenant_id": tenant_id})
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={
                "error": "Session expired",
                "session_id": session_id,
                "message": str(e)
            }
        )
    
    except Exception as e:
        logger.error(f"Error retrieving session history: {e}", extra={"session_id": session_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    tenant_id: str = Query(default="default", description="Tenant identifier"),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Delete a session.
    
    **Parameters:**
    - `session_id`: Session identifier
    - `tenant_id`: Tenant identifier (default: "default")
    
    **Returns:**
    - Confirmation message
    
    **Errors:**
    - `404`: Session not found
    """
    deleted = await session_manager.delete_session(session_id, tenant_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Session not found",
                "session_id": session_id,
                "tenant_id": tenant_id
            }
        )
    
    return {
        "message": "Session deleted successfully",
        "session_id": session_id,
        "tenant_id": tenant_id,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("", response_model=SessionListResponse)
async def list_sessions(
    tenant_id: str = Query(default="default", description="Tenant identifier"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of sessions to return"),
    offset: int = Query(default=0, ge=0, description="Number of sessions to skip"),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    List all sessions for a tenant.
    
    **Parameters:**
    - `tenant_id`: Tenant identifier (default: "default")
    - `limit`: Maximum number of sessions (1-100, default: 50)
    - `offset`: Number of sessions to skip (default: 0)
    
    **Returns:**
    - List of session summaries
    """
    try:
        sessions = await session_manager.list_sessions(tenant_id, limit, offset)
        
        # Get total count for tenant
        total = session_manager.store.count_by_tenant(tenant_id)
        
        return SessionListResponse(
            tenant_id=tenant_id,
            total=total,
            limit=limit,
            offset=offset,
            sessions=sessions
        )
    
    except Exception as e:
        logger.error(f"Error listing sessions: {e}", extra={"tenant_id": tenant_id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal server error", "message": str(e)}
        )


@router.post("/{session_id}/cleanup")
async def trigger_session_cleanup(
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Manually trigger session cleanup (removes expired sessions).
    
    This is typically called automatically by a background task,
    but can be triggered manually via this endpoint.
    
    **Returns:**
    - Number of sessions deleted
    """
    try:
        deleted_count = await session_manager.cleanup_expired_sessions()
        
        return {
            "message": "Session cleanup completed",
            "deleted_count": deleted_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error during session cleanup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Cleanup failed", "message": str(e)}
        )


@router.get("/stats")
async def get_session_stats(
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Get session statistics.
    
    **Returns:**
    - Session statistics including total count
    """
    try:
        stats = session_manager.get_stats()
        return stats
    
    except Exception as e:
        logger.error(f"Error getting session stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Failed to get stats", "message": str(e)}
        )
