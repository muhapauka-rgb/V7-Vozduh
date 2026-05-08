# V7 Phase94: Egress Draft Quarantine Test

Date: 2026-05-08

## Human Meaning

This phase adds a safe "quarantine" step for a new VPN channel.

Quarantine means:

- the channel is still not used by users;
- V7 temporarily starts it only for testing;
- V7 checks whether the internet sees a real external IP through it;
- only if that works, V7 runs a small service check list;
- V7 then removes the temporary interface/config;
- the channel remains outside the active pool.

## Terms

- Draft: a saved VPN config that is not active yet.
- Preflight: static checks before starting anything.
- Runtime test: temporary start of the draft tunnel.
- Quarantine test: runtime test plus service checks, still isolated from users.
- Service matrix: a small table of important services and whether the channel can reach them.
- Pool: the active list of egress channels available to V7 routing.

## What Changed

- Added admin action: `/api/actions/egress-draft-quarantine-run`.
- Added admin UI button: `Quarantine`.
- Extended `v7-egress-draft-runtime-helper` with quarantine mode.
- Quarantine mode runs service checks only after external IP succeeds.
- If external IP fails, service checks are skipped and the draft stays blocked.

## Safety Model

- Requires explicit confirmation: `RUN_QUARANTINE_TEST`.
- Requires previous preflight `PASS`.
- Does not modify `egress.registry`.
- Does not modify `users.registry`.
- Does not switch users.
- Uses temporary interface names: `v7rt*`.
- Uses temporary configs: `/etc/wireguard/v7rt*.conf`.
- Cleanup removes temporary interface and config.
- Raw private keys are not returned in API output.

## Live VPS Validation

VPS: `195.2.79.116`

Checks completed:

- Local compile: `python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper`
- Local diff check: `git diff --check`
- VPS compile: `python3 -m py_compile /usr/local/bin/v7-admin-api /usr/local/bin/v7-egress-draft-runtime-helper`
- Service restart: `systemctl restart v7-admin-api`
- Service health: `systemctl is-active v7-admin-api` returned `active`
- API health: `GET http://127.0.0.1:7080/health` returned `status=OK`

Live quarantine test used a temporary WireGuard draft with a reserved TEST-NET endpoint.

Expected result:

- temporary interface can be created;
- external IP check fails because the peer is fake;
- service matrix is skipped;
- cleanup succeeds.

Actual result:

- status: `FAIL_EXTERNAL_IP`
- quarantine status: `BLOCKED`
- requested mode: `quarantine`
- service matrix: `SKIPPED`
- cleanup: `OK`
- pool action: `still_not_added`
- route action: `none`
- secret redaction: OK

Cleanup verification:

- temporary interface removed: yes
- temporary `/etc/wireguard/v7rt*.conf` removed: yes
- test draft was not found in `egress.registry`
- test draft was not found in `users.registry`

Temporary test drafts and runs were removed after validation.

## Next Step

Phase95 should add `Add to Pool Preview`.

Human meaning:

- after a real draft passes quarantine, V7 should show exactly what would be added;
- it should not activate automatically;
- the operator must explicitly approve;
- V7 should create backups before changing registry files.
