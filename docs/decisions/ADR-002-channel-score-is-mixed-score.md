# ADR-002 Channel Score Is A Mixed Score

Status: Accepted
Date: 2026-06-18
Commit: `8ba2178f`

## Context

Channel UI previously risked implying that the visible score answered whether a channel could receive users. Audits showed this was unsafe: assignment eligibility, evacuation, retention, and execution readiness belong to planner truth, while the score is a technical/mixed health explanation.

Examples from prior audits showed that a high-quality channel can still be restricted by planner gates or role flags, and a lower-scored channel can still be eligible depending on planner truth.

## Decision

Channel Score remains a 0-100 technical/mixed health score derived from existing suitability components: services, stability, capacity, route, runtime/readiness, and history.

It must not be treated as assignment truth. Operator-facing channel decision must come first from V7 Decision / planner-derived assignment role: Use, Evacuate, Keep Current Users, Emergency Only, or Blocked.

## Alternatives considered

- Make score equal assignment eligibility: rejected because assignment has hard gates and role flags that are not reducible to a numeric score.
- Hide score entirely: rejected because it is useful diagnostics once the decision is clear.
- Keep old TRUSTED/WATCH/QUARANTINED framing: rejected because it was not operator-understandable enough.

## Consequences

- UI must present decision first and score/health second.
- High score plus assignment restriction is valid and must be explainable.
- Diagnostics can explain score, but planner truth decides assignment.

## Affected modules

- `admin/v7-admin-api`
- `admin_core/operator_decision_surface.py`
- `tools/v7-users-autoswitch`
- Channel table and Channel Drawer

## Reference updates

- `docs/reference/V7_CANONICAL_REFERENCE.md` sections: Channel Decision V7, Channel Score, Technical Health, Assignment.

## Related reports

- `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`
- `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`
- `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`
- `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`
- `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`
