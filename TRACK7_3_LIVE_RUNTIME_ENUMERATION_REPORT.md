# V7 Vozduh — Track 7.3 Live Runtime Manifest Enumeration & Lineage Expansion Report

## 1. Expanded Runtime Inventory

Track 7.3 added a read-only runtime enumeration path, but live VPS enumeration did not complete because SSH authentication failed.

Current honest inventory state:

| Metric | Status |
|---|---:|
| Production-only tools | 103 |
| Named deeper-inspection entries | 20 |
| Not locally enumerated entries | 83 |
| Known critical lineage gaps | 16 |
| Live runtime enumeration completed | No |
| Runtime mutation performed | No |

Local default enumeration result:

```text
V7 runtime tool enumeration (read-only)
total_v7_tools=0 production_only=0 repo_present=0
known_deeper_inspection_entries_found=0
must_be_release_owned=0 operator_only_optional=0 safe_archive_candidate_future=0
warning=No runtime tools found in supplied runtime dirs. Run on VPS or provide mounted/copied runtime directory.
```

This is expected locally because the workstation does not contain the VPS `/usr/local/bin/v7*` runtime inventory.

## 2. Newly Enumerated Tools

No new live VPS tools were enumerated in this pass.

Reason:

```text
root@195.2.79.116: Permission denied (publickey,password).
```

No tool names were invented or guessed to hide the gap.

## 3. Updated Governance Classification

New read-only tooling:

```text
tools/v7-runtime-tool-enumerate
```

The enumerator assigns:

- `authoritative_runtime` when systemd references are found;
- `repo_missing_critical` for routing, autoswitch, identity, policy, Direct/RU-adjacent, and provisioning-like missing tools;
- `repo_missing_noncritical` for backup/rollback or referenced noncritical helpers;
- `operator_local_helper` for read-only/manual diagnostics with no runtime binding;
- `legacy_runtime_drift` for unreferenced runtime-local tools;
- `runtime_local_pending_lineage` for referenced runtime-local tools that still need ownership and release decisions.

Because live enumeration failed, these classifications are not yet applied to the remaining 83 tools.

## 4. Runtime Criticality Expansion

The enumerator maps tools into:

- datapath-critical;
- autoswitch-critical;
- provisioning-critical;
- identity-critical;
- observability-only;
- rollback-only;
- dormant/legacy;
- operator-convenience;
- runtime-critical when bound by systemd.

Current status:

```text
criticality expansion model: implemented
live criticality expansion for 83 tools: not completed
```

## 5. Release Relevance Expansion

Release relevance model implemented:

- `must_be_release_owned`;
- `runtime_local_allowed`;
- `operator_only_optional`;
- `safe_archive_candidate_future`.

Current release relevance status:

| Area | Status |
|---|---|
| Known 20 production-only tools | Already governed from Track 7.2 |
| Remaining 83 production-only tools | Still unresolved |
| Release ownership boundary | Tooling supports it |
| Commercial reproducibility impact | Still medium/high risk |

## 6. Provenance Confidence Map

The enumerator assigns confidence:

- `high`: repo-present and systemd-bound;
- `medium`: systemd-bound, referenced, or repo-present;
- `low`: likely legacy drift;
- `unknown`: no clear repo/runtime/reference evidence.

Current result:

```text
confidence model: implemented
confidence ranking for remaining 83: blocked by live enumeration access
```

## 7. Repo Convergence Priorities

Safest-first order remains:

1. Audit/state support tools:
   - `v7-audit-log`;
   - `v7-state-json`;
   - `v7-user-desired-state`;
   - `v7-switch-log`.
2. Identity/profile support:
   - `v7-user-reissue-config`;
   - `v7-user-rotate-key`.
3. Routing/reconcile support:
   - `v7-user-reconcile-apply`;
   - `v7-users-rebalance`;
   - `v7-users-rebalance-dry-run`.
4. Proxy/profile public tools.
5. Read-only operator utilities.
6. Remaining 83 only after live enumeration names them.

No convergence/import was performed in Track 7.3.

## 8. Governance UX Summary

Current calm operator summary:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 103
Named lineage gaps: 20
Critical known lineage gaps: 16
Unlisted lineage gaps: 83
Runtime inventory ambiguity: unresolved
Next evidence required: read-only VPS enumeration or copied runtime tool tree
```

## 9. Exact Files / Tools / Docs Changed

Created:

```text
tools/v7-runtime-tool-enumerate
docs/track7/LIVE_RUNTIME_ENUMERATION.md
TRACK7_3_LIVE_RUNTIME_ENUMERATION_REPORT.md
```

Updated:

```text
tools/v7-runtime-repo-diff
```

Existing compile gate already includes:

```text
tools/v7-runtime-tool-enumerate
```

## 10. Verification Results

Read-only SSH access test:

```text
ssh -o BatchMode=yes -o ConnectTimeout=8 root@195.2.79.116 true
root@195.2.79.116: Permission denied (publickey,password).
```

Local enumerator default:

```text
total_v7_tools=0
production_only=0
warning=No runtime tools found in supplied runtime dirs. Run on VPS or provide mounted/copied runtime directory.
```

Local enumerator against repo `tools/` for tool validation:

```text
total_v7_tools=28
production_only=0
repo_present=28
```

Governance diff after update:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 103
Named lineage gaps: 20
Critical lineage gaps (known): 16
Unlisted lineage gaps: 83
Safe convergence candidates (known): 4
```

## 11. Remaining Unresolved Lineage Blockers

Critical:

- 83 production-only tools remain anonymous locally;
- no per-tool hashes/modes/mtimes for those 83;
- no release relevance classification for those 83;
- no provenance confidence for those 83;
- no repo convergence decision can be made safely for those 83.

Commercial impact:

- release provenance remains partial;
- deployment reproducibility remains medium/high risk;
- commercial-grade release ownership is not yet complete.

## 12. Runtime Inventory Ambiguity Verdict

Runtime inventory ambiguity is **not resolved**.

Track 7.3 improved the tooling and the governance path, but did not complete live enumeration because SSH authentication blocked read-only access. The next safe step is to run:

```bash
tools/v7-runtime-tool-enumerate --references > runtime-enumeration.json
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
```

on the VPS, or provide a copied read-only runtime tree for local enumeration.
