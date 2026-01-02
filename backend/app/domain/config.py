from enum import Enum

from pydantic import BaseModel


class DomainType(str, Enum):
    PARROT = "PARROT"
    PRINTER = "PRINTER"
    LLM_SUPPORT = "LLM_SUPPORT"
    LLM_REPORT = "LLM_REPORT"


class DomainConfig(BaseModel):
    domain: DomainType
