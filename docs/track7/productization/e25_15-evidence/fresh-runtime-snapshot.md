# E25.15 Fresh Runtime Snapshot

date_utc=2026-05-28T20:51:08Z
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
drift_row=ip=10.7.0.16 current=vless table=1014 enabled=1
table_1009=default dev v7e356a192b79 scope link  
route_get_10_7_0_11=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  
table_1014=default dev tun0 scope link  
route_get_10_7_0_16=8.8.8.8 from 10.7.0.16 dev tun0 table 1014      cache iif wg0  
target_row=id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
target_users=0
selected_moves_count=0
selected_moves_hash=NONE
hidden_movers_count=0
runtime_checkers_ok=true

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
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=43.269; min=24.798; stability=0.5392; reason=interface state unknown; occupied by registry users: 10.7.0.16; load-state users=2; diagnose SUSPECT; missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=43.759; min=16.687; stability=0.3863; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; stability below floor (0.3863); missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=57.285; min=36.568; stability=0.605; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=66.124; min=59.045; stability=0.8914; reason=interface state unknown; diagnose SUSPECT
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=21.74; min=16.587; stability=0.7292; reason=ready
  - amneziawg-exec-20260528-10-8-1-14: GO; zero_user=True; diagnose=OK; avg=27.12; min=10.67; stability=1.0; reason=ready
should_E9_3_execute_now=False
execution_allowed_now=False

## Restore Settle
V7 restore settle gate (read-only)
runtime_commands_executed=False
mode=pre-restore
gate_status=GO
sample_count=3
required_samples=3
samples_span_seconds=49
apply_timer_intervals_covered=2.45
required_apply_timer_intervals=2
selected_moves_by_sample=[0, 0, 0]
telegram_hard_blocked_by_sample=[False, False, False]
egress_1_eligible_by_sample=[True, True, True]
movement_count_by_sample=[0, 0, 0]
registry_stable=True
egress_registry_stable=True
checkers_ok=True
hidden_movers_observed=False
moved_users=[]
recommended_action=pre_restore_gate_clean_request_separate_apply_restore_approval
execution_allowed_now=False
sample_sources:
  - /tmp/e25_15_settle_samples/sample-01.json
  - /tmp/e25_15_settle_samples/sample-02.json
  - /tmp/e25_15_settle_samples/sample-03.json

## Timers
v7_users_autoswitch_timer=inactive
v7_users_autoswitch_service=inactive
