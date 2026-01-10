from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.api.event_view import WorkflowEventView
from app.domain.workflow import WaitingReason, Workflow, WorkflowState


class WorkflowListResponse(BaseModel):
    workflows: list[Workflow]
    status: str


class WorkflowDetailResponse(BaseModel):
    workflow_id: UUID
    workflow: Workflow
    waiting_reason: WaitingReason | None = None
    workflow_confidence: float | None = None
    status: str


class SnapshotDetailResponse(BaseModel):
    workflow_id: UUID
    snapshot: WorkflowState
    waiting_reason: WaitingReason | None = None
    workflow_confidence: float | None = None
    status: str


class LLMResponse(BaseModel):
    response_json: dict[str, Any]
    status: str


class WorkflowHistoryResponse(BaseModel):
    workflow_id: UUID
    parent_workflow_id: UUID | None = None
    current_snapshot_id: UUID
    events: list[WorkflowEventView] = Field(default_factory=list)
    status: str
