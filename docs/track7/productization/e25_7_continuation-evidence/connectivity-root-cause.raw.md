# E25.7 continuation connectivity root-cause raw evidence
timestamp_utc=2026-05-28T12:30:12Z
hostname=v3119922.hosted-by-vdsina.ru

endpoint_redacted=<redacted-endpoint>
endpoint_port=51889
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7

## wg_initial
$ wg show v7execwg0
interface: v7execwg0
  public key: <redacted>
  private key: <redacted>
  listening port: 38538

peer: NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=
  preshared key: <redacted>
  endpoint: <redacted-endpoint>
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 1.73 KiB sent
  persistent keepalive: every 25 seconds
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	1776
$ ip addr show v7execwg0
441: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none 
    inet 10.89.0.2/32 scope global v7execwg0
       valid_lft forever preferred_lft forever
$ ip link show v7execwg0
441: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
$ ip -s link show v7execwg0
441: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1280 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
    RX:  bytes packets errors dropped  missed   mcast           
             0       0      0       0       0       0 
    TX:  bytes packets errors dropped carrier collsns           
          1776      12      0       0       0       0 

## endpoint_reachability_via_main
$ ip route get 195.2.79.116
local 195.2.79.116 dev lo table local src 195.2.79.116 uid 0 
    cache <local> 
$ ping -c 3 -W 2 195.2.79.116
PING 195.2.79.116 (195.2.79.116) 56(84) bytes of data.
64 bytes from 195.2.79.116: icmp_seq=1 ttl=64 time=0.083 ms
64 bytes from 195.2.79.116: icmp_seq=2 ttl=64 time=0.046 ms
64 bytes from 195.2.79.116: icmp_seq=3 ttl=64 time=0.040 ms

--- 195.2.79.116 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2054ms
rtt min/avg/max/mdev = 0.040/0.056/0.083/0.019 ms
$ nc -zvu -w 3 195.2.79.116 51889
exit=1

## target_local_route_behavior
$ ip route get 1.1.1.1 oif v7execwg0
1.1.1.1 dev v7execwg0 src 10.89.0.2 uid 0 
    cache 
$ ip route get 8.8.8.8 oif v7execwg0
8.8.8.8 dev v7execwg0 src 10.89.0.2 uid 0 
    cache 
