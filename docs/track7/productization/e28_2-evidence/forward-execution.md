# E28.2 Forward Execution

date_utc=2026-05-29T10:08:40Z
command_10.7.0.11=v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
command_10.7.0.12=v7-user-switch 10.7.0.12 amneziawg-exec-20260528-10-8-1-14
command_10.7.0.14=v7-user-switch 10.7.0.14 amneziawg-exec-20260528-10-8-1-14
command_10.7.0.15=v7-user-switch 10.7.0.15 amneziawg-exec-20260528-10-8-1-14

exit_code_10.7.0.11=0
stdout_10.7.0.11=[V7] user 10.7.0.11 → amneziawg-exec-20260528-10-8-1-14 / table 1009 / dev v7execwg0;=== ROUTE ===;8.8.8.8 from 10.7.0.11 dev v7execwg0 table 1009 ;    cache iif wg0 ;=== STATE ===;egress=amneziawg-exec-20260528-10-8-1-14;last_switch=1780049320;fail_count=0;
stderr_10.7.0.11=
exit_code_10.7.0.12=0
stdout_10.7.0.12=[V7] user 10.7.0.12 → amneziawg-exec-20260528-10-8-1-14 / table 1010 / dev v7execwg0;=== ROUTE ===;8.8.8.8 from 10.7.0.12 dev v7execwg0 table 1010 ;    cache iif wg0 ;=== STATE ===;egress=amneziawg-exec-20260528-10-8-1-14;last_switch=1780049320;fail_count=0;
stderr_10.7.0.12=
exit_code_10.7.0.14=0
stdout_10.7.0.14=[V7] user 10.7.0.14 → amneziawg-exec-20260528-10-8-1-14 / table 1012 / dev v7execwg0;=== ROUTE ===;8.8.8.8 from 10.7.0.14 dev v7execwg0 table 1012 ;    cache iif wg0 ;=== STATE ===;egress=amneziawg-exec-20260528-10-8-1-14;last_switch=1780049320;fail_count=0;
stderr_10.7.0.14=
exit_code_10.7.0.15=0
stdout_10.7.0.15=[V7] user 10.7.0.15 → amneziawg-exec-20260528-10-8-1-14 / table 1013 / dev v7execwg0;=== ROUTE ===;8.8.8.8 from 10.7.0.15 dev v7execwg0 table 1013 ;    cache iif wg0 ;=== STATE ===;egress=amneziawg-exec-20260528-10-8-1-14;last_switch=1780049321;fail_count=0;
stderr_10.7.0.15=

## Registry Diff
--- /tmp/e28_2/users.before.forward	2026-05-29 01:38:15.013072885 +0300
+++ /tmp/e28_2/users.after.forward	2026-05-29 13:08:41.244883175 +0300
@@ -10,9 +10,9 @@
 ip=10.7.0.8 current=awg3 table=1006 enabled=1
 ip=10.7.0.9 current=awg0 table=1007 enabled=1
 ip=10.7.0.10 current=awg0 table=1008 enabled=1
-ip=10.7.0.11 current=1 table=1009 enabled=1
-ip=10.7.0.12 current=1 table=1010 enabled=1
+ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
+ip=10.7.0.12 current=amneziawg-exec-20260528-10-8-1-14 table=1010 enabled=1
 ip=10.7.0.13 current=awg0 table=1011 enabled=1
-ip=10.7.0.14 current=1 table=1012 enabled=1
-ip=10.7.0.15 current=1 table=1013 enabled=1
+ip=10.7.0.14 current=amneziawg-exec-20260528-10-8-1-14 table=1012 enabled=1
+ip=10.7.0.15 current=amneziawg-exec-20260528-10-8-1-14 table=1013 enabled=1
 ip=10.7.0.16 current=vless table=1014 enabled=1

## Route Table 1009 Diff
--- /tmp/e28_2/route-1009.before.forward	2026-05-29 13:08:40.308894852 +0300
+++ /tmp/e28_2/route-1009.after.forward	2026-05-29 13:08:41.394881304 +0300
@@ -1 +1 @@
-default dev v7e356a192b79 scope link 
+default dev v7execwg0 scope link 

## Route Table 1010 Diff
--- /tmp/e28_2/route-1010.before.forward	2026-05-29 13:08:40.311894814 +0300
+++ /tmp/e28_2/route-1010.after.forward	2026-05-29 13:08:41.397881266 +0300
@@ -1 +1 @@
-default dev v7e356a192b79 scope link 
+default dev v7execwg0 scope link 

## Route Table 1012 Diff
--- /tmp/e28_2/route-1012.before.forward	2026-05-29 13:08:40.313894789 +0300
+++ /tmp/e28_2/route-1012.after.forward	2026-05-29 13:08:41.399881241 +0300
@@ -1 +1 @@
-default dev v7e356a192b79 scope link 
+default dev v7execwg0 scope link 

## Route Table 1013 Diff
--- /tmp/e28_2/route-1013.before.forward	2026-05-29 13:08:40.315894765 +0300
+++ /tmp/e28_2/route-1013.after.forward	2026-05-29 13:08:41.402881204 +0300
@@ -1 +1 @@
-default dev v7e356a192b79 scope link 
+default dev v7execwg0 scope link 
audit_record_hash=8d2d6a7ba121dc077ad4ed477161bbe5a1cbdc11ae99ff52b4519291c26c963e
