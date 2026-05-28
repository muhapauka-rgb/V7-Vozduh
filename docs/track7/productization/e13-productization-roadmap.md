# E13 Productization Roadmap

## Verdict

The orchestration core is ready for productization of bounded operator
governance. Larger cohort execution should wait until the operator UX,
observability, approval contracts, and dedicated test capacity are productized.

## Recommended Order

### 1. E14 - Approval Contract Schema And Read-Only API

Build the schema layer first:

- movement preview contract;
- generation token contract;
- rollback contract;
- restore barrier contract;
- delayed monitor contract;
- evidence bundle contract.

Scope:

- read-only generation and validation;
- no runtime mutation from UI;
- contract fixtures and tests;
- stale/replay rejection semantics.

Why first:

- UI without contracts becomes cosmetic;
- contracts preserve E12 governance truth.

### 2. E15 - Operator Overview And Observability UI

Build read-only screens:

- Runtime Overview;
- Target Pool;
- Operations History;
- Evidence Viewer;
- Runtime Warnings;
- Delayed Movement Monitor.

Scope:

- dark-first V7 visual language;
- no mutating controls;
- evidence freshness and state source visible;
- mobile-aware layouts.

Why second:

- operators need truth before actions.

### 3. E16 - Approval Center And Safe Action UX

Add controlled approval surfaces:

- Pending Movement Preview;
- Approval Center;
- Restore Lifecycle;
- Generation Governance;
- Cohort Governance;
- Reservation Management.

Scope:

- approval generation;
- dual-confirmation UX;
- disabled dangerous actions until contract gates pass;
- no broad autoswitch apply.

Why third:

- action UX should consume the read-only truth and contract layer.

### 4. E17 - Runtime/Repo Lineage Convergence

Close partial lineage gaps:

- release manifest coverage;
- runtime/repo diff authority;
- current deployed tool provenance;
- evidence source labeling;
- rollback material index.

Why before larger cohort:

- larger blast radius requires stronger auditability.

### 5. E18 - Audit Search And Evidence Detail Hardening

Harden the read-only archive:

- audit search/filtering;
- hardened evidence detail drawer;
- stale/conflict warnings;
- bounded fulltext-like discovery;
- secret-safe evidence excerpts.

Why before mutating UX:

- operators need audit-grade history before approving actions.

### 6. Stage 2 Finalization - Production Operator System Completion

Close the read-only operator layer:

- audit export/runbook packet preview;
- multi-operator approval audit model;
- coherent operator navigation;
- final read-only safety review.

### 7. E19 - Safe Action UX And Dual-Confirmation Execution Design

Design mutating action semantics without exposing execution yet:

- approval author/reviewer;
- approval expiry;
- immutable generation ownership;
- selected-move fingerprint binding;
- rollback manifest binding;
- exact runtime execution boundary.

Status after E19:

- safe action UX exists;
- dual-confirmation model is visible;
- replay rejection is visible;
- execution controls remain disabled;
- no mutating endpoint exists.

### 8. E20 - Mutating Execution Governance Rehearsal

Rehearse execution governance without production movement:

- runtime recheck model;
- immutable audit semantics;
- dual-confirmation lifecycle;
- replay rejection;
- stale approval denial;
- denial/containment lineage.

Status after E20:

- execution governance rehearsal complete;
- real runtime execution still disabled;
- next step must be a first real bounded execution packet.

### 9. E21 - First Real Operator-Driven Bounded Execution Packet

Generate a packet for one bounded operator-driven action:

- exact operation scope;
- production approval persistence requirement;
- dual-operator auth binding requirement;
- runtime recheck against live state;
- rollback-bound execution;
- delayed monitoring plan.

No execution unless the packet explicitly reaches GO.

Status after E21:

- selected first action is approval-record plus runtime-recheck only;
- UI-triggered execution remains forbidden;
- CLI packet execution is recommended;
- no user or routing mutation is approved.

### 10. E22 - First Real Approval Record And Runtime Recheck Execution

Execute only the zero-user governance transition:

