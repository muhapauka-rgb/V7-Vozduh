# V7 Provisioning Architecture

Date: 2026-05-06
Status: draft, based on current migrated VPS core

## Goal

V7 must grow from a manually operated production-like VPN aggregator into a system where users are added safely through an admin panel or API.

The existing orchestration-core is preserved. It remains the data-plane engine for:

- sticky assignment
- health-aware failover
- diagnostics
- benchmark/state pipeline
- per-user routing
- manual rebalance preview and execution

The next layer is a provisioning/control plane that creates users, generates WireGuard profiles, applies peers, syncs Linux routing, and records audit history.

## Key Lesson From Migration

Client traffic path is:

```text
iPhone -> wg0 -> per-user routing table -> egress interface -> Internet
```

For that to work, NAT is required not only on the public VPS interface, but also on V7 egress interfaces:

```text
10.0.0.0/24 -> awg2 MASQUERADE
10.0.0.0/24 -> tun0 MASQUERADE
```

This is now part of the V7 bootstrap invariant. It must not be treated as an incidental manual fix.

## Architecture Principle

Separate control plane and data plane.

Data plane:

- WireGuard inbound `wg0`
- sing-box/VLESS egress `tun0`
- AmneziaWG egress `awg2`
- Linux `ip rule`
- Linux routing tables
- V7 shell orchestration scripts
- local JSON API on `127.0.0.1:7077`

Control plane:

- backend API
- admin UI
- PostgreSQL source of truth
- user/device provisioning
- key/QR generation
- idempotent sync worker
- audit log
- reconciliation loop

## Source Of Truth

Future source of truth should be PostgreSQL, not hand-edited files.

The current files remain generated/runtime artifacts:

- `/etc/wireguard/wg0.conf`
- `/opt/v7/egress/state/users.registry`
- `/opt/v7/egress/state/user-*.assign`
- routing tables and `ip rule`
- live `wg set` peers

The control plane writes desired state to DB, then a sync worker reconciles Linux actual state.

## Minimal Data Model

### users

- `id`
- `display_name`
- `status`: active, disabled, deleted
- `created_at`
- `updated_at`

### devices

- `id`
- `user_id`
- `name`
- `type`: iphone, android, desktop, router
- `status`: active, disabled, revoked
- `created_at`
- `revoked_at`

### wireguard_peers

- `id`
- `device_id`
- `client_ip`
- `public_key`
- `private_key_encrypted` or one-time generated secret
- `preshared_key_encrypted`, optional
- `allowed_ips`
- `endpoint`
- `persistent_keepalive`
- `created_at`
- `rotated_at`

### routing_assignments

- `id`
- `client_ip`
- `routing_table`
- `current_egress`: vless, awg2
- `enabled`
- `last_switch_at`
- `fail_count`

### egresses

- `id`: vless, awg2
- `type`: proxy, interface
- `interface`
- `test_mode`
- `enabled`
- `expected_external_ip`

### audit_log

- `id`
- `actor`
- `action`
- `target_type`
- `target_id`
- `before_json`
- `after_json`
- `created_at`

## IPAM

The current `/24` is too small for a 500-user target if we want growth headroom.

Recommended next range:

```text
10.7.0.0/22
```

This gives 1022 usable addresses and leaves room for multiple devices per user later.

Short-term compatibility:

```text
10.0.0.0/24
```

Keep current users as-is:

```text
10.0.0.2 -> table 100
10.0.0.3 -> table 101
```

Before scaling, create a migration plan for a larger inbound subnet.

## Routing Tables

Current model:

```text
one client IP -> one routing table -> one default egress dev
```

This is simple and clear, but 500 users means 500 `ip rule` entries and 500 routing tables.

This can still work on Linux if managed carefully, but it must be generated and reconciled. No manual edits.

Future optimization options:

- fwmark-based policy routing
- nftables maps
- ipsets
- grouped routing by egress

Do not switch to those until the current model is automated and measured.

## Provisioning Flow

Create iPhone user/device:

1. Allocate `client_ip`.
2. Allocate `routing_table`.
3. Generate WireGuard keypair.
4. Insert DB records in one transaction.
5. Apply live peer:

```bash
wg set wg0 peer <client_public_key> allowed-ips <client_ip>/32
```

6. Generate persistent WireGuard config from DB.
7. Render client `.conf` and QR.
8. Add/update V7 user registry generated from DB.
9. Run:

```bash
v7-routing-sync
```

10. Verify:

```bash
wg show wg0
ip route get 8.8.8.8 from <client_ip> iif wg0
curl http://127.0.0.1:7077/health
```

## Idempotency Rules

Every sync operation must be safe to run repeatedly.

Required behavior:

- existing peer with same public key is not duplicated
- existing `ip rule` is replaced or deduplicated
- existing route table default is replaced atomically
- generated config is written via temp file plus rename
- secrets are never printed in normal logs
- failed apply leaves DB desired state intact and marks sync error

## Reconciliation Loop

A future worker should periodically compare:

Desired state:

- DB users/devices/assignments

Actual state:

- `wg show wg0`
- `/etc/wireguard/wg0.conf`
- `ip rule`
- `ip route show table N`
- `/opt/v7/egress/state/users.registry`

Then it applies only missing or drifted pieces.

## Safety Invariants

Must always hold:

- `net.ipv4.ip_forward=1`
- `wg0` is up
- `sing-box` is up and owns `tun0`
- `awg2` is up before assigning users to awg2
- NAT exists for client subnet to `awg2`
- NAT exists for client subnet to `tun0`
- V7 health loop does not run automatic rebalance
- `v7-users-rebalance` remains manual
- `v7-users-rebalance-dry-run` is read-only

## Current VPS Baseline

New VPS:

```text
IP: 195.2.79.116
public interface: ens3
inbound: wg0
vless egress: tun0
awg egress: awg2
```

Current working client:

```text
v7-iphone
client IP: 10.0.0.3
routing table: 101
current egress: awg2
```

Expected egress IPs:

```text
vless/tun0: 77.110.103.131
awg2: 94.241.139.241
```

## Near-Term Roadmap

Phase 1: make current manual flow reproducible.

- create `v7-user-create` CLI
- create `v7-user-disable` CLI
- create `v7-user-rotate-key` CLI
- create `v7-users-sync` reconciliation command
- generate QR/config into protected directory

Phase 2: introduce DB source of truth.

- PostgreSQL schema
- migration from current registries
- backend API
- audit log

Phase 3: admin panel.

- user list
- create user
- disable user
- show QR once
- regenerate QR
- show handshake/status
- show assigned egress
- show last switch/failover reason

Phase 4: scale hardening.

- larger WireGuard subnet
- load tests with hundreds of peers
- nftables/ipset evaluation
- metrics and alerting
- backup/restore runbooks

