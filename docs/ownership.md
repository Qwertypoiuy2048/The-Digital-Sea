# Ownership

Human ownership is not configured. `.github/CODEOWNERS` still contains `[insert ...]` placeholders, so no real DRI, backup, security owner, on-call owner, or communication channel can be inferred.

| Area | DRI | Backup | Source |
|---|---|---|---|
| Application/runtime | UNKNOWN — needs human confirmation | UNKNOWN | `main.py`, `program_runtime.py` |
| UI/screens/design | UNKNOWN — needs human confirmation | UNKNOWN | `code_screen.py`, `network_screen.py`, `design/` |
| Data fixtures | UNKNOWN — needs human confirmation | UNKNOWN | `data/`, `data_loader.py` |
| Tests | UNKNOWN — needs human confirmation | UNKNOWN | `tests/` |
| CI/playbook | UNKNOWN — needs human confirmation | UNKNOWN | `.github/`, `scripts/`, `.githooks/` |

Agent role sign-off is procedural and does not substitute for human CODEOWNERS approval. When humans disagree, the named DRI should decide and record a meaningful architectural decision; the names are not yet supplied.

## Update this document when

Update when CODEOWNERS, module ownership, DRI/backups, review routing, escalation, or on-call information changes.
