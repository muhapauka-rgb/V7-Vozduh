# V7 Vozduh — Track 7.2 Production-Only Tool Governance & Lineage Resolution Report

Generated: 2026-05-23

## Scope

Track 7.2 created a production-only governance layer.

No runtime tools were imported.
No runtime tools were deleted or archived.
No deployment sync was performed.
No routing/datapath/autoswitch/Trusted RU/Gosuslugi behavior was touched.

## 1. Expanded Governance Inventory

Created:

- `docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md`
- `tools/v7-runtime-repo-diff`

Known state:

| Metric | Count |
|---|---:|
| Unknown active-like runtime tools | 117 |
| Repo-known unknown tools | 14 |
| Production-only unknown tools | 103 |
| Referenced unknown tools | 90 |
| Unreferenced unknown tools | 27 |
| Known deeper-inspection entries available locally | 20 |
| Not locally enumerated production-only tools | 83 |

Important constraint:

Track 7.2 does not invent names for the 83 unlisted tools. They remain governed as an aggregate until live manifest import or read-only VPS enumeration is available.

## 2. Governance Taxonomy

Finalized classes:

| Class | Operational Rule |
|---|---|
| `authoritative_runtime` | Must be release-owned; cleanup forbidden without replacement release. |
| `runtime_local_pending_lineage` | Temporarily accepted; must gain owner/role/hash or be imported. |
| `runtime_generated` | Link generator and inputs; do not hand-edit. |
| `legacy_runtime_drift` | Freeze; archive only in dedicated cleanup block. |
| `operator_local_helper` | Document allowed use; keep out of automated dependency chains. |
| `repo_missing_critical` | Highest import/rewrite priority. |
| `repo_missing_noncritical` | Import later or mark runtime-local. |
| `safe_archive_candidate` | Archive-only candidate after verification; never delete. |

## 3. Runtime Criticality Map

Criticality classes:

- datapath-critical;
- autoswitch-critical;
- provisioning-critical;
- identity-critical;
- observability-only;
- operator convenience;
- rollback-only;
- dormant/legacy.

Known critical lineage gaps from local data:

- 16 of the 20 named deeper-inspection tools are `must_resolve_for_release`;
- 4 are `optional_or_operator_local`;
- 83 remain unknown/unlisted and require live evidence.

Examples of must-resolve tools:

- `v7-audit-log`
- `v7-state-json`
- `v7-user-desired-state`
- `v7-user-reconcile-apply`
- `v7-user-reissue-config`
- `v7-user-rotate-key`
- `v7-users-rebalance`
- proxy public mutation/render tools.

## 4. Repo Convergence Strategy

Safest-first sequence:

1. Audit/state support:
   - `v7-audit-log`;
   - `v7-state-json`;
   - `v7-user-desired-state`;
   - `v7-switch-log`.
2. Identity/profile:
   - `v7-user-reissue-config`;
   - `v7-user-rotate-key`.
3. Routing/reconcile/rebalance:
   - `v7-user-reconcile-apply`;
   - `v7-users-rebalance`;
   - keep `v7-users-rebalance-dry-run` as planning utility.
4. Proxy/profile public tools:
   - render;
   - enable/disable;
   - canary;
   - service render.
5. Observability/read-only helpers:
   - import later or mark `operator_local_helper`.
6. Remaining 83:
   - require live manifest import or read-only VPS enumeration before per-tool decisions.

Explicitly rejected:

- mass-import all 103 tools;
- cleanup by filename pattern;
- force runtime/repo sync.

## 5. Runtime Ownership Model

Defined owners:

| Owner | Scope |
|---|---|
| `safety` | kill switch/no-leak/route safety verification |
| `routing` | user assignment, route tables, rebalance, reconcile |
| `autoswitch` | guarded switching, anti-flap, capacity/safety memory |
| `provisioning` | egress lifecycle, drafts, enable/disable, rollback |
| `identity/profile` | identity DB, devices, profile delivery, key rotation |
| `policy` | global/org policy and Direct/RU-adjacent policy |
| `observability` | summaries, service matrix, diagnostics, operator truth |
| `audit/runtime` | audit events, switch logs, actor/reason traceability |
| `admin` | admin API, safe-run, operator workflows |
| `security` | secret cleanup and sensitive-state warnings |

