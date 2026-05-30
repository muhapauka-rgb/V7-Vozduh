# P1.A Gap Analysis

implementation_gaps_defined=true

## Missing APIs

- `GET /api/evidence`
- `GET /api/evidence/{id}`
- `GET /api/evidence/by-object/{type}/{id}`
- Optional future closure/annotation endpoints with audit.

## Missing Storage

- Evidence Bundle Store.
- Evidence item summary store.
- Evidence timeline store.
- Evidence linkage index.
- Evidence closure record store.
- Evidence retention/archival policy.

## Missing UI

- Shared Evidence Drawer.
- Evidence link chips in user/channel/route/check/log rows.
- Evidence timeline component.
- Verification and closure sections.
- Role-gated advanced detail panel.

## Missing Integrations

- Checks to evidence bundles.
- Logs to evidence bundles.
- User required-service issues to evidence bundles.
- Channel readiness/service matrix to evidence bundles.
- Route reality and routing recommendations to evidence bundles.
- Proposal System to evidence bundles.
- Release/backup/restore verification to evidence bundles.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- initial Evidence Store backend: file-backed, SQLite, or existing admin DB
- first writer source: checks, logs, proposals, or all through adapter
- closure mutation endpoint scope and required role
- raw payload retention and redaction policy
- whether evidence ids are time-sortable ids or UUIDs
```

## Gap Verdict

The current architecture has enough definition to start implementation, but P0 requires a real storage/API/UI slice before evidence can become visible in admin.

