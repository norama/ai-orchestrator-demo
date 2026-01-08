from uuid import UUID

from fastapi import Depends

from app.application.exceptions import WorkflowNotFound
from app.application.registry import domain_registry
from app.application.workflow_service import WorkflowService
from app.domain.workflow import WorkflowCreate
from app.infrastructure.persistence.sqlite_workflow_repository import (
    SqliteWorkflowRepository,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

# Singleton-ish repo (OK for SQLite demo)
_repo = SqliteWorkflowRepository()


def get_workflow_repository() -> WorkflowRepository:
    return _repo


def get_workflow_service(
    workflow_id: UUID,
    repo: WorkflowRepository = Depends(get_workflow_repository),
) -> WorkflowService:
    workflow = repo.get_workflow(workflow_id)
    if not workflow:
        raise WorkflowNotFound(f"Workflow {workflow_id} not found")

    domain = domain_registry.get(workflow.domain_type)

    return WorkflowService(
        repo=repo,
        domain=domain,
    )


def get_workflow_service_for_creation(
    req: WorkflowCreate,
    repo: WorkflowRepository = Depends(get_workflow_repository),
) -> WorkflowService:
    domain = domain_registry.get(req.domain_type)

    return WorkflowService(
        repo=repo,
        domain=domain,
    )
