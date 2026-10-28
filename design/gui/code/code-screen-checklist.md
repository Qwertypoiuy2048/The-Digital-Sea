# Code Screen Frontend Checklist

## Current frontend scope

- [x] Show player, compute, memory, and core telemetry.
- [x] Show the cached module and extension library.
- [x] Group extensions by extension type.
- [x] Show module instances in the main program stack.
- [x] Connect attached extensions to their module cards.
- [x] Show inactive modules and missing required extension types.
- [x] Open a control popup when a module is clicked.
- [x] Add and remove modules through the visible controls.
- [x] Add extensions from a module popup.
- [x] Add extensions by clicking an extension in the library.
- [x] Remove attached extensions.
- [x] Increase and decrease module compute tiers.
- [x] Show module base, extension, and total compute costs.
- [x] Show proportional memory and compute bars.
- [x] Show an error state when a resource exceeds capacity.
- [x] Keep panel titles and usage bars visible while content scrolls.
- [x] Wrap descriptions and constrain compact labels.
- [x] Render popups above the content they belong to.

## Deferred frontend work

- [ ] Add Escape-key dismissal for open popups.
- [ ] Add hover and pressed states for popup actions.
- [ ] Add graceful scrolling or repositioning for oversized popups.
- [ ] Add confirmation or undo feedback for destructive actions.
- [ ] Add input and output port visuals.
- [ ] Add drag-and-drop editing.
- [ ] Add compilation progress and pending-change visuals.

## Deferred backend-dependent display work

- [ ] Display applied extension gameplay effects.
- [ ] Display multiple independently editable program instances.
- [ ] Display persisted edits after restart.
