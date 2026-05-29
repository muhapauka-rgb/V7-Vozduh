# E25.9 profile acquisition check raw evidence
timestamp_utc=2026-05-28T13:48:46Z
hostname=v3119922.hosted-by-vdsina.ru


## expected_import_locations
dir_missing=/root/v7-execution-profile-import
dir_missing=/root/v7-execution-profile-upload
dir_missing=/root/v7-external-execution-profile
dir_missing=/opt/v7/operator-import
dir_missing=/opt/v7/egress/import
dir_missing=/tmp/v7-execution-profile-import
dir_missing=/root/v7-new-profile
dir_missing=/root/v7-import

## recent_profile_like_files_since_e25_8
2026-05-28T16:48:36.5620289980 /opt/v7/egress/state/egress-load-summary.json 2034 bytes\n2026-05-28T16:48:42.4679370070 /opt/v7/egress/state/telegram-sentinel.json 10588 bytes\n2026-05-28T16:47:41.5190095320 /opt/v7/egress/state/egress-quality-summary.json 10356 bytes\n2026-05-28T16:48:14.2649747320 /opt/v7/egress/state/v7-state.json 10175 bytes\n2026-05-28T16:48:46.5665730130 /opt/v7/egress/state/service-matrix.json 101761 bytes\n2026-05-28T16:47:41.5333817530 /opt/v7/egress/state/egress-quality-ring.json 687217 bytes\n2026-05-28T16:33:37.0637134800 /opt/v7/egress/state/service-matrix-refresh-summary.json 16033 bytes\n

## candidate_classification_from_expected_locations

## known_dead_profiles_guard
dead_profile_e25_7=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
dead_profile_e25_8=/etc/wireguard/vps.conf
known_dead_present=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf sha256=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1
known_dead_present=/etc/wireguard/vps.conf sha256=dbc463e711667f2d8d6ed87f191f4b2c17bb5d2eada29e6f363bf6a28de3d3aa

## runtime_safety_snapshot
$ test ! -e /etc/wireguard/v7execwg0.conf
$ ip link show v7execwg0
Device "v7execwg0" does not exist.
exit=1
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

## runtime_checkers
v7-reconcile-check rc=0
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
v7-user-route-check rc=0
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
v7-killswitch-check rc=0
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
v7-provisioning-reconcile-check rc=0
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
