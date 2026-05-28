# E18 Audit Search And Evidence Hardening Review

## Purpose

E18 hardens the E17 lineage archive into a more discoverable read-only operator
audit surface. The goal is not runtime execution; it is safer discovery,
evidence detail, stale/conflict labeling, and audit-grade navigation.

## Implemented Read Models

| Object | Purpose |
|---|---|
| `AuditSearchResult` | Unified search result across operation lineage and evidence records. |
| `EvidenceArchive` | Indexed report/evidence file metadata with stable evidence ids. |
| `EvidenceFileDetail` | Safe redacted excerpt and metadata for a single evidence item. |
| `conflict_warnings` | Highlights contradictory archive states such as delayed movement under a safe-looking state. |
| `stale_warnings` | Keeps report/evidence-backed data labeled historical instead of live. |

## Safety Hardening

- Evidence detail is restricted to repository-local indexed evidence ids.
- Evidence file excerpts are limited by suffix and size.
- Large or non-text files are labeled `PARTIAL`.
- Secret-like lines are redacted from excerpts.
- Search indexes normalized text but does not expose raw unbounded evidence.
- Unknown evidence ids return `evidence_not_found`.

## UI Additions

- Audit search input inside the Operator timeline section.
- Operation type filter.
- Operation state filter.
- Evidence kind filter.
- Evidence result cards with metadata and warning badges.
- Evidence detail drawer with metadata, path, warnings, and safe excerpt.

## Endpoint Additions

- `GET /api/operator/audit-search`
- `GET /api/operator/evidence-archive`
- `GET /api/operator/evidence-file-detail?id=...`

All endpoints return read-only data and keep `execution_allowed_now=false`.

## Hardening Verdict

The operator archive now behaves like a governed operational archive rather
than scattered evidence folders. It remains strictly read-only and does not add
execution or mutation capability.

