# ADR-AUTONOMY-TRUST-SUFFICIENCY-TIER-AWARE

Status: Accepted  
Date: 2026-06-24  
Commit: `d4ee291be875b825fb883d835621c8530c8eda8c`  

## Context

V7 has certified evidence through `AUTONOMY_TIER1_GOVERNED_CANARY_READINESS_REPORT.md`.

Current facts:

- Prediction matches: `21/21`.
- Candidate outcomes: `84/156`.
- Missing candidate outcomes: `72`.
- Blast confidence: `100.0`.
- Rollback confidence: `100.0`.
- Capture/visibility/aggregation loss: `0`.
- Current state: `TIER_1 MARGINAL_OPERATOR_REVIEW`, `TIER_2+ NO_GO`.
- Autonomous one-user canary: `NO_GO`.

The user question was whether V7 requires more evidence than necessary for the current risk tier.

## Decision

Trust sufficiency is tier-aware.

`Sufficient trust` means enough trust for a specific tier and authority boundary:

- `TIER_0`: read-only preview may be available without movement authority.
- `TIER_1`: first one-user governed canary may be `MARGINAL_OPERATOR_REVIEW` when non-negotiable gates are clean, even when confidence/trust/prediction floors are below `70`.
- `TIER_2`: governed canary requires hard governed floors.
- `TIER_3+`: autonomous tiers require hard autonomous/bounded/production floors and future explicit autonomy authorization.

The current trust model verdict is `TRUST_MODEL_MIXED`:

- Correct and safe for blocking autonomous canary and production autonomy.
- Correct for allowing TIER_1 review semantics rather than pretending the system is fully ready.
- Incomplete in communication because `70/70/70` can be misunderstood as a universal threshold instead of a tier-specific progression boundary.

No floor, formula, planner, governance, execution, truth source, daemon, autoswitch, runtime apply, synthetic evidence, or user movement changed.

## Alternatives Considered

1. Lower the `70/70/70` floors.
   - Rejected. No certified evidence proves autonomous tiers are safe with lower floors.

2. Treat `21/21` prediction matches as enough for canary GO.
   - Rejected. Prediction accuracy is strong, but source confidence is low and suitability remains incomplete.

3. Treat blast and rollback `100` as enough for autonomy.
   - Rejected. They make small governed action safer; they do not prove prediction, service, or suitability quality.

4. Require full floors before even preparing TIER_1 review.
   - Rejected. Current code already supports `TIER_1 MARGINAL_OPERATOR_REVIEW`, and mature progressive-delivery systems allow small reviewed canaries before broad automation.

## Consequences

- Future reports must state the tier when saying trust is sufficient or insufficient.
- `TIER_1 MARGINAL_OPERATOR_REVIEW` must not be described as `AUTONOMY_CANARY_GO`.
- TIER_2+ remains blocked until current hard floors pass.
- The next safe phase is a separate operator-approved TIER_1 apply decision for the exact validated packet, or an operator rejection returning to candidate review.

## Affected Modules

- `admin_core/operator_execution_pipeline.py`
- `admin_core/autonomy_trust_acceleration.py`
- `admin_core/intelligence_platform.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tools/v7-users-autoswitch`
- `tools/v7-operator-execution-packet`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`

## Related Reports

- `docs/reports/AUTONOMY_TIER1_GOVERNED_CANARY_READINESS_REPORT.md`
- `docs/reports/AUTONOMY_FLOOR_SEMANTICS_AND_RISK_TIER_REVIEW_REPORT.md`
- `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`
- `docs/reports/AUTONOMY_TRUST_SUFFICIENCY_MODEL_REPORT.md`
