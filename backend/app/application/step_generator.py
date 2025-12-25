from typing import Protocol

from app.domain.workflow import NextStepDecision, WorkflowContext


class StepGenerator(Protocol):
    def propose_next(
        self,
        ctx: WorkflowContext,
    ) -> NextStepDecision:
        """
        Decide whether another clarification step is needed.

        Returns:
        - next_step: ClarificationStep | None
        - confidence: float (0.0-1.0)
        - reason: human-readable explanation
        """
        ...
