# V7 Admin Access Reliability Report

Date: 2026-05-12

## What was checked

- `v7-admin-api` service status.
- `v7-public-gateway` service status.
- `caddy` service status.
- Local admin endpoint on `127.0.0.1:7080`.
- Public admin endpoint on `https://v7-admin.195-2-79-116.sslip.io`.
- HTTP access to the admin hostname.

## Finding

The admin service was running. The confusing part was access behavior:

- `HEAD /admin-v2` returned `404`, which made simple availability checks look broken.
- The public admin should be opened through HTTPS.
- Port `7080` stays local-only by design and should not be opened to the internet.

## Changes

- `admin/v7-admin-api`
  - `HEAD /admin-v2` now follows the same access logic as the page itself.
  - If auth is enabled and there is no session, it returns `303` to `/login`.
  - This removes the false "admin is down" signal from HEAD checks.

- `public/v7-public-gateway`
  - HTTP requests to `v7-admin.195-2-79-116.sslip.io` now redirect to HTTPS.
  - The public connect/profile gateway behavior remains unchanged for normal user links.

## Validation

On the VPS:

```bash
systemctl is-active v7-admin-api v7-public-gateway caddy
```

Result:

```text
active
active
active
```

Local admin HEAD check:

```bash
curl -I http://127.0.0.1:7080/admin-v2
```

Result:

```text
HTTP/1.0 303 See Other
Location: /login
```

Public admin GET check:

```bash
curl -L https://v7-admin.195-2-79-116.sslip.io/admin-v2
```

Result:

```text
final=https://v7-admin.195-2-79-116.sslip.io/login
```

HTTP redirect check:

```bash
curl -I http://v7-admin.195-2-79-116.sslip.io/admin-v2
```

Result:

```text
HTTP/1.0 308 Permanent Redirect
Location: https://v7-admin.195-2-79-116.sslip.io/admin-v2
```

## Operator Note

Use this admin URL:

```text
https://v7-admin.195-2-79-116.sslip.io/login
```

Do not use `http://195.2.79.116:7080` from outside. Port `7080` is intentionally bound to localhost on the VPS.
