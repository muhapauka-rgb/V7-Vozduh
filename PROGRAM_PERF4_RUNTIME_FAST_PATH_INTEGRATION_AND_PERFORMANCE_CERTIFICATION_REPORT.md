# PROGRAM PERF.4 — Runtime Fast Path Integration, Snapshot Consumption And Performance Certification Report

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Date: 2026-06-03

## Executive Verdict

PERF.4 is complete.

Runtime planner now has a snapshot-backed fast path for routing intelligence. When a runtime intelligence snapshot store is active, `tools/v7-users-autoswitch` consumes compact snapshot files instead of constructing `RoutingBrain` and reading runtime history in the hot path.

No deployment, autoswitch apply, user movement, runtime mutation, service restart, systemd mutation, cleanup, merge, pull, or push was performed.

## Discovery Result

Existing runtime ownership remains centralized in:

- `tools/v7-users-autoswitch`

Existing heavy intelligence components:

- `admin_core/routing_brain.py`
- `admin_core/routing_intelligence.py`
- `admin_core/intelligence_snapshots.py`
- `admin_core/intelligence_workers.py`

Pre-PERF.4 runtime planner still instantiated `RoutingBrain` directly and read `switch-history.jsonl` through `_recent_audit_records()`.

PERF.4 did not create a parallel orchestrator or duplicate execution path. It extended the existing planner with read-only snapshot consumption.

## Runtime Snapshot Integration

Added runtime snapshot root:

- default: `/opt/v7/egress/state/intelligence`
- CLI: `--intelligence-snapshot-root`

Integrated snapshot families:

- `service-scores`
- `channel-service-scores`
- `user-service-scores` advisory-only
- `risk-summaries`
- `trust-summaries`
- `blast-radius-summaries`

Required runtime fast-path families:

- `service-scores`
- `channel-service-scores`
- `risk-summaries`
- `trust-summaries`
- `blast-radius-summaries`

Not integrated in PERF.4:

- `capacity-forecast-summaries`

Reason: current runtime already owns load/capacity guards through existing state and dynamic load logic, while the current PERF.3 worker set does not produce capacity snapshots. Pulling capacity snapshots into PERF.4 would create a false mandatory dependency.

## Fast Path Behavior

When snapshot store is absent:

- planner keeps legacy `RoutingBrain` fallback
- behavior remains compatible with existing runtime tests

When snapshot store is active and valid:

- candidate advisory ranking uses `channel-service-scores.json`
- advisory context uses risk/trust/blast snapshots
- runtime history is not read in the snapshot-backed path
- planner remains the decision owner
- snapshots have no execution, governance, or selected move authority

When required snapshot truth is unsafe:

- selected moves are suppressed
- terminal reason becomes `dry_run_intelligence_snapshot_stop_required`
- governance/execution/rollback paths are not touched

## Fail-Closed Gate

The runtime snapshot gate stops selected moves for:

- missing required snapshot
- corrupt required snapshot
- expired required snapshot
- unknown required snapshot freshness
- low required snapshot confidence
- stale runtime-required snapshot with STOP behavior
- oversized required snapshot
- source hash mismatch for runtime source-backed snapshots

Advisory-only `user-service-scores` can be stale or missing without suppressing selected moves.

## Authority Preservation

Planner decision owner:

- `tools/v7-users-autoswitch`

Snapshot write authority:

- none in runtime

Execution authority:

- none in snapshots

Selected moves write authority:

- none in snapshots

Hard gate override:

- forbidden

Reservation/canary/manual-only override:

- forbidden

Governance bypass:

- forbidden

## Code Changes

Modified:

- `tools/v7-users-autoswitch`
- `admin_core/intelligence_snapshots.py`
- `tests/unit/test_intelligence_snapshots.py`

Added:

- `tests/unit/test_runtime_snapshot_fast_path.py`
- `perf4_evidence/discovery_and_duplication_audit.md`
- `perf4_evidence/performance_certification.json`
- `perf4_evidence/verification.md`

Contract update:

- `runtime_read_contract()["planner_integration_status"] = "integrated_in_PERF4_runtime_fast_path"`
- added `perf4_integrated_runtime_families`

## Performance Certification

Read-only local benchmark:

```json
{
  "runs": 25,
  "legacy_mean_ms": 2.7198,
  "legacy_p95_ms": 3.0028,
  "snapshot_mean_ms": 1.1775,
  "snapshot_p95_ms": 1.3808,
  "snapshot_mode": "snapshot_backed_planner_advisory_context",
  "selected_moves": 1,
  "stop_required": false
}
```

Verdict:

- performance_budget_pass=true

## Verification

Compile:

```text
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m py_compile tools/v7-users-autoswitch admin_core/intelligence_snapshots.py
```

Result: PASS

Targeted tests:

```text
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m unittest tests.unit.test_runtime_snapshot_fast_path tests.unit.test_intelligence_snapshots tests.unit.test_routing_brain
```

Result:

```text
Ran 28 tests in 0.202s
OK
```

Full suite:

```text
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m unittest discover tests
```

Result:

```text
Ran 245 tests in 15.210s
OK
```

## Evidence

Evidence folder:

- `perf4_evidence/`

Evidence files:

- `perf4_evidence/discovery_and_duplication_audit.md`
- `perf4_evidence/performance_certification.json`
- `perf4_evidence/verification.md`

## Final Verdicts

snapshot_runtime_integration_complete=true

runtime_fast_path_certified=true

heavy_brain_runtime_separation_complete=true

logs_history_flow_certified=true

performance_budget_pass=true

tests_pass=true

safe_to_begin_RI4=true

