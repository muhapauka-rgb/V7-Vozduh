# E25.7 continuation fresh safe activation raw evidence
timestamp_utc=2026-05-28T12:29:07Z
hostname=v3119922.hosted-by-vdsina.ru


## pre_state
$ ip link show v7execwg0
Device "v7execwg0" does not exist.
exit=1
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
users_hash_before=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash_before=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
dns_hash_before=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
default_route_hash_before=4a75b4e867418b1a91218f8bcfc5127436d4662255c27c5f45eeb8e5965bb324
ip_rule_hash_before=5da4d16e6a4bf08ccded30b7050fdf4caddadeb2c3bb5bdbd0832bbd7a1f0a05
table_1009_hash_before=faa64ed459ed4ff6c2f427525116646eff7edfcad87712b10b4281cc795621ab
$ grep -n 10.7.0.11 /opt/v7/egress/state/users.registry
13:ip=10.7.0.11 current=1 table=1009 enabled=1
$ ip route show table 1009
default dev v7e356a192b79 scope link 
$ ip route get 8.8.8.8 from 10.7.0.11 iif wg0
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
$ ip route show default
default via 195.2.79.1 dev ens3 proto static onlink 
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 1.1.1.1

## selected_moves_and_hidden_movers_before
$ find /opt/v7 -maxdepth 5 -iname *selected*move* -type f -printf %p %s bytes\\n
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1

## runtime_checkers_before
$ v7-reconcile-check
===== V7 RECONCILE CHECK =====
2026-05-28T15:29:07+03:00
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
$ v7-user-route-check
===== V7 USER ROUTE REALITY CHECK =====
2026-05-28T15:29:08+03:00

USER=10.0.0.2 TABLE=100 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.0.0.2 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.0.0.2 table=100 default dev awg3
route_get=8.8.8.8 from 10.0.0.2 dev awg3 table 100 
    cache iif wg0 
OK: user=10.0.0.2 route_get uses awg3

USER=10.0.0.3 TABLE=101 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.0.0.3 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.0.0.3 table=101 default dev awg3
route_get=8.8.8.8 from 10.0.0.3 dev awg3 table 101 
    cache iif wg0 
OK: user=10.0.0.3 route_get uses awg3

USER=10.0.0.6 TABLE=104 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.0.0.6 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.0.0.6 table=104 default dev awg3
route_get=8.8.8.8 from 10.0.0.6 dev awg3 table 104 
    cache iif wg0 
OK: user=10.0.0.6 route_get uses awg3

USER=10.7.0.3 TABLE=1001 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.3 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.3 table=1001 default dev awg3
route_get=8.8.8.8 from 10.7.0.3 dev awg3 table 1001 
    cache iif wg0 
OK: user=10.7.0.3 route_get uses awg3

USER=10.7.0.2 TABLE=1000 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.2 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.2 table=1000 default dev awg3
route_get=8.8.8.8 from 10.7.0.2 dev awg3 table 1000 
    cache iif wg0 
OK: user=10.7.0.2 route_get uses awg3

USER=10.7.0.4 TABLE=1002 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.4 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.4 table=1002 default dev awg3
route_get=8.8.8.8 from 10.7.0.4 dev awg3 table 1002 
    cache iif wg0 
OK: user=10.7.0.4 route_get uses awg3

USER=10.7.0.5 TABLE=1003 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.5 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.5 table=1003 default dev awg3
route_get=8.8.8.8 from 10.7.0.5 dev awg3 table 1003 
    cache iif wg0 
OK: user=10.7.0.5 route_get uses awg3

USER=10.7.0.6 TABLE=1004 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.6 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.6 table=1004 default dev awg3
route_get=8.8.8.8 from 10.7.0.6 dev awg3 table 1004 
    cache iif wg0 
OK: user=10.7.0.6 route_get uses awg3

USER=10.7.0.8 TABLE=1006 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.8 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.8 table=1006 default dev awg3
route_get=8.8.8.8 from 10.7.0.8 dev awg3 table 1006 
    cache iif wg0 
OK: user=10.7.0.8 route_get uses awg3

USER=10.7.0.9 TABLE=1007 REGISTRY_EGRESS=awg0 ASSIGN_EGRESS=awg0 EXPECTED_DEV=awg0
OK: user=10.7.0.9 registry matches assignment
table_route=default dev awg0 scope link 
OK: user=10.7.0.9 table=1007 default dev awg0
route_get=8.8.8.8 from 10.7.0.9 dev awg0 table 1007 
    cache iif wg0 
