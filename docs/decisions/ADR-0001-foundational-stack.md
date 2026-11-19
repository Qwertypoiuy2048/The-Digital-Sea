# ADR-0001: Local Python/Pygame prototype stack

- Status: accepted for the current prototype; 2026-11-19.
- Context: the repository implements a local interactive 2D prototype with a Pygame event loop, JSON fixtures, and Python tests.
- Decision: keep Python, Pygame `>=2.6.0`, repository-local JSON, and `unittest` as the current stack.
- Consequences: simple local iteration and no service infrastructure; dependency versions are not reproducibly locked, persistence is absent, and distribution/online scale are unresolved.
- Alternatives: not recorded in repository history; do not infer a rejected alternative.
- Grounding: `main.py`, `requirements.txt`, `data_loader.py`, `tests/`.
