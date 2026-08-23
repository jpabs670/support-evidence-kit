"""Conservative redaction helpers for diagnostic text."""

from __future__ import annotations

import re

_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    (
        "ipv4",
        re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
        ),
    ),
    (
        "bearer_token",
        re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{8,}", re.I),
    ),
    (
        "secret_assignment",
        re.compile(
            r"\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*"
            r"([^\s,;]+)",
            re.I,
        ),
    ),
)


def redact_text(text: str) -> tuple[str, dict[str, int]]:
    """Return redacted text and counts by redaction category."""

    counts: dict[str, int] = {}
    redacted = text

    for label, pattern in _PATTERNS:
        if label == "secret_assignment":
            redacted, count = pattern.subn(
                lambda match: f"{match.group(1)}=[REDACTED]", redacted
            )
        elif label == "bearer_token":
            redacted, count = pattern.subn("Bearer [REDACTED]", redacted)
        else:
            redacted, count = pattern.subn(f"[REDACTED_{label.upper()}]", redacted)

        if count:
            counts[label] = count

    return redacted, counts

