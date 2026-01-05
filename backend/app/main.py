from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.catalog_router import catalog_router
from app.api.error_handlers import (
    catalog_item_not_found_handler,
    invalid_workflow_operation_handler,
    snapshot_not_found_handler,
    workflow_not_found_handler,
)
from app.api.llm_router import llm_router
from app.api.workflows_router import workflows_router
from app.application.exceptions import (
    CatalogItemNotFound,
    InvalidWorkflowOperation,
    SnapshotNotFound,
    WorkflowNotFound,
)
from app.logging_utils import get_logger, setup_logging

setup_logging()

app = FastAPI(title="AI Orchestrator Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

logger = get_logger(__name__)


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


app.include_router(workflows_router)
app.include_router(catalog_router)
app.include_router(llm_router)
