from typing import Protocol

from app.domain.workflow import ClarificationStep


class AnswerParser(Protocol):
    def parse_answer(
        self,
        step: ClarificationStep,
    ) -> None:
        """
        Given a step with a raw answer, return the step with
        domain-specific metadata updated (e.g. parsed_answer).

        Must be pure and deterministic.
        """
        ...
