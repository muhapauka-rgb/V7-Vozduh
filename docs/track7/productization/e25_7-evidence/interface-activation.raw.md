# E25.7 normalized config creation and activation raw
generated_utc=2026-05-28T12:11:39Z
source_profile=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
source_hash=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1
destination=/etc/wireguard/v7execwg0.conf

## before side-effect baselines
users_hash_before=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash_before=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
default_route_before=default via 195.2.79.1 dev ens3 proto static onlink ;
resolv_hash_before=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
candidate_table_before=default dev v7e356a192b79 scope link ;
candidate_route_before=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif wg0 ;
normalized_config_written=true
normalized_hash=c838438d6a6d5f82d8137c6d1aaa0682ccf52446c7bc563168009e2873ee16ed
unsafe_directives_remaining=false
table_off_present=true

## redacted normalized preview
[Interface]
PrivateKey = <REDACTED>
Address = 10.89.0.2/32
MTU = 1280

Table = off
[Peer]
PublicKey = <REDACTED>
PresharedKey = <REDACTED>
Endpoint = <REDACTED_ENDPOINT>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

## activation
wg_quick_up_exit=0
[#] ip link add dev v7execwg0 type wireguard
[#] wg setconf v7execwg0 /dev/fd/63
[#] ip -4 address add 10.89.0.2/32 dev v7execwg0
[#] ip link set mtu 1280 up dev v7execwg0
profile_activated=true

## after side-effect checks
users_hash_after=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash_after=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
default_route_after=default via 195.2.79.1 dev ens3 proto static onlink ;
resolv_hash_after=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
candidate_table_after=default dev v7e356a192b79 scope link ;
candidate_route_after=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009 ;    cache iif wg0 ;

## interface state
v7execwg0        UNKNOWN        <POINTOPOINT,NOARP,UP,LOWER_UP> 
v7execwg0        UNKNOWN        10.89.0.2/32 
interface: v7execwg0
  public key: <REDACTED>
  private key: <REDACTED>
  listening port: 54073

peer: NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=
  preshared key: <REDACTED>
  endpoint: <REDACTED_ENDPOINT>
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 148 B sent
  persistent keepalive: every 25 seconds

## route/rule after

## hidden movers after
