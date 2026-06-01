# PROGRAM Z3.2 Autonomous Execution

## Scope

Execute one bounded autonomous move:

- user: `10.7.0.16`
- from: `vless`
- to: `awg3`
- budget: `1`
- route_class: `GLOBAL_STABLE`

## Commands Used

The live runtime path used:

- filtered dry-run: `v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE --user 10.7.0.16 --target-egress awg3`
- generation-bound clearance packet in `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- filtered apply: `v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE --user 10.7.0.16 --target-egress awg3 --apply`

No bulk apply was used.

## Runtime Recheck

- pre_generation_id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- pre_selected_hash: `f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- recheck guard: `restore_barrier_clearance_budget_and_generation_ok`
- recheck selected_moves: `1`

## Execution Result

- apply_rc: `0`
- applied: `true`
- candidate_moves: `1`
- selected_moves: `1`
- moved: `10.7.0.16 vless -> awg3`
- verify_rc: `0`
- route_check: `V7_USER_ROUTE_CHECK=OK`

## After Observation

- user row: `ip=10.7.0.16 current=awg3 table=1014 enabled=1`
- users_registry_hash: `40c342ee47d7ed20db44939686f8732a2423a023fb68610140edbf0854733f70`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`

## Verdict

- autonomous_execution_successful=true
- autonomous_budget=1
- scope_expanded=false
- autoswitch_apply_outside_packet=false

