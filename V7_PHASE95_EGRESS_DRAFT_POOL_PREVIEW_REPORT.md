# V7 Phase95: Egress Draft Add-to-Pool Preview

Date: 2026-05-08

## Human Meaning

This phase adds a preview before a new VPN channel can enter the active V7 pool.

It does not add the channel yet.

It only answers:

- what would V7 add;
- where would V7 write it;
- what backups would be needed;
- what is still blocking the channel from being added.

## Terms

- Pool: the active list of egress channels that V7 may use for users.
- Draft: a saved VPN config that is not active yet.
- Registry: the text file where active egress channels are listed.
- Registry line: the exact line that would be written into `egress.registry`.
- Enabled 0: the channel would start disabled, so users would not use it until an operator explicitly enables it.

## What Changed

- Added admin API action: `/api/actions/egress-draft-pool-preview`.
- Added admin UI button: `Pool Preview`.
- Preview returns:
  - proposed egress id;
  - protocol;
  - type;
  - interface/test mode;
  - proposed registry line;
  - readiness state;
  - blockers;
  - files that would be backed up;
  - files that would and would not change.

## Safety Model

- Preview is read-only.
- No registry files are changed.
- Users are not moved.
- Routes are not changed.
- Secrets are not returned.
- A draft is not considered ready unless:
  - preflight passed;
  - runtime test passed;
  - quarantine test passed;
  - proposed egress id does not already exist.

## Live VPS Validation

VPS: `195.2.79.116`

Checks completed:

- Local compile: `python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper`
- Local diff check: `git diff --check`
- VPS compile: `python3 -m py_compile /usr/local/bin/v7-admin-api`
- Service restart: `systemctl restart v7-admin-api`
- Service health: `systemctl is-active v7-admin-api` returned `active`
- API health: `GET http://127.0.0.1:7080/health` returned `status=OK`

Live preview test result:

- ready: `false`
- blockers:
  - `preflight_not_passed`
  - `runtime_not_passed`
  - `quarantine_not_passed`
- pool action: `preview_only_not_added`
- secret redaction: OK

Registry check:

- Test draft id was not found in `/opt/v7/egress/state/egress.registry`.
- Test draft id was not found in `/opt/v7/egress/state/users.registry`.

Temporary test draft was removed after validation.

## Next Step

Phase96 should add guarded `Add to Pool Apply`.

Human meaning:

- only a draft with a successful quarantine can be applied;
- V7 must create backups first;
- V7 must add the new channel disabled by default;
- users must not be moved automatically;
- enabling the channel should remain a separate explicit action.
