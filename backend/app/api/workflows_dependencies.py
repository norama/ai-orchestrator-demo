from uuid import UUID, uuid4

from fastapi import Depends, Request, Response

from app.application.exceptions import WorkflowNotFound
from app.application.registry import domain_registry
from app.application.workflow_service import WorkflowService
from app.domain.workflow import WorkflowCreate
from app.infrastructure.persistence.sqlite_workflow_repository import (
    SqliteWorkflowRepository,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

WORKSPACE_COOKIE = "ai_orchestrator_ws"


def set_workspace_cookie(response: Response) -> str:
    ws = f"ws_{uuid4()}"
    response.set_cookie(
        key=WORKSPACE_COOKIE,
        value=ws,
        path="/",
        httponly=False,  # OK for demo
        samesite="none",  # cross-site
        secure=True,  # required with samesite=none
        max_age=60 * 60 * 24 * 7,  # 7 days
    )
    return ws


def get_workspace_name(request: Request, response: Response) -> str:
    ws = request.cookies.get(WORKSPACE_COOKIE)
    if ws:
        return ws

    return set_workspace_cookie(response)


def get_workflow_repository(
    workspace_name: str = Depends(get_workspace_name),
) -> WorkflowRepository:
    return SqliteWorkflowRepository(workspace_name=workspace_name)


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
