from typing import Any, override

from openai import OpenAI

from app.application.services.probabilistic.llm.client.json_utils import extract_json
from app.application.services.probabilistic.llm.client.llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI()

    @override
    def complete(self, prompt: str) -> str:
        resp = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )
        if not resp.output_text:
            raise RuntimeError("Empty LLM response")
        return resp.output_text.strip()

    @override
    def complete_json(self, prompt: str) -> dict[str, Any]:
        raw = self.complete(prompt)
        return extract_json(raw)
