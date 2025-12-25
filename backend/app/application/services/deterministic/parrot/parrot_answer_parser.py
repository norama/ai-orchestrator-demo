from app.application.answer_parser import AnswerParser
from app.domain.workflow import ClarificationStep


class PrinterAnswerParser(AnswerParser):
    def parse_answer(self, step: ClarificationStep) -> None:
        return None
