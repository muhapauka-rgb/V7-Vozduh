# V7 Phase 55: Gosuslugi Live User-Flow Trace

Date: 2026-05-07

## Context

The user reported that Gosuslugi still hangs while loading through V7 after
`TRUSTED_RU_SENSITIVE` domains were added to the direct-exclude list.

The goal of this trace was to verify the real path taken by iPhone traffic
before making any further routing changes.

## Findings

Active user:

```text
10.0.0.3
latest handshake: active
```

Current routing:

```text
10.0.0.3 -> table 101 -> tun0 -> vless
```

Direct policy state for core Gosuslugi domains:

```text
gosuslugi.ru       direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
www.gosuslugi.ru   direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
esia.gosuslugi.ru  direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
lk.gosuslugi.ru    direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
gu-st.ru           direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
```

Yandex remained direct:

```text
yandex.ru direct_exclude=no decision=DIRECT_READY
```

## nftables Verification

The live nftables rule correctly avoids marking excluded destinations for
direct routing:

```text
ip saddr 10.0.0.0/24 ip daddr @v7_direct_dst ip daddr != @v7_direct_exclude_dst meta mark set 0x77
```

The leak guard also only allows direct `ens3` traffic when the destination is in
the direct set and not in the exclude set.

## Live tcpdump Result

During a real iPhone attempt to open Gosuslugi:

```text
wg0 In:  10.0.0.3 -> 109.207.x.x:443
tun0 Out: 172.19.0.1 -> 109.207.x.x:443
tun0 In:  109.207.x.x:443 -> 172.19.0.1
wg0 Out: 109.207.x.x:443 -> 10.0.0.3
```

This proves the traffic was not going directly through `ens3`; it was routed
through `tun0` and sing-box `vless-out`.

The TCP connection was established and the iPhone sent TLS ClientHello packets.
The remote side acknowledged the data, but normal TLS response/application data
did not arrive before the client closed/retried the connections.

## DNS Trace

The iPhone queried V7 DNS:

```text
HTTPS? www.gosuslugi.ru
A?     www.gosuslugi.ru
```

Resolved A records:

```text
109.207.1.118
109.207.8.97
109.207.8.118
109.207.1.97
```

No additional hidden Gosuslugi domains were observed during this short trace.

## Egress Tests

Server-side tests to `https://www.gosuslugi.ru/` timed out through:

```text
direct ens3
awg2
socks 127.0.0.1:1080 -> vless
tun0 -> vless
```

TLS variants also timed out through the current VLESS SOCKS path:

```text
default
http1.1
tls1.2
tls1.3
browser user-agent
```

A temporary isolated sing-box test with `flow=xtls-rprx-vision` on
`127.0.0.1:1081` was performed without touching the production sing-box
service. It broke even `ifconfig.me`, so it was not applied.

## Conclusion

The `.ru direct` mistake has been fixed. Gosuslugi traffic is now taking the
intended sensitive/VLESS path.

The current failure is no longer a broad-direct routing issue. It is a path
viability issue for Gosuslugi over the available egresses from this VPS:

```text
DIRECT_RU via ens3       -> timeout
TRUSTED_RU via vless     -> timeout / no useful TLS response
TRUSTED_RU via awg2      -> timeout
```

If Gosuslugi works on a phone connected directly to a VLESS app, that direct
phone profile may not be identical to the V7 sing-box profile or may have its
own split-routing behavior. This must be verified before relying on that
channel as the trusted route.

## Next Safe Steps

1. Add a persistent `v7-user-flow-trace` diagnostic command so this exact
   analysis can be repeated from the admin panel.
2. Add explicit `TRUSTED_RU_SENSITIVE` state fields:
   `real_user_path`, `last_trace_result`, `safe_path`, `requires_action`.
3. Build an isolated `TRUSTED_RU_TLS` experiment for direct VPS behavior using
   browser-like TLS tools, without touching active users.
4. Verify whether the user's direct phone VLESS profile is full-tunnel or
   silently split-routes Russian sensitive domains outside VLESS.
