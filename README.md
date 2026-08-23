# Support Evidence Kit

A small, dependency-free Python tool for turning raw support diagnostics into a
sanitized, reproducible escalation bundle.

It is a public demonstrator of the workflow I use when an issue crosses systems,
networking, storage, application, and data layers:

1. preserve the original evidence;
2. redact obvious secrets and personal data;
3. classify the evidence by technical layer;
4. hash every source file for traceability; and
5. produce a concise Markdown handoff for engineering or incident review.

The sample data is synthetic. This repository contains no employer or customer
logs, credentials, source code, or internal configuration.

## Quick start

```bash
python -m support_evidence_kit examples/sample-incident --output build
```

From a source checkout without installing:

```bash
PYTHONPATH=src python -m support_evidence_kit examples/sample-incident --output build
```

Generated files:

- `build/evidence.json` — structured manifest and sanitized excerpts
- `build/escalation.md` — human-readable escalation handoff

## What it detects

- Linux/service evidence (`systemd`, `journalctl`, service states)
- HTTP/application evidence (status codes, routes, upstream behavior)
- network evidence (DNS, TCP/IP, SSH, ping, timeouts)
- storage evidence (SMB/NAS, disks, mounts, backups)
- database evidence (SQL, migrations, queries, indexes)

The redactor masks common email addresses, IPv4 addresses, bearer-style tokens,
and obvious secret assignments. It is a safety aid, not a substitute for human
review.

## Verification

```bash
python -m unittest discover -s tests -v
```

## Why this exists

Good technical support is not just finding a workaround. It is producing enough
clean evidence for another engineer to reproduce the issue, understand what was
ruled out, and act without exposing sensitive information.

Built by [Jeremy Pabalan](https://www.linkedin.com/in/jeremy-pabalan-bab061a1),
an infrastructure and technical-support professional based in Saipan, Northern
Mariana Islands, USA (UTC+10).

