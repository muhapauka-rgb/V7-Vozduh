# P2.8.1 Runtime Provenance

Project: V7 Vozduh
Block: P2.8.1
Mode: Audit / Discovery / Version Governance
Date: 2026-05-31

## Scope

This file records read-only runtime provenance collected from the production host.

Forbidden actions were not performed: no runtime mutation, no user movement, no autoswitch apply, no routing apply, no policy apply, no killswitch mutation, no trusted/direct RU mutation, no execution engine or hooks, no push, no merge, no rebase, no deploy, no systemd change.

## Runtime Identity

| Field | Value |
| --- | --- |
| Hostname | `v3119922.hosted-by-vdsina.ru` |
| Kernel | `Linux v3119922.hosted-by-vdsina.ru 7.0.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC Mon Apr 13 11:09:53 UTC 2026 x86_64 GNU/Linux` |
| Audit time | `2026-05-31T18:50:03+03:00` |
| Collection mode | SSH read-only shell commands |

## Runtime Service Provenance

| Unit | Runtime state | Fragment | ExecStart |
| --- | --- | --- | --- |
| `v7-admin-api.service` | active/running | `/etc/systemd/system/v7-admin-api.service` | `/usr/local/bin/v7-admin-api` |
| `v7-public-gateway.service` | active/running | `/etc/systemd/system/v7-public-gateway.service` | `/usr/local/bin/v7-public-gateway` |
| `v7-api.service` | active/running | `/etc/systemd/system/v7-api.service` | `/usr/local/bin/v7-api` |
| `v7-client-speed-api.service` | active/running | `/etc/systemd/system/v7-client-speed-api.service` | `/usr/local/bin/v7-client-speed-api` |
| `v7-benchmark.service` | active/running | `/etc/systemd/system/v7-benchmark.service` | shell loop calling `v7-egress-benchmark-all` |
| `v7-health.service` | active/running | `/etc/systemd/system/v7-health.service` | shell loop calling history/stability/load/diagnose/state save tools |
| `v7-routing-sync.service` | active/exited | `/etc/systemd/system/v7-routing-sync.service` | `/usr/local/bin/v7-routing-sync` |
| `v7-killswitch.service` | active/exited | `/etc/systemd/system/v7-killswitch.service` | `/usr/local/bin/v7-killswitch-enable` |
| `v7-direct-autosync.service` | inactive/dead | `/etc/systemd/system/v7-direct-autosync.service` | `/usr/local/bin/v7-direct-auto-sync` |
| `v7-users-autoswitch.service` | inactive/dead | `/etc/systemd/system/v7-users-autoswitch.service` | `/usr/local/bin/v7-users-autoswitch --apply` |
| `v7-autoswitch-planner.service` | inactive/dead | `/etc/systemd/system/v7-autoswitch-planner.service` | `/usr/local/bin/v7-users-autoswitch` |
| `v7-service-matrix-refresh.service` | inactive/dead | `/etc/systemd/system/v7-service-matrix-refresh.service` | `/usr/local/bin/v7-service-matrix-refresh-all` |
| `v7-egress-quality-compact.service` | inactive/dead | `/etc/systemd/system/v7-egress-quality-compact.service` | `/usr/local/bin/v7-egress-quality-compact` |
| `v7-telegram-sentinel.service` | inactive/dead | `/etc/systemd/system/v7-telegram-sentinel.service` | `/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch` |
| `v7-traffic-collector.service` | inactive/dead | `/etc/systemd/system/v7-traffic-collector.service` | `/usr/local/bin/v7-traffic-snapshot --collect` |

## Runtime Listeners

Read-only `ss` output identified listeners:

| Address | Owner |
| --- | --- |
| `127.0.0.1:7080` | `python3 /usr/local/bin/v7-admin-api` |
| `0.0.0.0:80` | `python3 /usr/local/bin/v7-public-gateway` |
| `127.0.0.1:7077` | `python3 /usr/local/bin/v7-api` |
| `10.0.0.1:7090` | `python3 /usr/local/bin/v7-client-speed-api` |
| `0.0.0.0:1443` | `sing-box` public candidate |
| `0.0.0.0:1445` | `sing-box` AWG/SMUX runtime |
| `*:443` | `caddy` |

## Provenance Gaps

Runtime files are proven by path, size, mtime, and hash. Their originating Git commit, deployment command, deploy actor, and signed release manifest remain UNKNOWN.

runtime_provenance_complete=false
