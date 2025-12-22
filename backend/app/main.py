from uuid import UUID

from fastapi import FastAPI

from app.application.commands import (
    AddAnswerCommand,
    AddChatMessageCommand,
    ChangePhaseCommand,
)
from app.application.workflow_service import WorkflowService
from app.domain.workflow import WorkflowStateCreate
from app.infrastructure.persistence.sqlite_workflow_repository import (
    SqliteWorkflowRepository,
)
from app.logging_utils import get_logger, setup_logging

setup_logging()

app = FastAPI(title="AI Orchestrator Demo")

logger = get_logger(__name__)


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.post("/workflows/")
def create_workflow(workflow_state_create: WorkflowStateCreate):
    logger.info("Creating a new workflow")
    repo = SqliteWorkflowRepository()
    workflow = repo.create(workflow_state_create)
    return {
        "workflow_id": workflow.id,
        "status": "created",
        "state": workflow.model_dump(),
    }


@app.get("/workflows")
def get_workflows():
    logger.info("Fetching all workflows")
    service = WorkflowService(SqliteWorkflowRepository())
    workflows = service.list_workflows()
    return {
        "workflows": [workflow.model_dump() for workflow in workflows],
        "status": "fetched",
    }


@app.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: UUID):
    logger.info(f"Fetching workflow with ID: {workflow_id}")
    service = WorkflowService(SqliteWorkflowRepository())
    workflow = service.get_workflow(workflow_id)
    return {
        "workflow_id": workflow.id,
        "status": "fetched",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/change_phase")
def change_workflow_phase(workflow_id: UUID, cmd: ChangePhaseCommand):
    logger.info(f"Changing phase of workflow with ID: {workflow_id} to {cmd.phase}")
    service = WorkflowService(SqliteWorkflowRepository())
    workflow = service.change_phase(workflow_id, cmd)
    return {
        "workflow_id": workflow.id,
        "status": "phase_changed",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/add_answer")
def add_workflow_answer(workflow_id: UUID, cmd: AddAnswerCommand):
    logger.info(
        f"Adding answer to workflow with ID: {workflow_id} for question {cmd.question_id}"
    )
    service = WorkflowService(SqliteWorkflowRepository())
    workflow = service.add_answer(workflow_id, cmd)
    return {
        "workflow_id": workflow.id,
        "status": "answer_added",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/add_chat_message")
def add_workflow_chat_message(workflow_id: UUID, cmd: AddChatMessageCommand):
    logger.info(
        f"Adding chat message to workflow with ID: {workflow_id} from role {cmd.role}"
    )
    service = WorkflowService(SqliteWorkflowRepository())
    workflow = service.add_chat_message(workflow_id, cmd)
    return {
        "workflow_id": workflow.id,
        "status": "chat_message_added",
        "state": workflow.model_dump(),
    }
