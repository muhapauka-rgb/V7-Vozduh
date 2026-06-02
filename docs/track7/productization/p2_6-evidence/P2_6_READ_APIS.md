# P2.6 Read APIs

## Result

read_apis_implemented=true

## Endpoints

- `GET /api/execution/candidates`
- `GET /api/execution/candidates/{id}`
- `GET /api/execution/candidates/readiness`
- `GET /api/execution/candidates/risks`
- `GET /api/execution/candidates/explain`
- `GET /api/execution/candidates/timeline`

## Security

All endpoints require authenticated admin API access. Viewer role is sufficient.

## Safety Flags

Every response preserves read-only, non-authoritative, preview-only, and `execution_allowed_now=false` semantics.
