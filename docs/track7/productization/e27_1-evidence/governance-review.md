# E27.1 Governance Review

date_utc=2026-05-28T22:15:01Z
## Target Row
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=2 hard_limit=2 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU

## Candidate Rows
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1

## Registry Hashes
f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042  /opt/v7/egress/state/users.registry
13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed  /opt/v7/egress/state/egress.registry

## Target Users
0

## Selected Moves
selected_moves_dir_absent
selected_moves_count=0

## Hidden Movers

## Runtime Checkers
### v7-reconcile-check
OK
### v7-user-route-check
OK
### v7-killswitch-check
OK
### v7-provisioning-reconcile-check
OK

## Readiness
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
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=55.102; min=49.454; stability=0.8879; reason=interface state unknown; occupied by registry users: 10.7.0.16; load-state users=2; diagnose SUSPECT; missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=62.967; min=45.508; stability=0.7; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=75.943; min=60.401; stability=0.787; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=6.425; min=3.415; stability=0.4747; reason=interface state unknown; diagnose SUSPECT; avg_mbps below floor (6.425); min_mbps below floor (3.415)
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=51.612; min=44.067; stability=0.8079; reason=ready
  - amneziawg-exec-20260528-10-8-1-14: GO; zero_user=True; diagnose=OK; avg=27.12; min=10.67; stability=1.0; reason=ready
should_E9_3_execute_now=False
execution_allowed_now=False
