# V7 Phase 7 Backup And Restore Maturity

## Purpose

Backups must be restorable, verified, and safe for datapath.

## Backup Scope

Back up:

- registries;
- policies;
- org policy;
- identity DB;
- admin auth and safe-mode;
- egress draft metadata;
- runtime profiles;
- audit/events;
- rollback metadata.

## Backup Requirements

- timestamped;
- integrity checked;
- encrypted when stored outside the host;
- includes restore manifest;
- includes source paths and file modes;
- includes rollback pointer for dangerous changes.

## Restore Gates

Restore must not silently apply runtime changes.

Before applying restore:

- validate archive integrity;
- validate schema/contracts;
- compare before/after impact;
- preview affected users/egress;
- confirm rollback path;
- plan runtime reconciliation.

After restore:

- run contract validation;
- run lifecycle validation;
- run provisioning reconciliation;
- run kill switch check;
- verify route classes;
- keep platform in safe/maintenance mode until verified.

## Forbidden Restore Behavior

Restore must not:

- overwrite unknown paths;
- enable unverified egress;
- silently change route policy;
- silently bypass kill switch;
- delete current state before backup.

