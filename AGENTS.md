# AGENTS.md — support-evidence-kit

## Purpose
Dependency-free Python CLI that turns raw support diagnostics into a sanitized,
reproducible escalation bundle: redact secrets/PII, classify evidence by layer,
hash every source file, and write `evidence.json` + `escalation.md`.
Public demonstrator: all sample data is synthetic.

## Stack
- Python >= 3.10, standard library only (`dependencies = []` in `pyproject.toml`).
- setuptools build backend; console script `support-evidence` -> `support_evidence_kit.cli:main`.
- Tests use `unittest` (no pytest required).

## Folder map
- `src/support_evidence_kit/` — package: `cli.py` (args), `bundle.py` (manifest + Markdown),
  `classify.py` (layer keywords), `redact.py` (masking rules), `__main__.py`.
- `tests/test_support_evidence_kit.py` — redaction, classification and bundle tests.
- `examples/sample-incident/` — synthetic logs used by the quick start.
- `build/` — generated output; gitignored, never commit it.

## Setup
No install needed. Run from the repo root with `PYTHONPATH=src`.
Optional: `python3 -m venv .venv && . .venv/bin/activate && pip install -e .`

## Commands (verified 2026-10-25, Python 3.13)
- Tests: `PYTHONPATH=src python3 -m unittest discover -s tests -v` (3 tests, OK).
  Without `PYTHONPATH=src` (and no editable install) the import fails.
- Run: `PYTHONPATH=src python3 -m support_evidence_kit examples/sample-incident --output build`
  (writes `build/evidence.json` and `build/escalation.md`).
- Lint: no linter is configured. Do not add one unless the ticket asks.

## Code style
- Keep it dependency-free: standard library only; do not add packages to `pyproject.toml`.
- Type hints on public functions, `from pathlib import Path`, UTF-8 explicit on file I/O.
- Small pure functions; redaction and classification must stay deterministic.
- New redaction or classification rules need a test in `tests/` with synthetic data.
- Never add real logs, hostnames, emails or IPs; use RFC 5737 IPs (192.0.2.x) and example.com.

## Done means
- Tests pass with the command above, and the quick-start run still writes both files.
- README updated if CLI flags or output files change.

## Rules for every Codex run
- Never push to `main` (or any default branch) and never force-push. The agent pushes the reviewed branch once.
- No secrets in code, commits, logs or briefs: no passwords, tokens, API keys, `.env` values or customer data.
- Keep changes inside this repo. Do not edit files in other repos, the Obsidian vault or `~/`.
- One ticket per branch and per PR; stay inside the files the brief puts in scope.
- Run the tests listed above before reporting done, and paste the result lines in your summary.
- Codex cannot commit (`.git` is read-only to it). Leave changes uncommitted; the agent reviews and commits.
- If a command fails because of the environment (missing tool, no network), report it; do not change config to dodge it.
