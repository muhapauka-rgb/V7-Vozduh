# V7 Phase 56: User Flow Trace Diagnostic

Date: 2026-05-07

## Goal

Add a repeatable diagnostic for cases where the policy decision looks correct
but a real user-facing site or app still does not load.

This was added after confirming that Gosuslugi works through the user's direct
VLESS client, but not through V7 using the current `tun0 -> vless-out` path.

## Added

```text
hardening/v7-user-flow-trace
```

Usage:

```text
v7-user-flow-trace <user_ip> <domain> [duration_seconds]
```

The command records:

- DNS result through V7 DNS;
- service-aware policy decision;
- direct-routing decision;
- `ip route get` result per resolved IP;
- short tcpdump trace for the user and destination;
- observed path summary: `tun0`, `awg2`, `ens3`, `wg_only`, or `NO_TRAFFIC`;
- verdict summary.

Latest state is written to:

```text
/opt/v7/egress/state/user-flow-trace.state
```

Raw reports are stored under:

```text
/opt/v7/egress/state/flow-traces/
```

## Admin

The Sensitive RU Diagnostics panel now shows:

- last flow verdict;
- last observed path;
- last traced domain.

It also has a `Trace User Flow` action. This action is operator-level and is
blocked by Safe Mode.

## VPS Installation

Installed on the VPS:

```text
/usr/local/bin/v7-user-flow-trace
/usr/local/bin/v7-admin-api
```

Backup created before replacing the admin API:

```text
/usr/local/bin/v7-admin-api.backup.phase56.<timestamp>
```

## Validation

The script passed shell syntax check. The updated admin API passed Python AST
parse and was restarted.

Validation on VPS:

```text
v7-admin-api active
http://127.0.0.1:7080/login returns HTML
```

A short test trace without a simultaneous user reload produced:

```text
observed_path=NO_TRAFFIC
verdict=NO_TRAFFIC
```

The internal route check for `10.0.0.3 -> www.gosuslugi.ru` still showed:

```text
table 101 -> tun0
```

## Next

Run the trace while the user reloads Gosuslugi from the iPhone. This will
produce a durable admin-visible result instead of relying on manual tcpdump
output.

## Live Gosuslugi Trace Result

A live trace was run while the user kept Gosuslugi open through V7:

```text
user_ip=10.0.0.3
domain=www.gosuslugi.ru
observed_path=tun0
verdict=EGRESS_PATH_OPEN_BUT_APP_CLOSED_OR_NO_TLS_RESPONSE
reason=tcp_payload_seen_then_fin_or_rst
wg_in_packets=194
wg_out_packets=187
tun_out_packets=149
tun_in_packets=105
awg_out_packets=0
awg_in_packets=0
ens_out_packets=0
dns_packets=2
syn_packets=86
payload_packets=65
fin_rst_packets=99
```

Conclusion: the direct RU override is working and there is no `ens3` leak for
this flow. The failure is in the viability/behavior of the current
`wg0 -> tun0 -> sing-box vless-out -> Gosuslugi` path.
