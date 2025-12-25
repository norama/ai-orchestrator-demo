from app.application.answer_parser import AnswerParser
from app.domain.workflow import ClarificationStep


class ParrotAnswerParser(AnswerParser):
    def parse_answer(self, step: ClarificationStep) -> None:
        return None
