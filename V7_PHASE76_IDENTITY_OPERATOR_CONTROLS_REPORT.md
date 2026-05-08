# V7 Phase 76 - Identity Operator Controls

Date: 2026-05-08

## Goal

Turn Identity / Onboarding into a more practical operator tool without changing the existing VPN routing architecture.

## Implemented

- Added global access settings update:
  - default max devices for new users;
  - existing users keep their individual limits.
- Added allowed phone bulk import:
  - accepts CSV with header: `phone,name,note`;
  - also accepts simple rows: `phone,name,note`;
  - supports optional organization/group IDs from the API payload.
- Added allowed phone export:
  - returns CSV from the current Identity DB;
  - secrets are not included.
- Added allowed phone enable/disable actions in the admin UI.
- Improved allowed phone upsert safety:
  - status-only updates keep existing name, organization, group, and note.
- Improved Identity UI:
  - access settings panel;
  - bulk import textarea;
  - export action;
  - allowed phone action column.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Isolated unit test with temporary Identity DB:
  - access settings update: OK
  - allowed phones import: OK
  - allowed phones export: OK
  - status-only allowed phone update preserves metadata: OK
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK

## Notes

- This phase does not touch WireGuard, routing tables, V7 policy, egress selection, or live user traffic.
- Connection password remains one shared password stored only as a hash.

## Next

Phase 77 should improve production onboarding workflow:

- organization/group selector usability;
- import preview before applying big phone lists;
- onboarding attempts table in the admin UI;
- clearer device-limit warnings before users hit `/connect`.
