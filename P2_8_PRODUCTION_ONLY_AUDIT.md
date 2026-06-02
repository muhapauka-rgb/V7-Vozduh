# P2.8 Production-Only Audit

## Production-Only Categories

Historical production evidence identifies these production-only or runtime-only categories:

- `/usr/local/bin/v7-*` deployed executables
- `/etc/systemd/system/v7-*.service`
- `/etc/systemd/system/v7-*.timer`
- `/opt/v7/egress/state/*`
- `/opt/v7/events/*`
- `/opt/v7/audit/*`
- `/etc/v7/*`
- Caddy public ingress
- proxy/sing-box runtime
- runtime state and profile delivery token files

## Current Local Repository Coverage

Local repo contains many source equivalents:

- `admin/v7-admin-api`
- `tools/v7-*`
- `tools/runtime-support/v7-*`
- `systemd/v7-*.service`
- `systemd/v7-*.timer`

But local repo does not contain production live state and does not prove deployed runtime content.

## Known Historical Risk

Prior reports mention production-only lineage gaps and stale executable cleanup:

- production `/usr/local/bin/v7*` inventory was historically large
- some production-only tools previously lacked clean repository lineage
- `/usr/local/bin/v7-admin-api.tmp` was archived as stale

## Verdict

production_only_audited=true

Production-only risk remains unresolved until a fresh runtime manifest and source hash comparison are collected.
