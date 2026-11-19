# The Digital Sea living documentation

These documents are the project-specific adoption of the Agentic playbook. They describe the current repository as implemented, not a planned cloud service. Read every file here before changing code, then read `tasks/INDEX.md`.

## Current scope

The Digital Sea is a local Python/Pygame prototype. `main.py` loads JSON fixtures from `data/`, creates the Code and Network screens, and runs a 60 FPS resizable event loop. There is no server, network API, database, authentication, persistence implementation, queue, or deployment artifact in the application code.

## Document map

- `architecture.md`: runtime shape and boundaries.
- `contracts.md`: exhaustive inventory of code/data/config contracts.
- `api.md`: local Python interface narrative; HTTP is N/A.
- `data-model.md`: JSON fixtures and mutation/persistence boundary.
- `stack.md`: language, dependency, tooling, and license facts.
- `testing.md`: unittest/Pygame coverage and regression procedure.
- `deployment.md`: current local-run and CI posture.
- `domain.md`, `ux.md`, `glossary.md`: product vocabulary and interaction model.
- `ownership.md`, `onboarding.md`: repository ownership and first-session path.
- `decisions/`: architectural decision records.
- `reviews/`: bootstrap review evidence and future review artifacts.
- `runbooks/`: current local failure playbooks.

## Grounding and freshness

Facts were checked against Python source, JSON fixtures, tests, design notes, requirements, CI, hooks, and CODEOWNERS on 2026-11-19. Unknown human-owned values remain `UNKNOWN — needs human confirmation`; they are not guessed.

The Agentic playbook requires unanimous nine-role consensus for `/docs/*` changes. The bootstrap review artifact records the current review status and any remaining human/process gates.

## Update this folder when

Update the affected document in the same change as any edit to its cited code, data, design, CI, ownership, or operational paths.