OK: user=10.7.0.9 route_get uses awg0

USER=10.7.0.10 TABLE=1008 REGISTRY_EGRESS=awg0 ASSIGN_EGRESS=awg0 EXPECTED_DEV=awg0
OK: user=10.7.0.10 registry matches assignment
table_route=default dev awg0 scope link 
OK: user=10.7.0.10 table=1008 default dev awg0
route_get=8.8.8.8 from 10.7.0.10 dev awg0 table 1008 
    cache iif wg0 
OK: user=10.7.0.10 route_get uses awg0

USER=10.7.0.11 TABLE=1009 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.11 registry matches assignment
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
$ v7-killswitch-check
===== V7 KILL SWITCH CHECK =====
2026-05-28T15:29:09+03:00
vpn_subnets=10.0.0.0/24,10.7.0.0/22
public_if=ens3
egress_ifs=awg0 awg3 tun0 v7e06a394c478 v7e356a192b79 v7edb0c189291
table=present
client_source_set=present
client_source_subnet=10.0.0.0/24 present
reverse_route_subnet=10.0.0.0/24 present
client_source_subnet=10.7.0.0/22 present
reverse_route_subnet=10.7.0.0/22 present
direct_leak_drop_rule=present
direct_whitelist_rule=present
sysctl_net.ipv4.ip_forward = 1
direct_fwmark_rule=present
direct_fwmark_precedes_user_rules=OK
direct_route_table=present
direct_mark_rule=present
dns_capture_udp=present
dns_capture_tcp=present
nat_awg0=present
mss_clamp_awg0=present_nft
nat_awg3=present
mss_clamp_awg3=present_nft
nat_tun0=present
mss_clamp_tun0=present_nft
nat_v7e06a394c478=present
mss_clamp_v7e06a394c478=present_nft
nat_v7e356a192b79=present
mss_clamp_v7e356a192b79=present_nft
nat_v7edb0c189291=present
mss_clamp_v7edb0c189291=present_nft

===== USER ROUTE CHECK =====
user=10.0.0.2 table=100 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.0.0.2 dev awg3 table 100 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.0.0.2 route_get uses expected egress
user=10.0.0.3 table=101 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.0.0.3 dev awg3 table 101 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.0.0.3 route_get uses expected egress
user=10.0.0.6 table=104 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.0.0.6 dev awg3 table 104 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.0.0.6 route_get uses expected egress
user=10.7.0.3 table=1001 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.3 dev awg3 table 1001 
    cache iif wg0  table_default=default dev awg3 scope link 
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
$ v7-provisioning-reconcile-check
===== V7 PROVISIONING RECONCILE CHECK =====
2026-05-28T15:29:10+03:00
registry=/opt/v7/egress/state/users.registry
vpn_subnets=10.0.0.0/24,10.7.0.0/22
public_if=ens3
egress_ifs=awg0 awg3 tun0 v7e06a394c478 v7e356a192b79 v7edb0c189291

===== SOURCE SET =====
client_source_set=present
client_source_subnet=10.0.0.0/24 present
reverse_route_subnet=10.0.0.0/24 present
client_source_subnet=10.7.0.0/22 present
reverse_route_subnet=10.7.0.0/22 present

===== NAT =====
nat_awg0=present_nft
mss_clamp_awg0=present_nft
nat_awg3=present_nft
mss_clamp_awg3=present_nft
nat_tun0=present_nft
mss_clamp_tun0=present_nft
nat_v7e06a394c478=present_nft
mss_clamp_v7e06a394c478=present_nft
nat_v7e356a192b79=present_nft
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

## normalized_config_creation
666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1  /root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
c838438d6a6d5f82d8137c6d1aaa0682ccf52446c7bc563168009e2873ee16ed  /etc/wireguard/v7execwg0.conf
[Interface]
PrivateKey = <redacted>
Address = 10.89.0.2/32
MTU = 1280

Table = off
[Peer]
PublicKey = <redacted>
PresharedKey = <redacted>
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
hooks_present=0
dns_present=0
table_off_present=1

