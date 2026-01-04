from typing import Iterator

from app.application.services.probabilistic.llm.client.llm_client import LLMClient


class StreamingLLMClient(LLMClient):
    def stream_text(self, prompt: str) -> Iterator[str]:
        """
        Stream raw text deltas for the given prompt.
        """
        ...
