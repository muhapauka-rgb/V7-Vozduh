# ADR-AUTONOMY-EVIDENCE-SATURATION

Status: Accepted  
Date: 2026-06-24  
Commit: `55ad5436f50ce0563b26a990d5c5ad175dcfdfa7`  

## Context

V7 has certified:

- prediction matches `21/21`;
- candidate outcomes `84/156`;
- missing candidate outcomes `72`;
- blast confidence `100`;
- rollback confidence `100`;
- capture/visibility/aggregation loss `0`;
- current state `TIER_1 MARGINAL_OPERATOR_REVIEW`;
- `TIER_2+ NO_GO`.

The open question is whether V7 can ever know that it has enough evidence, or whether it can demand new evidence forever.

## Decision

Evidence saturation is tier-aware and component-specific.

V7 must treat evidence as saturated for a given tier only when:

1. Required non-negotiable safety gates are clean.
2. The component's confidence has crossed the tier floor, or additional same-source evidence would not change the tier decision.
3. The evidence is real, current enough for its type, and source-owned by existing V7 owners.
4. The conclusion is tied to a specific tier and authority boundary.

Current verdict: `SATURATION_MODEL_PARTIAL`.

V7 already has indirect saturation behavior through:

- `0..100` score clamps;
- risk tier floors;
- finite candidate outcome coverage;
- canary proximity projections;
- source-confidence attribution;
- truth/convergence gates.

V7 did not previously have an explicit project-level saturation rule. This ADR supplies that rule without changing code, floors, formulas, planner, governance, execution, truth source, runtime apply, daemon, autoswitch, synthetic evidence, or user movement.

## Alternatives Considered

1. Treat any fixed evidence count as saturation.
   - Rejected. Quantity without quality can converge below floor.

2. Treat perfect prediction matches as global saturation.
   - Rejected. Prediction source confidence and suitability evidence still matter.

3. Treat blast and rollback `100` as global saturation.
   - Rejected. Safety evidence does not substitute for prediction/service/suitability correctness.

4. Add new formula or lower floors.
   - Rejected. No certified code gap justifies formula or floor changes.

## Consequences

- Future autonomy phases must not ask for generic "more evidence".
- They must name the unsaturated component, the target tier, the current value, the floor, and what kind of real evidence can change the decision.
- `TIER_1 MARGINAL_OPERATOR_REVIEW` remains reachable now.
- `TIER_2+` remains blocked until component quality and floors pass.
- Synthetic evidence remains forbidden.

## Affected Modules

- `admin_core/intelligence_platform.py`
- `admin_core/autonomy_trust_acceleration.py`
- `admin_core/operator_execution_pipeline.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tools/v7-users-autoswitch`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`

## Related Reports

- `docs/reports/AUTONOMY_TRUST_SUFFICIENCY_MODEL_REPORT.md`
- `docs/reports/AUTONOMY_EVIDENCE_SATURATION_MODEL_REPORT.md`
- `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`
- `docs/reports/AUTONOMY_SOURCE_CONFIDENCE_REALITY_AUDIT_REPORT.md`
