# E25.11 Safe Execution Target Activation

## Result

`handshake_successful=true`

`rx_packets_present=true`

`target_connectivity_usable=true`

`global_route_side_effects_prevented=true`

`dns_side_effect_blocked=true`

`routing_mutation_for_users=false`

`raw_profile_executed=false`

## Activation

- checked_at_utc: `2026-05-28T14:48:53Z`
- interface: `v7execwg0`
- config: `/etc/amnezia/v7execwg0.conf`
- activation command: `awg-quick up /etc/amnezia/v7execwg0.conf`
- activation result: `up_rc=0`
- interface address: `10.8.1.14/32`
- MTU: `1280`

## Side-Effect Check

Before and after activation:

- default route: `default via 195.2.79.1 dev ens3 proto static onlink`
- user table `1009`: `default dev v7e356a192b79 scope link`
- DNS: unchanged; `v7execwg0` has no DNS servers assigned
- `users.registry` SHA256: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` SHA256 before metadata integration: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

No user routing mutation occurred.

## Connectivity

`awg show v7execwg0` after activation:

- latest handshake: `Now`
- transfer: `92 B received, 432 B sent`

Ping through the target:

- command: `ping -c 3 -W 3 -I v7execwg0 1.1.1.1`
- result: `3 packets transmitted, 3 received, 0% packet loss`
- RTT: `min/avg/max/mdev = 26.284/28.799/31.371/2.077 ms`

HTTP probe through the target:

- command: `curl --interface v7execwg0 -4 -L --max-time 12 https://speed.cloudflare.com/__down?bytes=1048576`
- HTTP code: `200`
- size: `1048576`
- speed_download: `2755255 B/s`
- estimated throughput: `22.04 Mbps`

`awg show v7execwg0` after probes:

- latest handshake: `3 seconds ago`
- transfer: `1.08 MiB received, 39.67 KiB sent`

Proceed to metadata and NAT/MSS integration.
