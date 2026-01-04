import logging
from typing import Any

from app.application.services.probabilistic.llm.client.json_utils import extract_json
from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.client.streaming_llm_client import StreamingLLMClient
from app.domain.streaming import StreamSink

logger = logging.getLogger(__name__)

SENTINEL = "\x1f"

STRICT_JSON_SUFFIX = """
    IMPORTANT:
    - RETURN ONLY RAW JSON.
    - NO Markdown.
    - NO explanations.
    - NO backticks.
    - JSON MUST match the schema EXACTLY.
"""

STRICT_TEXT_WITH_JSON_SUFFIX = """
    IMPORTANT:
    - RETURN TEXT {SENTINEL} RAW JSON, IN THIS ORDER.
    - NO explanations.
    - NO backticks.
    - JSON MUST match the schema EXACTLY.
"""


def complete_json(llm: LLMClient, prompt: str) -> dict[str, Any]:
    raw = llm.complete_text(prompt)
    return extract_json(raw)


def call_llm_json(llm: LLMClient, prompt: str, strict_prompt: str | None = None) -> dict[str, Any]:
    try:
        return complete_json(llm, prompt)
    except Exception as e:
        # One retry, stricter instructions
        logger.warning("LLM JSON parse failed, retrying with strict prompt: %s", e)
        if strict_prompt is None:
            strict_prompt = prompt + STRICT_JSON_SUFFIX
        return complete_json(llm, strict_prompt)


def split_text_and_json(raw: str) -> tuple[str, dict[str, Any]]:
    before, after = raw.rsplit(SENTINEL, 1)
    return (before, extract_json(after))


def complete_text_with_json(llm: LLMClient, prompt: str) -> tuple[str, dict[str, Any]]:
    raw = llm.complete_text(prompt)
    logger.info("LLM raw response for text with JSON: %s", raw)
    return split_text_and_json(raw)


def call_llm_text_with_json(
    llm: LLMClient, prompt: str, strict_prompt: str | None = None
) -> tuple[str, dict[str, Any]]:
    try:
        return complete_text_with_json(llm, prompt)
    except Exception as e:
        # One retry, stricter instructions
        logger.warning("LLM text with JSON parse failed, retrying with strict prompt: %s", e)
        if strict_prompt is None:
            strict_prompt = prompt + STRICT_TEXT_WITH_JSON_SUFFIX
        return complete_text_with_json(llm, strict_prompt)


def call_llm_stream_text_with_json(
    llm: StreamingLLMClient, stream: StreamSink, prompt: str
) -> tuple[str, dict[str, Any]]:
    streaming_solution = True
    try:
        raw = ""
        for delta in llm.stream_text(prompt):
            raw += delta

            if streaming_solution:
                if SENTINEL in delta:
                    before, _after = delta.rsplit(SENTINEL, 1)
                    stream(before)
                    streaming_solution = False
                else:
                    stream(delta)

        if streaming_solution:
            # Never saw the sentinel, fallback to non-streaming call
            raise ValueError("LLM streaming response missing sentinel for JSON part")

        return split_text_and_json(raw)

    except Exception as e:
        logger.error(f"Error streaming LLM report solution: {e}")
        logger.error("Falling back to non-streaming LLM call.")
        stream("\n\n⚠️ Streaming failed, regenerating solution…\n\n")

        return call_llm_text_with_json(llm, prompt)
