# P2.7 Read APIs

## Added APIs

- `GET /api/execution/candidate-approval`
- `GET /api/execution/candidate-governance`
- `GET /api/execution/candidate-rehearsal`
- `GET /api/execution/candidate-workflow`

All APIs are read-only, preview-only, viewer-accessible, and derived from existing candidate and operator observability models.

## Detail Mode

Each API supports `?detail=1` for detail read models. Without detail mode, APIs return summaries.

## Safety

No write APIs, approval actions, execution actions, POST handlers, runtime hooks, or apply paths were added.

## Verdict

read_apis_implemented=true
implementation_safe=true
