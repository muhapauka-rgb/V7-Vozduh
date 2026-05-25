# V7 Vozduh — Track 7.13 Backup & Rollback Support Lineage Batch

Generated: 2026-05-24

Scope: repo-side lineage resolution only. No live deploy, no VPS runtime mutation, no rollback execution, no config restore, no backup restore, no routing/datapath/autoswitch changes.

## 1. Tools Resolved

Resolved into repo-side lineage:

```text
v7-rollback-last-change
v7-policy-live-rollback
v7-proxy-runtime-guard-rollback
v7-subnet-test-rollback
```

`v7-subnet-test-rollback` was included as the optional same-scope rollback tool because it is present in runtime enumeration and clearly rollback/restore scoped.

Repo path for all resolved tools:

```text
tools/runtime-support/
```

All copied hashes match `runtime-enumeration.json`.

## 2. Tools Skipped

No recommended rollback tools were missing or skipped.

Explicitly excluded from this batch:

```text
v7-routing-sync
v7-user-switch
v7-users-autoswitch
v7-policy-apply
v7-direct-*
v7-proxy-public-enable
v7-proxy-runtime-guard-apply
v7-user-reconcile-apply
```

## 3. Repo Paths Created / Updated

Created repo-side lineage copies:

```text
tools/runtime-support/v7-rollback-last-change
tools/runtime-support/v7-policy-live-rollback
tools/runtime-support/v7-proxy-runtime-guard-rollback
tools/runtime-support/v7-subnet-test-rollback
```

Created metadata:

```text
docs/track7/lineage/rollback-backup-support-tools.json
```

Updated governance:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Rollback Safety Review

| Tool | Classification | Safety Notes |
|---|---|---|
| `v7-rollback-last-change` | `rollback-write` | Dry-run finds newest backup candidate. Apply can restore broad target classes: executables, WireGuard configs, V7 configs, admin auth config, identity DB, egress state. |
| `v7-policy-live-rollback` | `rollback-preview` | Guarded placeholder. Validates backup readability, then returns `BLOCKED_PLACEHOLDER`; no live policy rollback currently performed. |
| `v7-proxy-runtime-guard-rollback` | `proxy-runtime-restore` | Requires confirm and root. Restores nftables ruleset from backup and can remove a runtime user created by apply. |
| `v7-subnet-test-rollback` | `routing-restore` | Dry-run by default. Apply rewrites `/etc/v7/node.env`, removes iptables NAT rules for test subnet, runs kill switch rebuild/check, and audits. |

No selected tool was executed against live rollback/runtime state.

## 5. Owner / Purpose / Mutation Classification

Owners:

```text
rollback: v7-rollback-last-change, v7-subnet-test-rollback
policy: v7-policy-live-rollback
proxy-runtime: v7-proxy-runtime-guard-rollback
```

Mutation classes:

```text
rollback-write: 1
rollback-preview: 1
proxy-runtime-restore: 1
routing-restore: 1
```

## 6. Static Verification Results

Passed:

```text
tools/v7-run-tests
Ran 28 tests OK
```

Passed:

```text
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile \
  admin/v7-admin-api admin_core/*.py \
  tools/v7-release-lineage-check tools/v7-runtime-repo-diff
```

Passed:

```text
bash -n \
  tools/runtime-support/v7-rollback-last-change \
  tools/runtime-support/v7-policy-live-rollback \
  tools/runtime-support/v7-proxy-runtime-guard-rollback \
  tools/runtime-support/v7-subnet-test-rollback
```

Passed:

```text
python3 -m json.tool docs/track7/lineage/rollback-backup-support-tools.json
```

## 7. Updated Governance Counts

Before Track 7.13:

```text
Runtime-only unresolved tools: 82
Critical unresolved lineage: 55
Total lineage resolved in metadata: 44
```

After Track 7.13:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 48
Remaining known unresolved by lineage metadata: 70
```

## 8. Runtime / Repo Diff Result

Read-only diff result:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 78
Named lineage gaps: 78
Critical lineage gaps (known): 52
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
```

Warning remains:

```text
runtime_manifest_not_supplied
```

## 9. Release Object Warning Status

Release lineage checker result:

```text
lineage_resolved_tools=48
remaining_known_unresolved=70
runtime_lineage=partial
release_provenance=incomplete
release_object=releases/v7-runtime-20260523T174503Z ready=True missing=0
```

Warnings remain:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_70_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

Rollback lineage visibility improved, but rollback safety is not proven.

## 10. Remaining Rollback / Runtime Blockers

- Apply-side rollback runbooks are not validated.
- `v7-rollback-last-change` is broad and target-dependent; it needs stricter operator UX before commercial use.
- Proxy runtime guard apply tooling remains intentionally excluded.
- Routing, policy apply, Direct/RU, proxy-public, and autoswitch mutation layers remain unresolved high-risk lineage groups.

## 11. Next Bounded Batch Safety

Next batch is safe only if narrow and repo-side. Reasonable next scopes:

- profile delivery/token tooling lineage;
- read-only policy diagnostics;
- backup list/verify/restore-preview if present.

Do not include routing mutation, policy apply, Direct/RU apply, proxy-public apply, or autoswitch tools in the next batch.
