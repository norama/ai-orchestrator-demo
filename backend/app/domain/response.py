from typing import Any
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
    workflow_confidence: float | None = None


class LLMResponse(BaseModel):
    response_json: dict[str, Any]
    status: str
