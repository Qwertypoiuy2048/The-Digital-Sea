# Glossary

- **Program**: the configured collection of module instances owned by the player.
- **Module definition**: catalog entry describing a module's compute tiers, memory size, requirements, and behavior metadata.
- **Module instance**: a placed module with an instance ID and current compute allocation.
- **Extension**: catalog entry attachable to compatible module types to change costs/effects.
- **Cached module/extension**: definition ID available in the local cached inventory.
- **Compute**: module and extension processing allocation; default capacity is 256.
- **Memory**: module/extension storage usage; default capacity is 128.
- **Core**: runtime capacity consumed by effects such as dual-thread scheduling; default capacity is 2.
- **Network cache**: local JSON snapshot of nodes and connections; it is not a live network connection.
- **Monitored**: data flag rendered with monitored styling; game-domain status, not application telemetry.
- **Compile state**: program metadata containing state, progress, and remaining seconds.

## Update this document when

Update when a term is added, renamed, or changes meaning in code/design/docs.
