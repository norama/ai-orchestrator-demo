from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.domain.chat import ChatHistory
from app.domain.config import DomainType
from app.domain.db import DbEntry
from app.domain.ticket import Ticket


class WorkflowPhase(str, Enum):
    COLLECTING = "COLLECTING"
    SOLVING = "SOLVING"
    DISCUSSION = "DISCUSSION"
    DONE = "DONE"


class WaitingReason(str, Enum):
    ANSWER_NEEDED = "ANSWER_NEEDED"
    CHAT = "CHAT"


class ClarificationStep(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    prompt: str
    answer: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class NextStepDecision(BaseModel):
    next_step: ClarificationStep | None
    confidence: float
    reason: str


class Solution(BaseModel):
    content: str
    confidence: float  # 0.0–1.0
    rationale: str | None = None


class WorkflowStateCreate(BaseModel):
    ticket: Ticket
    domain: DomainType = DomainType.PARROT
    name: str | None = None
    description: str | None = None
    max_steps: int = 8


class WorkflowState(WorkflowStateCreate, DbEntry):
    phase: WorkflowPhase = WorkflowPhase.COLLECTING
    steps: list[ClarificationStep] = Field(default_factory=list)
    last_decision: NextStepDecision | None = None
    solution: Solution | None = None
    chat_history: ChatHistory = Field(default_factory=ChatHistory)
    skipped: bool = False


class WorkflowContext(BaseModel):
    workflow_id: UUID
    ticket: Ticket
    steps: list[ClarificationStep]
    last_decision: NextStepDecision | None = None
    skipped: bool
    max_steps: int
    phase: WorkflowPhase

    model_config = ConfigDict(frozen=True)
