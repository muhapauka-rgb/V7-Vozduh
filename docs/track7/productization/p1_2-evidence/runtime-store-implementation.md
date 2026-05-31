# P1.2 Runtime Trust Store Implementation

runtime_store_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: prove whether current runtime can be trusted
Operator Meaning: system matches release, drift detected, trust unknown, or blocking
Admin Surface: Главная, Проверки, Безопасность
Runtime Service: convergence snapshot helpers in admin/v7-admin-api, read-only by default
Storage: Runtime Convergence Store
API: GET /api/runtime/convergence, GET /api/runtime/fingerprint, GET /api/runtime/drift
UI Component: RuntimeTrustStatus, RuntimeTrustDrawer, DriftComponent, VerificationHistoryView
```

## Implementation Location

Initial implementation should live beside the existing admin service:

- source: `admin/v7-admin-api`;
- API style: current HTTP handler branch pattern;
- data source: current overview/check/runtime state plus future convergence snapshot helper;
- UI: embedded `/admin-v2` components.

## Storage Schema

Recommended backend: same backend selected for Evidence/Proposal stores. SQLite is preferred because drift and history need indexed lookup.

### `runtime_convergence_snapshots`

| Column | Type | Notes |
| --- | --- | --- |
| `snapshot_id` | text primary key | Stable snapshot id. |
| `status` | text not null | `RUNTIME_OK`, `RUNTIME_WARNING`, `RUNTIME_DRIFT`, `RUNTIME_UNKNOWN`, `RUNTIME_BLOCKING`. |
| `release_ref` | text | Expected release id/label. |
| `release_match` | integer | 0/1/null. |
| `fingerprint_id` | text | FK/reference to fingerprint summary. |
| `drift_count` | integer | Current drift count. |
| `blocking` | integer not null | 0/1. |
| `summary` | text not null | Operator-readable. |
| `recommended_action_json` | text | Optional action object. |
| `evidence_bundle_id` | text | Evidence link. |
| `captured_at` | text not null | ISO timestamp. |
| `expires_at` | text | Freshness expiry. |

### `runtime_fingerprints`

| Column | Type | Notes |
| --- | --- | --- |
| `fingerprint_id` | text primary key | Stable id. |
| `captured_at` | text not null | ISO timestamp. |
| `runtime_label` | text | Operator label. |
| `release_ref` | text | Expected release. |
| `hash_summary` | text | `match`, `mismatch`, `unknown`, not raw hashes. |
| `payload_ref` | text | Advanced referenced payload. |
| `payload_hash` | text | Optional hash. |
| `redaction_state` | text not null | `redacted`, `safe`, `restricted`. |
| `source_checker` | text | Checker/helper name. |

### `runtime_drift_records`

| Column | Type | Notes |
| --- | --- | --- |
| `drift_id` | text primary key | Stable drift id. |
| `snapshot_id` | text | FK/reference to snapshot. |
| `drift_type` | text not null | `runtime_drift`, `config_drift`, `release_drift`, `lineage_drift`. |
| `severity` | text not null | `info`, `warn`, `bad`, `muted`. |
| `status` | text not null | `open`, `known`, `closed`, `failed_closed`. |
| `affected_surface` | text | Admin surface or subsystem. |
| `summary` | text not null | Operator-readable. |
| `impact` | text | Forward action impact. |
| `recommended_action_json` | text | Optional action object. |
| `evidence_bundle_id` | text | Evidence link. |
| `detected_at` | text not null | ISO timestamp. |
| `closed_at` | text | Nullable. |

### `runtime_verification_events`

| Column | Type | Notes |
| --- | --- | --- |
| `event_id` | text primary key | Stable event id. |
| `snapshot_id` | text | FK/reference. |
| `timestamp` | text not null | ISO timestamp. |
| `source` | text not null | checker/helper/operator. |
| `result` | text not null | `OK`, `WARN`, `DRIFT`, `BLOCKED`, `UNKNOWN`. |
| `summary` | text not null | Operator-readable. |
| `lineage_ref_json` | text | Release/backup/restore refs. |
| `evidence_bundle_id` | text | Evidence link. |

## Lineage References

Runtime store must reference:

- release id;
- release verification event;
- backup/restore reference if relevant;
- evidence bundle id;
- audit reference when available.

## Indexes

- `idx_runtime_snapshot_status(status, captured_at)`;
- `idx_runtime_snapshot_release(release_ref)`;
- `idx_runtime_drift_status(status, severity)`;
- `idx_runtime_drift_type(drift_type)`;
- `idx_runtime_verification_snapshot(snapshot_id, timestamp)`;
- `idx_runtime_fingerprint_release(release_ref, captured_at)`.

## Refresh Model

P0 can expose stored/latest state only. A guarded refresh endpoint can be P1 unless implementation chooses a strictly read-only recompute-on-read helper.

No refresh path may mutate routing or users.

## Implementation Completeness

Runtime Store implementation is defined. Missing build decision: backend and canonical fingerprint source.
