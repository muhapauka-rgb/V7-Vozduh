# E27.1 Capacity Requalification

date_utc=2026-05-28T21:40:02Z
target=amneziawg-exec-20260528-10-8-1-14
backup=/opt/v7/egress/state/e27_1-backups/egress.registry.20260528T214002Z

## Before
43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380  /opt/v7/egress/state/egress.registry
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU

## After
13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed  /opt/v7/egress/state/egress.registry
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=2 hard_limit=2 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU

## Diff
--- /opt/v7/egress/state/e27_1-backups/egress.registry.20260528T214002Z	2026-05-28 17:49:51.587091699 +0300
+++ /opt/v7/egress/state/egress.registry	2026-05-29 00:40:02.276800239 +0300
@@ -4,4 +4,4 @@
 id=1 protocol=amneziawg type=interface interface=v7e356a192b79 test=interface enabled=1 config=/etc/amnezia/amneziawg/v7e356a192b79.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
 id=openvpn-1779388847-d2ad7c protocol=openvpn type=interface interface=v7edb0c189291 test=interface enabled=1 config=/etc/v7/egress-openvpn/v7edb0c189291.ovpn role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
 id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance
-id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
+id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=2 hard_limit=2 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU

## Validation
v7-reconcile-check=0
v7-user-route-check=0
v7-killswitch-check=0
v7-provisioning-reconcile-check=0
v7-second-canary-target-readiness=0

### Readiness
V7 second canary target readiness (read-only)
runtime_commands_executed=False
candidate_user=10.7.0.11
candidate_still_valid=True
current_egress=1
execution_only_mode=True
execution_target_id=amneziawg-exec-20260528-10-8-1-14
selected_target=amneziawg-exec-20260528-10-8-1-14
approval_status=GO
second_canary_readiness=GO
target_1_current_user=['10.7.0.11', '10.7.0.12', '10.7.0.14', '10.7.0.15']
zero_user_targets=openvpn-1779388847-d2ad7c,wireguard-1779454504-c43409,amneziawg-exec-20260528-10-8-1-14
target_candidates:
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=50.286; min=40.502; stability=0.7857; reason=interface state unknown; occupied by registry users: 10.7.0.16; load-state users=2; diagnose SUSPECT; missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=53.258; min=23.3; stability=0.4217; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; stability below floor (0.4217); missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=70.173; min=52.255; stability=0.7212; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=15.664; min=8.933; stability=0.4204; reason=interface state unknown; diagnose SUSPECT; min_mbps below floor (8.933); stability below floor (0.4204)
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=32.615; min=22.349; stability=0.6183; reason=ready
  - amneziawg-exec-20260528-10-8-1-14: GO; zero_user=True; diagnose=OK; avg=27.12; min=10.67; stability=1.0; reason=ready
should_E9_3_execute_now=False
execution_allowed_now=False

## Verdict
capacity_requalification_attempted=true
capacity_requalification_successful=true
runtime_mutation_scope=target metadata soft_limit/hard_limit only
user_movement_performed=false
routing_mutation_for_users=false
