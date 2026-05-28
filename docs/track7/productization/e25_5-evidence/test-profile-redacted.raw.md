--- /etc/wireguard/wg-client-test.conf
[Interface]
PrivateKey = <redacted>
Address = 10.89.0.1/24
ListenPort = 51889
MTU = 1200
PostUp = sysctl -w net.ipv4.ip_forward=1; ip -4 rule add pref 189 from 10.89.0.0/24 lookup 189 2>/dev/null || true; ip -4 route replace 10.89.0.0/24 dev %i scope link table 189; ip -4 route replace default via 195.2.79.1 dev ens3 table 189
PreDown = ip -4 rule delete pref 189 2>/dev/null || true; ip -4 route flush table 189 2>/dev/null || true; nft delete table inet v7_wg_client_test 2>/dev/null || true

[Peer]
PublicKey = <redacted>
PresharedKey = <redacted>
AllowedIPs = 10.89.0.2/32, fd89:89::2/128
--- /etc/amnezia/amneziawg/awg-client-test.conf
[Interface]
Address = 10.88.0.1/24
ListenPort = 51888
PrivateKey = <redacted>
MTU = 1420
Jc = 6
Jmin = 10
Jmax = 50
S1 = 193
S2 = 157
H1 = 1191178254
H2 = 1732013724
H3 = 1828439483
H4 = 1855252243

PostUp = sysctl -w net.ipv4.ip_forward=1
PostUp = ip -4 rule add pref 188 from 10.88.0.0/24 lookup 188 2>/dev/null || true
PostUp = ip -4 route replace 10.88.0.0/24 dev %i scope link table 188
PostUp = ip -4 route replace default via 195.2.79.1 dev ens3 table 188
PostUp = nft delete table inet v7_awg_client_test 2>/dev/null || true
PostUp = nft -f /etc/v7/awg-client-test/nft-direct.nft
PostDown = ip -4 rule del pref 188 from 10.88.0.0/24 lookup 188 2>/dev/null || true
PostDown = ip -4 route flush table 188 2>/dev/null || true
PostDown = nft delete table inet v7_awg_client_test 2>/dev/null || true

[Peer]
# v7-awg-test-user 10.88.0.2
PublicKey = <redacted>
PresharedKey = <redacted>
AllowedIPs = 10.88.0.2/32
--- /etc/wireguard/vps.conf
[Interface]
PrivateKey = <redacted>
Address = 10.10.0.2/24

[Peer]
PublicKey = <redacted>
Endpoint = 77.110.103.131:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
