# Local test failure

1. Run `python -m unittest discover -v` from the repository root.
2. If Pygame cannot import, install `requirements.txt`; for headless execution set `SDL_VIDEODRIVER=dummy` before importing Pygame.
3. If the runtime fixture assertion fails, inspect `data/player.json`, `data/modules.json`, and `program_runtime.py` together; do not weaken the test without documenting the contract decision.
4. Record environment and result in the task/review artifact. There is no production escalation path yet.
