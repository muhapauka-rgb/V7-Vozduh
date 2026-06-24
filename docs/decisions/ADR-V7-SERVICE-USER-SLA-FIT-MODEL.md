# ADR-V7-SERVICE-USER-SLA-FIT-MODEL

Status: Accepted
Date: 2026-06-24
Commit: V7.AUTONOMOUS.ROUTING.FIT_OUTCOME_RECOVERY_FOUNDATION implementation commit

## Context

V7 previously knew channel quality, planner candidates, service matrix results, and user assignment truth, but did not expose one explicit read model answering: "for this user, with these required services and safety constraints, is this channel a fit now?"

## Decision

Service/user/SLA fit is implemented as a read-only routing foundation overlay in `admin_core/autonomy_trust_acceleration.py::build_service_user_sla_fit` and surfaced through `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`.

The model reuses existing operator decision surface rows, intelligence snapshots, required service hints, candidate rows, service freshness, capacity/policy hints, route/runtime safety hints, and current assignment. It returns `fit_score`, `fit_verdict`, `missing_requirements`, `best_channel`, `safe_alternatives`, and `reason`.

## Alternatives Considered

- Add a new planner: rejected.
- Change channel score formula: rejected.
- Let UI labels imply fit without a contract: rejected.

## Consequences

The fit model can inform future planner/input certification, but it has no action authority. It does not move users, change formulas, create storage, create snapshots, or bypass governance.

## Affected Modules

- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tests/unit/test_autonomy_trust_acceleration.py`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`
- `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`

## Related Reports

- `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md`
