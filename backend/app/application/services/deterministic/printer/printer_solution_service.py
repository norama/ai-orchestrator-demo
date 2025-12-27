from app.application.services.deterministic.printer.domain.printer_domain import (
    PrinterExpectedAnswer,
    PrinterParsedAnswer,
    PrinterStepMetadata,
)
from app.application.solution_service import SolutionService
from app.domain.workflow import Solution, WorkflowContext


class PrinterSolutionService(SolutionService):
    def generate_solution(self, ctx: WorkflowContext) -> Solution:
        steps = ctx.steps

        summary = "\n".join(f"- {s.prompt} → {s.answer}" for s in steps)

        yes_no_step = next(
            (
                step
                for step in reversed(steps)
                if PrinterStepMetadata.model_validate(step.metadata).expected_answer == PrinterExpectedAnswer.YES_NO
            ),
            None,
        )

        # Infer outcome
        likely_cause = None
        recommendations = None
        if yes_no_step:
            metadata = PrinterStepMetadata.model_validate(yes_no_step.metadata)
            parsed_answer = metadata.parsed_answer
            if parsed_answer == PrinterParsedAnswer.YES:
                likely_cause = "The print queue was blocked."
                recommendations = [
                    "Clear the print queue.",
                    "Restart the print spooler service.",
                ]
            elif parsed_answer == PrinterParsedAnswer.NO:
                likely_cause = "The printer connection or service was inactive."
                recommendations = [
                    "Restart the printer.",
                    "Check printer network connectivity.",
                ]
        if not likely_cause:
            likely_cause = "Unable to determine the issue from the provided information."
        if not recommendations:
            recommendations = [
                "Ensure the printer is powered on and connected.",
                "Check for any error messages on the printer display.",
            ]

        free_text_step = next(
            (
                step
                for step in reversed(steps)
                if PrinterStepMetadata.model_validate(step.metadata).expected_answer == PrinterExpectedAnswer.FREE_TEXT
            ),
            None,
        )

        additional_info = free_text_step.answer if free_text_step else "No additional information provided."

        content = f"""
            Investigation summary:
            {summary}

            Likely cause:
            {likely_cause}

            Recommended steps:
            {recommendations}

            Additional information:
            {additional_info}
        """

        confidence = 0.9 if yes_no_step and yes_no_step.answer else 0.6

        return Solution(
            content=content.strip(),
            confidence=confidence,
            rationale="Conclusion derived from observed printer behavior.",
        )
