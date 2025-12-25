from fastapi import Depends

from app.application.answer_parser import AnswerParser
from app.application.services.deterministic.printer.printer_answer_parser import PrinterAnswerParser
from app.application.services.deterministic.printer.printer_solution_service import PrinterSolutionService
from app.application.services.deterministic.printer.printer_step_generator import PrinterStepGenerator
from app.application.solution_service import SolutionService
from app.application.step_generator import StepGenerator
from app.application.workflow_service import WorkflowService
from app.infrastructure.persistence.sqlite_workflow_repository import (
    SqliteWorkflowRepository,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

# Singleton-ish repo (OK for SQLite demo)
_repo = SqliteWorkflowRepository()


def get_workflow_repository() -> WorkflowRepository:
    return _repo


def get_step_generator() -> StepGenerator:
    return PrinterStepGenerator()


def get_solution_service() -> SolutionService:
    return PrinterSolutionService()


def get_answer_parser() -> AnswerParser:
    return PrinterAnswerParser()


def get_workflow_service(
    repo: WorkflowRepository = Depends(get_workflow_repository),
    step_generator: StepGenerator = Depends(get_step_generator),
    solution_service: SolutionService = Depends(get_solution_service),
    answer_parser: AnswerParser = Depends(get_answer_parser),
) -> WorkflowService:
    return WorkflowService(
        repo=repo,
        step_generator=step_generator,
        solution_service=solution_service,
        answer_parser=answer_parser,
    )
