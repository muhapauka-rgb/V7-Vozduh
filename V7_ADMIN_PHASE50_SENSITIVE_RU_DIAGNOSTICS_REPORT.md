# V7 Admin Phase 50: Sensitive RU Diagnostics

Date: 2026-05-07

## Goal

Add a controlled diagnostics block for sensitive Russian services such as Gosuslugi, ESIA, and banks.

This does not change user routing and does not enable live service-aware marks. It is an evidence layer for deciding how `TRUSTED_RU_SENSITIVE` should work without relying blindly on the temporary VLESS path.

## Implemented

### Server diagnostic

Updated:

- `/usr/local/bin/v7-trusted-ru-diagnostic`

It now checks each sensitive domain through:

- direct VPS public interface `ens3`;
- direct OpenSSL TLS handshake;
- optional browser-like direct probe if `curl-impersonate` tooling is installed;
- VLESS SOCKS path `127.0.0.1:1080`;
- AWG interface path `awg2`.

The script writes:

- `/opt/v7/egress/state/trusted-ru-diagnostic.state`

### JSON state

Updated:

- `/usr/local/bin/v7-state-json`

`/state` now includes:

```json
"trusted_ru_diagnostic": {
  "updated": "...",
  "direct_if": "ens3",
  "socks": "127.0.0.1:1080",
  "awg_if": "awg2"
}
```

### Admin UI/API

Updated:

- `/usr/local/bin/v7-admin-api`

Added:

- `Sensitive RU Diagnostics` dashboard section;
- `Run Check` button;
- per-domain table with:
  - direct HTTP;
  - direct TLS/OpenSSL;
  - browser-like test availability/result;
  - VLESS result;
  - AWG result;
  - reason/error;
- authenticated action:
  - `/api/actions/trusted-ru-diagnostic`

This action requires operator-level access and is audit-logged.

## VPS Validation

Installed and tested on VPS `195.2.79.116`.

Admin:

```text
systemctl is-active v7-admin-api
active

curl /login
LOGIN_HTTP=200

overview()
OVERVIEW_OK True OK
TRUSTED_ITEMS 11
```

Short live test:

```text
v7-trusted-ru-diagnostic www.gosuslugi.ru alfa-mobile.alfabank.ru
V7_TRUSTED_RU_DIAGNOSTIC=OK
```

Observed:

- `www.gosuslugi.ru`
  - direct via `ens3`: timeout before TLS;
  - OpenSSL direct: fail / timeout;
  - browser-like direct: unavailable because curl-impersonate is not installed;
  - VLESS/AWG curl checks also timed out for this exact host in this run.
- `alfa-mobile.alfabank.ru`
  - direct via `ens3`: timeout before TLS;
  - OpenSSL direct: fail / timeout;
  - VLESS: HTTP 404 with successful TCP/TLS path;
  - AWG: HTTP 404 with successful TCP/TLS path.

Final health checks:

```text
v7-killswitch-check
V7_KILLSWITCH_CHECK=OK

v7-system-check
V7_RESULT=OK
```

## Interpretation

For at least the tested Alfa path, the direct public VPS IP is blocked before TLS, while VPN egress paths can establish TCP/TLS. This supports the current `TRUSTED_RU_SENSITIVE` architecture: sensitive RU traffic must be handled by a separate route class and should not simply inherit broad `.ru` direct routing.

The next step is to improve the trusted-RU decision model and keep it in preview until we have a stable non-temporary local strategy.

