# UX baseline

## Current journeys

1. Launch: the app opens on the Code screen.
2. Configure program: inspect telemetry and library, select a module, add/remove compatible modules or extensions, change compute tier, and scroll panels.
3. Inspect network: switch to Network, click nodes/connections for readouts, zoom with the wheel, pan with middle/right drag, and return to Code.
4. Review state: read warnings, resource bars, cached/active styling, and selected-object details.

The Code screen uses independent scrollable library/workspace/state regions and click-to-open menus. Escape closes menus. The Network screen uses visual distinctions for active/cached nodes, bandwidth, stability, security, and monitored state. These facts are grounded in `code_screen.py`, `network_screen.py`, and `design/gui/*`.

## Accessibility and known gaps

No formal WCAG target, keyboard navigation, focus model, screen-reader text layer, localization policy, or non-pointer map interaction is implemented; target and enforcement are UNKNOWN. Color encodings have some shape redundancy (dashes, thickness, lock icon), but accessibility remains a prototype gap.

Design/code mismatches to preserve as known issues: cached-node `C` markers and route planning are specified but not implemented; monitored connections are purple but lack the specified `!` marker; incompatible choices can fail without explanatory feedback; module removal has no confirmation/undo.

## Update this document when

Update when screens, interactions, design specs, accessibility, localization, or user journeys change.
