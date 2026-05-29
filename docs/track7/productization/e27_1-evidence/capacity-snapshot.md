# E27.1 Capacity Snapshot

date_utc=2026-05-28T21:36:05Z
hostname=v3119922.hosted-by-vdsina.ru
pwd=/root

## Registry Hashes
f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042  /opt/v7/egress/state/users.registry
43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380  /opt/v7/egress/state/egress.registry

## Target Metadata
id=amneziawg-exec-20260528-10-8-1-14 protocol=amneziawg type=interface interface=v7execwg0 test=interface enabled=1 config=/etc/amnezia/v7execwg0.conf role=EXECUTION_ONLY route_table=1250 priority=10 weight=1 soft_limit=1 hard_limit=1 manual_only=1 reserve_only=1 canary_reserved=true execution_reserved=true reservation_owner=operator_execution_governance autoswitch_allowed=false rebalance_allowed=false production_assignment_allowed=false service_tags=governance,execution exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU

## Candidate Rows
ip=10.7.0.11 current=1 table=1009 enabled=1
ip=10.7.0.12 current=1 table=1010 enabled=1

## Target Users Count
0

## Interface State
450: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
450: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.8.1.14/32 scope global v7execwg0
       valid_lft forever preferred_lft forever

## WireGuard/Amnezia State
interface: v7execwg0
  public key: JrtgiYy6JqK/YHdkqKFvHciclUf26Felg0t+0SJpsEE=
  private key: (hidden)
  listening port: 52668
  jc: 6
  jmin: 10
  jmax: 50
  s1: 27
  s2: 54
  h1: 1728986848
  h2: 206880873
  h3: 835680411
  h4: 47849916

peer: qYixieOopzFefThoPUnUNce9CG1YOCUuN2h8cDdbgWs=
  preshared key: (hidden)
  endpoint: 194.124.210.244:34403
  allowed ips: 0.0.0.0/0, ::/0
  latest handshake: 1 minute, 55 seconds ago
  transfer: 617.67 MiB received, 35.02 MiB sent
  persistent keepalive: every 25 seconds

## Target Route/DNS Side Effects
default via 195.2.79.1 dev ens3 proto static onlink 
default dev v7e356a192b79 scope link 
default dev v7e356a192b79 scope link 

## Selected Moves
selected_moves_dir_absent
selected_moves_count=0

## Hidden Mover Scan

## Runtime Checkers
### v7-reconcile-check
===== V7 RECONCILE CHECK =====
2026-05-29T00:36:06+03:00
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
2026-05-29T00:36:07+03:00

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
2026-05-29T00:36:08+03:00
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
2026-05-29T00:36:09+03:00
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

## Readiness Explicit Target
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
  - vless: NO-GO; zero_user=False; diagnose=SUSPECT; avg=49.721; min=38.45; stability=0.7512; reason=interface state unknown; occupied by registry users: 10.7.0.16; load-state users=2; diagnose SUSPECT; missing Direct/RU and Trusted RU sensitive exclusions
  - awg0: NO-GO; zero_user=False; diagnose=OK; avg=51.009; min=19.452; stability=0.3731; reason=occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13; load-state users=3; stability below floor (0.3731); missing Direct/RU and Trusted RU sensitive exclusions
  - awg3: NO-GO; zero_user=False; diagnose=OK; avg=69.256; min=48.968; stability=0.681; reason=occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8; load-state users=9; missing Direct/RU and Trusted RU sensitive exclusions
  - openvpn-1779388847-d2ad7c: NO-GO; zero_user=True; diagnose=SUSPECT; avg=18.086; min=10.608; stability=0.4511; reason=interface state unknown; diagnose SUSPECT
  - wireguard-1779454504-c43409: GO; zero_user=True; diagnose=OK; avg=29.703; min=18.347; stability=0.5599; reason=ready
  - amneziawg-exec-20260528-10-8-1-14: GO; zero_user=True; diagnose=OK; avg=27.12; min=10.67; stability=1.0; reason=ready
should_E9_3_execute_now=False
execution_allowed_now=False
exit_code=0

