# E10.3 OpenVPN / WireGuard Suspect Review

Mode: read-only zero-user target review.

## OpenVPN

Egress:

```text
openvpn-1779388847-d2ad7c
interface=v7edb0c189291
zero_user=true
diagnose=SUSPECT
diagnose_detail=handshake_age_seconds=999999
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Target-readiness result:

```text
status=NO-GO
reason=diagnose SUSPECT; min_mbps below floor (8.83); stability below floor (0.1641)
```

Planner evidence also reports `severity_SUSPECT`. Although older E10.2.x analysis treated stale handshake as potentially idle-but-healthy, the current E10.3 target-readiness view adds quality-floor blockers. OpenVPN is not a good waiver target right now.

## WireGuard

Egress:

```text
wireguard-1779454504-c43409
interface=v7e06a394c478
zero_user=true
diagnose=SUSPECT
diagnose_detail=handshake_age_seconds=999999
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Target-readiness result:

```text
status=NO-GO
reason=diagnose SUSPECT
avg_mbps=46.7763
min_mbps=44.93
stability=0.960529
```

WireGuard has the best quality numbers among zero-user targets, but the `SUSPECT` diagnose state still blocks clean target approval. It is the least-bad conditional waiver candidate if an operator explicitly accepts a stale-handshake mechanics canary. It is not a clean GO target.

## Waiver Implication

```text
clean_zero_user_target_exists=false
openvpn_waiver_recommended=false
wireguard_waiver_possible=true
wireguard_waiver_acceptable_without_separate_packet=false
```

No waiver is approved by E10.3. A separate approval packet would be required before using WireGuard.

