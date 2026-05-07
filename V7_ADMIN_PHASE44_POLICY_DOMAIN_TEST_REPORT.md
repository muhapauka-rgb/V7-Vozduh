# V7 Admin Phase 44: Policy domain test

Date: 2026-05-07

## Goal

Add an admin-side diagnostic for service-aware routing decisions:

```text
domain -> route class -> current direct engine -> desired path
```

This is the next step toward handling many apps without manually hardcoding
every single website after a user reports a failure.

## Changed

### Admin UI

The `Service-aware Policy` section now has:

- domain input;
- user IP input;
- `Test Domain` button.

The result is shown in the same policy preview console.

### Admin API

Added:

```text
POST /api/actions/policy-domain-test
```

It runs:

```bash
v7-policy-test-domain <domain> <user_ip>
```

Minimum role:

```text
viewer
```

This action is diagnostic only and does not change routes.

## Validation

Command run on VPS:

```bash
v7-policy-test-domain www.gosuslugi.ru 10.0.0.3
```

Important result:

```text
route_class=TRUSTED_RU_SENSITIVE
mode=egress
active_egress=vless
temporary=1
local_direct=TCP_TIMEOUT_BEFORE_TLS
decision=SERVICE_AWARE_SENSITIVE
desired_path=vless
reason=sensitive_app_overrides_broad_direct
```

The current direct engine still sees the resolved Gosuslugi IPs as direct-ready
because they are in the broad direct set. The service-aware policy layer now
correctly overrides that classification for sensitive RU.

## Health Checks

Commands run:

```bash
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
curl -sS -I http://127.0.0.1:7080/login
v7-system-check
```

Results:

- `HTTP /login`: `200 OK`
- `v7-system-check`: `OK`

Live user routes stayed unchanged.

## Next Phase

Create a policy diagnostics matrix:

```text
Gosuslugi / banks / Yandex / Ozon / YouTube / Telegram
```

For each domain/app group, show:

- route class;
- desired path;
- current direct-engine result;
- server direct reachability;
- egress reachability;
- operator recommendation.
