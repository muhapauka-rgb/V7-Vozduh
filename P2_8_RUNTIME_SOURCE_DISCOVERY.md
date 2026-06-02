# P2.8 Runtime Source Discovery

## Local Source Files That Define Runtime

Local repository runtime source candidates:

- `admin/v7-admin-api`
- `admin_core/operator_observability.py`
- `admin_core/operator_execution.py`
- `admin_core/events.py`
- `admin_core/registry_readers.py`
- `admin_core/sanitize.py`
- `admin_core/time.py`
- `tools/v7-*`
- `tools/runtime-support/v7-*`
- `systemd/*.service`
- `systemd/*.timer`
- `systemd/drafts/*`

## Runtime Paths Declared By Source

Important source defaults:

- Admin host/port: `V7_ADMIN_HOST` default `127.0.0.1`, `V7_ADMIN_PORT` default `7080`
- State root: `/opt/v7/egress/state`
- Event root: `/opt/v7/events`
- Audit file: `/opt/v7/audit/audit.jsonl`
- Auth file: `/etc/v7/admin/auth.json`
- Policy file: `/etc/v7/policy.json`
- Org policy file: `/etc/v7/org-egress-policy.json`
- Runtime executable convention: `/usr/local/bin/v7-*`

## Historical Runtime Source Evidence

Historical docs identify production runtime source as:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-public-gateway`
- `/usr/local/bin/v7-client-speed-api`
- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-telegram-sentinel`
- `/usr/local/bin/v7-service-matrix-refresh-all`
- `/usr/local/bin/v7-egress-quality-compact`

## Current Verification Limit

Public checks prove that Admin and Public Gateway are running, but do not expose source hashes. This audit did not SSH into production and did not authenticate into admin because the block is discovery-only and must avoid unnecessary runtime side effects.

## Verdict

Runtime source discovery is partial:

- runtime_source_files_identified=true
- runtime_source_hash_verified=false
- runtime_local_source_equivalence_proven=false
