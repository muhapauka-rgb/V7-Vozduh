# P2.8 API Drift

## Current Local Source Inventory

Generated read-only to `/private/tmp/p2_8-endpoint-inventory.json`:

- endpoint_count: `264`
- GET: `118`
- HEAD: `8`
- POST: `138`
- public: `19`
- required auth: `245`
- critical risk: `13`
- high risk: `95`
- medium risk: `38`
- low risk: `118`
- csrf_required_count: `133`
- safe_mode_blocked_count: `86`

## Documented Inventory

`docs/track5/endpoint-inventory.json` reports:

- endpoint_count: `211`
- GET: `66`
- HEAD: `8`
- POST: `137`

## Runtime API

Public runtime confirms:

- `/health`
- `/admin-v2` route to login

Authenticated runtime API endpoints were not probed to avoid login/session side effects during this audit.

## Drift

API drift is present between implemented local source and documented inventory. Runtime API equivalence is not proven.

## Verdict

api_drift_found=true
