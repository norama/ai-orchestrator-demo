from datetime import datetime, timezone

from pydantic import BaseModel, Field


class DbEntry(BaseModel):
    id: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
