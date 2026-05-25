# V7 Phase 7 Infrastructure Auditability

## Purpose

Critical infrastructure actions must be attributable and reversible.

## Audit Contract

Every critical action should record:

- actor;
- reason;
- timestamp;
- target;
- impact;
- before state;
- after state;
- verification result;
- rollback path.

## Critical Actions

- backup restore;
- upgrade apply;
- rollback apply;
- systemd interval apply;
- egress maintenance;
- egress quarantine;
- route rebuild;
- kill switch rebuild;
- runtime profile rewrite.

## Missing Audit Behavior

If audit cannot be written:

- block dangerous actions;
- allow read-only diagnostics;
- show operator warning.

