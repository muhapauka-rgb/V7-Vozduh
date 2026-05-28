# E11.1 WireGuard Deep Diagnostic

Mode: read-only diagnostic. No interface restart, route mutation, registry mutation, reservation, canary, or systemd mutation was performed.

## Target

```text
egress_id=wireguard-1779454504-c43409
interface=v7e06a394c478
protocol=wireguard
role=GLOBAL_FAST
enabled=1
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

## Current Runtime Truth

Fresh snapshot: `2026-05-26T18:14:08Z`.

```text
wireguard_users_from_registry=0
wireguard_users_from_load_state=0
wireguard_load_status=OK
interface_state=UP,LOWER_UP
route_get_oif_wireguard=OK
nat_rule_present=true
mss_rule_present=true
allow_rule_present=true
selected_moves=0
candidate_moves_total=0
runtime_checks_ok=true
```

The persisted diagnose state still reports:

```text
diagnose_severity=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
diagnose_detail=handshake_age_seconds=999999
```

Live WireGuard state contradicts that persisted stale age:

```text
latest_handshake=57 seconds ago
transfer_received=6.85 GiB
transfer_sent=276.84 MiB
endpoint=89.191.226.228:51820
allowed_ips=0.0.0.0/0,::/0
```

## Quality / Planner Evidence

Latest planner evidence keeps WireGuard blocked only by `severity_SUSPECT`:

```text
wireguard_eligible=false
wireguard_blocked=["severity_SUSPECT"]
wireguard_avg_mbps=48.57 to 48.92
wireguard_min_mbps=45.35
wireguard_stability=0.927 to 0.934
wireguard_load_status=OK
wireguard_users=0
```

The quality floor is satisfied. There is no evidence of route failure, missing NAT/MSS coverage, missing interface, hidden user occupancy, or active planner pressure.

## Classification

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
confidence=high
real_failure=false
idle_but_healthy=true
quality_degraded=false
route_issue=false
unknown=false
```

Interpretation:

```text
persisted_diagnose_state_false_positive=true
live_handshake_fresh=true
diagnose_semantics_too_conservative_for_zero_user_reserved_targets=true
```

WireGuard appears operationally suitable as a target candidate, but it cannot be strict-clean while readiness gates treat any `SUSPECT` diagnose as hard NO-GO.
