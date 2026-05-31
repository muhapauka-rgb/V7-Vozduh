# P1.2 Release Trust Store Implementation

release_store_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: prove release identity, certification and rollback availability
Operator Meaning: current release certified, rollback available, attention required
Admin Surface: Главная, Проверки, Безопасность
Runtime Service: release trust helpers in admin/v7-admin-api, read-only by default
Storage: Release Trust Store
API: GET /api/release/current, GET /api/release/history, GET /api/release/{id}
UI Component: ReleaseTrustStatus, ReleaseDrawer, ReleaseHistory, RollbackAvailability
```

## Storage Schema

### `release_summaries`

| Column | Type | Notes |
| --- | --- | --- |
| `release_id` | text primary key | Stable release id. |
| `label` | text not null | Operator label. |
| `status` | text not null | `RELEASE_OK`, `RELEASE_WARNING`, `RELEASE_UNKNOWN`, `RELEASE_DRIFT`, `RELEASE_BLOCKING`. |
| `certified` | integer | 0/1/null. |
| `runtime_match` | integer | 0/1/null. |
| `rollback_available` | integer | 0/1/null. |
| `certification_state` | text | `certified`, `warning`, `unknown`, `expired`, `blocked`. |
| `evidence_bundle_id` | text | Evidence link. |
| `created_at` | text | ISO timestamp. |
| `verified_at` | text | ISO timestamp. |
| `expires_at` | text | Freshness expiry. |

### `release_lineage_events`

| Column | Type | Notes |
| --- | --- | --- |
| `event_id` | text primary key | Stable event id. |
| `previous_release_id` | text | Nullable. |
| `release_id` | text not null | Current release. |
| `event_type` | text not null | `created`, `deployed`, `verified`, `rollback_target_set`, `superseded`. |
| `timestamp` | text not null | ISO timestamp. |
| `actor` | text | Source/operator/system. |
| `summary` | text not null | Operator-readable. |
| `audit_ref` | text | Optional. |
| `evidence_bundle_id` | text | Evidence link. |

### `rollback_lineage_records`

| Column | Type | Notes |
| --- | --- | --- |
| `rollback_id` | text primary key | Stable rollback lineage id. |
| `release_id` | text not null | Release this rollback supports. |
| `rollback_target_release_id` | text | Target release. |
| `backup_ref` | text | Backup/restore ref. |
| `status` | text not null | `available`, `unknown`, `blocked`, `expired`. |
| `verification_state` | text | Summary state. |
| `summary` | text not null | Operator-readable. |
| `evidence_bundle_id` | text | Evidence link. |
| `updated_at` | text not null | ISO timestamp. |

### `release_verification_events`

| Column | Type | Notes |
| --- | --- | --- |
| `event_id` | text primary key | Stable event id. |
| `release_id` | text not null | Release id. |
| `timestamp` | text not null | ISO timestamp. |
| `source` | text not null | checker/helper/operator. |
| `result` | text not null | `OK`, `WARN`, `UNKNOWN`, `DRIFT`, `BLOCKED`. |
| `runtime_snapshot_id` | text | Runtime convergence ref. |
| `summary` | text not null | Operator-readable. |
| `evidence_bundle_id` | text | Evidence link. |

## Indexes

- `idx_release_status(status, verified_at)`;
- `idx_release_certified(certified, expires_at)`;
- `idx_release_lineage_release(release_id, timestamp)`;
- `idx_rollback_release(release_id, status)`;
- `idx_release_verification_release(release_id, timestamp)`.

## Certification State

Certification state persists independently of runtime match. A release can be certified but runtime can drift away from it.

## Implementation Completeness

Release Store implementation is defined. Missing build decision: canonical release identity source.
