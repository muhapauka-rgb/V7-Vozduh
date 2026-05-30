# P1.A Evidence Model

evidence_model_defined=true

## Bundle Shape

```json
{
  "bundle_id": "evb_20260530_000001",
  "object_type": "user",
  "object_id": "10.7.0.11",
  "status": "open",
  "severity": "warn",
  "summary": {
    "title": "Required service degraded on current channel",
    "operator_meaning": "User may need a safer channel recommendation.",
    "current_diagnosis": "service_health_mismatch"
  },
  "timeline": [],
  "evidence_items": [],
  "recommendation": {},
  "verification_state": {},
  "closure_state": {}
}
```

## Required Fields

| Field | Meaning |
| --- | --- |
| `bundle_id` | Stable evidence identifier. |
| `object_type` | Linked domain object type. |
| `object_id` | Linked domain object identifier. |
| `status` | Bundle lifecycle state: `open`, `investigating`, `action_ready`, `verifying`, `closed`, `failed_closed`. |
| `severity` | Operator severity: `ok`, `info`, `warn`, `bad`, `muted`. |
| `summary` | Human-readable problem and diagnosis summary. |
| `timeline` | Ordered events that explain how evidence evolved. |
| `evidence_items` | Structured proof items with source, timestamp, redaction and trust level. |
| `recommendation` | Next safe action, if one exists. |
| `verification_state` | Required and completed verification checks. |
| `closure_state` | Whether the issue is closed and why. |

## Evidence Item Shape

Each evidence item should include:

- `item_id`;
- `source`;
- `source_ref`;
- `captured_at`;
- `type`;
- `status`;
- `summary`;
- `redaction_state`;
- `payload_ref`;
- `operator_visibility`;
- `trust_level`.

## Timeline Shape

Each timeline event should include:

- `event_id`;
- `timestamp`;
- `actor`;
- `event_type`;
- `summary`;
- `linked_item_ids`;
- `audit_ref`.

## Status Semantics

Evidence status is descriptive only. It cannot authorize mutation by itself.

Forward mutation still requires approval packet, policy admission, capacity gates, runtime checkers and execution-time recheck.

