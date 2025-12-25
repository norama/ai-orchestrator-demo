from enum import Enum

from pydantic import BaseModel


class DomainType(str, Enum):
    PARROT = "PARROT"
    PRINTER = "PRINTER"


class DomainConfig(BaseModel):
    domain: DomainType
