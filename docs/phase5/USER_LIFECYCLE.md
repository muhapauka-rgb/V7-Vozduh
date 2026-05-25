# V7 Phase 5 User Lifecycle

## Purpose

User lifecycle must be explicit, auditable, and compatible with current runtime behavior.

## Target Lifecycle

- invited;
- pending;
- onboarded;
- active;
- degraded;
- suspended;
- reconnect_required;
- revoked;
- archived.

## Current Compatibility Mapping

Current SQLite statuses include:

- `active`;
- `pending`;
- `blocked`;
- `disabled`.

Compatibility mapping:

- `pending` -> pending;
- `active` with no active device -> onboarded;
- `active` with active device -> active;
- `blocked` -> suspended;
- `disabled` -> suspended;
- deleted or tombstoned future state -> archived.

## State Meanings

invited:

- allowed user exists;
- no identity user or device yet.

pending:

- connect session or pending profile exists;
- user has not completed activation.

onboarded:

- identity user exists;
- no usable active device yet.

active:

- at least one active device exists;
- runtime assignment is consistent.

degraded:

- user exists and has active device, but readiness or routing is degraded.

suspended:

- operator blocks access without destroying audit history.

reconnect_required:

- profile exists but user needs a fresh import, reconnect, or profile rotation.

revoked:

- access is intentionally removed.

archived:

- historical record retained; no active access.

## Safety Rules

Lifecycle changes must:

- be audited;
- preserve rollback context when runtime access changes;
- never silently issue new access;
- never leave revoked devices active in `users.registry`;
- never remove audit history just to simplify UI.

