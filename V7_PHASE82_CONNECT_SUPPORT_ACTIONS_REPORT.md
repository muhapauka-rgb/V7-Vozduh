# V7 Phase 82 - Connect Support Actions

Date: 2026-05-08

## Goal

Make support work for `/connect` failures faster and less error-prone for an operator.

## Implemented

- Added filters to `Connect Support`:
  - by phone;
  - by failure reason.
- Added filtered details:
  - `Details` now respects the phone filter.
- Improved `Use Phone` action:
  - fills phone;
  - fills entered name;
  - fills operator note with source failure reason and timestamp.
- Added operator note field to Allowed Phone form.
- Allowed Phone upsert now sends the note from the UI.
- Added Identity user note action:
  - each user row has `Note`;
  - notes are saved through the existing `identity-user-update` action.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Local admin HTML smoke test:
  - `Connect Support`: present;
  - phone filter: present;
  - allowed phone note: present;
  - identity user note action: present.
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- Live admin check:
  - POST `/login`: HTTP `303`
  - admin page: HTTP `200`
  - Phase82 UI elements present.

## Next

Phase 83 should tighten auditability around support actions:

- show operator notes in user/phone detail views;
- add audit-oriented wording around phone/user changes;
- add quick filters in Events/Security Audit for Identity changes.
