# Block E11.2 WireGuard Reservation And Stale-Handshake Semantics Approval Packet

Mode: bounded governance + approval packet. No live mutation was performed.

## Executive Verdict

```text
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
secondary_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness=CONDITIONAL_AFTER_RESERVATION_WITH_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
best_strategy=WIREGUARD_RESERVATION_THEN_DIAGNOSE_SEMANTICS_FIX_PREFERRED
recommended_next_block=E11.3_BOUNDED_WIREGUARD_RESERVATION_METADATA_MUTATION
execution_allowed_now=false
```

WireGuard is approved for a separate bounded reservation mutation packet, not
for immediate canary execution. The stale-handshake issue is classified as a
diagnose persistence/semantics blocker: strict tooling still sees
`diagnose=SUSPECT`, while live WireGuard evidence shows a fresh handshake and
working route.

## Current WireGuard Truth

Fresh runtime snapshot: `2026-05-26T18:33:21Z`.

```text
target=wireguard-1779454504-c43409
interface=v7e06a394c478
enabled=1
role=GLOBAL_FAST
manual_only=0
reserve_only=0
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
load_users=0
registry_users=0
load_status=OK
diagnose_severity=SUSPECT
diagnose_reason=curl_ok_but_handshake_stale
diagnose_detail=handshake_age_seconds=999999
interface_state=UP,LOWER_UP
live_latest_handshake=1 minute, 47 seconds ago
transfer=6.87 GiB received, 277.58 MiB sent
route_get=8.8.8.8 dev v7e06a394c478 src 10.8.0.17
selected_moves=[]
apply_result.applied=false
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Stale-Handshake Semantics

```text
REAL_FAILURE=false
STALE_HANDSHAKE_ONLY=true
IDLE_BUT_HEALTHY=true
ROUTE_ISSUE=false
DIAGNOSE_SEMANTICS_TOO_STRICT=true
UNKNOWN=false
confidence=high
```

The persisted diagnose state is stale relative to live `wg show`. This should
remain a strict clean-readiness blocker until either:

1. Diagnose semantics are fixed/refreshed to account for live WireGuard
   handshake evidence; or
2. A bounded stale-handshake waiver is explicitly accepted for one canary
   window.

## Reservation Approval Preview

Proposed metadata only:

```text
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Scope:

```text
affected_file=/opt/v7/egress/state/egress.registry
affected_row=wireguard-1779454504-c43409 only
policy_apply_required=false
routing_mutation_required=false
users_registry_mutation_required=false
kill_switch_recheck_required=true
```

Reservation approval:

```text
reservation_approval_status=GO_FOR_SEPARATE_BOUNDED_METADATA_MUTATION_PACKET
```

No reservation was applied in E11.2.

## Waiver Decision

```text
waiver_required=true
waiver_status=waiver_conditional
waiver_name=wireguard_stale_handshake_reserved_target
waiver_scope=one_user_second_canary_only
waiver_duration=single bounded canary window only
waiver_blast_radius=one_user
```

The waiver is acceptable only if all future execution gates remain OK:
restore-settle GO, runtime checkers OK, WireGuard interface UP/LOWER_UP, route
evidence OK, zero users, no hidden movers, and rollback certainty.

## Second Canary Simulation

After reservation:

```text
expected_selected_target=wireguard-1779454504-c43409
expected_second_canary_readiness=CONDITIONAL
```

After reservation plus diagnose semantics fix:

```text
expected_second_canary_readiness=GO
```

Fresh candidate selection is still required. Old E9/E10 candidates are stale.

## Final Approval Decision

Chosen path:

```text
A=ready_for_bounded_reservation_mutation_packet
preferred_followup=diagnose_semantics_fix_before_direct_canary
fallback=explicit_stale_handshake_waiver_in_fresh_second_canary_packet
```

Do not proceed directly to canary. Do not mutate reservation in this block.

## Final Answers

```text
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
wireguard_quality_ok=true
wireguard_zero_user=true
reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness=CONDITIONAL_AFTER_RESERVATION_WITH_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
best_strategy=WIREGUARD_RESERVATION_THEN_DIAGNOSE_SEMANTICS_FIX_PREFERRED
recommended_next_block=E11.3_BOUNDED_WIREGUARD_RESERVATION_METADATA_MUTATION
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
