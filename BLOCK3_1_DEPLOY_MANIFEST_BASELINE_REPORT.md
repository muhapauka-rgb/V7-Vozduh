# V7 VOZDUH — BLOCK 3.1 REPORT
## Deploy Manifest & Runtime Baseline Snapshot

Date: 2026-05-23 Europe/Moscow  
Live VPS: `195.2.79.116`  
Mode: manifest/snapshot generation only  
No cleanup, no migration, no service restart, no datapath changes

--------------------------------------------------
## 1. Deploy Manifest Structure

Created live snapshot directory:

```text
/opt/v7/ops/deploy-baseline/20260523T122251Z
```

Files created:

```text
manifest.json
checksums.sha256
runtime-summary.md
unit-summary.json
contract-summary.json
snapshot-artifacts.sha256
```

Manifest schema:

```json
{
  "schema_version": 1,
  "generated_at": "...",
  "host": {},
  "snapshot_dir": "...",
  "runtime_roots": {},
  "executables": [],
  "executable_summary": {},
  "systemd_units": [],
  "configs": [],
  "state_contracts": [],
  "identity": {},
  "rollback_material": {},
  "verification": {},
  "observability_summary": {},
  "warnings": []
}
```

No sensitive DB rows, token values, or registry contents were copied into the report. The manifest stores metadata and hashes.

--------------------------------------------------
## 2. Active Executable Inventory

The manifest scanned:

```text
/usr/local/bin/v7*
```

Counts:

```text
total v7* files: 349
active runtime executables: 24
backup/stale executables in PATH: 207
suspicious executables in PATH: 1
unknown active-like executables not bound by systemd/shell-loop scan: 117
```

Active runtime executables detected from systemd explicit refs and shell-loop implicit refs:

```text
v7-admin-api
v7-api
v7-client-speed-api
v7-direct-auto-sync
v7-egress-benchmark-all
v7-egress-diagnose
v7-egress-history
v7-egress-load
v7-egress-quality-compact
v7-egress-stability
v7-killswitch-disable-temporary
v7-killswitch-enable
v7-mss-clamp-enable
v7-path-guard-repair
v7-path-sanity-check
v7-public-gateway
v7-routing-sync
v7-service-matrix-refresh-all
v7-state-json-save
v7-state-merge
v7-telegram-sentinel
v7-traffic-snapshot
v7-user-desired-state-save
v7-users-autoswitch
```

Each executable entry in `manifest.json` includes:

- name;
- path;
- classification;
- whether referenced by systemd/shell-loop scan;
- executable bit;
- size;
- mode;
- uid/gid;
- mtime;
- sha256.

--------------------------------------------------
## 3. Stale Executable Inventory

Detected:

```text
207 backup/stale v7 executables
```

Classification rule:

```text
backup, .bak, .old, .orig, .save, .copy, blockN, timestamp-like 20YYYY...
```

These files are still executable and still in `/usr/local/bin`, therefore still in PATH.

Examples:

```text
v7-admin-api.backup-nav-cache-20260520-182701
v7-admin-api.backup-routefix-20260520-103228
v7-admin-api.backup-telegram-sentinel-20260520
v7-admin-api.backup.balance-reconnect-20260522-170721
v7-admin-api.bak.20260508-114731
```

No stale executable was moved or chmodded in Block 3.1.

--------------------------------------------------
## 4. Systemd Dependency Map

`unit-summary.json` captures:

- V7 services;
- V7 timers;
- systemd templates;
- drop-ins;
- explicit `/usr/local/bin/v7*` references;
- implicit `v7-*` commands inside shell loops;
- `systemctl show` state for non-template units.

Captured systemd unit count:

```text
28
```

Important active bindings:

