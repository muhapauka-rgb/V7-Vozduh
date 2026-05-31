# P1.B Proposal Model

proposal_model_defined=true

## Proposal Shape

```json
{
  "proposal_id": "prop_20260530_000001",
  "proposal_type": "USER_MOVEMENT",
  "status": "ACTIVE",
  "confidence": "HIGH",
  "severity": "warn",
  "reason": "Required services are healthier on proposed target.",
  "affected_users": ["10.7.0.11"],
  "current_target": "1",
  "proposed_target": "amneziawg-exec-20260528-10-8-1-14",
  "required_services": ["ChatGPT", "Google Auth"],
  "evidence_bundle_id": "evb_20260530_000001",
  "expected_benefit": {
    "service_satisfaction": "higher",
    "quality": "GO",
    "risk_reduction": "medium"
  },
  "rollback_hint": {
    "rollback_target": "1",
    "rollback_scope": ["10.7.0.11"]
  },
  "created_at": "2026-05-30T00:00:00Z"
}
```

## Required Fields

| Field | Meaning |
| --- | --- |
| `proposal_id` | Stable proposal identifier. |
| `proposal_type` | Recommendation category. |
| `status` | Proposal lifecycle status. |
| `confidence` | Confidence in recommendation. |
| `severity` | Operator severity. |
| `reason` | Human-readable reason. |
| `affected_users` | Exact user scope, if user-affecting. |
| `current_target` | Current channel/target when relevant. |
| `proposed_target` | Proposed channel/target when relevant. |
| `required_services` | Services that shaped the recommendation. |
| `evidence_bundle_id` | Required evidence link. |
| `expected_benefit` | Expected improvement or risk reduction. |
| `rollback_hint` | Rollback target/scope hint, not authority. |
| `created_at` | Creation timestamp. |

## Proposal Types

Initial types:

- `USER_MOVEMENT`;
- `BATCH_MOVEMENT`;
- `CHANNEL_AVOIDANCE`;
- `ROUTE_REVIEW`;
- `SERVICE_HEALTH_REVIEW`;
- `RECOVERY_ACTION`;
- `OBSERVATION_ONLY`.

## Confidence

Recommended levels:

- `LOW`;
- `MEDIUM`;
- `HIGH`;
- `VERY_HIGH`.

Confidence is derived from evidence freshness, agreement between signals, validation history, service health and runtime gates.

## Authority Boundary

Proposal model may describe an action, but it cannot authorize or execute it.
