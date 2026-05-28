# Block E11.1 WireGuard Clean Target Diagnostic And Reservation Feasibility Report

Mode: large read-only governance + diagnostic milestone.

## Executive Verdict

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
wireguard_reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness_after_reservation=CONDITIONAL_OR_GO_IF_DIAGNOSE_SEMANTICS_FIXED
dedicated_test_egress_needed=false_for_next_packet
best_strategy=WIREGUARD_RESERVE_THEN_DIAGNOSE_FIX_OR_STALE_HANDSHAKE_WAIVER
recommended_next_block=E11.2_WIREGUARD_RESERVATION_AND_DIAGNOSE_SEMANTICS_APPROVAL_PACKET
execution_allowed_now=false
```

WireGuard is the best current target path. It is not yet strict-clean because `diagnose=SUSPECT` remains a hard readiness blocker, but the live evidence points to stale diagnose semantics rather than real datapath failure.

## Current Governance Snapshot

Fresh runtime snapshot: `2026-05-26T18:14:08Z`.

```text
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
hidden_user_switch=false
hidden_routing_sync=false
selected_moves=0
candidate_moves_total=0
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Current users:

```text
target_1_users=10.0.0.2,10.0.0.3,10.0.0.6
vless_users=13 enabled users
wireguard_users=0
```

## WireGuard Diagnostic

```text
target=wireguard-1779454504-c43409
interface=v7e06a394c478
users=0
load_status=OK
diagnose=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
diagnose_detail=handshake_age_seconds=999999
live_latest_handshake=57 seconds ago
route_get=OK
avg_mbps=48.57 to 48.92
min_mbps=45.35
stability=0.927 to 0.934
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Classification:

```text
REAL_FAILURE=false
IDLE_BUT_HEALTHY=true
STALE_HANDSHAKE_ONLY=true
QUALITY_DEGRADED=false
ROUTE_ISSUE=false
UNKNOWN=false
confidence=high
```

## Reservation Feasibility

```text
wireguard_reservation_feasible=true
reservation_requires_mutation=true
mutation_scope=/opt/v7/egress/state/egress.registry wireguard metadata only
policy_apply_required=false
runtime_route_mutation_required=false
Direct_RU_risk=LOW_EXISTING_EXCLUSION
Trusted_RU_risk=LOW_EXISTING_EXCLUSION
kill_switch_risk=LOW_RECHECK_REQUIRED
```

Reservation preview only:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

No reservation was applied.

## Waiver And Readiness

```text
waiver_required=true
waiver_status=waiver_conditional
```

If reservation is applied while diagnose remains `SUSPECT`, expected readiness is:

```text
expected_second_canary_readiness_after_reservation=CONDITIONAL
```

If diagnose semantics are fixed/refreshed so live fresh handshake clears the stale persisted state:

```text
expected_second_canary_readiness_after_reservation=GO
```

## Dedicated Test Egress Decision

```text
dedicated_test_egress_needed=false_for_next_packet
dedicated_test_egress_recommended=true_for_long_term
```

WireGuard is enough for the next approval packet. A dedicated test egress remains the better durable architecture, but it is not required before the next governance block.

## Final Strategy Decision

Chosen path:

```text
A=proceed_with_WireGuard_reservation_approval_packet
plus=diagnose_semantics_fix_or_explicit_stale_handshake_waiver
```

Do not proceed directly to canary. The next block should be approval-only or bounded metadata/tooling design for WireGuard reservation and diagnose semantics.

## Final Answers

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
wireguard_reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness_after_reservation=CONDITIONAL_OR_GO_IF_DIAGNOSE_SEMANTICS_FIXED
dedicated_test_egress_needed=false_for_next_packet
best_strategy=WIREGUARD_RESERVE_THEN_DIAGNOSE_FIX_OR_STALE_HANDSHAKE_WAIVER
recommended_next_block=E11.2_WIREGUARD_RESERVATION_AND_DIAGNOSE_SEMANTICS_APPROVAL_PACKET
execution_allowed_now=false
```

## Mutation Statement

```text
Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
