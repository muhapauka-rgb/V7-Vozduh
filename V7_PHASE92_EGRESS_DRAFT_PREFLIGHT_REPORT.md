# V7 Phase92: Egress Draft Preflight

Date: 2026-05-08

## What Changed

- Added an admin action to run root-only egress draft preflight checks.
- Added an admin UI button: `Run Preflight`.
- Preflight copies the saved draft config into an isolated test-run directory.
- Preflight checks runtime dependencies and static routing safety rules.
- Preflight does not start a tunnel, does not edit routes, and does not add the draft to the active pool.

## Storage

Drafts:

- `/etc/v7/egress-drafts/<draft_id>/config.input`
- `/etc/v7/egress-drafts/<draft_id>/metadata.json`

Preflight runs:

- `/opt/v7/admin/egress-draft-tests/<run_id>/config.input`
- `/opt/v7/admin/egress-draft-tests/<run_id>/result.json`

The preflight storage path was deliberately moved from `/var/tmp` to `/opt/v7/admin/egress-draft-tests`, because the admin service uses a systemd private tmp area. Keeping preflight reports under `/opt/v7/admin` makes them predictable and suitable for backup/restore.

## Safety Model

- Running preflight requires the explicit confirmation string `RUN_PREFLIGHT`.
- Admin Safe Mode blocks preflight runs.
- The API response does not include the raw config or internal config path.
- Test-run root directory is mode `700`.
- Each run directory is mode `700`.
- Copied config and result files are mode `600`.
- Active registries are checked to verify the draft is not already in the pool.

## Live VPS Validation

VPS: `195.2.79.116`

Checks completed:

- Local compile: `python3 -m py_compile admin/v7-admin-api`
- Local diff check: `git diff --check`
- VPS compile: `python3 -m py_compile /usr/local/bin/v7-admin-api`
- Service restart: `systemctl restart v7-admin-api`
- Service health: `systemctl is-active v7-admin-api` returned `active`
- API health: `GET http://127.0.0.1:7080/health` returned `status=OK`

Live preflight test result:

- protocol: `wireguard`
- runtime mode: `interface`
- preflight status: `PASS`
- mode: `no_runtime_start`
- pool action: `still_not_added`
- dependency checks:
  - `ip`: OK
  - `wg`: OK
  - `wg-quick`: OK
  - `curl`: OK
- static checks:
  - detected required fields: OK
  - not in active registry: OK
  - `Table = off`: OK
  - endpoint present: OK
- secret redaction: OK

Final permission check:

```text
drwx------ root root /opt/v7/admin/egress-draft-tests
drwx------ root root /opt/v7/admin/egress-draft-tests/<run_id>
-rw------- root root /opt/v7/admin/egress-draft-tests/<run_id>/config.input
-rw------- root root /opt/v7/admin/egress-draft-tests/<run_id>/result.json
```

Registry check:

- Test draft id was not found in `/opt/v7/egress/state/egress.registry`.
- Test draft id was not found in `/opt/v7/egress/state/users.registry`.

Temporary test drafts and test runs were removed after validation.

## Next Step

Phase93 should add a real isolated runtime test stage:

- use the preflight result as a gate;
- create a temporary profile/interface/proxy name;
- start only the temporary runtime;
- verify external IP and service matrix;
- stop and clean up temporary runtime;
- keep the draft quarantined until all checks pass.
