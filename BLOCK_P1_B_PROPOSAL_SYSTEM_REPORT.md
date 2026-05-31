# BLOCK P1.B Proposal System Report

p1_b_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

proposal_system_defined=true

proposal_product_capability_defined=true
proposal_admin_surface_defined=true
proposal_model_defined=true
proposal_lifecycle_defined=true
proposal_storage_defined=true
proposal_api_defined=true
proposal_drawer_defined=true
proposal_governance_integration_defined=true
implementation_backlog_defined=true
implementation_gaps_defined=true
reality_first_rule_satisfied=true

## Summary

P1.B defines Proposal System as the product layer between Evidence Bundle and Governance.

Proposal turns evidence-backed diagnosis into an operator-readable recommendation, but remains non-authoritative.

It may:

- recommend;
- explain;
- prioritize;
- preview.

It may not:

- move users;
- mutate runtime;
- change routing;
- execute autoswitch;
- bypass governance.

## Product Capability

Proposal System supports:

```text
Problem
-> Evidence Bundle
-> Proposal
-> Governance
-> Execution
```

Proposal must not exist without Evidence Bundle.

## Admin Surface

Proposal integrates into existing V7 Admin sections:

- `Главная`;
- `Маршруты`;
- `Пользователи`;
- `Каналы`.

No new top-level navigation is required.

## Proposal Model

Required fields:

- `proposal_id`;
- `proposal_type`;
- `status`;
- `confidence`;
- `severity`;
- `reason`;
- `affected_users`;
- `current_target`;
- `proposed_target`;
- `required_services`;
- `evidence_bundle_id`;
- `expected_benefit`;
- `rollback_hint`;
- `created_at`.

## Lifecycle

Defined states:

- `DRAFT`;
- `OBSERVED`;
- `ACTIVE`;
- `REVIEW_REQUIRED`;
- `EXPIRED`;
- `SUPERSEDED`;
- `CLOSED`.

Expired, superseded or review-required proposals cannot execute without fresh governance.

## Storage/API

Required P0 components:

- Proposal Store;
- proposal timeline;
- evidence linkage;
- object linkage;
- closure records;
- governance references;
- `GET /api/proposals`;
- `GET /api/proposals/{id}`;
- `GET /api/proposals/by-object/{type}/{id}`.

## Proposal Drawer

Proposal Drawer includes:

- summary;
- confidence;
- impact;
- affected users;
- required services;
- evidence link;
- expected benefit;
- rollback hint;
- governance path;
- advanced details.

## Governance Integration

Proposal can enter:

```text
Batch
-> Policy
-> Capacity
-> Concurrency
-> Scheduling
-> Execution-Time Recheck
-> Execution
```

Proposal cannot reserve capacity, lock users, create packet authority or execute movement by itself.

## Implementation Backlog

P0:

- Proposal Store;
- Proposal API;
- Proposal Drawer;
- mandatory Evidence Bundle link;
- proposal chips / row indicators;
- governance path summary;
- expiration/freshness contract.

P1:

- proposal refresh flow;
- closure workflow;
- search;
- batch conversion API;
- required-services integration;
- policy trace integration;
- proposal timeline.

P2:

- correlation;
- multi-target alternatives;
- operator feedback loop;
- production pool proposals;
- optional AI-drafted rationale.

## Gaps

Current missing implementation pieces:

- Proposal Store backend decision;
- Proposal API implementation;
- Proposal Drawer UI;
- proposal writer ownership;
- proposal-to-batch API shape;
- role model for closure/submission.

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

## Evidence Files

- `docs/track7/productization/p1_b-evidence/product-capability.md`
- `docs/track7/productization/p1_b-evidence/admin-surface.md`
- `docs/track7/productization/p1_b-evidence/proposal-model.md`
- `docs/track7/productization/p1_b-evidence/proposal-lifecycle.md`
- `docs/track7/productization/p1_b-evidence/proposal-storage-model.md`
- `docs/track7/productization/p1_b-evidence/proposal-api-model.md`
- `docs/track7/productization/p1_b-evidence/proposal-drawer-model.md`
- `docs/track7/productization/p1_b-evidence/governance-integration.md`
- `docs/track7/productization/p1_b-evidence/implementation-backlog.md`
- `docs/track7/productization/p1_b-evidence/gap-analysis.md`
- `docs/track7/productization/p1_b-evidence/tests.md`
- `docs/track7/productization/p1_b-evidence/final-model-decision.md`

## Recommended Next Block

recommended_next_block=P1.C_RUNTIME_CONVERGENCE_SURFACE

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
