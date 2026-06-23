# ADR-OBSERVED-OUTCOME-PRIMARY-TRUST

Status: Accepted

Date: 2026-06-23

Commit: this ADR commit

## Context

V7 previously treated operator comparison as a major trust-growth path because the existing `/api/actions/shadow-autonomy-compare` endpoint and shadow comparison store can produce agreement rate and earned confidence.

That path is technically valid, durable, and useful, but the operator does not directly observe real service quality for all users across the city. For many user/channel recommendations, forcing the operator to review many decisions would create blind training history rather than reliable autonomy evidence.

Existing evidence already proves that the stronger trust signal is observed network outcome:

- service and channel quality observations;
- forecast-to-actual matching;
- post-action verification;
- rollback/no-rollback result;
- blast-radius safety;
- governed feedback and learning;
- future client telemetry when implemented.

## Decision

Observed network outcome is the primary autonomy trust source for V7.

Operator comparison is secondary supervised confirmation. It is valid only when the operator has enough operational context to judge the recommendation. It must not be required as blind bulk training data.

Manual operator action is authoritative for the system state, but it is not synthetic agreement with V7's autonomous recommendation. The system should respect the action, observe the resulting network outcome, and use that outcome through existing evidence owners.

## Alternatives considered

1. Keep operator comparison as primary trust source.
   - Rejected because it pressures the operator to judge outcomes they cannot truthfully observe.

2. Remove operator comparison.
   - Rejected because operator agreement, disagreement, and override are still valuable supervised/contextual evidence.

3. Lower trust floors or change formulas to compensate.
   - Rejected because that would weaken safety and manufacture readiness without real outcome evidence.

## Consequences

- Readiness language must prioritize observed outcome evidence.
- Operator review batches may remain visible, but only as secondary supervised confirmation.
- Blind operator training history is forbidden.
- Canary readiness must still block when observed outcome confidence, trust, or prediction confidence is insufficient.
- Existing comparison endpoint and store remain valid; no new storage or truth source is created.

## Affected modules

- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `admin_core/shadow_autonomy.py`
- `admin_core/intelligence_workers.py`
- `admin_core/intelligence_platform.py`
- `admin_core/operator_execution_feedback.py`
- `admin_core/operator_execution_pipeline.py`

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_PROJECT_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`

## Related reports

- `docs/reports/AUTONOMY_TRUST_SOURCE_REALITY_1_REPORT.md`
- `docs/reports/AUTONOMY_TRUST_ACCELERATION_1_REPORT.md`
- `docs/reports/OPERATOR_COMPARISON_COLLECTION_1_REPORT.md`
- `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_2_REPORT.md`
- `docs/reports/AUTONOMY_TRUST_DURABILITY_1_REPORT.md`
- `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`
- `docs/reports/POOL.3_RUNTIME_DISCOVER.md`
