from uuid import UUID

from pydantic import BaseModel

from app.domain.workflow import WorkflowState


class WorkflowListResponse(BaseModel):
    workflows: list[WorkflowState]
    status: str


class WorkflowDetailResponse(BaseModel):
    workflow_id: UUID
    status: str
    state: WorkflowState
