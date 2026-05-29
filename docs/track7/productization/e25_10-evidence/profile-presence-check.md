# E25.10 Profile Presence Check

## Result

`new_profile_found=true`

`profile_path=/Users/ponch/Downloads/amnezia_for_awg (1) (1).conf`

## Local Source

- size: `462B`
- SHA256: `d6029f2b6e4d33afd458d3b9a4bd18ad436c1b4de4a6ee78b4194213f8448ce8`
- protocol class: `amneziawg`

## Known-Dead Reuse Check

Known-dead hashes:

- E25.7 self endpoint profile: `666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1`
- E25.8 external dead peer profile: `dbc463e711667f2d8d6ed87f191f4b2c17bb5d2eada29e6f363bf6a28de3d3aa`

Provided profile hash does not match known-dead hashes.

`profile_reused_known_dead=false`

## Redacted Profile Shape

```ini
[Interface]
Address = 10.8.1.14/32
DNS = <redacted-dns> 1.0.0.1
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

[Peer]
PublicKey = <redacted>
PresharedKey = <redacted>
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = <redacted-endpoint>
PersistentKeepalive = 25
```

## Initial Safety Classification

- external endpoint: pending VPS route check
- server/inbound config: no, appears client/outbound
- route/nft hooks: absent in local redacted scan
- DNS side effect: present, must be removed during normalization
- full-tunnel semantics: present, must be normalized with `Table=off`

## Decision

Proceed to quarantine/offline safety analysis on VPS. Raw profile execution remains forbidden.
