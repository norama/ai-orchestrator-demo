import logging

from app.application.solution_service import SolutionService
from app.domain.streaming import StreamSink
from app.domain.workflow import Solution, WorkflowContext

logger = logging.getLogger(__name__)


class ParrotSolutionService(SolutionService):
    def generate_solution(self, ctx: WorkflowContext, stream: StreamSink | None = None) -> Solution:
        # A deterministic solution generation for testing purposes
        if stream:
            logger.warning("Streaming not supported in ParrotSolutionService; ignoring stream parameter.")

        steps = "\n".join(str(step) for step in ctx.steps)
        chat_history = "\n".join(f"{msg.role.value}: {msg.content}" for msg in ctx.chat_history.messages)
        answer = f"Deterministic solution based on answers:\n{steps}\n\nChat History:\n{chat_history}"
        confidence = ctx.last_decision.workflow_confidence if ctx.last_decision else 0.5
        return Solution(content=answer, confidence=confidence, rationale="ParrotSolutionService rationale.")
