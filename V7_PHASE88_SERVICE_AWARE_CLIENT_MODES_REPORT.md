# V7 Phase88 Service-aware Client Modes Report

Date: 2026-05-08

## Goal

Tie service-aware routing to user/client onboarding without changing live VPN routes.

This phase keeps the current server-side model intact and adds the missing operator layer:

- client-side RU filtering modes are visible in Admin;
- Identity group `route_policy` now controls the smart profile mode for public `/connect` onboarding;
- generated smart profile metadata records what each mode does with ordinary RU, sensitive RU, and global traffic.

## Changes

- Added `SMART_MODE_ROUTES` to Admin:
  - `RU_LOCAL`
  - `ABROAD_RU_VIA_V7`
  - `AUTO_TRAVEL`
  - `STRICT_V7`
- Added `Client Route Modes` table in Service-aware Policy.
- Public onboarding now resolves profile mode from Identity group route policy:
  - allowed phone group wins;
  - otherwise organization group wins;
  - otherwise connect form/default mode is used.
- User detail now shows ordinary RU / sensitive RU behavior for smart profile modes.
- Karing profile metadata now includes `mode_routes`.

## Current Meaning

```text
RU_LOCAL:
  ordinary RU -> client direct
  sensitive RU -> client direct
  global -> V7

ABROAD_RU_VIA_V7:
  ordinary RU -> V7 DIRECT_RU
  sensitive RU -> requires separately proven trusted RU abroad path
  global -> V7

AUTO_TRAVEL:
  ordinary RU -> selector client direct or V7 direct
  sensitive RU -> selector client direct or trusted RU
  global -> V7

STRICT_V7:
  ordinary RU -> V7 DIRECT_RU
  sensitive RU -> requires separately proven trusted RU abroad path
  global -> V7
```

## Live VPS Validation

Admin health remained OK.

Overview exposes four smart modes:

```text
ABROAD_RU_VIA_V7
AUTO_TRAVEL
RU_LOCAL
STRICT_V7
```

Karing generator dry-run:

```text
V7_SMART_CLIENT_PROFILE_DRY_RUN=OK
adapter=karing
mode=AUTO_TRAVEL
```

## Safety Notes

- No live routing rules were changed.
- No new user was created.
- No client key or profile secret was printed.
- Sensitive RU for abroad remains marked as requiring a separately proven route.

