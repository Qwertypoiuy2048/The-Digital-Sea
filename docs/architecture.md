# Architecture

Descriptive of the current local prototype. Sources: `main.py`, `screen_manager.py`, `screen.py`, `code_screen.py`, `network_screen.py`, `program_runtime.py`, `data_loader.py`, and `constants.py`.

## Runtime shape

```text
data/*.json -> load_json -> main.py shared state -> ScreenManager -> CodeScreen
                                                     \-> NetworkScreen
                         Pygame event loop / resizable window
```

`main.main()` initializes Pygame, opens a resizable `1000x800` window, loads four JSON files, constructs both screens with the same state dictionary, starts on `code`, dispatches events, draws the active screen, flips the display, and caps the loop at 60 FPS. `pygame.quit()` runs after the loop.

The Code screen derives program state through `program_runtime.py` and mutates the in-memory player fixture for module/extension actions. The Network screen derives node positions from the network cache and maintains camera, selection, drag, and zoom state locally. `data_loader.py` exposes persistence hooks, but both update functions are currently no-ops.

## Boundaries and security

- Presentation: `Screen` defines `handle_event(event)` and `draw(surface)`; `ScreenManager` routes to the active implementation.
- Data: `load_json()` reads only from the repository `data/` directory.
- Runtime: `program_runtime.py` calculates derived resources and validates/mutates program state.
- External: no sockets, HTTP clients, cloud services, database drivers, secrets, or OS services exist in the application.

This is an offline prototype. No identity, authorization, secret, PII, or remote trust boundary is implemented. JSON files are trusted local fixtures; `load_json()` propagates missing-file and JSON parsing errors.

The current scale is one local process with small JSON fixtures. Persistence, multiplayer, remote content, or online services would be architectural changes requiring a threat model and ADR.

## Update this document when

Update when entry-point flow, screen routing, screen implementations, runtime boundaries, data loading/persistence, dependencies, or trust boundaries change.
