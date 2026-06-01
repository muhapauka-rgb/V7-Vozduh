# P5.1 State Access Review

## Direct File Access

The canonical access pattern is direct file access through `STATE_DIR`.

Default:

`/opt/v7/egress/state`

Environment override:

`V7_STATE_DIR`

## Registry Loading

Registry parsing is centralized through simple key/value line parsing:

- `admin_core/registry_readers.py`
- `admin/v7-admin-api::parse_registry`

The parser is presentation-safe and redacts sensitive values.

## Hash Generation

Runtime action recheck computes hashes in `admin_core/operator_execution.py`:

- `sha256_file(users.registry)`
- `sha256_file(egress.registry)`
- selected moves canonical JSON hash
- runtime snapshot hash over users, egress, and selected moves hashes

Admin runtime fingerprint computes file-level components from:

- `users.registry`
- `egress.registry`
- `v7-state.json`
- policy files
- service preferences

## Selected Moves Loading

For P5 action recheck, selected moves are loaded from:

- `selected-moves.json`
- `selected_moves.json`
- `current-selected-moves.json`

If none exists, `operator_execution.selected_moves_state(...)` treats selected moves as empty and hashes `[]`.

For admin execution gates, selected moves also checks `autoswitch-selected-moves.json` and historical local copies. Those historical copies are not valid for P5.1 runtime truth.

## Verdicts

- state_access_understood=true
- canonical_state_dir_model=true
- hash_generation_understood=true
- selected_moves_access_understood=true
