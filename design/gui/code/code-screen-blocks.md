# Code Screen — Modular Program Blocks

## Direction

The Code screen uses a visual program stack. The player configures which modules are active and how much processing power each module receives. The player does not write general loops or conditionals in this screen; execution order and runtime control are handled by the game.

The central metaphor is a program assembled from code blocks with typed inputs, outputs, and optional extension sockets.

## Layout

- Desktop fullscreen, 16:9
- Top: customizable information bars
- Left: expandable saved-code and extension library
- Center: main program stack
- Right: current abilities, resulting stats, and processing summary

The existing teal, blue, purple, amber, and dark ocean palette is retained.

## Main program stack

The central workspace contains one `main-program-container` and one `main-program-header`. Modules are placed into the stack in execution order.

The first milestone includes:

- `module-movement`
- `module-scan`
- `main-program-drop-zone`

The stack is intentionally not a general-purpose programming language. The player selects and configures capabilities; the runtime determines when the program invokes them.

## Module blocks

Each module should display:

- Module name
- Active/offline state
- Input ports
- Output ports
- Compatible extension sockets
- Current processing allocation
- Frequency or priority setting
- Resource requirements

### Movement module

The movement module accepts extensions such as:

- Pathing
- Burst transmission
- Stealth movement
- Remote-control movement

The extension socket is `movement-extension-socket`.

### Scan module

The scan module accepts scan-type extensions such as:

- Deep scan
- Passive scan
- Hardware scan
- Program analysis

The extension socket is `scan-extension-socket`.

An extension changes or expands a module’s output. For example, a deep-scan extension may increase compute cost but expose additional device or connection details.

## Inputs and outputs

Ports should be typed and visually distinct. Initial port types can include:

- Signal
- Data
- Destination
- Scan result
- Process
- Extension

An extension socket accepts only compatible extension blocks. A module should show a preview when a dragged extension can fit. Invalid drops should explain the mismatch.

Examples:

```text
MOVEMENT MODULE
  IN: destination / route
  OUT: position / signal
  EXTENSION: pathing

SCAN MODULE
  IN: nearby signal
  OUT: scan result
  EXTENSION: deep scan
```

## Processing allocation

The player can decide how much processing power or frequency each module receives. Each module should expose:

- A processing allocation control
- Current compute cost
- Maximum useful allocation
- Frequency or priority mode
- Resulting quality or speed

Possible frequency modes:

- Low
- Normal
- High
- Burst
- Throttled

The UI should make tradeoffs visible. Increasing scan frequency may improve scan results but reduce movement responsiveness or leave less compute for other modules.

Suggested module data:

```json
{
  "id": "movement",
  "type": "module",
  "state": "active",
  "processing": {
    "allocated": 12,
    "minimum": 4,
    "maximum": 20,
    "frequency": "high"
  },
  "extensions": ["pathing"],
  "inputs": ["destination"],
  "outputs": ["position"]
}
```

## Replication

Most modules should support multiple active instances when the program has enough processing capacity. Replication should be represented as additional module instances in the main stack or as a count control on the module.

Some modules may not replicate because they require a unique system role, a single hardware interface, or exclusive access to a core. The module should expose:

```json
{
  "replicable": true,
  "maxInstances": null,
  "replicationCostMultiplier": 1.0
}
```

The UI must explain why a module cannot be replicated instead of silently rejecting the action.

## Compilation

Changes to the stack do not become active immediately.

1. Removed modules go offline.
2. Added modules and extensions enter the compile queue.
3. Unchanged modules remain active.
4. Processing allocations can be previewed before compilation.
5. The new configuration becomes active when compilation completes.

Suggested states:

- `active`
- `pending-add`
- `pending-remove`
- `offline`
- `compiling`
- `blocked`
- `failed`

The SVG uses `compile-status` to show a 62% compilation state while the current modules remain visible.

## Saved-code library

The left library supports expandable menus and multiple sorting modes.

Initial groups:

- Modules
- Extensions
- Compatible now
- Requires more compute
- Requires hardware
- Risky or unknown

Initial saved items:

- `saved-code-movement`
- `saved-code-scan`
- `saved-code-copy`
- `saved-extension-pathing`
- `saved-extension-burst`
- `saved-extension-deep-scan`
- `saved-extension-passive-scan`

## Stable element IDs

- `customizable-info-bars`
- `saved-code-sidebar`
- `main-program-stack`
- `main-program-container`
- `main-program-header`
- `module-movement`
- `module-scan`
- `movement-extension-socket`
- `scan-extension-socket`
- `movement-processing-control`
- `scan-processing-control`
- `main-program-drop-zone`
- `working-stats-panel`
- `compile-status`

## First milestone acceptance criteria

The first implementation is successful when the player can:

1. See the main program stack.
2. Drag a module into the stack.
3. Drag a compatible extension into a module socket.
4. See invalid extension drops explained.
5. Allocate more or less compute to a module.
6. Change a module’s frequency or priority.
7. See resulting ability stats update.
8. Replicate a module when capacity allows.
9. See a changed configuration enter compilation.
10. See unchanged modules remain active while changed modules are offline or compiling.
