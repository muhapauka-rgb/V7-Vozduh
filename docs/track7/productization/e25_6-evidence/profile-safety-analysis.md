# E25.6 Profile Safety Analysis

## Best Candidate

- `path=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`
- `protocol=wireguard`
- `sha256=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1`
- `classification=SAFE_FOR_V7_NORMALIZATION`

## WireGuard Safety Checks

| Check | Result |
| --- | --- |
| Interface private key present | `true` |
| Interface address present | `true` |
| Peer public key present | `true` |
| Endpoint present | `true` |
| AllowedIPs full tunnel | `true` |
| DNS side effect | `true` |
| `Table=off` present | `false` |
| PostUp/PostDown hooks | `false` |
| PreUp/PreDown hooks | `false` |
| nft/iptables hooks | `false` |
| route hooks | `false` |
| raw activation safe | `false` |
| V7 normalization safe | `true` |

## Classification

`SAFE_FOR_V7_NORMALIZATION`

The profile is a real outbound-style WireGuard client candidate. It must not be started raw because `AllowedIPs=0.0.0.0/0`, DNS behavior, and missing `Table=off` could create global route/DNS side effects. It can be safely imported in the next block only after writing a normalized V7 wrapper that blocks wg-quick route management and leaves movement routing under V7 governance.

## Rejected Alternatives

- Dual-stack WireGuard candidate is valid but adds IPv6 scope; postpone for first movement.
- AWG candidates are plausible but add protocol-specific fields and tooling risk; keep as backup.
- Existing `/etc/wireguard/vps.conf` is too broad and not the cleanest candidate.
- Server/test profiles with hooks remain rejected.

