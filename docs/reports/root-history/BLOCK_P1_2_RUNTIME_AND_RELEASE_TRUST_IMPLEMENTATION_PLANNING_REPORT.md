# BLOCK P1.2 Runtime And Release Trust Implementation Planning Report

p1_2_completed=true

runtime_mutation_performed=false

runtime_store_implementation_defined=true
runtime_api_implementation_defined=true
runtime_ui_implementation_defined=true
release_store_implementation_defined=true
release_api_implementation_defined=true
release_ui_implementation_defined=true
trust_chain_defined=true
implementation_order_defined=true
build_ready=true
reality_first_rule_satisfied=true

## Summary

P1.2 converts Runtime Trust and Release Trust from architecture into implementation-ready plans.

The plan targets the current V7 Admin:

- service file: `admin/v7-admin-api`;
- admin route: `/admin-v2`;
- existing UI patterns: drawer, panel, pill, status strip, checks/security surfaces.

No new top-level navigation is introduced.

## Runtime Trust Implementation

Defined:

- Runtime Convergence Store;
- runtime status storage;
- fingerprint storage;
- drift storage;
- verification history;
- lineage references;
- RuntimeTrustStatus;
- RuntimeTrustDrawer;
- DriftComponent;
- VerificationHistoryView.

Read APIs:

- `GET /api/runtime/convergence`;
- `GET /api/runtime/fingerprint`;
- `GET /api/runtime/drift`.

Admin placement:

- `Главная`;
- `Проверки`;
- `Безопасность`.

## Release Trust Implementation

Defined:

- Release Trust Store;
- release summary;
- release lineage;
- rollback lineage;
- verification history;
- certification state;
- ReleaseTrustStatus;
- ReleaseDrawer;
- ReleaseHistory;
- RollbackAvailability.

Read APIs:

- `GET /api/release/current`;
- `GET /api/release/history`;
- `GET /api/release/{id}`.

Admin placement:

- `Главная`;
- `Проверки`;
- `Безопасность`.

## Trust Chain

Defined chain:

```text
Problem
-> Evidence
-> Proposal
-> Runtime Trust
-> Release Trust
```

Runtime and release trust states must fail closed for forward action when unknown, drifted or blocking.

## Implementation Order

P0:

1. Runtime Convergence Store.
2. Release Trust Store.
3. Runtime read APIs.
4. Release read APIs.
5. RuntimeTrustStatus and ReleaseTrustStatus on `Главная`.
6. RuntimeTrustDrawer and ReleaseDrawer.
7. `Проверки` and `Безопасность` placements.

P1:

- guarded trust refresh flows;
- release verification refresh;
- drift closure workflow;
- release history search;
- proposal/batch blocker display.

P2:

- multi-node trust;
- drift diff viewer;
- release comparison drawer;
- trust trend alerts;
- installer/deployment integration.

## Build Readiness

build_ready=true

P0 read-only implementation can begin immediately.

## Remaining Blockers

No product-planning blockers remain for read-only P0.

Implementation decisions still required:

- canonical runtime fingerprint source;
- canonical release identity source;
- SQLite vs JSONL backend;
- runtime convergence TTL;
- release verification TTL;
- advanced details role.

## Evidence Files

- `docs/track7/productization/p1_2-evidence/runtime-store-implementation.md`
- `docs/track7/productization/p1_2-evidence/runtime-api-implementation.md`
- `docs/track7/productization/p1_2-evidence/runtime-ui-implementation.md`
- `docs/track7/productization/p1_2-evidence/release-store-implementation.md`
- `docs/track7/productization/p1_2-evidence/release-api-implementation.md`
- `docs/track7/productization/p1_2-evidence/release-ui-implementation.md`
- `docs/track7/productization/p1_2-evidence/trust-chain-integration.md`
- `docs/track7/productization/p1_2-evidence/implementation-order.md`
- `docs/track7/productization/p1_2-evidence/build-readiness-review.md`
- `docs/track7/productization/p1_2-evidence/tests.md`

## Recommended Next Block

recommended_next_block=P1_3_IMPLEMENTATION_ROADMAP_AND_BUILD_SEQUENCE

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
