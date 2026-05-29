# E25.8 quarantine and safety analysis raw evidence
timestamp_utc=2026-05-28T12:42:24Z
hostname=v3119922.hosted-by-vdsina.ru

## best_candidate
path=/etc/wireguard/vps.conf
sha256=dbc463e711667f2d8d6ed87f191f4b2c17bb5d2eada29e6f363bf6a28de3d3aa
size=238
protocol=wireguard
endpoint_host_sha256=0fd7d1aeb7daa3a96765cba18ac0e87419408dbea3b5e84fd7593c841f99b962
endpoint_route_summary=<ip> via <ip> dev ens3 src <ip> uid 0 
endpoint_self_reference=false
hooks_present=0
dns_side_effect_present=0
full_tunnel_semantics=1
table_off_present=0
redacted_config:
[Interface]
PrivateKey = <redacted>
Address = 10.10.0.2/24

[Peer]
PublicKey = <redacted>
Endpoint = <redacted-endpoint>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

## unsafe_hook_scan

## runtime_safety_before_any_activation
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
$ pgrep -af v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply
exit=1
