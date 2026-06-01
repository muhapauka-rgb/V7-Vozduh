# PROGRAM Z3.2 Runtime Audit

## Runtime Inputs

- state_dir: `/opt/v7/egress/state`
- users registry: live
- egress registry: live
- planner: live
- rollback command: live
- route verification: live

## Before Execution

- collected_at: `2026-06-01T17:57:11.920504+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- candidate: `10.7.0.16`, `vless`, table `1014`

## During Execution

- selected_moves: `1`
- moved_user: `10.7.0.16`
- target: `awg3`
- planner guard: `restore_barrier_clearance_budget_and_generation_ok`
- autoswitch_apply_result: `applied=true`
- verify_rc: `0`

## After Execution

- collected_at: `2026-06-01T17:58:28.439309+00:00`
- users_registry_hash: `40c342ee47d7ed20db44939686f8732a2423a023fb68610140edbf0854733f70`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- candidate: `10.7.0.16`, `awg3`, table `1014`
- route_check: `OK`

## Restore-Settle Observation

- gate_status: `CONDITIONAL`
- checkers_ok: `true`
- mutation: `false`
- runtime_commands_executed: `false`
- reason: `sample_count_below_required:1<3`
- reason: `apply_timer_intervals_below_required:0.00<2`
- action: rollback was performed explicitly instead of promoting the state.

## Final State

- collected_at: `2026-06-01T17:59:57.857017+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`
- candidate: `10.7.0.16`, `vless`, table `1014`

## Verdict

- live_runtime_audited=true
- final_state_restored=true
- runtime_checks_clean=true
- egress_registry_unchanged=true

