# P4.A First Action Candidate Review

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Candidate Actions Reviewed

| Candidate | Safety | Observability | Reversibility | Decision |
| --- | --- | --- | --- | --- |
| Single-user move | Higher risk: user and route blast radius | Observable but user-affecting | Rollback needed | Reject as first action |
| Single-user rollback | Requires a prior forward action | Observable | Risk depends on prior state | Reject as first action |
| Single-user trust action | Could write trust/routing policy state | Observable | Risk of truth-source confusion | Reject as first action |
| Single-user approval flow | Mostly governance, but may imply movement | Observable | Packet expiry/reject only | Defer |
| Zero-movement governance state transition | Smallest runtime governance mutation, no user movement, no routing | Fully auditable | Compensating append-only reversal marker | Select |

## Selected First Action

`ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`

## Exact Meaning

The first real runtime action V7 should ever perform is an append-only governed runtime marker that records that a fully approved, fully rechecked, zero-movement action passed the control plane.

It must:

- move zero users
- change zero routes
- apply zero autoswitch plans
- execute zero rollback commands
- change zero systemd/deploy state
- write only a scoped governance/audit action record in the later authorized block

## Why This Is The First Action

It tests the hardest governance requirements without user blast radius:

- dual approval
- packet expiry
- runtime recheck
- hash matching
- replay denial
- audit lineage
- observation
- abort behavior
- compensating record model

## Verdict

`first_action_candidate_defined=true`

