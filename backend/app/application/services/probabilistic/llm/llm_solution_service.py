from app.application.solution_service import SolutionService
from app.domain.workflow import Solution, WorkflowContext


class LLMSolutionService(SolutionService):
    def generate_solution(self, ctx: WorkflowContext) -> Solution:
        answers = {s.prompt: s.answer for s in ctx.steps}

        return Solution(
            content=(f"Based on the provided information, here is a proposed solution.\n\nDetails:\n{answers}"),
            confidence=0.6,
            rationale="This is a generic solution without real LLM reasoning yet.",
        )
