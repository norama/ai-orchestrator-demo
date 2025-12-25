from fastapi import Depends

from app.application.services.deterministic.parrot.parrot_solution_service import (
    ParrotSolutionService,
)
from app.application.services.deterministic.parrot.parrot_step_generator import (
    ParrotStepGenerator,
)
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
    return ParrotStepGenerator()


def get_solution_service() -> SolutionService:
    return ParrotSolutionService()


def get_workflow_service(
    repo: WorkflowRepository = Depends(get_workflow_repository),
    step_generator: StepGenerator = Depends(get_step_generator),
    solution_service: SolutionService = Depends(get_solution_service),
) -> WorkflowService:
    return WorkflowService(repo=repo, step_generator=step_generator, solution_service=solution_service)
