from typing import Protocol

from app.domain.streaming import StreamSink
from app.domain.workflow import Solution, WorkflowContext


class SolutionService(Protocol):
    def generate_solution(self, ctx: WorkflowContext, stream: StreamSink | None = None) -> Solution:
        """
        Generate a solution draft based on collected steps.
        """
        ...
