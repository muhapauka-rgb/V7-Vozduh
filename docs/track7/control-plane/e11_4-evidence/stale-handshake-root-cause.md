# E11.4 Stale Handshake Root Cause

## Finding

WireGuard remains strict `NO-GO` because persisted diagnose severity is:

```text
diagnose=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
```

Current target readiness confirms the target is otherwise attractive for a clean canary target:

```text
egress=wireguard-1779454504-c43409
zero_user=true
avg_mbps=51.648
min_mbps=48.01
stability=0.929562
reason=diagnose SUSPECT
```

## Exact Root Cause

The runtime diagnose script computes handshake age with `awg show "$iface"` for all interfaces. WireGuard requires `wg show "$iface"` for authoritative live handshake data.

When `awg show` does not produce a `latest handshake` line for the WireGuard interface, the script falls back to:

```text
handshake_age_seconds=999999
```

That stale fallback can persist as `curl_ok_but_handshake_stale` even when the interface is up, route evidence is sane, counters are moving, and prior live `wg show` evidence showed a fresh handshake.

## Classification

```text
wireguard_root_cause_classification=DIAGNOSE_REFRESH_BUG
secondary_classification=ZERO_USER_IDLE_SEMANTICS_WRONG
confidence=HIGH
```

This is not classified as `REAL_RUNTIME_FAILURE` because the blocking evidence is a persisted diagnose semantic/path issue, while E11.2/E11.3 runtime evidence showed:

```text
wireguard_zero_user=true
wireguard_quality_ok=true
wireguard_interface=UP,LOWER_UP
wireguard_route_get=OK
live_handshake_fresh=true
counters_growing=true
exclusions_present=TRUSTED_RU_SENSITIVE,DIRECT_RU
restore_governance_live_proven=true
```

## Why Strict Readiness Still Blocks

The strict target readiness checker is intentionally conservative. It has no live WireGuard override and therefore rejects persisted `SUSPECT`:

```text
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
wireguard_reason=diagnose SUSPECT
```

That strict behavior is correct for governance until either:

1. the diagnose semantics are fixed and deployed; or
2. a fresh explicit stale-handshake waiver approval accepts the mismatch for one bounded canary.

