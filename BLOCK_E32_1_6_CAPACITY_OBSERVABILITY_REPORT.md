# BLOCK E32.1.6 Capacity Observability Report

e32_1_6_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_observability_model_defined=true
operator_questions_defined=true
capacity_dashboard_defined=true
status_visibility_defined=true
confidence_visibility_defined=true
certification_history_defined=true
alert_model_defined=true
production_pool_compatible=true

## Summary

E32.1.6 defines how operators observe capacity. The model separates capacity health, certification, confidence, current eligibility, evidence, and next safe action so operators do not mistake a certified class for unconditional execution authority.

## Operator View

Operators must see:

- target id and role;
- capacity class;
- capacity status;
- capacity confidence;
- certified capacity;
- hard limit;
- active policy cap;
- effective batch cap;
- available capacity;
- target users count;
- reserved capacity;
- validation age;
- stale and expiration times;
- readiness, restore-settle, and runtime checker status;
- allowed actions;
- blocked action reasons.

## Dashboard Sections

- Target Summary
- Capacity Summary
- Certification Summary
- Validation Summary
- Risk Summary

## Status Visibility

Runtime status display:

- `CERTIFIED`: eligible only if execution-time recheck passes.
- `STALE`: historical certification exists; refresh required.
- `DEGRADED`: forward movement blocked; diagnose/remediate.
- `EXPIRED`: full recertification required.
- `REVOKED`: incident review required.
- `CANDIDATE`: preparation only.
- `VALIDATING`: evidence collection in progress.
- `UNKNOWN`: inspect/discover before use.

## Confidence Visibility

Confidence levels:

- `LOW`: static or incomplete evidence.
- `MEDIUM`: target-local plus long-window validation.
- `HIGH`: governed execution plus rollback, replay, delayed monitoring, and audit proof.
- `VERY_HIGH`: repeated success plus production-pool controls.

Current target:

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
capacity_status=CERTIFIED
capacity_confidence=HIGH
```

## Alerts

Required alerts:

- `CAPACITY_STALE`
- `CAPACITY_DEGRADED`
- `CAPACITY_EXPIRED`
- `CONFIDENCE_DROP`
- `RECERTIFICATION_FAILED`

Each alert must show what changed, what is blocked, what remains allowed, and the next safe action.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- capacity_dashboard_authoritative_source
```

Recommendation:

```text
Use generated capacity view model now; move to policy-engine API after policy engine exists.
```

## Remaining Open Questions

- exact dashboard schema;
- whether status color semantics should be CLI-compatible or UI-specific;
- generated view model storage location;
- alert retention period;
- production-pool aggregate capacity display;
- operator drill-down depth for evidence links.

recommended_next_block=E32_1_7_CAPACITY_FAILURE_MODES

## Evidence Files

- `docs/track7/productization/e32_1_6-evidence/operator-questions-review.md`
- `docs/track7/productization/e32_1_6-evidence/capacity-dashboard-model.md`
- `docs/track7/productization/e32_1_6-evidence/status-visibility-model.md`
- `docs/track7/productization/e32_1_6-evidence/confidence-visibility-model.md`
- `docs/track7/productization/e32_1_6-evidence/certification-history-model.md`
- `docs/track7/productization/e32_1_6-evidence/alert-model.md`
- `docs/track7/productization/e32_1_6-evidence/production-pool-compatibility.md`
- `docs/track7/productization/e32_1_6-evidence/final-model-decision.md`
- `docs/track7/productization/e32_1_6-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

