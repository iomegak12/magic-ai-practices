"""LLM-based guardrail classifier using Azure OpenAI."""

import json
import logging

from openai import AzureOpenAI

logger = logging.getLogger("guardrail")


def create_guardrail_client(
    azure_endpoint: str,
    api_key: str,
    api_version: str = "2025-03-01-preview",
) -> AzureOpenAI:
    """Create an AzureOpenAI client for guardrail classification calls."""
    return AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )


def classify_text(
    client: AzureOpenAI,
    model: str,
    text: str,
    system_prompt: str,
) -> dict:
    """Send text to the LLM for guardrail classification.

    Returns a dict with keys: safe (bool), category (str|None), reason (str).
    Fails open on error — if classification fails, the request is allowed through.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.0,
            max_tokens=200,
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Guardrail classification failed: {e}")
        return {"safe": True, "category": None, "reason": f"Classification error: {e}"}
