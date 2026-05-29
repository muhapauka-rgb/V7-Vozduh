# E25.8 Profile Source Search

## Result

`replacement_candidate_found=true`

`best_replacement_candidate=/etc/wireguard/vps.conf`

`best_candidate_protocol=wireguard`

The search found many WireGuard-like files, but most are not usable as a new dedicated execution profile:

- active production/runtime profiles;
- historical backups of the inbound `wg0` server profile;
- sanitized draft artifacts for already-known targets;
- the known failed self-referential `10.89.0.2` test profile;
- client/mobile JSON/YAML exports that are not direct server-side execution egress profiles.

## Best Candidate

`/etc/wireguard/vps.conf`

Why selected:

- protocol: WireGuard;
- endpoint present;
- endpoint is external, not self/local;
- route to endpoint goes through `ens3`, not `lo`;
- no route hooks;
- no nft/iptables hooks;
- no DNS side effect;
- full-tunnel `AllowedIPs=0.0.0.0/0`, but normalizable with `Table=off`.

Risk:

- raw config has no `Table=off`;
- raw startup is forbidden;
- server-side peer validity was unknown until activation test.

## Rejected/Non-Replacement Classes

- `wireguard-1779454504-c43409` / `v7e06a394c478`: known spiky target, not a replacement.
- `v7execwg0.conf.e25_7_*`: artifacts from the failed self-referential profile, not candidates.
- `wg0.conf*`: inbound server profile/backups, not outbound replacement egress.
- AWG/OpenVPN/VLESS runtime configs: either active production, protocol adapter mismatch, historical backup, or not zero-user dedicated execution replacement.

## Runtime Baseline

Before acquisition work:

- `v7execwg0` absent;
- `/etc/wireguard/v7execwg0.conf` absent;
- `10.7.0.11` remained on egress `1`;
- route table `1009` unchanged;
- selected moves absent;
- hidden movers absent.

## Raw Evidence

See `profile-source-search.raw.md`.