$ ip route show dev v7execwg0
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
$ ip route show table all
default via 195.2.79.1 dev ens3 table 70 
default dev awg3 table 100 scope link 
default dev awg3 table 101 scope link 
default dev awg3 table 104 scope link 
default dev awg3 table 1000 scope link 
default dev awg3 table 1001 scope link 
default dev awg3 table 1002 scope link 
default dev awg3 table 1003 scope link 
default dev awg3 table 1004 scope link 
default dev awg3 table 1006 scope link 
default dev awg0 table 1007 scope link 
default dev awg0 table 1008 scope link 
default dev v7e356a192b79 table 1009 scope link 
default dev v7e356a192b79 table 1010 scope link 
default dev awg0 table 1011 scope link 
default dev v7e356a192b79 table 1012 scope link 
default dev v7e356a192b79 table 1013 scope link 
default via 195.2.79.1 dev ens3 proto static onlink 
10.0.0.0/24 dev wg0 proto kernel scope link src 10.0.0.1 
10.0.70.0/24 dev v7edb0c189291 proto kernel scope link src 10.0.70.4 
10.7.0.0/22 dev wg0 scope link 
10.8.0.0/24 dev v7e06a394c478 proto kernel scope link src 10.8.0.17 
172.19.0.0/30 dev tun0 proto kernel scope link src 172.19.0.1 
195.2.79.0/24 dev ens3 proto kernel scope link src 195.2.79.116 
local 10.0.0.1 dev wg0 table local proto kernel scope host src 10.0.0.1 
broadcast 10.0.0.255 dev wg0 table local proto kernel scope link src 10.0.0.1 
local 10.0.70.4 dev v7edb0c189291 table local proto kernel scope host src 10.0.70.4 
broadcast 10.0.70.255 dev v7edb0c189291 table local proto kernel scope link src 10.0.70.4 
local 10.8.0.17 dev v7e06a394c478 table local proto kernel scope host src 10.8.0.17 
broadcast 10.8.0.255 dev v7e06a394c478 table local proto kernel scope link src 10.8.0.17 
local 10.8.1.10 dev awg0 table local proto kernel scope host src 10.8.1.10 
local 10.8.1.13 dev awg3 table local proto kernel scope host src 10.8.1.13 
local 10.10.120.8 dev v7e356a192b79 table local proto kernel scope host src 10.10.120.8 
local 10.89.0.2 dev v7execwg0 table local proto kernel scope host src 10.89.0.2 
local 127.0.0.0/8 dev lo table local proto kernel scope host src 127.0.0.1 
local 127.0.0.1 dev lo table local proto kernel scope host src 127.0.0.1 
broadcast 127.255.255.255 dev lo table local proto kernel scope link src 127.0.0.1 
local 172.19.0.1 dev tun0 table local proto kernel scope host src 172.19.0.1 
broadcast 172.19.0.3 dev tun0 table local proto kernel scope link src 172.19.0.1 
local 195.2.79.116 dev ens3 table local proto kernel scope host src 195.2.79.116 
broadcast 195.2.79.255 dev ens3 table local proto kernel scope link src 195.2.79.116 
unreachable default dev lo table 189 metric 1 pref medium
fe80::/64 dev ens3 proto kernel metric 256 pref medium
fe80::/64 dev tun0 proto kernel metric 256 pref medium
fe80::/64 dev v7edb0c189291 proto kernel metric 256 pref medium
local ::1 dev lo table local proto kernel metric 0 pref medium
local fe80::5054:ff:fe2f:9b32 dev ens3 table local proto kernel metric 0 pref medium
local fe80::5e1f:261b:be1a:a12f dev v7edb0c189291 table local proto kernel metric 0 pref medium
local fe80::b629:dee6:fab5:9667 dev tun0 table local proto kernel metric 0 pref medium
multicast ff00::/8 dev ens3 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev wg0 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev tun0 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev v7e356a192b79 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev awg0 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev awg3 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev v7edb0c189291 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev v7e06a394c478 table local proto kernel metric 256 pref medium
multicast ff00::/8 dev v7execwg0 table local proto kernel metric 256 pref medium

## probe_ping_default_mtu
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	1776
$ ping -c 3 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2058ms

exit=1
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	1924
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0

## probe_ping_small_payload
$ ping -c 3 -W 3 -s 200 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 200(228) bytes of data.

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2047ms

exit=1
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	2072
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0

## probe_ping_mtu_payloads
### payload_size=1000
$ ping -c 2 -W 3 -s 1000 -M do -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 1000(1028) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1021ms

exit=1
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	2220
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
### payload_size=1180
$ ping -c 2 -W 3 -s 1180 -M do -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 1180(1208) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1024ms

exit=1
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	2368
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
### payload_size=1200
$ ping -c 2 -W 3 -s 1200 -M do -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 1200(1228) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1023ms

exit=1
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	2516
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0

## curl_probe_if_available
$ curl --interface v7execwg0 --max-time 8 -sS https://ifconfig.me
curl: (28) Connection timed out after 8002 milliseconds
exit=28
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	2664
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0

