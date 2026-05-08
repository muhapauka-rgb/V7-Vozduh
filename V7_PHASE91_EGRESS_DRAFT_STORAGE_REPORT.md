# V7 Phase91: Egress Draft Storage

Date: 2026-05-08

## What Changed

- Added inactive egress draft storage to the admin API.
- Draft configs are saved under `/etc/v7/egress-drafts/<draft_id>/config.input`.
- Draft metadata is saved under `/etc/v7/egress-drafts/<draft_id>/metadata.json`.
- Drafts are not added to `egress.registry`, not started, and not routed.
- Admin UI now has `Add Egress Draft`, `Save Draft`, `Refresh Drafts`, and `Test Plan` actions.

## Safety Model

- Saving a draft requires the explicit confirmation string `SAVE_EGRESS_DRAFT`.
- `/etc/v7/egress-drafts` is forced to mode `700`.
- Each draft directory is mode `700`.
- Raw config and metadata files are mode `600`.
- API responses do not return the raw config or internal `config_path`.
- Admin Safe Mode blocks draft creation.

## Live VPS Validation

VPS: `195.2.79.116`

Checks completed:

- Local compile: `python3 -m py_compile admin/v7-admin-api`
- Local diff check: `git diff --check`
- VPS compile: `python3 -m py_compile /usr/local/bin/v7-admin-api`
- Service restart: `systemctl restart v7-admin-api`
- Service health: `systemctl is-active v7-admin-api` returned `active`
- API health: `GET http://127.0.0.1:7080/health` returned `status=OK`
- Draft create live-test returned:
  - protocol: `wireguard`
  - runtime mode: `interface`
  - test preview mode: `preview_only`
  - pool action: `still_not_added`
  - secret redaction: `ok`

Final permission check:

```text
drwx------ root root /etc/v7/egress-drafts
drwx------ root root /etc/v7/egress-drafts/<draft_id>
-rw------- root root /etc/v7/egress-drafts/<draft_id>/config.input
-rw------- root root /etc/v7/egress-drafts/<draft_id>/metadata.json
```

Registry check:

- Test draft id was not found in `/opt/v7/egress/state/egress.registry`.
- Test draft id was not found in `/opt/v7/egress/state/users.registry`.

Temporary test drafts were removed after validation.

## Next Step

Phase92 should add an isolated egress draft test executor:

- copy a draft into a temporary isolated profile;
- validate required native runtime tools;
- start a temporary interface/proxy without touching active egresses;
- run external IP and service matrix checks;
- keep the draft quarantined until all checks pass.
