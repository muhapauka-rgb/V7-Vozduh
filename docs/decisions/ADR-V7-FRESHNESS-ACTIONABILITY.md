# ADR-V7-FRESHNESS-ACTIONABILITY

Status: Accepted
Date: 2026-06-24
Commit: V7.AUTONOMOUS.ROUTING.FIT_OUTCOME_RECOVERY_FOUNDATION implementation commit

## Context

V7 has snapshot freshness contracts, but future routing decisions need an explicit read-only answer: is this evidence actionable now, stale and requiring recheck, diagnostic-only, history-only, or unknown?

## Decision

Freshness actionability is implemented in `admin_core/autonomy_trust_acceleration.py::build_freshness_actionability` and surfaced through `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`.

The model classifies service, quality, route, capacity, prediction, suitability, and recovery evidence as:

- `ACTIONABLE_NOW`
- `STALE_RECHECK_REQUIRED`
- `DIAGNOSTIC_ONLY`
- `HISTORY_ONLY`
- `UNKNOWN`

## Alternatives Considered

- Treat all non-missing evidence as usable: rejected.
- Build a new evidence index now: rejected.
- Change planner/trust formulas based on freshness immediately: rejected.

## Consequences

Stale or missing evidence is explicit and can block readiness, but the classification is read-only. Long-term evidence index work remains deferred until production autonomy certification or proven scale pressure.

## Affected Modules

- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `tests/unit/test_autonomy_trust_acceleration.py`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`

## Related Reports

- `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md`
