from typing import Protocol

from pydantic import BaseModel

from app.domain.workflow import ClarificationStep, WorkflowContext


class NextStepDecision(BaseModel):
    next_step: ClarificationStep | None
    confidence: float
    reason: str


class StepGenerator(Protocol):
    def propose_next(
        self,
        ctx: WorkflowContext,
    ) -> NextStepDecision:
        """
        Decide whether another clarification step is needed.

        Returns:
        - next_step: ClarificationStep | None
        - confidence: float (0.0–1.0)
        - reason: human-readable explanation
        """
        ...
