# V7 Phase 78 - Identity Import Preview and Selectors

Date: 2026-05-08

## Goal

Reduce operator mistakes during onboarding management.

## Implemented

- Added allowed phone import preview.
- Import now refuses to apply if preview contains row errors.
- Preview detects:
  - invalid phone numbers;
  - duplicate phones inside the pasted import;
  - existing phones that will be updated;
  - missing group or organization references.
- Added organization/group selectors in Identity UI:
  - organization group assignment;
  - allowed phone organization assignment;
  - allowed phone group assignment;
  - bulk import default organization/group.
- Added clearer device-limit visibility:
  - Identity summary now shows users at device limit.

## Operator Flow

1. Paste phone CSV into Bulk Import Phones.
2. Choose default organization/group from selectors.
3. Press `Preview Import`.
4. Review rows, errors, and existing updates.
5. Press `Apply Import`.
6. Confirm with `APPLY_PHONE_IMPORT`.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Isolated unit test with temporary Identity DB:
  - preview detects duplicate and invalid rows: OK
  - import refuses rows with preview errors: OK
  - clean import applies successfully: OK
  - repeated preview marks existing rows as updates: OK
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- VPS live smoke test:
  - preview rows: `2`
  - valid rows: `1`
  - error rows: `1`
  - DB mutation: none

## Next

Phase 79 should improve the public `/connect` user experience:

- show clearer user-facing messages for common failures;
- expose organization choices safely where appropriate;
- show device-limit guidance without exposing internal details;
- keep public gateway locked down to `/connect`, `/profile-delivery/*`, and `/health`.
