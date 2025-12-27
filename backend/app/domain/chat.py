from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ChatRole(str, Enum):
    USER = "USER"
    AI = "AI"
    SYSTEM = "SYSTEM"


class ChatMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    role: ChatRole
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatHistory(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_message(self, message: ChatMessage) -> None:
        self.messages.append(message)
        self.updated_at = datetime.now(timezone.utc)

    def get_messages(self) -> list[ChatMessage]:
        return self.messages
