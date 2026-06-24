# ADR-AUTONOMY-RISK-TIERED-FLOORS

Status: Accepted
Date: 2026-06-24
Commit: PENDING

## Context

V7 had one operator-visible canary floor family in `admin_core/operator_execution_pipeline.py`: confidence `70.0`, trust `70.0`, and prediction confidence `70.0`. That floor correctly blocks operator-free bounded autonomy today, because current production evidence is still below floor: confidence `38.872`, trust `54.154`, prediction confidence `35.385`, and candidate outcomes are `84/156` with `72` outcomes that have not happened yet.

The ambiguity was semantic: the same `70/70/70` wording was being read as the floor for every risk tier, including the first one-user governed canary review. That made V7 look like it required production-grade confidence before any supervised one-user canary could even be reasoned about.

## Decision

V7 will expose a tiered autonomy floor model without lowering any hard autonomy floor.

The accepted tiers are:

| Tier | Meaning | Status Semantics |
| --- | --- | --- |
| TIER_0 | Read-only preview | No apply, no movement |
| TIER_1 | First one-user governed canary review | May be `MARGINAL_OPERATOR_REVIEW` when only confidence floors fail; still requires existing packet, restore barrier, operator approval, and explicit existing runtime apply |
| TIER_2 | Governed canary | Requires `70/70/70` hard governed review floor |
| TIER_3 | Bounded autonomous one-user canary | Requires existing `70/70/70` hard autonomy floor and future explicit autonomy authority |
| TIER_4 | Bounded autonomous small batch | Requires `85/85/85` |
| TIER_5 | Batch autonomy | Requires `90/90/90` |
| TIER_6 | Production autonomy | Requires `95/95/95` and is not granted by the current program |

Non-negotiable gates remain absolute for every movement tier: candidate exists, packet valid, rollback target known, restore barrier available before apply, snapshot gate clean, no hard service/capacity blocker, and existing runtime owner only.

## Alternatives Considered

1. Keep one floor model for all tiers.
   Rejected because it hides the difference between supervised first-canary review and operator-free autonomy.

2. Lower the existing canary floor below `70`.
   Rejected because current evidence does not justify weakening autonomous safety gates.

3. Create a new planner/governance/execution path for canary tiers.
   Rejected because V7 must reuse existing planner, packet, restore barrier, execution, feedback, learning, truth, and convergence owners.

## Consequences

- `70/70/70` remains the hard gate for autonomous canary readiness.
- Under-floor current production state can now be described honestly as `TIER_1 MARGINAL_OPERATOR_REVIEW`, not `AUTONOMY_CANARY_GO`.
- `canary_autonomy_ready` remains false while hard floor blockers exist.
- Runtime apply, user movement, daemon enablement, thresholds, formulas, planner, governance, and execution paths are unchanged.

## Affected Modules

- `admin_core/operator_execution_pipeline.py`
- `admin_core/autonomy_trust_acceleration.py`
- `tests/unit/test_operator_execution_pipeline.py`
- `tests/unit/test_autonomy_trust_acceleration.py`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`

## Reference Updates

Canonical reference now includes `AUTONOMY_RISK_TIERED_FLOOR_MODEL`.

## Related Reports

- `docs/reports/AUTONOMY_FLOOR_SEMANTICS_AND_RISK_TIER_REVIEW_REPORT.md`
- `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`
- `docs/reports/AUTONOMY_CANARY_1D_CONFIDENCE_TRUST_PREDICTION_FLOOR_CLOSURE_REPORT.md`
- `docs/reports/AUTONOMY_CANARY_1C_RESTORE_BARRIER_LIFECYCLE_AND_NEXT_BLOCKER_REPORT.md`
