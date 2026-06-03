# PERF.1 Implementation Roadmap

## PERF.2 - Snapshot Store

Goal:

- Define versioned intelligence snapshot schemas and storage ownership.

Scope:

- snapshot envelope
- freshness/confidence model
- source hashes
- snapshot readers
- runtime gate semantics
- no background workers yet unless explicitly approved

Success:

- runtime can read compact summaries with known freshness
- stale/UNKNOWN behavior is defined

## PERF.3 - Background Intelligence Workers

Goal:

- Move expensive service/history/trust/risk work into explicit workers.

Scope:

- service score worker
- audit trust aggregator
- quality/history compactor
- adaptive probe scheduler
- snapshot atomic writes

Success:

- Heavy Brain produces compact summaries
- runtime no longer needs heavy reads

## PERF.4 - Runtime Fast Path Integration

Goal:

- Planner consumes snapshots instead of recomputing heavy intelligence.

Scope:

- bounded snapshot reader
- RI advisory score from precomputed summaries
- stale/UNKNOWN gate
- selected-move hash preservation

Success:

- planner remains deterministic and fast at 2000 users / 50 channels

## PERF.5 - Admin Performance Layer

Goal:

- Admin overview and diagnostics read snapshots by default.

Scope:

- overview snapshot read path
- explicit refresh/status actions
- async diagnostic result surfaces
- pagination and bounded history reads

Success:

- admin UI remains responsive without hidden probes
