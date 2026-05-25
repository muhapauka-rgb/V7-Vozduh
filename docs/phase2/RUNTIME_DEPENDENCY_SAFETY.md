# V7 Phase 2 - Runtime Dependency Safety

## Purpose

Provisioning must fail closed when runtime dependencies are missing or broken.

Missing dependency means quarantine/blocker, not partial enable.

## Required Dependency Families

Core:

- `ip`;
- `nft`;
- `systemctl`;
- `curl`;
- `v7-audit-log`;
- `v7-killswitch-check`;
- `v7-provisioning-reconcile-check`.

WireGuard:

- `wg`;
- `wg-quick`.

AmneziaWG:

- `awg`;
- `awg-quick` or compatible runtime.

OpenVPN:

- `openvpn`;
- optional `v7-egress-openvpn@.service`.

Proxy/sing-box:

- `sing-box`.

## Dependency Failure Behavior

If required dependency is missing:

- preflight blocks;
- quarantine blocks;
- egress remains disabled;
- operator sees exact missing dependency;
- no runtime partial enable.

## Permission Checks

Provisioning must verify access to:

- draft dir;
- test dir;
- runtime profile dir;
- egress registry;
- egress flags;
- audit path;
- managed OpenVPN directory;
- WireGuard/AmneziaWG managed directories.

## Future Readiness

Drivers should expose dependency requirements declaratively so UI and CLI can show the same blockers.
