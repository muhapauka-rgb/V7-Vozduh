# API.1 Safe Decomposition Plan

Primary question: what is the safest path to decompose `admin/v7-admin-api` without changing behavior?

Answer: start with read-only view modules and deterministic builders. Leave routing, auth, actions, execution, governance writes, rollback apply, audit writes, closure writes, and UI shell ownership in the monolith until contracts are stronger.

## Stage 1: Read-Only Extraction

Scope:

- registry view helpers;
- event/audit/evidence serializers;
- redacted response builders;
- no route movement;
- no writes;
- no command execution.

Risk: LOW/MEDIUM.

Complexity: LOW.

Estimated line reduction: 300-1,000.

Expected performance gain: small immediately; enables request snapshots and caching.

Exit criteria:

- endpoint inventory unchanged except timestamps if regenerated;
- `py_compile` passes;
- read-only endpoint contract tests pass;
- no new stores.

## Stage 2: Shared Builders

Scope:

- overview sub-builders;
- service matrix read summaries;
- route-class metadata views;
- policy read summaries;
- bounded request snapshot object.

Risk: MEDIUM.

Complexity: MEDIUM.

Estimated line reduction: 1,000-2,500.

Expected performance gain: medium through reduced repeated reads.

Exit criteria:

- `/api/overview` nested schema snapshots;
- before/after redaction checks;
- bounded JSONL and registry reads.

## Stage 3: Routing Intelligence Views

Scope:

- display adapters over `admin_core.routing_brain` and `admin_core.routing_intelligence`;
- planner advisory explanation views;
- no planner scoring change;
- no autoswitch apply behavior change.

Risk: MEDIUM.

Complexity: MEDIUM.

Estimated line reduction: 300-800.

Expected performance gain: small/medium; clearer ownership.

Exit criteria:

- RI.3 advisory contract fixtures;
- planner ranking tests remain unchanged;
- admin display does not recompute authority.

## Stage 4: Action Handler Preparation

Scope:

- define action handler registry metadata;
- extract pure request parsing/validation;
- keep actual route dispatch in `Handler.do_POST`;
- keep `run_action` in monolith.

Risk: HIGH.

Complexity: HIGH.

Estimated line reduction: 500-1,500.

Expected performance gain: low; maintainability gain high.

Exit criteria:

- all action paths have contract fixtures;
- CSRF/auth/safe-mode/confirm behavior locked;
- no command argument drift.

## Stage 5: Governance Handlers

Scope:

- read-only governance views first;
- approval/rehearsal serializers over `admin_core.operator_execution`;
- mutation endpoints last.

Risk: HIGH.

Complexity: HIGH.

Estimated line reduction: 500-1,200.

Expected performance gain: low/medium.

Exit criteria:

- packet/event store truth source locked;
- approval audit behavior locked;
- no parallel governance store.

## Stage 6: Execution Handlers

Scope:

- only after action/gov contracts;
- isolate execution wrappers around existing tools;
- do not introduce a new executor;
- keep audit/closure compatibility.

Risk: CRITICAL.

Complexity: HIGH.

Estimated line reduction: 800-2,000.

Expected performance gain: low; reliability/ownership gain high.

Exit criteria:

- dry-run/live smoke matrix;
- rollback test coverage;
- audit and closure lineage preserved;
- runtime support tools remain authoritative.

## Stage 7: UI Separation

Scope:

- split static CSS/JS/templates from `html_page_v2`;
- keep `/admin-v2` path;
- no new top-level admin surface;
- preserve action names and API contracts.

Risk: MEDIUM/HIGH.

Complexity: HIGH.

Estimated line reduction: 8,000-12,000 from monolith.

Expected performance gain: medium for maintainability and response generation, not necessarily runtime routing.

Exit criteria:

- API contracts frozen;
- browser smoke for `/admin-v2`;
- visual regression/screenshot checks;
- no new navigation authority.

## API.2 Starting Scope

Recommended API.2 title:

`API.2 Read-Only Registry And Operator View Extraction`

Allowed:

- create small `admin_core` modules;
- move pure read-only helpers;
- add/adjust unit tests;
- regenerate endpoint inventory if code touched;
- no behavior change.

Forbidden:

- runtime mutation;
- routing changes;
- user movement;
- deploy;
- force push;
- action execution extraction;
- UI split.

## Decomposition Verdict

Decomposition can begin safely only under a narrow Stage 1 scope. It is not safe to begin with action handlers, execution handlers, governance mutation handlers, rollback apply, or UI separation.
