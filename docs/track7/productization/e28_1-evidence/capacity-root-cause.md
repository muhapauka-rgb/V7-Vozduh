# E28.1 Capacity Root Cause

date_utc=2026-05-29T06:39:06Z
target=amneziawg-exec-20260528-10-8-1-14
target_row=id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=2 hard_limit=2 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
soft_limit=2
hard_limit=2
target_users=0
readiness_status=GO
avg_mbps=27.12
min_mbps=10.67
stability=1.0
selected_moves_count=0
hidden_movers_present=false
runtime_checkers_ok=true

## Previous Capacity Decisions
E27.1 classified 1->2 as GOVERNANCE_LIMIT_ONLY_WITH_METADATA_DRIFT after target-local validation and long-window validation.
E28 found 4 clean rollback candidates but blocked on hard_limit=2.

capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_4_USER_VALIDATION
