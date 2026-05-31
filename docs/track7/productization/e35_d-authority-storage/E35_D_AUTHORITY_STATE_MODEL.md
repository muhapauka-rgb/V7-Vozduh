# E35.D Authority State Model

## Product Meaning

Authority state records who is allowed to change a user's channel and why.

It is not current routing state.

## Operator Meaning

The operator can answer:

- is this user AUTO, pinned or manual?
- who owns this decision?
- why is movement allowed or blocked?
- when does the authority expire?

## Runtime Mapping

Runtime still reads actual current assignment from:

```text
users.registry.current
users.registry.table
```

Authority state is read by:

- evaluator;
- autoswitch gate;
- manual switch precheck;
- governed execution recheck;
- admin read models.

## State Object

```json
{
  "schema_version": "e35d.authority-state.v1",
  "updated_at": "ISO-8601",
  "updated_by": "system",
  "users": {
    "10.7.0.11": {
      "routing_mode": "AUTO",
      "authority_owner": "AUTOSWITCH",
      "authority_source": "group_default",
      "authority_status": "ACTIVE",
      "authority_reason": "default_auto",
      "preferred_egress": "",
      "authority_created_at": "ISO-8601",
      "authority_expires_at": "",
      "pin_metadata": {},
      "manual_metadata": {},
      "containment_metadata": {}
    }
  }
}
```

## Fields

| Field | Purpose | Required |
|---|---|---:|
| `routing_mode` | AUTO / OPERATOR_PINNED / MANUAL | Yes |
| `authority_owner` | AUTOSWITCH / OPERATOR / GOVERNANCE / SCHEDULER / CONTAINMENT | Yes |
| `authority_source` | group_default, operator_pin, governance, emergency, imported | Yes |
| `authority_status` | ACTIVE / EXPIRED / REVIEW_REQUIRED / EMERGENCY | Yes |
| `authority_reason` | operator-readable reason | Yes |
| `preferred_egress` | pinned/preferred/manual target when relevant | Optional |
| `authority_created_at` | lineage | Yes |
| `authority_expires_at` | expiry when bounded | Optional |
| `pin_metadata` | pin actor/comment/evidence/proposal | Optional |
| `manual_metadata` | manual actor/comment/expiry | Optional |
| `containment_metadata` | emergency state/return target/lease | Optional |

## API Contract

Read state through read models, not raw file:

- `GET /api/authority/user/{id}`
- `GET /api/authority/summary`

## Retention

Current authority state is retained while user exists. Historical changes move to event storage.

## Audit Rules

Every state change must create an event with actor, reason, previous state, next state and safety flags.

## Tests

- missing user derives group default;
- explicit user state overrides group default;
- expired authority resolves to REVIEW_REQUIRED or group default;
- current routing is not duplicated as authority truth.

## Verdict

```text
authority_state_model_defined=true
```
