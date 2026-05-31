# P1.1 Implementation Order

implementation_order_defined=true

## P0 — Required Build Slice

### Stores

1. Add Evidence Store schema/adapter.
2. Add Proposal Store schema/adapter using the same backend.
3. Add lightweight seed/dev fixtures for empty-state UI.

### Services

1. Add Evidence Store helper functions.
2. Add Proposal Store helper functions.
3. Add object-link lookup helpers.
4. Add redaction/visibility helper.

### APIs

1. `GET /api/evidence`
2. `GET /api/evidence/{id}`
3. `GET /api/evidence/by-object/{type}/{id}`
4. `GET /api/proposals`
5. `GET /api/proposals/{id}`
6. `GET /api/proposals/by-object/{type}/{id}`

### UI

1. EvidenceChip.
2. EvidenceDrawer.
3. ProposalStatus.
4. ProposalDrawer.
5. Section placements:
   - `Главная`;
   - `Пользователи`;
   - `Каналы`;
   - `Маршруты`;
   - `Проверки`;
   - `Логи`.

## P1 — Production Hardening

### Stores

- retention job;
- closure records;
- proposal expiration/supersession;
- evidence/proposal search indexes.

### APIs

- role-gated closure endpoints;
- proposal refresh endpoint;
- proposal-to-batch preparation endpoint;
- evidence export endpoint.

### UI

- closure workflow;
- advanced details role gating;
- search/filter surfaces;
- proposal governance-path preview.

## P2 — Future

- evidence correlation;
- multi-target proposal alternatives;
- operator feedback loop;
- production pool proposal support;
- multi-node evidence/proposal federation.

## Recommended Build Sequence

```text
1. Storage adapter
2. Read APIs
3. Drawer components
4. Chips/cards in existing admin sections
5. Seed/read-only generation from current checks/logs
6. Closure/refresh/governance submission later
```

## Implementation Order Verdict

Build should start with read-only store/API/UI. Mutation workflows come only after operators can see and trust evidence/proposals.
