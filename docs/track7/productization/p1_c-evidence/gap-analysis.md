# P1.C Gap Analysis

implementation_gaps_defined=true

## Missing APIs

- `GET /api/runtime/convergence`
- `GET /api/runtime/fingerprint`
- `GET /api/runtime/drift`
- Future role-gated verification refresh endpoint.
- Future drift closure endpoint.

## Missing Storage

- Runtime Convergence Store.
- Fingerprint summary store.
- Drift record store.
- Verification history store.
- Lineage reference store.
- Drift closure records.

## Missing UI

- Runtime trust status component.
- Runtime Convergence Drawer.
- Drift summary row/card.
- Verification history section.
- Release match indicator.
- Runtime trust blocker display in proposal/batch surfaces.

## Missing Integrations

- Evidence Bundle linkage.
- Release/provenance expected identity.
- Backup/restore verification.
- Governance gate display.
- Checks/readiness map display.
- Security overview trust indicator.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- canonical runtime fingerprint source
- runtime convergence TTL and staleness threshold
- initial storage backend for convergence snapshots
- role required for advanced fingerprint/drift details
- role required to close known intentional drift
- whether verification refresh is P0 or P1
```

## Gap Verdict

Runtime Convergence Surface is defined enough for P0, but implementation requires choosing a fingerprint source, storage backend and freshness policy.
