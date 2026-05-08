# V7 Phase 79 - Admin Login Password Controls

Date: 2026-05-08

## Goal

Make `/login` admin password manageable from the admin panel and set the current live admin login to the requested known value.

## Implemented

- Added `ADMIN_PASSWORD_MIN_LENGTH` with default `5`.
- Added backend action:
  - `/api/actions/admin-account-password-set`
  - owner-only;
  - CSRF-protected;
  - requires confirmation `SET_ADMIN_PASSWORD`;
  - stores only a password hash.
- Added Admin Accounts UI controls:
  - set explicit login password for an account;
  - row-level `Set Password` action;
  - existing random reset remains available as `Reset Random`.
- Legacy owner password hash is kept in sync when changing the legacy admin account.

## Live Server Change

- Updated the live `admin` login password to the requested value.
- Updated local ignored password handoff file:
  - `admin/v7-admin-password.txt`

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Isolated unit test with temporary `auth.json`: OK
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- HTTP login check:
  - POST `/login`: HTTP `303`
  - `/health`: HTTP `200`

## Next

Phase 80 should return to public `/connect` UX:

- clearer user-facing error messages;
- better organization guidance;
- device-limit explanation before support has to intervene.
