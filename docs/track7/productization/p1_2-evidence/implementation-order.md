# P1.2 Implementation Order

implementation_order_defined=true

## P0 — Required Build Slice

### Stores

1. Runtime Convergence Store.
2. Release Trust Store.
3. Shared trust/evidence linkage helpers.

### APIs

1. `GET /api/runtime/convergence`
2. `GET /api/runtime/fingerprint`
3. `GET /api/runtime/drift`
4. `GET /api/release/current`
5. `GET /api/release/history`
6. `GET /api/release/{id}`

### UI

1. RuntimeTrustStatus.
2. RuntimeTrustDrawer.
3. DriftComponent.
4. ReleaseTrustStatus.
5. ReleaseDrawer.
6. RollbackAvailability.
7. Placement in:
   - `Главная`;
   - `Проверки`;
   - `Безопасность`.

## P1 — Production Hardening

- guarded trust refresh flows;
- release verification refresh;
- drift closure workflow;
- release history search;
- runtime/release blocker display in proposal/batch surfaces;
- advanced details role gating.

## P2 — Future

- multi-node runtime/release trust;
- drift diff viewer;
- release comparison drawer;
- trust trend alerts;
- installer/deployment integration.

## Recommended Build Sequence

```text
1. Define canonical runtime/release snapshot adapters
2. Add stores
3. Add read APIs
4. Add status components to Главная
5. Add drawers
6. Add Проверки and Безопасность placements
7. Wire Evidence links
8. Add guarded refresh/closure later
```

## Implementation Order Verdict

Build should start with read-only trust visibility before refresh, reconciliation or recovery actions.
