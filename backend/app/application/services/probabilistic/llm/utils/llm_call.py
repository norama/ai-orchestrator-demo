import logging
from typing import Any

from app.application.services.probabilistic.llm.client.llm_client import LLMClient

logger = logging.getLogger(__name__)

STRICT_JSON_SUFFIX = """
    IMPORTANT:
    - RETURN ONLY RAW JSON.
    - NO Markdown.
    - NO explanations.
    - NO backticks.
    - JSON MUST match the schema EXACTLY.
"""


def call_llm_json(llm: LLMClient, prompt: str, strict_prompt: str | None = None) -> dict[str, Any]:
    try:
        return llm.complete_json(prompt)
    except Exception as e:
        # One retry, stricter instructions
        logger.warning("LLM JSON parse failed, retrying with strict prompt: %s", e)
        if strict_prompt is None:
            strict_prompt = prompt + STRICT_JSON_SUFFIX
        return llm.complete_json(strict_prompt)
