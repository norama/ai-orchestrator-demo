from app.application.answer_parser import AnswerParser
from app.domain.workflow import ClarificationStep


class LLMAnswerParser(AnswerParser):
    def parse_answer(self, step: ClarificationStep) -> None:
        pass
