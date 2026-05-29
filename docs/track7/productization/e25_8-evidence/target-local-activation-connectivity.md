# E25.8 Target-Local Activation Connectivity

## Activation Result

The V7-normalized wrapper activated safely.

- interface: `v7execwg0`
- raw profile executed: false
- default route changed: false
- DNS changed: false
- IP rules changed: false
- route table `1009` changed: false
- main route table changed during `/32` primary activation: false
- users registry changed: false
- egress registry changed: false
- selected moves: absent/zero
- hidden movers: absent
- runtime checkers: OK

## Connectivity Result

`handshake_successful=false`

`rx_packets_present=false`

`target_connectivity_usable=false`

Observed:

- endpoint external and reachable by ICMP;
- UDP endpoint probe reported reachable;
- tcpdump saw outbound WireGuard UDP packets;
- no inbound UDP reply was captured;
- `latest-handshakes=0`;
- RX remained `0`;
- ping and curl through `v7execwg0` timed out.

## Remediation Matrix

Tried bounded variants:

- `10.10.0.2/32`, MTU `1200`;
- `10.10.0.2/24`, MTU `1280`;
- `10.10.0.2/24`, MTU `1200`.

All variants failed the same way:

- no handshake;
- no RX;
- outbound probes timed out.

## Root Cause

`SERVER_SIDE_PEER_INVALID_OR_STALE`

The endpoint is externally reachable, but WireGuard peer negotiation does not complete. This points to remote peer/key/server-side mismatch rather than V7 normalization, local route policy, DNS, or MTU.

## Raw Evidence

See:

- `target-local-activation-connectivity.raw.md`
- `replacement-remediation-and-removal.raw.md`
