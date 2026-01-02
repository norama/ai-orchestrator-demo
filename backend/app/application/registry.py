import logging
from typing import NamedTuple

from app.application.answer_parser import AnswerParser
from app.application.chat_service import ChatService
from app.application.services.deterministic.parrot.parrot_chat_service import ParrotChatService
from app.application.services.deterministic.parrot.parrot_solution_service import ParrotSolutionService
from app.application.services.deterministic.parrot.parrot_step_generator import ParrotStepGenerator
from app.application.services.deterministic.printer.printer_answer_parser import PrinterAnswerParser
from app.application.services.deterministic.printer.printer_solution_service import PrinterSolutionService
from app.application.services.deterministic.printer.printer_step_generator import PrinterStepGenerator
from app.application.services.probabilistic.llm.client.openai.openai_client import OpenAIClient
from app.application.services.probabilistic.llm.domain.llm_stats import LLMUsage
from app.application.services.probabilistic.llm.support.llm_support_chat_service import LLMSupportChatService
from app.application.services.probabilistic.llm.support.llm_support_solution_service import LLMSupportSolutionService
from app.application.services.probabilistic.llm.support.llm_support_step_generator import LLMSupportStepGenerator
from app.application.solution_service import SolutionService
from app.application.step_generator import StepGenerator
from app.domain.config import DomainType

logger = logging.getLogger(__name__)


class WorkflowDomain(NamedTuple):
    step_generator: StepGenerator
    solution_service: SolutionService
    answer_parser: AnswerParser | None = None
    chat_service: ChatService | None = None


class DomainRegistry:
    def __init__(self):
        self._domains: dict[DomainType, WorkflowDomain] = {}

    def register(self, domain: DomainType, bundle: WorkflowDomain) -> None:
        self._domains[domain] = bundle

    def get(self, domain: DomainType) -> WorkflowDomain:
        if domain not in self._domains:
            raise ValueError(f"Domain {domain} not registered")
        return self._domains[domain]


domain_registry = DomainRegistry()

domain_registry.register(
    DomainType.PARROT,
    WorkflowDomain(
        step_generator=ParrotStepGenerator(),
        solution_service=ParrotSolutionService(),
        chat_service=ParrotChatService(),
    ),
)

domain_registry.register(
    DomainType.PRINTER,
    WorkflowDomain(
        step_generator=PrinterStepGenerator(),
        answer_parser=PrinterAnswerParser(),
        solution_service=PrinterSolutionService(),
    ),
)


def create_llm_client() -> OpenAIClient:
    def log_usage(usage: LLMUsage):
        logger.info(
            "model=%s tokens=%s",
            usage.model,
            usage.total_tokens,
        )

    return OpenAIClient(on_usage=log_usage)


llm_client = create_llm_client()

domain_registry.register(
    DomainType.LLM_SUPPORT,
    WorkflowDomain(
        step_generator=LLMSupportStepGenerator(llm_client),
        solution_service=LLMSupportSolutionService(llm_client),
        chat_service=LLMSupportChatService(llm_client),
    ),
)