Each runtime tool must eventually declare:

- owner;
- maintainer;
- mutation level;
- state reads/writes;
- release relevance;
- verification required.

## 6. Release Relevance Classification

Defined:

- `must_be_release_owned`;
- `runtime_local_allowed`;
- `generated_runtime`;
- `operator_only_optional`;
- `archive_candidate_future`.

Current local classification:

```text
must_resolve_for_release: 16 known tools
optional_or_operator_local: 4 known tools
unlisted_lineage_gaps: 83
```

Commercial release boundary:

- mutation/identity/provisioning/policy/runtime support tools cannot remain unknown;
- operator-local tools can remain outside package only if owner/purpose are documented.

## 7. Optional Diff Tooling

Created:

- `tools/v7-runtime-repo-diff`

Behavior:

- read-only;
- compares local repo V7 files against release `production-only-tools.json`;
- optionally accepts a runtime manifest;
- emits governance classes and convergence recommendations;
- prints calm operator summary.

It does not:

- import;
- delete;
- sync;
- chmod/chown;
- require runtime access.

Observed pretty output:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 103
Critical lineage gaps (known): 16
Unlisted lineage gaps: 83
Safe convergence candidates (known): 4
warnings:
  - unlisted_production_only_tools_require_live_manifest
  - runtime_manifest_not_supplied
```

## 8. Governance UX Summary

Recommended calm summary:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 103
Critical lineage gaps: 16 known + 83 unlisted
Safe convergence candidates: 4 known
Next action: import/govern audit/state/identity/routing support tools first
```

Avoid:

- raw filesystem walls;
- per-file noise by default;
- greenwashing incomplete lineage.

## 9. Exact Files / Tools / Docs Created

Created:

- `tools/v7-runtime-repo-diff`
- `docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md`
- `TRACK7_2_PRODUCTION_ONLY_TOOL_GOVERNANCE_REPORT.md`

Changed:

- `tools/v7-run-tests`
  - now compiles `tools/v7-runtime-repo-diff`.

No runtime files changed.

## 10. Verification Results

Command:

```bash
tools/v7-run-tests
```

Result:

- PASS;
- 28 tests discovered and passed;
- py_compile OK.

Command:

```bash
tools/v7-runtime-repo-diff --pretty
```

Result:

- PASS;
- read-only governance summary emitted.

Command:

```bash
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py admin_core/events.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff
```

Result:

- PASS.

Live VPS verification:

- not performed;
- no live mutation attempted.

## 11. Remaining Reproducibility Blockers

1. 83 production-only tools are still not locally enumerated.
2. 16 known tools require lineage resolution before commercial release trust.
3. Runtime manifest is still linked by VPS path, not locally imported.
4. Source worktree is dirty.
5. No clean import/convergence workflow exists yet.

## 12. Recommended Next Governance Priorities

1. Import or read-only enumerate the live runtime manifest so the remaining 83 tools can be named.
2. Start with audit/state support tools:
   - `v7-audit-log`;
   - `v7-state-json`;
   - `v7-user-desired-state`;
   - `v7-switch-log`.
3. Then resolve identity/profile and routing mutation tools.
4. Keep Direct/RU, Trusted RU, autoswitch and datapath-adjacent tools under stricter owner review.
5. Do not archive anything until governance status becomes `safe_archive_candidate`.

## Final Verdict

Track 7.2 improves governance and lineage clarity, but does not resolve all production-only lineage.

Current honest state:

```text
runtime governance: partial
production-only tools: 103
known critical lineage gaps: 16
unknown/unlisted lineage gaps: 83
commercial reproducibility: still incomplete
```
