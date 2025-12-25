from uuid import UUID

from pydantic import BaseModel

from app.domain.workflow import WaitingReason, WorkflowState


class WorkflowListResponse(BaseModel):
    workflows: list[WorkflowState]
    status: str


class WorkflowDetailResponse(BaseModel):
    workflow_id: UUID
    status: str
    state: WorkflowState
    waiting_reason: WaitingReason | None = None
