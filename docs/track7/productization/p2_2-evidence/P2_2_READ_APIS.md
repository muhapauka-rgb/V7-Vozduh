# P2.2 Read APIs

## Endpoints Added

Read-only endpoints:

- `GET /api/execution/contracts/draft`
- `GET /api/execution/contracts/draft/{id}`
- `GET /api/execution/validation-preview`
- `GET /api/execution/verification-preview`
- `GET /api/execution/rollback-preview`
- `GET /api/execution/readiness-preview`

## Endpoint Behavior

All endpoints:

- require existing admin auth
- are read-only
- return preview-only models
- set `execution_allowed_now=false`
- do not create contracts
- do not consume authority
- do not execute anything

## No Mutation Endpoints

No P2.2 POST, PUT, PATCH, DELETE, apply, execute, route, switch, policy, or autoswitch endpoint was added.

## Verdict

read_apis_implemented=true
read_apis_preview_only=true
runtime_mutation_performed=false
