from fastapi import HTTPException, Request

from app.application.exceptions import (
    InvalidWorkflowOperation,
    WorkflowNotFound,
)


def workflow_not_found_handler(
    request: Request,
    exc: WorkflowNotFound,
):
    raise HTTPException(status_code=404, detail=str(exc))


def invalid_workflow_operation_handler(
    request: Request,
    exc: InvalidWorkflowOperation,
):
    raise HTTPException(status_code=409, detail=str(exc))
