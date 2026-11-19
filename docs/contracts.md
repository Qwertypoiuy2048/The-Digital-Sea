# Contracts inventory

Exhaustive current inventory as of 2026-11-19. HTTP/GraphQL/gRPC routes, webhooks, published events, queues, cron jobs, feature flags, and remote integrations are **N/A — none exist in the application**.

## Application and screen contracts

| Contract | Shape / invariant | Blast radius |
|---|---|---|
| `main.main()` (`main.py`) | Initializes Pygame, loads `player.json`, `modules.json`, `cached_modules.json`, `network_cache.json`, creates screens, starts `code`, dispatches events, draws at `FRAME_RATE`, then quits. | Process entry point; changes affect every run. |
| `Screen.handle_event(event)` / `Screen.draw(surface)` (`screen.py`) | Two-method screen interface. | `ScreenManager`, both screens, UI tests. |
| `ScreenManager(screens, starting_screen)` and methods in `screen_manager.py` | Screen name must exist or `KeyError`; event handler may return a screen name; optional `refresh()` runs on activation. | `main.py`, both screens, tests. |

## Public Python interfaces

`data_loader`: `load_json(filename: str) -> dict` reads `data/<filename>` as UTF-8 JSON; `update_player_data(player: dict) -> None` is a no-op; `update_network_cach(network_cache: dict) -> None` is a no-op and its spelling is compatibility-sensitive.

`program_runtime`: `_as_number(value, fallback=0)`, `_frequency(definition, allocation)`, `_scaled_extension_cost(base_cost, frequency)`, `build_program_runtime(player, module_catalog, resource_capacity=None, cached_modules=None)`, `remove_module_instance(player, instance_id)`, `remove_extension_from_instance(player, instance_id, extension_id)`, `adjust_module_compute(player, module_catalog, instance_id, direction)`, `module_compute_error(player, module_catalog, instance_id, direction)`, `module_add_error(player, module_catalog, cached_modules, definition_id)`, `add_module_instance(player, module_catalog, cached_modules, definition_id)`, `extension_add_error(player, module_catalog, cached_modules, instance_id, extension_id)`, and `add_extension_to_instance(player, module_catalog, cached_modules, instance_id, extension_id)`.

`code_layout`: `scale_rect(rect, surface_size)`, `screen_rects(surface_size)`, `telemetry_rects(surface_size)`; layouts scale from `DESIGN_SIZE` and remain inside the design surface.

`network_layout.compute_node_positions(nodes, connections, primary_id)` returns deterministic positions for every node, including disconnected nodes.

`network_screen`: `distance_to_segment(point, start, end)` and `NetworkScreen` methods in `network_screen.py` are consumed by `ScreenManager` and tests; coordinate transforms round-trip and zoom remains between `MIN_ZOOM` and `MAX_ZOOM`.

`code_screen`: `CodeScreen` methods in `code_screen.py` are consumed by `ScreenManager`, Pygame events, and UI tests. Module/extension operations preserve runtime validation and call the current no-op persistence hook.

`drawing`: `draw_transparent_line`, `draw_dashed_line`, `draw_transparent_circle`, `draw_fuzzy_glow`, `draw_cubic_curve`, `draw_lock`, `draw_background`, `draw_help` render on a Pygame surface without changing application data.

`constants.node_radius(size: str) -> float` returns a configured radius or `30` fallback.

## JSON contracts

`data/player.json`: top-level `playerId`; `scanner.level`; `scanner.capabilities` with `scanDistance`, `nodeSize`, `nodePower`, `nodePrograms`, `connectionBandwidth`, `connectionStability`, `connectionSecurity`; `program` list; `activeNodes.primary` and `activeNodes.secondary`. Each program has `instanceId`, `modules`, `activeExtensions`, and `compile` (`state`, `progress`, `remainingSeconds`). Each module has `instanceId`, `definitionId`, `compute`.

`data/modules.json`: `modules` and `extensions` mappings. Module definitions have `name`, `necessaryExtensions`, `optionalExtensions`, `description`, `lowCompute`, `mediumCompute`, `highCompute`, `replicable`, `cooldown`, `automatic`, `compileTime`, `size`, with `scan` additionally using `distance` and `details`. Extension definitions have `name`, `type`, `description`, `computeCost`, `compileTime`, `effects`, `size`; effects may contain `details`, `cooldown`, `automatic`, `distance`, `size`, `cores`, or `highCompute`.

`data/cached_modules.json`: `modules` and `extensions` lists of catalog IDs; validation treats them as availability.

`data/network_cache.json`: `nodes` with `id`, `state`, `size`, `label`, `monitored`; `connections` with `from`, `to`, `bandwidth`, `stability`, `security`, `monitored`.

## Configuration, integrations, and invariants

- Application environment variables, feature flags, persistence, auth, secrets, telemetry, background jobs, and external integrations: N/A. Tests set `SDL_VIDEODRIVER=dummy` for headless Pygame.
- Runtime derivation must not mutate player input.
- Missing required extensions block modules and produce warnings; missing/duplicate/incompatible selections return errors.
- Compute changes move only across low/medium/high tiers and stop at limits.
- Cached memory counts only known catalog IDs.
- Layout/drawing works at tested sizes; network zoom is bounded.

## Verification and maintenance

Inventory derived by enumerating definitions/imports with `rg`, reading all application modules, JSON fixtures, design notes, tests, requirements, CI, and CODEOWNERS; behavior was cross-checked against both test modules. Update this file in the same change as any route (future), JSON key/return field, public signature, event contract, integration, environment read, flag, job, or invariant change.
