# E25.8 replacement remediation and removal raw evidence
timestamp_utc=2026-05-28T12:45:31Z
hostname=v3119922.hosted-by-vdsina.ru
endpoint_host_sha256=0fd7d1aeb7daa3a96765cba18ac0e87419408dbea3b5e84fd7593c841f99b962
endpoint_port=51820

## endpoint_reachability_and_udp_trace
$ ip route get 77.110.103.131
77.110.103.131 via 195.2.79.1 dev ens3 src 195.2.79.116 uid 0 
    cache 
$ ping -c 3 -W 2 77.110.103.131
PING 77.110.103.131 (77.110.103.131) 56(84) bytes of data.
64 bytes from 77.110.103.131: icmp_seq=1 ttl=62 time=49.3 ms
64 bytes from 77.110.103.131: icmp_seq=2 ttl=62 time=49.3 ms
64 bytes from 77.110.103.131: icmp_seq=3 ttl=62 time=49.3 ms

--- 77.110.103.131 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 49.266/49.295/49.318/0.021 ms
$ nc -zvu -w 3 77.110.103.131 51820
Connection to 77.110.103.131 51820 port [udp/*] succeeded!
tcpdump: WARNING: any: That device doesn't support promiscuous mode
(Promiscuous mode not supported on the "any" device)
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
15:45:38.213552 ens3  Out IP 195.2.79.116.49293 > <redacted-endpoint-host>.51820: UDP, length 148

1 packet captured
1 packet received by filter
0 packets dropped by kernel
### ping_during_tcpdump
PING 1.1.1.1 (1.1.1.1) from 10.10.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1028ms


## remediation_matrix
### remediation_variant=mtu1200_32 addr=10.10.0.2/32 mtu=1200
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
[Interface]
PrivateKey = <redacted>
Address = 10.10.0.2/32

Table = off
MTU = 1200
[Peer]
PublicKey = <redacted>
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
$ wg-quick up v7execwg0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.10.0.2/32 dev v7execwg0
[#] ip link set mtu 1200 up dev v7execwg0
$ ip addr show v7execwg0
445: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.10.0.2/32 scope global v7execwg0
       valid_lft forever preferred_lft forever
$ ip route show table main
default via 195.2.79.1 dev ens3 proto static onlink 
10.0.0.0/24 dev wg0 proto kernel scope link src 10.0.0.1 
10.0.70.0/24 dev v7edb0c189291 proto kernel scope link src 10.0.70.4 
10.7.0.0/22 dev wg0 scope link 
10.8.0.0/24 dev v7e06a394c478 proto kernel scope link src 10.8.0.17 
172.19.0.0/30 dev tun0 proto kernel scope link src 172.19.0.1 
195.2.79.0/24 dev ens3 proto kernel scope link src 195.2.79.116 
### probe=mtu1200_32
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	296
$ ping -c 2 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.10.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1040ms

exit=1
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	444
### remediation_variant=addr24_mtu1280 addr=10.10.0.2/24 mtu=1280
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
[Interface]
PrivateKey = <redacted>
Address = 10.10.0.2/24

Table = off
MTU = 1280
[Peer]
PublicKey = <redacted>
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
$ wg-quick up v7execwg0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.10.0.2/24 dev v7execwg0
[#] ip link set mtu 1280 up dev v7execwg0
$ ip addr show v7execwg0
446: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.10.0.2/24 scope global v7execwg0
       valid_lft forever preferred_lft forever
$ ip route show table main
default via 195.2.79.1 dev ens3 proto static onlink 
10.0.0.0/24 dev wg0 proto kernel scope link src 10.0.0.1 
10.0.70.0/24 dev v7edb0c189291 proto kernel scope link src 10.0.70.4 
10.7.0.0/22 dev wg0 scope link 
10.8.0.0/24 dev v7e06a394c478 proto kernel scope link src 10.8.0.17 
10.10.0.0/24 dev v7execwg0 proto kernel scope link src 10.10.0.2 
172.19.0.0/30 dev tun0 proto kernel scope link src 172.19.0.1 
195.2.79.0/24 dev ens3 proto kernel scope link src 195.2.79.116 
### probe=addr24_mtu1280
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	296
$ ping -c 2 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.10.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1042ms

exit=1
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	444
### remediation_variant=addr24_mtu1200 addr=10.10.0.2/24 mtu=1200
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
[Interface]
PrivateKey = <redacted>
Address = 10.10.0.2/24

Table = off
MTU = 1200
[Peer]
PublicKey = <redacted>
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
$ wg-quick up v7execwg0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.10.0.2/24 dev v7execwg0
[#] ip link set mtu 1200 up dev v7execwg0
$ ip addr show v7execwg0
447: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.10.0.2/24 scope global v7execwg0
       valid_lft forever preferred_lft forever
$ ip route show table main
default via 195.2.79.1 dev ens3 proto static onlink 
10.0.0.0/24 dev wg0 proto kernel scope link src 10.0.0.1 
10.0.70.0/24 dev v7edb0c189291 proto kernel scope link src 10.0.70.4 
10.7.0.0/22 dev wg0 scope link 
10.8.0.0/24 dev v7e06a394c478 proto kernel scope link src 10.8.0.17 
10.10.0.0/24 dev v7execwg0 proto kernel scope link src 10.10.0.2 
172.19.0.0/30 dev tun0 proto kernel scope link src 172.19.0.1 
195.2.79.0/24 dev ens3 proto kernel scope link src 195.2.79.116 
### probe=addr24_mtu1200
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	296
$ ping -c 2 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.10.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1053ms

exit=1
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	444

## post_remediation_verdict
$ wg show v7execwg0 latest-handshakes
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0
$ wg show v7execwg0 transfer
LTV4R/fmawlYK70hQKV7q7S6J5XdesH0f4u8oodK3Ro=	0	444

## rollback_removal
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
active_config_archived=/root/e25_8_v7execwg0.conf.removed.20260528T124531Z
983c83f4d46797034e245c8b9d660669158d714b85ed800bb265a41f62a92cc7  /root/e25_8_v7execwg0.conf.removed.20260528T124531Z

## final_safety
$ ip link show v7execwg0
Device "v7execwg0" does not exist.
exit=1
$ test ! -e /etc/wireguard/v7execwg0.conf
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
$ grep -n 10.7.0.11 /opt/v7/egress/state/users.registry
13:ip=10.7.0.11 current=1 table=1009 enabled=1
$ ip route show table 1009
default dev v7e356a192b79 scope link 
$ ip route get 8.8.8.8 from 10.7.0.11 iif wg0
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
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
$ find /opt/v7 -maxdepth 5 -iname *selected*move* -type f -printf %p %s bytes\\n
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1
v7-reconcile-check rc=0
===== V7 RECONCILE CHECK =====
2026-05-28T15:46:25+03:00
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
v7-user-route-check rc=0
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
v7-killswitch-check rc=0
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
v7-provisioning-reconcile-check rc=0
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
