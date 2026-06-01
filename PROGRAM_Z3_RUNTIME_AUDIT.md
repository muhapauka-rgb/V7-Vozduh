# Program Z3 Runtime Audit

Date: 2026-06-01

## Verdict

runtime_audit_complete=true
runtime_recheck_passed=false

## Runtime Hashes

- users registry hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- planner generation id: `07fc79a3931bdf39b1969699d31f69b05756805a28cdfbcb9e039bcaeba010e1`

## Health And Capacity

- capacity status: `ok`
- active users: `18`
- healthy channels: `2`
- degraded or dead channels: `5`
- all live per-egress capacity rows reported `OK`

## Candidate State

Fresh live planner found 12 switch candidates.

Representative candidate:

- user: `10.7.0.16`
- current egress: `vless`
- recommended egress: `awg3`
- move type: `failover`
- current score: `0.0`
- recommended score: `2045.51`
- reason: `current_egress_not_eligible`
- rollback target: `vless`

## Target State

Recommended target:

- target: `awg3`
- role: `GLOBAL_STABLE`
- diagnose: `OK`
- current users: `3`
- capacity status: `OK`

## Runtime Blocker

The planner selected no movement:

- candidate moves: `12`
- selected moves: `0`
- guard reason: `restore_barrier_clearance_selected_moves_exceed_budget`
- barrier clearance max selected moves: `0`

## Safety

- runtime_mutation_performed=false
- users_moved=false
- routing_changed=false
- autoswitch_apply_outside_packet=false

