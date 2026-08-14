# SOURCE_CONSISTENCY_REALITY_MAP

Program: PROGRAM_SOURCE1_SNAPSHOT_SOURCE_CONSISTENCY_CLOSURE_AND_OPERATOR_VISIBLE_UNLOCK
Date: 2026-06-05

## Inputs

service_matrix:

- file: /opt/v7/egress/state/service-matrix.json
- refresh build read: tools/v7-intelligence-snapshot-refresh load_inputs()
- snapshot hash owner: admin_core.routing_intelligence.sha256_json()
- planner validation read: tools/v7-users-autoswitch AutoswitchPlanner.matrix
- planner gate validation: _intelligence_snapshot_source_mismatches()

quality_summary:

- file: /opt/v7/egress/state/egress-quality-summary.json
- refresh build read: tools/v7-intelligence-snapshot-refresh load_inputs()
- snapshot hash owner: admin_core.routing_intelligence.sha256_json()
- planner validation read: tools/v7-users-autoswitch AutoswitchPlanner.quality_summary
- planner gate validation: _intelligence_snapshot_source_mismatches()

service_preferences:

- file: /opt/v7/egress/state/service-preferences.json
- refresh build read: tools/v7-intelligence-snapshot-refresh load_inputs()
- snapshot hash owner: admin_core.routing_intelligence.sha256_json()
- planner validation read: tools/v7-users-autoswitch AutoswitchPlanner.service_prefs
- planner gate validation: _intelligence_snapshot_source_mismatches()

## Previous Divergence

AutoswitchPlanner loaded service_matrix and quality_summary during __init__ before running pre-planner refresh. The refresh command then read current source files, built snapshots, and wrote source_hashes from its own source read. If service_matrix or quality_summary changed during that window, the planner gate compared refreshed snapshots against stale in-memory planner inputs.

Classification:

- primary: STALE_SOURCE_REFERENCE
- secondary: TIMING_RACE
- not accepted as fix: weakening source hash gate

## Closure

After REFRESH_SUCCESS in write mode, tools/v7-users-autoswitch now reloads:

- service_matrix
- quality_summary
- service_preferences

before loading and validating the snapshot bundle.

Written evidence path:

```text
plan.safety.intelligence_snapshots.pre_planner_refresh.source_reload
```

## Decision -> Action

Condition: pre-planner refresh writes snapshots successfully.
Decision: planner must validate snapshots against current post-refresh source inputs.
Action: reload source inputs before snapshot gate.
Executor: tools/v7-users-autoswitch.
Trigger: REFRESH_SUCCESS with --pre-planner-refresh=write.
Written Evidence: plan.safety.intelligence_snapshots.pre_planner_refresh.source_reload.
Blocked Actions: none.
Next State: load_refreshed_snapshots_with_current_source_inputs.

