# Block E Operator Proposal

Date: 2026-06-01
Status: STOP_GATE_1_PENDING_OPERATOR_APPROVAL

## Bounded Proposal

- budget: `1`
- raw candidates: `12`
- held candidates: `10`
- eligible candidates: `2`
- proposal count: `1`
- ready for operator review: `true`

## Exact Candidate

- user: `10.7.0.16`
- current egress: `vless`
- target egress: `awg3`
- target interface: `awg3`
- table: `1014`
- move type: `failover`
- route class: `GLOBAL_STABLE`
- reason: `current_egress_not_eligible`
- recommended score: `1966.98`

## Exact Rollback

Rollback command if execution is approved and post-checks fail:

`v7-user-switch 10.7.0.16 vless`

## Exact Observation Plan

Before:

- capture users registry hash
- capture egress registry hash
- run `v7-killswitch-check`
- run `v7-user-route-check`
- confirm `10.7.0.16 current=vless`

After:

- verify `10.7.0.16 current=awg3`
- verify table `1014` default dev `awg3`
- run `v7-killswitch-check`
- run `v7-user-route-check`

Delayed:

- repeat route/user check
- repeat registry hash capture
- confirm outside users unchanged

Final:

- certify one-user scope
- certify rollback readiness
- certify no outside routing drift

## Stop Gate 1

Proposal valid: true

Capacity valid: true

Trust valid for one-user bounded movement: true with wider-autonomy blockers noted

Target readiness valid: true

Rollback ready: true

Execution is not approved yet.

Required approval text:

`APPROVE BLOCK E STAGE 2: move 10.7.0.16 from vless to awg3 with budget=1 and rollback=v7-user-switch 10.7.0.16 vless`

