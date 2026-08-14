# V7 Vozduh — Track 7.8 Maintenance & Node Runtime Support Lineage Batch

## 1. Tools Resolved

Resolved recommended maintenance/node-runtime batch:

```text
v7-log-maintenance-status
v7-maintenance-cleanup-preview
v7-node-config-check
v7-node-env
```

All four were copied read-only from live VPS `/usr/local/bin` into:

```text
tools/runtime-support/
```

No VPS runtime files were modified.

## 2. Tools Skipped

No recommended tool was skipped.

Optional tools intentionally skipped:

```text
v7-maintenance-cleanup-apply
v7-secrets-cleanup-preview
v7-secrets-cleanup-apply
```

Reason:

- `v7-maintenance-cleanup-apply` is an apply tool and explicitly out of this batch.
- `v7-secrets-cleanup-preview` belongs in a separate security/sensitive-state batch.
- `v7-secrets-cleanup-apply` is explicitly forbidden in this track.

## 3. Repo Paths Created / Updated

Created:

```text
tools/runtime-support/v7-log-maintenance-status
tools/runtime-support/v7-maintenance-cleanup-preview
tools/runtime-support/v7-node-config-check
tools/runtime-support/v7-node-env
```

Hashes match `runtime-enumeration.json`.

## 4. Lineage Metadata File

Created:

```text
docs/track7/lineage/maintenance-node-runtime-tools.json
```

Metadata includes:

- basename;
- batch;
- runtime path;
- sha256;
- size;
- mode;
- mtime epoch;
- governance class;
- runtime criticality;
- release relevance;
- provenance confidence;
- reference count and samples;
- repo path;
- owner;
- purpose;
- mutation level;
- state reads/writes;
- verification requirement;
- special safety notes;
- lineage status.

## 5. Owner / Purpose / Mutation Classification

| Tool | Owner | Mutation Level | Purpose |
|---|---|---|---|
| `v7-log-maintenance-status` | `maintenance` | `runtime-check` | Report log/journal maintenance status and large V7 logs |
| `v7-maintenance-cleanup-preview` | `maintenance` | `maintenance-preview` | Preview backup retention, journal, and logrotate cleanup plan |
| `v7-node-config-check` | `node-runtime` | `runtime-check` | Validate loaded/detected node network configuration |
| `v7-node-env` | `node-runtime` | `read-only` | Print detected/default node env variables |

## 6. Special Safety Review Findings

`v7-maintenance-cleanup-preview`:

- does not invoke `v7-maintenance-cleanup-apply`;
- does not run `journalctl --vacuum-*`;
- does not run `logrotate`;
- does not delete backups;
- does read `/root/v7-backups`, `/etc/v7/maintenance.conf`, journal usage, and disk usage;
- does create and remove a temporary file for sorted backup metadata.

Verdict:

```text
preview-only intent confirmed
not pure read-only because of temporary local file use
safe for lineage import
not safe as a unit-test command against live runtime
```

## 7. Static Verification Results

Static checks:

```text
bash -n tools/runtime-support/v7-log-maintenance-status
bash -n tools/runtime-support/v7-maintenance-cleanup-preview
bash -n tools/runtime-support/v7-node-config-check
bash -n tools/runtime-support/v7-node-env
```

Result:

```text
OK
```

Full local gate:

```text
tools/v7-run-tests
Ran 28 tests
OK
```

No imported tool was executed against live state.

## 8. Updated Governance Counts

Before Track 7.8:

```text
Runtime-only unresolved tools: 104
Critical unresolved lineage: 67
Total lineage resolved in metadata: 19
```

After Track 7.8:

```text
Tools resolved in Track 7.8: 4
Runtime-only unresolved tools by basename: 100
Critical unresolved lineage by basename: 67
Total lineage resolved in metadata: 23
Remaining known unresolved by lineage metadata: 95
```

Critical count did not drop because these tools are classified as runtime-local/noncritical support.

## 9. Runtime / Repo Diff Result

After Track 7.8:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 100
Named lineage gaps: 100
Critical lineage gaps (known): 67
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warnings:
  - runtime_manifest_not_supplied
```

## 10. Release Object Warning Status

Release lineage checker:

```text
production_only_tools=118
lineage_resolved_tools=23
remaining_known_unresolved=95
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_95_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

The platform is still not commercially reproducible.

## 11. Remaining Lineage Blockers

Still unresolved:

- 100 runtime-only tools by basename;
- 67 critical/release-relevant runtime-only tools by basename;
- 95 remaining tools by lineage metadata model;
- cleanup apply and secrets cleanup tools require separate safety review;
- runtime manifest and archive manifests remain linked by VPS path, not local artifact;
- no deployment convergence has happened.

## 12. Next Bounded Batch Safety

Next batch is safe only if it stays narrow.

Recommended next area:

```text
security/sensitive-state preview-only tools
```

Do not include apply tools or routing/policy/Direct/RU/proxy/autoswitch/user-switch tools without a dedicated higher-risk review.
