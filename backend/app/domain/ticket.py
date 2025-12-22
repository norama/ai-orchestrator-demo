from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TicketSource(Enum):
    RESTFUL_API_DEV = "RESTFUL_API_DEV"


class Ticket(BaseModel):
    id: UUID
    title: str
    description: str
    source: TicketSource
    source_dump: dict[str, Any] = Field(default_factory=dict)
