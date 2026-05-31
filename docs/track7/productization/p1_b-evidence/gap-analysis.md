# P1.B Gap Analysis

implementation_gaps_defined=true

## Missing APIs

- `GET /api/proposals`
- `GET /api/proposals/{id}`
- `GET /api/proposals/by-object/{type}/{id}`
- Future role-gated proposal refresh/close/submit endpoints.

## Missing Storage

- Proposal Store.
- Proposal timeline store.
- Proposal evidence linkage store.
- Proposal object linkage index.
- Proposal closure record store.
- Governance reference linkage.

## Missing UI

- Proposal Drawer.
- Proposal chips in overview/user/channel/route surfaces.
- Proposal status and confidence display.
- Required-services proposal section.
- Governance path preview.
- Proposal timeline.

## Missing Integrations

- Evidence Bundle required link.
- Routing Intelligence proposal writer.
- Required Services and service matrix.
- Capacity model and target eligibility.
- Policy admission trace.
- Execution Batch conversion.
- Logs/audit lineage.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- initial Proposal Store backend: file-backed, SQLite, or existing admin DB
- proposal id format and TTL defaults
- which subsystem creates first proposals: routing intelligence, checks, or manual operator review
- exact role required to close or submit proposal to governance
- proposal-to-batch API shape
- whether multi-target alternatives are P1 or P2
```

## Gap Verdict

Proposal architecture is defined enough to implement P0, but storage/API/UI integration and proposal writer ownership must be decided before code implementation.