## Readiness JSON
{
  "approval_status": "GO",
  "candidate": {
    "candidate_still_valid": true,
    "current_egress": "1",
    "enabled": true,
    "expected_current_egress": "1",
    "reasons": [],
    "table": "1009",
    "user": "10.7.0.11"
  },
  "candidate_still_valid": true,
  "candidate_user": "10.7.0.11",
  "current_egress": "1",
  "execution_allowed_now": false,
  "execution_only_mode": true,
  "execution_target_id": "amneziawg-exec-20260528-10-8-1-14",
  "forbidden_commands_called": false,
  "mutation": false,
  "quality_floor": {
    "avg_mbps": 15.0,
    "min_mbps": 10.0,
    "stability": 0.45
  },
  "read_only": true,
  "rejected_targets": [
    {
      "egress_id": "vless",
      "reasons": [
        "interface state unknown",
        "occupied by registry users: 10.7.0.16",
        "load-state users=2",
        "diagnose SUSPECT",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ]
    },
    {
      "egress_id": "awg0",
      "reasons": [
        "occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13",
        "load-state users=3",
        "stability below floor (0.3731)",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ]
    },
    {
      "egress_id": "awg3",
      "reasons": [
        "occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8",
        "load-state users=9",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ]
    },
    {
      "egress_id": "openvpn-1779388847-d2ad7c",
      "reasons": [
        "interface state unknown",
        "diagnose SUSPECT"
      ]
    }
  ],
  "required_excluded_route_classes": [
    "DIRECT_RU",
    "TRUSTED_RU_SENSITIVE"
  ],
  "runtime_commands_executed": false,
  "schema_version": 1,
  "second_canary_readiness": "GO",
  "selected_target": "amneziawg-exec-20260528-10-8-1-14",
  "should_e9_3_execute_now": false,
  "state_dir": "/opt/v7/egress/state",
  "target_1_current_user": [
    "10.7.0.11",
    "10.7.0.12",
    "10.7.0.14",
    "10.7.0.15"
  ],
  "target_candidates": [
    {
      "autoswitch_allowed": false,
      "avg_mbps": 49.721,
      "diagnose_detail": "protocol=vless",
      "diagnose_status": "SUSPECT",
      "direct_ru_trusted_ru_risk": "unknown_or_sensitive",
      "egress_id": "vless",
      "enabled": true,
      "exclude_route_classes": [],
      "execution_only": false,
      "execution_target_allowed": false,
      "execution_target_requested": false,
      "interface": "tun0",
      "interface_up_lower_up": null,
      "load_status": "HARD_FULL",
      "manual_only": false,
      "min_mbps": 38.45,
      "production_assignment_allowed": false,
      "rebalance_allowed": false,
      "rejection_reasons": [
        "interface state unknown",
        "occupied by registry users: 10.7.0.16",
        "load-state users=2",
        "diagnose SUSPECT",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ],
      "reserve_only": false,
      "role": "",
      "safe_for_operator_execution": false,
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 49.721,
        "min_mbps": 38.45,
        "stability": 0.7512
      },
      "stability": 0.7512,
      "status": "NO-GO",
      "users_count_from_load_state": 2,
      "users_count_from_registry": 1,
      "warnings": [
        "load_status=HARD_FULL"
      ],
      "zero_user": false
    },
    {
      "autoswitch_allowed": false,
      "avg_mbps": 51.009,
      "diagnose_detail": "handshake_age_seconds=19",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "unknown_or_sensitive",
      "egress_id": "awg0",
      "enabled": true,
      "exclude_route_classes": [],
      "execution_only": false,
      "execution_target_allowed": false,
      "execution_target_requested": false,
      "interface": "awg0",
      "interface_up_lower_up": true,
      "load_status": "HARD_FULL",
      "manual_only": false,
      "min_mbps": 19.452,
      "production_assignment_allowed": false,
      "rebalance_allowed": false,
      "rejection_reasons": [
        "occupied by registry users: 10.7.0.9, 10.7.0.10, 10.7.0.13",
        "load-state users=3",
        "stability below floor (0.3731)",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ],
      "reserve_only": false,
      "role": "GLOBAL_STABLE",
      "safe_for_operator_execution": false,
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 51.009,
        "min_mbps": 19.452,
        "stability": 0.3731
      },
      "stability": 0.3731,
      "status": "NO-GO",
      "users_count_from_load_state": 3,
      "users_count_from_registry": 3,
      "warnings": [
        "load_status=HARD_FULL"
      ],
      "zero_user": false
    },
    {
      "autoswitch_allowed": false,
      "avg_mbps": 69.256,
      "diagnose_detail": "handshake_age_seconds=73",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "unknown_or_sensitive",
      "egress_id": "awg3",
      "enabled": true,
      "exclude_route_classes": [],
      "execution_only": false,
      "execution_target_allowed": false,
      "execution_target_requested": false,
      "interface": "awg3",
      "interface_up_lower_up": true,
      "load_status": "HARD_FULL",
      "manual_only": false,
      "min_mbps": 48.968,
      "production_assignment_allowed": false,
      "rebalance_allowed": false,
      "rejection_reasons": [
        "occupied by registry users: 10.0.0.2, 10.0.0.3, 10.0.0.6, 10.7.0.3, 10.7.0.2, 10.7.0.4, 10.7.0.5, 10.7.0.6, 10.7.0.8",
        "load-state users=9",
        "missing Direct/RU and Trusted RU sensitive exclusions"
      ],
      "reserve_only": false,
      "role": "GLOBAL_STABLE",
      "safe_for_operator_execution": false,
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 69.256,
        "min_mbps": 48.968,
        "stability": 0.681
      },
      "stability": 0.681,
      "status": "NO-GO",
      "users_count_from_load_state": 9,
      "users_count_from_registry": 9,
      "warnings": [
        "load_status=HARD_FULL"
      ],
      "zero_user": false
    },
    {
      "autoswitch_allowed": false,
      "avg_mbps": 18.086,
      "diagnose_detail": "protocol=openvpn",
      "diagnose_status": "SUSPECT",
      "direct_ru_trusted_ru_risk": "low_excluded",
      "egress_id": "openvpn-1779388847-d2ad7c",
      "enabled": true,
      "exclude_route_classes": [
        "DIRECT_RU",
        "TRUSTED_RU_SENSITIVE"
      ],
      "execution_only": false,
      "execution_target_allowed": false,
      "execution_target_requested": false,
      "interface": "v7edb0c189291",
      "interface_up_lower_up": null,
      "load_status": "OK",
      "manual_only": false,
      "min_mbps": 10.608,
      "production_assignment_allowed": false,
      "rebalance_allowed": false,
      "rejection_reasons": [
        "interface state unknown",
        "diagnose SUSPECT"
      ],
      "reserve_only": false,
      "role": "GLOBAL_FAST",
      "safe_for_operator_execution": false,
      "safe_for_second_canary": false,
      "score": {
        "avg_mbps": 18.086,
        "min_mbps": 10.608,
        "stability": 0.4511
      },
      "stability": 0.4511,
      "status": "NO-GO",
      "users_count_from_load_state": 0,
      "users_count_from_registry": 0,
      "warnings": [],
      "zero_user": true
    },
    {
      "autoswitch_allowed": false,
      "avg_mbps": 29.703,
      "diagnose_detail": "handshake_age_seconds=5",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "low_excluded",
      "egress_id": "wireguard-1779454504-c43409",
      "enabled": true,
      "exclude_route_classes": [
        "DIRECT_RU",
        "TRUSTED_RU_SENSITIVE"
      ],
      "execution_only": false,
      "execution_target_allowed": false,
      "execution_target_requested": false,
      "interface": "v7e06a394c478",
      "interface_up_lower_up": true,
      "load_status": "OK",
      "manual_only": false,
      "min_mbps": 18.347,
      "production_assignment_allowed": false,
      "rebalance_allowed": false,
      "rejection_reasons": [],
      "reserve_only": false,
      "role": "GLOBAL_FAST",
      "safe_for_operator_execution": true,
      "safe_for_second_canary": true,
      "score": {
        "avg_mbps": 29.703,
        "min_mbps": 18.347,
        "stability": 0.5599
      },
      "stability": 0.5599,
      "status": "GO",
      "users_count_from_load_state": 0,
      "users_count_from_registry": 0,
      "warnings": [],
      "zero_user": true
    },
    {
      "autoswitch_allowed": false,
      "avg_mbps": 27.12,
      "diagnose_detail": "handshake_age_seconds=107",
      "diagnose_status": "OK",
      "direct_ru_trusted_ru_risk": "low_excluded",
      "egress_id": "amneziawg-exec-20260528-10-8-1-14",
      "enabled": true,
      "exclude_route_classes": [
        "DIRECT_RU",
        "TRUSTED_RU_SENSITIVE"
      ],
      "execution_only": true,
      "execution_target_allowed": true,
      "execution_target_requested": true,
      "interface": "v7execwg0",
      "interface_up_lower_up": true,
      "load_status": "OK",
      "manual_only": true,
      "min_mbps": 10.67,
      "production_assignment_allowed": false,
      "rebalance_allowed": false,
      "rejection_reasons": [],
      "reserve_only": true,
      "role": "EXECUTION_ONLY",
      "safe_for_operator_execution": true,
      "safe_for_second_canary": true,
      "score": {
        "avg_mbps": 27.12,
        "min_mbps": 10.67,
        "stability": 1.0
      },
      "stability": 1.0,
      "status": "GO",
      "users_count_from_load_state": 0,
      "users_count_from_registry": 0,
      "warnings": [],
      "zero_user": true
    }
  ],
  "tool": "v7-second-canary-target-readiness",
  "zero_user_targets": [
    "openvpn-1779388847-d2ad7c",
    "wireguard-1779454504-c43409",
    "amneziawg-exec-20260528-10-8-1-14"
  ]
}

