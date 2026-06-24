# ADR-V7-RECOVERY-ADMISSION-ANTI-FLAP

Status: Accepted
Date: 2026-06-24
Commit: V7.AUTONOMOUS.ROUTING.FIT_OUTCOME_RECOVERY_FOUNDATION implementation commit

## Context

V7 already has trust evolution, recovery lifecycle evidence, audit records, and governed movement records. The missing contract was explicit: a channel must not jump from bad to fully trusted after one PASS, and users must not oscillate between channels because recommendations change too quickly.

## Decision

Recovery admission and anti-flapping are implemented as read-only routing foundation overlays:

- `build_recovery_admission`
- `build_anti_flapping`

Recovery admission exposes `QUARANTINED`, `PROBING`, `LIMITED_RECOVERY`, `RECOVERED_WATCH`, `ELIGIBLE`, and `BLOCKED` as admission states. Anti-flap exposes cooldown, minimum observation window, hysteresis requirement, rapid reverse movement detection, and read-only blocker reasons.

## Alternatives Considered

- Trust a single successful check: rejected.
- Add a new recovery planner: rejected.
- Hide anti-flap behind operator memory or reports: rejected.

## Consequences

Recovery and anti-flap are visible before autonomous routing escalation, but they do not change trust scores, planner selection, execution, governance, formulas, floors, storage, snapshots, or runtime state.

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
