# P2.3 Read APIs

## Result

read_apis_implemented=true

## Endpoints

GET `/api/execution/gates`

Returns the gate catalog, status per gate, adapter sources, and per-draft checks.

GET `/api/execution/gates/{id}`

Returns one gate with its draft-level adapter checks.

GET `/api/execution/readiness`

Returns readiness status, unknown/review/failed gates, gate summary, recent generated drafts, and preview safety flags.

GET `/api/execution/readiness/detail`

Returns readiness plus validation, verification, and rollback previews.

GET `/api/execution/validation-evidence`

Returns adapter-backed validation evidence grouped by draft and gate.

## Security

All endpoints are read-only and require authenticated admin API access. Viewer role is sufficient.

## Safety flags

Every response includes read-only/preview-only semantics where applicable:

- read_only=true
- non_authoritative=true
- preview_only=true
- execution_allowed_now=false
