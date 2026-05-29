# E30 Ten User Discovery

candidate_count=4
rollback_target=1
requirement=candidate_count>=10
ten_user_discovery_status=NO-GO
eligible_rollback_users:
- ip=10.7.0.11 current=1 table=1009 enabled=1
- ip=10.7.0.12 current=1 table=1010 enabled=1
- ip=10.7.0.14 current=1 table=1012 enabled=1
- ip=10.7.0.15 current=1 table=1013 enabled=1

all_enabled_known_table_users:
- ip=10.0.0.2 current=awg3 table=100 enabled=1
- ip=10.0.0.3 current=awg3 table=101 enabled=1
- ip=10.0.0.6 current=awg3 table=104 enabled=1
- ip=10.7.0.3 current=awg3 table=1001 enabled=1
- ip=10.7.0.2 current=awg3 table=1000 enabled=1
- ip=10.7.0.4 current=awg3 table=1002 enabled=1
- ip=10.7.0.5 current=awg3 table=1003 enabled=1
- ip=10.7.0.6 current=awg3 table=1004 enabled=1
- ip=10.7.0.8 current=awg3 table=1006 enabled=1
- ip=10.7.0.9 current=awg0 table=1007 enabled=1
- ip=10.7.0.10 current=awg0 table=1008 enabled=1
- ip=10.7.0.11 current=1 table=1009 enabled=1
- ip=10.7.0.12 current=1 table=1010 enabled=1
- ip=10.7.0.13 current=awg0 table=1011 enabled=1
- ip=10.7.0.14 current=1 table=1012 enabled=1
- ip=10.7.0.15 current=1 table=1013 enabled=1
- ip=10.7.0.16 current=vless table=1014 enabled=1

blocker=INSUFFICIENT_ROLLBACK_TARGET_1_CANDIDATES
reason=Only users already on rollback target 1 qualify for this preparation scope; changing other users' current egress would be user movement/routing mutation and is forbidden in E30.
