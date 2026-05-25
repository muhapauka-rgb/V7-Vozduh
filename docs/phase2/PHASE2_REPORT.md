# V7 Phase 2 - Provisioning And Egress Lifecycle Report

## Scope

Phase 2 was applied as a bounded, non-runtime-changing pass.

Implemented:

- formal egress lifecycle model;
- driver/capability model;
- unified import pipeline model;
- quarantine model;
- runtime enable gates;
- maintenance/drain model;
- rollback/recovery model;
- runtime dependency safety model;
- registry/runtime reconciliation model;
- safe operator workflows;
- egress health history model;
- safe state persistence model;
- provisioning auditability model;
- read-only egress lifecycle validator.

Not changed:

- routing core;
- nftables;
- kill switch behavior;
- autoswitch behavior;
- admin API behavior;
- provisioning runtime behavior;
- existing registry format;
- systemd units.

## Findings From Inspection

Current project already has substantial Phase 2 foundation:

- admin API can create drafts and stores root-only metadata/config;
- preflight checks validate tools and static safety;
- runtime tests use temporary isolated interface/proxy where supported;
- quarantine mode checks service matrix before pool add;
- pool add writes egress as `enabled=0`;
- runtime provision prepares profiles without moving users;
- enable preview and apply are guarded;
- `v7-egress-set-state` defaults to dry-run and backs up registry/flags before apply;
- existing channel update includes backup and rollback behavior.

Main gaps formalized:

- lifecycle states were implicit rather than project-wide contract;
- driver capabilities were spread across protocol branches;
- quarantine needed explicit "no production eligibility" language;
- maintenance/drain requires a clear operator workflow;
- rollback and cleanup need one shared model;
- lifecycle consistency needed a read-only validation helper.

## Verification Principle

Provisioning verification must prove:

`source -> draft -> preflight -> isolated runtime -> quarantine -> disabled pool -> explicit enable`

It must not jump directly from import to production.

## Next Phase Gate

Do not proceed to Phase 3 until explicitly instructed.
