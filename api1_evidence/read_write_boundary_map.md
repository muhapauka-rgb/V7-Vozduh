# API.1 Read/Write Boundary Map

Generated source: `api1_evidence/endpoint_boundary_map.json`.

## Boundary Counts

| Boundary | Count | Meaning |
|---|---:|---|
| READ | 62 | JSON/API read endpoints with no direct mutation classification |
| UI | 19 | pages, redirects, public delivery and UI authority |
| ACTION | 130 | operator/admin POST actions; may include dry-run/preview |
| WRITE | 2 | direct write/config update surfaces not otherwise classified |
| EXECUTION | 38 | endpoints that can launch or prepare runtime execution |
| GOVERNANCE | 7 | approval/governance/control-plane semantics |
| ROLLBACK | 6 | rollback preview or apply semantics |

## Safe Read-Only Area

Read-only extraction candidates may include:

- GET endpoint payload builders;
- registry readers and redacted row serializers;
- event list builders;
- audit search/export preview builders;
- operator evidence/detail serializers;
- overview sub-summaries after snapshot tests;
- service matrix and route-class summaries;
- preview result formatting when preview execution remains in the monolith.

## Action Area

Action endpoints are POST routes under `/api/actions/*`. The inventory reports:

- 138 POST endpoints total;
- 133 action-family endpoints;
- 133 CSRF-required endpoints;
- 86 safe-mode-blocked endpoints.

The action area must remain inside `Handler.do_POST` until API contracts cover:

- auth response behavior;
- CSRF failure behavior;
- role checks;
- safe-mode behavior;
- confirmation strings;
- audit output;
- command invocation;
- response schemas.

## Execution Area

Execution-class endpoints include user switch, autoswitch apply/dry-run, egress state apply, proxy runtime guard, public proxy enable/disable, trusted RU diagnostics, and service-aware apply/preview operations.

Extraction rule:

- read-only execution packet/detail views may move;
- command execution and apply routes must not move first;
- planner/runtime tools stay authoritative.

## Governance Area

Governance endpoints and builders are tied to operator approval, packet/evidence lineage, and execution rehearsal. They may be decomposed only as read-only serializers over the existing `admin_core.operator_execution` and `admin_core.operator_observability` models.

Extraction rule:

- preview and evidence views can move first;
- approval mutation and governance state writes cannot move first.

## Rollback Area

Rollback surfaces are high-risk because a response-shape or command-argument change can affect recovery. Only rollback preview read models are candidates for early extraction.

Extraction rule:

- no rollback apply handler extraction until action contracts and live dry-run smoke tests are complete.

## UI Area

`html_page_v2` is the largest single function, but it should not be the first extraction target. It is coupled to endpoint shapes, action names, confirmation flows, drawer state, and operator workflows.

Extraction rule:

- first freeze API contracts;
- then split static assets/templates;
- then split page rendering;
- do not create a second admin surface.

## Boundary Verdict

The read/write boundary map is complete enough for API.2. API.2 should be scoped to READ/UI-adjacent serializers only, with no mutation or runtime behavior changes.
