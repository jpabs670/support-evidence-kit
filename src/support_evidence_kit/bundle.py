"""Build structured and human-readable support evidence bundles."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

from .classify import classify_text, merge_layers
from .redact import redact_text

SUPPORTED_SUFFIXES = {".log", ".txt", ".json", ".md", ".csv"}
MAX_EXCERPT_CHARS = 4_000


def _source_files(source: Path) -> list[Path]:
    return sorted(
        path
        for path in source.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def build_bundle(source: Path, output: Path) -> dict[str, object]:
    """Build an evidence manifest and escalation handoff."""

    source = source.resolve()
    output.mkdir(parents=True, exist_ok=True)

    files: list[dict[str, object]] = []
    total_redactions: Counter[str] = Counter()

    for path in _source_files(source):
        raw_bytes = path.read_bytes()
        text = raw_bytes.decode("utf-8", errors="replace")
        sanitized, redactions = redact_text(text)
        total_redactions.update(redactions)
        files.append(
            {
                "path": str(path.relative_to(source)),
                "sha256": sha256(raw_bytes).hexdigest(),
                "bytes": len(raw_bytes),
                "layers": classify_text(sanitized),
                "redactions": redactions,
                "sanitized_excerpt": sanitized[:MAX_EXCERPT_CHARS],
            }
        )

    manifest: dict[str, object] = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_name": source.name,
        "file_count": len(files),
        "layers": merge_layers(item["layers"] for item in files),
        "redactions": dict(sorted(total_redactions.items())),
        "files": files,
    }

    (output / "evidence.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (output / "escalation.md").write_text(
        render_markdown(manifest), encoding="utf-8"
    )
    return manifest


def render_markdown(manifest: dict[str, object]) -> str:
    """Render a concise escalation handoff from a manifest."""

    layers = ", ".join(manifest["layers"]) or "unclassified"
    lines = [
        "# Technical Support Escalation Bundle",
        "",
        f"- Source: `{manifest['source_name']}`",
        f"- Evidence files: {manifest['file_count']}",
        f"- Technical layers: {layers}",
        f"- Redactions: {json.dumps(manifest['redactions'], sort_keys=True)}",
        "",
        "## Evidence inventory",
        "",
    ]

    for item in manifest["files"]:
        item_layers = ", ".join(item["layers"]) or "unclassified"
        lines.extend(
            [
                f"### `{item['path']}`",
                "",
                f"- SHA-256: `{item['sha256']}`",
                f"- Size: {item['bytes']} bytes",
                f"- Layers: {item_layers}",
                f"- Redactions: {json.dumps(item['redactions'], sort_keys=True)}",
                "",
                "```text",
                str(item["sanitized_excerpt"]).rstrip(),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Human review checklist",
            "",
            "- [ ] Confirm no secrets or personal data remain.",
            "- [ ] State the customer-visible impact and reproduction steps.",
            "- [ ] Separate verified facts from hypotheses.",
            "- [ ] Record what was ruled out and how.",
            "- [ ] Define the next owner and validation step.",
            "",
        ]
    )
    return "\n".join(lines)

