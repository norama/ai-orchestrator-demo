import asyncio
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.workflows_dependencies import (
    get_workflow_repository,
    get_workflow_service,
    get_workflow_service_for_creation,
)
from app.application.commands import AddChatMessageCommand, AnswerStepCommand
from app.application.workflow_service import WorkflowService
from app.domain.response import WorkflowDetailResponse, WorkflowListResponse
from app.domain.workflow import WorkflowStateCreate
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

workflows_router = APIRouter(prefix="/workflows", tags=["workflows"])


@workflows_router.get("", response_model=WorkflowListResponse)
def list_workflows(
    repo: WorkflowRepository = Depends(get_workflow_repository),
):
    workflows = repo.list()
    return WorkflowListResponse(
        workflows=workflows,
        status="ok",
    )


@workflows_router.get("/{workflow_id}", response_model=WorkflowDetailResponse)
def get_workflow(
    workflow_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    workflow = service.get_workflow(workflow_id)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="ok",
        state=workflow,
    )


@workflows_router.post("", response_model=WorkflowDetailResponse)
def create_workflow(
    req: WorkflowStateCreate,
    service: WorkflowService = Depends(get_workflow_service_for_creation),
):
    workflow = service.create(req)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="created",
        state=workflow,
        waiting_reason=service.get_waiting_reason(workflow),
        workflow_confidence=service.get_workflow_confidence(workflow),
    )


@workflows_router.post("/{workflow_id}/answer", response_model=WorkflowDetailResponse)
async def answer_step(
    workflow_id: UUID,
    cmd: AnswerStepCommand,
    service: WorkflowService = Depends(get_workflow_service),
):
    await asyncio.sleep(4)
    workflow = service.answer_step(workflow_id, cmd)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="updated",
        state=workflow,
        waiting_reason=service.get_waiting_reason(workflow),
        workflow_confidence=service.get_workflow_confidence(workflow),
    )


@workflows_router.post("/{workflow_id}/skip", response_model=WorkflowDetailResponse)
async def skip_to_solution(
    workflow_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    await asyncio.sleep(4)
    workflow = service.skip_to_solution(workflow_id)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="skipped",
        state=workflow,
        waiting_reason=service.get_waiting_reason(workflow),
        workflow_confidence=service.get_workflow_confidence(workflow),
    )


@workflows_router.post("/{workflow_id}/chat", response_model=WorkflowDetailResponse)
async def send_chat_message(
    workflow_id: UUID,
    cmd: AddChatMessageCommand,
    service: WorkflowService = Depends(get_workflow_service),
):
    await asyncio.sleep(4)
    workflow = service.add_chat_message(workflow_id, cmd)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="chat_added",
        state=workflow,
        waiting_reason=service.get_waiting_reason(workflow),
        workflow_confidence=service.get_workflow_confidence(workflow),
    )
