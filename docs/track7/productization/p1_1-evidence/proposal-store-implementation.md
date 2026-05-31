# P1.1 Proposal Store Implementation

proposal_store_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: durable evidence-backed recommendations
Admin Surface: proposal cards/chips/drawers in Главная, Пользователи, Каналы, Маршруты
Runtime Service: read/write proposal helper inside admin/v7-admin-api, no runtime mutation
Storage: Proposal Store tables or adapter
API: GET /api/proposals endpoints
UI Component: ProposalCard, ProposalDrawer, ProposalTimeline, ProposalStatus
```

## Storage Schema

### `proposals`

| Column | Type | Notes |
| --- | --- | --- |
| `proposal_id` | text primary key | Stable id. |
| `proposal_type` | text not null | `USER_MOVEMENT`, `BATCH_MOVEMENT`, `CHANNEL_AVOIDANCE`, etc. |
| `status` | text not null | `DRAFT`, `OBSERVED`, `ACTIVE`, `REVIEW_REQUIRED`, `EXPIRED`, `SUPERSEDED`, `CLOSED`. |
| `confidence` | text not null | `LOW`, `MEDIUM`, `HIGH`, `VERY_HIGH`. |
| `severity` | text not null | `ok`, `info`, `warn`, `bad`, `muted`. |
| `reason` | text not null | Operator-readable reason. |
| `affected_users_json` | text | JSON array. |
| `current_target` | text | Nullable. |
| `proposed_target` | text | Nullable. |
| `required_services_json` | text | JSON array. |
| `evidence_bundle_id` | text not null | Required evidence link. |
| `expected_benefit_json` | text | JSON object. |
| `rollback_hint_json` | text | JSON object. |
| `governance_ref_json` | text | JSON object or null. |
| `expires_at` | text | ISO timestamp. |
| `created_at` | text not null | ISO timestamp. |
| `updated_at` | text not null | ISO timestamp. |

### `proposal_timeline`

| Column | Type | Notes |
| --- | --- | --- |
| `event_id` | text primary key | Stable id. |
| `proposal_id` | text not null | FK to proposal. |
| `timestamp` | text not null | ISO timestamp. |
| `actor` | text | system/operator/source. |
| `event_type` | text not null | created, observed, activated, reviewed, expired, superseded, closed. |
| `summary` | text not null | Operator-readable. |
| `evidence_bundle_id` | text | Optional supporting evidence. |
| `audit_ref` | text | Optional. |

### `proposal_links`

| Column | Type | Notes |
| --- | --- | --- |
| `proposal_id` | text not null | FK to proposal. |
| `object_type` | text not null | user, channel, route, evidence, batch. |
| `object_id` | text not null | Linked id. |
| `relationship` | text not null | primary, affected, target, source, governance. |
| `display_label` | text | Admin label. |
| `created_at` | text not null | ISO timestamp. |

## Evidence Linkage

`evidence_bundle_id` is mandatory.

Proposal creation must fail if referenced evidence bundle does not exist.

## Lifecycle Persistence

Every lifecycle transition must:

- update `proposals.status`;
- append `proposal_timeline`;
- preserve previous state through timeline;
- never delete active lineage.

## Status Persistence

Expired and superseded proposals remain queryable for history. They are not actionable.

## Indexes

- `idx_proposal_status(status, severity)`;
- `idx_proposal_type(proposal_type)`;
- `idx_proposal_confidence(confidence)`;
- `idx_proposal_evidence(evidence_bundle_id)`;
- `idx_proposal_updated(updated_at)`;
- `idx_proposal_link_object(object_type, object_id)`;
- `idx_proposal_expires(expires_at)`.

## Implementation Completeness

Store plan is implementation-ready. Missing decision: initial backend should match Evidence Store backend.
