# V7 Admin Phase 51: Trusted RU Decision Preview

Date: 2026-05-07

## Goal

Turn raw `TRUSTED_RU_SENSITIVE` diagnostics into a clear, read-only route decision preview.

This is still not live service-aware routing. It does not change users, routing tables, nftables marks, or active egress assignments.

## Implemented

### New CLI

Added:

- `/usr/local/bin/v7-trusted-ru-decision`

The command reads:

- `/opt/v7/egress/state/trusted-ru-diagnostic.state`
- `/etc/v7/policy/trusted_ru_sensitive_domains.conf`

It writes:

- `/opt/v7/egress/state/trusted-ru-decision.state`

Supported output decisions:

- `DIRECT_OK`
- `BROWSER_LIKE_DIRECT_OK`
- `USE_TEMP_VLESS`
- `USE_AWG`
- `NO_SAFE_PATH`
- `MISSING_DIAGNOSTIC`

Overall states:

- `LOCAL_DIRECT_READY`
- `TEMPORARY_EGRESS_REQUIRED`
- `NEEDS_ATTENTION`
- `UNKNOWN`

### Admin UI/API

Updated:

- `/usr/local/bin/v7-admin-api`

The `Sensitive RU Diagnostics` panel now shows:

- overall decision;
- per-domain decision;
- selected preview path;
- direct/VLESS/AWG probe values;
- reason.

Added action:

- `/api/actions/trusted-ru-decision`

This action is read-only, viewer-accessible, and audit-logged.

The existing diagnostic action now also refreshes the decision preview after a successful run.

### JSON state

Updated:

- `/usr/local/bin/v7-state-json`

`/state` now exposes decision summary under `trusted_ru_diagnostic`:

- `decision_updated`
- `decision`
- `direct_ok`
- `temporary_vless`
- `awg`
- `blocked`

### Safe Run

Updated:

- `/usr/local/bin/v7-safe-run`

Allowed read-only command:

- `v7-trusted-ru-decision`

## VPS Validation

Installed on VPS `195.2.79.116`.

Decision preview for two fresh test domains:

```text
www.gosuslugi.ru                 NO_SAFE_PATH       none
alfa-mobile.alfabank.ru          USE_TEMP_VLESS     vless

V7_TRUSTED_RU_DECISION=NEEDS_ATTENTION
```

Full trusted list preview:

```text
count=11
direct_ok=0
temporary_vless=1
awg=0
blocked=1
missing=9
V7_TRUSTED_RU_DECISION=NEEDS_ATTENTION
```

Admin runtime:

```text
OVERVIEW_OK NEEDS_ATTENTION 11 1 9
systemctl is-active v7-admin-api
active
LOGIN_HTTP=200
```

Final health:

```text
v7-killswitch-check
V7_KILLSWITCH_CHECK=OK

v7-system-check
V7_RESULT=OK
```

## Interpretation

The admin panel now separates three layers:

1. Domain group membership.
2. Raw reachability diagnostics.
3. Read-only routing decision preview.

This is the right staging model for a large V7 architecture: no blind live changes, no over-trusting temporary VLESS, and no pretending that direct VPS egress can solve sensitive RU when probes show timeout before TLS.

