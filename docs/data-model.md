# Data model

The current model is four repository-local JSON documents, not a database. Tables, collections, indexes, foreign keys, migrations, replication, and partitioning are N/A. No obvious personal data is present; formal PII classification is UNKNOWN — needs human confirmation.

- `data/player.json`: player ID, scanner capabilities, program containers, module instances, active extension mapping, compile state, and active node IDs.
- `data/modules.json`: five module definitions and ten extension definitions keyed by definition ID. `scan` additionally has `distance` and `details`; extension `effects` is polymorphic.
- `data/cached_modules.json`: cached module and extension definition-ID lists.
- `data/network_cache.json`: node records and connection records; connection endpoints reference node IDs.

Definition IDs must resolve across files; active-extension keys should name module instances; node IDs and connection endpoints should be referentially valid; module compute should correspond to a catalog tier. The shipped fixture has two Signal Disrupter instances without the required `combatType` extension, which the runtime reports as blocked/warnings.

`load_json()` performs no schema validation, migration, versioning, or error normalization. Runtime mutations are in memory; `update_player_data()` and `update_network_cach()` are currently no-ops. Any fixture-shape change must update normalization, tests, design notes, and `contracts.md` together.

## Update this document when

Update when any `data/*.json` schema, `data_loader.py`, `program_runtime.py`, persistence hook, or related mutation call site changes.
