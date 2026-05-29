# E25.7 continuation rollback/removal raw evidence
timestamp_utc=2026-05-28T12:33:23Z
hostname=v3119922.hosted-by-vdsina.ru

## pre_removal
$ ip link show v7execwg0
443: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
$ wg show v7execwg0
interface: v7execwg0
  public key: Tx/LUxab6MMcgUiENrSeGe8kEpmIlLUngXroHzkuSRk=
  private key: (hidden)
  listening port: 54926

peer: NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=
  preshared key: (hidden)
  endpoint: 195.2.79.116:51889
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 1.59 KiB sent
  persistent keepalive: every 10 seconds
$ ip route show table 1250
$ ip route show default
default via 195.2.79.1 dev ens3 proto static onlink 
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 1.1.1.1
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry

## removal
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
active_config_archived=/root/e25_7_continuation_v7execwg0.conf.removed.20260528T123323Z
c8621f5b3a07a1753a1d4143783de32cd251350cea6e65d0f84ded487753b2e5  /root/e25_7_continuation_v7execwg0.conf.removed.20260528T123323Z
$ ip route flush table 1250

## post_removal_safety
$ ip link show v7execwg0
Device "v7execwg0" does not exist.
exit=1
$ test ! -e /etc/wireguard/v7execwg0.conf
$ ip route show table 1250
$ ip route show default
default via 195.2.79.1 dev ens3 proto static onlink 
$ ip rule show
0:	from all lookup local
50:	from all fwmark 0x77 lookup 70
55:	from 195.2.79.116 lookup main
60:	from all uidrange 995-995 lookup 100
100:	from 10.0.0.2 lookup 100
101:	from 10.0.0.3 lookup 101
104:	from 10.0.0.6 lookup 104
1000:	from 10.7.0.2 lookup 1000
1001:	from 10.7.0.3 lookup 1001
1002:	from 10.7.0.4 lookup 1002
1003:	from 10.7.0.5 lookup 1003
1004:	from 10.7.0.6 lookup 1004
1006:	from 10.7.0.8 lookup 1006
1007:	from 10.7.0.9 lookup 1007
1008:	from 10.7.0.10 lookup 1008
1009:	from 10.7.0.11 lookup 1009
1010:	from 10.7.0.12 lookup 1010
1011:	from 10.7.0.13 lookup 1011
1012:	from 10.7.0.14 lookup 1012
1013:	from 10.7.0.15 lookup 1013
32766:	from all lookup main
32767:	from all lookup default
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 1.1.1.1
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
$ grep -n 10.7.0.11 /opt/v7/egress/state/users.registry
13:ip=10.7.0.11 current=1 table=1009 enabled=1
$ ip route show table 1009
default dev v7e356a192b79 scope link 
$ ip route get 8.8.8.8 from 10.7.0.11 iif wg0
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
$ find /opt/v7 -maxdepth 5 -iname *selected*move* -type f -printf %p %s bytes\\n
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1

## runtime_checkers_after_removal
### v7-reconcile-check rc=0
===== V7 RECONCILE CHECK =====
2026-05-28T15:33:24+03:00
state_dir=/opt/v7/egress/state
users_registry=/opt/v7/egress/state/users.registry
egress_registry=/opt/v7/egress/state/egress.registry
wg_if=wg0

===== USERS =====
user=10.0.0.2 enabled=1 current=awg3 table=100
user=10.0.0.3 enabled=1 current=awg3 table=101
user=10.0.0.6 enabled=1 current=awg3 table=104
user=10.7.0.3 enabled=1 current=awg3 table=1001
user=10.7.0.2 enabled=1 current=awg3 table=1000
user=10.7.0.4 enabled=1 current=awg3 table=1002
user=10.7.0.5 enabled=1 current=awg3 table=1003
user=10.7.0.6 enabled=1 current=awg3 table=1004
user=10.7.0.7 enabled=0 current=vless table=1005
user=10.7.0.8 enabled=1 current=awg3 table=1006
user=10.7.0.9 enabled=1 current=awg0 table=1007
user=10.7.0.10 enabled=1 current=awg0 table=1008
user=10.7.0.11 enabled=1 current=1 table=1009
user=10.7.0.12 enabled=1 current=1 table=1010
user=10.7.0.13 enabled=1 current=awg0 table=1011
user=10.7.0.14 enabled=1 current=1 table=1012
user=10.7.0.15 enabled=1 current=1 table=1013

