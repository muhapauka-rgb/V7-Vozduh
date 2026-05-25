# V7 VOZDUH — BLOCK 3 REPORT
## Runtime Contracts, Deploy Truth & Operational Baseline Cleanup

Date: 2026-05-23 Europe/Moscow  
Live VPS: `195.2.79.116`  
Scope: live runtime/deploy audit, identity contract audit, rollback/deploy truth classification  
Mode: read-only inspection; no cleanup applied

--------------------------------------------------
## 1. Runtime Truth Map

### Runtime roots

Current live platform is file-based, not git-release based.

| Runtime area | Path | Role | Status |
|---|---|---|---|
| Runtime state root | `/opt/v7` | operational state, admin DB, egress state | present |
| Config root | `/etc/v7` | policies, egress drafts/config, admin safe-mode, node config | present |
| Executable root | `/usr/local/bin` | active V7 commands and many backups | present, cluttered |
| Service manager | `/etc/systemd/system` | authoritative service/timer definitions | present |

### Git baseline

No `.git` directory was found under:

```text
/opt/v7
/root
/home
```

Verdict:

```text
VPS has no clean git checkout / release baseline.
Current deploy truth is the live filesystem itself.
```

This is the main Block 3 operational risk. There is no reliable answer to:

```text
which commit produced this VPS state?
which exact local files match live?
what is the current release id?
```

### Active systemd runtime commands

Systemd references these V7 executables directly:

```text
/usr/local/bin/v7-admin-api
/usr/local/bin/v7-api
/usr/local/bin/v7-client-speed-api
/usr/local/bin/v7-direct-auto-sync
/usr/local/bin/v7-egress-quality-compact
/usr/local/bin/v7-killswitch-enable
/usr/local/bin/v7-mss-clamp-enable
/usr/local/bin/v7-path-guard-repair
/usr/local/bin/v7-path-sanity-check
/usr/local/bin/v7-public-gateway
/usr/local/bin/v7-routing-sync
/usr/local/bin/v7-service-matrix-refresh-all
/usr/local/bin/v7-telegram-sentinel
/usr/local/bin/v7-traffic-snapshot
/usr/local/bin/v7-users-autoswitch
/usr/local/bin/v7-watch
```

Other active units also execute shell loops that call additional V7 tools by PATH:

```text
v7-benchmark.service:
  v7-egress-benchmark-all

v7-health.service:
  v7-egress-history
  v7-egress-stability
  v7-egress-load
  v7-egress-diagnose
  v7-state-merge
  v7-user-desired-state-save
  v7-state-json-save
  v7-users-autoswitch
```

This means runtime truth is not only explicit `ExecStart` paths. Some runtime dependencies are implicit PATH lookups inside shell loops.

### Runtime ownership model

| Area | Owner/writer | Runtime meaning |
|---|---|---|
| `/etc/systemd/system/v7*.service`, `v7*.timer` | operator/deploy | service authority |
| `/usr/local/bin/v7*` active files | operator/deploy | executable authority |
| `/etc/v7/policy.json` | operator/admin | hard autoswitch/policy authority |
| `/etc/v7/org-egress-policy.json` | operator/admin | tenant/group policy authority |
| `/opt/v7/egress/state/users.registry` | user/admin/provisioning/autoswitch | user assignment/effective user routing intent |
| `/opt/v7/egress/state/egress.registry` | provisioning/admin | egress inventory authority |
| `/opt/v7/admin/v7-identity.db` | admin API/identity layer | identity authority |
| `autoswitch-safety.json` | autoswitch | anti-flap/freeze authority |
| `telegram-sentinel.json` | Telegram sentinel | advisory fast Telegram signal |
| `egress-quality-summary.json` | quality compactor | historical quality signal |
| `egress-load-summary.json` | autoswitch | capacity signal |
| `v7-state.json` | state merge/save loop | generated aggregate/cache |

--------------------------------------------------
## 2. Deploy Structure Analysis

### Current deploy model

The VPS is deployed by copying standalone executables into:

```text
/usr/local/bin
```

and managing service definitions under:

```text
/etc/systemd/system
```

There is no release directory like:

```text
/opt/v7/releases/<version>
/opt/v7/current
```

There is no manifest tying together:

- executable hashes;
- systemd unit versions;
- config versions;
- migration steps;
- rollback points.

### Active services observed

Important active service/timer facts:

