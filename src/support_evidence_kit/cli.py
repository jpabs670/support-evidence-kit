"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from .bundle import build_bundle


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Create a sanitized technical-support escalation bundle."
    )
    result.add_argument("source", type=Path, help="Directory of diagnostic files")
    result.add_argument(
        "--output", type=Path, default=Path("build"), help="Output directory"
    )
    return result


def main() -> int:
    args = parser().parse_args()
    if not args.source.is_dir():
        parser().error(f"source directory not found: {args.source}")
    manifest = build_bundle(args.source, args.output)
    print(
        f"Wrote {manifest['file_count']} evidence files to "
        f"{args.output.resolve()}"
    )
    return 0

