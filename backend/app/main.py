from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.catalog_router import catalog_router
from app.api.error_handlers import (
    catalog_item_not_found_handler,
    invalid_workflow_operation_handler,
    snapshot_not_found_handler,
    snapshot_workflow_mismatch_handler,
    workflow_not_found_handler,
)
from app.api.llm_router import llm_router
from app.api.workflows_router import workflows_router
from app.api.workspace_router import workspace_router
from app.application.exceptions import (
    CatalogItemNotFound,
    InvalidWorkflowOperation,
    SnapshotNotFound,
    SnapshotWorkflowMismatch,
    WorkflowNotFound,
)
from app.logging_utils import get_logger, setup_logging
from app.settings import env_settings

setup_logging()

logger = get_logger(__name__)

app = FastAPI(title="AI Orchestrator Demo")


if env_settings.cors_origins_list:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=env_settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if env_settings.cors_origins_list:
    logger.info("CORS enabled for origins: %s", env_settings.cors_origins_list)
else:
    logger.info("CORS disabled (same-origin mode)")


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


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


app.include_router(workflows_router, prefix="/api")
app.include_router(catalog_router, prefix="/api")
app.include_router(llm_router, prefix="/api")
app.include_router(workspace_router, prefix="/api")

##############################################
# Frontend static files serving (deployment) #
##############################################

FRONTEND_DIR = Path(__file__).parent / "frontend_dist"

if FRONTEND_DIR.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="assets",
    )

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(FRONTEND_DIR / "index.html")
