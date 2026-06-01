# P6.A Movement Domain Model

Project: V7 Vozduh

Block: P6.A

## Movement

A movement is a bounded, approved change of one enabled user's current egress from a source channel to one destination channel, with matching route-table update and audit evidence.

P6.A movement design:

- user: `10.7.0.11`
- from: `1`
- to: `amneziawg-exec-20260528-10-8-1-14`
- table: `1009`
- target interface: `v7execwg0`
- rollback target: `1`

## Movement Scope

Scope is exactly:

- one user
- one source
- one destination
- one route table
- one forward command in future certification
- one rollback command in future certification if needed

No autoswitch apply, broad routing sync, policy apply, cohort movement, or UI execution is included.

## Movement Evidence

Required evidence:

- fresh packet
- users registry hash
- egress registry hash
- selected moves hash/count
- route table `1009` before/after
- user assignment file before/after
- route movement preview
- target readiness output
- checker outputs
- audit/switch-history records

## Movement Verification

Verification must prove:

- only `10.7.0.11` changed;
- only route table `1009` changed;
- destination interface is `v7execwg0`;
- no other users moved;
- selected moves remain zero;
- runtime checkers pass;
- hidden movers are absent.

## Movement Rollback

Rollback is a bounded switch back:

`10.7.0.11 -> 1`

Rollback verification must restore:

- users registry candidate row to `current=1`
- route table `1009` to source interface for `1`
- checker results to OK

## Movement Observation

Observation is sampled before, during, immediately after, and delayed after movement. It tracks registry hashes, route table, selected moves, checkers, switch-history, and destination occupancy.

## Verdict

- movement_domain_defined=true
- movement_scope_single_user=true
- movement_scope_single_target=true
