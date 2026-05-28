# E25.6 Profile Acquisition Inventory

Generated from read-only VPS inventory at `2026-05-28T11:59:41Z` and targeted review at `2026-05-28T12:00:40Z`.

## Result

- `safe_candidate_found=true`
- `candidate_count=4 plausible profile files`
- `best_candidate=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`
- `best_candidate_protocol=wireguard`
- `best_candidate_hash=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1`
- `profile_activated=false`
- `no_profile_executed=true`

## Candidate Classes

| Candidate | Protocol | Classification | Decision |
| --- | --- | --- | --- |
| `/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf` | WireGuard | `SAFE_FOR_V7_NORMALIZATION` with raw full-tunnel semantics | Best candidate for next activation block after wrapper normalization. |
| `/root/v7-wg-client-test/v7-wg-client-test-v2-ipv6-mtu1200-10.89.0.2.conf` | WireGuard dual-stack | `SAFE_FOR_V7_NORMALIZATION` but broader IPv6 scope | Secondary candidate; defer until IPv6 policy is explicitly validated. |
| `/root/v7-awg-client-test/v7-awg-client-test-direct-10.88.0.2.conf` | AmneziaWG | `SAFE_FOR_V7_NORMALIZATION` but protocol adds AWG-specific fields | Tertiary candidate; use only if WireGuard candidate fails. |
| `/root/amnezia_for_awg_direct.conf` | AmneziaWG | `SAFE_FOR_V7_NORMALIZATION` but older/direct profile | Do not prefer for first movement. |
| `/etc/wireguard/vps.conf` | WireGuard | `UNSAFE_FULL_TUNNEL_RAW` | Rejected for raw start; not chosen because `/root/v7-wg-client-test` candidate is cleaner. |
| `/etc/wireguard/wg-client-test.conf` | WireGuard/server-test | `UNSAFE_SERVER_STYLE` | Rejected due route hooks/server-test style. |
| `/etc/amnezia/amneziawg/awg-client-test.conf` | AmneziaWG/server-test | `UNSAFE_SERVER_STYLE` | Rejected due route/nft hooks/server-test style. |
| OpenVPN drafts | OpenVPN | mixed `PASS`/`FAIL` but hook/DNS/script complexity | Not selected for first execution-only target. |

## Best Candidate Properties

- `private_key_present=true`
- `endpoint_present=true`
- `peer_public_key_present=true`
- `address_present=true`
- `allowedips_0_0_0_0=true`
- `table_off=false`
- `mtu_present=true`
- `route_hooks_present=false`
- `dns_side_effect=true`

The candidate is not safe to activate as raw `wg-quick` config because it is full-tunnel and has DNS behavior. It is safe to prepare for V7 normalization because it has no route/nft hooks and contains a complete client profile shape.

## Evidence

- Raw inventory: `profile-acquisition-inventory.raw.md`
- Targeted redacted review: `targeted-profile-review.raw.md`
- Redacted quarantine files: `quarantine/`

