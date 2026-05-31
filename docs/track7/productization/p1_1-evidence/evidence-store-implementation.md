# P1.1 Evidence Store Implementation

evidence_store_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: durable proof bundles for checks, logs, users, channels, routes and future proposals
Admin Surface: chips/drawers in Главная, Пользователи, Каналы, Маршруты, Проверки, Безопасность, Логи
Runtime Service: read/write helper inside admin/v7-admin-api, no runtime mutation
Storage: SQLite/file-backed evidence tables under admin state storage
API: GET /api/evidence, GET /api/evidence/{id}, GET /api/evidence/by-object/{type}/{id}
UI Component: EvidenceChip, EvidenceDrawer, EvidenceTimeline, EvidenceSummary
```

## Implementation Location

Initial implementation should live in the current runtime admin service:

- source: `admin/v7-admin-api`;
- route style: existing `elif path == "/api/..."` handler;
- auth model: existing role/action access helpers;
- frontend surface: existing `/admin-v2` script and drawer patterns.

## Storage Schema

Recommended first implementation: SQLite tables in the existing admin state area. If the current admin database is unavailable, use a file-backed JSONL adapter with the same logical fields and a migration path.

### `evidence_bundles`

| Column | Type | Notes |
| --- | --- | --- |
| `bundle_id` | text primary key | Stable id, preferably sortable. |
| `object_type` | text not null | Primary linked object type. |
| `object_id` | text not null | Primary linked object id. |
| `status` | text not null | `open`, `investigating`, `action_ready`, `verifying`, `closed`, `failed_closed`. |
| `severity` | text not null | `ok`, `info`, `warn`, `bad`, `muted`. |
| `summary_title` | text not null | Drawer/table title. |
| `operator_meaning` | text | Human summary. |
| `current_diagnosis` | text | Diagnosis code/label. |
| `recommendation_json` | text | JSON object, nullable. |
| `verification_json` | text | JSON object. |
| `closure_json` | text | JSON object. |
| `created_at` | text not null | ISO timestamp. |
| `updated_at` | text not null | ISO timestamp. |

### `evidence_items`

| Column | Type | Notes |
| --- | --- | --- |
| `item_id` | text primary key | Stable item id. |
| `bundle_id` | text not null | FK to bundle. |
| `source` | text not null | `check`, `log`, `proposal`, `release`, `backup`, etc. |
| `source_ref` | text | Source id/path/ref. |
| `type` | text not null | `check_result`, `log_event`, `snapshot`, `probe`, `audit`, `summary`. |
| `status` | text not null | Source-specific status normalized to ok/warn/bad/info/muted. |
| `summary` | text not null | Operator-readable line. |
| `payload_ref` | text | Raw payload reference, never inline secrets. |
| `payload_hash` | text | Optional immutable hash. |
| `redaction_state` | text not null | `redacted`, `safe`, `restricted`. |
| `operator_visibility` | text not null | `default`, `advanced`, `restricted`. |
| `trust_level` | text | `low`, `medium`, `high`, `verified`. |
| `captured_at` | text not null | ISO timestamp. |

### `evidence_timeline`

| Column | Type | Notes |
| --- | --- | --- |
| `event_id` | text primary key | Stable timeline id. |
| `bundle_id` | text not null | FK to bundle. |
| `timestamp` | text not null | ISO timestamp. |
| `actor` | text | `system`, `operator`, `checker`, service id. |
| `event_type` | text not null | `detected`, `checked`, `diagnosed`, `recommended`, `verified`, `closed`. |
| `summary` | text not null | Operator-readable line. |
| `linked_item_ids_json` | text | JSON array. |
| `audit_ref` | text | Optional audit reference. |

### `evidence_links`

| Column | Type | Notes |
| --- | --- | --- |
| `bundle_id` | text not null | FK to bundle. |
| `object_type` | text not null | User, Channel, Proposal, Alert, Route, Release, Backup, Restore. |
| `object_id` | text not null | Linked object id. |
| `relationship` | text not null | `primary`, `related`, `source`, `verification`, `closure`. |
| `display_label` | text | Admin label. |
| `admin_surface` | text | Section where link appears. |
| `created_at` | text not null | ISO timestamp. |

## Object Relationships

```text
evidence_bundles 1 -> many evidence_items
evidence_bundles 1 -> many evidence_timeline
evidence_bundles 1 -> many evidence_links
evidence_links many -> one domain object
```

## Indexes

Required indexes:

- `idx_evidence_bundle_object(object_type, object_id)`;
- `idx_evidence_bundle_status(status, severity)`;
- `idx_evidence_bundle_updated(updated_at)`;
- `idx_evidence_item_bundle(bundle_id)`;
- `idx_evidence_item_source(source, source_ref)`;
- `idx_evidence_timeline_bundle_time(bundle_id, timestamp)`;
- `idx_evidence_link_object(object_type, object_id)`.

## Retention Model

Default retention:

- open/failed-closed bundles: retain until closed plus retention period;
- closed operational bundles: 180 days;
- release/backup/restore/security bundles: 365 days minimum;
- raw payload refs: can expire earlier if summary, hash and redaction metadata remain.

## Lineage Model

Every bundle must preserve:

- creation source;
- linked source refs;
- timeline ordering;
- item hashes when available;
- audit references;
- closure event.

Payload refs and hashes are append-only. Bundle status and summary can change only with timeline events.

## Implementation Completeness

Complete for planning. Build can start after choosing initial backend: SQLite preferred for query/index support.
