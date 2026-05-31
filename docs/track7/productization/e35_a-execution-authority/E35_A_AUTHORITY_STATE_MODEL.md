# E35.A Authority State Model

## Design Principle

Authority state is intent and permission.

It must not replace runtime truth.

Current runtime truth remains:

```text
users.registry.current
users.registry.table
```

Authority state explains:

```text
who is allowed to change this user
why
for how long
under what override rules
```

## Recommended Storage

Start with a dedicated JSON-compatible authority store:

```text
STATE_DIR/routing-authority.json
```

and append-only events:

```text
STATE_DIR/routing-authority-events.jsonl
```

Reason:

- keeps intent separate from `users.registry`;
- avoids overloading service preferences;
- easy to migrate to SQLite later;
- supports audit history.

## User Authority Record

```json
{
  "schema_version": 1,
  "users": {
    "10.7.0.11": {
      "routing_mode": "AUTO",
      "routing_owner": "AUTOSWITCH",
      "authority_source": "group_default",
      "authority_reason": "default_auto",
      "authority_created_at": "2026-05-31T00:00:00Z",
      "authority_expires_at": "",
      "preferred_egress": "",
      "pin_created_by": "",
      "pin_evidence_bundle": "",
      "pin_proposal_id": "",
      "pin_comment": "",
      "emergency_state": "NONE",
      "emergency_started_at": "",
      "emergency_return_target": ""
    }
  }
}
```

## Field Definitions

| Field | Meaning | Authority |
|---|---|---|
| `routing_mode` | AUTO / OPERATOR_PINNED / MANUAL | Authoritative |
| `routing_owner` | AUTOSWITCH / OPERATOR / GOVERNANCE / SCHEDULER / CONTAINMENT | Authoritative |
| `authority_source` | where rule came from | Authoritative |
| `authority_reason` | human-readable why | Authoritative |
| `authority_created_at` | creation timestamp | Authoritative |
| `authority_expires_at` | optional expiry | Authoritative |
| `preferred_egress` | intended/pinned/preferred target | Authoritative for pin/manual, preference for AUTO |
| `pin_created_by` | operator id | Authoritative |
| `pin_evidence_bundle` | evidence linkage | Reference |
| `pin_proposal_id` | proposal linkage | Reference |
| `pin_comment` | operator note | Authoritative note |
| `emergency_state` | NONE / ESCAPED / RETURN_READY / RETURNED | Derived from events + current state |
| `emergency_return_target` | original target for return | Authoritative during emergency |

## Derived Effective Authority

Effective authority is computed from:

```text
user authority record
group default routing mode
users.registry current state
channel eligibility
runtime trust
restore-settle
packet/governance state
```

Default:

```text
if no user authority record:
  use group.default_routing_mode
if no group default:
  AUTO
```

## Event Record

```json
{
  "schema_version": 1,
  "event_id": "auth_evt_<hash>",
  "event_type": "AUTHORITY_SET",
  "user_ip": "10.7.0.11",
  "from": {"routing_mode": "AUTO"},
  "to": {"routing_mode": "OPERATOR_PINNED", "preferred_egress": "1"},
  "actor": "admin",
  "reason": "operator_pin",
  "evidence_bundle_id": "",
  "proposal_id": "",
  "created_at": "2026-05-31T00:00:00Z",
  "runtime_mutation": false,
  "routing_mutation": false,
  "user_movement": false
}
```

## API Mapping

Read:

- `GET /api/routing-authority/users`
- `GET /api/routing-authority/users/{ip}`
- `GET /api/routing-authority/events`

Preview:

- `POST /api/routing-authority/decision-preview`

Future mutation:

- `POST /api/routing-authority/users/{ip}/set-mode`
- `POST /api/routing-authority/users/{ip}/pin`
- `POST /api/routing-authority/users/{ip}/unpin`

Mutation APIs must not move users. They only change authority intent.

## Tests

- default authority derives from group;
- explicit user record overrides group default;
- expired authority returns `REVIEW_REQUIRED` or group default;
- pin event is append-only;
- setting authority does not mutate routing;
- authority preview never calls `v7-user-switch`.

## Verdict

```text
authority_state_model_defined=true
runtime_truth_preserved=true
```
