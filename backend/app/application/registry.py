from typing import NamedTuple

from app.application.answer_parser import AnswerParser
from app.application.services.deterministic.parrot.parrot_answer_parser import ParrotAnswerParser
from app.application.services.deterministic.parrot.parrot_solution_service import ParrotSolutionService
from app.application.services.deterministic.parrot.parrot_step_generator import ParrotStepGenerator
from app.application.services.deterministic.printer.printer_answer_parser import PrinterAnswerParser
from app.application.services.deterministic.printer.printer_solution_service import PrinterSolutionService
from app.application.services.deterministic.printer.printer_step_generator import PrinterStepGenerator
from app.application.services.probabilistic.llm.llm_answer_parser import LLMAnswerParser
from app.application.services.probabilistic.llm.llm_solution_service import LLMSolutionService
from app.application.services.probabilistic.llm.llm_step_generator import LLMStepGenerator
from app.application.solution_service import SolutionService
from app.application.step_generator import StepGenerator
from app.domain.config import DomainType


class DomainBundle(NamedTuple):
    step_generator: StepGenerator
    answer_parser: AnswerParser
    solution_service: SolutionService


class DomainRegistry:
    def __init__(self):
        self._domains: dict[DomainType, DomainBundle] = {}

    def register(self, domain: DomainType, bundle: DomainBundle) -> None:
        self._domains[domain] = bundle

    def get(self, domain: DomainType) -> DomainBundle:
        if domain not in self._domains:
            raise ValueError(f"Domain {domain} not registered")
        return self._domains[domain]


domain_registry = DomainRegistry()

domain_registry.register(
    DomainType.PARROT,
    DomainBundle(
        step_generator=ParrotStepGenerator(),
        answer_parser=ParrotAnswerParser(),
        solution_service=ParrotSolutionService(),
    ),
)

domain_registry.register(
    DomainType.PRINTER,
    DomainBundle(
        step_generator=PrinterStepGenerator(),
        answer_parser=PrinterAnswerParser(),
        solution_service=PrinterSolutionService(),
    ),
)

domain_registry.register(
    DomainType.LLM_SUPPORT,
    DomainBundle(
        step_generator=LLMStepGenerator(),
        answer_parser=LLMAnswerParser(),
        solution_service=LLMSolutionService(),
    ),
)
