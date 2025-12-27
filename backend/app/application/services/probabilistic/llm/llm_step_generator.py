from app.application.step_generator import StepGenerator
from app.domain.workflow import ClarificationStep, NextStepDecision, WorkflowContext


class LLMStepGenerator(StepGenerator):
    def propose_next(self, ctx: WorkflowContext) -> NextStepDecision:
        if len(ctx.steps) == 0:
            return NextStepDecision(
                next_step=ClarificationStep(prompt="What is the exact problem you are facing?"),
                workflow_confidence=1.0,
                reason="Initial clarification",
            )

        if len(ctx.steps) == 1 and ctx.steps[0].answer is not None:
            return NextStepDecision(
                next_step=ClarificationStep(prompt="What environment or system is this related to?"),
                workflow_confidence=0.9,
                reason="Need environment details",
            )

        return NextStepDecision(
            next_step=None,
            workflow_confidence=0.8,
            reason="Enough information collected",
        )
