from typing import Protocol

from app.domain.workflow import Solution, WorkflowContext


class SolutionService(Protocol):
    def generate_solution(
        self,
        ctx: WorkflowContext,
    ) -> Solution:
        """
        Generate a solution draft based on collected steps.
        """
        ...
