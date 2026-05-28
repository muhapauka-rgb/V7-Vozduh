# E11.18 Promotion-Clean Matrix

## Classification

classification=TWO_USER_PROMOTION_CLEAN
scope=exact_two_user_bounded_lifecycle_only
larger_cohort_blocked=true
execution_allowed_now=false

| Control | Proven | Bounded | Reproducible | Remaining Risk | Larger Cohort Relevance | Operational Maturity |
|---|---:|---:|---:|---|---|---|
| planner/apply split | yes | yes | yes | apply recomputes fresh state | larger cohorts amplify fresh recompute | production-grade bounded |
| restore barrier | yes | yes | yes | barrier metadata must be present | required for any cohort | production-grade bounded |
| generation clearance | yes | conditional | yes | no immutable generation token | nonzero budgets need stronger proof | conditional |
| selected-move budget | yes | yes | yes | budget is count-based | larger cohorts need budget semantics | promotion-clean for 2 users |
| delayed movement protection | yes | yes | yes | pressure can recur but selected moves are blocked | core larger-cohort blocker | promotion-clean for 2 users |
| reservation enforcement | yes | yes | yes | manual bypass always requires governance | prevents WireGuard production leak | production-grade bounded |
| rollback discipline | yes | yes | yes | simultaneous rollback grows with cohort size | 3+ increases complexity | proven for 2 users |
| target readiness | yes | yes | yes | readiness is time-sensitive | must refresh per block | mature with fresh gates |
| restore-settle | yes | yes | yes | insufficient alone without barrier/clearance | larger cohorts need longer settle | mature as one gate |
| apply restore | yes | conditional | yes | unsafe without barrier and budget | main scaling risk | bounded only |
| hidden mover protection | yes | yes | yes | requires repeated process scans | larger blast radius if missed | mature gate |
| WireGuard target integrity | yes | yes | yes | hard cap 2 | 3-user cohort forbidden | production-grade bounded |
| runtime tooling consistency | yes | conditional | yes | runtime/repo lineage partial | larger cohorts need convergence | acceptable for 2 users |
| governance checker coverage | yes | yes | yes | lineages still partial | must evolve per block | current coverage OK |

## Decision

two_user_promotion_clean=true
generation_governance_complete=true_for_bounded_two_user_lifecycle
delayed_movement_protection_complete=true_for_bounded_two_user_lifecycle
larger_cohort_blocked=true
operational_maturity_status=TWO_USER_PROMOTION_CLEAN_LARGER_COHORT_BLOCKED
