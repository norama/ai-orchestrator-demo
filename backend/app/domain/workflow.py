from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from app.domain.chat import ChatHistory
from app.domain.db import DbEntry
from app.domain.ticket import Ticket


class WorkflowPhase(str, Enum):
    COLLECTING = "COLLECTING"
    SOLVING = "SOLVING"
    DISCUSSION = "DISCUSSION"
    DONE = "DONE"


class ClarificationStep(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    prompt: str
    answer: str | None = None


class NextQuestionDecision(BaseModel):
    next_step: ClarificationStep | None
    confidence: float
    reason: str


class Solution(BaseModel):
    content: str
    confidence: float  # 0.0–1.0
    rationale: str | None = None


class WorkflowStateCreate(BaseModel):
    ticket: Ticket
    max_steps: int = 8


class WorkflowState(WorkflowStateCreate, DbEntry):
    phase: WorkflowPhase
    steps: list[ClarificationStep] = Field(default_factory=list)
    solution: Solution | None = None
    chat_history: ChatHistory = Field(default_factory=ChatHistory)
    skipped: bool = False


class WorkflowContext(BaseModel):
    workflow_id: UUID
    ticket: Ticket
    steps: list[ClarificationStep]
    skipped: bool
    max_steps: int
    phase: WorkflowPhase

    model_config = ConfigDict(frozen=True)
