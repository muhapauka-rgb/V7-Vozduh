# V7 Phase 0 Legacy Map

Purpose: identify legacy and archive candidates without deleting or moving them during Phase 0.

## Stable Legacy

These areas are legacy-shaped but still useful and should not be removed:

- `V7_ADMIN_PHASE21_*` through `V7_ADMIN_PHASE26_*`
- `V7_PHASE27_30_*` through `V7_PHASE34_*`
- `V7_MASTER_PLAN.md`
- `V7_PROVISIONING_ARCHITECTURE.md`
- `V7_DIRECT_RU_ROUTING.md`
- `V7_TRUSTED_RU_EGRESS_PLAN.md`
- `V7_DATAPATH_OPTIMIZER_PLAN.md`

Reason: they encode decisions, validation history, and production lessons. They should eventually move to `docs/archive/phase-reports/`, but only after links and references are updated.

## Design Legacy

Candidates:

- `design/v7-admin-alternative-dashboard.html`
- `design/v7-admin-live-7080-current.html`
- `design/v7-admin-page-export.html`
- `design/v7-admin-working-current.html`
- `design/Norm*` copies with Russian filenames

Classification: design snapshots and prototypes.

Archive strategy:

- Keep in place for now.
- Later move to `legacy/design_snapshots/` or `docs/design/archive/`.
- Preserve at least one canonical current snapshot before moving copies.

## Test Artifact Legacy

Candidates:

- `artifacts/awg-client-test/*`
- `artifacts/wg-client-test/*`
- `test-results/.last-run.json`

Classification: test artifacts, not runtime source.

Archive strategy:

- Keep during Phase 0.
- Later move generated artifacts out of source or mark as fixture/testdata explicitly.

## Operational Legacy That Must Not Move Yet

Candidates:

- `admin/v7-admin-api`
- current `tools/*`
- current `hardening/*`
- current `systemd/*`

Reason: production install scripts and operator muscle memory may depend on current paths and names. Moving them without wrappers would violate compatibility-first governance.

## Do Not Delete

No legacy area should be deleted in Phase 0.

Deletion requires:

- proof it is unused;
- rollback plan;
- compatibility impact analysis;
- operator-visible migration note.

