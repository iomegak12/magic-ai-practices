"""Singleton AgentManager — owns the agent, sessions, and execute methods."""

import json
import logging
import time
from datetime import datetime, timezone

from app.config import Settings
from app.middleware.function_logger import get_tool_calls, reset_tool_calls

logger = logging.getLogger("agent")

_manager: "AgentManager | None" = None


class AgentManager:
    """Manages the agent lifecycle and request execution."""

    def __init__(self) -> None:
        self._agent = None
        self._credential = None
        self._history_provider = None
        self._mcp_tools: list = []
        self._sessions: dict = {}
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    async def initialize(self, settings: Settings) -> None:
        """Build the agent and mark the manager as ready."""
        from app.agent.builder import build_agent

        self._agent, self._credential, self._history_provider, self._mcp_tools = build_agent(settings)
        self._initialized = True
        logger.info("AgentManager initialized")

    def _get_or_create_session(self, session_id: str | None):
        """Return an existing session or create a new one."""
        if session_id and session_id in self._sessions:
            logger.info("Resuming session: %s", session_id)
            return self._sessions[session_id]

        session = self._agent.create_session()
        self._sessions[session.session_id] = session
        logger.info("Created new session: %s", session.session_id)
        return session

    async def execute(self, message: str, session_id: str | None = None) -> dict:
        """Run the agent (non-streaming) and return the response with metadata."""
        session = self._get_or_create_session(session_id)
        reset_tool_calls()

        start = time.time()
        result = await self._agent.run(message, session=session)
        duration = time.time() - start

        response_text = str(result) if result else ""
        tools_used = get_tool_calls()

        logger.info(
            "Agent run completed | session=%s | duration=%.2fs | tools=%d",
            session.session_id,
            duration,
            len(tools_used),
        )

        return {
            "session_id": session.session_id,
            "response": response_text,
            "tools_used": tools_used,
            "duration_seconds": round(duration, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    async def execute_stream(self, message: str, session_id: str | None = None):
        """Run the agent with streaming and yield SSE events."""
        session = self._get_or_create_session(session_id)
        reset_tool_calls()

        start = time.time()
        try:
            async for update in self._agent.run(message, session=session, stream=True):
                if update.text:
                    yield f"data: {update.text}\n\n"
        except (ConnectionResetError, BrokenPipeError):
            logger.warning("Client disconnected during streaming")
            return

        duration = time.time() - start
        tools_used = get_tool_calls()

        metadata = {
            "session_id": session.session_id,
            "tools_used": tools_used,
            "duration_seconds": round(duration, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        yield f"event: metadata\ndata: {json.dumps(metadata)}\n\n"
        yield "data: [DONE]\n\n"

        logger.info(
            "Agent stream completed | session=%s | duration=%.2fs | tools=%d",
            session.session_id,
            duration,
            len(tools_used),
        )

    async def shutdown(self) -> None:
        """Clean up resources — MCP tools first, then credential."""
        for mcp_tool in self._mcp_tools:
            try:
                await mcp_tool.close()
                logger.info("Closed MCP tool: %s", mcp_tool.name)
            except Exception:
                logger.warning("Error closing MCP tool '%s'", mcp_tool.name, exc_info=True)
        self._mcp_tools.clear()

        if self._credential:
            await self._credential.close()

        self._sessions.clear()
        self._initialized = False
        logger.info("AgentManager shut down")


async def initialize_manager(settings: Settings) -> AgentManager:
    """Create and initialize the global AgentManager singleton."""
    global _manager  # noqa: PLW0603
    _manager = AgentManager()
    await _manager.initialize(settings)
    return _manager


def get_manager() -> AgentManager:
    """Return the global AgentManager. Raises if not initialized."""
    if _manager is None or not _manager.is_initialized:
        raise RuntimeError("AgentManager has not been initialized")
    return _manager


async def shutdown_manager() -> None:
    """Shut down the global AgentManager."""
    global _manager  # noqa: PLW0603
    if _manager:
        await _manager.shutdown()
        _manager = None
