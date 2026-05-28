# E11.11 Mini-Cohort Readiness

mini_cohort_readiness=CONDITIONAL

## Verdict

The system is ready to plan a mini-cohort, but not to execute one in E11.11.

Classification: `MINI_COHORT_CONDITIONAL`

## Capacity And Movement Budget

| Item | Current state | Mini-cohort implication |
|---|---|---|
| Candidate target | `wireguard-1779454504-c43409` clean and reserved | Suitable only under explicit cohort approval |
| Target users | `0` | Clean starting point |
| Target configured limit | `soft_limit=1 hard_limit=2` | Safe cohort budget is `2`, not `3`, unless capacity is separately expanded |
| Current production distribution | `8` on `awg0`, `8` on target `1`, disabled `vless` row remains | Baseline is stable but crowded on active production channels |
| Selected moves | `0` | No background autoswitch pressure currently |
| Restore-settle | `GO` | Restore governance is usable |

## Risk Analysis

| Risk | Level | Evidence | Mitigation |
|---|---|---|---|
| Rollback complexity | Medium | One-user rollback proven; N-user rollback not yet exercised | Use exact N-user manifest and rollback manifest |
| Capacity overload | Medium | WireGuard hard limit is `2` | Limit first mini-cohort to two users |
| Target starvation | Low | WireGuard zero-user and quality OK | Keep reservation; do not production-assign |
| Autoswitch churn | Low now, medium during cohort | `selected_moves=0`, but history has frozen users and prior churn | Hold planner/apply during movement; delayed monitoring after restore |
| Delayed movement | Medium | E9.4 had delayed movement; E11.10 clean | Keep restore-settle and delayed monitoring mandatory |
| Historical/live evidence confusion | Low after E11.11 fix | Defaults now prefer E11.11 state | Keep explicit state-dir in reports anyway |

## Blocking Conditions Before Execution

- A separate E11.12 approval packet must name exact 2 users, forward target, rollback targets, and timers to hold.
- No `3`-user cohort unless WireGuard hard limit/capacity is explicitly changed and verified.
- Fresh live checkers must be OK immediately before execution.
- Fresh selected moves must be zero immediately before hold.
- Execution must remain `execution_allowed_now=false` in E11.11.

recommended_next_block=E11.12_TWO_USER_MINI_COHORT_APPROVAL_PACKET
