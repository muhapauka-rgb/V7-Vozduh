# E25.9 Operator Profile Requirements

Block: E25.9
Mode: external execution profile acquisition

## Required Input

The operator/provider must provide one fresh external outbound profile.

Preferred protocol:

- WireGuard client/outbound config.

Required properties:

- endpoint must be external, not this VPS public IP;
- endpoint must not route as `local` through `lo`;
- remote peer must be active;
- server-side peer must include this client public key;
- endpoint UDP port must be reachable;
- profile should be freshly generated or freshly repaired;
- `AllowedIPs=0.0.0.0/0` is allowed only because V7 will normalize with `Table=off`;
- no required `PostUp`, `PostDown`, `PreUp`, or `PreDown` hooks;
- no provider-required local firewall scripts;
- no raw default route takeover required;
- DNS directives may exist only if they can be removed safely;
- profile must be usable through target-local probes before any user movement.

## Expected Delivery Locations

Accepted locations for operator-provided profiles:

- `/root/v7-execution-profile-import/`
- `/root/v7-execution-profile-upload/`
- `/root/v7-external-execution-profile/`
- `/opt/v7/operator-import/`
- `/opt/v7/egress/import/`
- `/tmp/v7-execution-profile-import/`
- workspace evidence directory if explicitly supplied by the operator.

## Required Validation

A profile is not accepted as ready until all are true:

- quarantined without execution;
- secrets redacted in evidence;
- endpoint is external;
- unsafe hooks absent or removed before activation;
- normalized wrapper created with `Table=off`;
- raw profile never executed;
- target-local activation does not change default route, DNS, user registry, egress registry, route table `1009`, or IP rules;
- WireGuard handshake succeeds;
- RX packets are present;
- ping/curl or equivalent target-local probe succeeds;
- runtime checkers remain OK;
- selected moves remain zero;
- hidden movers remain absent.

## No-Profile Rule

If no new profile is provided, the block must stop with:

`OPERATOR_INPUT_REQUIRED`

Known dead profiles from E25.7/E25.8 must not be reused unless the remote peer is repaired and proven by handshake/RX.
