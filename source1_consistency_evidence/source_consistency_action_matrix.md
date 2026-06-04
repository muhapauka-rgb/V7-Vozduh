# SOURCE_CONSISTENCY_ACTION_MATRIX

Program: PROGRAM_SOURCE1_SNAPSHOT_SOURCE_CONSISTENCY_CLOSURE_AND_OPERATOR_VISIBLE_UNLOCK
Date: 2026-06-05

| State | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_MATCH | Required snapshot source_hashes match post-refresh planner source inputs | Trust snapshot family | Allow snapshot-backed advisory context | tools/v7-users-autoswitch | snapshot gate | plan.safety.intelligence_snapshots.results | none | planner_advisory_context_available |
| SOURCE_WARNING | Advisory family stale or warning only | Ignore or warn without movement authority | Keep required families authoritative, mark advisory family ignored/warned | tools/v7-users-autoswitch | snapshot reader validation | ignored_families/warn_families | advisory promotion | planner_continues_without_that_advice |
| SOURCE_MISMATCH | Required family hash mismatch | Fail closed | Set runtime_behavior=STOP | tools/v7-users-autoswitch | source_hash comparison | validation_errors/source_mismatch_families | selected_moves, apply, operator_visible_promotion | fail_closed_snapshot_gate |
| SOURCE_VOLATILE | Refresh cannot get stable source bundle | Fail closed | Do not write snapshots, stop pre-planner path | tools/v7-intelligence-snapshot-refresh and tools/v7-users-autoswitch | source consistency retries exhausted | source_consistency_errors/pre_planner_refresh.state | selected_moves, apply, operator_visible_promotion | fail_closed_pre_planner_refresh |
| SOURCE_UNVERIFIED | Missing/corrupt required snapshot | Fail closed | Stop required family | tools/v7-users-autoswitch | snapshot read/validation | validation_errors/stop_families | selected_moves, apply, operator_visible_promotion | fail_closed_snapshot_gate |