```text
v7-admin-api.service              active/running -> /usr/local/bin/v7-admin-api
v7-api.service                    active/running -> /usr/local/bin/v7-api
v7-client-speed-api.service       active/running -> /usr/local/bin/v7-client-speed-api
v7-killswitch.service             active/exited  -> /usr/local/bin/v7-killswitch-enable
v7-routing-sync.service           active/exited  -> /usr/local/bin/v7-routing-sync
v7-users-autoswitch.timer         active/waiting -> v7-users-autoswitch.service
v7-users-autoswitch.service       inactive/dead  -> /usr/local/bin/v7-users-autoswitch --apply
v7-telegram-sentinel.timer        active         -> v7-telegram-sentinel.service
v7-telegram-sentinel.service      uses /usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
v7-health.service                 active/running -> shell loop calling multiple v7 tools
```

Block 1.1 advisory-first sentinel is still present:

```text
/etc/systemd/system/v7-telegram-sentinel.service.d/10-advisory-first.conf
ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch
```

### Deploy ambiguity

There are three overlapping deploy truths:

1. Current active systemd `ExecStart`.
2. Current executable names in `/usr/local/bin`.
3. Historical backup executables also in `/usr/local/bin`.

Only the first two are runtime-active. The third is rollback material, but it lives in the same PATH namespace as active commands.

--------------------------------------------------
## 3. Executable Clutter Analysis

### Counts

Current `/usr/local/bin` V7 file count:

```text
total v7* files: 349
active-like files: 142
backup/stale-like files: 207
executable backups: 207
```

Every detected backup/stale file is executable and still in PATH.

### Examples of active-like files

Examples:

```text
v7-admin-api
v7-api
v7-audit-log
v7-killswitch-check
v7-killswitch-enable
v7-observability-summary
v7-provisioning-reconcile-check
v7-routing-sync
v7-service-matrix-test
v7-telegram-sentinel
v7-users-autoswitch
```

One suspicious active-like name also exists:

```text
v7-admin-api.tmp
```

This is not classified as backup by name, but it is not obviously an intended command. It should be manually classified before any cleanup.

### Examples of backup/stale files in PATH

Examples:

```text
v7-admin-api.backup-nav-cache-20260520-182701
v7-admin-api.backup-routefix-20260520-103228
v7-admin-api.backup-telegram-sentinel-20260520
v7-admin-api.backup.balance-reconnect-20260522-170721
v7-admin-api.bak.20260508-114731
v7-admin-api.bak.20260511-160534
```

The pattern repeats heavily for `v7-admin-api`.

### Risk

This is dangerous because:

- backups are executable;
- backups are in PATH;
- tab completion / manual operator commands can accidentally run stale code;
- a service or script could explicitly call a backup name later;
- no manifest distinguishes current executable from rollback copy.

### Cleanup verdict

No cleanup was applied.

Reason:

```text
207 executable backups should not stay in PATH,
but moving them without a manifest/reference check could destroy rollback evidence.
```

Safe cleanup must be a separate controlled operation.

--------------------------------------------------
## 4. Identity DB Dependency Map

### Live DB paths

Observed:

```text
/opt/v7/admin/v7-identity.db      exists
/opt/v7/identity/v7-identity.db   missing
```

Live DB:

```text
path: /opt/v7/admin/v7-identity.db
mode: 0600
size: 200704 bytes
tables: 12
```

Tables:

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

SQLite read-only access succeeded.

### Active references

Current active admin executable:

```text
/usr/local/bin/v7-admin-api
line 47:
IDENTITY_DB_FILE = Path(os.environ.get("V7_IDENTITY_DB_FILE", "/opt/v7/admin/v7-identity.db"))
```

Current admin systemd service:

```text
/etc/systemd/system/v7-admin-api.service
ReadWritePaths includes /opt/v7/admin
```

No active service default points to:

```text
/opt/v7/identity/v7-identity.db
```

Many historical `v7-admin-api.bak*` and `v7-admin-api.backup*` files also reference `/opt/v7/admin/v7-identity.db`.

### Canonical path verdict

For current production runtime, the canonical identity DB path is:

```text
/opt/v7/admin/v7-identity.db
```

The path:

```text
/opt/v7/identity/v7-identity.db
```

is not a live runtime contract today. It is a future/desired structure idea or stale assumption.

### Safest alignment plan

Do not move the live DB now.

Safe staged plan:

1. Document `/opt/v7/admin/v7-identity.db` as current canonical runtime path.
2. Add validators to accept this current path as canonical.
3. If future migration to `/opt/v7/identity` is desired:
   - stop admin API;
   - backup DB;
   - copy DB to new path;
   - set `V7_IDENTITY_DB_FILE=/opt/v7/identity/v7-identity.db` explicitly in systemd;
   - keep old path as compatibility symlink only after verifying SQLite access and app start;
   - verify onboarding/profile delivery;
   - only then update docs.

