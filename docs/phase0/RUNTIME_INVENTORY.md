# V7 Phase 0 Runtime Inventory

Purpose: document runtime paths, state, services, interfaces, and assumptions discovered from the repository.

## Main Runtime Interfaces

- Public interface: `ens3` by default.
- VPN/user subnets: `10.0.0.0/24`, `10.7.0.0/22`.
- Inbound interface referenced by docs: `wg0`.
- Existing egress examples from docs: `tun0`, `awg2`.
- Direct/RU fwmark: `0x77`.
- Direct/RU routing table: `70`.
- Direct/RU rule preference: `50`.

## Main Runtime Directories

```text
/opt/v7/egress/state
/opt/v7/events
/opt/v7/audit
/opt/v7/admin
/opt/v7/ipam
/opt/v7/traffic
/etc/v7
/etc/v7/admin
/etc/v7/direct
/etc/v7/policy
/etc/v7/egress-drafts
/etc/v7/egress-runtime
/etc/v7/egress-openvpn
/etc/v7/inbound-runtime
/etc/wireguard
/etc/amnezia
/etc/amnezia/amneziawg
/etc/amneziawg
/etc/sing-box
/root/v7-clients
/root/v7-smart-clients
/root/v7-backups
```

## Main State Files

```text
/opt/v7/egress/state/users.registry
/opt/v7/egress/state/egress.registry
/opt/v7/egress/state/egress-flags.state
/opt/v7/egress/state/v7-state.json
/opt/v7/egress/state/egress-speed.json
/opt/v7/egress/state/service-matrix.json
/opt/v7/egress/state/telegram-sentinel.json
/opt/v7/egress/state/egress-quality-summary.json
/opt/v7/egress/state/egress-quality-ring.json
/opt/v7/egress/state/autoswitch-safety.json
/opt/v7/egress/state/client-reconnect-state.json
/opt/v7/egress/state/vless-activity.json
/opt/v7/egress/state/client-speed.json
/opt/v7/egress/state/client-agents.json
/opt/v7/egress/state/client-commands.json
/opt/v7/egress/state/client-speed-links.json
/opt/v7/egress/state/client-profile-preferences.json
/opt/v7/egress/state/profile-delivery-tokens.json
/opt/v7/egress/state/path-samples.json
/opt/v7/egress/state/path-benchmark.json
/opt/v7/egress/state/path-optimizer-advice.json
/etc/v7/policy.json
/etc/v7/org-egress-policy.json
/etc/v7/admin/auth.json
/etc/v7/admin/safe-mode.json
/opt/v7/admin/v7-identity.db
/opt/v7/traffic/traffic.sqlite
```

## systemd Inventory

```text
v7-users-autoswitch.service
v7-users-autoswitch.timer
v7-egress-quality-compact.service
v7-egress-quality-compact.timer
v7-telegram-sentinel.service
v7-telegram-sentinel.timer
v7-service-matrix-refresh.service
v7-service-matrix-refresh.timer
v7-egress-openvpn@.service
```

Timer behavior in repository:

- autoswitch: after boot 2 minutes, then every 20 seconds;
- Telegram sentinel: after boot 30 seconds, then every 4 seconds;
- quality compaction: after boot 3 minutes, then every 5 minutes;
- service matrix refresh: after boot 2 minutes, then every 15 minutes with randomized delay.

## Admin API Environment Variables

Key environment variables used by `admin/v7-admin-api` include:

- `V7_ADMIN_HOST`
- `V7_ADMIN_PORT`
- `V7_STATE_DIR`
- `V7_PUBLIC_IF`
- `V7_AUDIT_FILE`
- `V7_EVENT_DIR`
- `V7_BACKUP_DIR`
- `V7_ADMIN_AUTH_FILE`
- `V7_ADMIN_SAFE_MODE_FILE`
- `V7_MAINTENANCE_CONF`
- `V7_EGRESS_DRAFTS_DIR`
- `V7_EGRESS_DRAFT_TESTS_DIR`
- `V7_EGRESS_RUNTIME_DIR`
- `V7_WIREGUARD_DIR`
- `V7_AMNEZIAWG_DIR`
- `V7_OPENVPN_EGRESS_DIR`
- `V7_IDENTITY_DB_FILE`
- `V7_POLICY_FILE`
- `V7_ORG_EGRESS_POLICY_FILE`
- `V7_ROUTE_CLASSES_REG`
- `V7_CLIENT_ROOT`
- `V7_SMART_CLIENT_ROOT`
- `V7_SERVICE_MATRIX_FILE`
- `V7_PROFILE_PUBLIC_BASE_URL`
- `V7_CLIENT_SPEED_PUBLIC_BASE_URL`

## Runtime Assumptions

- Scripts expect Linux networking tools and systemd.
- State is file-based plus SQLite, not a single database.
- Many production commands are expected in `/usr/local/bin`.
- Admin API is designed to run close to the host runtime, with permission to read/write sensitive operational files.
- The repository is not a complete standalone production image; it depends on installed runtime commands and host configuration.

## Inventory Boundary

This inventory is static repository analysis. It does not prove current server state.

