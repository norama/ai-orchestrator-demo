from app.application.services.deterministic.printer.domain.printer_domain import (
    PrinterExpectedAnswer,
    PrinterParsedAnswer,
)


def parse_printer_answer(
    raw: str,
    expected: PrinterExpectedAnswer,
) -> PrinterParsedAnswer:
    text = raw.lower().strip()

    if expected == PrinterExpectedAnswer.YES_NO:
        if "yes" in text or text == "y":
            return PrinterParsedAnswer.YES
        if "no" in text or text == "n":
            return PrinterParsedAnswer.NO
        return PrinterParsedAnswer.INVALID

    return PrinterParsedAnswer.FREE_TEXT
