"""Middleware classes for guardrailing, exception handling, and logging."""

import logging
import time
from collections.abc import Awaitable, Callable

from agent_framework import (
    AgentContext,
    AgentMiddleware,
    AgentResponse,
    FunctionInvocationContext,
    FunctionMiddleware,
    Message,
)

from prompts import INPUT_GUARDRAIL_SYSTEM_PROMPT, OUTPUT_GUARDRAIL_SYSTEM_PROMPT

guardrail_logger = logging.getLogger("guardrail")
function_logger = logging.getLogger("function")
agent_logger = logging.getLogger("agent")


# ---------------------------------------------------------------------------
# Input Guardrail
# ---------------------------------------------------------------------------

class LLMInputGuardrailMiddleware(AgentMiddleware):
    """Agent middleware that uses LLM classification to validate user input.

    Intercepts the user's query BEFORE the agent processes it. Sends the query
    to the LLM classifier and blocks unsafe requests with a polite refusal.
    """

    REFUSAL_MESSAGES = {
        "sensitive_pii": (
            "I cannot process requests that contain or ask for sensitive information "
            "such as passwords, API keys, or personal data. Please rephrase your question."
        ),
        "toxic_harmful": (
            "I cannot process messages that contain harmful, abusive, or inappropriate "
            "content. Please rephrase your question respectfully."
        ),
        "prompt_injection": (
            "I cannot process requests that attempt to manipulate my instructions or "
            "behavior. Please ask a genuine question."
        ),
        "off_topic": (
            "I'm a technology-focused assistant. I can only help with topics related to "
            "Weather Information, IT, Computer Science, Software Engineering, and Technology. "
            "Please ask a relevant question."
        ),
    }

    def __init__(self, classify_fn: Callable[[str, str], dict]):
        self.classify_fn = classify_fn

    async def process(
        self,
        context: AgentContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        last_message = context.messages[-1] if context.messages else None

        if last_message and last_message.text:
            query = last_message.text
            display = f"'{query[:80]}...'" if len(query) > 80 else f"'{query}'"
            guardrail_logger.info(f"[INPUT] Classifying: {display}")

            classification = self.classify_fn(query, INPUT_GUARDRAIL_SYSTEM_PROMPT)

            if not classification.get("safe", True):
                category = classification.get("category", "unknown")
                reason = classification.get("reason", "No reason provided.")
                guardrail_logger.warning(
                    f"[INPUT] BLOCKED | category={category} | reason={reason}"
                )
                refusal = self.REFUSAL_MESSAGES.get(
                    category,
                    "Your request has been blocked by the safety filter.",
                )
                context.result = AgentResponse(
                    messages=[Message(role="assistant", contents=[refusal])]
                )
                return  # Do NOT call call_next() — blocks the request

            guardrail_logger.info(
                f"[INPUT] PASSED | reason={classification.get('reason', '')}"
            )

        await call_next()


# ---------------------------------------------------------------------------
# Output Guardrail
# ---------------------------------------------------------------------------

class LLMOutputGuardrailMiddleware(AgentMiddleware):
    """Agent middleware that validates agent output using LLM classification.

    Lets the agent generate its response first, then validates the output
    through the LLM classifier. Replaces unsafe output with a safe fallback.
    """

    FALLBACK_MESSAGE = (
        "I apologize, but I'm unable to provide that response as it was flagged "
        "by our safety filter. Please try rephrasing your question."
    )

    def __init__(self, classify_fn: Callable[[str, str], dict]):
        self.classify_fn = classify_fn

    async def process(
        self,
        context: AgentContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        await call_next()

        if context.result and context.result.messages:
            response_text = (
                context.result.messages[-1].text
                if context.result.messages[-1].text
                else ""
            )

            if response_text:
                display = (
                    f"'{response_text[:80]}...'"
                    if len(response_text) > 80
                    else f"'{response_text}'"
                )
                guardrail_logger.info(f"[OUTPUT] Classifying response: {display}")

                classification = self.classify_fn(
                    response_text, OUTPUT_GUARDRAIL_SYSTEM_PROMPT
                )

                if not classification.get("safe", True):
                    category = classification.get("category", "unknown")
                    reason = classification.get("reason", "No reason provided.")
                    guardrail_logger.warning(
                        f"[OUTPUT] BLOCKED | category={category} | reason={reason}"
                    )
                    context.result = AgentResponse(
                        messages=[
                            Message(role="assistant", contents=[self.FALLBACK_MESSAGE])
                        ]
                    )
                    return

                guardrail_logger.info(
                    f"[OUTPUT] APPROVED | reason={classification.get('reason', '')}"
                )


# ---------------------------------------------------------------------------
# Exception Handling
# ---------------------------------------------------------------------------

class ExceptionHandlingMiddleware(AgentMiddleware):
    """Agent-level catch-all middleware that handles unhandled exceptions.

    Wraps downstream execution in try/except. On any exception, logs full
    error details for debugging and returns a polished, user-friendly message
    with NO internal error details leaked.
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
                f"[EXCEPTION] {type(e).__name__}: {e}", exc_info=True
            )
            context.result = AgentResponse(
                messages=[Message(role="assistant", contents=[self.POLISHED_MESSAGE])]
            )


# ---------------------------------------------------------------------------
# Function Logging
# ---------------------------------------------------------------------------

class LoggingFunctionMiddleware(FunctionMiddleware):
    """Function middleware that logs tool calls with timing and details."""

    async def process(
        self,
        context: FunctionInvocationContext,
        call_next: Callable[[], Awaitable[None]],
    ) -> None:
        function_name = context.function.name
        function_logger.info(
            f"Calling: {function_name} | args={context.arguments}"
        )

        start_time = time.time()
        await call_next()
        duration = time.time() - start_time

        result_preview = str(context.result)[:100] if context.result else "None"
        function_logger.info(
            f"Completed: {function_name} | duration={duration:.4f}s | result={result_preview}"
        )
