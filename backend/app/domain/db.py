from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DbEntry(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
