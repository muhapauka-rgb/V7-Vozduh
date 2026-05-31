# P1.C API Model

runtime_convergence_api_defined=true

## API Surface

Required read APIs:

```text
GET /api/runtime/convergence
GET /api/runtime/fingerprint
GET /api/runtime/drift
```

These APIs expose runtime trust state. They must not mutate runtime or apply recovery.

## `GET /api/runtime/convergence`

Purpose: return operator-ready runtime trust summary.

Response shape:

```json
{
  "status": "RUNTIME_OK",
  "release_match": true,
  "summary": "System matches release",
  "verification_age_seconds": 120,
  "drift_count": 0,
  "blocking": false,
  "evidence_bundle_id": "evb_20260530_runtime",
  "recommended_action": null
}
```

## `GET /api/runtime/fingerprint`

Purpose: return current fingerprint summary and role-gated details.

Response shape:

```json
{
  "fingerprint_id": "rtfp_20260530_000001",
  "captured_at": "2026-05-30T00:00:00Z",
  "release_ref": "release_20260530",
  "hash_summary": "match",
  "redaction_state": "redacted",
  "advanced_details_allowed": false
}
```

## `GET /api/runtime/drift`

Purpose: list current and historical drift records.

Filters:

- `status`;
- `severity`;
- `drift_type`;
- `from`;
- `to`;
- `blocking`;
- `q`;
- `limit`;
- `cursor`.

Response shape:

```json
{
  "items": [],
  "next_cursor": null,
  "summary": {
    "blocking": 0,
    "warning": 0,
    "closed": 0
  }
}
```

## Security Model

APIs must:

- redact raw hash internals by default;
- hide sensitive file/config details unless role-gated;
- avoid returning secrets or private profile material;
- clearly separate summary from advanced details;
- never execute convergence repair as a side effect.

## API Verdict

Runtime Convergence API is a read-first trust API for current admin surfaces and future release/recovery workflows.
