from fastapi import Request, Response
from fastapi.responses import JSONResponse

from app.application.exceptions import (
    CatalogItemNotFound,
    InvalidWorkflowOperation,
    SnapshotNotFound,
    SnapshotWorkflowMismatch,
    WorkflowNotFound,
)


def workflow_not_found_handler(
    request: Request,
    exc: Exception,
) -> Response:
    assert isinstance(exc, WorkflowNotFound)

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


def invalid_workflow_operation_handler(
    request: Request,
    exc: Exception,
) -> Response:
    assert isinstance(exc, InvalidWorkflowOperation)

    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


def catalog_item_not_found_handler(
    request: Request,
    exc: Exception,
) -> Response:
    assert isinstance(exc, CatalogItemNotFound)

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


def snapshot_not_found_handler(
    request: Request,
    exc: Exception,
) -> Response:
    assert isinstance(exc, SnapshotNotFound)

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


def snapshot_workflow_mismatch_handler(
    request: Request,
    exc: Exception,
) -> Response:
    assert isinstance(exc, SnapshotWorkflowMismatch)

    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )
