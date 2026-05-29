# E25.8 Replacement Profile Requirements

Block: E25.8
Mode: replacement outbound profile acquisition and validation

## Hard Requirements

A replacement execution profile must satisfy all of the following before it can be activated as a dedicated execution target:

- true outbound/client profile;
- external endpoint, not equal to the VPS public IP and not routed as local;
- server-side peer exists and can complete a WireGuard handshake;
- RX packets are present after target-local probes;
- no `PostUp`, `PostDown`, `PreUp`, or `PreDown` route/firewall hooks;
- no nftables/iptables side effects;
- DNS side effects are removable;
- full-tunnel `AllowedIPs` is acceptable only when normalized with `Table=off`;
- no global route takeover;
- no user route table mutation;
- compatible with zero-user validation;
- compatible with execution-only metadata:
  - `role=EXECUTION_ONLY`
  - `manual_only=1`
  - `reserve_only=1`
  - `autoswitch_allowed=false`
  - `rebalance_allowed=false`
  - `production_assignment_allowed=false`

## Rejection Rules

Reject a profile if any of these are true:

- endpoint points to the same VPS;
- endpoint has no reachable server-side peer;
- handshake remains zero after bounded target-local remediation;
- RX remains zero after probes;
- profile requires raw startup to work;
- profile requires route/nft hooks;
- profile requires global default route takeover;
- profile is server/inbound style instead of outbound/client style;
- profile contains missing or incomplete endpoint/key material;
- profile cannot be redacted safely for evidence.

## Activation Rule

Only a V7-normalized wrapper may be activated:

- `Table=off`
- DNS removed
- hooks absent
- dedicated interface name
- no production user assignment
- no autoswitch apply
- no `v7-user-switch`

## Success Criteria

The block may declare a replacement target usable only if:

- `handshake_successful=true`
- `rx_packets_present=true`
- `target_connectivity_usable=true`
- `routing_mutation_for_users=false`
- `runtime_checkers_ok=true`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
