from uuid import UUID

from pydantic import BaseModel

from app.domain.chat import ChatRole
from app.domain.workflow import WorkflowPhase


class AddChatMessageCommand(BaseModel):
    role: ChatRole
    content: str


class ChangePhaseCommand(BaseModel):
    phase: WorkflowPhase


class AddStepCommand(BaseModel):
    prompt: str


class AnswerStepCommand(BaseModel):
    step_id: UUID
    answer: str
