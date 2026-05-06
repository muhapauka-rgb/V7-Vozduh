# V7 Admin Phase 7: User Creation Workflow

Date: 2026-05-06

## Goal

Add an authenticated admin workflow for creating WireGuard users through the local V7 Admin API/UI without exposing private keys in API logs, audit logs, or chat output.

## Implemented

- Added authenticated UI form for creating a user.
- Added `POST /api/actions/user-create`.
- Added protected artifact download:
  - `GET /api/client-artifact?name=<client>&type=conf`
  - `GET /api/client-artifact?name=<client>&type=qr`
- Added safe client-name validation.
- Added parsed action result fields for admin UI/API.
- Kept generated configs and QR artifacts under `/root/v7-clients/<client>/`.
- Updated `v7-admin-api.service` write paths so the admin API can safely call the existing user creation core.
- Updated overview summary so disabled users are not counted as active route/leak failures.

## Security

- Auth is required for user creation.
- CSRF token is required for user creation.
- Artifact downloads require an authenticated session.
- Private keys are not printed in validation output.
- Audit entries record user name/IP/table/egress, not WireGuard private keys.
- Admin service remains local-only on `127.0.0.1:7080`.

## Validation

- No CSRF request returned `403 csrf_failed`.
- Dry-run user creation worked and selected the next free user:
  - IP: `10.0.0.4`
  - table: `102`
  - egress: `awg2`
- Real test user creation via admin API succeeded.
- Generated config download required auth and returned a valid WireGuard config.
- Generated QR download required auth and returned a valid PNG.
- Test user was disabled and fully cleaned up after validation.
- Final `users.registry` contains only production test users:
  - `10.0.0.2 current=awg2 table=100 enabled=1`
  - `10.0.0.3 current=awg2 table=101 enabled=1`
- `/root/v7-clients/phase7-test-195019` was removed.
- `v7-user-route-check` result: `V7_USER_ROUTE_CHECK=OK`.
- `v7-system-check` result: `V7_RESULT=OK`.
- `v7-killswitch-check` result: `V7_KILLSWITCH_CHECK=OK`.
- Admin overview summary:
  - `users_total=2`
  - `users_registry_total=2`
  - `egress_total=2`
  - `egress_healthy=2`
  - `route_ok=2`
  - `route_leak_risk=false`
  - `killswitch_ok=true`
  - `stale_ok=true`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-195630.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-195630.tar.gz.sha256`

## Notes

- Current workflow is suitable for admin-driven user provisioning.
- Next production step should be user lifecycle controls in admin:
  - disable user
  - reissue config
  - rotate peer key
  - show user history
  - show route reality and leak status per user
