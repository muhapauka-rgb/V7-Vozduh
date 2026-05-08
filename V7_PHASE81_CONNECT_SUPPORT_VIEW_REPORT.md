# V7 Phase 81 - Connect Support View

Date: 2026-05-08

## Goal

Make `/connect` failures actionable for an operator inside the admin panel.

## Implemented

- Added `Connect Support` block to `Identity / Onboarding`.
- Recent failed onboarding attempts are grouped by reason.
- Each reason shows:
  - count;
  - number of affected phones;
  - number of entered organizations;
  - latest occurrence;
  - suggested operator action;
  - details button.
- Details modal shows matching attempts:
  - time;
  - phone;
  - entered name;
  - entered organization;
  - request IP.
- Added `Use Phone` action from the details modal to fill the Allowed Phone form.

## Operator Actions Covered

- `phone_not_allowed`: add the phone and assign organization/group.
- `invalid_connection_password`: share or reset the connection password.
- `organization_not_found`: create the organization or tell the exact name.
- `organization_mismatch`: fix allowed phone organization assignment.
- `device_limit_reached`: increase device limit or revoke an old device.
- `safe_mode_enabled`: disable safe mode when onboarding can resume.
- provisioning/profile/delivery failures: run system checks and inspect backend/runtime logs.

## Verification

- Local syntax compile: OK
- `git diff --check`: OK
- Local render smoke test: OK
- VPS deploy:
  - previous admin API backed up;
  - `v7-admin-api` restarted;
  - `/health`: OK
- Live admin check:
  - POST `/login`: HTTP `303`
  - admin page: HTTP `200`
  - `Connect Support` UI present.

## Next

Phase 82 should add safer onboarding support actions:

- one-click allowed-phone prefill with organization/group selector focus;
- optional attempt filters by phone/reason;
- operator note field for why a phone/user was changed.
