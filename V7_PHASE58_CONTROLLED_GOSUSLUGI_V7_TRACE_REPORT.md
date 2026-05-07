# V7 Phase 58: Controlled Gosuslugi V7 User Trace

Date: 2026-05-07

## Goal

Run a controlled live trace while the phone uses the V7 WireGuard profile and reloads Gosuslugi during the trace window.

This was needed because previous traces either captured only background Apple traffic or no user traffic.

## Trace Command

```bash
/usr/local/bin/v7-user-flow-trace 10.0.0.3 www.gosuslugi.ru 90
```

## Policy Result

Domain:

- `www.gosuslugi.ru`

Resolved IPs:

- `109.207.1.118`
- `109.207.1.97`
- `109.207.8.118`
- `109.207.8.97`

Policy:

- route class: `TRUSTED_RU_SENSITIVE`
- mode: `egress`
- active egress: `vless`
- desired path: `vless`

Direct RU engine:

- direct set: yes
- direct exclude: yes
- decision: `VPN_PREFERRED_DIRECT_EXCLUDED`

This confirms that broad `.ru` direct routing is not capturing Gosuslugi.

## Route Result

For all resolved Gosuslugi IPs:

```text
route_without_mark=... from 10.0.0.3 dev tun0 table 101 cache iif wg0
```

Direct route with mark `0x77` exists, but the sensitive direct-exclude rule prevents Gosuslugi from using it.

## Packet Trace Summary

```text
observed_path=tun0
verdict=EGRESS_PATH_OPEN_BUT_APP_CLOSED_OR_NO_TLS_RESPONSE
reason=tcp_payload_seen_then_fin_or_rst
wg_in_packets=788
wg_out_packets=734
tun_out_packets=554
tun_in_packets=381
awg_out_packets=0
awg_in_packets=0
ens_out_packets=0
dns_packets=10
syn_packets=396
payload_packets=385
fin_rst_packets=285
```

## Interpretation

The trace proves:

1. The phone was using V7.
2. V7 did not leak Gosuslugi traffic directly through `ens3`.
3. Gosuslugi traffic went through the intended `vless`/`tun0` path.
4. TCP connection establishment succeeded.
5. The phone sent TLS ClientHello payloads.
6. The remote side acknowledged the payloads.
7. A normal TLS response was not observed.
8. The connection was eventually closed with FIN/RST behavior.

This means the current failure is not caused by:

- missing DNS resolution;
- wrong `.ru` direct classification;
- wrong per-user route table;
- direct leak through the VPS public interface;
- V7 sending sensitive traffic to `awg2`.

The failure is now isolated to the selected sensitive RU egress path behavior after TCP setup and TLS ClientHello.

## Current Server Health After Trace

```text
sing-box: active
vless external IP: 77.110.103.131
awg2 external IP: 94.241.139.241
V7_RESULT=OK
```

## Next Engineering Direction

Do not keep changing policy routing. The policy layer is now behaving correctly.

Next diagnostics should focus on why the working phone-direct VLESS path differs from the V7-mediated VLESS path:

- exact iPhone VLESS app/core behavior;
- DNS behavior in the direct VLESS app;
- whether the direct VLESS app bypasses RU sensitive domains despite showing the VLESS external IP on generic IP checks;
- whether the app uses a different transport/core option than the exported profile;
- whether sensitive RU should be treated as a separate adapter/route class with its own tested egress implementation.

