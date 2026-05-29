# E30.1 Candidate Pool Normalization

date_utc=2026-05-29T14:06:49Z
command_10.7.0.2=v7-user-switch 10.7.0.2 1
exit_code_10.7.0.2=0
stdout_10.7.0.2=[V7] user 10.7.0.2 → 1 / table 1000 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.2 dev v7e356a192b79 table 1000 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780063609;fail_count=0;
stderr_10.7.0.2=
command_10.7.0.3=v7-user-switch 10.7.0.3 1
exit_code_10.7.0.3=0
stdout_10.7.0.3=[V7] user 10.7.0.3 → 1 / table 1001 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.3 dev v7e356a192b79 table 1001 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780063609;fail_count=0;
stderr_10.7.0.3=
command_10.7.0.4=v7-user-switch 10.7.0.4 1
exit_code_10.7.0.4=0
stdout_10.7.0.4=[V7] user 10.7.0.4 → 1 / table 1002 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.4 dev v7e356a192b79 table 1002 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780063610;fail_count=0;
stderr_10.7.0.4=
command_10.7.0.5=v7-user-switch 10.7.0.5 1
exit_code_10.7.0.5=0
stdout_10.7.0.5=[V7] user 10.7.0.5 → 1 / table 1003 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.5 dev v7e356a192b79 table 1003 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780063610;fail_count=0;
stderr_10.7.0.5=
command_10.7.0.6=v7-user-switch 10.7.0.6 1
exit_code_10.7.0.6=0
stdout_10.7.0.6=[V7] user 10.7.0.6 → 1 / table 1004 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.6 dev v7e356a192b79 table 1004 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780063611;fail_count=0;
stderr_10.7.0.6=
command_10.7.0.8=v7-user-switch 10.7.0.8 1
exit_code_10.7.0.8=0
stdout_10.7.0.8=[V7] user 10.7.0.8 → 1 / table 1006 / dev v7e356a192b79;=== ROUTE ===;8.8.8.8 from 10.7.0.8 dev v7e356a192b79 table 1006 ;    cache iif wg0 ;=== STATE ===;egress=1;last_switch=1780063611;fail_count=0;
stderr_10.7.0.8=

## Registry Diff
--- /tmp/e30_1/users.before.normalization	2026-05-29 13:13:57.495937787 +0300
+++ /tmp/e30_1/users.after.normalization	2026-05-29 17:06:51.480845618 +0300
@@ -1,13 +1,13 @@
 ip=10.0.0.2 current=awg3 table=100 enabled=1
 ip=10.0.0.3 current=awg3 table=101 enabled=1
 ip=10.0.0.6 current=awg3 table=104 enabled=1
-ip=10.7.0.3 current=awg3 table=1001 enabled=1
-ip=10.7.0.2 current=awg3 table=1000 enabled=1
-ip=10.7.0.4 current=awg3 table=1002 enabled=1
-ip=10.7.0.5 current=awg3 table=1003 enabled=1
-ip=10.7.0.6 current=awg3 table=1004 enabled=1
+ip=10.7.0.3 current=1 table=1001 enabled=1
+ip=10.7.0.2 current=1 table=1000 enabled=1
+ip=10.7.0.4 current=1 table=1002 enabled=1
+ip=10.7.0.5 current=1 table=1003 enabled=1
+ip=10.7.0.6 current=1 table=1004 enabled=1
 ip=10.7.0.7 current=vless table=1005 enabled=0
-ip=10.7.0.8 current=awg3 table=1006 enabled=1
+ip=10.7.0.8 current=1 table=1006 enabled=1
 ip=10.7.0.9 current=awg0 table=1007 enabled=1
 ip=10.7.0.10 current=awg0 table=1008 enabled=1
 ip=10.7.0.11 current=1 table=1009 enabled=1

## Route Table 1000 Diff
--- /tmp/e30_1/route-1000.before.normalization	2026-05-29 17:06:49.274873131 +0300
+++ /tmp/e30_1/route-1000.after.normalization	2026-05-29 17:06:51.703842836 +0300
@@ -1 +1 @@
-default dev awg3 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1001 Diff
--- /tmp/e30_1/route-1001.before.normalization	2026-05-29 17:06:49.277873094 +0300
+++ /tmp/e30_1/route-1001.after.normalization	2026-05-29 17:06:51.705842811 +0300
@@ -1 +1 @@
-default dev awg3 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1002 Diff
--- /tmp/e30_1/route-1002.before.normalization	2026-05-29 17:06:49.281873044 +0300
+++ /tmp/e30_1/route-1002.after.normalization	2026-05-29 17:06:51.710842749 +0300
@@ -1 +1 @@
-default dev awg3 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1003 Diff
--- /tmp/e30_1/route-1003.before.normalization	2026-05-29 17:06:49.285872994 +0300
+++ /tmp/e30_1/route-1003.after.normalization	2026-05-29 17:06:51.713842712 +0300
@@ -1 +1 @@
-default dev awg3 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1004 Diff
--- /tmp/e30_1/route-1004.before.normalization	2026-05-29 17:06:49.289872944 +0300
+++ /tmp/e30_1/route-1004.after.normalization	2026-05-29 17:06:51.716842674 +0300
@@ -1 +1 @@
-default dev awg3 scope link 
+default dev v7e356a192b79 scope link 

## Route Table 1006 Diff
--- /tmp/e30_1/route-1006.before.normalization	2026-05-29 17:06:49.292872907 +0300
+++ /tmp/e30_1/route-1006.after.normalization	2026-05-29 17:06:51.719842637 +0300
@@ -1 +1 @@
-default dev awg3 scope link 
+default dev v7e356a192b79 scope link 
diff_status=OK
audit_record_hash=a39c9fc75d1b41e2cf2eba9b081b7a97af79c6f8dc46fbe45f7f51570f67b70e
