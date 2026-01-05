from typing import Any
from uuid import UUID

from pydantic import BaseModel

from app.domain.workflow import WaitingReason, Workflow


class WorkflowListResponse(BaseModel):
    workflows: list[Workflow]
    status: str


class WorkflowDetailResponse(BaseModel):
    workflow_id: UUID
    status: str
    workflow: Workflow
    waiting_reason: WaitingReason | None = None
    workflow_confidence: float | None = None


class LLMResponse(BaseModel):
    response_json: dict[str, Any]
    status: str
