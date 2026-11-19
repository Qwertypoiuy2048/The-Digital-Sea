# Onboarding

1. Read `AGENTS.md` Quick Summary and this folder: `architecture.md`, `stack.md`, `domain.md`, `contracts.md`, then the area-specific doc.
2. Read `tasks/INDEX.md` and the relevant task file; do not use `.starter/` as project history.
3. Use Python 3.13 (verified locally), install Pygame from `requirements.txt`, and run `python main.py` from the repository root. Python 3.14 currently falls back to an incompatible Pygame source build.
4. Run the test suite with `python -m unittest discover -v`. UI tests require Pygame; headless CI uses `SDL_VIDEODRIVER=dummy`.
5. Install hooks with `sh scripts/setup-hooks.sh` in a POSIX shell where required.
6. Before code, copy `tasks/_TEMPLATE.md`, get the plan through the Agentic review process, and use `.github/pull_request_template.md` and `.github/CODEOWNERS`.

For questions, use `ownership.md`; the current DRI is `@Qwertypoiuy2048`, while backups and communication channels are UNKNOWN. A safe first contribution is a focused test or documentation correction that preserves contracts. 30/60/90-day expectations are intentionally lightweight: first understand the fixtures and runtime, then own a small vertical slice, then propose a grounded architectural improvement.

## Update this document when

Update when setup, commands, read order, hooks, review process, contacts, or newcomer expectations change.
