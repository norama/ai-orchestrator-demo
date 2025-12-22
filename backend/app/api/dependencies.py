from fastapi import Depends

from app.application.workflow_service import WorkflowService
from app.infrastructure.persistence.sqlite_workflow_repository import (
    SqliteWorkflowRepository,
)
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

# Singleton-ish repo (OK for SQLite demo)
_repo = SqliteWorkflowRepository()


def get_workflow_repository() -> WorkflowRepository:
    return _repo


def get_workflow_service(
    repo: WorkflowRepository = Depends(get_workflow_repository),
) -> WorkflowService:
    return WorkflowService(repo)
