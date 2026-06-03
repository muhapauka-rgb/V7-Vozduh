# PERF.3 Bounded Execution Rules

## Verified

Workers never:

- move users
- write selected moves
- approve governance
- execute runtime actions
- restart services
- call planner apply
- call `run_action`
- call `run_readonly`
- run curl/socket probes
- run SQLite rollups

## Allowed

Workers may:

- read JSON state inputs
- read bounded JSONL history tails
- parse registries
- compute in memory
- produce snapshot envelopes
- write snapshot files only when explicitly invoked

## Runtime Isolation

No imports were added from runtime planner to worker code.

No planner behavior changed.

No governance behavior changed.

No admin endpoint behavior changed.
