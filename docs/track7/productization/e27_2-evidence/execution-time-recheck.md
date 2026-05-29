# E27.2 Execution-Time Recheck

date_utc=2026-05-28T22:30:47Z
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
egress_registry_hash=13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed
candidate_user_A_row=ip=10.7.0.11 current=1 table=1009 enabled=1
candidate_user_B_row=ip=10.7.0.12 current=1 table=1010 enabled=1
route_table_1009=default dev v7e356a192b79 scope link ;
route_table_1010=default dev v7e356a192b79 scope link ;
route_get_A=1.1.1.1 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif lo ;
route_get_B=1.1.1.1 from 10.7.0.12 dev v7e356a192b79 table 1010 ;    cache iif lo ;
target_row=id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=2 hard_limit=2 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
target_users=0
soft_limit=2
hard_limit=2
readiness_status=GO
restore_settle_gate_status=GO
selected_moves_count=0
selected_moves_hash=NONE
hidden_movers_present=false
runtime_checkers_ok=true
execution_recheck_passed=true