- consume UI-generated packet through CLI;
- bind two operator confirmations;
- run live runtime recheck;
- persist append-only approval/audit record;
- stop before user movement and routing mutation.

Status after E22:

- CLI packet consumer implemented;
- append-only audit store implemented;
- live runtime recheck connected;
- local execution failed closed with DENY_STALE_RUNTIME because live VPS
  runtime state was unavailable in the workspace;
- denial record persistence and replay rejection were proven;
- approval success path still requires fresh VPS runtime state.

### 11. E22.1 - Run Packet Consumer Against Fresh VPS Runtime State

Repeat the same zero-movement approval-record action where live runtime files are
available:

- no user movement;
- no routing mutation;
- no UI execution;
- approval record may be written only if live recheck passes.

Status after E22.1:

- live VPS runtime recheck passed;
- append-only approval record was written;
- replay and denial records were verified;
- no runtime action beyond approval/audit persistence occurred;
- VPS runtime/repo convergence gap remained for target-readiness and
  restore-settle helpers.

### 12. E23 - First Real Zero-Move Runtime Action

Execute the first real governed runtime action with zero blast radius:

- selected action: append-only runtime governance state transition;
- write governance action lineage under `/opt/v7/audit`;
- keep `users.registry`, `egress.registry`, routes, timers, and autoswitch
  state unchanged;
- verify replay denial and invalid packet denial;
- observe delayed effects.

Status after E23:

- first real zero-move runtime action executed;
- immutable audit chain verified;
- runtime/repo convergence verified for the selected zero-move scope;
- missing VPS target-readiness and restore-settle helpers remain blockers for
  movement-bearing actions;
- operator-driven execution is production-grade only for zero-move governance
  state transitions.

### 13. E24 - First Operator-Driven Bounded User Movement Approval Packet

Generate a separate larger-cohort approval packet only after E22.1:

- first bounded user movement should be an approval packet, not direct movement;
- exact candidate user;
- exact target;
- zero ambiguity around VPS readiness/restore-settle tooling;
- exact rollback path;
- exact containment path.

No execution in the approval packet.

### 14. E25 - First Operator-Driven Bounded User Movement Execution

Execute only if E24 is GO:

- exact candidate list;
- nonzero movement budget;
- matching generation token;
- selected-move fingerprint;
- rollback contract;
- delayed monitoring plan.
- final report;
- no cohort expansion until the one-user operator-driven path is proven.

## Later Roadmap

After larger-cohort governance:

- multi-operator approval and audit logging;
- autoswitch autonomy limits;
- commercial role/permission hardening;
- customer/org-level blast radius;
- operational SLO reporting;
- support runbooks and incident export.

## What Should Not Be Built Yet

- one-click broad autoswitch apply;
- generic network topology dashboard;
- AI autopilot for routing;
- arbitrary route editor;
- Direct/RU mutation UI beyond existing governance;
- Trusted RU refresh UI beyond existing governance;
- multi-tenant commercial dashboard before governance UX;
- larger cohort execution without dedicated test capacity.

## Dependency Map

| Stage | Depends on | Unlocks |
|---|---|---|
| E14 contracts | E12 generation governance | Safe UI approval semantics |
| E15 read-only UI | E14 contracts read models | Operator observability |
| E16 approval UX | E15 overview and E14 contracts | Safe bounded actions |
| E17 lineage | E12/E14 evidence model | Audit confidence |
| E18 audit search | E17 lineage | Evidence discovery |
| Stage 2 finalization | E15-E18 | Production Operator System |
| E19 safe action design | Stage 2 | Future mutating approval contract |
| E20 rehearsal | E19 | execution governance proof |
| E21 first bounded packet | E20 GO | first real operator execution decision |
| E22 approval record execution | E21 GO | denial/replay proof |
| E22.1 VPS runtime repeat | E22 fail-closed result | approval success proof |
| E23 larger-cohort packet | E22.1 proof plus target capacity | larger-cohort decision |
| E24 execution | E23 GO | larger-cohort evidence |
