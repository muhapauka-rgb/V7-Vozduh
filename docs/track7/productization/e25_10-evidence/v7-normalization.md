# E25.10 V7 Normalization

## Result

`normalized_config_written=true`

`normalized_interface=v7execwg0`

`raw_profile_not_executed=true`

`table_off_enforced=true`

`dns_side_effect_blocked=true`

`hooks_absent=true`

## Source And Destination

- source profile: `/root/v7-execution-profile-import/e25_10_operator_amnezia_for_awg.conf`
- normalized config: `/etc/amnezia/v7execwg0.conf`
- protocol: `amneziawg`
- normalized config mode: `600 root:root`
- normalized config SHA256: `8ca4f8d31b9e39cb7e3ff3a0d46ddb29226d6cd13163c48705dd6e232e439aa8`

## Normalization Rules Applied

- removed `DNS`
- removed/blocked `PreUp`, `PostUp`, `PreDown`, `PostDown`
- removed/blocked `SaveConfig`
- enforced `Table = off`
- set conservative `MTU = 1280`
- preserved AmneziaWG fields `Jc`, `Jmin`, `Jmax`, `S1`, `S2`, `H1`-`H4`, `I1`-`I5`
- preserved peer endpoint and cryptographic peer settings
- preserved `AllowedIPs = 0.0.0.0/0, ::/0` only as peer selector; route installation is blocked by `Table=off`

## Redacted Shape

```ini
[Interface]
Address = 10.8.1.14/32
PrivateKey = <redacted>
Jc = 6
Jmin = 10
Jmax = 50
S1 = 27
S2 = 54
H1 = 1728986848
H2 = 206880873
H3 = 835680411
H4 = 47849916
I1 =
I2 =
I3 =
I4 =
I5 =

Table = off
MTU = 1280
[Peer]
PublicKey = <redacted>
PresharedKey = <redacted>
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25
```

## Safety Check

- `DNS` present after normalization: `false`
- `Table=off` present after normalization: `true`
- hooks or `SaveConfig` present after normalization: `false`
- interface present before activation: `false`

## Decision

Proceed to target-local activation of the normalized wrapper only.