Immediate symlink or move is not recommended in Block 3.

--------------------------------------------------
## 5. Runtime Contract Classification

### Authoritative contracts

| File | Classification | Rebuildability | Notes |
|---|---|---|---|
| `/etc/v7/policy.json` | hard policy authority | not rebuildable safely without backup | autoswitch/policy hard limits |
| `/etc/v7/org-egress-policy.json` | tenant/group policy authority | not rebuildable safely without backup | org/group route policy |
| `/opt/v7/egress/state/users.registry` | user assignment authority / effective routing intent | not rebuildable safely from runtime alone | actively changes |
| `/opt/v7/egress/state/egress.registry` | egress inventory authority | not rebuildable safely from runtime alone | enabled egress list |
| `/opt/v7/admin/v7-identity.db` | identity authority | not rebuildable from JSON state | SQLite live DB |
| `/opt/v7/egress/state/profile-delivery-tokens.json` | profile delivery authority/sensitive state | not safely rebuildable | token state, should be protected |

### Runtime safety authorities

| File | Classification | Rebuildability | Notes |
|---|---|---|---|
| `/opt/v7/egress/state/autoswitch-safety.json` | anti-flap/freeze authority | technically rebuildable but losing it removes safety memory | runtime-critical for calm routing |
| `/opt/v7/egress/state/client-reconnect-state.json` | client experience/supporting state | partially rebuildable over time | useful for autoswitch/reconnect signals |

### Advisory/supporting signals

| File | Classification | Rebuildability | Notes |
|---|---|---|---|
| `/opt/v7/egress/state/telegram-sentinel.json` | fast Telegram advisory signal | rebuildable by sentinel | runtime-critical as a signal, not policy |
| `/opt/v7/egress/state/egress-quality-summary.json` | historical quality signal | rebuildable over time, history loss affects confidence | not hard live truth |
| `/opt/v7/egress/state/egress-load-summary.json` | capacity signal | rebuildable on autoswitch run | operator-facing capacity summary |

### Generated aggregate/cache

| File | Classification | Rebuildability | Notes |
|---|---|---|---|
| `/opt/v7/egress/state/v7-state.json` | generated aggregate/cache | rebuildable from source state | useful for UI/summary but not primary authority |

### Observed contract stats

```text
users.registry: 17 lines, mtime 2026-05-23T12:10:22Z
egress.registry: 6 lines, mtime 2026-05-22T13:37:36Z
autoswitch-safety.json: dict, keys schema_version/users/egress/updated
telegram-sentinel.json: dict, advisory signal keys present
egress-quality-summary.json: dict, windows/items
egress-load-summary.json: dict, operator_status/semantics/summary
client-reconnect-state.json: dict, users/events
v7-state.json: dict aggregate
profile-delivery-tokens.json: dict tokens
```

--------------------------------------------------
## 6. Backup & Rollback Safety Analysis

### What is trustworthy

Trustworthy rollback material:

- explicitly named config backups outside active command names, for example `/etc/v7/policy.json.backup.block1-20260523-002634`;
- live state backups under `/opt/v7/egress/state/*.backup.*`, if used with explicit restore procedure;
- local repo versions, if matched by checksum to live;
- service drop-ins with clear purpose, such as sentinel advisory-first override.

### What is weak

Weak rollback material:

```text
/usr/local/bin/v7-admin-api.backup*
/usr/local/bin/v7-admin-api.bak*
other executable backups in /usr/local/bin
```

They are valuable as historical artifacts, but weak as rollback mechanism because:

- no manifest says which backup is safe;
- no checksum/release ID;
- many are executable in PATH;
- many represent intermediate phases, not known-good releases.

### Backup safety verdict

Backups should be preserved, but moved out of PATH only after:

1. Create archive directory:

```text
/root/v7-backups/usr-local-bin-archive/<timestamp>/
```

2. Save manifest:

```text
filename
size
mode
mtime
sha256
current active counterpart if known
```

3. Verify no systemd unit references backup names.
4. Move only files matching strict backup patterns.
5. Re-run systemd and runtime checks.

No such move was performed in Block 3.

--------------------------------------------------
## 7. Exact Changes Applied

No live changes were applied.

No files were moved, deleted, rewritten, symlinked, or chmodded.

No systemd units were changed or restarted.

No DB migration was performed.

This was intentional. The current deploy ambiguity is real, but cleanup is not safe without a manifest-producing step.

--------------------------------------------------
## 8. Verification Results

Required checks after inspection:

```text
v7-killswitch-check: 0 / OK
v7-user-route-check: 0 / OK
v7-provisioning-reconcile-check: 0 / OK
```

