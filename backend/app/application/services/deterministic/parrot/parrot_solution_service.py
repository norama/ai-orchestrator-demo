from app.application.solution_service import SolutionService
from app.domain.workflow import Solution, WorkflowContext


class ParrotSolutionService(SolutionService):
    def generate_solution(
        self,
        ctx: WorkflowContext,
    ) -> Solution:
        # A deterministic solution generation for testing purposes
        steps = "\n".join(str(step) for step in ctx.steps)
        answer = f"Deterministic solution based on answers:\n{steps}"
        confidence = ctx.last_decision.workflow_confidence if ctx.last_decision else 0.5
        return Solution(content=answer, confidence=confidence, rationale="ParrotSolutionService rationale.")