## activation
$ wg-quick up v7execwg0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.89.0.2/32 dev v7execwg0
[#] ip link set mtu 1280 up dev v7execwg0
activation_interface_present=true

## post_state
users_hash_after=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash_after=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
dns_hash_after=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
default_route_hash_after=4a75b4e867418b1a91218f8bcfc5127436d4662255c27c5f45eeb8e5965bb324
ip_rule_hash_after=5da4d16e6a4bf08ccded30b7050fdf4caddadeb2c3bb5bdbd0832bbd7a1f0a05
table_1009_hash_after=faa64ed459ed4ff6c2f427525116646eff7edfcad87712b10b4281cc795621ab
users_registry_changed=false
egress_registry_changed=false
dns_changed=false
default_route_changed=false
ip_rules_changed=false
table_1009_changed=false
$ ip link show v7execwg0
441: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
$ ip addr show v7execwg0
441: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.89.0.2/32 scope global v7execwg0
       valid_lft forever preferred_lft forever
$ wg show v7execwg0
interface: v7execwg0
  public key: Tx/LUxab6MMcgUiENrSeGe8kEpmIlLUngXroHzkuSRk=
  private key: (hidden)
  listening port: 38538

peer: NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=
  preshared key: (hidden)
  endpoint: 195.2.79.116:51889
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 148 B sent
  persistent keepalive: every 25 seconds
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
$ ip route show table 1009
default dev v7e356a192b79 scope link 
$ ip route get 8.8.8.8 from 10.7.0.11 iif wg0
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
$ grep -n 10.7.0.11 /opt/v7/egress/state/users.registry
13:ip=10.7.0.11 current=1 table=1009 enabled=1
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 1.1.1.1

## selected_moves_and_hidden_movers_after
$ find /opt/v7 -maxdepth 5 -iname *selected*move* -type f -printf %p %s bytes\\n
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1

## runtime_checkers_after
### v7-reconcile-check rc=0
===== V7 RECONCILE CHECK =====
2026-05-28T15:29:10+03:00
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
===== V7 USER ROUTE REALITY CHECK =====
2026-05-28T15:29:12+03:00

USER=10.0.0.2 TABLE=100 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.0.0.2 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.0.0.2 table=100 default dev awg3
route_get=8.8.8.8 from 10.0.0.2 dev awg3 table 100 
    cache iif wg0 
OK: user=10.0.0.2 route_get uses awg3

USER=10.0.0.3 TABLE=101 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.0.0.3 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.0.0.3 table=101 default dev awg3
route_get=8.8.8.8 from 10.0.0.3 dev awg3 table 101 
    cache iif wg0 
OK: user=10.0.0.3 route_get uses awg3

USER=10.0.0.6 TABLE=104 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.0.0.6 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.0.0.6 table=104 default dev awg3
route_get=8.8.8.8 from 10.0.0.6 dev awg3 table 104 
    cache iif wg0 
OK: user=10.0.0.6 route_get uses awg3

USER=10.7.0.3 TABLE=1001 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.3 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.3 table=1001 default dev awg3
route_get=8.8.8.8 from 10.7.0.3 dev awg3 table 1001 
    cache iif wg0 
OK: user=10.7.0.3 route_get uses awg3

USER=10.7.0.2 TABLE=1000 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.2 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.2 table=1000 default dev awg3
route_get=8.8.8.8 from 10.7.0.2 dev awg3 table 1000 
    cache iif wg0 
OK: user=10.7.0.2 route_get uses awg3

USER=10.7.0.4 TABLE=1002 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.4 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.4 table=1002 default dev awg3
route_get=8.8.8.8 from 10.7.0.4 dev awg3 table 1002 
    cache iif wg0 
OK: user=10.7.0.4 route_get uses awg3

USER=10.7.0.5 TABLE=1003 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.5 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.5 table=1003 default dev awg3
route_get=8.8.8.8 from 10.7.0.5 dev awg3 table 1003 
    cache iif wg0 
OK: user=10.7.0.5 route_get uses awg3

USER=10.7.0.6 TABLE=1004 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.6 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.6 table=1004 default dev awg3
route_get=8.8.8.8 from 10.7.0.6 dev awg3 table 1004 
    cache iif wg0 
OK: user=10.7.0.6 route_get uses awg3

USER=10.7.0.8 TABLE=1006 REGISTRY_EGRESS=awg3 ASSIGN_EGRESS=awg3 EXPECTED_DEV=awg3
OK: user=10.7.0.8 registry matches assignment
table_route=default dev awg3 scope link 
OK: user=10.7.0.8 table=1006 default dev awg3
route_get=8.8.8.8 from 10.7.0.8 dev awg3 table 1006 
    cache iif wg0 
OK: user=10.7.0.8 route_get uses awg3

USER=10.7.0.9 TABLE=1007 REGISTRY_EGRESS=awg0 ASSIGN_EGRESS=awg0 EXPECTED_DEV=awg0
OK: user=10.7.0.9 registry matches assignment
table_route=default dev awg0 scope link 
OK: user=10.7.0.9 table=1007 default dev awg0
route_get=8.8.8.8 from 10.7.0.9 dev awg0 table 1007 
    cache iif wg0 
OK: user=10.7.0.9 route_get uses awg0

USER=10.7.0.10 TABLE=1008 REGISTRY_EGRESS=awg0 ASSIGN_EGRESS=awg0 EXPECTED_DEV=awg0
OK: user=10.7.0.10 registry matches assignment
table_route=default dev awg0 scope link 
OK: user=10.7.0.10 table=1008 default dev awg0
route_get=8.8.8.8 from 10.7.0.10 dev awg0 table 1008 
    cache iif wg0 
OK: user=10.7.0.10 route_get uses awg0

USER=10.7.0.11 TABLE=1009 REGISTRY_EGRESS=1 ASSIGN_EGRESS=1 EXPECTED_DEV=v7e356a192b79
OK: user=10.7.0.11 registry matches assignment
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
===== V7 KILL SWITCH CHECK =====
2026-05-28T15:29:13+03:00
vpn_subnets=10.0.0.0/24,10.7.0.0/22
public_if=ens3
egress_ifs=awg0 awg3 tun0 v7e06a394c478 v7e356a192b79 v7edb0c189291
table=present
client_source_set=present
client_source_subnet=10.0.0.0/24 present
reverse_route_subnet=10.0.0.0/24 present
client_source_subnet=10.7.0.0/22 present
reverse_route_subnet=10.7.0.0/22 present
direct_leak_drop_rule=present
direct_whitelist_rule=present
sysctl_net.ipv4.ip_forward = 1
direct_fwmark_rule=present
direct_fwmark_precedes_user_rules=OK
direct_route_table=present
direct_mark_rule=present
dns_capture_udp=present
dns_capture_tcp=present
nat_awg0=present
mss_clamp_awg0=present_nft
nat_awg3=present
mss_clamp_awg3=present_nft
nat_tun0=present
mss_clamp_tun0=present_nft
nat_v7e06a394c478=present
mss_clamp_v7e06a394c478=present_nft
nat_v7e356a192b79=present
mss_clamp_v7e356a192b79=present_nft
nat_v7edb0c189291=present
mss_clamp_v7edb0c189291=present_nft

===== USER ROUTE CHECK =====
user=10.0.0.2 table=100 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.0.0.2 dev awg3 table 100 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.0.0.2 route_get uses expected egress
user=10.0.0.3 table=101 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.0.0.3 dev awg3 table 101 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.0.0.3 route_get uses expected egress
user=10.0.0.6 table=104 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.0.0.6 dev awg3 table 104 
    cache iif wg0  table_default=default dev awg3 scope link 
OK: user=10.0.0.6 route_get uses expected egress
user=10.7.0.3 table=1001 current=awg3 expected_if=awg3 route=8.8.8.8 from 10.7.0.3 dev awg3 table 1001 
    cache iif wg0  table_default=default dev awg3 scope link 
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
===== V7 PROVISIONING RECONCILE CHECK =====
2026-05-28T15:29:13+03:00
registry=/opt/v7/egress/state/users.registry
vpn_subnets=10.0.0.0/24,10.7.0.0/22
public_if=ens3
egress_ifs=awg0 awg3 tun0 v7e06a394c478 v7e356a192b79 v7edb0c189291

===== SOURCE SET =====
client_source_set=present
client_source_subnet=10.0.0.0/24 present
reverse_route_subnet=10.0.0.0/24 present
client_source_subnet=10.7.0.0/22 present
reverse_route_subnet=10.7.0.0/22 present

===== NAT =====
nat_awg0=present_nft
mss_clamp_awg0=present_nft
nat_awg3=present_nft
mss_clamp_awg3=present_nft
nat_tun0=present_nft
mss_clamp_tun0=present_nft
nat_v7e06a394c478=present_nft
mss_clamp_v7e06a394c478=present_nft
nat_v7e356a192b79=present_nft
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

## abort_flags
abort_default_route_changed=false
abort_dns_changed=false
abort_user_table_changed=false
abort_runtime_checkers_failed=false
