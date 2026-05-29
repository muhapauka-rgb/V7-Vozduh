# E25.14 Execution-Time Recheck

hostname=v3119922.hosted-by-vdsina.ru
date_utc=2026-05-28T20:35:59Z

## Packet
packet_id=packet-6cda2c9e4c42133eedfebd5b
approval_id=approval-4602f4946f57be3bf9212b03
operation_id=e25-13-first-movement-20260528T181306Z
approval_expires_at=2026-05-28T22:13:06Z
packet_non_expired=true
packet_hash_expected=b5b9484ff1ccd1f78b3eded361dce38348327518f36c657c2ea3087a2dc2b939
packet_hash_actual=b5b9484ff1ccd1f78b3eded361dce38348327518f36c657c2ea3087a2dc2b939
packet_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
packet_egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
packet_selected_moves_hash=NONE

## Runtime
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
table_1009=default dev v7e356a192b79 scope link  
route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  
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
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=46.166; min=36.578; stability=0.7658; reason=interface state unknown; occupied by registry users: 10.7.0.16; load-state users=2; diagnose SUSPECT; missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=41.789; min=16.456; stability=0.3998; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; stability below floor (0.3998); missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=48.919; min=23.919; stability=0.4696; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=67.508; min=57.067; stability=0.8403; reason=interface state unknown; diagnose SUSPECT
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=19.503; min=12.205; stability=0.5927; reason=ready
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
samples_span_seconds=48
apply_timer_intervals_covered=2.4
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
  - /tmp/e25_14_recheck_settle_samples/sample-01.json
  - /tmp/e25_14_recheck_settle_samples/sample-02.json
  - /tmp/e25_14_recheck_settle_samples/sample-03.json

## Authorization
execution_authorized=false
authorization_reasons=users_registry_hash_mismatch
execution_allowed_now=false_until_command_boundary

## Audit Tail
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_expired_packet","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.269826+00:00","errors":["approval_expired"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_expired_packet","previous_record_hash":"cc62d11f72ddeb7f8efe4c94d7e014d51bb912dd3a6a2744dc15b2e1536ebaf0","record_hash":"0e184967fbd7a57237c1f2e2f936f9227d8a60b817eabeb62dae45bf3563d1c1","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_stale_generation","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.270674+00:00","errors":["generation_id_missing"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_stale_generation","previous_record_hash":"0e184967fbd7a57237c1f2e2f936f9227d8a60b817eabeb62dae45bf3563d1c1","record_hash":"71c1bb3e3b3b5b4ab926a9b3ebc5229b16e864d15b2290649fae32ef652d6121","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_stale_selected_move_hash","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.271510+00:00","errors":["selected_move_hash_invalid_for_zero_budget"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_stale_selected_move_hash","previous_record_hash":"71c1bb3e3b3b5b4ab926a9b3ebc5229b16e864d15b2290649fae32ef652d6121","record_hash":"27a79b6e2f5cf1ae7f2b7d417196f33d0c3b08cb9dcfaebbb9141c125191fb9b","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_modified_runtime_action","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.273320+00:00","errors":["runtime_action_not_allowed"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_modified_runtime_action","previous_record_hash":"27a79b6e2f5cf1ae7f2b7d417196f33d0c3b08cb9dcfaebbb9141c125191fb9b","record_hash":"ec705cff96b92eeb86e8b2366c6a4298a3e475e052d1424277f3648d5f64a068","record_type":"denial_record","routing_mutation":false,"runtime_action":"MOVE_USER","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_modified_blast_radius","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.274267+00:00","errors":["allowed_targets_not_empty"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_modified_blast_radius","previous_record_hash":"ec705cff96b92eeb86e8b2366c6a4298a3e475e052d1424277f3648d5f64a068","record_hash":"9ad6456a3e2123f08a9f60b3f6da72c0fdc3db091fa0a252e4a5f68e2d7f5b7e","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_unauthorized_movement_budget","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.274954+00:00","errors":["selected_move_budget_not_zero"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_unauthorized_movement_budget","previous_record_hash":"9ad6456a3e2123f08a9f60b3f6da72c0fdc3db091fa0a252e4a5f68e2d7f5b7e","record_hash":"4f1009cb771ab3205b9bceabb561b2e417bbda49f4cd929467a7519ba18eb497","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_attempt_user_movement","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.279031+00:00","errors":["allowed_users_not_empty","user_movement_not_forbidden"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_attempt_user_movement","previous_record_hash":"4f1009cb771ab3205b9bceabb561b2e417bbda49f4cd929467a7519ba18eb497","record_hash":"f778d2fa60b5d9ef1269f1a26a9bad46f89582b99a9d4a744423d716040a1edd","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
{"approval_id":"appr_e23_zero_move_governance_state_20260528T080017Z_attempt_routing_mutation","autoswitch_apply":false,"canary":false,"checks":{},"created_at":"2026-05-28T08:03:59.280006+00:00","errors":["routing_mutation_not_forbidden"],"kill_switch_mutation":false,"operation_id":"E23_FIRST_REAL_ZERO_MOVE_RUNTIME_ACTION","packet_id":"pkt_e23_zero_move_governance_state_20260528T080017Z_attempt_routing_mutation","previous_record_hash":"f778d2fa60b5d9ef1269f1a26a9bad46f89582b99a9d4a744423d716040a1edd","record_hash":"4e6297be2ff4d9acfe83f5dab77e8ffb421ee64640a5fd687b986c42ff924789","record_type":"denial_record","routing_mutation":false,"runtime_action":"ZERO_MOVE_GOVERNANCE_STATE_TRANSITION","runtime_action_performed":false,"runtime_action_record_hash":"","runtime_mutation":false,"runtime_mutation_scope":"none","schema_version":"e23.operator-execution-audit-record.v1","selected_first_action":"ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK","user_movement":false,"verdict":"DENY_PACKET_INVALID"}
