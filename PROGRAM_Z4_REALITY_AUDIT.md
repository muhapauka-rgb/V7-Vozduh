# PROGRAM Z4 Reality Audit

Program: Z4 Production Stress Certification

Mode: stress testing, reliability certification, production readiness.

## Live Runtime Snapshot

Collected from live runtime:

- collected_at: `2026-06-01T18:17:57.977505+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- candidate row: `ip=10.7.0.16 current=vless table=1014 enabled=1`
- adjacent row: `ip=10.7.0.17 current=vless table=1015 enabled=1`
- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`

## Live Planner Snapshot

Command shape:

- `v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE --user 10.7.0.16 --target-egress awg3`

Planner result:

- users_total: `18`
- egress_total: `7`
- healthy_egress_total: `0`
- candidate_moves_total: `0`
- selected_moves: `0`
- current_egress: `vless`
- recommended_egress: `vless`
- decision: `no_eligible_failover_target`

## Health, Capacity, Trust Reality

Current target pool is not production-autonomy-ready:

- capacity operator status: `warm`
- active users: `18`
- working channels: `1`
- healthy egress total in planner: `0`
- `awg3` blocked by `stability_below_floor`
- `awg0` blocked by `stability_below_floor`
- `vless` blocked by `severity_SUSPECT`
- execution-only target blocked by `manual_only`, `reserve_only`, and `canary_reserved_production_assignment_blocked`
- canary-reserved target blocked by `canary_reserved_production_assignment_blocked`, `min_mbps_below_floor`, and `stability_below_floor`

## Stress Probe Method

Z4 stress testing used a live-derived copy of `/opt/v7/egress/state` on the VPS:

- stress_workspace: `/tmp/z4-stress-881sfifh`
- source_users_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- source_egress_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- production_mutation: `false`

This preserves live-runtime-first evidence while avoiding unsafe production degradation mutation.

## Post-Stress Production Verification

Collected after stress probe:

- collected_at: `2026-06-01T18:19:40.778208+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`
- candidate row unchanged: `ip=10.7.0.16 current=vless table=1014 enabled=1`

## Verdict

- live_runtime_used=true
- live_planner_used=true
- live_hashes_used=true
- selected_moves=0
- production_mutation_performed=false
- runtime_unchanged_after_stress_probe=true
- current_runtime_autonomy_ready=false

