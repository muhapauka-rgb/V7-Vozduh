# P1.1 Evidence API Implementation

evidence_api_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: read and inspect evidence bundles
Admin Surface: tables, chips, drawers, logs, checks
Runtime Service: read-only handlers in admin/v7-admin-api
Storage: Evidence Store tables or adapter
API: /api/evidence endpoints
UI Component: EvidenceChip/EvidenceDrawer data loaders
```

## Endpoint: `GET /api/evidence`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `object_type` | string | Optional. |
| `object_id` | string | Optional. |
| `status` | string | Optional comma-list. |
| `severity` | string | Optional comma-list. |
| `source` | string | Optional. |
| `tag` | string | Future optional. |
| `from` | ISO datetime | Optional lower bound. |
| `to` | ISO datetime | Optional upper bound. |
| `q` | string | Search summary/object/source. |
| `limit` | int | Default 50, max 200. |
| `cursor` | string | Opaque pagination cursor. |

### Response

```json
{
  "items": [
    {
      "bundle_id": "evb_20260530_000001",
      "object_type": "user",
      "object_id": "10.7.0.11",
      "status": "open",
      "severity": "warn",
      "title": "Required service degraded",
      "operator_meaning": "User may need route review.",
      "current_diagnosis": "service_health_mismatch",
      "updated_at": "2026-05-30T12:00:00Z",
      "links": []
    }
  ],
  "next_cursor": null,
  "summary": {
    "open": 1,
    "warn": 1,
    "bad": 0
  }
}
```

## Endpoint: `GET /api/evidence/{id}`

### Request Path

`id` is `bundle_id`.

### Response

```json
{
  "bundle": {},
  "links": [],
  "timeline": [],
  "items": [],
  "recommendation": {},
  "verification_state": {},
  "closure_state": {},
  "advanced_details_allowed": false
}
```

## Endpoint: `GET /api/evidence/by-object/{type}/{id}`

### Request Path

- `type`: normalized object type: `user`, `channel`, `proposal`, `alert`, `route`, `release`, `backup`, `restore`.
- `id`: URL-encoded object id.

### Response

Same list envelope as `GET /api/evidence`, scoped through `evidence_links`.

## Pagination

Use cursor format:

```text
base64(updated_at|bundle_id)
```

Cursor is opaque to UI. Sorting defaults to `updated_at DESC`.

## Security Model

Required role:

- list/detail default: `viewer`;
- advanced restricted details: role-gated later, likely `admin` or `owner`;
- no mutation through these endpoints.

Rules:

- never inline secrets;
- respect `operator_visibility`;
- show `redaction_state`;
- payload refs remain references unless advanced role is allowed.

## Handler Placement

Add read handlers near existing `/api/overview`, `/api/users` and other GET endpoints in `admin/v7-admin-api`.

Do not place under `/api/actions` because these are read-only.

## Implementation Completeness

Endpoint contracts are implementation-ready. Missing decision: storage backend finalization.
