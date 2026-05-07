# V7 Admin Phase 52: Trusted RU Missing Batch

Date: 2026-05-07

## Goal

Make `TRUSTED_RU_SENSITIVE` diagnostics operationally usable without running the full slow probe set every time.

The problem found in Phase 51:

- a short diagnostic run for 1-2 domains overwrote the diagnostic state;
- untested domains then appeared as `MISSING_DIAGNOSTIC`;
- the admin needed a safe way to fill missing probes gradually.

## Implemented

### Preserve Existing Diagnostic State

Updated:

- `/usr/local/bin/v7-trusted-ru-diagnostic`

The diagnostic now preserves previous probe lines for domains that were not part of the current run.

This allows small scoped runs such as:

```text
v7-trusted-ru-diagnostic alfabank.ru
```

without deleting existing results for:

- `www.gosuslugi.ru`
- `alfa-mobile.alfabank.ru`
- other sensitive domains.

### Missing Batch Command

Added:

- `/usr/local/bin/v7-trusted-ru-refresh-missing`

Usage:

```text
v7-trusted-ru-refresh-missing --limit 2
```

Behavior:

1. Reads `/opt/v7/egress/state/trusted-ru-decision.state`.
2. Selects domains currently marked `MISSING_DIAGNOSTIC`.
3. Runs diagnostics only for a small batch.
4. Recalculates full decision preview.
5. Saves JSON state.

The limit is clamped to `1..6` to avoid accidental heavy runs.

### Admin UI/API

Updated:

- `/usr/local/bin/v7-admin-api`

Added button:

- `Run Missing Batch`

Added action:

- `/api/actions/trusted-ru-refresh-missing`

This action:

- requires operator access;
- is audit-logged;
- is blocked by Admin Safe Mode;
- does not change routes, users, nftables marks, or active egress assignments.

### JSON State

Updated:

- `/usr/local/bin/v7-state-json`

`/state.trusted_ru_diagnostic` now also includes:

- `missing`

### Safe Run

Updated:

- `/usr/local/bin/v7-safe-run`

Allowed read-only helper:

- `v7-trusted-ru-refresh-missing`

## VPS Validation

Installed on VPS `195.2.79.116`.

Executed:

```text
v7-trusted-ru-refresh-missing --limit 1
```

Selected domain:

```text
selected_domains=alfabank.ru
```

Probe result:

```text
alfabank.ru
direct: 000 / TLS FAIL
vless: 200
awg: 200
decision: USE_TEMP_VLESS
```

Decision summary after run:

```text
count=11
direct_ok=0
temporary_vless=2
awg=0
blocked=1
missing=8
V7_TRUSTED_RU_DECISION=NEEDS_ATTENTION
```

Admin/API:

```text
OVERVIEW_OK NEEDS_ATTENTION 11 8
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

## Result

Sensitive RU probing is now incremental:

- no broad rerun is required for every admin action;
- old probe evidence is preserved;
- missing domains can be filled gradually;
- the system remains in preview mode and does not change live routing.

