import asyncio
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.event_view import event_to_view
from app.api.response import (
    SnapshotDetailResponse,
    WorkflowDetailResponse,
    WorkflowHistoryResponse,
    WorkflowListResponse,
)
from app.api.streaming_utils import stream_command
from app.api.workflows_dependencies import (
    get_workflow_repository,
    get_workflow_service,
    get_workflow_service_for_creation,
)
from app.application.commands import AddChatMessageCommand, AnswerStepCommand
from app.application.workflow_service import WorkflowService
from app.application.workflow_utils import get_waiting_reason, get_workflow_confidence
from app.domain.workflow import WorkflowCreate
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

workflows_router = APIRouter(prefix="/workflows", tags=["workflows"])


@workflows_router.get("", response_model=WorkflowListResponse)
def get_workflows(
    repo: WorkflowRepository = Depends(get_workflow_repository),
):
    workflows = repo.get_workflows()
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
        workflow=workflow,
        waiting_reason=get_waiting_reason(workflow.state),
        workflow_confidence=get_workflow_confidence(workflow.state),
    )


@workflows_router.get("/{workflow_id}/snapshots/{snapshot_id}", response_model=SnapshotDetailResponse)
def get_snapshot(
    workflow_id: UUID,
    snapshot_id: UUID,
    repo: WorkflowRepository = Depends(get_workflow_repository),
):
    snapshot = repo.get_snapshot(workflow_id, snapshot_id)

    return SnapshotDetailResponse(
        workflow_id=workflow_id,
        snapshot_id=snapshot_id,
        snapshot=snapshot,
        waiting_reason=get_waiting_reason(snapshot),
        workflow_confidence=get_workflow_confidence(snapshot),
        status="ok",
    )


@workflows_router.get("/{workflow_id}/history", response_model=WorkflowHistoryResponse)
def get_workflow_history(
    workflow_id: UUID,
    repo: WorkflowRepository = Depends(get_workflow_repository),
    service: WorkflowService = Depends(get_workflow_service),
):
    workflow = service.get_workflow(workflow_id)

    events = repo.get_events(workflow_id)
    current_snapshot_id = repo.get_current_snapshot_id(workflow_id)
    parent_workflow_id = workflow.parent_id

    return WorkflowHistoryResponse(
        workflow_id=workflow_id,
        parent_workflow_id=parent_workflow_id,
        current_snapshot_id=current_snapshot_id,
        events=[event_to_view(event) for event in events],
        status="ok",
    )


@workflows_router.post("", response_model=WorkflowDetailResponse)
def create_workflow(
    req: WorkflowCreate,
    service: WorkflowService = Depends(get_workflow_service_for_creation),
):
    workflow = service.create(req)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="created",
        workflow=workflow,
        waiting_reason=get_waiting_reason(workflow.state),
        workflow_confidence=get_workflow_confidence(workflow.state),
    )


@workflows_router.post("/{workflow_id}/snapshots/{snapshot_id}/branch", response_model=WorkflowDetailResponse)
def branch_workflow(
    workflow_id: UUID,
    snapshot_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    workflow = service.branch(workflow_id, snapshot_id)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="branched",
        workflow=workflow,
        waiting_reason=get_waiting_reason(workflow.state),
        workflow_confidence=get_workflow_confidence(workflow.state),
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
        workflow=workflow,
        waiting_reason=get_waiting_reason(workflow.state),
        workflow_confidence=get_workflow_confidence(workflow.state),
    )


@workflows_router.post("/{workflow_id}/answer/stream", response_model=None)
async def answer_step_stream(
    workflow_id: UUID,
    cmd: AnswerStepCommand,
    service: WorkflowService = Depends(get_workflow_service),
):
    await asyncio.sleep(4)
    return stream_command(
        lambda stream: service.answer_step(
            workflow_id,
            cmd,
            stream=stream,
        )
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
        workflow=workflow,
        waiting_reason=get_waiting_reason(workflow.state),
        workflow_confidence=get_workflow_confidence(workflow.state),
    )


@workflows_router.post("/{workflow_id}/skip/stream")
def skip_to_solution_stream(
    workflow_id: UUID,
    service: WorkflowService = Depends(get_workflow_service),
):
    return stream_command(
        lambda stream: service.skip_to_solution(
            workflow_id,
            stream=stream,
        )
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
        workflow=workflow,
        waiting_reason=get_waiting_reason(workflow.state),
        workflow_confidence=get_workflow_confidence(workflow.state),
    )
