# Program Z3 Runtime Recheck

Date: 2026-06-01

## Verdict

runtime_recheck_passed=false

## Recheck Inputs

- live users registry hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- live egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- live planner generation id: `07fc79a3931bdf39b1969699d31f69b05756805a28cdfbcb9e039bcaeba010e1`
- live capacity status: `ok`
- live selected moves from planner: `0`

## Recheck Decision

DENY

## Denial Reason

The runtime selected-move gate denied autonomous execution:

- expected budget: `1`
- planner selected moves: `0`
- planner candidate moves: `12`
- restore barrier clearance max selected moves: `0`
- guard: `restore_barrier_clearance_selected_moves_exceed_budget`

Z3 cannot safely execute movement while the live governance guard says no selected move is authorized.

## Safety

- runtime_mutation_performed=false
- users_moved=false
- routing_changed=false
- autoswitch_apply_outside_packet=false

