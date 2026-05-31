# P1.2 Runtime Trust API Implementation

runtime_api_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: read runtime trust and drift state
Operator Meaning: runtime OK, warning, drift, unknown or blocking
Admin Surface: Главная, Проверки, Безопасность
Runtime Service: read-only API handlers in admin/v7-admin-api
Storage: Runtime Convergence Store
API: runtime trust endpoints
UI Component: RuntimeTrustStatus and RuntimeTrustDrawer loaders
```

## Endpoint: `GET /api/runtime/convergence`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `include_history` | bool | Optional, default false. |
| `include_drift` | bool | Optional, default true summary only. |

### Response

```json
{
  "status": "RUNTIME_OK",
  "release_match": true,
  "summary": "System matches release",
  "verification_age_seconds": 120,
  "expires_at": "2026-05-30T12:10:00Z",
  "drift_count": 0,
  "blocking": false,
  "fingerprint_id": "rtfp_20260530_000001",
  "release_ref": "rel_20260530",
  "evidence_bundle_id": "evb_runtime_20260530",
  "recommended_action": null
}
```

## Endpoint: `GET /api/runtime/fingerprint`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `id` | string | Optional fingerprint id; latest if omitted. |
| `advanced` | bool | Optional; honored only by role. |

### Response

```json
{
  "fingerprint_id": "rtfp_20260530_000001",
  "captured_at": "2026-05-30T12:00:00Z",
  "runtime_label": "V7 Admin runtime",
  "release_ref": "rel_20260530",
  "hash_summary": "match",
  "redaction_state": "redacted",
  "advanced_details_allowed": false,
  "payload_ref": null
}
```

## Endpoint: `GET /api/runtime/drift`

### Request Query

| Query | Type | Notes |
| --- | --- | --- |
| `status` | string | Optional comma-list. |
| `severity` | string | Optional comma-list. |
| `drift_type` | string | Optional. |
| `blocking` | bool | Optional. |
| `from` | ISO datetime | Optional. |
| `to` | ISO datetime | Optional. |
| `limit` | int | Default 50, max 200. |
| `cursor` | string | Opaque cursor. |

### Response

```json
{
  "items": [
    {
      "drift_id": "rtdrift_20260530_000001",
      "drift_type": "release_drift",
      "severity": "bad",
      "status": "open",
      "summary": "Runtime does not match expected release",
      "impact": "forward_governance_blocked",
      "detected_at": "2026-05-30T12:00:00Z",
      "evidence_bundle_id": "evb_runtime_20260530"
    }
  ],
  "next_cursor": null,
  "summary": {
    "open": 1,
    "blocking": 1,
    "warning": 0
  }
}
```

## Security

Required role:

- default summary/list: `viewer`;
- advanced fingerprint payload refs: role-gated, likely `admin` or `owner`.

Security rules:

- no secrets or raw configs in default response;
- raw hashes are not primary operator data;
- no route/user/runtime mutation;
- refresh, if implemented later, must be guarded and audited.

## Refresh Model

P0:

- read latest stored state;
- optionally recompute safe summary from existing read-only overview/check state.

P1:

- `POST /api/actions/runtime-convergence-refresh-preview`;
- `POST /api/actions/runtime-convergence-refresh-apply` only if refresh is proven read-only and role-gated.

## Implementation Completeness

Runtime API implementation is defined for read-only P0.
