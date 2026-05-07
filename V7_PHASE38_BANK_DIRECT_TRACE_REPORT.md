# V7 Phase 38: Banking app direct-routing trace

Date: 2026-05-07

## Context

After fixing `.ru` and Yandex direct routing, the user reported that an online
bank app stopped working through V7.

The active iPhone client was detected as:

```text
10.0.0.3
```

## Added

### `/usr/local/bin/v7-app-domain-trace`

Read-only DNS trace helper:

```bash
v7-app-domain-trace 10.0.0.3 90 bank
```

It captures dnsmasq query logs for one client IP during a short reproduction
window and prints unique domains.

It does not inspect HTTPS contents, credentials, banking payloads, or app data.
It only observes DNS names resolved through V7 DNS.

## Trace Result

Domains observed during the banking app reproduction:

```text
alfa-mobile.alfabank.ru
metrics.alfabank.ru
pushserver.edna.id
app-analytics-services.com
www.google.com
firebaselogging-pa.googleapis.com
fitbitvestibuleshim-pa.googleapis.com
iphone-api.fitbit.com
```

Interpretation:

- `alfa-mobile.alfabank.ru` and `metrics.alfabank.ru` are already covered by
  broad `.ru` direct routing.
- `pushserver.edna.id` is a likely banking dependency for push/OTP/notification
  traffic and was not covered by `.ru`.
- Google/Fitbit domains looked like background phone/app traffic and were not
  added to banking direct routing.

## Changed

Added to `/etc/v7/direct/domains.conf`:

```text
alfabank.ru
edna.id
```

Then regenerated dnsmasq config and restarted dnsmasq:

```bash
v7-direct-render-dnsmasq
systemctl restart dnsmasq
```

## Validation

Commands run:

```bash
v7-direct-test-domain alfabank.ru 10.0.0.3
v7-direct-test-domain alfa-mobile.alfabank.ru 10.0.0.3
v7-direct-test-domain pushserver.edna.id 10.0.0.3
v7-system-check
```

Result:

- `alfabank.ru`: `DIRECT_READY`
- `alfa-mobile.alfabank.ru`: `DIRECT_READY`
- `pushserver.edna.id`: `DIRECT_READY`
- `dnsmasq`: active
- `v7-system-check`: `V7_RESULT=OK`

## Next If Still Failing

If the banking app still rejects the connection, the likely next cause is not
domain routing but IP reputation:

- The bank may reject datacenter/VPS IPs.
- In that case, the future solution is a dedicated `trusted_ru_egress` group:
  residential/home/RU egress for sensitive services, separate from generic
  direct routing and external VPN egresses.
