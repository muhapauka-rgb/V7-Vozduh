# E30.1 Normalization Plan

normalization_needed=true
normalization_user_count=6
normalization_plan_safe=true
rollback_target=1
rollback_target_row=id=1 protocol=amneziawg type=interface interface=v7e356a192b79 test=interface enabled=1 config=/etc/amnezia/amneziawg/v7e356a192b79.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
rollback_target_probe_summary={   "aggregate_avg_mbps": 319.624,   "aggregate_min_mbps": 306.711,   "aggregate_rounds_mbps": [     336.0,     306.711,     316.162   ],   "all_rc_ok": true,   "iface": "v7e356a192b79",   "no_aggregate_round_below_10": true,   "probe_count": 30,   "probe_streams_per_round": 10,   "rollback_target_capacity_probe_safe": true,   "round_count": 3 } 

selected_normalization_users:
- ip=10.7.0.2 current_before=awg3 table=1000 command=v7-user-switch 10.7.0.2 1 rollback_if_failed=v7-user-switch 10.7.0.2 awg3
- ip=10.7.0.3 current_before=awg3 table=1001 command=v7-user-switch 10.7.0.3 1 rollback_if_failed=v7-user-switch 10.7.0.3 awg3
- ip=10.7.0.4 current_before=awg3 table=1002 command=v7-user-switch 10.7.0.4 1 rollback_if_failed=v7-user-switch 10.7.0.4 awg3
- ip=10.7.0.5 current_before=awg3 table=1003 command=v7-user-switch 10.7.0.5 1 rollback_if_failed=v7-user-switch 10.7.0.5 awg3
- ip=10.7.0.6 current_before=awg3 table=1004 command=v7-user-switch 10.7.0.6 1 rollback_if_failed=v7-user-switch 10.7.0.6 awg3
- ip=10.7.0.8 current_before=awg3 table=1006 command=v7-user-switch 10.7.0.8 1 rollback_if_failed=v7-user-switch 10.7.0.8 awg3

exact_commands:
- v7-user-switch 10.7.0.2 1
- v7-user-switch 10.7.0.3 1
- v7-user-switch 10.7.0.4 1
- v7-user-switch 10.7.0.5 1
- v7-user-switch 10.7.0.6 1
- v7-user-switch 10.7.0.8 1

audit_evidence_plan=record stdout/stderr/exit codes, registry diff, route table diff, post-normalization verification, restore-settle, audit hash
