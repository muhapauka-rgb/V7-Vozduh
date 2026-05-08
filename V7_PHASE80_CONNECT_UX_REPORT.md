# V7 Phase 80 - Public Connect UX

Date: 2026-05-08

## Goal

Improve the public `/connect` page so non-technical users understand common onboarding failures without exposing internal admin data.

## Implemented

- Added structured public error rendering for `/connect`.
- Added human guidance for:
  - missing required fields;
  - rate limit;
  - phone not allowed;
  - invalid connection password;
  - organization not found;
  - organization mismatch;
  - blocked or disabled user;
  - device limit reached;
  - safe mode;
  - provisioning/profile/delivery failures.
- Preserved form values after an error:
  - name;
  - phone;
  - organization;
  - selected VPN client.
- Password is never preserved back into the form.
- Public page does not expose organization lists, group IDs, user records, tokens, or keys.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Local page render unit test:
  - device-limit guidance: OK
  - form value preservation: OK
  - password not prefilled: OK
  - selected client preservation: OK
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- Live `/connect` UX test:
  - invalid password returns HTTP `403`;
  - public page shows clear password guidance;
  - name/organization/client selection preserved;
  - public `/connect`: HTTP `200`;
  - public `/api/overview`: HTTP `404`.

## Next

Phase 81 should add a small operator-side support view for connect failures:

- group recent failures by reason;
- show suggested operator action per reason;
- add one-click filters for phone/organization/user.
