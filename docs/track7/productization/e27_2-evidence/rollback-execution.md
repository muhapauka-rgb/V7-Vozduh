# E27.2 Rollback Execution

date_utc=2026-05-28T22:38:14Z
command_A=v7-user-switch 10.7.0.11 1
command_B=v7-user-switch 10.7.0.12 1

exit_code_A=0
stdout_A=[V7] user 10.7.0.11 → 1 / table 1009 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780007894;fail_count=0;
stderr_A=
exit_code_B=0
stdout_B=[V7] user 10.7.0.12 → 1 / table 1010 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780007895;fail_count=0;
stderr_B=

## Registry Diff
--- /tmp/e27_2/users.before.rollback	2026-05-29 01:33:37.138507996 +0300
+++ /tmp/e27_2/users.after.rollback	2026-05-29 01:38:15.013072885 +0300
@@ -10,8 +10,8 @@
 ip=10.7.0.8 current=awg3 table=1006 enabled=1
 ip=10.7.0.9 current=awg0 table=1007 enabled=1
 ip=10.7.0.10 current=awg0 table=1008 enabled=1
-ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
-ip=10.7.0.12 current=amneziawg-exec-20260528-10-8-1-14 table=1010 enabled=1
+ip=10.7.0.11 current=1 table=1009 enabled=1
+ip=10.7.0.12 current=1 table=1010 enabled=1
 ip=10.7.0.13 current=awg0 table=1011 enabled=1
 ip=10.7.0.14 current=1 table=1012 enabled=1
 ip=10.7.0.15 current=1 table=1013 enabled=1

## Route Table 1009 Diff
--- /tmp/e27_2/route-1009.before.rollback	2026-05-29 01:38:14.546078658 +0300
+++ /tmp/e27_2/route-1009.after.rollback	2026-05-29 01:38:15.168070969 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1010 Diff
--- /tmp/e27_2/route-1010.before.rollback	2026-05-29 01:38:14.551078596 +0300
+++ /tmp/e27_2/route-1010.after.rollback	2026-05-29 01:38:15.171070932 +0300
@@ -1 +1 @@
-default dev v7execwg0 scope link 
+default dev v7e356a192b79 scope link 
audit_record_hash=08ea660df685b3ae53422ac756aa08d7632259f5e33f391b1887cc73fae0d016
