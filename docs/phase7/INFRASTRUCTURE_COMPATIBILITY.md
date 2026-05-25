# V7 Phase 7 Infrastructure Compatibility

## Purpose

V7 runtime assumptions must be explicit.

## Supported Foundation

Required families:

- Linux host with systemd;
- nftables;
- iproute2;
- Python 3;
- curl;
- SQLite runtime for identity;
- WireGuard tooling when WG is used;
- AmneziaWG tooling when AWG is used;
- OpenVPN when OpenVPN egress is used;
- sing-box when proxy transports are used.

## Compatibility Checks

Before upgrade or provisioning:

- kernel supports required nftables behavior;
- `ip rule` and route tables are available;
- systemd timers/services are available;
- required transport commands exist;
- managed directories are readable/writable as expected;
- backup and audit paths are writable.

## Unsupported Shortcut

Do not assume a host is compatible because one tunnel starts.

Compatibility means routing, kill switch, state, audit, backup, and reconciliation can all work.

