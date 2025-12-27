from app.application.answer_parser import AnswerParser
from app.application.solution_service import SolutionService
from app.application.step_generator import StepGenerator
from app.domain.workflow import ClarificationStep, NextStepDecision, Solution, WorkflowContext


class FakeAnswerParser(AnswerParser):
    def parse_answer(self, step: ClarificationStep) -> None:
        return None


class FakeStepGenerator(StepGenerator):
    def propose_next(self, ctx: WorkflowContext) -> NextStepDecision:
        if not ctx.steps:
            return NextStepDecision(
                next_step=ClarificationStep(prompt="Q1"),
                workflow_confidence=0.1,
                reason="initial",
            )
        return NextStepDecision(
            next_step=None,
            workflow_confidence=1.0,
            reason="done",
        )


class FakeSolutionService(SolutionService):
    def generate_solution(self, ctx: WorkflowContext) -> Solution:
        return Solution(
            content="Solved",
            confidence=1.0,
            rationale="Fake solver",
        )
