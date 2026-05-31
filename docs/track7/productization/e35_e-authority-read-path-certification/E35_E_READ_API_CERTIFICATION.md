# E35.E Read API Certification

## Certified Endpoints

- `GET /api/authority/summary`
- `GET /api/authority/user/{id}`
- `GET /api/authority/conflicts`
- `GET /api/authority/reviews`
- `GET /api/authority/emergency`
- `GET /api/authority/timeline`
- `GET /api/authority/explain`

## Endpoint Rules

For every endpoint:

- truth source is Authority Store/Event Store plus linked stores;
- derived fields must declare source;
- failure returns degraded/read-only state;
- caching requires source hash;
- drift returns warning and no movement authority.

## Response Requirements

Every response includes:

- `read_only=true`;
- `generated_at`;
- `source_hash`;
- `storage_backend`;
- `authority_health`;
- redacted payload.

## Verdict

```text
api_certified=true
```
