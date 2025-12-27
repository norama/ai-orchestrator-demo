from app.application.services.deterministic.printer.domain.printer_domain import (
    PrinterExpectedAnswer,
    PrinterParsedAnswer,
    PrinterStepMetadata,
    PrinterStepPhase,
)
from app.application.step_generator import StepGenerator
from app.domain.workflow import ClarificationStep, NextStepDecision, WorkflowContext


class PrinterStepGenerator(StepGenerator):
    def propose_next(self, ctx: WorkflowContext) -> NextStepDecision:
        steps = ctx.steps

        # Step 1: initial observation
        if not steps:
            return NextStepDecision(
                next_step=ClarificationStep(
                    prompt="Do you see the print job in the printer queue?",
                    metadata=PrinterStepMetadata(
                        phase=PrinterStepPhase.INITIAL, expected_answer=PrinterExpectedAnswer.YES_NO
                    ).model_dump(),
                ),
                workflow_confidence=0.2,
                reason="Initial observation required.",
            )

        last = steps[-1]

        if not last.answer:
            raise RuntimeError("Last step has no answer.")

        metadata = PrinterStepMetadata.model_validate(last.metadata)

        parsed_answer = metadata.parsed_answer

        if metadata.expected_answer == PrinterExpectedAnswer.YES_NO:
            # Branch: job visible
            if parsed_answer == PrinterParsedAnswer.YES:
                return NextStepDecision(
                    next_step=ClarificationStep(
                        prompt="Please clear the print queue and retry printing. What happens?",
                        metadata=PrinterStepMetadata(
                            phase=PrinterStepPhase.IN_PROGRESS, expected_answer=PrinterExpectedAnswer.FREE_TEXT
                        ).model_dump(),
                    ),
                    workflow_confidence=0.6,
                    reason="Queue blockage suspected.",
                )

            # Branch: job not visible
            if parsed_answer == PrinterParsedAnswer.NO:
                return NextStepDecision(
                    next_step=ClarificationStep(
                        prompt="Please restart the printer and retry printing. What happens?",
                        metadata=PrinterStepMetadata(
                            phase=PrinterStepPhase.IN_PROGRESS, expected_answer=PrinterExpectedAnswer.FREE_TEXT
                        ).model_dump(),
                    ),
                    workflow_confidence=0.6,
                    reason="Connection or spooler issue suspected.",
                )

            # Unclear answer → ask for clarification
            return NextStepDecision(
                next_step=ClarificationStep(
                    prompt="Please answer with 'yes' or 'no'. Do you see the print job in the queue?",
                    metadata=PrinterStepMetadata(
                        phase=PrinterStepPhase.IN_PROGRESS, expected_answer=PrinterExpectedAnswer.YES_NO
                    ).model_dump(),
                ),
                workflow_confidence=0.3,
                reason="Initial answer unclear.",
            )

        if metadata.expected_answer == PrinterExpectedAnswer.FREE_TEXT:
            return NextStepDecision(next_step=None, workflow_confidence=0.9, reason="Sufficient information collected.")

        # Safety fallback (should not normally happen)
        raise RuntimeError("Unhandled printer troubleshooting state.")
