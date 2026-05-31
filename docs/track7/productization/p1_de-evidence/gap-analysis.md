# P1.D/E Gap Analysis

implementation_gaps_defined=true

## Missing APIs

- `GET /api/release/current`
- `GET /api/release/history`
- `GET /api/release/{id}`
- Future release verification refresh endpoint.
- Future drift/release correlation endpoint.

## Missing Storage

- Release Trust Store.
- Release summary store.
- Release certification store.
- Release lineage store.
- Rollback lineage store.
- Release verification history.

## Missing UI

- Release trust status component.
- Release Drawer.
- Rollback availability display.
- Runtime/release match display.
- Release verification history.
- Role-gated advanced provenance details.

## Missing Integrations

- Runtime Convergence Surface.
- Evidence Bundle System.
- Backup/Restore surfaces.
- Security overview.
- Checks/readiness surface.
- Future installer/deployment state.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- canonical release identity source
- initial Release Trust Store backend
- release verification TTL and staleness threshold
- role required for advanced provenance details
- role required to refresh release verification
- rollback availability definition for first implementation
```

## Gap Verdict

Release Trust Surface is defined enough for P0 implementation, but needs canonical release identity, storage backend and verification freshness decisions.
