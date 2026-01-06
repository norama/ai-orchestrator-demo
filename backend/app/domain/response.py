from typing import Any
from uuid import UUID

from pydantic import BaseModel

from app.domain.workflow import WaitingReason, Workflow, WorkflowHistory


class WorkflowListResponse(BaseModel):
    workflows: list[Workflow]
    status: str


class WorkflowDetailResponse(BaseModel):
    workflow_id: UUID
    workflow: Workflow
    waiting_reason: WaitingReason | None = None
    workflow_confidence: float | None = None
    status: str


class LLMResponse(BaseModel):
    response_json: dict[str, Any]
    status: str


class WorkflowHistoryResponse(BaseModel):
    history: WorkflowHistory
    status: str
