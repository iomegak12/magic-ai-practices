"""
Agent API Endpoints

Endpoints for agent conversation management.
"""
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import StreamingResponse
from typing import Optional

from ..models import (
    CreateSessionRequest,
    CreateSessionResponse,
    SendMessageRequest,
    SendMessageResponse,
    ListSessionsResponse,
    SessionInfo,
    DeleteSessionResponse
)
from ...agent.manager import get_agent_manager
from ...utils.exceptions import (
    AgentInitializationError,
    AgentExecutionError,
    SessionNotFoundError
)
from ...utils.helpers import format_timestamp, generate_request_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post(
    "/sessions",
    response_model=CreateSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Session",
    description="Create a new conversation session with the agent"
)
async def create_session(
    request: CreateSessionRequest,
    x_request_id: Optional[str] = Header(None)
) -> CreateSessionResponse:
    """
    Create a new conversation session.
    
    Args:
        request: Session creation request
        x_request_id: Optional request ID for tracking
        
    Returns:
        CreateSessionResponse: Created session information
        
    Raises:
        HTTPException: If session creation fails
    """
    request_id = x_request_id or generate_request_id()
    logger.info(f"[{request_id}] Creating new session")
    
    try:
        agent_manager = get_agent_manager()
        
        if not agent_manager:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent manager not initialized"
            )
        
        # Create session
        session_id = agent_manager.create_session(session_id=request.session_id)
        
        logger.info(f"[{request_id}] Session created: {session_id}")
        
        return CreateSessionResponse(
            session_id=session_id,
            status="created",
            message="Session created successfully",
            created_at=format_timestamp(datetime.now()),
            metadata=request.metadata
        )
        
    except AgentInitializationError as e:
        logger.error(f"[{request_id}] Agent initialization error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Agent service unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"[{request_id}] Session creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@router.post(
    "/messages",
    response_model=SendMessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Send Message",
    description="Send a message to the agent in a session"
)
async def send_message(
    request: SendMessageRequest,
    x_request_id: Optional[str] = Header(None)
) -> SendMessageResponse:
    """
    Send a message to the agent.
    
    Args:
        request: Message request
        x_request_id: Optional request ID for tracking
        
    Returns:
        SendMessageResponse: Agent's response
        
    Raises:
        HTTPException: If message sending fails
    """
    request_id = x_request_id or generate_request_id()
    logger.info(f"[{request_id}] Sending message to session: {request.session_id}")
    
    try:
        agent_manager = get_agent_manager()
        
        if not agent_manager:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent manager not initialized"
            )
        
        # Execute agent
        result = await agent_manager.execute(
            session_id=request.session_id,
            message=request.message
        )
        
        logger.info(f"[{request_id}] Message processed successfully")
        
        return SendMessageResponse(
            session_id=request.session_id,
            response=result["response"],
            status="success",
            timestamp=format_timestamp(datetime.now()),
            metadata={
                "request_id": request_id
            }
        )
        
    except SessionNotFoundError as e:
        logger.warning(f"[{request_id}] Session not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except AgentExecutionError as e:
        logger.error(f"[{request_id}] Agent execution error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.post(
    "/messages/stream",
    status_code=status.HTTP_200_OK,
    summary="Send Message (Streaming)",
    description="Send a message to the agent and receive streaming response"
)
async def send_message_stream(
    request: SendMessageRequest,
    x_request_id: Optional[str] = Header(None)
):
    """
    Send a message to the agent with streaming response.
    
    Args:
        request: Message request
        x_request_id: Optional request ID for tracking
        
    Returns:
        StreamingResponse: Server-Sent Events stream of agent response
        
    Raises:
        HTTPException: If message sending fails
    """
    request_id = x_request_id or generate_request_id()
    logger.info(f"[{request_id}] Sending message (streaming) to session: {request.session_id}")
    
    try:
        agent_manager = get_agent_manager()
        
        if not agent_manager:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent manager not initialized"
            )
        
        # Create async generator for SSE
        async def event_generator():
            try:
                async for chunk in agent_manager.execute_stream(
                    session_id=request.session_id,
                    message=request.message
                ):
                    # Send as Server-Sent Event
                    yield f"data: {chunk}\n\n"
                
                # Send done signal
                yield "data: [DONE]\n\n"
                
            except SessionNotFoundError as e:
                logger.warning(f"[{request_id}] Session not found: {str(e)}")
                yield f"event: error\ndata: Session not found\n\n"
            except AgentExecutionError as e:
                logger.error(f"[{request_id}] Agent execution error: {str(e)}")
                yield f"event: error\ndata: Agent execution failed\n\n"
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
                # Client disconnected - this is normal, just log it quietly
                logger.debug(f"[{request_id}] Client disconnected during streaming: {type(e).__name__}")
                return
            except Exception as e:
                logger.error(f"[{request_id}] Unexpected error: {str(e)}")
                yield f"event: error\ndata: {str(e)}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Request-ID": request_id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Failed to initiate streaming: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate streaming: {str(e)}"
        )


@router.get(
    "/sessions",
    response_model=ListSessionsResponse,
    status_code=status.HTTP_200_OK,
    summary="List Sessions",
    description="List all active conversation sessions"
)
async def list_sessions(
    x_request_id: Optional[str] = Header(None)
) -> ListSessionsResponse:
    """
    List all active sessions.
    
    Args:
        x_request_id: Optional request ID for tracking
        
    Returns:
        ListSessionsResponse: List of active sessions
        
    Raises:
        HTTPException: If listing fails
    """
    request_id = x_request_id or generate_request_id()
    logger.info(f"[{request_id}] Listing sessions")
    
    try:
        agent_manager = get_agent_manager()
        
        if not agent_manager:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent manager not initialized"
            )
        
        session_ids = agent_manager.list_sessions()
        
        # Create session info objects
        sessions = [
            SessionInfo(
                session_id=sid,
                created_at=format_timestamp(datetime.now()),  # Would need to track actual creation time
                message_count=0,  # Would need to track message count
                last_activity=format_timestamp(datetime.now())
            )
            for sid in session_ids
        ]
        
        return ListSessionsResponse(
            sessions=sessions,
            total_count=len(sessions),
            status="success"
        )
        
    except Exception as e:
        logger.error(f"[{request_id}] Failed to list sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


@router.delete(
    "/sessions/{session_id}",
    response_model=DeleteSessionResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete Session",
    description="Delete a conversation session"
)
async def delete_session(
    session_id: str,
    x_request_id: Optional[str] = Header(None)
) -> DeleteSessionResponse:
    """
    Delete a session.
    
    Args:
        session_id: Session ID to delete
        x_request_id: Optional request ID for tracking
        
    Returns:
        DeleteSessionResponse: Deletion confirmation
        
    Raises:
        HTTPException: If deletion fails
    """
    request_id = x_request_id or generate_request_id()
    logger.info(f"[{request_id}] Deleting session: {session_id}")
    
    try:
        agent_manager = get_agent_manager()
        
        if not agent_manager:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent manager not initialized"
            )
        
        # Delete session
        deleted = agent_manager.delete_session(session_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}"
            )
        
        logger.info(f"[{request_id}] Session deleted: {session_id}")
        
        return DeleteSessionResponse(
            session_id=session_id,
            status="deleted",
            message="Session deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Failed to delete session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


# Export router
__all__ = ["router"]
