# E35.D Read API Contract

## Rule

READ APIs only.

No write APIs.

No mutation APIs.

## Endpoints

### `GET /api/authority/summary`

Returns Authority Summary.

### `GET /api/authority/user/{id}`

Returns effective authority for one user:

- routing mode;
- owner;
- state;
- current channel;
- pin/manual/containment metadata;
- timeline preview;
- explanation.

### `GET /api/authority/conflicts`

Returns Conflict Summary and optionally details.

### `GET /api/authority/reviews`

Returns Review Queue.

### `GET /api/authority/emergency`

Returns Emergency Queue.

### `GET /api/authority/timeline`

Filters:

- user;
- channel;
- event type;
- timeframe;
- limit/cursor.

### `GET /api/authority/explain`

Returns Authority Explanation for a read-only context.

## Security

- auth required;
- redacted;
- no secrets;
- no runtime command execution;
- rate limited like other admin read APIs.

## Response Shape

```json
{
  "read_only": true,
  "storage_backend": "json_plus_jsonl",
  "items": [],
  "summary": {},
  "pagination": {},
  "generated_at": "ISO-8601"
}
```

## Tests

- every endpoint returns read_only=true;
- invalid user returns 404 or empty safe response;
- filters are bounded;
- no endpoint invokes runtime mutation.

## Verdict

```text
read_api_contract_defined=true
```
