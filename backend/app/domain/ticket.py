from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TicketSource(Enum):
    RESTFUL_API_DEV = "RESTFUL_API_DEV"


class Ticket(BaseModel):
    id: str
    title: str
    description: str
    source: TicketSource
    source_dump: dict[str, Any] = Field(default_factory=dict)