## firewall_relevant_readonly
### nft grep relevant
		oifname "ens3" counter packets 1746003 bytes 109982716 masquerade
		ip saddr 10.0.0.0/24 oifname "awg2" counter packets 21545 bytes 9095120 masquerade
		ip saddr 10.0.0.0/24 oifname "tun0" counter packets 49878 bytes 27849233 masquerade
		ip saddr 10.7.0.0/22 oifname "awg2" counter packets 925 bytes 55500 masquerade
		ip saddr 10.7.0.0/22 oifname "tun0" counter packets 205 bytes 13468 masquerade
		iifname "wg0" oifname "tun0" tcp flags & (syn | rst) == syn counter packets 29093 bytes 1856668 tcp option maxseg size set 1240
		iifname "wg0" oifname "awg2" tcp flags & (syn | rst) == syn counter packets 14091 bytes 871652 tcp option maxseg size set 1240
		iifname "wg0" oifname "ens3" tcp flags & (syn | rst) == syn counter packets 13845 bytes 885920 tcp option maxseg size set 1240
		ip saddr 10.0.0.2 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.2"
		ip daddr 10.0.0.2 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.2"
		ip saddr 10.0.0.3 counter packets 5142460 bytes 2513814156 comment "v7-user-up:10.0.0.3"
		ip daddr 10.0.0.3 counter packets 11813901 bytes 14217699835 comment "v7-user-down:10.0.0.3"
		ip saddr 10.0.0.6 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.6"
		ip daddr 10.0.0.6 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.6"
		ip saddr 10.7.0.3 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.3"
		ip daddr 10.7.0.3 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.3"
		ip saddr 10.7.0.4 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.4"
		ip daddr 10.7.0.4 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.4"
		ip saddr 10.7.0.5 counter packets 79468 bytes 10232365 comment "v7-user-up:10.7.0.5"
		ip daddr 10.7.0.5 counter packets 146818 bytes 213195589 comment "v7-user-down:10.7.0.5"
		ip saddr 10.7.0.6 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.6"
		ip daddr 10.7.0.6 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.6"
		ip saddr 10.0.0.7 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.7"
		ip daddr 10.0.0.7 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.7"
		ip saddr 10.0.0.8 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.8"
		ip daddr 10.0.0.8 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.8"
		ip saddr 10.0.0.9 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.9"
		ip daddr 10.0.0.9 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.9"
		ip saddr 10.0.0.10 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.10"
		ip daddr 10.0.0.10 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.10"
		ip saddr 10.0.0.11 counter packets 0 bytes 0 comment "v7-user-up:10.0.0.11"
		ip daddr 10.0.0.11 counter packets 0 bytes 0 comment "v7-user-down:10.0.0.11"
		ip saddr 10.7.0.7 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.7"
		ip daddr 10.7.0.7 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.7"
		ip saddr 10.7.0.2 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.2"
		ip daddr 10.7.0.2 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.2"
		ip saddr 10.7.0.8 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.8"
		ip daddr 10.7.0.8 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.8"
		ip saddr 10.7.0.9 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.9"
		ip daddr 10.7.0.9 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.9"
		ip saddr 10.7.0.10 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.10"
		ip daddr 10.7.0.10 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.10"
		ip saddr 10.7.0.11 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.11"
		ip daddr 10.7.0.11 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.11"
		ip saddr 10.7.0.12 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.12"
		ip daddr 10.7.0.12 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.12"
		ip saddr 10.7.0.13 counter packets 8389 bytes 1824103 comment "v7-user-up:10.7.0.13"
		ip daddr 10.7.0.13 counter packets 12919 bytes 5930038 comment "v7-user-down:10.7.0.13"
		ip saddr 10.7.0.14 counter packets 429209 bytes 27468410 comment "v7-user-up:10.7.0.14"
		ip daddr 10.7.0.14 counter packets 214389 bytes 1035344097 comment "v7-user-down:10.7.0.14"
		ip saddr 10.7.0.15 counter packets 0 bytes 0 comment "v7-user-up:10.7.0.15"
		ip daddr 10.7.0.15 counter packets 0 bytes 0 comment "v7-user-down:10.7.0.15"
		ip saddr @v7_client_src ip daddr @v7_direct_dst ip daddr != @v7_direct_exclude_dst meta mark set 0x00000077 counter packets 0 bytes 0 comment "V7 mark explicit direct whitelist"
		iifname "wg0" ip saddr @v7_client_src udp dport 53 counter packets 0 bytes 0 dnat ip to 10.0.0.1 comment "V7 capture client UDP DNS"
		iifname "wg0" ip saddr @v7_client_src tcp dport 53 counter packets 0 bytes 0 dnat ip to 10.0.0.1 comment "V7 capture client TCP DNS"
		ip saddr @v7_client_src oifname "awg0" counter packets 0 bytes 0 masquerade comment "V7 NAT users via awg0"
		ip saddr @v7_client_src oifname "awg3" counter packets 0 bytes 0 masquerade comment "V7 NAT users via awg3"
		ip saddr @v7_client_src oifname "tun0" counter packets 0 bytes 0 masquerade comment "V7 NAT users via tun0"
		ip saddr @v7_client_src oifname "v7e06a394c478" counter packets 0 bytes 0 masquerade comment "V7 NAT users via v7e06a394c478"
		ip saddr @v7_client_src oifname "v7e356a192b79" counter packets 0 bytes 0 masquerade comment "V7 NAT users via v7e356a192b79"
		ip saddr @v7_client_src oifname "v7edb0c189291" counter packets 0 bytes 0 masquerade comment "V7 NAT users via v7edb0c189291"
		ip saddr @v7_client_src oifname "awg0" tcp flags syn tcp option maxseg size set rt mtu counter packets 0 bytes 0 comment "V7 MSS clamp users via awg0"
		ip saddr @v7_client_src oifname "awg0" counter packets 0 bytes 0 accept comment "V7 allow users via awg0"
		ip saddr @v7_client_src oifname "awg3" tcp flags syn tcp option maxseg size set rt mtu counter packets 0 bytes 0 comment "V7 MSS clamp users via awg3"
		ip saddr @v7_client_src oifname "awg3" counter packets 0 bytes 0 accept comment "V7 allow users via awg3"
		ip saddr @v7_client_src oifname "tun0" tcp flags syn tcp option maxseg size set rt mtu counter packets 0 bytes 0 comment "V7 MSS clamp users via tun0"
		ip saddr @v7_client_src oifname "tun0" counter packets 0 bytes 0 accept comment "V7 allow users via tun0"
		ip saddr @v7_client_src oifname "v7e06a394c478" tcp flags syn tcp option maxseg size set rt mtu counter packets 0 bytes 0 comment "V7 MSS clamp users via v7e06a394c478"
		ip saddr @v7_client_src oifname "v7e06a394c478" counter packets 0 bytes 0 accept comment "V7 allow users via v7e06a394c478"
		ip saddr @v7_client_src oifname "v7e356a192b79" tcp flags syn tcp option maxseg size set rt mtu counter packets 0 bytes 0 comment "V7 MSS clamp users via v7e356a192b79"
		ip saddr @v7_client_src oifname "v7e356a192b79" counter packets 0 bytes 0 accept comment "V7 allow users via v7e356a192b79"
		ip saddr @v7_client_src oifname "v7edb0c189291" tcp flags syn tcp option maxseg size set rt mtu counter packets 0 bytes 0 comment "V7 MSS clamp users via v7edb0c189291"
		ip saddr @v7_client_src oifname "v7edb0c189291" counter packets 0 bytes 0 accept comment "V7 allow users via v7edb0c189291"
		ip saddr @v7_client_src oifname "ens3" ip daddr @v7_direct_dst ip daddr != @v7_direct_exclude_dst counter packets 0 bytes 0 accept comment "V7 allow explicit direct whitelist"
		ip saddr @v7_client_src oifname "ens3" counter packets 0 bytes 0 drop comment "V7 block direct leak to public interface"
