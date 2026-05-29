# E25.15 Registry Drift Classification

date_utc=2026-05-28T20:46:14Z
old_packet_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
current_users_registry_hash=
current_egress_registry_hash=

## Current users.registry
ip=10.0.0.2 current=awg3 table=100 enabled=1
ip=10.0.0.3 current=awg3 table=101 enabled=1
ip=10.0.0.6 current=awg3 table=104 enabled=1
ip=10.7.0.3 current=awg3 table=1001 enabled=1
ip=10.7.0.2 current=awg3 table=1000 enabled=1
ip=10.7.0.4 current=awg3 table=1002 enabled=1
ip=10.7.0.5 current=awg3 table=1003 enabled=1
ip=10.7.0.6 current=awg3 table=1004 enabled=1
ip=10.7.0.7 current=vless table=1005 enabled=0
ip=10.7.0.8 current=awg3 table=1006 enabled=1
ip=10.7.0.9 current=awg0 table=1007 enabled=1
ip=10.7.0.10 current=awg0 table=1008 enabled=1
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1
ip=10.7.0.13 current=awg0 table=1011 enabled=1
ip=10.7.0.14 current=1 table=1012 enabled=1
ip=10.7.0.15 current=1 table=1013 enabled=1
ip=10.7.0.16 current=vless table=1014 enabled=1

## Candidate
ip=10.7.0.11 current=1 table=1009 enabled=1
table_1009=default dev v7e356a192b79 scope link  
route_get_10_7_0_11=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  

## Drift Row
ip=10.7.0.16 current=vless table=1014 enabled=1
table_1014=default dev tun0 scope link  
route_get_10_7_0_16=8.8.8.8 from 10.7.0.16 dev tun0 table 1014      cache iif wg0  

## Target Capacity
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
target_users=0

## Selected Moves
selected_moves_count=0
selected_moves_hash=NONE

## Hidden Movers
hidden_movers_absent=true

## Runtime Checkers
v7_reconcile_check=OK
v7_user_route_check=OK
v7_killswitch_check=OK
v7_provisioning_reconcile_check=OK

## Switch History Tail
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1008", "to": "awg0", "ts": "2026-05-27T08:54:20.527515+00:00", "user_ip": "10.7.0.10"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "100", "to": "awg3", "ts": "2026-05-27T09:03:30.062250+00:00", "user_ip": "10.0.0.2"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "101", "to": "awg3", "ts": "2026-05-27T09:03:31.534467+00:00", "user_ip": "10.0.0.3"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "104", "to": "awg3", "ts": "2026-05-27T09:03:33.382412+00:00", "user_ip": "10.0.0.6"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1000", "to": "1", "ts": "2026-05-27T09:09:26.094179+00:00", "user_ip": "10.7.0.2"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1007", "to": "1", "ts": "2026-05-27T09:09:28.835227+00:00", "user_ip": "10.7.0.9"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1008", "to": "1", "ts": "2026-05-27T09:09:31.271443+00:00", "user_ip": "10.7.0.10"}
{"from": "awg3", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "100", "to": "1", "ts": "2026-05-27T09:27:18.937847+00:00", "user_ip": "10.0.0.2"}
{"from": "awg3", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "101", "to": "1", "ts": "2026-05-27T09:27:20.218937+00:00", "user_ip": "10.0.0.3"}
{"from": "awg3", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "104", "to": "1", "ts": "2026-05-27T09:27:21.541243+00:00", "user_ip": "10.0.0.6"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1003", "to": "awg3", "ts": "2026-05-27T09:36:24.888113+00:00", "user_ip": "10.7.0.5"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1001", "to": "awg0", "ts": "2026-05-27T09:36:26.219488+00:00", "user_ip": "10.7.0.3"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1000", "to": "awg3", "ts": "2026-05-27T09:36:27.727330+00:00", "user_ip": "10.7.0.2"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "100", "to": "awg0", "ts": "2026-05-27T09:43:05.117384+00:00", "user_ip": "10.0.0.2"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "101", "to": "awg0", "ts": "2026-05-27T09:43:07.281806+00:00", "user_ip": "10.0.0.3"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "104", "to": "awg0", "ts": "2026-05-27T09:43:09.514453+00:00", "user_ip": "10.0.0.6"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "100", "to": "awg3", "ts": "2026-05-27T10:04:31.680104+00:00", "user_ip": "10.0.0.2"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "101", "to": "awg3", "ts": "2026-05-27T10:04:33.220298+00:00", "user_ip": "10.0.0.3"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "104", "to": "awg3", "ts": "2026-05-27T10:04:34.635019+00:00", "user_ip": "10.0.0.6"}
{"from": "awg0", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1001", "to": "awg3", "ts": "2026-05-27T10:04:54.476357+00:00", "user_ip": "10.7.0.3"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1002", "to": "awg3", "ts": "2026-05-27T10:05:35.238691+00:00", "user_ip": "10.7.0.4"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1004", "to": "awg3", "ts": "2026-05-27T10:05:37.396195+00:00", "user_ip": "10.7.0.6"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1006", "to": "awg3", "ts": "2026-05-27T10:05:39.600244+00:00", "user_ip": "10.7.0.8"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "manual", "table": "1009", "to": "wireguard-1779454504-c43409", "ts": "2026-05-27T10:07:13.752537+00:00", "user_ip": "10.7.0.11"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "manual", "table": "1010", "to": "wireguard-1779454504-c43409", "ts": "2026-05-27T10:09:13.715713+00:00", "user_ip": "10.7.0.12"}
{"from": "wireguard-1779454504-c43409", "host": "v3119922.hosted-by-vdsina.ru", "reason": "manual", "table": "1009", "to": "1", "ts": "2026-05-27T10:12:48.953810+00:00", "user_ip": "10.7.0.11"}
{"from": "wireguard-1779454504-c43409", "host": "v3119922.hosted-by-vdsina.ru", "reason": "manual", "table": "1010", "to": "1", "ts": "2026-05-27T10:12:49.408242+00:00", "user_ip": "10.7.0.12"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1007", "to": "awg0", "ts": "2026-05-27T10:18:25.400165+00:00", "user_ip": "10.7.0.9"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1008", "to": "awg0", "ts": "2026-05-27T10:18:27.676019+00:00", "user_ip": "10.7.0.10"}
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "autoswitch_failover", "table": "1011", "to": "awg0", "ts": "2026-05-27T10:18:29.801927+00:00", "user_ip": "10.7.0.13"}

## Classification
registry_drift_classified=true
drift_user=10.7.0.16
drift_user_out_of_scope=true
candidate_still_on_1=true
unsafe_registry_drift=false
classification_basis=drift row is not candidate, target users remains zero, selected_moves=0, hidden movers absent, runtime checkers OK
