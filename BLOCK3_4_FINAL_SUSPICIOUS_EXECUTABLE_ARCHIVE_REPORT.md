# V7 Vozduh - Block 3.4 Final Suspicious Executable Classification & Safe Archive

Generated: 2026-05-23

Scope: final verification and archive of the single known suspicious executable:

```text
/usr/local/bin/v7-admin-api.tmp
```

Rules followed:

- No active runtime executables were touched.
- No systemd units were changed.
- No routing, datapath, kill switch, autoswitch, route class, Trusted RU, or Gosuslugi behavior was changed.
- No unknown operator utilities were cleaned.
- Only `v7-admin-api.tmp` was moved, after final reference verification.

## 1. Final Suspicious Executable Analysis

Target before archive:

| Field | Value |
|---|---|
| Path | `/usr/local/bin/v7-admin-api.tmp` |
| Type | Python script, UTF-8 text executable |
| Executable | Yes |
| Mode | `0755` |
| Owner | `root:root` |
| Size | `1,219,483` bytes |
| SHA256 | `0b8ba074a7392816a8705721a2a0746f1154bfc02967c77d75a8fc80b1e23c10` |
| Mtime | `2026-05-13T22:37:40Z` |
| PATH lookup before | `/usr/local/bin/v7-admin-api.tmp` |

Active admin runtime comparison:

| Field | Active `/usr/local/bin/v7-admin-api` |
|---|---|
| Type | Python script, UTF-8 text executable |
| Mode | `0755` |
| Owner | `root:root` |
| Size | `1,747,464` bytes |
| SHA256 | `f7fbb4234fa1d9a4cf4ef92f4b52bf30d315a9f818a235b7073a18c8a9ffb5d3` |
| Mtime | `2026-05-22T15:39:40Z` |
| Same hash as tmp | No |
| Tmp size delta vs active | `-527,981` bytes |

Verdict:

`v7-admin-api.tmp` was a stale temporary deploy artifact. It was executable and discoverable through PATH, but it did not match the active admin runtime and had no live runtime references.

## 2. Runtime Reference Verdict

Final reference scan covered:

- `/etc/systemd/system`
- `/lib/systemd/system`
- `/usr/local/bin`
- `/opt/v7`
- `/etc/v7`
- live process cmdlines under `/proc`
- PATH lookup

Results:

| Reference Type | Result |
|---|---|
| Runtime reference files | `0` |
| Live process references | `0` |
| Systemd runtime references | `0` |
| `/usr/local/bin` script/helper references | `0` |
| `/etc/v7` references | `0` |
| PATH lookup before archive | Found |
| PATH lookup after archive | Not found |

The only references found were historical inventory references:

- `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/checksums.sha256`

Those are baseline/snapshot records, not live runtime dependencies. The first conservative safety pass stopped on these references; the final pass explicitly classified them as non-runtime evidence before archiving.

Final dependency verdict:

```text
runtime_reference_count=0
process_reference_count=0
safe_to_archive=true
```

## 3. Archive Action Details

Action performed:

```text
/usr/local/bin/v7-admin-api.tmp
-> /root/v7-backups/usr-local-bin-archive/20260523T124646Z/v7-admin-api.tmp
```

Archive directory:

```text
/root/v7-backups/usr-local-bin-archive/20260523T124646Z/
```

Archive contents:

- `v7-admin-api.tmp`
- `archive-manifest.json`
- `checksums.sha256`
- `moved-files.txt`

Archive classification:

```text
temporary_deploy_artifact_suspicious_executable
```

Archive reason:

```text
Executable admin-like temporary artifact in PATH; no runtime/systemd/shell/process
references found; differs from active admin API.
```

No delete was performed. Rollback remains possible by moving the archived file back to the original path if ever needed.

## 4. Checksums And Archive Metadata

Archived file metadata:

| Field | Value |
|---|---|
| Archive path | `/root/v7-backups/usr-local-bin-archive/20260523T124646Z/v7-admin-api.tmp` |
| Size | `1,219,483` bytes |
| Mode | `0755` |
| Owner | `root:root` |
| SHA256 | `0b8ba074a7392816a8705721a2a0746f1154bfc02967c77d75a8fc80b1e23c10` |
| Mtime preserved | `2026-05-13T22:37:40Z` |

Manifest files created:

```text
/root/v7-backups/usr-local-bin-archive/20260523T124646Z/archive-manifest.json
/root/v7-backups/usr-local-bin-archive/20260523T124646Z/checksums.sha256
/root/v7-backups/usr-local-bin-archive/20260523T124646Z/moved-files.txt
```

Active admin runtime after archive:

- `/usr/local/bin/v7-admin-api` still exists.
- Active admin hash unchanged: yes.
- Active admin SHA256 remains:
  `f7fbb4234fa1d9a4cf4ef92f4b52bf30d315a9f818a235b7073a18c8a9ffb5d3`

## 5. Runtime Verification Results

Post-archive verification:

| Check | Result |
|---|---|
| `systemctl --failed` | PASS, `0 loaded units listed` |
| `v7-killswitch-check` | PASS |
| `v7-user-route-check` | PASS |
| `v7-provisioning-reconcile-check` | PASS |

No datapath regression was observed.

No route mismatch was introduced by this operation.

No active executable hash changed.

## 6. PATH Integrity Result

PATH state after archive:

| Check | Result |
|---|---|
| Original `/usr/local/bin/v7-admin-api.tmp` exists | No |
| `command -v v7-admin-api.tmp` | Empty |
| `v7*.tmp` files in `/usr/local/bin` | None |
| `/usr/local/bin/v7*` total | `141` |
| Known suspicious executables in PATH | `0` |

Updated operational baseline:

```text
Active runtime executables: stable
Backup clutter in PATH: removed in Block 3.2
Known suspicious executables in PATH: 0
Runtime baseline snapshot: present
Deploy manifest: present
Archive manifest for tmp artifact: present
Datapath checks: OK
```

## 7. Remaining Operational Risks

Block 3.4 removed the last known suspicious executable from PATH. It did not solve broader deploy governance risks.

Remaining risks:

- `117` unknown active-like runtime tools remain classified but not yet fully governed.
- `103` production-only tools still lack clean repository lineage.
- Hidden PATH dependencies remain possible for operator workflows, even though the known suspicious tmp artifact is gone.
- Sensitive state permissions from Block 3.3 still need a dedicated hardening pass, especially:
  `/opt/v7/egress/state/profile-delivery-tokens.json`.
- Deploy truth is better, but still not a full release system.

Do not do broad cleanup next. The safe next work is governance, lineage, and sensitive-state hardening.

## 8. Final Verdict

Block 3.4 completed the initial operational cleanup phase safely.

Result:

- `v7-admin-api.tmp` was confirmed as a stale temporary executable artifact.
- It had no live runtime references.
- It differed from the active admin API.
- It was archived out of PATH with hash and metadata preserved.
- Rollback material was kept.
- Runtime checks remained healthy.
- Known suspicious executables in PATH are now `0`.

The platform now has a cleaner operational baseline without changing routing behavior.

