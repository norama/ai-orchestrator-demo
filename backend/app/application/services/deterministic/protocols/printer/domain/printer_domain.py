from enum import Enum

from pydantic import BaseModel


class PrinterStepPhase(str, Enum):
    INITIAL = "INITIAL"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class PrinterExpectedAnswer(str, Enum):
    YES_NO = "YES_NO"
    FREE_TEXT = "FREE_TEXT"


class PrinterParsedAnswer(str, Enum):
    YES = "YES"
    NO = "NO"
    FREE_TEXT = "FREE_TEXT"
    INVALID = "INVALID"


class PrinterStepMetadata(BaseModel):
    phase: PrinterStepPhase
    expected_answer: PrinterExpectedAnswer
    parsed_answer: PrinterParsedAnswer | None = None
