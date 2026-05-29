# E25.15 Forward Execution

timestamp_start_utc=2026-05-28T20:54:09Z
timestamp_end_utc=2026-05-28T20:54:10Z
command=v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
exit_code=0
audit_record_hash=f4fd62bec6fff288d951876f6dfd62be3ff19a209e486998c0df022900bc4537

## Stdout
stdout: [V7] user 10.7.0.11 → amneziawg-exec-20260528-10-8-1-14 / table 1009 / dev v7execwg0
stdout: === ROUTE ===
stdout: 8.8.8.8 from 10.7.0.11 dev v7execwg0 table 1009 
stdout:     cache iif wg0 
stdout: === STATE ===
stdout: egress=amneziawg-exec-20260528-10-8-1-14
stdout: last_switch=1780001649
stdout: fail_count=0

## Stderr

## Before
candidate_row_before=ip=10.7.0.11 current=1 table=1009 enabled=1
target_users_before=0
route_table_1009_before=default dev v7e356a192b79 scope link  
route_get_before=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  
drift_row_before=ip=10.7.0.16 current=vless table=1014 enabled=1

## After
candidate_row_after=ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
target_users_after=1
route_table_1009_after=default dev v7execwg0 scope link  
route_get_after=8.8.8.8 from 10.7.0.11 dev v7execwg0 table 1009      cache iif wg0  
drift_row_after=ip=10.7.0.16 current=vless table=1014 enabled=1
selected_moves_after=0
hidden_movers_after=0
runtime_checkers_ok_after=true

## Registry Diff
--- /tmp/e25_15_users_before_forward.registry	2026-05-28 23:54:09.753723392 +0300
+++ /tmp/e25_15_users_after_forward.registry	2026-05-28 23:54:10.157512047 +0300
@@ -10,7 +10,7 @@
 ip=10.7.0.8 current=awg3 table=1006 enabled=1
 ip=10.7.0.9 current=awg0 table=1007 enabled=1
 ip=10.7.0.10 current=awg0 table=1008 enabled=1
-ip=10.7.0.11 current=1 table=1009 enabled=1
+ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
 ip=10.7.0.12 current=1 table=1010 enabled=1
 ip=10.7.0.13 current=awg0 table=1011 enabled=1
 ip=10.7.0.14 current=1 table=1012 enabled=1

## Route Table Diff
--- /tmp/e25_15_route_before_forward.txt	2026-05-28 23:54:09.768466287 +0300
+++ /tmp/e25_15_route_after_forward.txt	2026-05-28 23:54:10.166461395 +0300
@@ -1 +1 @@
-default dev v7e356a192b79 scope link  
\ No newline at end of file
+default dev v7execwg0 scope link  
\ No newline at end of file
