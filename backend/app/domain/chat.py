from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ChatRole(str, Enum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    id: str
    role: ChatRole
    content: str
    created_at: datetime


class ChatHistory(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.now())

    def add_message(self, message: ChatMessage) -> None:
        self.messages.append(message)
        self.updated_at = datetime.now()

    def get_messages(self) -> list[ChatMessage]:
        return self.messages
