from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TicketSource(Enum):
    RESTFUL_API_DEV = ("https://restful-api.dev/", "Demo Ticket API")

    def __init__(self, base_url: str, description: str):
        self.base_url = base_url
        self.description = description


class Ticket(BaseModel):
    id: str
    title: str
    description: str
    source: TicketSource
    source_dump: dict[str, Any] = Field(default_factory=dict)
