# E27 Fresh Runtime Snapshot

date_utc=2026-05-28T21:24:52Z
hostname=v3119922.hosted-by-vdsina.ru
pwd=/root

## Registry Hashes
f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042  /opt/v7/egress/state/users.registry
43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380  /opt/v7/egress/state/egress.registry

## Enabled Users
ip=10.0.0.2 current=awg3 table=100 enabled=1
ip=10.0.0.3 current=awg3 table=101 enabled=1
ip=10.0.0.6 current=awg3 table=104 enabled=1
ip=10.7.0.2 current=awg3 table=1000 enabled=1
ip=10.7.0.3 current=awg3 table=1001 enabled=1
ip=10.7.0.4 current=awg3 table=1002 enabled=1
ip=10.7.0.5 current=awg3 table=1003 enabled=1
ip=10.7.0.6 current=awg3 table=1004 enabled=1
ip=10.7.0.8 current=awg3 table=1006 enabled=1
ip=10.7.0.9 current=awg0 table=1007 enabled=1
ip=10.7.0.10 current=awg0 table=1008 enabled=1
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1
ip=10.7.0.13 current=awg0 table=1011 enabled=1
ip=10.7.0.14 current=1 table=1012 enabled=1
ip=10.7.0.15 current=1 table=1013 enabled=1
ip=10.7.0.16 current=vless table=1014 enabled=1

## Users On Egress 1
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1
ip=10.7.0.14 current=1 table=1012 enabled=1
ip=10.7.0.15 current=1 table=1013 enabled=1

## Candidate User Rows
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1
ip=10.7.0.14 current=1 table=1012 enabled=1
ip=10.7.0.15 current=1 table=1013 enabled=1

## Execution Target Row
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU

## Target Users Count
0

## Users Per Egress
1 4
awg0 3
awg3 9
vless 2

## Route Tables For Candidate Pool
### 10.7.0.11 row=ip=10.7.0.11 current=1 table=1009 enabled=1
default dev v7e356a192b79 scope link 
1.1.1.1 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif lo 
### 10.7.0.12 row=ip=10.7.0.12 current=1 table=1010 enabled=1
default dev v7e356a192b79 scope link 
1.1.1.1 from 10.7.0.12 dev v7e356a192b79 table 1010 
    cache iif lo 
### 10.7.0.14 row=ip=10.7.0.14 current=1 table=1012 enabled=1
default dev v7e356a192b79 scope link 
1.1.1.1 from 10.7.0.14 dev v7e356a192b79 table 1012 
    cache iif lo 
### 10.7.0.15 row=ip=10.7.0.15 current=1 table=1013 enabled=1
default dev v7e356a192b79 scope link 
1.1.1.1 from 10.7.0.15 dev v7e356a192b79 table 1013 
    cache iif lo 

## Selected Moves
selected_moves_dir_absent
selected_moves_count=0

## Hidden Mover Scan

## Runtime Checkers
### v7-reconcile-check
===== V7 RECONCILE CHECK =====
2026-05-29T00:24:53+03:00
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
user=10.7.0.16 enabled=1 current=vless table=1014

===== RESULT =====
warnings=0
errors=0
V7_RECONCILE_RESULT=OK
exit_code=0
### v7-user-route-check
===== V7 USER ROUTE REALITY CHECK =====
2026-05-29T00:24:54+03:00

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

USER=10.7.0.16 TABLE=1014 REGISTRY_EGRESS=vless ASSIGN_EGRESS=vless EXPECTED_DEV=tun0
OK: user=10.7.0.16 registry matches assignment
table_route=default dev tun0 scope link 
OK: user=10.7.0.16 table=1014 default dev tun0
route_get=8.8.8.8 from 10.7.0.16 dev tun0 table 1014 
    cache iif wg0 
OK: user=10.7.0.16 route_get uses tun0

===== RESULT =====
V7_USER_ROUTE_CHECK=OK
exit_code=0
### v7-killswitch-check
===== V7 KILL SWITCH CHECK =====
2026-05-29T00:24:56+03:00
vpn_subnets=10.0.0.0/24,10.7.0.0/22
public_if=ens3
egress_ifs=awg0 awg3 tun0 v7e06a394c478 v7e356a192b79 v7edb0c189291 v7execwg0
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
nat_v7execwg0=present
mss_clamp_v7execwg0=present_nft

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
user=10.7.0.16 table=1014 current=vless expected_if=tun0 route=8.8.8.8 from 10.7.0.16 dev tun0 table 1014 
    cache iif wg0  table_default=default dev tun0 scope link 
OK: user=10.7.0.16 route_get uses expected egress

===== RESULT =====
V7_KILLSWITCH_CHECK=OK
exit_code=0
### v7-provisioning-reconcile-check
===== V7 PROVISIONING RECONCILE CHECK =====
2026-05-29T00:24:57+03:00
registry=/opt/v7/egress/state/users.registry
vpn_subnets=10.0.0.0/24,10.7.0.0/22
public_if=ens3
egress_ifs=awg0 awg3 tun0 v7e06a394c478 v7e356a192b79 v7edb0c189291 v7execwg0

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
nat_v7execwg0=present_nft
mss_clamp_v7execwg0=present_nft

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
user=10.7.0.16 table=1014 current=vless expected_if=tun0 wg_peer=present route=ok table_default=ok detail=8.8.8.8 from 10.7.0.16 dev tun0 table 1014 
    cache iif wg0  table_detail=default dev tun0 scope link 

===== RESULT =====
V7_PROVISIONING_RECONCILE_CHECK=OK
exit_code=0

## Readiness Helper Explicit Target
V7 second canary target readiness (read-only)
runtime_commands_executed=False
candidate_user=10.7.0.11
candidate_still_valid=True
current_egress=1
execution_only_mode=True
execution_target_id=amneziawg-exec-20260528-10-8-1-14
selected_target=amneziawg-exec-20260528-10-8-1-14
approval_status=GO
second_canary_readiness=GO
target_1_current_user=['10.7.0.11', '10.7.0.12', '10.7.0.14', '10.7.0.15']
zero_user_targets=openvpn-1779388847-d2ad7c,wireguard-1779454504-c43409,amneziawg-exec-20260528-10-8-1-14
target_candidates:
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=48.044; min=34.235; stability=0.6855; reason=interface state unknown; occupied by registry users: 10.7.0.16; load-state users=2; diagnose SUSPECT; missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=48.932; min=13.396; stability=0.2784; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; stability below floor (0.2784); missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=65.723; min=39.759; stability=0.5806; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=25.429; min=15.308; stability=0.5085; reason=interface state unknown; diagnose SUSPECT
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=23.954; min=11.609; stability=0.46; reason=ready
  - amneziawg-exec-20260528-10-8-1-14: GO; zero_user=True; diagnose=OK; avg=27.12; min=10.67; stability=1.0; reason=ready
should_E9_3_execute_now=False
execution_allowed_now=False
exit_code=0

## Target Quality Artifacts
/opt/v7/egress/state/e25_11-backups/egress-diagnose.state.20260528T144951Z
/opt/v7/egress/state/e25_11-backups/egress-load.state.20260528T144951Z
/opt/v7/egress/state/egress-diagnose.state
/opt/v7/egress/state/egress-load-summary.json
/opt/v7/egress/state/egress-load.state
/opt/v7/egress/state/egress-quality-ring.json
/opt/v7/egress/state/egress-quality-summary.json
