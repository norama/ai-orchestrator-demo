from uuid import UUID

from fastapi import Depends, FastAPI

from app.api.dependencies import get_workflow_service
from app.application.commands import (
    AddAnswerCommand,
    AddChatMessageCommand,
    ChangePhaseCommand,
)
from app.application.workflow_service import WorkflowService
from app.domain.workflow import WorkflowStateCreate
from app.logging_utils import get_logger, setup_logging

setup_logging()

app = FastAPI(title="AI Orchestrator Demo")

logger = get_logger(__name__)


@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@app.post("/workflows/")
def create_workflow(
    workflow_state_create: WorkflowStateCreate,
    service: WorkflowService = Depends(get_workflow_service),
):
    logger.info("Creating a new workflow")
    workflow = service.create(workflow_state_create)
    return {
        "workflow_id": workflow.id,
        "status": "created",
        "state": workflow.model_dump(),
    }


@app.get("/workflows")
def get_workflows(service: WorkflowService = Depends(get_workflow_service)):
    logger.info("Fetching all workflows")
    workflows = service.list_workflows()
    return {
        "workflows": [workflow.model_dump() for workflow in workflows],
        "status": "fetched",
    }


@app.get("/workflows/{workflow_id}")
def get_workflow(
    workflow_id: UUID, service: WorkflowService = Depends(get_workflow_service)
):
    logger.info(f"Fetching workflow with ID: {workflow_id}")
    workflow = service.get_workflow(workflow_id)
    return {
        "workflow_id": workflow.id,
        "status": "fetched",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/change_phase")
def change_workflow_phase(
    workflow_id: UUID,
    cmd: ChangePhaseCommand,
    service: WorkflowService = Depends(get_workflow_service),
):
    logger.info(f"Changing phase of workflow with ID: {workflow_id} to {cmd.phase}")
    workflow = service.change_phase(workflow_id, cmd)
    return {
        "workflow_id": workflow.id,
        "status": "phase_changed",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/add_question")
def add_workflow_question(
    workflow_id: UUID,
    question: str,
    service: WorkflowService = Depends(get_workflow_service),
):
    logger.info(
        f"Adding question to workflow with ID: {workflow_id} with content: {question}"
    )
    workflow = service.add_question(workflow_id, question)
    return {
        "workflow_id": workflow.id,
        "status": "question_added",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/add_answer")
def add_workflow_answer(
    workflow_id: UUID,
    cmd: AddAnswerCommand,
    service: WorkflowService = Depends(get_workflow_service),
):
    logger.info(
        f"Adding answer to workflow with ID: {workflow_id} for question {cmd.clarification_id}"
    )
    workflow = service.add_answer(workflow_id, cmd)
    return {
        "workflow_id": workflow.id,
        "status": "answer_added",
        "state": workflow.model_dump(),
    }


@app.post("/workflows/{workflow_id}/add_chat_message")
def add_workflow_chat_message(
    workflow_id: UUID,
    cmd: AddChatMessageCommand,
    service: WorkflowService = Depends(get_workflow_service),
):
    logger.info(
        f"Adding chat message to workflow with ID: {workflow_id} from role {cmd.role}"
    )
    workflow = service.add_chat_message(workflow_id, cmd)
    return {
        "workflow_id": workflow.id,
        "status": "chat_message_added",
        "state": workflow.model_dump(),
    }
