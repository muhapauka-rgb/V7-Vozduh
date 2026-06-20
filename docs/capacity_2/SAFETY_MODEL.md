# SAFETY MODEL

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Safety Rule

Observed capacity must never immediately change assignments.

## Required Boundary

| Boundary | Rule |
| --- | --- |
| Planner | No eligibility, ranking, or selected-move influence. |
| Autoswitch | No movement, no target selection, no rebalance. |
| Governance | No new approval path. |
| Execution | No runtime action. |
| Limits | No automatic edits to `soft_limit`, `hard_limit`, or `capacity_users`. |
| UI | Advisory only until separate implementation approval. |

## Safe Maturity Stages

| Stage | Allowed behavior |
| --- | --- |
| `observe` | collect/derive evidence only |
| `learn` | summarize stable/degrading ranges |
| `recommend` | tell operator "consider reviewing limit" |
| `advisory` | show confidence and suggested next audit |
| `planner_integration_candidate` | separate future program only |

## Stop Conditions

Observed capacity must remain advisory when:

- sample count is low;
- measurements are stale;
- channel ownership is unknown;
- user traffic mix changed;
- service matrix is missing;
- runtime readiness is incomplete;
- degradation could be caused by route/service outage rather than load;
- evidence contradicts static safety rails.

## Certification Requirement

Before any future planner integration, V7 needs:

1. accepted ADR update;
2. explicit rollout governance;
3. truth/convergence gate;
4. shadow evidence with confidence;
5. rollback plan;
6. operator-visible explanation;
7. no hidden writeback to limits.

## Audit Verdict

Safe path is shadow-only now, advisory later, planner integration only after a separate governed program.
