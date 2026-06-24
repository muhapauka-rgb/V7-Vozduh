# ADR-V7-IDEAL-AUTONOMOUS-ROUTING-MODEL

Status: Accepted  
Date: 2026-06-24  
Commit: `61088d7a9fa48cc593a5cf2b681f520e8734b59d`

## Context

V7 has accumulated many certified reports and current truths:

- the canonical planner already exists;
- Channel Decision V7 is planner-first;
- governed execution, restore barrier, rollback, feedback, learning, trust, prediction, and event-consumer read-only owners already exist;
- production autonomy is blocked by evidence quality/floors and authority, not by missing a planner;
- evidence saturation is partial and tier/component-specific.

The project needed a target model for "what V7 is supposed to become" so future work stops circling around individual evidence blockers without a system destination.

## Decision

V7's ideal target is an event-driven autonomous routing control plane for `10,000+` users and `100+` channels.

The ideal system reconciles:

```text
desired user/service/channel policy state
  -> observed network/user/channel reality
  -> bounded plan
  -> certified action or explicit stop
  -> verification
  -> rollback if needed
  -> learning
```

The ideal model is documented in:

`docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`

Stable decisions:

1. V7 must remain event-driven, not timer-movement-driven.
2. V7 must not create a second planner, governance path, execution path, trust source, or truth source.
3. Routing decisions require service/user/channel fit, not channel score alone.
4. Evidence must mature from raw observation to autonomy-grade knowledge before it can drive autonomous movement.
5. Scale to `10,000+` users requires knowledge quality, freshness/decay, aggregated read models, channel/service/user cohorts, and anti-flapping/recovery admission.
6. Runtime authority remains tiered and must pass existing gates before any autonomous apply.

## Alternatives Considered

1. Continue with evidence/trust phases only.
   - Rejected. It risks optimizing local blockers without a stable target system.

2. Create a new planner or autonomy controller now.
   - Rejected. Existing owners are already present and must be reused.

3. Treat the current channel score as the routing system.
   - Rejected. Score is diagnostic; decision is planner/governance truth.

4. Treat more rows as enough data.
   - Rejected. Knowledge quality, freshness, correctness, diversity, and actionability matter more than row count.

5. Enable timer movement.
   - Rejected. V7's product model is event-driven autonomy.

## Consequences

- Future architecture phases must compare against the ideal model before proposing new owners.
- Future evidence phases must state which knowledge object and maturity stage they improve.
- The next safe phase is `V7.KNOWLEDGE.QUALITY.MODEL`.
- This ADR does not authorize runtime apply or user movement.

## Affected Modules

Documentation/reference only in this phase:

- `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_PROJECT_MAP.md`

Future implementation, if separately approved, should reuse:

- `tools/v7-users-autoswitch`
- `admin_core/operator_decision_surface.py`
- `admin_core/operator_execution_pipeline.py`
- `admin_core/operator_execution.py`
- `admin_core/operator_execution_feedback.py`
- `admin_core/intelligence_platform.py`
- `admin_core/intelligence_workers.py`
- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-intelligence-snapshot-refresh`

## Reference Updates

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_PROJECT_MAP.md`

## Related Reports

- `docs/reports/V7_IDEAL_AUTONOMOUS_ROUTING_SYSTEM_MODEL_REPORT.md`
- `docs/reports/AUTONOMY_EVIDENCE_SATURATION_MODEL_REPORT.md`
- `docs/reports/AUTONOMY_TRUST_SUFFICIENCY_MODEL_REPORT.md`
- `docs/reports/V7_AUTONOMY_BLUEPRINT_DISCOVERY_REPORT.md`

