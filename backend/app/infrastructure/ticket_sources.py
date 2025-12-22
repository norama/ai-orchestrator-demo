from dataclasses import dataclass

from app.domain.ticket import TicketSource


@dataclass(frozen=True)
class TicketSourceConfig:
    base_url: str
    description: str


TICKET_SOURCE_REGISTRY: dict[TicketSource, TicketSourceConfig] = {
    TicketSource.RESTFUL_API_DEV: TicketSourceConfig(
        base_url="https://restful-api.dev/",
        description="Demo Ticket API",
    )
}


def get_ticket_source_config(source: TicketSource) -> TicketSourceConfig:
    if source not in TICKET_SOURCE_REGISTRY:
        raise ValueError(f"Ticket source '{source}' is not registered.")
    return TICKET_SOURCE_REGISTRY[source]
