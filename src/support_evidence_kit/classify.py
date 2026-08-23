"""Keyword-based evidence classification."""

from __future__ import annotations

from collections.abc import Iterable

_LAYER_TERMS: dict[str, tuple[str, ...]] = {
    "linux_service": ("systemctl", "journalctl", "systemd", "nginx", "service"),
    "application_http": ("http", "status code", "route", "upstream", "curl"),
    "network": ("dns", "tcp", "ssh", "ping", "timeout", "gateway", "arp"),
    "storage": ("smb", "nas", "disk", "mount", "backup", "volume"),
    "database": ("sql", "mysql", "sqlite", "query", "migration", "index"),
}


def classify_text(text: str) -> list[str]:
    """Return matching technical layers in stable order."""

    lowered = text.lower()
    return [
        layer
        for layer, terms in _LAYER_TERMS.items()
        if any(term in lowered for term in terms)
    ]


def merge_layers(items: Iterable[Iterable[str]]) -> list[str]:
    """Merge classified layers without losing stable order."""

    seen: set[str] = set()
    merged: list[str] = []
    for item in items:
        for layer in item:
            if layer not in seen:
                seen.add(layer)
                merged.append(layer)
    return merged

