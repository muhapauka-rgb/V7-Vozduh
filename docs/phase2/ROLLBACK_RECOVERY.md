# V7 Phase 2 - Rollback And Recovery

## Purpose

Every provisioning action that changes persistent state or runtime must have rollback context.

## Rollback Context

Capture:

- actor;
- reason;
- timestamp;
- action id;
- target draft/egress;
- before state;
- after state;
- changed files;
- backup files;
- runtime commands;
- verification result.

## Current Backup Surfaces

Current code already creates backups for:

- draft metadata during pool apply;
- egress registry during pool apply;
- runtime provision metadata;
- egress registry and flags during `v7-egress-set-state`;
- existing channel config update.

## Recovery Targets

Recovery must handle:

- stale runtime profile;
- stale temporary interface;
- stale proxy process;
- stale route/nft entries;
- stale registry enabled flag;
- inconsistent metadata lifecycle;
- orphan OpenVPN pid/unit;
- profile exists with different content.

## Cleanup Rules

Cleanup must be:

- explicit;
- verified;
- audited;
- safe to retry.

No cleanup should delete unknown files outside V7-managed paths.

## Failure Policy

If rollback cannot be verified:

- mark egress `failed` or `rollback_candidate`;
- block production enable;
- show manual intervention guidance;
- do not hide partial state.
