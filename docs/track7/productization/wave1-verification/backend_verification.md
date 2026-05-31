# Wave 1 Backend Verification

Verification date: 2026-05-30

Mode: verification only.

Runtime state used for verification: isolated temporary state under `/private/tmp/v7-wave1-verify-*`.

## Endpoints

| Endpoint | Result | Notes |
| --- | --- | --- |
| `GET /api/evidence?limit=10` | PASS | Returned HTTP 200 with `items`, `count`, `total`, `next_cursor`, `read_only`, `storage_backend`, `storage_path`, and `generated_sources`. |
| `GET /api/evidence/evidence-check-state-freshness` | PASS | Returned HTTP 200 with a single `bundle` object containing summary, timeline, evidence items, recommendation, verification state, closure state, links, and read-only metadata. |
| `GET /api/evidence/by-object/check/diagnostics?limit=10` | PASS | Returned HTTP 200 with one diagnostics evidence bundle. |
| `GET /api/evidence/no-such-bundle` | PASS | Returned HTTP 404 with `error=evidence_not_found`. |
| `GET /api/evidence/by-object/check` | PASS | Returned HTTP 400 with `error=invalid_evidence_object`. |
| `POST /api/evidence` | PASS | Returned HTTP 404. No mutation endpoint exists for Evidence. |

## Response Shape

List responses include:

- `items`
- `count`
- `total`
- `next_cursor`
- `read_only=true`
- `storage_backend=jsonl`
- `storage_path`
- `generated_sources`

Detail responses include:

- `bundle.bundle_id`
- `bundle.object_type`
- `bundle.object_id`
- `bundle.status`
- `bundle.severity`
- `bundle.summary`
- `bundle.timeline`
- `bundle.evidence_items`
- `bundle.recommendation`
- `bundle.verification_state`
- `bundle.closure_state`
- `bundle.links`
- `read_only=true`
- `storage_backend=jsonl`

## Data Returned

The backend generated real evidence from the isolated runtime state:

- check evidence: `evidence-check-state-freshness`
- route evidence: `evidence-route-reality`
- user evidence for `10.7.0.11` and `10.7.0.12`
- channel evidence for `1` and `amneziawg-exec-20260528-10-8-1-14`
- log evidence: `evidence-log-latest-audit`

## Storage

Selected backend observed in API response:

`jsonl`

Observed store path during verification:

`/private/tmp/v7-wave1-verify-state/evidence-bundles.jsonl`

## Read-Only Behavior

Evidence API is read-only:

- no `POST /api/evidence` handler exists
- no evidence mutation endpoint was observed
- API detail/list responses explicitly return `read_only=true`
- dangerous-call scan of the Wave 1 diff found no added `v7-user-switch`, routing, autoswitch, kill-switch, or action endpoint paths

## Backend Verdict

`evidence_api_working=true`

Backend implementation exists and returns structured, real generated evidence. The backend side of Wave 1 is verified.
