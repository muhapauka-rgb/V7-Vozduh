# V7 Phase 2 - Provisioning Auditability

## Purpose

Every lifecycle action must be attributable and explainable.

## Required Fields

Each lifecycle action should capture:

- actor;
- reason;
- timestamp;
- lifecycle state before;
- lifecycle state after;
- draft id;
- egress id;
- files changed;
- runtime commands;
- verification result;
- rollback availability.

## Actions Requiring Audit

- draft create;
- preflight run;
- runtime/quarantine test;
- pool add;
- runtime profile provision;
- enable;
- disable;
- maintenance;
- drain;
- existing egress update;
- rollback;
- delete/archive.

## Audit Quality

Good:

- `egress awg3 added disabled after quarantine PASS`
- `openvpn profile provisioned; enable blocked by runtime readiness`
- `maintenance requested for egress e1; 4 users require drain`

Bad:

- `fix`;
- `auto`;
- empty reason;
- hidden tool action.

## Phase 2 Boundary

This audit contract does not change current audit implementation. It defines what future lifecycle actions must preserve.
