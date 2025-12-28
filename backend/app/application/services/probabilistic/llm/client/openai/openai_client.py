from typing import Any, Callable, override

from openai import OpenAI

from app.application.services.probabilistic.llm.client.json_utils import extract_json
from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.domain.llm_stats import LLMUsage


class OpenAIClient(LLMClient):
    def __init__(
        self,
        client: OpenAI | None = None,
        *,
        model: str = "gpt-4.1-mini",
        on_usage: Callable[[LLMUsage], None] | None = None,
    ) -> None:
        self.client = client or OpenAI()
        self.model = model
        self.on_usage = on_usage

    @override
    def complete(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        if self.on_usage and response.usage:
            self.on_usage(
                LLMUsage(
                    prompt_tokens=response.usage.input_tokens,
                    completion_tokens=response.usage.output_tokens,
                    total_tokens=response.usage.total_tokens,
                    model=response.model,
                )
            )

        if not response.output_text:
            raise RuntimeError("Empty LLM response")

        return response.output_text.strip()

    @override
    def complete_json(self, prompt: str) -> dict[str, Any]:
        raw = self.complete(prompt)
        return extract_json(raw)
