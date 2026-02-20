"""
Chat Endpoint

Handles conversational interactions with the customer service agent.
Supports both streaming and non-streaming responses.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from datetime import datetime
import asyncio
import json

from ..schemas import ChatRequest, ChatResponse, ErrorResponse
from ..services.agent_service import get_agent_service
from ..services.session_manager import get_session_manager

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Customer Service Agent",
    description="Send a message to the AI customer service agent. Supports multi-turn conversations and streaming."
)
async def chat(request: ChatRequest):
    """
    Chat endpoint for conversational AI interactions.
    
    Supports:
    - Multi-turn conversations using session_id
    - Non-streaming responses (default)
    - Streaming responses via SSE (when stream=true)
    
    Args:
        request: ChatRequest with message, optional session_id, and stream flag
        
    Returns:
        ChatResponse with agent's reply and metadata
        
    Raises:
        HTTPException: If agent execution fails
    """
    session_manager = get_session_manager()
    agent_service = get_agent_service()
    
    # Get or create session
    session_id, session = session_manager.get_or_create_session(request.session_id)
    
    try:
        if request.stream:
            # Streaming response using Server-Sent Events
            return StreamingResponse(
                _stream_response(request.message, session, session_id, agent_service, session_manager),
                media_type="text/event-stream"
            )
        else:
            # Non-streaming response
            agent_response = await agent_service.run(request.message, session)
            session_manager.increment_turn(session_id)
            
            # Convert AgentResponse to string for Pydantic validation
            response_text = str(agent_response)
            
            return ChatResponse(
                session_id=session_id,
                response=response_text,
                timestamp=datetime.now(),
                metadata={
                    "turn_count": session_manager.get_turn_count(session_id),
                    "tools_used": [],  # TODO: Track tool calls from agent
                    "tokens_used": 0,   # TODO: Track token usage
                    "streaming": False
                }
            )
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"❌ Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )


async def _stream_response(
    message: str,
    session,
    session_id: str,
    agent_service,
    session_manager
):
    """
    Generator for streaming responses using Server-Sent Events.
    
    Args:
        message: User message
        session: Agent session
        session_id: Session identifier
        agent_service: Agent service instance
        session_manager: Session manager instance
        
    Yields:
        SSE formatted events with response chunks
    """
    try:
        # Note: Streaming implementation depends on agent framework's streaming support
        # For now, we'll implement a simple chunk-based streaming
        
        agent_response = await agent_service.run(message, session)
        session_manager.increment_turn(session_id)
        
        # Convert AgentResponse to string
        response_text = str(agent_response)
        
        # Split response into chunks for streaming effect
        words = response_text.split()
        chunk_size = 3  # Words per chunk
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            if i + chunk_size < len(words):
                chunk += " "
            
            # Send SSE event
            event_data = {
                "chunk": chunk,
                "session_id": session_id
            }
            yield f"event: message\ndata: {json.dumps(event_data)}\n\n"
            
            # Small delay to simulate streaming
            await asyncio.sleep(0.05)
        
        # Send completion event
        completion_data = {
            "session_id": session_id,
            "metadata": {
                "turn_count": session_manager.get_turn_count(session_id),
                "streaming": True
            }
        }
        yield f"event: done\ndata: {json.dumps(completion_data)}\n\n"
        
    except Exception as e:
        error_data = {
            "error": str(e),
            "session_id": session_id
        }
        yield f"event: error\ndata: {json.dumps(error_data)}\n\n"
