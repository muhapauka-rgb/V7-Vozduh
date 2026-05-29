# E25.7 continuation server peer and bounded remediation raw evidence
timestamp_utc=2026-05-28T12:32:11Z
hostname=v3119922.hosted-by-vdsina.ru
endpoint_host_is_local=true
endpoint_port=51889
endpoint_host_sha256=8f92c309b396ef8dec14611843cc453eb25cdec8c5749e10547f48c47045a8f7

## listener_and_wireguard_state
$ wg show all
interface: wg0
  public key: a9MNyFSM0anpyXlSo2DEn2Tt0NRhsIdGW3ncGO19ejo=
  private key: (hidden)
  listening port: 51820

peer: PTjnlK95nMK8nS8Iocucl1voY2RypMajqVCzkJP9jSo=
  endpoint: 178.176.73.117:24028
  allowed ips: 10.7.0.13/32
  latest handshake: 5 days, 20 hours, 6 minutes, 40 seconds ago
  transfer: 3.58 MiB received, 20.33 MiB sent

peer: leEcfiODElYb4zJ3DLPpn4tQObfnBiU4VYGJ3CueQGY=
  endpoint: 109.252.176.232:1108
  allowed ips: 10.7.0.14/32
  latest handshake: 5 days, 22 hours, 36 minutes, 51 seconds ago
  transfer: 57.64 MiB received, 1.54 GiB sent

peer: Ec0pY6QYlQVZSL0Tn3djy6t1mqTJw2EJDVCd+AKNzmQ=
  endpoint: 31.173.87.131:6589
  allowed ips: 10.0.0.3/32
  latest handshake: 7 days, 14 hours, 25 minutes, 45 seconds ago
  transfer: 3.78 GiB received, 22.66 GiB sent

peer: Oc9ECXADrmq1TuwK8SuQ7GHKMZqJ+8woxAfiQsqudmY=
  endpoint: 109.252.176.232:2357
  allowed ips: 10.0.0.2/32
  latest handshake: 21 days, 22 hours, 38 minutes, 33 seconds ago
  transfer: 77.86 KiB received, 1.23 KiB sent

peer: +SLwwhZrpGjlJFjG9jbxvyk2ecVaVFDC8ihfgkvZjVQ=
  allowed ips: 10.0.0.6/32

peer: W9q3F62RP7L8x+kgZDVjO2j8fEPKifXgmZjpMhtvMl0=
  allowed ips: 10.7.0.3/32

peer: YY4NbergrYyanEhD8UOc4NcDTap9X3y93msa5xz2Vmk=
  allowed ips: 10.7.0.2/32

peer: 4dvWrzIoUzwTeWOve4WfcVo477lDt3mCGSn45tH24xg=
  allowed ips: 10.7.0.4/32

peer: 4Iv3TqnTiVliapzX+alw/olS7mju8ojhEyvijNcE3wA=
  allowed ips: 10.7.0.5/32

peer: 3oVO7RkRQrmUZZ7o7+V8OSJO0RE4ObwwSruFL6oKuTI=
  allowed ips: 10.7.0.6/32

peer: iGlyKHlap8uQs+VZ0eGElvC5TnU+zRR+B+dJlaTJHWM=
  allowed ips: 10.7.0.8/32

peer: gStlgxSMk3PZQG+25MKJvDW+up1f39h6iOUvS30CiBQ=
  allowed ips: 10.7.0.9/32

peer: XUFA7GRkXXdWl7juuuznm3wAXQx9RuOLn4O2Kd6cCmM=
  allowed ips: 10.7.0.10/32

peer: rTDkqkpPvfVfTLvGYPP7WWdhEkB9c79b2LJSPT4Cc2g=
  allowed ips: 10.7.0.11/32

peer: P/GpQj9qVrKulh6gUX2Y+4BZKzrLr9pvlGSNxFsFQ34=
  allowed ips: 10.7.0.12/32

peer: M0nlK5PSBlwZtNRUWuBsnKKQUt9987RGA3dul6PNrgI=
  allowed ips: 10.7.0.15/32

interface: v7e06a394c478
  public key: 5JvoR9IwONdb9c5Sgz05XZrn4F9XISOwCYjuWYx2bno=
  private key: (hidden)
  listening port: 36540

peer: VdM0jVhWfgGV0PQwNm137orOY/51lDXg/sVwdcV+TSg=
  preshared key: (hidden)
  endpoint: 89.191.226.228:51820
  allowed ips: 0.0.0.0/0, ::/0
  latest handshake: 16 seconds ago
  transfer: 9.75 GiB received, 393.98 MiB sent

interface: v7execwg0
  public key: Tx/LUxab6MMcgUiENrSeGe8kEpmIlLUngXroHzkuSRk=
  private key: (hidden)
  listening port: 38538

peer: NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=
  preshared key: (hidden)
  endpoint: 195.2.79.116:51889
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 4.91 KiB sent
  persistent keepalive: every 25 seconds
