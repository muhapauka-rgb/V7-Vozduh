# E10.5 WireGuard Stale-Handshake Analysis

Mode: read-only diagnostic only. No reservation, canary, route, registry, or systemd mutation was performed.

## Target

```text
egress_id=wireguard-1779454504-c43409
interface=v7e06a394c478
protocol=wireguard
zero_user=true
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

## Persisted Diagnose State

The persisted diagnose state marks the target as suspect:

```text
wireguard-1779454504-c43409_diagnose_reason=curl_ok_but_handshake_stale
wireguard-1779454504-c43409_diagnose_severity=SUSPECT
wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=999999
```

Planner and target-readiness logic therefore reject WireGuard with:

```text
blocked=["severity_SUSPECT"]
```

## Live Interface / Handshake Reality

The live read-only interface evidence contradicts the stale persisted handshake age:

```text
interface=v7e06a394c478 UP,LOWER_UP
latest_handshake=3 seconds ago
transfer_received=6.83 GiB
transfer_sent=276.24 MiB
route_get_oif_wireguard=8.8.8.8 dev v7e06a394c478 src 10.8.0.17
```

Route and nft evidence are present for the interface:

```text
connected_route=10.8.0.0/24 dev v7e06a394c478
nat_rule_present=true
mss_rule_present=true
allow_rule_present=true
```

No enabled user is assigned to WireGuard, so idle periods are expected and should not by themselves prove datapath failure.

## Classification

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
confidence=high
real_datapath_failure_detected=false
route_issue_detected=false
quality_degraded=false
```

Operational nuance:

```text
persisted_diagnose_state_false_positive=true
live_handshake_fresh=true
diagnose_semantics_too_conservative_for_zero_user_reserved_target=true
```

The blocker is not current WireGuard datapath failure. The blocker is that the target-readiness gate currently treats persisted `SUSPECT` as a hard clean-target rejection even when live WireGuard evidence shows a fresh handshake.

## Waiver Implication

Clean target readiness still cannot be declared while the default readiness checker sees `diagnose=SUSPECT`.

```text
waiver_required=true_until_diagnose_semantics_is_fixed_or_refreshed
waiver_status=waiver_conditional
```

Waiver can be considered only if the future live gate reconfirms:

```text
zero_user=true
interface=UP,LOWER_UP
live_handshake_fresh=true
route_get_sane=true
quality_ok=true
Direct_RU_exclusion_present=true
Trusted_RU_exclusion_present=true
restore_settle_gate_status=GO
runtime_checks_ok=true
```
