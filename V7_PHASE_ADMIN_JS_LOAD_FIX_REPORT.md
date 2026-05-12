# V7 Admin JS Load Fix Report

Date: 2026-05-12

## Problem

The admin page opened, but the workspace stayed in a partial loading state:

- top status showed loading;
- topology/users/channels blocks stayed empty;
- no useful error was shown to the operator.

## Root Cause

The admin HTML loaded, but browser JavaScript stopped during parsing because several regex literals were over-escaped inside the embedded script.

That means the page shell rendered, but `load()`, `/api/session`, `/api/overview`, and all render functions never finished.

## Fix

- Fixed invalid JavaScript regex escaping in the i18n/technical-output helpers.
- Added a guarded load failure path so API errors show a visible retry block instead of endless loading.
- Kept the VPN runtime, routing, kill switch and V7 services untouched.

## Validation

Local checks:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m py_compile admin/v7-admin-api
git diff --check
```

Embedded browser script check:

```text
script syntax OK
```

VPS checks:

```bash
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api caddy
curl https://v7-admin.195-2-79-116.sslip.io/admin-v2
curl http://127.0.0.1:7080/health
```

Result:

```text
v7-admin-api active
caddy active
admin endpoint reachable
health OK
```

## Operator Note

Open or hard-refresh:

```text
https://v7-admin.195-2-79-116.sslip.io/admin-v2
```

If the browser still shows the old half-loaded screen, use hard refresh because the broken JavaScript may still be in the current tab memory.