$ wg show all listen-port
wg0	51820
v7e06a394c478	36540
v7execwg0	38538
$ ss -ulnp
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                                   
UNCONN 0      0          127.0.0.1:53         0.0.0.0:*    users:(("dnsmasq",pid=1060516,fd=7))     
UNCONN 0      0           10.0.0.1:53         0.0.0.0:*    users:(("dnsmasq",pid=1060516,fd=5))     
UNCONN 0      0         127.0.0.54:53         0.0.0.0:*    users:(("systemd-resolve",pid=753,fd=18))
UNCONN 0      0      127.0.0.53%lo:53         0.0.0.0:*    users:(("systemd-resolve",pid=753,fd=16))
UNCONN 0      0          127.0.0.1:323        0.0.0.0:*    users:(("chronyd",pid=1073,fd=4))        
UNCONN 0      0            0.0.0.0:33311      0.0.0.0:*                                             
UNCONN 0      0            0.0.0.0:51820      0.0.0.0:*                                             
UNCONN 0      0            0.0.0.0:39567      0.0.0.0:*    users:(("openvpn",pid=55732,fd=3))       
UNCONN 0      0            0.0.0.0:34292      0.0.0.0:*                                             
UNCONN 0      0            0.0.0.0:38538      0.0.0.0:*                                             
UNCONN 0      0            0.0.0.0:36540      0.0.0.0:*                                             
UNCONN 0      0            0.0.0.0:49099      0.0.0.0:*                                             
UNCONN 0      0              [::1]:53            [::]:*    users:(("dnsmasq",pid=1060516,fd=9))     
UNCONN 0      0              [::1]:323           [::]:*    users:(("chronyd",pid=1073,fd=5))        
UNCONN 0      0                  *:443              *:*    users:(("caddy",pid=2866106,fd=7))       
UNCONN 0      0               [::]:33311         [::]:*                                             
UNCONN 0      0               [::]:51820         [::]:*                                             
UNCONN 0      0               [::]:34292         [::]:*                                             
UNCONN 0      0               [::]:38538         [::]:*                                             
UNCONN 0      0               [::]:36540         [::]:*                                             
UNCONN 0      0               [::]:49099         [::]:*                                             
$ lsof -nP -iUDP:51889
exit=1
$ ip route get 195.2.79.116
local 195.2.79.116 dev lo table local src 195.2.79.116 uid 0 
    cache <local> 
		ip saddr @v7_client_src oifname "ens3" counter packets 0 bytes 0 drop comment "V7 block direct leak to public interface"

## candidate_profile_family_inventory
$ find /root/v7-wg-client-test -maxdepth 2 -type f -printf %p %s bytes\\n
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.png 1132 bytes\n/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf 343 bytes\n/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf 249 bytes\n/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.png 1258 bytes\n/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf 321 bytes\n### file=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1  /root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
Address = 10.89.0.2/32
DNS = 1.1.1.1
MTU = 1280
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
### file=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf
7df64e1dcf3adab44bc92d08e1f89256f48344e31045c6fb330619297be8dc3c  /root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf
Address = 10.89.0.2/32
DNS = 1.1.1.1
MTU = 1280
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
### file=/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf
45f742717428217c8e3d55a9ba020f6546a0db34770026043b55605456be9445  /root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf
Address = 10.89.0.2/32, fd89:89::2/128
DNS = 1.1.1.1
MTU = 1200
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25

## server_side_search_readonly
$ find /root /etc/wireguard /opt/v7 -maxdepth 5 -type f ( -iname *10.89* -o -iname *51889* -o -iname *v7exec* -o -iname *wg-client-test* ) -printf %p %s bytes\\n
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.png 1132 bytes\n/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf 343 bytes\n/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf 249 bytes\n/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.png 1258 bytes\n/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf 321 bytes\n/root/e25_7_v7execwg0.conf.removed.20260528T121350Z 319 bytes\n/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.conf 430 bytes\n/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.png 1523 bytes\n/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.redacted.conf 322 bytes\n/etc/wireguard/wg-client-test.conf 697 bytes\n/etc/wireguard/v7execwg0.conf 319 bytes\n$ grep -Rsl 10\.89\.0\.2\|51889\|v7execwg0 /root/v7-wg-client-test /etc/wireguard /opt/v7
/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.redacted.conf
/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
/etc/wireguard/wg-client-test.conf
/etc/wireguard/v7execwg0.conf
/opt/v7/events/telegram-sentinel-20260523.jsonl
/opt/v7/audit/audit.jsonl

## remediation_decision_precheck
Observation: endpoint routes locally to VPS public IP; current WireGuard latest handshake remains 0; no RX packets recorded.
Safe remediation candidates: keepalive, MTU variants, target-local routing are allowed, but no-handshake with local endpoint/listener absent is expected to remain blocked.

## bounded_remediation_keepalive_no_route_side_effect
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
$ wg-quick up v7execwg0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.89.0.2/32 dev v7execwg0
[#] ip link set mtu 1280 up dev v7execwg0
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	444
$ ping -c 2 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1028ms

exit=1
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	592

## bounded_remediation_mtu1200_no_route_side_effect
$ wg-quick down v7execwg0
[#] ip link delete dev v7execwg0
$ wg-quick up v7execwg0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.89.0.2/32 dev v7execwg0
[#] ip link set mtu 1200 up dev v7execwg0
$ ip link show v7execwg0
443: v7execwg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1200 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/none 
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	148
$ ping -c 2 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1003ms

exit=1
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	296

## bounded_remediation_target_local_table1250_probe_only
$ ip route replace default dev v7execwg0 table 1250
$ ip route show table 1250
default dev v7execwg0 scope link 
$ ip route get 1.1.1.1 from 10.89.0.2 table 1250
Error: inet prefix is expected rather than "table".
exit=1
$ ping -c 2 -W 3 -I v7execwg0 1.1.1.1
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1012ms

exit=1
$ wg show v7execwg0 latest-handshakes
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0
$ wg show v7execwg0 transfer
NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=	0	444
$ ip route flush table 1250
$ ip route show table 1250

## post_remediation_safety
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
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 1.1.1.1
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
