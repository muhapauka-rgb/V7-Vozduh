# P2.8 Runtime vs Local Diff

## Proven Differences

| Area | Runtime | Local |
| --- | --- | --- |
| Admin availability | Public `/health` OK | Local `127.0.0.1:7080` not listening |
| Admin source | Running behind Caddy as `V7Admin/0.1 Python/3.14.4` | `admin/v7-admin-api` dirty with P2.7 changes |
| Runtime state paths | Historical production uses `/opt/v7` and `/etc/v7` | Local macOS has no `/opt/v7` or `/etc/v7` |
| System manager | Historical production uses systemd | Local machine uses launchd |
| Docker | Not production evidence | Local Docker runs unrelated `rent_*` containers |

## Runtime-Only / Production-Only Indicators

Historical docs show production uses `/usr/local/bin/v7-*`, `/opt/v7`, `/etc/v7`, systemd services, Caddy, public gateway, proxy/sing-box, and multiple state files. These are not present locally as live runtime paths.

## Local-Only Indicators

Local repository has uncommitted/untracked P2.1-P2.7 implementation work and docs. These are not proven deployed to runtime.

## Verdict

runtime_local_aligned=false

Runtime and local repository are not aligned as live systems. Exact source-level diff is unresolved because runtime source hashes were not collected.
