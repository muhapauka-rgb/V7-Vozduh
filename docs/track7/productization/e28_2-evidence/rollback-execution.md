# E28.2 Rollback Execution

date_utc=2026-05-29T10:13:56Z
command_10.7.0.11=v7-user-switch 10.7.0.11 1
command_10.7.0.12=v7-user-switch 10.7.0.12 1
command_10.7.0.14=v7-user-switch 10.7.0.14 1
command_10.7.0.15=v7-user-switch 10.7.0.15 1

exit_code_10.7.0.11=0
stdout_10.7.0.11=[V7] user 10.7.0.11 → 1 / table 1009 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780049636;fail_count=0;
stderr_10.7.0.11=
exit_code_10.7.0.12=0
stdout_10.7.0.12=[V7] user 10.7.0.12 → 1 / table 1010 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780049636;fail_count=0;
stderr_10.7.0.12=
exit_code_10.7.0.14=0
stdout_10.7.0.14=[V7] user 10.7.0.14 → 1 / table 1012 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780049637;fail_count=0;
stderr_10.7.0.14=
exit_code_10.7.0.15=0
stdout_10.7.0.15=[V7] user 10.7.0.15 → 1 / table 1013 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780049637;fail_count=0;
stderr_10.7.0.15=

## Registry Diff
--- /tmp/e28_2/users.before.rollback	2026-05-29 13:08:41.244883175 +0300
+++ /tmp/e28_2/users.after.rollback	2026-05-29 13:13:57.495937787 +0300
@@ -10,9 +10,9 @@
 ip=10.7.0.8 current=awg3 table=1006 enabled=1
 ip=10.7.0.9 current=awg0 table=1007 enabled=1
 ip=10.7.0.10 current=awg0 table=1008 enabled=1
-ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
-ip=10.7.0.12 current=amneziawg-exec-20260528-10-8-1-14 table=1010 enabled=1
+ip=10.7.0.11 current=1 table=1009 enabled=1
+ip=10.7.0.12 current=1 table=1010 enabled=1
 ip=10.7.0.13 current=awg0 table=1011 enabled=1
-ip=10.7.0.14 current=amneziawg-exec-20260528-10-8-1-14 table=1012 enabled=1
-ip=10.7.0.15 current=amneziawg-exec-20260528-10-8-1-14 table=1013 enabled=1
+ip=10.7.0.14 current=1 table=1012 enabled=1
+ip=10.7.0.15 current=1 table=1013 enabled=1
 ip=10.7.0.16 current=vless table=1014 enabled=1

## Route Table 1009 Diff
--- /tmp/e28_2/route-1009.before.rollback	2026-05-29 13:13:56.532949801 +0300
+++ /tmp/e28_2/route-1009.after.rollback	2026-05-29 13:13:57.653935816 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1010 Diff
--- /tmp/e28_2/route-1010.before.rollback	2026-05-29 13:13:56.535949763 +0300
+++ /tmp/e28_2/route-1010.after.rollback	2026-05-29 13:13:57.655935791 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1012 Diff
--- /tmp/e28_2/route-1012.before.rollback	2026-05-29 13:13:56.538949726 +0300
+++ /tmp/e28_2/route-1012.after.rollback	2026-05-29 13:13:57.658935754 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1013 Diff
--- /tmp/e28_2/route-1013.before.rollback	2026-05-29 13:13:56.541949689 +0300
+++ /tmp/e28_2/route-1013.after.rollback	2026-05-29 13:13:57.661935716 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link 
+default dev v7e356a192b79 scope link 
audit_record_hash=dfe8fce3edb88657c3d89056621bf2da7805bb533b41094ab5de8e04e979894a