Identity DB:

```text
/opt/v7/admin/v7-identity.db: readable via SQLite mode=ro
/opt/v7/identity/v7-identity.db: missing
```

Observability at first snapshot:

```text
system.status: unstable
system.severity: critical
autoswitch_state: degraded
capacity.status: healthy
autoswitch.reason: 16 users frozen by anti-flap safety
```

Systemd integrity:

```text
active V7 units resolved to current /usr/local/bin executables
sentinel drop-in still uses --no-autoswitch
autoswitch service still uses --apply via timer
```

--------------------------------------------------
## 9. Remaining Operational Risks

### 1. No clean git/release baseline on VPS

This is the largest Block 3 issue.

The VPS can run, but it cannot currently prove:

- which commit is deployed;
- which files differ from source;
- which deploy set is canonical;
- which rollback point is known-good.

### 2. Executable backups in PATH

There are:

```text
207 executable backup/stale-like files in /usr/local/bin
```

This is not merely untidy. It is an operational hazard.

### 3. Runtime truth changes while auditing

During the audit, live user assignment state changed again. A later snapshot showed:

```text
current_user_assignment_counts:
  1: 15
  vless: 2
```

This differs from the earlier Block 2.2 snapshot where all users were on `vless`.

This does not mean Block 3 caused movement. It means timers/autoswitch/health loops continue to evolve runtime while audits run. Any future deploy baseline must capture timestamped snapshots and service state at the same time.

### 4. Identity path mismatch is documentation/contract risk

Runtime uses:

```text
/opt/v7/admin/v7-identity.db
```

Any code, validator, or documentation expecting:

```text
/opt/v7/identity/v7-identity.db
```

is wrong for current production.

### 5. Active shell-loop dependencies are implicit

`v7-health.service` and `v7-benchmark.service` call tools by name inside shell loops. A PATH collision or stale executable name can affect runtime in ways that are less obvious than explicit `ExecStart=/usr/local/bin/...`.

### 6. Sensitive token file permissions

`profile-delivery-tokens.json` exists and is mode `0644`.

This should be reviewed. It may be acceptable in current single-root deployment, but for a commercial/multi-tenant platform it is too permissive unless proven otherwise.

--------------------------------------------------
## 10. Recommended Next Stabilization Priorities

### Priority 1 — Create deploy manifest, not cleanup first

Create a read-only manifest tool that records:

```text
/usr/local/bin/v7* active files
/etc/systemd/system/v7* units/drop-ins
/etc/v7/*.json policy/config
/opt/v7/admin/v7-identity.db metadata
/opt/v7/egress/state authoritative contracts metadata
sha256, size, mtime, mode
```

This should produce:

```text
/opt/v7/ops/deploy-baseline/<timestamp>/manifest.json
```

No runtime behavior change required.

### Priority 2 — Archive executable backups out of PATH with manifest

After manifest creation:

```text
move backup/stale-like executable files from /usr/local/bin
to /root/v7-backups/usr-local-bin-archive/<timestamp>/
```

Only after verifying:

- no systemd references them;
- no active shell loops reference them;
- current active command set remains unchanged;
- checks pass.

### Priority 3 — Formalize identity DB current contract

Document current canonical path:

```text
/opt/v7/admin/v7-identity.db
```

Do not migrate yet.

Add validator behavior:

- current path = OK;
- future `/opt/v7/identity` missing = warning only, not failure;
- if both exist, warn unless explicitly configured by `V7_IDENTITY_DB_FILE`.

### Priority 4 — Add compact operator runtime baseline summary

Operator-facing summary should be calm:

```text
Runtime baseline: unversioned filesystem deploy
Deploy manifest: missing
Executable clutter: 207 backups in PATH
Identity DB: current canonical /opt/v7/admin/v7-identity.db
Rollback paths: available but unverified
Datapath checks: OK
```

No giant filesystem dashboard.

### Priority 5 — Protect sensitive state permissions

Review:

```text
/opt/v7/egress/state/profile-delivery-tokens.json
```

Recommended future target:

```text
0600 root:root
```

Do not change until admin/API read/write expectations are verified.

--------------------------------------------------
## Final Verdict

Block 3 confirms the platform’s main current risk is operational baseline ambiguity:

```text
V7 is operational,
datapath checks pass,
but deploy truth is filesystem-only and cluttered.
```

The correct next move is not a rewrite and not aggressive cleanup.

The correct next move is:

```text
manifest -> classify -> archive backups out of PATH -> verify
```

Only after that should the VPS be considered to have a predictable operational baseline.
