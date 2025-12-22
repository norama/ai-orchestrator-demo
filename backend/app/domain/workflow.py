from enum import Enum

from pydantic import BaseModel, Field

from app.domain.chat import ChatHistory
from app.domain.db import DbEntry
from app.domain.qa import Clarification
from app.domain.ticket import Ticket


class WorkflowPhase(str, Enum):
    COLLECTING = "collecting"
    SOLVING = "solving"
    DISCUSSION = "discussion"
    DONE = "done"


class WorkflowStateCreate(BaseModel):
    ticket: Ticket
    phase: WorkflowPhase
    clarifications: list[Clarification] = Field(default_factory=list)
    solution: str | None = None
    chat_history: ChatHistory = Field(default_factory=ChatHistory)


class WorkflowState(WorkflowStateCreate, DbEntry):
    pass
