"""Chat endpoints — non-streaming and SSE streaming."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.agent.manager import get_manager
from app.api.errors import AgentExecutionError
from app.api.models import ChatRequest, ChatResponse, ErrorResponse, ToolCallInfo

logger = logging.getLogger("api")

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        502: {"model": ErrorResponse, "description": "Agent execution error"},
        503: {"model": ErrorResponse, "description": "Agent not initialized"},
    },
    summary="Send a message (non-streaming)",
    description="Send a message to the agent and receive the complete response "
    "along with tool usage metadata and timing information.",
)
async def chat(body: ChatRequest, request: Request) -> ChatResponse:
    manager = get_manager()

    try:
        result = await manager.execute(
            message=body.message,
            session_id=body.session_id,
        )
    except Exception as exc:
        logger.error("Agent execution failed: %s", exc, exc_info=True)
        raise AgentExecutionError(str(exc)) from exc

    return ChatResponse(
        session_id=result["session_id"],
        response=result["response"],
        tools_used=[ToolCallInfo(**tc) for tc in result["tools_used"]],
        duration_seconds=result["duration_seconds"],
        timestamp=result["timestamp"],
    )


@router.post(
    "/stream",
    responses={
        200: {
            "description": "SSE stream of agent response tokens, followed by a "
            "`metadata` event containing tool usage and timing, ending with `[DONE]`.",
            "content": {"text/event-stream": {}},
        },
        422: {"model": ErrorResponse, "description": "Validation error"},
        502: {"model": ErrorResponse, "description": "Agent execution error"},
        503: {"model": ErrorResponse, "description": "Agent not initialized"},
    },
    summary="Send a message (SSE streaming)",
    description="Send a message to the agent and receive tokens as Server-Sent Events. "
    "A final `event: metadata` carries tool usage details before the `[DONE]` sentinel.",
)
async def chat_stream(body: ChatRequest, request: Request):
    manager = get_manager()

    async def event_generator():
        try:
            async for chunk in manager.execute_stream(
                message=body.message,
                session_id=body.session_id,
            ):
                if await request.is_disconnected():
                    logger.info("Client disconnected during streaming")
                    return
                yield chunk
        except Exception as exc:
            logger.error("Streaming error: %s", exc, exc_info=True)
            yield f"event: error\ndata: {exc!s}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
