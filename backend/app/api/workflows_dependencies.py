import re
from uuid import UUID

from fastapi import Depends, Header

from app.application.exceptions import InvalidWorkspaceId, MissingWorkspaceId, WorkflowNotFound
from app.application.registry import domain_registry
from app.application.workflow_service import WorkflowService
from app.domain.workflow import WorkflowCreate
from app.infrastructure.persistence.sqlite_workflow_repository import (
    SqliteWorkflowRepository,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

WORKSPACE_RE = re.compile(r"^ws_[a-zA-Z0-9\-]+$")


def get_workspace_id(
    x_workspace_id: str | None = Header(default=None),
) -> str:
    if not x_workspace_id:
        raise MissingWorkspaceId("Missing workspace id")

    if not WORKSPACE_RE.match(x_workspace_id):
        raise InvalidWorkspaceId("Invalid workspace id")

    return x_workspace_id


def get_workflow_repository(
    workspace_id: str = Depends(get_workspace_id),
) -> WorkflowRepository:
    return SqliteWorkflowRepository(workspace_id=workspace_id)


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
