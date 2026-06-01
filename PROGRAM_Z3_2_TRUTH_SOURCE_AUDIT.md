# PROGRAM Z3.2 Truth Source Audit

## Truth Source Matrix

| Domain | Truth source | Evidence |
| --- | --- | --- |
| Proposal | live `v7-users-autoswitch` filtered dry-run | selected move count, generation id, selected hash |
| Approval | Z2 hybrid approval contract plus Z3.2 generation-bound runtime clearance | policy budget `1`, user filter, target filter, generation match |
| Movement | live `v7-users-autoswitch --apply` | candidate row changed from `vless` to `awg3` |
| Rollback | live `v7-user-switch 10.7.0.16 vless` | candidate row restored to `vless` |
| Verification | live route, reconcile, killswitch checks | final rc values all `0` |
| Observation | live users and egress registry hashes | users hash returned to pre-move value; egress hash unchanged |

## Dominance Rules

Runtime state overrides report assumptions.

Fresh planner output overrides historical proposal records.

Generation-bound clearance overrides stale barrier state only for the exact filtered user and exact budget.

Rollback verification is complete only when registry state and route checks agree.

## Clean Truth Sources

- proposal_truth_live=true
- approval_truth_generation_bound=true
- movement_truth_live=true
- rollback_truth_live=true
- observation_truth_live=true
- stale_report_used_as_runtime_truth=false

## Residual Gaps

Capacity, health, and trust degradation were not injected live. Their truth source remains baseline live eligibility plus existing unit-level fail-closed tests, not production degradation evidence.

