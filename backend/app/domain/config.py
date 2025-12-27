from enum import Enum

from pydantic import BaseModel


class DomainType(str, Enum):
    PARROT = "PARROT"
    PRINTER = "PRINTER"
    LLM_SUPPORT = "LLM_SUPPORT"


class DomainConfig(BaseModel):
    domain: DomainType
