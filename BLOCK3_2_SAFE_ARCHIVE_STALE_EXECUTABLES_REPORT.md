# V7 VOZDUH — BLOCK 3.2 REPORT
## Safe Archive Of Stale Executables Out Of PATH

Date: 2026-05-23 Europe/Moscow  
Live VPS: `195.2.79.116`  
Baseline source: `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`  
Action: moved only `backup_or_stale_executable_in_path` files from `/usr/local/bin` to archive

--------------------------------------------------
## 1. Manifest Validation Result

Before cleanup, Block 3.1 snapshot artifacts were verified:

```text
checksums.sha256: OK
contract-summary.json: OK
manifest.json: OK
runtime-summary.md: OK
unit-summary.json: OK
```

Manifest classification counts:

```text
active_runtime_executable: 24
backup_or_stale_executable_in_path: 207
suspicious_executable_in_path: 1
unknown_executable_not_bound_by_systemd: 117
```

Cleanup candidates:

```text
stale_candidates: 207
stale_active_overlap: 0
stale_missing_before: 0
```

Suspicious exclusion:

```text
v7-admin-api.tmp
```

The manifest was accepted as the authoritative source of truth.

--------------------------------------------------
## 2. Files Archived

Archive directory:

```text
/root/v7-backups/usr-local-bin-archive/20260523T122936Z
```

Archive result:

```text
candidates: 207
moved: 207
skipped: 0
active_excluded: 24
unknown_excluded: 117
suspicious_excluded: 1
```

The moved files were all classified as:

```text
backup_or_stale_executable_in_path
```

No active runtime executable was moved.

No unknown executable was moved.

No suspicious executable was moved.

--------------------------------------------------
## 3. Files Intentionally Skipped

### Active runtime executables skipped

All 24 active runtime executables from the Block 3.1 manifest were excluded from archive.

Examples:

```text
v7-admin-api
v7-api
v7-killswitch-enable
v7-routing-sync
v7-telegram-sentinel
v7-users-autoswitch
```

### Unknown executable tools skipped

All 117 `unknown_executable_not_bound_by_systemd` files were left in place.

Reason:

```text
They may be valid operator/admin tools even if not systemd-bound.
They require separate classification before archive.
```

### Suspicious executable skipped

Left intentionally in PATH:

```text
/usr/local/bin/v7-admin-api.tmp
```

Reason:

```text
It is suspicious, but not classified as stale by manifest.
It must be inspected separately before any move.
```

--------------------------------------------------
## 4. Unknown Executable Count Remaining

Remaining unknown/operator-tool class:

```text
117
```

These were not touched.

The cleanup intentionally targeted only stale executable backups, not all non-runtime tools.

--------------------------------------------------
## 5. Suspicious Executable Status

Suspicious executable still present:

```text
v7-admin-api.tmp
```

Post-cleanup inventory confirmed:

```text
suspicious_missing_should_be_0: 0
suspicious_remaining:
  - v7-admin-api.tmp
```

This is correct for Block 3.2. It should be handled only after separate classification.

--------------------------------------------------
## 6. PATH Cleanup Result

Before:

```text
/usr/local/bin/v7* total: 349
backup/stale executable files in PATH: 207
```

After:

```text
/usr/local/bin/v7* total: 142
backup-like remaining in PATH: 0
suspicious-like remaining in PATH: 1
```

The PATH is now substantially cleaner while preserving rollback material outside PATH.

--------------------------------------------------
## 7. Archive Manifest Summary

Created:

```text
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/archive-manifest.json
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/moved-files.txt
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/skipped-files.json
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/checksums.sha256
```

Archive contents:

```text
archive size: 117M
moved stale executables: 207
archive-manifest.json: 228K
checksums.sha256: 23K
moved-files.txt: 33K
skipped-files.json: empty list
```

Archive hash verification:

```text
sha256sum -c checksums.sha256: OK
```

The archive manifest stores for each moved file:

- original path;
- archive path;
- classification;
- size;
- mode;
- uid/gid;
- mtime;
- sha256;
- Block 3.1 snapshot reference.

--------------------------------------------------
## 8. Runtime Verification Results

### Active executable integrity

Post-archive verification:

```text
active_missing: []
active_changed: []
stale_remaining_from_manifest: 0
unknown_missing_should_be_0: 0
suspicious_missing_should_be_0: 0
```

All active runtime executable hashes remained unchanged relative to Block 3.1 manifest.

### Systemd integrity

```text
systemctl --failed: 0 loaded units listed
```

No systemd unit failures were introduced.

### Datapath and runtime checks

```text
v7-killswitch-check: OK
v7-user-route-check: OK
v7-provisioning-reconcile-check: OK
```

No datapath regression was observed.

### Observability summary after cleanup

```text
system.status: unstable
system.severity: critical
attention_incidents: 7
trusted_ru_state: unknown
capacity.status: high
autoswitch.status: degraded
autoswitch.reason: 17 users frozen by anti-flap safety
```

This is not caused by PATH cleanup. It reflects ongoing runtime/autoswitch/health state.

--------------------------------------------------
## 9. Rollback Safety Explanation

No backup was deleted.

No backup was compressed.

No backup content was modified.

Files were moved from:

```text
/usr/local/bin/<filename>
```

to:

```text
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/<filename>
```

Restore procedure:

1. Locate entry in:

```text
/root/v7-backups/usr-local-bin-archive/20260523T122936Z/archive-manifest.json
```

2. Verify archive file hash against `after.sha256`.
3. Move exact file back to `original_path`.
4. Verify mode/mtime if needed from manifest.
5. Run:

```text
systemctl --failed
v7-killswitch-check
v7-user-route-check
v7-provisioning-reconcile-check
```

Because these files were not active runtime executables, restoring them should normally not require service restarts.

--------------------------------------------------
## 10. Remaining Operational Risks

### 1. No release lineage yet

The VPS now has a clean baseline snapshot and archive manifest, but still no git/release deployment model.

### 2. Unknown executable set remains

There are still 117 active-like V7 executables not bound by systemd/shell-loop scan. They may be valid operator tools. They should be classified separately before any further cleanup.

### 3. Suspicious `v7-admin-api.tmp`

This remains intentionally untouched. It should be inspected in a separate small block.

### 4. Runtime health remains unstable

Post-cleanup observability still reports:

```text
system: unstable
autoswitch: degraded
capacity: high
```

This is not a deploy cleanup regression, but the platform remains operationally noisy.

### 5. Sensitive token permissions

`profile-delivery-tokens.json` permission warning remains from Block 3.1 and should be handled separately after access expectations are verified.

--------------------------------------------------
## Final Verdict

Block 3.2 successfully removed stale executable clutter from PATH while preserving rollback material.

V7 now has:

- no manifest-classified stale executable backups left in `/usr/local/bin`;
- active executable hashes unchanged;
- unknown and suspicious files preserved for later classification;
- archive manifest with restore mapping;
- datapath checks still OK;
- systemd failed units count still zero.

This improves operational predictability without changing routing, datapath, systemd behavior, or active runtime executables.
