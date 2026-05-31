# P1.D/E API Model

release_trust_api_defined=true

## API Surface

Required read APIs:

```text
GET /api/release/current
GET /api/release/history
GET /api/release/{id}
```

These APIs expose release trust state. They must not deploy, rollback or mutate runtime.

## `GET /api/release/current`

Purpose: return operator-ready current release trust summary.

Response shape:

```json
{
  "release_id": "rel_20260530",
  "label": "2026.05.30",
  "status": "RELEASE_OK",
  "certified": true,
  "rollback_available": true,
  "runtime_match": true,
  "verification_age_seconds": 120,
  "evidence_bundle_id": "evb_20260530_release",
  "recommended_action": null
}
```

## `GET /api/release/history`

Purpose: list release lineage and verification history.

Filters:

- `status`;
- `certified`;
- `from`;
- `to`;
- `q`;
- `limit`;
- `cursor`.

Response shape:

```json
{
  "items": [],
  "next_cursor": null,
  "summary": {
    "current": "rel_20260530",
    "rollback_available": true
  }
}
```

## `GET /api/release/{id}`

Purpose: return full Release Drawer data.

Response includes:

- release summary;
- status;
- certification;
- provenance;
- release lineage;
- rollback lineage;
- runtime convergence link;
- verification history;
- advanced details allowed for caller role.

## Security Model

APIs must:

- avoid exposing secrets or deploy credentials;
- hide raw manifest/signature internals by default;
- show advanced detail only by role;
- never trigger deployment, rollback or mutation as side effect.

## Operator Visibility

Primary response fields must be operator-readable:

- current release;
- certified;
- rollback available;
- runtime match;
- attention required.

## API Verdict

Release Trust API is a read-first product API for admin trust surfaces, runtime convergence and recovery workflows.
