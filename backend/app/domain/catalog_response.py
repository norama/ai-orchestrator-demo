from uuid import UUID

from pydantic import BaseModel

from app.domain.config import DomainType


class CatalogItemResponse(BaseModel):
    id: UUID
    title: str
    description: str
    category: str | None = None
    domain_type: DomainType


class CatalogResponse(BaseModel):
    items: list[CatalogItemResponse]
    status: str
