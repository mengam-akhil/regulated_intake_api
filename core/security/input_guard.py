import re
from typing import Dict

# Simple but effective red flags (expandable)
SUSPICIOUS_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"system\s*:",
    r"assistant\s*:",
    r"act\s+as\s+",
    r"override",
    r"bypass",
]

MAX_TEXT_LENGTH = 1000


def validate_input(payload: Dict):
    """
    Defensive input validation.
    Blocks prompt injection attempts and abusive payloads.
    """

    text_fields = [
        v for v in payload.values()
        if isinstance(v, str)
    ]

    for text in text_fields:
        if len(text) > MAX_TEXT_LENGTH:
            raise ValueError("Input text too long")

        lowered = text.lower()
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, lowered):
                raise ValueError("Suspicious or unsafe input detected")