```text
v7-admin-api.service -> /usr/local/bin/v7-admin-api
v7-api.service -> /usr/local/bin/v7-api
v7-client-speed-api.service -> /usr/local/bin/v7-client-speed-api
v7-killswitch.service -> /usr/local/bin/v7-killswitch-enable
v7-routing-sync.service -> /usr/local/bin/v7-routing-sync
v7-users-autoswitch.service -> /usr/local/bin/v7-users-autoswitch --apply
v7-telegram-sentinel.service -> /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

Important implicit PATH dependencies:

```text
v7-health.service:
  v7-egress-history
  v7-egress-stability
  v7-egress-load
  v7-egress-diagnose
  v7-state-merge
  v7-user-desired-state-save
  v7-state-json-save
  v7-users-autoswitch

v7-benchmark.service:
  v7-egress-benchmark-all
```

### Dangerous PATH collision analysis

PATH risk remains high because:

- 207 executable backups are still in `/usr/local/bin`;
- 117 active-like executables are not bound by the current systemd/shell-loop scan;
- shell loops call tools by bare command names;
- backup filenames are unlikely to collide directly with active command names, but they remain executable and operator-visible.

--------------------------------------------------
## 5. Runtime Contract Snapshot

`contract-summary.json` captures metadata for:

```text
/opt/v7/egress/state/users.registry
/opt/v7/egress/state/egress.registry
/opt/v7/egress/state/autoswitch-safety.json
/opt/v7/egress/state/telegram-sentinel.json
/opt/v7/egress/state/egress-quality-summary.json
/opt/v7/egress/state/egress-load-summary.json
/opt/v7/egress/state/client-reconnect-state.json
/opt/v7/egress/state/v7-state.json
/opt/v7/egress/state/profile-delivery-tokens.json
```

Each contract snapshot includes:

- classification;
- role;
- rebuildability;
- metadata;
- sha256;
- top-level JSON keys where applicable;
- counts only where safe.

Sensitive content was not copied.

Runtime contract classifications:

| Contract | Classification | Rebuildability |
|---|---|---|
| `users.registry` | authoritative | not safely rebuildable |
| `egress.registry` | authoritative | not safely rebuildable |
| `autoswitch-safety.json` | runtime safety authority | technically rebuildable, but safety memory loss is dangerous |
| `telegram-sentinel.json` | advisory signal | rebuildable |
| `egress-quality-summary.json` | historical signal | rebuildable over time |
| `egress-load-summary.json` | capacity signal | rebuildable |
| `client-reconnect-state.json` | supporting signal | rebuildable over time |
| `v7-state.json` | generated aggregate | rebuildable from sources |
| `profile-delivery-tokens.json` | sensitive authority | not safely rebuildable |

--------------------------------------------------
## 6. Identity Runtime Snapshot

Canonical identity DB:

```text
/opt/v7/admin/v7-identity.db
```

Future/stale path:

```text
/opt/v7/identity/v7-identity.db
```

Snapshot result:

```text
canonical DB exists: yes
future/stale path exists: no
tables: 12
content copied: false
```

Tables captured by name and row counts only:

```text
access_settings
admin_table_settings
allowed_users
connect_sessions
devices
groups
identity_users
onboarding_attempts
organizations
pending_profiles
provisioning_jobs
user_metadata
```

No SQLite rows were copied into the snapshot.

--------------------------------------------------
## 7. Rollback Trust Classification

Rollback material is now classified in `manifest.json`.

### Trustworthy

```text
/etc/v7/*.backup*
```

These are explicit config backups with paths and timestamps.

### Weak

```text
/usr/local/bin/v7*.backup*
/usr/local/bin/v7*.bak*
```

These are useful historical artifacts but weak rollback material because they were executable in PATH and had no manifest lineage before Block 3.1.

### Unknown

```text
active-like /usr/local/bin/v7* not referenced by systemd or shell-loop scan
```

There are 117 unknown active-like executables. Some may be valid operator tools, but they are not proven runtime-bound by this snapshot.

--------------------------------------------------
## 8. Dangerous PATH Clutter Analysis

Warnings recorded in `manifest.json`:

```text
no git checkout/release baseline found on VPS
207 backup/stale v7 executables are executable and still in /usr/local/bin PATH
1 suspicious v7 executables found in /usr/local/bin
117 active-like v7 executables are not referenced by systemd/shell-loop scan
/opt/v7/identity/v7-identity.db missing; current canonical identity DB is /opt/v7/admin/v7-identity.db
profile-delivery-tokens.json is readable beyond owner; review permissions before commercial production
```

Suspicious executable:

```text
v7-admin-api.tmp
```

This should not be removed blindly, but it should be inspected before cleanup.

--------------------------------------------------
## 9. Exact Files Created

On VPS:

```text
/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json
/opt/v7/ops/deploy-baseline/20260523T122251Z/checksums.sha256
/opt/v7/ops/deploy-baseline/20260523T122251Z/runtime-summary.md
/opt/v7/ops/deploy-baseline/20260523T122251Z/unit-summary.json
/opt/v7/ops/deploy-baseline/20260523T122251Z/contract-summary.json
/opt/v7/ops/deploy-baseline/20260523T122251Z/snapshot-artifacts.sha256
```

File sizes:

```text
manifest.json: 307K
checksums.sha256: 42K
unit-summary.json: 46K
contract-summary.json: 9.5K
runtime-summary.md: 1.1K
snapshot-artifacts.sha256: 420B
```

No runtime files were moved, deleted, chmodded, symlinked, or overwritten.

--------------------------------------------------
## 10. Verification Results

Manifest readability:

```text
manifest_schema: 1
executables: 349
units: 28
contracts: 9
warnings: 6
identity_tables: 12
```

Snapshot artifact checksum verification:

```text
checksums.sha256: OK
contract-summary.json: OK
manifest.json: OK
runtime-summary.md: OK
unit-summary.json: OK
```

Runtime checks after snapshot:

```text
v7-killswitch-check: OK
v7-user-route-check: OK
v7-provisioning-reconcile-check: OK
systemctl --failed: 0 loaded units listed
```

No datapath regression was observed.

--------------------------------------------------
## 11. Remaining Operational Risks

### 1. No release lineage

The snapshot now captures current truth, but it still does not create a git/release lineage.

### 2. Executable backups still in PATH

The manifest makes this visible and hashable, but no cleanup happened yet.

### 3. Unknown operator tools

117 active-like V7 executables are not referenced by systemd/shell-loop scan. They may be valid admin tools, but they are not runtime-bound by this manifest.

### 4. Sensitive token permission warning

`profile-delivery-tokens.json` should be reviewed before commercial production.

### 5. Runtime remains moving

Autoswitch/timers continue changing state after snapshot. This is expected. The snapshot is authoritative for its timestamp, not a permanent frozen runtime.

--------------------------------------------------
## 12. Readiness For Safe Cleanup Phase

Block 3.1 makes Block 3.2 possible.

Safe cleanup can now use:

```text
/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json
/opt/v7/ops/deploy-baseline/20260523T122251Z/checksums.sha256
```

Recommended Block 3.2 rule:

1. Use the manifest as source of truth.
2. Archive only `backup_or_stale_executable_in_path`.
3. Do not touch `active_runtime_executable`.
4. Do not touch `unknown_executable_not_bound_by_systemd` until separately classified.
5. Inspect `v7-admin-api.tmp` separately.
6. Preserve mode/mtime/hash manifest before move.
7. Re-run:

```text
v7-killswitch-check
v7-user-route-check
v7-provisioning-reconcile-check
systemctl --failed
```

--------------------------------------------------
## Final Verdict

Block 3.1 successfully created an authoritative deploy/runtime snapshot.

V7 now has:

- timestamped runtime manifest;
- executable hashes;
- systemd dependency map;
- contract metadata;
- identity DB metadata;
- rollback material classification;
- checksum verification for snapshot artifacts.

The platform is still operationally cluttered, but no longer invisible.

Next step should be controlled archival of stale executable backups out of PATH, using this manifest as the guardrail.
