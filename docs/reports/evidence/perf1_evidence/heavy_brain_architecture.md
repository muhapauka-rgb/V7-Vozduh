# PERF.1 Heavy Brain Architecture

## Principle

Brain may be heavy. Runtime may not be heavy.

Heavy Brain runs outside the hot runtime path and publishes compact, versioned, freshness-aware summaries.

## Responsibilities

- service testing
- service history aggregation
- route-class suitability scoring
- user service weight aggregation
- execution trust aggregation
- dynamic blast radius recommendations
- predictive routing foundation
- capacity forecasting
- anomaly and degradation detection
- log/history compaction

## Inputs

- service matrix probe results
- egress quality samples
- service preferences
- users/egress registries
- audit/event JSONL logs
- traffic SQLite summaries or compact exports
- route reality probe outputs
- runtime state snapshots

## Outputs

- `service-scores`
- `channel-service-scores`
- `user-service-scores`
- `route-class-scores`
- `risk-summaries`
- `trust-summaries`
- `blast-radius-summaries`
- `capacity-forecast-summaries`
- `prediction-summaries`
- `admin-overview-summaries`

## Heavy Brain Must Never Do

- move users
- approve execution
- bypass planner
- bypass governance
- write selected moves directly
- mutate runtime state
- restart services

## Processing Model

- background worker or explicit refresh command
- adaptive probe scheduler
- bounded history compaction
- atomic snapshot writes
- freshness and confidence attached to every output
- runtime rejects UNKNOWN or stale required summaries when policy requires them
