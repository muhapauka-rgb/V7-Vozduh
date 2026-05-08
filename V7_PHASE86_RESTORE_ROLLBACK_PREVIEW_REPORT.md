# V7 Phase86 Restore Rollback Preview Report

Date: 2026-05-08

## Goal

Make restore and rollback safer for an operator by turning raw command output into explicit preview fields.

## Changes

- Backup restore preview now opens a focused Admin modal with:
  - identity/admin file inclusion
  - sensitive material warning
  - raw preview output
- Rollback preview now returns structured fields:
  - candidate backup
  - target file
  - target kind
  - restart required
  - sensitive material
  - apply guard
  - dry-run mode
- Fixed `v7-rollback-last-change` candidate selection so `find | sort | head` cannot fail with SIGPIPE under `set -o pipefail`.

## Live VPS Validation

Admin health remained OK after deployment.

Rollback preview through authenticated Admin API:

```text
action=rollback_preview
target_kind=v7_executable
restart_required=none
sensitive_material=no
apply_guard=requires_owner_role_and_ROLLBACK_confirmation
MODE=dry_run
ACTION=none
rc=0
```

## Safety Notes

- No rollback apply was run.
- Apply still requires owner role and exact `ROLLBACK` confirmation.
- Restore remains preview-only and does not extract archives.

