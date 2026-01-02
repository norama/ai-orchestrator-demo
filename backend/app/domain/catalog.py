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
        title="Project status report",
        description=(
            "Prepare a concise status report for stakeholders about the current state "
            "of the Q2 platform migration project. "
            "Summarize progress so far, key findings, and recommended next steps."
        ),
        category="Reporting",
        domain_type=DomainType.LLM_REPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Incident post-mortem summary",
        description=(
            "Create a written report summarizing a recent service outage. "
            "The report should explain what happened, what was found during investigation, "
            "and what actions are recommended to prevent similar incidents."
        ),
        category="Reporting",
        domain_type=DomainType.LLM_REPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Internal technical review report",
        description=(
            "Write an internal report reviewing a recently completed technical initiative. "
            "The report should summarize background context, key technical findings, "
            "and recommendations for future improvements."
        ),
        category="Reporting",
        domain_type=DomainType.LLM_REPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Application fails to start after recent update",
        description=(
            "After installing the latest update, the application no longer starts. "
            "It exits immediately without showing an error message. "
            "This issue started right after the update was applied."
        ),
        category="Software Issues",
        domain_type=DomainType.LLM_SUPPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="Intermittent service outages in production",
        description=(
            "A backend service occasionally becomes unavailable in production. "
            "The outages are short-lived and resolve on their own, "
            "but they occur several times per day and affect users."
        ),
        category="Reliability Issues",
        domain_type=DomainType.LLM_SUPPORT,
        source_dump={"origin": "demo"},
    ),
    CatalogItem(
        title="User cannot log in after password reset",
        description=(
            "A user reports that they cannot log in after resetting their password. "
            "The password reset process completed successfully, "
            "but login attempts continue to fail."
        ),
        category="Authentication Issues",
        domain_type=DomainType.LLM_SUPPORT,
        source_dump={"origin": "demo"},
    ),
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
