# E25.15 Delayed Monitoring B

date_utc=2026-05-28T21:00:57Z
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
drift_row=ip=10.7.0.16 current=vless table=1014 enabled=1
target_users=0
route_get_10_7_0_11=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  
route_get_10_7_0_16=8.8.8.8 from 10.7.0.16 dev tun0 table 1014      cache iif wg0  
selected_moves_count=0
hidden_movers_count=0
runtime_checkers_ok=true
delayed_movement_observed=false
unapproved_user_movement=false
routing_drift=false
audit_tail={"approval_id": "approval-4bbbbf5f5d145367d490d523", "block": "E25.15", "candidate_user": "10.7.0.11", "details": "rc=0;from=1;to=amneziawg-exec-20260528-10-8-1-14;candidate_after=amneziawg-exec-20260528-10-8-1-14", "event": "forward_movement", "operation_id": "e25-15-first-movement-retry-20260528T205228Z", "packet_id": "packet-0671c44ea5024978724e11e9", "record_hash": "f4fd62bec6fff288d951876f6dfd62be3ff19a209e486998c0df022900bc4537", "target": "amneziawg-exec-20260528-10-8-1-14", "ts": "2026-05-28T20:54:13Z"} {"approval_id": "approval-4bbbbf5f5d145367d490d523", "block": "E25.15", "candidate_user": "10.7.0.11", "details": "rc=0;from=amneziawg-exec-20260528-10-8-1-14;to=1;candidate_after=1", "event": "rollback_movement", "operation_id": "e25-15-first-movement-retry-20260528T205228Z", "packet_id": "packet-0671c44ea5024978724e11e9", "record_hash": "792c6d82b6d8ced4b96b68b1562fd2bde601cb0e6af91c37a07f54295e9865c1", "target": "amneziawg-exec-20260528-10-8-1-14", "ts": "2026-05-28T20:57:19Z"} 
