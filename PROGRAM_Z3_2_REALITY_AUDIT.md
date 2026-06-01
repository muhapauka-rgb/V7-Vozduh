# PROGRAM Z3.2 Reality Audit

Program: Z3.2 Autonomy Stress And Governance Certification

Mode: live runtime, bounded autonomous execution, stress certification.

## Current Branch

- branch: `v7-next`

## Live Runtime Snapshot

Pre-execution runtime snapshot:

- collected_at: `2026-06-01T17:57:11.920504+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- candidate row: `ip=10.7.0.16 current=vless table=1014 enabled=1`
- initial barrier condition: stale Z3.1 generation, generation mismatch

Live autonomous movement snapshot:

- user: `10.7.0.16`
- from: `vless`
- to: `awg3`
- budget: `1`
- selected_moves: `1`
- users_total: `18`
- healthy_egress_total: `2`
- planner guard: `restore_barrier_clearance_budget_and_generation_ok`
- pre_generation_id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- pre_selected_hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`

Post-move snapshot:

- collected_at: `2026-06-01T17:58:28.439309+00:00`
- users_registry_hash: `40c342ee47d7ed20db44939686f8732a2423a023fb68610140edbf0854733f70`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- route_check: `OK`
- candidate row: `ip=10.7.0.16 current=awg3 table=1014 enabled=1`

Post-rollback final snapshot:

- collected_at: `2026-06-01T17:59:57.857017+00:00`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`
- row: `ip=10.7.0.16 current=vless table=1014 enabled=1`
- row: `ip=10.7.0.17 current=vless table=1015 enabled=1`

## Health, Capacity, Trust

Target `awg3` was healthy at execution time:

- users_before: `3`
- avg_mbps: `71.83`
- min_mbps: `55.03`
- stability: `0.766`
- telegram: `OK`
- load class: acceptable for one bounded move

No artificial capacity, health, or trust degradation was injected into production runtime during Z3.2.

## Reality Classification

- live_users_registry_used=true
- live_egress_registry_used=true
- live_planner_used=true
- live_hashes_used=true
- live_movement_performed=true
- live_rollback_performed=true
- runtime_restored_to_pre_move_user_hash=true
- egress_registry_unchanged=true
- scope_expanded=false
- autonomous_budget=1

