# P1.1 Proposal API Implementation

proposal_api_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: read and inspect evidence-backed recommendations
Admin Surface: Главная, Пользователи, Каналы, Маршруты
Runtime Service: read-only proposal handlers in admin/v7-admin-api
Storage: Proposal Store
API: /api/proposals endpoints
UI Component: ProposalCard/ProposalDrawer loaders
```

## Endpoint: `GET /api/proposals`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `proposal_type` | string | Optional comma-list. |
| `status` | string | Optional comma-list. |
| `confidence` | string | Optional comma-list. |
| `severity` | string | Optional comma-list. |
| `object_type` | string | Optional linked object scope. |
| `object_id` | string | Optional linked object id. |
| `user` | string | Optional user IP. |
| `current_target` | string | Optional. |
| `proposed_target` | string | Optional. |
| `required_service` | string | Optional. |
| `from` | ISO datetime | Optional. |
| `to` | ISO datetime | Optional. |
| `q` | string | Search reason/object/target. |
| `limit` | int | Default 50, max 200. |
| `cursor` | string | Opaque pagination cursor. |

### Response

```json
{
  "items": [
    {
      "proposal_id": "prop_20260530_000001",
      "proposal_type": "USER_MOVEMENT",
      "status": "ACTIVE",
      "confidence": "HIGH",
      "severity": "warn",
      "reason": "Required services are healthier on proposed target.",
      "affected_users": ["10.7.0.11"],
      "current_target": "1",
      "proposed_target": "amneziawg-exec-20260528-10-8-1-14",
      "required_services": ["ChatGPT"],
      "evidence_bundle_id": "evb_20260530_000001",
      "expires_at": "2026-05-30T13:00:00Z",
      "updated_at": "2026-05-30T12:00:00Z"
    }
  ],
  "next_cursor": null,
  "summary": {
    "active": 1,
    "review_required": 0,
    "expired": 0
  }
}
```

## Endpoint: `GET /api/proposals/{id}`

### Response

```json
{
  "proposal": {},
  "links": [],
  "timeline": [],
  "evidence": {
    "bundle_id": "evb_20260530_000001",
    "status": "open",
    "severity": "warn"
  },
  "governance_path": {
    "batch_ready": false,
    "blocked_reasons": []
  },
  "advanced_details_allowed": false
}
```

## Endpoint: `GET /api/proposals/by-object/{type}/{id}`

Returns proposals linked to current admin object.

Supported object types:

- `user`;
- `channel`;
- `route`;
- `evidence`;
- `batch` future.

## Filter Model

Filters should be applied server-side. UI should not load all proposals and filter client-side after first implementation scale.

## Security Model

Required role:

- list/detail default: `viewer`;
- advanced details: role-gated later;
- submission/closure endpoints are future and must be audited.

Read endpoints must never:

- move users;
- create approval packets;
- mutate runtime;
- apply autoswitch.

## Implementation Completeness

API plan is implementation-ready for read-only proposal surfaces. Mutation/submission endpoints remain P1.
