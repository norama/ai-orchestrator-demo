from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class TicketSource(Enum):
    RESTFUL_API_DEV = "RESTFUL_API_DEV"
    DEMO_CATALOG = "DEMO_CATALOG"


class Ticket(BaseModel):
    id: UUID
    title: str
    description: str
    source: TicketSource = TicketSource.RESTFUL_API_DEV
    category: str | None = None
    source_dump: dict[str, Any] = Field(default_factory=dict)
