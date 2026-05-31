# P1.2 Release Trust API Implementation

release_api_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: read current release trust and rollback lineage
Operator Meaning: release certified, rollback available, attention required
Admin Surface: Главная, Проверки, Безопасность
Runtime Service: read-only release handlers in admin/v7-admin-api
Storage: Release Trust Store
API: release trust endpoints
UI Component: ReleaseTrustStatus and ReleaseDrawer loaders
```

## Endpoint: `GET /api/release/current`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `include_runtime` | bool | Optional, include runtime match summary. |
| `include_rollback` | bool | Optional, default true. |

### Response

```json
{
  "release_id": "rel_20260530",
  "label": "2026.05.30",
  "status": "RELEASE_OK",
  "certified": true,
  "certification_state": "certified",
  "rollback_available": true,
  "runtime_match": true,
  "verified_at": "2026-05-30T12:00:00Z",
  "expires_at": "2026-05-30T13:00:00Z",
  "evidence_bundle_id": "evb_release_20260530",
  "recommended_action": null
}
```

## Endpoint: `GET /api/release/history`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `status` | string | Optional comma-list. |
| `certified` | bool | Optional. |
| `from` | ISO datetime | Optional. |
| `to` | ISO datetime | Optional. |
| `q` | string | Search release label/id. |
| `limit` | int | Default 50, max 200. |
| `cursor` | string | Opaque cursor. |

### Response

```json
{
  "items": [],
  "next_cursor": null,
  "summary": {
    "current": "rel_20260530",
    "rollback_available": true,
    "blocking": 0
  }
}
```

## Endpoint: `GET /api/release/{id}`

### Response

```json
{
  "release": {},
  "certification": {},
  "lineage": [],
  "rollback_lineage": [],
  "verification_history": [],
  "runtime_convergence": {},
  "advanced_details_allowed": false
}
```

## Security Model

Required role:

- default summary/list/detail: `viewer`;
- advanced provenance details: role-gated, likely `admin` or `owner`.

Rules:

- no deploy credentials;
- no secrets;
- no mutation side effects;
- commit/signature/manifest internals hidden by default.

## Search Model

Release history supports search by:

- release id;
- label;
- status;
- certification state;
- verification time;
- rollback availability.

## Implementation Completeness

Release API implementation is defined for read-only P0.
