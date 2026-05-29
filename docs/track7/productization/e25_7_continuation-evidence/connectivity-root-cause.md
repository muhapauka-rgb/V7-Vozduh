# E25.7 Continuation Connectivity Root Cause

## Classification

`STALE_SERVER_PEER_OR_DEAD_PROFILE`

The current WireGuard execution profile is not usable as an outbound execution target in the current VPS runtime.

## Evidence

- The profile endpoint resolves to the VPS public IP itself.
- `ip route get <endpoint>` returned local routing through `lo`, not an external peer path.
- WireGuard interface `v7execwg0` came up successfully.
- `latest-handshakes` stayed `0`.
- RX stayed `0 B`.
- TX increased during ping/curl probes.
- Ping through `v7execwg0` failed at default and small payload sizes.
- MTU-sized probes failed the same way.
- `curl --interface v7execwg0` timed out.
- `ss -ulnp` and `lsof -iUDP:51889` showed no active listener on the profile endpoint port.
- Existing WireGuard listening ports did not include `51889`.

## Why This Is Not Primarily MTU

MTU mismatch usually requires an established peer path or at least handshake evidence. Here:

- no handshake occurred;
- RX remained zero;
- small payload pings failed;
- MTU `1200` remediation also failed.

## Why This Is Not Governance Failure

The V7-normalized activation boundary held:

- `Table=off` prevented global route takeover;
- DNS did not change;
- user route table `1009` did not change;
- no selected moves appeared;
- runtime checkers remained OK.

## Raw Evidence

See:

- `connectivity-root-cause.raw.md`
- `server-peer-and-remediation.raw.md`
