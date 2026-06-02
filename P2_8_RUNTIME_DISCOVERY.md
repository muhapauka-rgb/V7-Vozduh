# P2.8 Runtime Discovery

Project: V7 Vozduh
Block: P2.8
Mode: Read-only audit

## Current Local Execution Environment

- Host inspected from this workspace: macOS Darwin `MacBook-Air-Portal.local`
- Init system: `launchd`, not Linux `systemd`
- Local workspace: `/Users/ponch/Documents/New project`
- Local `/opt/v7` and `/etc/v7` are not present; `/opt` exists only as a root-owned macOS directory
- Local `127.0.0.1:7080/health` is not listening
- Local Docker is running unrelated `rent_*` containers, not V7 containers:
  - `rent_api` on host port `8001`
  - `rent_ocr` on host port `8002`
  - `rent_bot`
  - `rent_db` on host port `5433`

## Public Runtime Evidence

Read-only public checks succeeded:

- `https://v7-admin.195-2-79-116.sslip.io/health`
  - `status=OK`
  - `auth_configured=true`
  - `local_only=true`
  - server headers include `V7Admin/0.1 Python/3.14.4`
- `https://v7-admin.195-2-79-116.sslip.io/admin-v2`
  - returns `303 Location: /login`
  - served through `Caddy`
- `http://195.2.79.116/`
  - returns `404`
  - server header: `V7PublicGateway/0.1 Python/3.14.4`
- `http://195.2.79.116:7090/health`
  - connection refused from this network path

## Historical Runtime Snapshot Evidence

Existing docs say the production runtime previously had:

- Ubuntu/KVM host `v3119922.hosted-by-vdsina.ru`
- `v7-admin-api.service active/running`
- `process=python3 /usr/local/bin/v7-admin-api`
- `listener=127.0.0.1:7080`
- public gateway on `0.0.0.0:80`
- Caddy on `*:443`
- client speed API on `10.0.0.1:7090`
- multiple V7 services and timers active

Historical evidence lives in:

- `docs/track7/truth-snapshot/ADMIN_API_RUNTIME_SNAPSHOT.md`
- `docs/track7/truth-snapshot/PROXY_RUNTIME_SNAPSHOT.md`
- `docs/track7/truth-snapshot/RUNTIME_IDENTITY_SNAPSHOT.md`

## Active Components Proven Now

Proven from public checks:

- V7 Admin public ingress exists
- V7 Admin health endpoint responds
- V7 Public Gateway responds on port 80
- Caddy fronts admin over HTTPS

Not proven now:

- exact runtime source hash
- exact `/usr/local/bin/v7-admin-api` content
- exact active systemd service list
- exact active timer list
- exact runtime state file contents

## Verdict

runtime_discovered=true

Runtime is alive, but exact source equivalence is not proven from this workstation without SSH or authenticated runtime introspection.

runtime_mutation_performed=false
systemd_changed=false
deploy_performed=false
