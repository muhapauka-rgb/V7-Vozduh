# V7 Phase93: Isolated Egress Draft Runtime Test

Date: 2026-05-08

## What Changed

- Added isolated runtime testing for inactive egress drafts.
- Added admin UI action: `Runtime`.
- Added admin API action: `/api/actions/egress-draft-runtime-run`.
- Added root-owned helper: `/usr/local/bin/v7-egress-draft-runtime-helper`.
- Admin API delegates real network runtime tests to the helper through `systemd-run`.

## Why A Helper Was Needed

The admin API service intentionally runs with a constrained systemd sandbox:

- `NoNewPrivileges=yes`
- `PrivateTmp=yes`
- limited write paths

During validation, direct `wg-quick up` from inside the admin API failed with:

```text
/usr/bin/ip: Operation not permitted
```

Rather than expanding the web admin process privileges, Phase93 keeps the admin API as a control plane and uses a short-lived transient systemd job for the actual network operation.

## Runtime Safety Model

- Runtime requires a previous preflight `PASS`.
- Runtime requires explicit confirmation: `RUN_RUNTIME_TEST`.
- Drafts remain inactive and are not added to `egress.registry`.
- User routes and `users.registry` are not changed.
- Interface tests use a temporary name: `v7rt*`.
- Runtime config is temporarily copied to `/etc/wireguard/v7rt*.conf`.
- Cleanup removes:
  - temporary interface;
  - temporary `/etc/wireguard/v7rt*.conf`.
- Sanitized config copy and result are stored root-only under:
  - `/opt/v7/admin/egress-draft-tests/<run_id>/`
- Raw private keys are not returned by API responses.
- Unsafe WireGuard options are blocked before runtime:
  - `PreUp`
  - `PostUp`
  - `PreDown`
  - `PostDown`
  - `SaveConfig`
  - `DNS`

## Live VPS Validation

VPS: `195.2.79.116`

Checks completed:

- Local compile: `python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper`
- Local diff check: `git diff --check`
- VPS compile: `python3 -m py_compile /usr/local/bin/v7-admin-api /usr/local/bin/v7-egress-draft-runtime-helper`
- Service restart: `systemctl restart v7-admin-api`
- Service health: `systemctl is-active v7-admin-api` returned `active`
- API health: `GET http://127.0.0.1:7080/health` returned `status=OK`

Live runtime test used a temporary WireGuard draft with a reserved TEST-NET endpoint.

Expected result for the fake endpoint:

- temporary interface starts;
- external IP test fails;
- cleanup succeeds.

Actual result:

- status: `FAIL_EXTERNAL_IP`
- mode: `temporary_interface_auto_cleanup`
- pool action: `still_not_added`
- route action: `none`
- cleanup: `OK`
- temporary interface removed: yes
- temporary `/etc/wireguard/v7rt*.conf` removed: yes
- secret redaction: OK

Registry check:

- Test draft id was not found in `/opt/v7/egress/state/egress.registry`.
- Test draft id was not found in `/opt/v7/egress/state/users.registry`.

Temporary test drafts and test runs were removed after validation.

## Next Step

Phase94 should connect successful runtime tests to quarantine service-matrix testing:

- if runtime external IP is present, run service matrix against the temporary interface/proxy;
- compare expected external IP;
- keep the draft in quarantine until service matrix passes;
- only after that prepare an explicit `Add to Pool` preview.
