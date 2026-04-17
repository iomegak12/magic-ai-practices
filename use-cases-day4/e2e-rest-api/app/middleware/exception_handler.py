"""Agent-level catch-all middleware for unhandled exceptions."""

import logging
from collections.abc import Awaitable, Callable

from agent_framework import AgentContext, AgentMiddleware, AgentResponse, Message

agent_logger = logging.getLogger("agent")


class ExceptionHandlingMiddleware(AgentMiddleware):
    """Wraps downstream execution in try/except.

    On any exception, logs full error details for debugging and returns
    a polished, user-friendly message with NO internal error details leaked.
    """

    POLISHED_MESSAGE = (
        "We encountered an unexpected issue processing your request. "
        "Please try again later. If the problem persists, contact support."
    )

    async def process(
        self,
        context: AgentContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        try:
            await call_next()
        except Exception as e:
            agent_logger.error(
                "[EXCEPTION] %s: %s", type(e).__name__, e, exc_info=True
            )
            context.result = AgentResponse(
                messages=[Message(role="assistant", contents=[self.POLISHED_MESSAGE])]
            )
