# V7 Phase 77 - Onboarding Attempts Visibility

Date: 2026-05-08

## Goal

Make `/connect` onboarding observable for an operator directly inside the admin panel.

## Implemented

- Added recent onboarding attempts to `identity_state`.
- Added summary counters:
  - total connect attempts;
  - failed connect attempts.
- Added Identity UI table:
  - result;
  - phone;
  - entered name;
  - organization;
  - failure/success reason;
  - request IP;
  - timestamp.

## Why It Matters

When a user cannot connect, the operator can now see whether the reason was:

- phone not allowed;
- invalid connection password;
- organization mismatch or not found;
- device limit reached;
- provisioning/profile generation failure;
- successful device creation.

This keeps support work inside the admin panel and avoids SSH log reading for normal cases.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- Live Identity state:
  - onboarding attempts visible: OK
  - current attempts count: `3`
  - current failed attempts count: `2`

## Next

Phase 78 should add import preview and safer organization/group selection:

- preview phone import before applying;
- map imported phones to group/organization from UI controls;
- replace raw group IDs with selector-style controls where practical;
- add clearer warnings for device limits before users hit `/connect`.
