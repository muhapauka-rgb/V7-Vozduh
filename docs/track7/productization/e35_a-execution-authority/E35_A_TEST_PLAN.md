# E35.A Test Plan

## Unit Tests

### Authority Resolver

- missing user record derives group default AUTO;
- explicit user AUTO overrides group default;
- OPERATOR_PINNED blocks autoswitch forward movement;
- MANUAL blocks autoswitch forward movement;
- expired pin returns REVIEW_REQUIRED or configured default;
- emergency state allows only containment actions.

### Override Matrix

- autoswitch cannot override pin;
- autoswitch cannot override manual;
- operator can remove own pin;
- governance requires explicit override for pinned/manual users;
- containment can emergency-override pin only on hard failure;
- safety blocks everyone for forward movement.

### API Tests

- `GET /api/routing-authority/users` returns effective authority;
- `GET /api/routing-authority/users/{ip}` returns mode/owner/reason/current channel;
- `GET /api/routing-authority/events` returns redacted append-only events;
- `POST /api/routing-authority/decision-preview` returns ALLOW/DENY/REVIEW_REQUIRED/EMERGENCY_ONLY;
- preview never mutates runtime.

### Autoswitch Integration Tests

- AUTO user can be selected when all gates pass;
- OPERATOR_PINNED user is not selected for higher score;
- OPERATOR_PINNED user is not selected for higher speed;
- MANUAL user is not selected;
- authority denial appears in plan explanation;
- emergency failover path is separate from planned movement.

### Governance Tests

- packet includes authority state hash;
- stale authority hash denies execution;
- pinned user requires override reason;
- replay remains denied;
- rollback remains allowed under containment/approved scope.

### Admin Tests

- Users drawer shows Routing Mode;
- Users drawer shows owner/reason/expiry;
- Channels drawer shows pinned users;
- Home shows pinned/emergency/conflict counts;
- Logs filter authority events;
- authority change does not move user.

### Safety Scans

- no authority API calls `v7-user-switch`;
- no authority API calls autoswitch apply;
- no authority API calls routing sync;
- no kill switch mutation;
- no policy apply;
- no Direct/Trusted RU refresh.

## Acceptance Scenarios

| Scenario | Expected |
|---|---|
| AUTO user normal movement | `ALLOW` if all gates pass |
| Pinned user faster alternative | `DENY` |
| Pinned user current channel hard down | `EMERGENCY_ONLY` |
| Pinned user recovered target | return available after restore-settle |
| MANUAL user autoswitch | `DENY` |
| Governance packet stale authority | `DENY` |
| Safety block | forward `DENY` |
| Rollback containment | allowed when scoped |
| Group conflict | `DENY` before score |
| Required service conflict | `DENY` or `REVIEW_REQUIRED` per service policy |

## Verdict

```text
test_plan_defined=true
```
