# PROGRAM PERF.2 - Intelligence Snapshot Store and Runtime Read Contract Report

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: Updatesystem

## Result

PASS.

PERF.2 created the canonical Intelligence Snapshot Store contract and bounded read-only snapshot readers.

No planner behavior, runtime behavior, governance, execution, deployment, service restart, user movement, or autoswitch apply was changed.

## Human Explanation

PERF.2 defines the interface between Brain and Runtime.

Brain computes expensive intelligence before runtime needs it.

Runtime reads compact snapshots only.

Runtime must not recompute service intelligence, scan raw history, run probes, execute prediction engines, or perform SQLite rollups.

## Implemented Module

`admin_core/intelligence_snapshots.py`

The module provides:

- canonical snapshot root contract
- snapshot family contracts
- universal snapshot envelope schema
- freshness model
- confidence model
- runtime stop condition matrix
- bounded read-only snapshot readers
- PERF.3 worker recommendations

It does not write files, execute commands, import planner logic, or integrate with runtime.

## Snapshot Store Architecture

Canonical location:

`/opt/v7/egress/state/intelligence/`

Ownership:

- Heavy Brain producers write complete snapshots.
- Runtime and Admin read snapshots.
- Raw history remains outside the store.
- Rotation and retention are producer-owned and bounded.

## Universal Snapshot Envelope

Required fields:

- `schema`
- `generated_at`
- `expires_at`
- `ttl_seconds`
- `freshness_state`
- `confidence`
- `source_hashes`
- `generator`
- `item_count`
- `warnings`

Every snapshot family must use this envelope.

## Snapshot Families

- `service-scores.json`
- `channel-service-scores.json`
- `user-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `capacity-forecast-summaries.json`
- `prediction-summaries.json`
- `overview-summary.json`

## Freshness Model

States:

- FRESH
- STALE
- EXPIRED
- UNKNOWN

Runtime behavior:

- FRESH: ALLOW
- STALE: family-specific WARN, IGNORE, or STOP
- EXPIRED: STOP
- UNKNOWN: STOP

## Confidence Model

Confidence is normalized from `0.0` to `1.0`.

Supported factors:

- source completeness
- history completeness
- probe completeness
- service completeness

Runtime-required snapshots below family confidence floor stop runtime use.

Advisory-only snapshots below floor are ignored.

## Runtime Read Contract

Planner may read compact snapshots only.

Planner must never read:

- raw history
- large JSONL
- service probes
- prediction engines
- SQLite rollups
- network probes
- admin overview recomputation

Planner must validate:

- schema
- freshness
- expiry
- confidence
- source hashes
- item count
- max file size

Planner integration status:

`not_integrated_in_PERF2`

## Tests

- py_compile: PASS
- `python3 -m unittest tests.unit.test_intelligence_snapshots`: PASS, 10 tests
- `python3 -m unittest discover tests`: PASS, 232 tests

## Performance Findings

- single snapshot read average: 0.0543 ms
- 9-family bundle read average: 0.5122 ms
- validation/freshness/behavior check average: 0.0049 ms

Runtime consumption remains cheap if snapshots stay compact and bounded.

## PERF.3 Recommendation

Begin PERF.3 next.

PERF.3 should implement background producers for:

- service scores
- channel service scores
- user service scores
- risk summaries
- trust summaries
- blast radius summaries
- capacity forecasts
- prediction summaries
- admin overview summaries

First recommended workers:

1. service score worker
2. trust summary worker

These remove the largest future pressure from runtime.

## Evidence

- `perf2_evidence/discovery_and_duplication_audit.md`
- `perf2_evidence/snapshot_store_architecture.md`
- `perf2_evidence/snapshot_envelope_and_families.md`
- `perf2_evidence/freshness_confidence_stop_model.md`
- `perf2_evidence/runtime_read_contract.md`
- `perf2_evidence/test_results.md`
- `perf2_evidence/performance_certification.md`
- `perf2_evidence/perf3_recommendation.md`
- `perf2_evidence/safety_scan.md`

## Final Verdicts

snapshot_store_architecture_complete=true

snapshot_envelope_complete=true

snapshot_families_defined=true

freshness_model_complete=true

confidence_model_complete=true

runtime_read_contract_complete=true

bounded_snapshot_readers_created=true

tests_pass=true

performance_certified=true

safe_to_begin_PERF3=true