===== RESULT =====
warnings=0
errors=0
V7_RECONCILE_RESULT=OK
### v7-user-route-check rc=0
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.11 table=1009 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
OK: user=10.7.0.11 route_get uses v7e356a192b79

USER=10.7.0.12 TABLE=1010 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.12 registry matches assignment
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.12 table=1010 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif wg0 
OK: user=10.7.0.12 route_get uses v7e356a192b79

USER=10.7.0.13 TABLE=1011 REGISTRY_EGRESS=awg0 ASSIGN_EGRESS=awg0 EXPECTED_DEV=awg0
OK: user=10.7.0.13 registry matches assignment
table_route=default dev awg0 scope link 
OK: user=10.7.0.13 table=1011 default dev awg0
route_get=8.8.8.8 from 10.7.0.13 dev awg0 table 1011 
    cache iif wg0 
OK: user=10.7.0.13 route_get uses awg0

USER=10.7.0.14 TABLE=1012 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.14 registry matches assignment
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.14 table=1012 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0 
OK: user=10.7.0.14 route_get uses v7e356a192b79

USER=10.7.0.15 TABLE=1013 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.15 registry matches assignment
table_route=default dev v7e356a192b79 scope link 
OK: user=10.7.0.15 table=1013 default dev v7e356a192b79
route_get=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0 
OK: user=10.7.0.15 route_get uses v7e356a192b79

===== RESULT =====
V7_USER_ROUTE_CHECK=OK
### v7-killswitch-check rc=0
OK: user=10.7.0.3 route_get uses expected egress
user=10.7.0.2 table=1000 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.2 dev awg3 table 1000 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.2 route_get uses expected egress
user=10.7.0.4 table=1002 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.4 dev awg3 table 1002 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.4 route_get uses expected egress
user=10.7.0.5 table=1003 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.5 dev awg3 table 1003 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.5 route_get uses expected egress
user=10.7.0.6 table=1004 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.6 dev awg3 table 1004 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.6 route_get uses expected egress
user=10.7.0.8 table=1006 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.8 dev awg3 table 1006 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.7.0.8 route_get uses expected egress
user=10.7.0.9 table=1007 current=awg0 expected_if=awg0 route=8.8.8.8 from 10.7.0.9 dev awg0 table 1007 
    cache iif wg0  table_default=default dev awg0 scope link 
OK: user=10.7.0.9 route_get uses expected egress
user=10.7.0.10 table=1008 current=awg0 expected_if=awg0 route=8.8.8.8 from 10.7.0.10 dev awg0 table 1008 
    cache iif wg0  table_default=default dev awg0 scope link 
OK: user=10.7.0.10 route_get uses expected egress
user=10.7.0.11 table=1009 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.11 route_get uses expected egress
user=10.7.0.12 table=1010 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.12 route_get uses expected egress
user=10.7.0.13 table=1011 current=awg0 expected_if=awg0 route=8.8.8.8 from 10.7.0.13 dev awg0 table 1011 
    cache iif wg0  table_default=default dev awg0 scope link 
OK: user=10.7.0.13 route_get uses expected egress
user=10.7.0.14 table=1012 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.14 route_get uses expected egress
user=10.7.0.15 table=1013 current=1 expected_if=v7e356a192b79 route=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0  table_default=default dev v7e356a192b79 scope link 
OK: user=10.7.0.15 route_get uses expected egress

