# Pre-activation safety snapshot raw
generated_utc=2026-05-28T12:10:18Z
hostname=v3119922.hosted-by-vdsina.ru
pwd=/root

## target profile
666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1  /root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf

## registries
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry

## candidate row and routes
ip=10.7.0.11 current=1 table=1009 enabled=1
default dev v7e356a192b79 scope link 
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 

## default route and dns
default via 195.2.79.1 dev ens3 proto static onlink 
nameserver 8.8.8.8
nameserver 1.1.1.1

## interfaces
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP> 
ens3             UP             52:54:00:2f:9b:32 <BROADCAST,MULTICAST,UP,LOWER_UP> 
wg0              UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
tun0             UNKNOWN        <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> 
v7e356a192b79    UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
awg0             UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
awg3             UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
v7edb0c189291    UP             <POINTOPOINT,NOARP,UP,LOWER_UP> 
v7e06a394c478    UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
lo               UNKNOWN        127.0.0.1/8 ::1/128 
ens3             UP             195.2.79.116/24 fe80::5054:ff:fe2f:9b32/64 
wg0              UNKNOWN        10.0.0.1/24 
tun0             UNKNOWN        172.19.0.1/30 fe80::b629:dee6:fab5:9667/64 
v7e356a192b79    UNKNOWN        10.10.120.8/32 
awg0             UNKNOWN        10.8.1.10/32 
awg3             UNKNOWN        10.8.1.13/32 
v7edb0c189291    UP             10.0.70.4/24 fe80::5e1f:261b:be1a:a12f/64 
v7e06a394c478    UNKNOWN        10.8.0.17/24 

## route table conflicts

## egress registry
id=vless protocol=vless type=proxy interface=tun0 test=socks5://127.0.0.1:1080 enabled=1 expected_ip=77.110.103.131 config_path=/etc/sing-box/config.json
id=awg0 protocol=amneziawg type=interface interface=awg0 test=interface enabled=1 expected_ip=194.124.210.244 config_path=/etc/amnezia/amneziawg/awg0.conf role=GLOBAL_STABLE service_tags=telegram,google,youtube,global priority=60 weight=70 connect_timeout=12s
id=awg3 protocol=amneziawg type=interface interface=awg3 test=interface enabled=1 expected_ip=194.124.210.244 config_path=/etc/amnezia/amneziawg/awg3.conf role=GLOBAL_STABLE service_tags=telegram,google,youtube,global priority=70 weight=75 connect_timeout=12s
id=1 protocol=amneziawg type=interface interface=v7e356a192b79 test=interface enabled=1 config=/etc/amnezia/amneziawg/v7e356a192b79.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
id=openvpn-1779388847-d2ad7c protocol=openvpn type=interface interface=v7edb0c189291 test=interface enabled=1 config=/etc/v7/egress-openvpn/v7edb0c189291.ovpn role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance

## selected moves files

## hidden mover scan

## runtime checkers

### v7-reconcile-check
===== V7 RECONCILE CHECK =====
2026-05-28T15:10:18+03:00
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
exit=0

### v7-user-route-check
===== V7 USER ROUTE REALITY CHECK =====
2026-05-28T15:10:19+03:00

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
exit=0

### v7-killswitch-check
===== V7 KILL SWITCH CHECK =====
2026-05-28T15:10:21+03:00
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
exit=0

### v7-provisioning-reconcile-check
===== V7 PROVISIONING RECONCILE CHECK =====
2026-05-28T15:10:21+03:00
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
exit=0
