from datetime import datetime
from enum import Enum

from backend.app.domain.chat import ChatHistory
from backend.app.domain.ticket import Ticket
from pydantic import BaseModel, Field


class WorkflowPhase(str, Enum):
    COLLECTING = "collecting"
    SOLVING = "solving"
    DISCUSSION = "discussion"
    DONE = "done"


class WorkflowState(BaseModel):
    workflow_id: str
    ticket: Ticket
    phase: WorkflowPhase
    answers: dict[str, str] = Field(default_factory=dict)
    solution: str | None = None
    chat_history: ChatHistory = Field(default_factory=ChatHistory)
    updated_at: datetime = Field(default_factory=datetime.now())
