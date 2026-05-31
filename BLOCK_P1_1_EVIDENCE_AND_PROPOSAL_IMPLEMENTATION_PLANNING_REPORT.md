# BLOCK P1.1 Evidence And Proposal Implementation Planning Report

p1_1_completed=true

runtime_mutation_performed=false

evidence_store_implementation_defined=true
evidence_api_implementation_defined=true
evidence_ui_implementation_defined=true
proposal_store_implementation_defined=true
proposal_api_implementation_defined=true
proposal_ui_implementation_defined=true
implementation_order_defined=true
build_ready=true
reality_first_rule_satisfied=true

## Summary

P1.1 converts Evidence Bundle System and Proposal System from product architecture into implementation-ready plans.

The plan targets the current V7 Admin:

- service file: `admin/v7-admin-api`;
- admin route: `/admin-v2`;
- existing read source: `/api/overview`;
- existing UI patterns: drawer, table-shell, pill, workspace tabs.

No new top-level navigation is introduced.

## Reality-First Mapping

Every planned component maps:

```text
Product Capability
-> Admin Surface
-> Runtime Service
-> Storage
-> API
-> UI Component
```

## Evidence Implementation

Defined:

- Evidence Store schema;
- bundle/item/timeline/link relationships;
- indexes;
- retention model;
- lineage model;
- Evidence API contracts;
- EvidenceChip;
- EvidenceDrawer;
- EvidenceTimeline;
- EvidenceSummary.

Read APIs:

- `GET /api/evidence`;
- `GET /api/evidence/{id}`;
- `GET /api/evidence/by-object/{type}/{id}`.

Admin placement:

- `Главная`;
- `Пользователи`;
- `Каналы`;
- `Маршруты`;
- `Проверки`;
- `Безопасность`;
- `Логи`.

## Proposal Implementation

Defined:

- Proposal Store schema;
- mandatory evidence linkage;
- lifecycle/status persistence;
- proposal timeline;
- proposal links;
- Proposal API contracts;
- ProposalCard;
- ProposalStatus;
- ProposalDrawer;
- ProposalTimeline.

Read APIs:

- `GET /api/proposals`;
- `GET /api/proposals/{id}`;
- `GET /api/proposals/by-object/{type}/{id}`.

Admin placement:

- `Главная`;
- `Пользователи`;
- `Каналы`;
- `Маршруты`.

## Implementation Order

P0:

1. Storage adapter.
2. Read APIs.
3. Drawer components.
4. Chips/cards in existing admin sections.
5. Seed/read-only generation from current checks/logs.

P1:

- closure records;
- proposal expiration/supersession;
- search indexes;
- role-gated closure/refresh endpoints;
- proposal-to-batch preparation.

P2:

- evidence correlation;
- multi-target alternatives;
- operator feedback;
- production pool support.

## Build Readiness

build_ready=true

P0 read-only implementation can begin immediately.

## Remaining Blockers

No product-planning blockers remain for read-only P0.

Implementation decisions still required:

- SQLite vs JSONL initial backend;
- exact admin state directory for new store files;
- id format: sortable ids vs UUIDs;
- first writer source: seeded fixtures, checks, logs or manual adapter;
- advanced details role: `admin` or `owner`.

These do not block implementation planning.

## Evidence Files

- `docs/track7/productization/p1_1-evidence/evidence-store-implementation.md`
- `docs/track7/productization/p1_1-evidence/evidence-api-implementation.md`
- `docs/track7/productization/p1_1-evidence/evidence-ui-implementation.md`
- `docs/track7/productization/p1_1-evidence/proposal-store-implementation.md`
- `docs/track7/productization/p1_1-evidence/proposal-api-implementation.md`
- `docs/track7/productization/p1_1-evidence/proposal-ui-implementation.md`
- `docs/track7/productization/p1_1-evidence/implementation-order.md`
- `docs/track7/productization/p1_1-evidence/build-readiness-review.md`
- `docs/track7/productization/p1_1-evidence/tests.md`

## Recommended Next Block

recommended_next_block=P1.2_RUNTIME_AND_RELEASE_TRUST_IMPLEMENTATION_PLANNING

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
