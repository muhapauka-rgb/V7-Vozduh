# E35.D Test Plan

## Storage Tests

- authority state read;
- authority state schema validation;
- unreadable state fails closed;
- single source of truth enforced;
- no duplication of `users.registry.current`.

## Event Tests

- timeline read;
- event id uniqueness;
- corrupt JSONL line handled safely;
- event links preserved;
- archive rules preserve unresolved items.

## Read Model Tests

- Authority Summary;
- Authority Timeline;
- Conflict Summary;
- Conflict Detail;
- Review Queue;
- Emergency Queue;
- Authority Health;
- Authority Explanation.

## API Tests

- `GET /api/authority/summary`;
- `GET /api/authority/user/{id}`;
- `GET /api/authority/conflicts`;
- `GET /api/authority/reviews`;
- `GET /api/authority/emergency`;
- `GET /api/authority/timeline`;
- `GET /api/authority/explain`;
- every endpoint `read_only=true`.

## Admin Tests

- Home renders summary;
- Users renders authority state;
- Channels renders pinned/conflict state;
- Checks renders authority health;
- Logs renders authority events.

## Safety Tests

- no runtime mutation;
- no user movement;
- no routing mutation;
- no autoswitch apply;
- no policy apply;
- no kill switch mutation.

## Verdict

```text
test_plan_defined=true
```
