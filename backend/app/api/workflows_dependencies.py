import logging
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
from app.settings import env_settings

logger = logging.getLogger(__name__)

WORKSPACE_COOKIE = "ai_orchestrator_ws"


def set_workspace_cookie(response: Response) -> str:
    ws = f"ws_{uuid4()}"
    if env_settings.cors_origins_list:
        # Local dev: cross-origin, HTTP
        response.set_cookie(
            key=WORKSPACE_COOKIE,
            value=ws,
            path="/",
            httponly=False,
            samesite="none",  # REQUIRED for cross-site cookies
            secure=True,  # REQUIRED for cross-site cookies
            max_age=60 * 60 * 24 * 7,  # 7 days
        )
    else:
        # Production: same-origin, HTTPS
        response.set_cookie(
            key=WORKSPACE_COOKIE,
            value=ws,
            path="/",
            httponly=False,
            samesite="lax",  # Same-site cookies (Docker deployment ensures same-site)
            secure=True,  # HTTPS only
            max_age=60 * 60 * 24 * 7,  # 7 days
        )
    logger.info("Setting new workspace cookie: %s", ws)
    return ws


def get_workspace_name(request: Request, response: Response) -> str:
    ws = request.cookies.get(WORKSPACE_COOKIE)
    logger.info("Workspace cookie seen: %s", ws)
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
