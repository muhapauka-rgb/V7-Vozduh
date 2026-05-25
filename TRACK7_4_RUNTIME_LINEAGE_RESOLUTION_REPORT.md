# V7 Vozduh — Track 7.4 Runtime Lineage Resolution & Authoritative Runtime Enumeration Report

## 1. Runtime Enumeration Result

Authoritative live runtime enumeration was completed on VPS `195.2.79.116`.

Artifacts returned into the local workspace:

```text
runtime-enumeration.json
runtime-repo-diff.txt
runtime-repo-diff.remote.txt
```

Remote artifacts were also written on the VPS:

```text
/root/runtime-enumeration.json
/root/runtime-repo-diff.txt
```

No runtime cleanup, import, archive, chmod/chown, service restart, datapath change, routing change, autoswitch change, or Trusted RU/Gosuslugi change was performed.

## 2. Newly Named Tools

Live enumeration found:

```text
Total /usr/local/bin/v7* tools: 141
Repo-present by basename: 23
Runtime-only by basename: 118
Anonymous lineage gaps: 0
```

This supersedes the older planning estimate of 103 production-only tools. The previous `83 anonymous gaps` are now resolved as named runtime inventory, but the live truth shows a larger runtime/repo divergence: `118` runtime-only tools.

First runtime-only names:

```text
v7-admin-auth-init
v7-admin-auth-status
v7-admin-password-rotate
v7-api
v7-app-domain-trace
v7-audit-log
v7-capacity-check
v7-capacity-readiness
v7-decide-egress
v7-direct-add-domain
v7-direct-auto-sync
v7-direct-exclude-add-domain
v7-direct-exclude-refresh
v7-direct-list
v7-direct-refresh-domains
v7-direct-remove-domain
v7-direct-status
v7-egress-benchmark-all
v7-egress-diagnose
v7-egress-draft-runtime-helper
v7-egress-guard
v7-egress-history
v7-egress-load
v7-egress-namespace-check
v7-egress-speedtest
v7-egress-stability
v7-installer-check
v7-ipam-allocate
v7-ipam-preview
v7-killswitch-disable-temporary
v7-killswitch-status
v7-log-maintenance-status
v7-maintenance-cleanup-apply
v7-maintenance-cleanup-preview
v7-mss-clamp-enable
v7-node-config-check
v7-node-env
v7-path-sanity-check
v7-policy-apply
v7-policy-apply-systemd
```

Full per-tool metadata is in `runtime-enumeration.json`.

## 3. Updated Governance Inventory

Repo-aware local diff result:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 118
Named lineage gaps: 118
Critical lineage gaps (known): 75
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
```

The `unlisted lineage gaps` category is now closed.

## 4. Runtime Criticality Resolution

For the 118 runtime-only tools:

```text
autoswitch-critical: 2
datapath-critical: 5
identity-critical: 7
observability-only: 20
operator-convenience: 59
provisioning-critical: 5
rollback-only: 3
runtime-critical: 17
```

Important: `operator-convenience` does not mean safe to delete. It means no immediate datapath-critical classification was inferred from name/reference heuristics. Cleanup still requires a separate dedicated verification block.

## 5. Release Relevance Resolution

For the 118 runtime-only tools:

```text
must_be_release_owned: 75
runtime_local_allowed: 43
```

No `safe_archive_candidate_future` was identified by the live/reference pass.

## 6. Provenance Confidence Map

For the 118 runtime-only tools:

```text
high: 17
medium: 101
```

There were no `low` or `unknown` confidence runtime-only tools in this pass because every runtime-only tool had either systemd/reference evidence or a medium-confidence classification path.

## 7. Runtime ↔ Repo Divergence Report

Current real divergence:

```text
Total runtime v7 tools: 141
Repo-present by basename: 23
Runtime-only by basename: 118
```

Governance classes for runtime-only tools:

```text
authoritative_runtime: 17
repo_missing_critical: 53
repo_missing_noncritical: 17
runtime_local_pending_lineage: 31
```

This means runtime/repo divergence is larger than the old release object suggested. Track 7.4 improved visibility, not reproducibility itself.

## 8. Convergence Readiness Ranking

Safest-first convergence order:

1. Audit/state support:
   - `v7-audit-log`;
   - state/switch/log helpers from the runtime-only inventory.
2. Observability helpers:
   - capacity/readiness/status/check tools.
3. Identity/profile helpers:
   - auth/password/profile/reissue/rotate-related tools.
4. Routing/reconcile/policy helpers:
   - `v7-decide-egress`;
   - Direct/RU and policy tools;
   - reconcile/switch/rebalance tools.
5. Provisioning/egress helpers:
   - egress draft/guard/history/load/stability tools.
6. Operator-local utilities:
   - installer, environment, review, maintenance preview tools.
7. Cleanup/archive decisions:
   - not allowed yet; no tool was classified as safe archive in this pass.

No convergence/import was performed.

## 9. Governance UX Summary

Updated calm operator summary:

```text
Runtime governance: partial but named
Runtime v7 tools: 141
Production-only/runtime-only tools: 118
Anonymous lineage gaps: 0
Critical unresolved lineage: 75
Release-owned required: 75
Runtime-local allowed pending governance: 43
Commercial reproducibility: still incomplete
```

## 10. Exact Files / Tools / Docs Changed

Created/returned artifacts:

```text
runtime-enumeration.json
runtime-repo-diff.txt
runtime-repo-diff.remote.txt
```

Updated locally:

```text
tools/v7-runtime-repo-diff
TRACK7_4_RUNTIME_LINEAGE_RESOLUTION_REPORT.md
```

Earlier Track 7.4 intake doc remains:

```text
docs/track7/RUNTIME_ENUMERATION_INTAKE.md
```

## 11. Verification Results

Remote read-only enumeration completed and produced:

```text
/root/runtime-enumeration.json 305K
/root/runtime-repo-diff.txt 850B
```

Local repo-aware diff:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 118
Named lineage gaps: 118
Critical lineage gaps (known): 75
Unlisted lineage gaps: 0
```

Local artifact sizes:

```text
runtime-enumeration.json 305K
runtime-repo-diff.txt 297B
runtime-repo-diff.remote.txt 850B
```

Live datapath checks were not run in this task because the user requested only runtime enumeration artifacts and no routing/datapath/autoswitch work.

## 12. Remaining Unresolved Lineage Blockers

Resolved:

- anonymous/unlisted lineage gaps;
- missing names for the former 83 anonymous production-only tools;
- lack of hashes/modes/mtimes/reference samples for runtime tools.

Still blocking commercial reproducibility:

- 118 runtime-only tools are not release-owned by repo;
- 75 runtime-only tools look release-relevant or critical;
- release object still references the older 103-tool estimate;
- runtime/repo convergence has not started;
- no safe archive candidates were proven;
- no deployment reproducibility guarantee exists yet.

## 13. Runtime Inventory Ambiguity Verdict

Runtime inventory ambiguity is **resolved at the naming/evidence level**.

It is **not resolved at the reproducibility/convergence level**.

Track 7.4 successfully converts anonymous gaps into named runtime inventory, but the result is not “green”: it reveals a larger divergence than expected and confirms that release lineage remains commercially incomplete.
