from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.domain.config import DomainType
from app.domain.ticket import Ticket, TicketSource


class CatalogItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    source: TicketSource = TicketSource.DEMO_CATALOG
    category: str | None = None
    domain_type: DomainType
    source_dump: dict[str, Any] = Field(default_factory=dict)

    def to_ticket(self) -> Ticket:
        return Ticket(
            id=uuid4(),
            title=self.title,
            description=self.description,
            source=self.source,
            category=self.category,
            source_dump=self.source_dump,
        )


class WorkflowStateCreateFromCatalog(BaseModel):
    item_id: UUID
    name: str | None = None
    description: str | None = None
    max_steps: int = 8


DEMO_CATALOG = [
    CatalogItem(
        title="Laptop suddenly became very slow",
        description=(
            "My laptop has become noticeably slower over the last few days. "
            "Apps take a long time to start, and the system feels unresponsive. "
            "There were no obvious error messages."
        ),
        category="Everyday Tech Issues",
        domain_type=DomainType.LLM_SUPPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Rent or buy an apartment",
        description=(
            "Help me think through whether it makes more sense to rent or buy an apartment "
            "in my situation. I want a balanced explanation of the trade-offs, "
            "not a one-size-fits-all answer."
        ),
        category="Personal Decision Support",
        domain_type=DomainType.LLM_REPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Printer won’t print, but no error is shown",
        description=(
            "I sent a document to the printer, but nothing happens. "
            "The printer appears to be idle and shows no obvious error message."
        ),
        category="Hardware Issues",
        domain_type=DomainType.PRINTER,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Parrot echo test",
        description=(
            "This workflow intentionally echoes every message back to the user "
            "and keeps asking for more input. It is used to test orchestration behavior."
        ),
        category="Test / Debug",
        domain_type=DomainType.PARROT,
        source_dump={"origin": "demo"},
    ),
]
