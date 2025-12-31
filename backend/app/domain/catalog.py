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
        title="Printer reports paper jam",
        description="A user reports that their office printer is showing a paper jam error, but there is no visible jam.",
        category="Hardware Issues",
        domain_type=DomainType.PRINTER,
        source_dump={"example_key": "example_value"},
    ),
    CatalogItem(
        title="Printer unable to connect to network",
        description="A user is experiencing issues connecting their office printer to the company Wi-Fi network.",
        category="Network Issues",
        domain_type=DomainType.PRINTER,
        source_dump={"example_key": "example_value"},
    ),
    CatalogItem(
        title="Parrot stopped talking",
        description="Previously talkative parrot is now silent.",
        category="Behavior Issues",
        domain_type=DomainType.PARROT,
        source_dump={"example_key": "example_value"},
    ),
    CatalogItem(
        title="Printer requires maintenance",
        description="The printer is showing a maintenance required message.",
        category="Maintenance Issues",
        domain_type=DomainType.LLM_SUPPORT,
        source_dump={"example_key": "example_value"},
    ),
    CatalogItem(
        title="Parrot exhibits aggressive behavior",
        description="The parrot has started to show signs of aggression towards its owner.",
        category="Behavior Issues",
        domain_type=DomainType.PARROT,
        source_dump={"example_key": "example_value"},
    ),
    CatalogItem(
        title="Parrot needs more social interaction",
        description="The parrot appears lonely and is not engaging with its environment.",
        category="Behavior Issues",
        domain_type=DomainType.PARROT,
        source_dump={"example_key": "example_value"},
    ),
]
