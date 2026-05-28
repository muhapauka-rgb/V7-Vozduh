# E25.7 target-local connectivity raw
generated_utc=2026-05-28T12:12:59Z

## interface before probe
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
  transfer: 0 B received, 2.17 KiB sent
  persistent keepalive: every 25 seconds

## ping via interface
PING 1.1.1.1 (1.1.1.1) from 10.89.0.2 v7execwg0: 56(84) bytes of data.

--- 1.1.1.1 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2063ms

ping_exit=1

## interface after probe
interface: v7execwg0
  public key: <REDACTED>
  private key: <REDACTED>
  listening port: 54073

peer: NXMv55pfP+tbTdhA+RD+wb8ucW+/vobLNTaBEEAijBo=
  preshared key: <REDACTED>
  endpoint: <REDACTED_ENDPOINT>
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 2.31 KiB sent
  persistent keepalive: every 25 seconds

## route side effects after probe
default via 195.2.79.1 dev ens3 proto static onlink 
default dev v7e356a192b79 scope link 
resolv_hash=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7
users_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
