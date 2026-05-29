# E25.15 Rollback Execution

timestamp_start_utc=2026-05-28T20:57:16Z
timestamp_end_utc=2026-05-28T20:57:16Z
command=v7-user-switch 10.7.0.11 1
exit_code=0
audit_record_hash=792c6d82b6d8ced4b96b68b1562fd2bde601cb0e6af91c37a07f54295e9865c1

## Stdout
stdout: [V7] user 10.7.0.11 → 1 / table 1009 / dev v7e356a192b79
stdout: === ROUTE ===
stdout: 8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
stdout:     cache iif wg0 
stdout: === STATE ===
stdout: egress=1
stdout: last_switch=1780001836
stdout: fail_count=0

## Stderr

## Before
candidate_row_before=ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
target_users_before=1
route_table_1009_before=default dev v7execwg0 scope link  
route_get_before=8.8.8.8 from 10.7.0.11 dev v7execwg0 table 1009      cache iif wg0  
drift_row_before=ip=10.7.0.16 current=vless table=1014 enabled=1

## After
candidate_row_after=ip=10.7.0.11 current=1 table=1009 enabled=1
target_users_after=0
route_table_1009_after=default dev v7e356a192b79 scope link  
route_get_after=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009      cache iif wg0  
drift_row_after=ip=10.7.0.16 current=vless table=1014 enabled=1
selected_moves_after=0
hidden_movers_after=0
runtime_checkers_ok_after=true

## Registry Diff
--- /tmp/e25_15_users_before_rollback.registry	2026-05-28 23:57:15.967520553 +0300
+++ /tmp/e25_15_users_after_rollback.registry	2026-05-28 23:57:16.297971381 +0300
@@ -10,7 +10,7 @@
 ip=10.7.0.8 current=awg3 table=1006 enabled=1
 ip=10.7.0.9 current=awg0 table=1007 enabled=1
 ip=10.7.0.10 current=awg0 table=1008 enabled=1
-ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
+ip=10.7.0.11 current=1 table=1009 enabled=1
 ip=10.7.0.12 current=1 table=1010 enabled=1
 ip=10.7.0.13 current=awg0 table=1011 enabled=1
 ip=10.7.0.14 current=1 table=1012 enabled=1

## Route Table Diff
--- /tmp/e25_15_route_before_rollback.txt	2026-05-28 23:57:15.974177313 +0300
+++ /tmp/e25_15_route_after_rollback.txt	2026-05-28 23:57:16.304173257 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link  
\ No newline at end of file
+default dev v7e356a192b79 scope link  
\ No newline at end of file
