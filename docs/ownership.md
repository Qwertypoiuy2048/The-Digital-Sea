# Ownership

CODEOWNERS now routes the repository and its major areas to `@Qwertypoiuy2048`. A separate backup, security owner, on-call owner, and communication channel are not configured.

| Area | DRI | Backup | Source |
|---|---|---|---|
| Application/runtime | @Qwertypoiuy2048 | UNKNOWN | `main.py`, `program_runtime.py` |
| UI/screens/design | @Qwertypoiuy2048 | UNKNOWN | `code_screen.py`, `network_screen.py`, `design/` |
| Data fixtures | @Qwertypoiuy2048 | UNKNOWN | `data/`, `data_loader.py` |
| Tests | @Qwertypoiuy2048 | UNKNOWN | `tests/` |
| CI/playbook | @Qwertypoiuy2048 | UNKNOWN | `.github/`, `scripts/`, `.githooks/` |

Agent role sign-off is procedural and does not substitute for human CODEOWNERS approval. When humans disagree, the named DRI should decide and record a meaningful architectural decision.

## Update this document when

Update when CODEOWNERS, module ownership, DRI/backups, review routing, escalation, or on-call information changes.
