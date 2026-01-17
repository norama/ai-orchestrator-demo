from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.catalog_router import catalog_router
from app.api.error_handlers import (
    catalog_item_not_found_handler,
    invalid_workflow_operation_handler,
    invalid_workspace_id_handler,
    missing_workspace_id_handler,
    snapshot_not_found_handler,
    snapshot_workflow_mismatch_handler,
    workflow_not_found_handler,
)
from app.api.llm_router import llm_router
from app.api.workflows_router import workflows_router
from app.application.exceptions import (
    CatalogItemNotFound,
    InvalidWorkflowOperation,
    InvalidWorkspaceId,
    MissingWorkspaceId,
    SnapshotNotFound,
    SnapshotWorkflowMismatch,
    WorkflowNotFound,
)
from app.logging_utils import get_logger, setup_logging
from app.settings import EnvSettings

setup_logging()


app = FastAPI(title="AI Orchestrator Demo")

settings = EnvSettings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "X-Workspace-Id",
    ],
)

app.add_exception_handler(
    WorkflowNotFound,
    workflow_not_found_handler,
)

app.add_exception_handler(
    InvalidWorkflowOperation,
    invalid_workflow_operation_handler,
)

app.add_exception_handler(
    CatalogItemNotFound,
    catalog_item_not_found_handler,
)

app.add_exception_handler(
    SnapshotNotFound,
    snapshot_not_found_handler,
)

app.add_exception_handler(
    SnapshotWorkflowMismatch,
    snapshot_workflow_mismatch_handler,
)

app.add_exception_handler(
    MissingWorkspaceId,
    missing_workspace_id_handler,
)

app.add_exception_handler(
    InvalidWorkspaceId,
    invalid_workspace_id_handler,
)

logger = get_logger(__name__)


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


app.include_router(workflows_router)
app.include_router(catalog_router)
app.include_router(llm_router)
