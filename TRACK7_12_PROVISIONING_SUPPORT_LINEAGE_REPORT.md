# V7 Vozduh — Track 7.12 Provisioning Support Lineage Batch

Generated: 2026-05-24

Scope: repo-side lineage resolution only. No live deploy, no VPS runtime mutation, no egress enable/disable, no live IP allocation, no registry writes, no draft runtime execution, no routing/datapath/autoswitch changes.

## 1. Tools Resolved

Resolved into repo-side lineage:

```text
v7-egress-guard
v7-egress-set-state
v7-egress-import-regression
v7-egress-draft-runtime-helper
v7-ipam-allocate
v7-ipam-preview
v7-reconcile-check
v7-reconcile-repair-preview
v7-provisioning-reconcile-check
```

Six tools were copied from live runtime into `tools/runtime-support/`. Three tools were already exact-hash present in the repo and were metadata-resolved without source duplication:

```text
tools/v7-egress-set-state
tools/v7-egress-import-regression
hardening/v7-provisioning-reconcile-check
```

## 2. Tools Skipped

No recommended provisioning-support tools were missing or skipped.

Explicitly excluded from this batch:

```text
v7-user-switch
v7-routing-sync
v7-users-autoswitch
v7-policy-*
v7-direct-*
v7-proxy-*
v7-user-enable
v7-user-disable
v7-user-create
v7-user-reconcile-apply
```

## 3. Repo Paths Created / Updated

Created repo-side lineage copies:

```text
tools/runtime-support/v7-egress-guard
tools/runtime-support/v7-egress-draft-runtime-helper
tools/runtime-support/v7-ipam-allocate
tools/runtime-support/v7-ipam-preview
tools/runtime-support/v7-reconcile-check
tools/runtime-support/v7-reconcile-repair-preview
```

Existing exact-hash repo paths used:

```text
tools/v7-egress-set-state
tools/v7-egress-import-regression
hardening/v7-provisioning-reconcile-check
```

Created metadata:

```text
docs/track7/lineage/provisioning-support-tools.json
```

Updated governance:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Provisioning Safety Review

| Tool | Classification | Safety Notes |
|---|---|---|
| `v7-egress-guard` | `read-only` | Reads egress/users registries and blocks unsafe disable/maintenance operations when users remain assigned. |
| `v7-egress-set-state` | `egress-state-write` | Dry-run by default, but `--apply` can start/stop interfaces, edit registry/flags, rebuild kill switch, and audit. |
| `v7-egress-import-regression` | `local-regression-write` | Regression harness that mutates temp fixtures and admin helper state under temp roots. Not a live runtime tool to execute casually. |
| `v7-egress-draft-runtime-helper` | `provisioning-write` | Writes draft runtime/quarantine results, updates draft metadata, can start temporary wg/awg/sing-box runtime probes. |
| `v7-ipam-allocate` | `IP-allocation` | Dry-run by default; apply writes `/opt/v7/ipam/leases.registry` after confirm and emits audit. |
| `v7-ipam-preview` | `provisioning-preview` | Read-only IPAM capacity/migration preview. |
| `v7-reconcile-check` | `reconcile-preview` | Reads users/egress/assign files and live wg/ip route state; no writes. |
| `v7-reconcile-repair-preview` | `reconcile-preview` | Prints suggested apply commands, but does not run them. |
| `v7-provisioning-reconcile-check` | `read-only` | Reads firewall/NAT/MSS/WireGuard/routing state; no repair writes. |

No selected tool was executed against live provisioning state.

## 5. Owner / Purpose / Mutation Classification

Owners:

```text
egress-lifecycle: v7-egress-guard, v7-egress-set-state
provisioning: v7-egress-import-regression, v7-egress-draft-runtime-helper, v7-ipam-allocate, v7-ipam-preview, v7-provisioning-reconcile-check
reconcile: v7-reconcile-check, v7-reconcile-repair-preview
```

Mutation classes:

```text
read-only: 2
egress-state-write: 1
local-regression-write: 1
provisioning-write: 1
IP-allocation: 1
provisioning-preview: 1
reconcile-preview: 2
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
  tools/v7-release-lineage-check tools/v7-runtime-repo-diff \
  tools/runtime-support/v7-egress-draft-runtime-helper \
  tools/v7-egress-import-regression
```

Passed:

```text
bash -n \
  tools/runtime-support/v7-egress-guard \
  tools/v7-egress-set-state \
  tools/runtime-support/v7-ipam-allocate \
  tools/runtime-support/v7-ipam-preview \
  tools/runtime-support/v7-reconcile-check \
  tools/runtime-support/v7-reconcile-repair-preview \
  hardening/v7-provisioning-reconcile-check
```

Passed:

```text
python3 -m json.tool docs/track7/lineage/provisioning-support-tools.json
```

## 7. Updated Governance Counts

Before Track 7.12:

```text
Runtime-only unresolved tools: 88
Critical unresolved lineage: 59
Total lineage resolved in metadata: 35
```

After Track 7.12:

```text
Runtime-only unresolved tools by basename: 82
Critical unresolved lineage by basename: 55
Total lineage resolved in metadata: 44
Remaining known unresolved by lineage metadata: 74
```

## 8. Runtime / Repo Diff Result

Read-only diff result:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 82
Named lineage gaps: 82
Critical lineage gaps (known): 55
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
lineage_resolved_tools=44
remaining_known_unresolved=74
runtime_lineage=partial
release_provenance=incomplete
release_object=releases/v7-runtime-20260523T174503Z ready=True missing=0
```

Warnings remain:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_74_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

Provisioning lineage visibility improved, but provisioning convergence is not complete.

## 10. Remaining Provisioning Blockers

- `v7-user-reconcile-apply` remains intentionally excluded and unresolved.
- Live user provisioning tools such as create/enable/disable remain out of scope.
- Routing sync and user switch tooling remain unresolved high-risk runtime mutation classes.
- `v7-egress-set-state` and `v7-egress-draft-runtime-helper` are lineage-resolved, but still require guarded runbooks before any live operation.

## 11. Next Bounded Batch Safety

Next batch is safe only if narrow and repo-side. Reasonable next scopes:

- backup/rollback support lineage;
- profile delivery/token tooling lineage;
- read-only policy diagnostics.

Do not mix routing mutation, policy apply, Direct/RU, proxy-public apply, or autoswitch tools into the next batch.
