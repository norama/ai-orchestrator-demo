from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMClient(Protocol):
    def complete_text(self, prompt: str) -> str:
        """
        Complete the given prompt and return the generated text.
        """
        ...
