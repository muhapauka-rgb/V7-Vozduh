# E35.C Event Model

## Event Types

- `VERDICT_CREATED`
- `VERDICT_DENIED`
- `VERDICT_ALLOWED`
- `VERDICT_REVIEW_REQUIRED`
- `VERDICT_EMERGENCY`
- `CONFLICT_DETECTED`
- `CONFLICT_RESOLVED`
- `REVIEW_CREATED`
- `REVIEW_CLOSED`
- `EMERGENCY_CREATED`
- `EMERGENCY_EXPIRED`

## Event Schema

```json
{
  "schema_version": "e35c.boundary-event.v1",
  "event_id": "evt_<hash>",
  "event_type": "VERDICT_DENIED",
  "created_at": "ISO-8601",
  "actor": "AUTOSWITCH",
  "action_id": "act_<id>",
  "action_type": "FORWARD_MOVE",
  "user_ip": "10.7.0.11",
  "current_channel": "1",
  "target_channel": "awg2",
  "verdict": "DENY",
  "reason": "operator_pinned",
  "domains": ["OPERATOR", "AUTOSWITCH"],
  "conflict_id": "",
  "review_id": "",
  "emergency_id": "",
  "evidence_bundle_id": "",
  "proposal_id": "",
  "input_hash": "",
  "policy_version": "e35c.boundary-policy.v1",
  "runtime_mutation": false,
  "routing_mutation": false,
  "user_movement": false
}
```

## Retention

Recommended:

- verdict events: 90 days active;
- conflicts/reviews/emergencies: 180 days active;
- compressed/archive retention per audit policy.

## Links

Events may link to:

- Evidence;
- Proposal;
- Runtime Trust;
- Release Trust;
- approval packet;
- authority state.

## Verdict

```text
event_model_defined=true
```
