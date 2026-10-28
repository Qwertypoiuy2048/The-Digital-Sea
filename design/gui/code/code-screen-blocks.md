# Code Screen - Interactive Program Blocks

## Direction

The Code screen is a visual program configuration interface. The player selects modules and extensions, changes module compute tiers, and reviews the resulting abilities and resource usage. It is not a general-purpose programming language: execution order and runtime behavior are determined by the game.

The current frontend uses click-to-open control menus. Drag-and-drop editing is a future interaction option, not a current requirement.

## Layout

- Top: player, compute, memory, and core telemetry.
- Left: cached module and extension library, grouped by extension type.
- Center: scrollable active program stack.
- Right: scrollable active abilities and processing summary.
- Bottom of the left and right panels: pinned memory and compute usage bars.

The existing teal, blue, purple, amber, and dark ocean palette is retained. Panel content scrolls independently while panel titles and resource bars remain visible.

## Main program stack

The central workspace shows the active program instance and its modules in order. Each module is rendered as a card with attached extensions displayed to its right as connected extension boxes.

Clicking a module opens its control menu. The current menu supports:

- Remove module.
- Add a compatible cached extension.
- Remove an attached extension.
- Increase or decrease the module's compute tier.

Missing required extension types are shown as red requirement boxes, and the module is visibly marked inactive.

## Module blocks

Each module displays:

- Module name and instance ID.
- Active or inactive state.
- Description text.
- Current frequency and compute usage.
- Module and extension memory size.
- Attached extension boxes.
- Missing required extension types when applicable.

Input and output ports are deferred. They are not part of the current frontend pass.

## Extension interaction

Extensions can be selected in either of two ways:

1. Click an extension in the left library, then choose a compatible active module instance.
2. Click an active module, choose `ADD EXTENSION`, then choose a compatible cached extension.

The interface shows incompatible or unavailable choices in an error color with an explanatory message where space permits. Attached extensions show their adjusted compute costs.

## Processing controls

Modules expose low, medium, and high compute tiers through the control menu. The screen shows:

- Current allocation and frequency.
- Module base compute cost.
- Per-extension compute cost.
- Total active compute usage.
- Available compute.

The processing bars fill proportionally. A resource exceeding capacity turns red and displays an error state.

## Replication

Replicated modules appear as separate instance cards in the program stack. Instance IDs are used to associate extensions with the correct module instance.

The library and add-module popup communicate when a module is unavailable, cannot be duplicated, or cannot fit the current compute budget.

## Compilation and runtime effects

Compilation behavior and extension gameplay effects are deferred backend features. The current screen displays the loaded configuration and derived preview values; it does not yet present a compilation queue or apply extension effects such as cooldown, distance, or core changes.

## Library

The left library contains cached modules and extensions. Modules are grouped together, while extensions are grouped by extension type. Each item retains a status color and exposes a hover bubble containing its availability and compute information.

Clicking a module opens its add-module popup. Clicking an extension opens its module-target popup. Popups render above the library and workspace content so the selected item remains visible.

## Text and responsive behavior

- Descriptions wrap inside their cards.
- Compact labels use a single line with ellipsis when necessary.
- Popup error messages wrap within their available area.
- Extension names reserve space for their compute values.
- Workspace, library, and state panels remain scrollable at smaller window sizes.

## Stable element IDs

- `customizable-info-bars`
- `saved-code-sidebar`
- `main-program-stack`
- `main-program-container`
- `main-program-header`
- `module-instance-card`
- `extension-connection-box`
- `module-control-popup`
- `extension-target-popup`
- `working-stats-panel`
- `memory-usage-bar`
- `compute-usage-bar`
