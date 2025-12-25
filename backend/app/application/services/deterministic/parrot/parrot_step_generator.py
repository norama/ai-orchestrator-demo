from app.application.step_generator import NextStepDecision, StepGenerator
from app.domain.workflow import ClarificationStep, WorkflowContext


class ParrotStepGenerator(StepGenerator):
    def propose_next(
        self,
        ctx: WorkflowContext,
    ) -> NextStepDecision:
        n = len(ctx.steps)
        c = ctx.last_decision.confidence if ctx.last_decision else 0.0
        return NextStepDecision(
            next_step=ClarificationStep(
                prompt=f"Parrot step {n + 1}: Please provide more information.",
            ),
            confidence=(1.0 + c) / 2.0,
            reason="ParrotStepGenerator always opts to add more steps.",
        )
