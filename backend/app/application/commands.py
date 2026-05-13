from uuid import UUID

from pydantic import BaseModel

from app.domain.chat import ChatRole


class AddChatMessageCommand(BaseModel):
    role: ChatRole
    content: str


class AnswerStepCommand(BaseModel):
    step_id: UUID
    answer: str
