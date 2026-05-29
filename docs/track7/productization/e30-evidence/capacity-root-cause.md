# E30 Capacity Root Cause

target_name=amneziawg-exec-20260528-10-8-1-14
target_row=id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=4 hard_limit=4 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
soft_limit=4
hard_limit=4
previous_certified_scale=4
capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_10_USER_VALIDATION
reason=E28.1 proved 2->4 was metadata-only after four-stream validation; no evidence yet proves 4->10 is physical, but 10-user candidate discovery is blocked before safe requalification.
