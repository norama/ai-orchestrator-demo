from app.application.answer_parser import AnswerParser
from app.application.services.deterministic.printer.domain.printer_domain import PrinterStepMetadata
from app.application.services.deterministic.printer.domain.printer_domain_parser import parse_printer_answer
from app.domain.workflow import ClarificationStep


class PrinterAnswerParser(AnswerParser):
    def parse_answer(self, step: ClarificationStep) -> None:
        meta = PrinterStepMetadata.model_validate(step.metadata)

        parsed = parse_printer_answer(
            raw=step.answer or "",
            expected=meta.expected_answer,
        )

        meta.parsed_answer = parsed

        step.metadata = meta.model_dump()
