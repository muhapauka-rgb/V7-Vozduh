# E25.13 Fresh Runtime Snapshot

## Host
hostname=v3119922.hosted-by-vdsina.ru
date_utc=2026-05-28T18:11:20Z
git_branch=unavailable
git_head=unavailable

## Registry Hashes
users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380

## Candidate
ip=10.7.0.11 current=1 table=1009 enabled=1
table_1009=default dev v7e356a192b79 scope link  
route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  

## Execution Target Metadata
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
target_users=0
iface=450: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000\    link/none 
awg_latest_handshakes=qYixieOopzFefThoPUnUNce9CG1YOCUuN2h8cDdbgWs= 1779991843
awg_transfer=qYixieOopzFefThoPUnUNce9CG1YOCUuN2h8cDdbgWs= 393869588 21047479

## Quality State
amneziawg-exec-20260528-10-8-1-14_avg_mbps=27.12
amneziawg-exec-20260528-10-8-1-14_min_mbps=10.67
amneziawg-exec-20260528-10-8-1-14_stability=1.000

## Load And Diagnose
amneziawg-exec-20260528-10-8-1-14_users=0
amneziawg-exec-20260528-10-8-1-14_soft_limit=1
amneziawg-exec-20260528-10-8-1-14_hard_limit=2
amneziawg-exec-20260528-10-8-1-14_load_status=OK
amneziawg-exec-20260528-10-8-1-14_diagnose_reason=OK
amneziawg-exec-20260528-10-8-1-14_diagnose_severity=OK
amneziawg-exec-20260528-10-8-1-14_diagnose_detail=handshake_age_seconds=16

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
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=40.381; min=15.305; stability=0.3659; reason=interface state unknown; load-state users=1; diagnose SUSPECT; stability below floor (0.3659); missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=34.596; min=12.177; stability=0.4348; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; stability below floor (0.4348); missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=47.968; min=18.724; stability=0.4178; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; stability below floor (0.4178); missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=66.89; min=59.724; stability=0.8895; reason=interface state unknown; diagnose SUSPECT
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=22.789; min=12.027; stability=0.5196; reason=ready
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
samples_span_seconds=47
apply_timer_intervals_covered=2.35
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
  - /tmp/e25_13_restore_settle_samples/sample-01.json
  - /tmp/e25_13_restore_settle_samples/sample-02.json
  - /tmp/e25_13_restore_settle_samples/sample-03.json

## Selected Moves And Hidden Movers
selected_moves_count=0
selected_moves_hash=NONE
hidden_movers_count=0

## Runtime Checkers
v7_reconcile_check=OK
v7_user_route_check=OK
v7_killswitch_check=OK
v7_provisioning_reconcile_check=OK

## Timer State
v7_users_autoswitch_timer=inactive
v7_users_autoswitch_service=inactive

## Audit Store Tail
/opt/v7/audit/audit.jsonl.2.gz
/opt/v7/audit/audit.jsonl.3.gz
/opt/v7/audit/audit.jsonl.1
/opt/v7/audit/operator-execution-audit.jsonl
/opt/v7/audit/audit.jsonl
