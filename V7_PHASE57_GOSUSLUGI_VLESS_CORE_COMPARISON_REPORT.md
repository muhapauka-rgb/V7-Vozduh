# V7 Phase 57: Gosuslugi VLESS Core Comparison

Date: 2026-05-07

## Goal

Diagnose why Gosuslugi does not open through the V7 path when the sensitive RU policy correctly routes it through `vless`.

The key question was whether the failure is caused by the current V7 `sing-box` client implementation, because the same VLESS profile reportedly works when used directly from the phone.

## Current Verified State

- `sing-box` is active.
- `v7-system-check` returns `V7_RESULT=OK`.
- User `10.0.0.3` is assigned to `vless`.
- `ip route get` for `10.0.0.3` uses table `101` and `dev tun0`.
- Sensitive RU policy classifies `www.gosuslugi.ru` as `TRUSTED_RU_SENSITIVE`.
- Broad `.ru` direct routing excludes sensitive domains.
- Gosuslugi traffic is not allowed to fall into direct `ens3` by the broad RU rule.

## Experiments Completed

### 1. sing-box TLS record fragmentation

An isolated route rule was temporarily tested for current Gosuslugi IPs with `tls_record_fragment`.

Result:

- `sing-box check` passed.
- `ifconfig.me` through VLESS still returned `77.110.103.131`.
- User flow still did not open Gosuslugi.
- The experiment was rolled back.

### 2. sing-box override destination

An isolated route rule was temporarily tested for current Gosuslugi IPs with `override_address=www.gosuslugi.ru` and `override_port=443`.

Result:

- `sing-box check` passed.
- `ifconfig.me` through VLESS still returned `77.110.103.131`.
- User flow still did not open Gosuslugi.
- The experiment was rolled back.

### 3. Isolated Xray-core lab client

Installed official Xray-core `v26.3.27` as a lab binary only:

- Path: `/opt/v7-lab/xray/xray`
- Config: `/etc/v7-lab/xray/config.json`
- Local SOCKS: `127.0.0.1:1082`
- No system service was enabled.
- No active V7 routing was changed.

Result:

- Xray config validation passed.
- `curl --socks5-hostname 127.0.0.1:1082 https://ifconfig.me` returned `77.110.103.131`.
- This proves the same VLESS Reality profile works through Xray for generic internet traffic.

Gosuslugi checks through Xray:

- `gosuslugi.ru`: timeout
- `www.gosuslugi.ru`: timeout
- `esia.gosuslugi.ru`: timeout
- `lk.gosuslugi.ru`: timeout
- `gu-st.ru`: HTTP 403, so the VLESS path itself can reach at least part of the Gosuslugi static/service domain set.

The same Gosuslugi checks through current `sing-box` showed the same pattern:

- main Gosuslugi/ESIA domains timed out
- `gu-st.ru` returned HTTP 403

## Live Trace Result

When tracing `10.0.0.3` for `www.gosuslugi.ru`, the latest run captured no Gosuslugi traffic at all. This likely means the phone was not using the V7 WireGuard profile during that specific trace window, or the target page was not reloaded while the trace was active.

Earlier confirmed trace showed:

- traffic path: `wg0 -> tun0`
- no direct `ens3` leak
- TCP payload was observed
- the application closed or did not receive the expected TLS response

## Interpretation

This is no longer a simple `.ru direct` bug:

- Direct `.ru` capture was fixed.
- Sensitive RU is excluded from broad direct.
- V7 routes sensitive RU to `vless`.
- The server does not leak sensitive traffic to `ens3`.

This is also not proven to be only a `sing-box` client bug:

- Xray-core with the same VLESS Reality profile also times out for the main Gosuslugi/ESIA domains from the VPS lab.

The most likely explanation is that the phone's direct VLESS app is not a perfect equivalent to the V7 path for these domains. Possible reasons:

- the phone app may have its own routing rules and may send Russian sensitive domains directly from the phone even while generic sites use VLESS;
- the phone app may use a different DNS path for these domains;
- the phone app may use another core/profile behavior not present in the exported V7 profile;
- main Gosuslugi/ESIA domains may reject or blackhole the route behind `77.110.103.131` for server-originated proxy traffic, while some related static/service domains remain reachable.

## Next Required Step

Run a controlled user trace with the phone connected to the V7 WireGuard profile, while the direct VLESS phone profile is disabled.

Expected test setup:

1. Phone VPN profile: V7 WireGuard only.
2. Direct VLESS phone profile: disabled.
3. Open or reload `www.gosuslugi.ru` during the trace window.

Only this proves the actual V7 user path.

## Decision

Do not enable more experimental routing automatically.

Keep:

- `TRUSTED_RU_SENSITIVE` route class.
- Sensitive RU direct exclusions.
- Xray lab binary for comparison testing only.

Do not:

- replace the active `sing-box` egress with Xray yet;
- add Xray to the active pool;
- route users through lab Xray automatically;
- rely on temporary VLESS as the final sensitive RU solution.

