# E12 Scaling Governance Analysis

## Classification

scales_conditionally=true
scales_linearly=false
larger_cohort_readiness_after=CONDITIONAL_NO_GO

## Evidence

- WireGuard remains reserved and zero-user, with `hard_limit=2`.
- Current live/copy pressure can still produce selected moves outside a cohort.
- Plain clearance selected 3 moves in local rehearsal.
- E12 generation-token hardening makes nonzero budgets deterministic only when
  generation id and selected-move hash match.
- Live nonzero-budget timer rehearsal used no generation token and therefore
  failed closed with no movement.

## Scaling Risks

| Area | Scaling behavior | E12 verdict |
| --- | --- | --- |
| Target capacity | WireGuard first cohort is bounded by hard limit 2. | 3+ to WireGuard forbidden |
| Rollback complexity | Grows per moved user and per source target. | Conditional |
| Delayed movement | Controlled by generation token and budget hash, but still requires approval. | Controlled for rehearsed shape |
| Autoswitch pressure | Nonlinear because service signals and safety freezes vary by timer generation. | Larger cohort blocked |
| Planner/apply split | Safer after token hardening; still separate live recompute paths. | Controlled with token |
| Restore lifecycle | Works for two-user shape; larger cohorts need explicit budget proof. | Conditional |
| Target starvation | Still possible if healthy pool shrinks. | Monitor/blocker |
| Observability | Evidence is good for governance blocks, not yet operator-grade UX. | Productization needed |

## Larger-Cohort Decision

The core can leave the **bounded 2-user phase** only in the narrow sense that the
orchestration engine now has replay-resistant nonzero-budget primitives.

It should **not** execute a larger cohort yet because:

- no live matching-token nonzero movement is approved;
- WireGuard `hard_limit=2` forbids 3-user WireGuard cohort;
- nonzero budget can intentionally allow movement, so blast radius must be a
  separately approved cohort plan;
- restart durability and operator UX need hardening before unattended autonomy.

recommended_next_stage=operator UX/observability plus dedicated test egress or separate larger-cohort approval target
