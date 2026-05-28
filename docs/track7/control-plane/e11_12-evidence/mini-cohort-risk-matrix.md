# E11.12 Mini-Cohort Risk Matrix

risk_matrix_completed=true
execution_allowed_now=false

| Risk | Evidence | Verdict | Control |
| --- | --- | --- | --- |
| Target capacity overflow | WireGuard `users=0`, `soft_limit=1`, `hard_limit=2`; selected cohort size is exactly 2 | NO for selected packet; YES if third user added | Hard cap two users; three-user cohort forbidden |
| Delayed autoswitch movement | Restore-settle samples: selected moves `[0,0,0]`, registry stable, hidden movers false | NO observed | Repeat gate before execution and after restore |
| Planner/apply races | Planner dry-run selected moves `0`; no apply executed | LOW residual | Hold planner/apply before future execution |
| Reservation enforcement gap | Reserved target still production-blocked; target readiness uses explicit governed path | NO current gap | Future movement only by manifest |
| Rollback complexity | Both candidates rollback to current target `1` and current route tables are sane | MEDIUM | Stagger movement; rollback one user at a time |
| Restore-settle stability | Gate status `GO`, 3 samples across 4.45 apply timer intervals | YES stable | Gate remains mandatory |
| Mini-cohort starvation | Candidates have `switches_1h=0`; target has capacity exactly 2 | LOW | Keep cohort at 2 max |
| Target overload | Two users reaches hard limit, not above it | CONDITIONAL | Abort if WireGuard count is not zero before start |
| Hidden rebalance | Hidden movers observed false; selected moves zero | NO observed | Hidden process scan in every sample |
| Target readiness regression | Fresh readiness for both candidates is `GO` | NO observed | Re-run immediately before execution |
| WireGuard stability under 2-user load | Quality is adequate for zero-user readiness; no real two-user load test performed in E11.12 | CONDITIONAL | First execution must be capped and observable |
| Simultaneous rollback risk | Both rollback to target `1`; target already carries production load | MEDIUM | Roll back sequentially, verify after each user |
| Partial rollback edge case | Preview defines per-user rollback commands and stop rules | CONTROLLED | No second movement after first rollback failure |
| Staged restore edge case | Existing runbook requires planner restore, settle gate, then apply restore | CONTROLLED | No manual apply |
| Delayed monitoring blind spot | Samples include selected moves, hashes, checkers, hidden movers | NO current blind spot | Keep 3-sample minimum |
| Cohort blast radius | Exactly two named users | BOUNDED | No other user movement allowed |
| Autoswitch churn | Recent runtime drift moved other users before final packet; final samples stable | CONDITIONAL | Fresh pre-check must bind final hash |
| Capacity competition with production | Reserved target has zero users and production assignment blocked | LOW | Reservation enforcement remains mandatory |
| Restore timing overlap | Apply restore only after settle `GO` | CONTROLLED | Observe across multiple timer intervals |
| Target saturation edge case | Second user reaches hard limit | CONDITIONAL | Third user forbidden; abort on any unexpected WireGuard user |

mini_cohort_risk_verdict=CONDITIONAL_GO_FOR_APPROVAL_PACKET_ONLY

The residual risk is not uncontrolled chaos; it is bounded capacity saturation
at exactly two users plus the need for a future fresh pre-check because runtime
drift occurred during E11.12 evidence collection.
