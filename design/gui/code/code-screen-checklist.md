# Code Screen Functional Example Checklist

## Scope

Build a functional example of the modular Code screen using the existing 16:9 layout and color scheme.

The example should demonstrate configuring a main program with modules, attaching extensions, allocating compute, and compiling changes. It does not need a full game backend yet.

## Screen foundation

- [ ] Open the Code screen in a 16:9 fullscreen layout.
- [ ] Display the top information bars.
- [ ] Preserve the established dark ocean, teal, blue, purple, and amber visual style.
- [ ] Display the saved-code sidebar.
- [ ] Display the main program workspace.
- [ ] Display the working-state panel.
- [ ] Allow the major panels to collapse or expand.

## Information bars

- [ ] Show storage used and maximum storage.
- [ ] Show compute used and maximum compute.
- [ ] Show memory used and maximum memory.
- [ ] Show active cores and maximum cores.
- [ ] Allow a bar to be hidden.
- [ ] Allow bars to be reordered.
- [ ] Provide a placeholder for adding another telemetry bar.
- [ ] Keep the bar layout independent from the program module layout.

## Saved-code sidebar

- [ ] Show saved modules.
- [ ] Show saved extensions.
- [ ] Expand and collapse code categories.
- [ ] Sort saved code by at least one criterion.
- [ ] Display compatibility status.
- [ ] Display requirement warnings.
- [ ] Distinguish modules from extensions.
- [ ] Make saved items draggable.

Suggested initial items:

- [ ] Movement module
- [ ] Scan module
- [ ] Copy Data module

## Main program stack

- [ ] Show a single main program container.
- [ ] Allow a module to be dragged into the stack.
- [ ] Allow modules to be reordered.
- [ ] Allow a module to be removed.
- [ ] Show module name and state.
- [ ] Show module inputs.
- [ ] Show module outputs.
- [ ] Show compatible extension sockets.
- [ ] Show an obvious drop target when dragging.
- [ ] Reject invalid drops with a readable explanation.
- [ ] Do not implement general loops or conditionals in this milestone.

## Module behavior

- [ ] Movement accepts a Pathing extension.
- [ ] Movement shows destination input and position output.
- [ ] Scan accepts a Deep Scan or Passive Scan extension.
- [ ] Scan shows nearby-signal input and scan-result output.
- [ ] Copy Data can be placed in the main stack.
- [ ] Each module can be activated or deactivated.
- [ ] Each module displays its resource requirements.
- [ ] Each module displays its current processing allocation.

## Ports and extensions

- [ ] Give ports clear visual types.
- [ ] Highlight compatible ports during drag operations.
- [ ] Highlight incompatible ports differently.
- [ ] Allow an extension to snap into a compatible socket.
- [ ] Prevent an extension from occupying an incompatible socket.
- [ ] Explain why an extension cannot be attached.
- [ ] Update the module’s resulting stats after an extension is attached.

## Processing allocation

- [ ] Let the player assign compute to a module.
- [ ] Enforce minimum allocation requirements.
- [ ] Enforce available compute limits.
- [ ] Show current allocation and maximum useful allocation.
- [ ] Support at least Low, Normal, and High frequency.
- [ ] Make higher frequency visibly affect the resulting ability stats.
- [ ] Show when another module must lose processing to support the change.

## Replication

- [ ] Allow a supported module to be added more than once.
- [ ] Charge additional compute or core capacity for each instance.
- [ ] Show the number of active instances.
- [ ] Prevent replication when capacity is insufficient.
- [ ] Explain why a non-replicable module cannot be duplicated.

## Working-state panel

- [ ] List active abilities.
- [ ] List offline abilities.
- [ ] List compiling abilities.
- [ ] Show resulting ability statistics.
- [ ] Show current processing allocation summary.
- [ ] Update the panel when modules or extensions change.
- [ ] Show unavailable abilities as unavailable rather than hiding them.

## Compilation

- [ ] Detect when the program has unsaved changes.
- [ ] Mark removed modules as offline.
- [ ] Keep unchanged modules active.
- [ ] Place new modules and extensions into a compile queue.
- [ ] Display a new vs old stats in the Working-state panel
- [ ] The program should display a time to compile for staged changes

## Basic validation tests

- [ ] Drag Movement into the main program.
- [ ] Attach Pathing to Movement.
- [ ] Confirm Movement stats update.
- [ ] Drag Deep Scan onto Scan.
- [ ] Confirm an invalid extension is rejected.
- [ ] Increase Scan processing allocation.
- [ ] Confirm available compute decreases.
- [ ] Add a second supported module instance.
- [ ] Confirm replication consumes additional capacity.
- [ ] Remove a module.
- [ ] Confirm it becomes offline.
- [ ] Add a replacement module.
- [ ] Confirm unchanged modules remain active during compilation.
- [ ] Complete compilation.
- [ ] Confirm the replacement becomes active.
- [ ] Hide and reorder an information bar.
- [ ] Collapse and expand the saved-code categories.
