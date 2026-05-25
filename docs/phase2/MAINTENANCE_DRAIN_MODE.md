# V7 Phase 2 - Maintenance And Drain Mode

## Purpose

Maintenance must remove egress from normal service without abruptly breaking users or silently rerouting them.

## Maintenance State

Maintenance means:

- no new assignments;
- no autoswitch target eligibility;
- current users require a bounded migration plan;
- rollback context is required.

## Drain Mode

Drain mode should:

- preserve existing sessions where possible;
- prevent new users from being assigned;
- propose migrations in bounded batches;
- run dry-run before apply;
- verify destination egress health;
- audit every move.

## Disable Guard

Before disabling or maintenance:

- check assigned users;
- block if users remain and no migration plan exists;
- show impact count;
- suggest safe targets;
- require explicit operator confirmation for user moves.

Current code already references `v7-egress-guard` before disabling/maintenance when available.

## Rollback

Rollback should restore:

- previous enabled/maintenance flag;
- previous runtime state when safe;
- prior registry backup;
- user assignment plan if migrations were applied.

## Operator UX

Summary:

- `maintenance planned`;
- `draining`;
- `users remaining`;
- `rollback available`;
- `safe targets`.

Details:

- user list;
- route-class fit;
- per-destination health;
- exact migration plan.
