# PROGRAM Z4 Runtime Audit

## Live Runtime

- collected_at: `2026-06-01T18:17:57.977505+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`

## Candidate State

- user: `10.7.0.16`
- current egress: `vless`
- table: `1014`
- enabled: `1`

## Planner State

- planner_generation_id: `1e342e0ca505bb0d5ae5328ad911f33d48f50fd2ca8fc1427a993f205222a934`
- selected_moves: `0`
- candidate_moves_total: `0`
- healthy_egress_total: `0`
- guard: `restore_barrier_clearance_generation_expired`
- decision: `no_eligible_failover_target`

## Capacity State

- capacity operator status: `warm`
- active_users: `18`
- working_channels: `1`
- total_channels: `7`
- soft_limit: `21`
- hard_limit: `27`
- failover_hard_limit: `36`

## Target Quality Highlights

- `awg3`: role `GLOBAL_STABLE`, users `3`, blocked by `stability_below_floor`
- `awg0`: role `GLOBAL_STABLE`, users `3`, blocked by `stability_below_floor`
- `vless`: users `2`, blocked by `severity_SUSPECT`
- execution-only target: users `10`, blocked by manual/reserve/canary policy

## Post-Stress Integrity

- collected_at: `2026-06-01T18:19:40.778208+00:00`
- users_registry_hash unchanged: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash unchanged: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- checks: route `0`, reconcile `0`, killswitch `0`

## Verdict

- runtime_checks_clean=true
- production_state_unchanged=true
- live_selected_moves_zero=true
- current_candidate_movement_blocked=true

