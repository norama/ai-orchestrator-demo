from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Clarification(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    question: str
    answer: str | None = None
