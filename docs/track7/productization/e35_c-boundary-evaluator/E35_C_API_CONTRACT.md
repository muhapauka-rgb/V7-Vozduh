# E35.C API Contract

## Rule

READ APIs only.

No runtime mutation APIs in E35.C.

## Endpoints

### `GET /api/authority/verdicts`

Returns recent verdicts.

Filters:

- user;
- actor;
- verdict;
- action_type;
- timeframe;
- domain.

### `GET /api/authority/conflicts`

Returns current/recent conflicts.

### `GET /api/authority/reviews`

Returns review queue and closed reviews.

### `GET /api/authority/emergency`

Returns active/recent emergency verdicts/actions.

### `GET /api/authority/explain`

Returns explanation for a user/channel/action context.

Query examples:

- `user_ip`;
- `target_channel`;
- `action_type`;
- `actor`.

## Response Shape

```json
{
  "items": [],
  "pagination": {},
  "summary": {
    "pending_reviews": 0,
    "emergency_actions": 0,
    "denied_actions": 0,
    "boundary_conflicts": 0
  }
}
```

## Security

- auth required;
- redacted output;
- no raw secrets;
- no mutation side effects.

## Tests

- each endpoint returns redacted data;
- unknown filters fail safely;
- no endpoint invokes movement or apply commands.

## Verdict

```text
api_contract_defined=true
```
