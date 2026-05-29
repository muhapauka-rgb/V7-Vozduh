# E25.8 Server-Side Peer Review

## Existing Dead Profile

Profile:

`/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`

Verdict:

`existing_candidate_reusable=false`

Reason:

- endpoint points to the VPS public IP itself;
- endpoint route is local via `lo`;
- UDP listener on the configured endpoint port was absent;
- WireGuard handshake stayed `0`;
- RX packets stayed `0`;
- bounded remediation in E25.7 continuation did not restore usability.

Repair was not performed because making that self-referential profile work would not produce a genuine external outbound execution egress. It would at best repair a local client-to-this-VPS test loop.

## Replacement Candidate Peer

Profile:

`/etc/wireguard/vps.conf`

Endpoint:

- external route through `ens3`;
- ICMP reachable;
- UDP probe to endpoint port reported success;
- tcpdump observed outbound UDP handshake traffic.

But:

- no inbound UDP reply was captured;
- WireGuard `latest-handshakes` remained `0`;
- RX packets remained `0`.

Verdict:

`server_side_peer_valid=false`

The most likely cause is stale/invalid server-side peer state or a server-side WireGuard configuration mismatch. This cannot be repaired safely from the current VPS because the remote endpoint is external.

## Raw Evidence

See:

- `target-local-activation-connectivity.raw.md`
- `replacement-remediation-and-removal.raw.md`
