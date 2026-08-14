# BLOCK P1.A Evidence Bundle System Report

p1_a_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

evidence_bundle_system_defined=true

evidence_product_capability_defined=true
evidence_admin_surface_defined=true
evidence_model_defined=true
evidence_linkage_defined=true
evidence_storage_defined=true
evidence_api_defined=true
evidence_drawer_defined=true
implementation_backlog_defined=true
implementation_gaps_defined=true
reality_first_rule_satisfied=true

## Summary

P1.A defines the Evidence Bundle System as the first real product implementation package after the E32-E34 architecture work.

Evidence bundles turn scattered logs, checks, snapshots, probe outputs, audit records and diagnosis notes into one operator-readable proof package.

The system supports:

```text
Problem
-> Evidence
-> Diagnosis
-> Action
-> Verification
-> Closure
```

## Product Capability

Evidence bundles provide the proof layer for:

- Proposal System;
- Release Verification;
- Recovery Verification;
- Operator Runbooks;
- checks and diagnostics;
- user/channel/route investigation.

Evidence is descriptive and auditable. It is not an execution authority.

## Admin Surface

Evidence integrates into existing V7 Admin sections:

- `Главная`;
- `Проверки`;
- `Логи`;
- `Пользователи`;
- `Каналы`;
- `Маршруты`.

No new top-level navigation is required. Evidence opens through chips, links and drawers inside existing workflows.

## Model

An evidence bundle includes:

- `bundle_id`;
- `object_type`;
- `object_id`;
- `status`;
- `severity`;
- `summary`;
- `timeline`;
- `evidence_items`;
- `recommendation`;
- `verification_state`;
- `closure_state`.

## Linkage

Supported linkage:

- User;
- Channel;
- Proposal;
- Alert;
- Route;
- Release;
- Backup;
- Restore.

## Storage/API

Required P0 components:

- Evidence Bundle Store;
- Evidence linkage index;
- Evidence timeline and item summary store;
- `GET /api/evidence`;
- `GET /api/evidence/{id}`;
- `GET /api/evidence/by-object/{type}/{id}`;
- redaction and role-gated advanced detail rules.

## Drawer

Evidence Drawer includes:

- summary;
- timeline;
- evidence items;
- recommended action;
- verification;
- closure;
- advanced details.

## Implementation Backlog

P0:

- Evidence Bundle Store;
- Evidence Bundle API;
- Evidence Drawer Component;
- Evidence Link Chips;
- Redaction Contract;
- Source Reference Contract;
- existing-admin integration.

P1:

- Closure Workflow;
- Evidence Search;
- Proposal Integration;
- Recovery Integration;
- Release Verification Integration;
- Evidence Retention Policy;
- Role-Gated Advanced Details.

P2:

- evidence correlation;
- sanitized export;
- evidence diff;
- multi-node federation;
- optional AI-assisted diagnosis drafts.

## Gaps

Current missing implementation pieces:

- Evidence Store backend decision;
- Evidence API implementation;
- Evidence Drawer UI;
- evidence writers/adapters from checks, logs, proposals and recovery;
- retention and redaction policy details.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- initial Evidence Store backend: file-backed, SQLite, or existing admin DB
- first writer source: checks, logs, proposals, or all through adapter
- closure mutation endpoint scope and required role
- raw payload retention and redaction policy
- whether evidence ids are time-sortable ids or UUIDs
```

## Evidence Files

- `docs/track7/productization/p1_a-evidence/product-capability.md`
- `docs/track7/productization/p1_a-evidence/admin-surface.md`
- `docs/track7/productization/p1_a-evidence/evidence-model.md`
- `docs/track7/productization/p1_a-evidence/evidence-linkage-model.md`
- `docs/track7/productization/p1_a-evidence/evidence-storage-model.md`
- `docs/track7/productization/p1_a-evidence/evidence-api-model.md`
- `docs/track7/productization/p1_a-evidence/evidence-drawer-model.md`
- `docs/track7/productization/p1_a-evidence/implementation-backlog.md`
- `docs/track7/productization/p1_a-evidence/gap-analysis.md`
- `docs/track7/productization/p1_a-evidence/tests.md`
- `docs/track7/productization/p1_a-evidence/final-model-decision.md`

## Recommended Next Block

recommended_next_block=P1.B_PROPOSAL_SYSTEM

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