===== RESULT =====
V7_KILLSWITCH_CHECK=OK
### v7-provisioning-reconcile-check rc=0
mss_clamp_v7e356a192b79=present_nft
nat_v7edb0c189291=present_nft
mss_clamp_v7edb0c189291=present_nft

===== USERS =====
user=10.0.0.2 table=100 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.0.0.2 dev awg3 table 100 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.0.0.3 table=101 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.0.0.3 dev awg3 table 101 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.0.0.6 table=104 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.0.0.6 dev awg3 table 104 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.3 table=1001 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.3 dev awg3 table 1001 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.2 table=1000 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.2 dev awg3 table 1000 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.4 table=1002 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.4 dev awg3 table 1002 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.5 table=1003 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.5 dev awg3 table 1003 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.6 table=1004 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.6 dev awg3 table 1004 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.8 table=1006 current=awg3 expected_if=awg3 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.8 dev awg3 table 1006 
    cache iif wg0  table_detail=default dev awg3 scope link 
user=10.7.0.9 table=1007 current=awg0 expected_if=awg0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.9 dev awg0 table 1007 
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.10 table=1008 current=awg0 expected_if=awg0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.10 dev awg0 table 1008 
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.11 table=1009 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.12 table=1010 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.13 table=1011 current=awg0 expected_if=awg0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.13 dev awg0 table 1011 
    cache iif wg0  table_detail=default dev awg0 scope link 
user=10.7.0.14 table=1012 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 
user=10.7.0.15 table=1013 current=1 expected_if=v7e356a192b79 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif wg0  table_detail=default dev v7e356a192b79 scope link 

===== RESULT =====
V7_PROVISIONING_RECONCILE_CHECK=OK
runtime_checkers_ok=true

## restore_settle_if_available
$ v7-restore-settle-gate --pre-restore --pretty
V7 restore settle gate (read-only)
runtime_commands_executed=False
mode=pre-restore
gate_status=NO-GO
sample_count=0
required_samples=3
samples_span_seconds=0
apply_timer_intervals_covered=0.0
required_apply_timer_intervals=2
selected_moves_by_sample=[]
telegram_hard_blocked_by_sample=[]
egress_1_eligible_by_sample=[]
movement_count_by_sample=[]
registry_stable=unknown
egress_registry_stable=unknown
checkers_ok=False
hidden_movers_observed=False
moved_users=[]
recommended_action=no_go_review_restore_settle_evidence
execution_allowed_now=False
reasons:
  - sample_count_below_required:0<3
  - apply_timer_intervals_below_required:0.00<2
  - runtime_checker_failure_observed
$ v7-restore-settle-gate --pre-restore --json
{
  "apply_timer_intervals_covered": 0.0,
  "apply_timer_seconds": 20,
  "checkers_ok": false,
  "egress_1_eligible_by_sample": [],
  "egress_registry_stable": "unknown",
  "execution_allowed_now": false,
  "forbidden_commands_called": false,
  "gate_status": "NO-GO",
  "hidden_movers_observed": false,
  "interval_seconds": 60,
  "mode": "pre-restore",
  "moved_users": [],
  "movement_count_by_sample": [],
  "mutation": false,
  "read_only": true,
  "reasons": [
    "sample_count_below_required:0<3",
    "apply_timer_intervals_below_required:0.00<2",
    "runtime_checker_failure_observed"
  ],
  "recommended_action": "no_go_review_restore_settle_evidence",
  "registry_stable": "unknown",
  "required_apply_timer_intervals": 2,
  "required_samples": 3,
  "runtime_commands_executed": false,
  "sample_count": 0,
  "sample_sources": [],
  "samples_span_seconds": 0,
  "selected_moves_by_sample": [],
  "state_dir": "docs/track7/control-plane/e11_13-evidence/restore-settle-samples",
  "telegram_hard_blocked_by_sample": [],
  "tool": "v7-restore-settle-gate"
}
