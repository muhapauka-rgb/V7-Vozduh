# V7 Phase 2 - Safe Operator Workflows

## Purpose

Provisioning UX must stay calm and workflow-oriented.

The operator should see lifecycle state and next safe action, not a wall of runtime details.

## Channel Add Workflow

Summary states:

- `imported`;
- `testing`;
- `quarantine`;
- `ready`;
- `added disabled`;
- `enable guarded`;
- `degraded`;
- `rollback available`.

Default view:

- current stage;
- blocker;
- production impact;
- safe next action.

Drill-down:

- raw preflight checks;
- temporary runtime logs;
- service matrix;
- duplicate fingerprint;
- profile path.

## Maintenance Workflow

Default view:

- users impacted;
- safe target count;
- drain status;
- rollback availability.

No default giant user tables.

## Rollback Workflow

Default view:

- action to rollback;
- backup available;
- runtime cleanup status;
- expected impact.

Drill-down:

- before/after files;
- commands;
- audit event;
- verification output.

## UX Non-Negotiables

Do not show:

- raw command dumps as primary UI;
- all egress metrics on one page;
- noisy tables for every draft;
- ambiguous "AI recommends" phrasing.

Do show:

- state;
- impact;
- reason;
- suggested bounded action.
