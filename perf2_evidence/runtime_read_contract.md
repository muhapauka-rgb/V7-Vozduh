# PERF.2 Runtime Read Contract

## Core Rule

Brain computes.

Runtime reads.

Runtime must never recompute intelligence.

## Planner May Read

- `service-scores.json`
- `channel-service-scores.json`
- `user-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `capacity-forecast-summaries.json`
- `prediction-summaries.json`
- `overview-summary.json` only for admin contexts

## Planner Must Never Read

- raw history
- large JSONL logs
- service probe commands
- prediction engines
- SQLite rollups
- network probes
- admin overview recomputation

## Planner Must Validate

- schema
- freshness state
- `expires_at`
- confidence
- source hashes
- item count
- max file size

## Integration Status

`planner_integration_status=not_integrated_in_PERF2`

PERF.2 intentionally does not change planner behavior.
