"""Function middleware that tracks tool calls with timing via contextvars.

The per-request ContextVar collects tool call metadata that the API
endpoints consume to include ``tools_used`` in the response.
"""

import contextvars
import logging
import time
from collections.abc import Awaitable, Callable

from agent_framework import FunctionInvocationContext, FunctionMiddleware

function_logger = logging.getLogger("function")

# Per-request storage for tool call metadata
_tool_calls_var: contextvars.ContextVar[list[dict]] = contextvars.ContextVar(
    "tool_calls", default=[]
)


def reset_tool_calls() -> None:
    """Clear the tool call list for a new request."""
    _tool_calls_var.set([])


def get_tool_calls() -> list[dict]:
    """Return the list of tool calls captured during the current request."""
    return _tool_calls_var.get()


class TrackingFunctionMiddleware(FunctionMiddleware):
    """Logs and tracks each tool call with timing, arguments, and result preview."""

    async def process(
        self,
        context: FunctionInvocationContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        function_name = context.function.name
        arguments = {k: v for k, v in (context.arguments or {}).items()} if context.arguments else {}

        function_logger.info("Calling: %s | args=%s", function_name, arguments)

        start_time = time.time()
        await call_next()
        duration = time.time() - start_time

        result_preview = str(context.result)[:200] if context.result else "None"
        function_logger.info(
            "Completed: %s | duration=%.4fs | result=%s",
            function_name,
            duration,
            result_preview[:100],
        )

        # Capture metadata for the API response
        tool_record = {
            "name": function_name,
            "arguments": arguments,
            "duration_seconds": round(duration, 4),
            "result_preview": result_preview,
        }

        try:
            calls = _tool_calls_var.get()
        except LookupError:
            calls = []
            _tool_calls_var.set(calls)
        calls.append(tool_record)
