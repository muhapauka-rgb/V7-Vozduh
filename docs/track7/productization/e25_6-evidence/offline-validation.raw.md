# Offline validation raw
generated_utc=2026-05-28T12:02:16Z
best_candidate=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf
exists=true
sha256=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1
wg_quick_strip_exit=1
wg-quick: The config file must be a valid interface name, followed by .conf

## interface conflicts

## route table/rule conflicts

## normalized wrapper preview redacted
[Interface]
PrivateKey = <REDACTED>
Address = 10.89.0.2/32
# DNS removed by V7 normalization: <REDACTED>
MTU = 1280
Table = off
# V7 execution-only wrapper: no PostUp/PostDown hooks; policy routing added only by approved user movement path

[Peer]
PublicKey = <REDACTED>
PresharedKey = <REDACTED>
Endpoint = <REDACTED_ENDPOINT>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

## runtime safety quick
bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c  /opt/v7/egress/state/users.registry
a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8  /opt/v7/egress/state/egress.registry
