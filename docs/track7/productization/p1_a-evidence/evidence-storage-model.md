# P1.A Evidence Storage Model

evidence_storage_defined=true

## Storage Ownership

Evidence Store owns evidence bundle metadata, linkage, timeline and redacted item summaries.

Raw artifacts can be stored by their native subsystem and referenced by immutable `payload_ref` values.

## Storage Objects

Minimum storage entities:

- `evidence_bundles`;
- `evidence_items`;
- `evidence_timeline_events`;
- `evidence_links`;
- `evidence_payload_refs`;
- `evidence_closure_records`.

## Retention

Recommended retention:

| Evidence type | Retention |
| --- | --- |
| open or failed-closed bundles | until explicit closure plus policy retention |
| closed operational bundles | 180 days minimum |
| release/backup/restore bundles | match release and backup retention |
| security/incident bundles | 365 days minimum |
| raw volatile probe payloads | shorter retention allowed if summary and hash remain |

## Searchability

Search must cover:

- bundle id;
- object id;
- IP/user;
- channel/target;
- status;
- severity;
- source;
- tags;
- time range;
- diagnosis;
- recommendation state.

## Lineage

Every bundle must preserve:

- creation source;
- source references;
- timeline ordering;
- audit references when available;
- item hashes for immutable artifacts;
- redaction state.

## Immutability Rules

Evidence item payload references and hashes are append-only.

Mutable fields are limited to:

- bundle status;
- summary refinement;
- recommendation status;
- verification state;
- closure state;
- labels/tags.

Mutable fields must record a timeline event.

## Storage Verdict

Evidence storage is a product data store, not a runtime registry. It must be searchable and auditable while keeping raw secrets redacted or externally referenced.