### iptables filter relevant
### iptables nat relevant
-A POSTROUTING -o ens3 -j MASQUERADE
-A POSTROUTING -s 10.0.0.0/24 -o awg2 -j MASQUERADE
-A POSTROUTING -s 10.0.0.0/24 -o tun0 -j MASQUERADE
-A POSTROUTING -s 10.7.0.0/22 -o awg2 -j MASQUERADE
-A POSTROUTING -s 10.7.0.0/22 -o tun0 -j MASQUERADE

## tcpdump_endpoint_short_if_available
tcpdump: WARNING: any: That device doesn't support promiscuous mode
(Promiscuous mode not supported on the "any" device)
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
15:30:46.758356 lo    In  IP <redacted-endpoint-host>.38538 > <redacted-endpoint-host>.51889: UDP, length 148

1 packet captured
17 packets received by filter
0 packets dropped by kernel
### ping_during_tcpdump
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1028ms

$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	2812
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0

## runtime_safety_after_probes
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
$ grep -n 10.7.0.11 /opt/v7/egress/state/users.registry
13:ip=10.7.0.11 current=1 table=1009 enabled=1
$ ip route show table 1009
default dev v7e356a192b79 scope link 
$ ip route get 8.8.8.8 from 10.7.0.11 iif wg0
8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 
    cache iif wg0 
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1
v7-reconcile-check rc=0
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