## State Quality Files
--- /opt/v7/egress/state/e25_11-backups/egress-diagnose.state.20260528T144951Z
-rw-r--r-- 1 root root 802 May 28 17:49 /opt/v7/egress/state/e25_11-backups/egress-diagnose.state.20260528T144951Z
updated=2026-05-28T14:49:41Z
vless_diagnose_reason=handshake_unsupported_for_protocol_vless
vless_diagnose_severity=SUSPECT
vless_diagnose_detail=protocol=vless
awg0_diagnose_reason=OK
awg0_diagnose_severity=OK
awg0_diagnose_detail=handshake_age_seconds=58
awg3_diagnose_reason=OK
awg3_diagnose_severity=OK
awg3_diagnose_detail=handshake_age_seconds=122
1_diagnose_reason=OK
1_diagnose_severity=OK
1_diagnose_detail=handshake_age_seconds=34
openvpn-1779388847-d2ad7c_diagnose_reason=handshake_unsupported_for_protocol_openvpn
openvpn-1779388847-d2ad7c_diagnose_severity=SUSPECT
openvpn-1779388847-d2ad7c_diagnose_detail=protocol=openvpn
wireguard-1779454504-c43409_diagnose_reason=OK
wireguard-1779454504-c43409_diagnose_severity=OK
wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=63
--- /opt/v7/egress/state/e25_11-backups/egress-load.state.20260528T144951Z
-rw-r--r-- 1 root root 644 May 28 17:49 /opt/v7/egress/state/e25_11-backups/egress-load.state.20260528T144951Z
updated=2026-05-28T17:49:40+03:00
vless_users=1
vless_soft_limit=1
vless_hard_limit=2
vless_load_status=SOFT_FULL
awg0_users=3
awg0_soft_limit=1
awg0_hard_limit=2
awg0_load_status=HARD_FULL
awg3_users=9
awg3_soft_limit=1
awg3_hard_limit=2
awg3_load_status=HARD_FULL
1_users=4
1_soft_limit=1
1_hard_limit=2
1_load_status=HARD_FULL
openvpn-1779388847-d2ad7c_users=0
openvpn-1779388847-d2ad7c_soft_limit=1
openvpn-1779388847-d2ad7c_hard_limit=2
openvpn-1779388847-d2ad7c_load_status=OK
wireguard-1779454504-c43409_users=0
wireguard-1779454504-c43409_soft_limit=1
wireguard-1779454504-c43409_hard_limit=2
wireguard-1779454504-c43409_load_status=OK
--- /opt/v7/egress/state/egress-diagnose.state
-rw-r--r-- 1 root root 984 May 29 00:35 /opt/v7/egress/state/egress-diagnose.state
updated=2026-05-28T21:35:56Z
vless_diagnose_reason=handshake_unsupported_for_protocol_vless
vless_diagnose_severity=SUSPECT
vless_diagnose_detail=protocol=vless
awg0_diagnose_reason=OK
awg0_diagnose_severity=OK
awg0_diagnose_detail=handshake_age_seconds=19
awg3_diagnose_reason=OK
awg3_diagnose_severity=OK
awg3_diagnose_detail=handshake_age_seconds=73
1_diagnose_reason=OK
1_diagnose_severity=OK
1_diagnose_detail=handshake_age_seconds=49
openvpn-1779388847-d2ad7c_diagnose_reason=handshake_unsupported_for_protocol_openvpn
openvpn-1779388847-d2ad7c_diagnose_severity=SUSPECT
openvpn-1779388847-d2ad7c_diagnose_detail=protocol=openvpn
wireguard-1779454504-c43409_diagnose_reason=OK
wireguard-1779454504-c43409_diagnose_severity=OK
wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=5
amneziawg-exec-20260528-10-8-1-14_diagnose_reason=OK
amneziawg-exec-20260528-10-8-1-14_diagnose_severity=OK
amneziawg-exec-20260528-10-8-1-14_diagnose_detail=handshake_age_seconds=107
--- /opt/v7/egress/state/egress-load-summary.json
-rw-r--r-- 1 root root 2242 May 29 00:35 /opt/v7/egress/state/egress-load-summary.json
{
  "schema_version": 1,
  "updated": "2026-05-28T21:35:57.913831+00:00",
  "source": "v7-users-autoswitch",
  "authority": "capacity_signal",
  "operator_status": "ok",
  "semantics": {
    "ok": "capacity within soft limits",
    "warm": "limited healthy pool, monitor before broad movement",
    "high": "one or more egress reached soft limit",
    "full": "one or more egress reached hard limit",
    "overloaded": "one or more egress reached failover hard limit"
  },
  "summary": {
    "mode": "dynamic",
    "active_users": 17,
    "total_channels": 7,
    "healthy_channels": 3,
    "reserve_only_channels": 0,
    "degraded_or_dead_channels": 4,
    "reserve_ratio": 0.15,
    "reserve_channels": 1,
    "working_channels": 2,
    "avg_load": 8.5,
    "soft_limit": 10,
    "hard_limit": 13,
    "failover_hard_limit": 17,
    "per_egress": {
      "1": {
        "users": 4,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      },
      "amneziawg-exec-20260528-10-8-1-14": {
        "users": 0,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      },
      "awg0": {
        "users": 3,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      },
      "awg3": {
        "users": 9,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      },
      "openvpn-1779388847-d2ad7c": {
        "users": 0,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      },
      "vless": {
        "users": 1,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      },
      "wireguard-1779454504-c43409": {
        "users": 0,
        "soft_limit": 10,
        "hard_limit": 13,
        "failover_hard_limit": 17,
        "capacity_users": 0,
        "status": "OK"
      }
    },
    "status": "ok"
  }
}
--- /opt/v7/egress/state/egress-load.state
-rw-r--r-- 1 root root 829 May 29 00:35 /opt/v7/egress/state/egress-load.state
updated=2026-05-29T00:35:56+03:00
vless_users=2
vless_soft_limit=1
vless_hard_limit=2
vless_load_status=HARD_FULL
awg0_users=3
awg0_soft_limit=1
awg0_hard_limit=2
awg0_load_status=HARD_FULL
awg3_users=9
awg3_soft_limit=1
awg3_hard_limit=2
awg3_load_status=HARD_FULL
1_users=4
1_soft_limit=1
1_hard_limit=2
1_load_status=HARD_FULL
openvpn-1779388847-d2ad7c_users=0
openvpn-1779388847-d2ad7c_soft_limit=1
openvpn-1779388847-d2ad7c_hard_limit=2
openvpn-1779388847-d2ad7c_load_status=OK
wireguard-1779454504-c43409_users=0
wireguard-1779454504-c43409_soft_limit=1
wireguard-1779454504-c43409_hard_limit=2
wireguard-1779454504-c43409_load_status=OK
amneziawg-exec-20260528-10-8-1-14_users=0
amneziawg-exec-20260528-10-8-1-14_soft_limit=1
amneziawg-exec-20260528-10-8-1-14_hard_limit=2
amneziawg-exec-20260528-10-8-1-14_load_status=OK
--- /opt/v7/egress/state/egress-quality-ring.json
-rw-r--r-- 1 root root 688721 May 29 00:34 /opt/v7/egress/state/egress-quality-ring.json
{
  "schema_version": 1,
  "updated": "2026-05-28T21:34:48.498039+00:00",
  "max_items": 2000,
  "items": [
    {
      "ts": "2026-05-27T18:49:23.519717+00:00",
      "egress": "vless",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 48.062,
      "min_mbps": 43.18,
      "p95_latency_ms": 1250.5,
      "fail_rate": 1.0,
      "stability": 0.8984,
      "users": "1",
      "health_code": "200",
      "severity": "SUSPECT"
    },
    {
      "ts": "2026-05-27T18:49:23.519717+00:00",
      "egress": "wireguard-1779454504-c43409",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 34.686,
      "min_mbps": 25.85,
      "p95_latency_ms": 1084.7,
      "fail_rate": 0.0714,
      "stability": 0.7453,
      "users": "0",
      "health_code": "200",
      "severity": "OK"
    },
    {
      "ts": "2026-05-27T18:54:24.441509+00:00",
      "egress": "1",
      "kind": "quality",
      "ok": true,
      "avg_mbps": 70.507,
      "min_mbps": 58.34,
      "p95_latency_ms": 1091.5,
      "fail_rate": 0.0,
      "stability": 0.8274,
      "users": "4",
      "health_code": "200",
      "severity": "OK"
    },
    {
      "ts": "2026-05-27T18:54:24.441509+00:00",
      "egress": "awg0",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 38.741,
      "min_mbps": 30.17,
      "p95_latency_ms": 1923.1,
      "fail_rate": 0.0714,
      "stability": 0.7788,
      "users": "3",
      "health_code": "200",
      "severity": "OK"
    },
    {
      "ts": "2026-05-27T18:54:24.441509+00:00",
      "egress": "awg3",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 25.393,
      "min_mbps": 13.3,
      "p95_latency_ms": 2370.9,
      "fail_rate": 0.0714,
      "stability": 0.5238,
      "users": "9",
      "health_code": "200",
      "severity": "OK"
    },
    {
      "ts": "2026-05-27T18:54:24.441509+00:00",
      "egress": "openvpn-1779388847-d2ad7c",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 64.662,
      "min_mbps": 58.19,
      "p95_latency_ms": 1033.5,
      "fail_rate": 1.0,
      "stability": 0.8999,
      "users": "0",
      "health_code": "200",
      "severity": "SUSPECT"
    },
    {
      "ts": "2026-05-27T18:54:24.441509+00:00",
      "egress": "vless",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 47.19,
      "min_mbps": 43.18,
      "p95_latency_ms": 1250.5,
      "fail_rate": 1.0,
      "stability": 0.915,
      "users": "1",
      "health_code": "200",
      "severity": "SUSPECT"
    },
    {
      "ts": "2026-05-27T18:54:24.441509+00:00",
      "egress": "wireguard-1779454504-c43409",
      "kind": "quality",
      "ok": false,
      "avg_mbps": 23.486,
      "min_mbps": 7.57,
      "p95_latency_ms": 1084.7,
      "fail_rate": 0.0714,
      "stability": 0.3223,
      "users": "0",
      "health_code": "200",
      "severity": "OK"
    },
    {
      "ts": "2026-05-27T18:59:25.449760+00:00",
      "egress": "1",
--- /opt/v7/egress/state/egress-quality-summary.json
-rw-r--r-- 1 root root 11665 May 29 00:34 /opt/v7/egress/state/egress-quality-summary.json
{
  "schema_version": 1,
  "updated": "2026-05-28T21:34:48.486593+00:00",
  "windows": [
    "5m",
    "1h",
    "24h",
    "7d"
  ],
  "items": {
    "awg2": {
      "windows": {
        "5m": {
          "samples": 546,
          "avg_mbps": 64.849,
          "min_mbps": 56.705,
          "p95_latency_ms": 693.4,
          "fail_rate": 0.4676,
          "stability": 0.8745,
          "updated": "2026-05-20T15:41:54.429412+00:00"
        },
        "1h": {
          "samples": 546,
          "avg_mbps": 64.712,
          "min_mbps": 57.193,
          "p95_latency_ms": 702.9,
          "fail_rate": 0.4778,
          "stability": 0.8846,
          "updated": "2026-05-20T15:41:54.429412+00:00"
        },
        "24h": {
          "samples": 546,
          "avg_mbps": 65.567,
          "min_mbps": 57.687,
          "p95_latency_ms": 727.4,
          "fail_rate": 0.4376,
          "stability": 0.8816,
          "updated": "2026-05-20T15:41:54.429412+00:00"
        },
        "7d": {
          "samples": 546,
          "avg_mbps": 68.055,
          "min_mbps": 59.683,
          "p95_latency_ms": 724.6,
          "fail_rate": 0.4031,
          "stability": 0.8781,
          "updated": "2026-05-20T15:41:54.429412+00:00"
        }
      },
      "score": {
        "current": 179.41,
        "trend": "improving",
        "penalty": 47.78,
        "updated": "2026-05-20T15:41:54.429412+00:00"
      }
    },
    "vless": {
      "windows": {
        "5m": {
          "samples": 2902,
          "avg_mbps": 52.262,
          "min_mbps": 44.277,
          "p95_latency_ms": 1094.7,
          "fail_rate": 0.9999,
          "stability": 0.8399,
          "updated": "2026-05-28T21:34:48.486593+00:00"
        },
        "1h": {
          "samples": 2902,
          "avg_mbps": 49.721,
          "min_mbps": 38.45,
          "p95_latency_ms": 1263.6,
          "fail_rate": 0.9998,
          "stability": 0.7512,
          "updated": "2026-05-28T21:34:48.486593+00:00"
        },
        "24h": {
          "samples": 2902,
          "avg_mbps": 46.032,
          "min_mbps": 32.435,
          "p95_latency_ms": 1746.1,
          "fail_rate": 0.9992,
          "stability": 0.6773,
          "updated": "2026-05-28T21:34:48.486593+00:00"
        },
        "7d": {
          "samples": 2902,
          "avg_mbps": 45.038,
          "min_mbps": 31.959,
          "p95_latency_ms": 1822.3,
          "fail_rate": 0.9959,
          "stability": 0.6793,
          "updated": "2026-05-28T21:34:48.486593+00:00"
        }
      },
      "score": {
        "current": 0.0,
        "trend": "new",
        "penalty": 99.98,
        "updated": "2026-05-28T21:34:48.486593+00:00"
      }
    },
    "awg0": {
      "windows": {
        "5m": {
          "samples": 2558,
          "avg_mbps": 53.555,
          "min_mbps": 25.425,
          "p95_latency_ms": 2158.2,
          "fail_rate": 0.1606,
          "stability": 0.4632,
          "updated": "2026-05-28T21:34:48.486593+00:00"
        },
        "1h": {
          "samples": 2558,
          "avg_mbps": 51.009,
          "min_mbps": 19.452,
          "p95_latency_ms": 2214.3,
          "fail_rate": 0.1637,
          "stability": 0.3731,
--- /opt/v7/egress/state/egress-stability.state
-rw-r--r-- 1 root root 148 May 28 21:00 /opt/v7/egress/state/egress-stability.state
amneziawg-exec-20260528-10-8-1-14_avg_mbps=27.12 amneziawg-exec-20260528-10-8-1-14_min_mbps=10.67 amneziawg-exec-20260528-10-8-1-14_stability=1.000
--- /opt/v7/egress/state/stability.state
-rw-r--r-- 1 root root 854 May 29 00:35 /opt/v7/egress/state/stability.state
vless_avg_mbps=53.0013
vless_min_mbps=49.85
vless_stability=0.940543
vless_samples=30
awg0_avg_mbps=58.9773
awg0_min_mbps=40.83
awg0_stability=0.6923
awg0_samples=30
awg3_avg_mbps=74.5827
awg3_min_mbps=67.23
awg3_stability=0.901415
awg3_samples=30
1_avg_mbps=70.659
1_min_mbps=59.34
1_stability=0.839808
1_samples=30
openvpn-1779388847-d2ad7c_avg_mbps=4.02167
openvpn-1779388847-d2ad7c_min_mbps=1.30
openvpn-1779388847-d2ad7c_stability=0.323249
openvpn-1779388847-d2ad7c_samples=30
wireguard-1779454504-c43409_avg_mbps=43.9693
wireguard-1779454504-c43409_min_mbps=40.58
wireguard-1779454504-c43409_stability=0.922917
wireguard-1779454504-c43409_samples=30
amneziawg-exec-20260528-10-8-1-14_avg_mbps=65.7833
amneziawg-exec-20260528-10-8-1-14_min_mbps=55.30
amneziawg-exec-20260528-10-8-1-14_stability=0.840639
amneziawg-exec-20260528-10-8-1-14_samples=30
