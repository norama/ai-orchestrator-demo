import json
import re
from typing import Any


def extract_json(text: str) -> dict[str, Any]:
    """
    Extracts JSON from raw LLM output.
    Supports plain JSON or ```json fenced blocks.
    """
    text = text.strip()

    # Remove ```json fences if present
    fence_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    return json.loads(text)
