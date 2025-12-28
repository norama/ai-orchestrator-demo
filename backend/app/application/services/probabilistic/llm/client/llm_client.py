from typing import Any

from typing_extensions import Protocol


class LLMClient(Protocol):
    def complete(self, prompt: str) -> str:
        """
        Complete the given prompt and return the generated text.
        """
        ...

    def complete_json(self, prompt: str) -> dict[str, Any]:
        """
        Complete the given prompt and return the generated JSON.
        """
        ...
