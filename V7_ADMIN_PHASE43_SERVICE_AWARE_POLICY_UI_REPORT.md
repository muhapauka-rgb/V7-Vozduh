# V7 Admin Phase 43: Service-aware policy UI

Date: 2026-05-07

## Goal

Expose the new service-aware route policy foundation in the admin panel without
enabling live service-aware marks.

The admin now shows:

- route classes;
- route mode;
- active path;
- mark/table;
- domain counts;
- temporary status;
- policy apply preview state.

## Changed

### `/usr/local/bin/v7-admin-api`

Added a new dashboard section:

```text
Service-aware Policy
```

It renders data from:

```text
/opt/v7/egress/state/v7-state.json
```

Fields:

```text
route_classes
policy_apply_preview
```

### Admin action

Added:

```text
POST /api/actions/policy-route-preview
```

This action runs:

```bash
v7-policy-apply --apply
```

Important:

- it refreshes preview state;
- it does not enable live marks;
- it does not change user routes;
- it writes audit log through the existing admin action path.

Minimum role:

```text
viewer
```

because this is an operational preview, not a live routing change.

### HEAD check

`HEAD /login` now returns `200 OK`, so lightweight HTTP health checks do not
mistake the login page for a missing endpoint.

## Sensitive RU visibility

The admin now makes this visible:

```text
TRUSTED_RU_SENSITIVE
mode=egress
active_egress=vless
temporary=1
local_direct=TCP_TIMEOUT_BEFORE_TLS
```

This keeps the architectural truth clear:

- VLESS is only the current temporary path for sensitive RU;
- direct from the current VPS IP is not accepted by some sensitive services;
- no second server/mobile/home egress is being introduced.

## Validation

Commands run on VPS:

```bash
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
curl -sS -I http://127.0.0.1:7080/login
v7-killswitch-check
v7-system-check
```

Results:

- `HTTP /login`: `200 OK`
- `v7-killswitch-check`: `OK`
- `v7-system-check`: `OK`
- `v7-admin-api`: active

Current live routes stayed unchanged:

```text
10.0.0.2 -> awg2 table 100
10.0.0.3 -> vless table 101
```

## Next Phase

Add a read-only policy diagnostics page/action for domain-level checks:

```text
domain -> route class -> direct engine result -> desired path
```

This will let the operator test `gosuslugi.ru`, banks, Yandex, YouTube, and
future apps from the admin before any live policy rollout.
