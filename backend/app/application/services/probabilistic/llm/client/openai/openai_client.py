from typing import Callable, Iterator, override

from openai import OpenAI

from app.application.services.probabilistic.llm.client.streaming_llm_client import StreamingLLMClient
from app.application.services.probabilistic.llm.domain.llm_stats import LLMUsage


class OpenAIClient(StreamingLLMClient):
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
    def complete_text(self, prompt: str) -> str:
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
    def stream_text(self, prompt: str) -> Iterator[str]:
        """
        Synchronous streaming of raw text deltas.
        """
        with self.client.responses.stream(
            model=self.model,
            input=prompt,
        ) as stream:
            for event in stream:
                if event.type == "response.output_text.delta":
                    if event.delta:
                        yield event.delta

                elif event.type == "response.completed":
                    if self.on_usage and event.response.usage:
                        self.on_usage(
                            LLMUsage(
                                prompt_tokens=event.response.usage.input_tokens,
                                completion_tokens=event.response.usage.output_tokens,
                                total_tokens=event.response.usage.total_tokens,
                                model=event.response.model,
                            )
                        )
