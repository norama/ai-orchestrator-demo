from pydantic import BaseModel

from app.domain.chat import ChatRole
from app.domain.workflow import WorkflowPhase


class AddChatMessageCommand(BaseModel):
    role: ChatRole
    content: str


class ChangePhaseCommand(BaseModel):
    phase: WorkflowPhase


class AddAnswerCommand(BaseModel):
    question_id: str
    answer: str
