# V7 Phase97: Egress enable readiness visibility

## Human Meaning

V7 Admin now explains whether a channel is technically ready to be enabled.

This matters after Phase96: a new channel can be added to the pool disabled, but
that does not automatically mean it has a runtime profile that can be started.

The admin now shows this before an operator presses `Enable`.

## Terms

- Egress: an outgoing VPN/proxy channel.
- Runtime profile: the real config file/profile used to start that channel.
- Enable readiness: whether V7 has enough runtime information to safely enable
  the channel later.
- Disabled channel: a channel listed in `egress.registry` with `enabled=0`.

## What Changed

Updated:

- `admin/v7-admin-api`

Added backend readiness helper:

```text
egress_runtime_readiness()
```

It checks:

- registry presence;
- enabled flag;
- protocol;
- egress type;
- interface name for interface-mode channels;
- expected runtime profile paths;
- whether an interface is currently up.

The overview API now includes:

```text
egress_runtime_readiness
```

The egress table now includes all registry channels, not only channels already
present in `v7-state.json`. This makes disabled channels visible.

The egress detail view now shows:

- `Enable Readiness`;
- readiness reason;
- profile path if found;
- per-check status table.

## Safety Model

This phase is read-only.

It does not:

- enable channels;
- change routes;
- move users;
- edit configs;
- restart V7 routing services.

## Local Validation

Compile:

```text
python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
```

Result:

```text
OK
```

Whitespace check:

```text
git diff --check
```

Result:

```text
OK
```

Functional readiness test:

```json
{
  "ready_status": "READY",
  "ready_enable": true,
  "blocked_status": "BLOCKED",
  "blocked_enable": false,
  "blocked_reason": "no config found in expected interface profile paths"
}
```

## VPS Validation

Deployed to:

```text
/usr/local/bin/v7-admin-api
```

Backup created before replacement:

```text
/usr/local/bin/v7-admin-api.bak.phase97.<timestamp>
```

Validation:

```text
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api
curl -fsS http://127.0.0.1:7080/health
```

Result:

```text
active
status=OK
```

VPS temporary-path readiness test:

```json
{
  "ready_status": "READY",
  "ready_enable": true,
  "blocked_status": "BLOCKED",
  "blocked_enable": false,
  "blocked_reason": "no config found in expected interface profile paths"
}
```

## Current Status

Phase97 is complete.

Operators can now see a channel before enabling it and understand whether it is:

- ready;
- blocked because runtime profile is missing;
- warning/unknown because not enough information is present.

## Next Step

Phase98 should add guarded enable precheck.

Human meaning:

- before applying `Enable`, V7 should run a final precheck;
- if the channel is blocked by readiness checks, the enable action should refuse
  to run;
- this protects users from being routed into a channel that exists in registry
  but cannot actually carry traffic.
