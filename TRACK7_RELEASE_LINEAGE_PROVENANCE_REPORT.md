# V7 Vozduh — Track 7 Release Lineage, Runtime Provenance & Reproducibility Foundation Report

Generated: 2026-05-23

## Scope

Track 7 created a release lineage and runtime provenance foundation.

No deployment rewrite was performed.
No CI/CD was introduced.
No runtime files were synced, deleted, archived, chmodded, or chowned.
No routing/datapath/autoswitch/Trusted RU/Gosuslugi logic was touched.

## 1. Runtime Provenance Model

Created:

- `docs/track7/RELEASE_LINEAGE_AND_PROVENANCE.md`

Core vocabulary:

| Term | Meaning |
|---|---|
| `release` | Reviewable deployment unit linking source, runtime manifest, verification, rollback material, and warnings. |
| `release_id` | Stable runtime state identifier: `v7-runtime-YYYYMMDDTHHMMSSZ`. |
| `runtime_baseline` | Point-in-time snapshot of live runtime files, systemd bindings, checksums, state contracts, warnings. |
| `deployment_snapshot` | Manifest artifacts such as `manifest.json`, `checksums.sha256`, `unit-summary.json`, `contract-summary.json`. |
| `archive_lineage` | Mapping from archived files to original paths, hashes, mtimes, archive reason, and baseline reference. |
| `production_only_tool` | Runtime executable present on VPS but missing from repo by basename. Not automatically obsolete. |
| `authoritative_executable` | Runtime executable proven active through systemd, shell-loop, admin subprocess, or operator workflow binding. |
| `runtime_generated_artifact` | Rebuildable runtime output generated from authoritative state. |
| `state_authoritative` | Live state that must survive deploys and must not be overwritten from repo. |
| `runtime_local_pending_lineage` | Temporary state for runtime-local tools that need ownership/provenance before release confidence. |

## 2. Release Manifest Specification

Defined in `docs/track7/RELEASE_LINEAGE_AND_PROVENANCE.md`.

Minimal release manifest fields:

- `schema_version`
- `release_id`
- `generated_at`
- `source`
  - repo URL;
  - branch;
  - commit;
  - dirty state;
  - source snapshot notes.
- `runtime`
  - host;
  - runtime manifest;
  - checksums;
  - unit summary;
  - contract summary.
- `archives`
  - stale executable archive manifest;
  - suspicious executable archive manifest.
- `active_executables`
- `runtime_contracts`
- `known_production_only_tools`
- `verification`
- `rollback`
- `warnings`

This is a specification only, not a release system rollout.

## 3. Production-Only Governance Map

Known baseline from Block 3.3:

| Class | Count |
|---|---:|
| Unknown active-like tools | 117 |
| Runtime unknown tools also present in repo | 14 |
| Production-only unknown tools not present in repo | 103 |
| Referenced unknown tools | 90 |
| Unreferenced unknown tools | 27 |

Governance classes:

- `intentional_runtime_local`
- `missing_from_repo`
- `generated`
- `operator_local`
- `legacy_drift`
- `runtime_specific`
- `should_be_imported_to_repo`

Important rule:

`production_only` does not mean obsolete. It means not reproducible from repo until ownership/provenance is established.

## 4. Runtime ↔ Repo Linkage Analysis

Current linkage states defined:

- `repo_source_exact`
- `repo_source_diverged`
- `production_only_known`
- `generated_from_repo`
- `runtime_local_pending_lineage`
- `unknown_blocker`

Current known reality:

- Block 3.1 runtime baseline exists.
- Block 3.2 and Block 3.4 archive manifests exist on VPS.
- Local repo contains a growing but incomplete subset of V7 tools.
- 103 production-only tools still lack clean repo lineage.
- A rebuild from repo alone is not currently credible.

Local checker inventory:

```text
repo v7 files: 44
tools: 26
hardening: 8
systemd: 9
admin: 1
```

Local checker could not load live runtime manifest because `/opt/v7/ops/deploy-baseline/...` is not present on the local workstation.

## 5. Reproducibility Blocker Analysis

| Blocker | Severity | Explanation |
|---|---|---|
| 103 production-only tools | High | Runtime behavior cannot be rebuilt from repo alone. |
| No accepted release object | High | Baseline exists, but no release manifest owns source/runtime/archive/verification together. |
| Dirty source tree | Medium/high | Current repo state is not represented by a clean commit/release ID. |
| Hidden PATH dependencies | High | Admin/operator workflows can call `v7-*` tools not visible from systemd alone. |
| Runtime-local manual edits | High | VPS state may contain operational code not reviewable from repo. |
| Sensitive-state hardening pending | Medium/high | Commercial posture is not yet hardened. |

Commercial risk:

- rollback trust is improved but incomplete;
- onboarding/commercial deployments cannot yet claim reproducible release lineage;
- support/debug depends on runtime filesystem knowledge.

## 6. Release Verification Gate

Defined gate:

1. Runtime manifest exists.
2. Checksums exist.
3. Archive manifests are linked.
4. `tools/v7-run-tests` passes.
5. `py_compile` passes.
6. Endpoint inventory counts remain unchanged unless intentionally changed.
7. Runtime governance registry is updated.
8. Production-only tools are classified or marked `runtime_local_pending_lineage`.
9. Sensitive-state warning posture is reviewed.
10. No live deploy without explicit approval and rollback plan.
11. If deployed, live verification passes:
    - `systemctl --failed`
    - `v7-killswitch-check`
    - `v7-user-route-check`
    - `v7-provisioning-reconcile-check`
    - `v7-observability-summary --pretty`

## 7. Optional Provenance Validator

Created:

- `tools/v7-release-lineage-check`

Behavior:

- read-only;
- inspects git commit/branch/dirty state;
- counts repo-side V7 files;
- optionally loads runtime manifest;
- optionally links archive manifests;
- emits release gate blockers;
- prints calm operator summary.

It does not:

- deploy;
- sync runtime to repo;
- delete files;
- chmod/chown;
- restart services.

Local observed output:

```text
runtime_manifest=/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json exists=False
production_only_tools=103
runtime_lineage=partial
release_provenance=incomplete
warnings:
  - runtime_manifest_missing_locally_or_not_supplied
  - source_worktree_dirty
  - known_103_production_only_tools_require_lineage
  - archive_manifest_missing_locally_or_not_supplied
```

These warnings are expected locally because the live VPS manifests are not present on the workstation.

## 8. Operator Runtime Trust Model

Recommended calm summary:

```text
Runtime lineage: partial
Release provenance: incomplete
Production-only tools: 103
Runtime baseline: verified from Block 3.1
Deployment reproducibility: medium/high risk
Next safe action: classify/import production-only tools, do not sync blindly
```

Do not show:

- giant filesystem dumps;
- raw manifest walls;
- per-file noise by default.

## 9. Exact Files / Tools / Docs Created

Created:

- `tools/v7-release-lineage-check`
- `docs/track7/RELEASE_LINEAGE_AND_PROVENANCE.md`
- `TRACK7_RELEASE_LINEAGE_PROVENANCE_REPORT.md`

Changed:

- `tools/v7-run-tests`
  - now compiles `tools/v7-sensitive-state-check`;
  - now compiles `tools/v7-release-lineage-check`.

No runtime files changed.

## 10. Verification Results

Command:

```bash
tools/v7-run-tests
```

Result:

- OK;
- 28 tests discovered and passed;
- py_compile OK.

Command:

```bash
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py admin_core/events.py tools/v7-release-lineage-check
```

Result:

- OK.

Command:

```bash
tools/v7-release-lineage-check --pretty
```

Result:

- OK;
- read-only warnings emitted;
- no mutation.

Live VPS verification:

- not performed in Track 7;
- previous Track 6 BatchMode SSH read-only attempt failed authentication;
- no live changes were attempted.

## 11. Remaining Commercial Blockers

1. No accepted release manifest object yet.
2. 103 production-only runtime tools still lack repo lineage.
3. Runtime manifest/archive manifests are on VPS, not mirrored into repo-local release object.
4. Source tree is dirty, so current repo state is not a clean release.
5. Sensitive-state hardening remains dry-run only.
6. No runtime-to-repo convergence workflow exists yet.

## 12. Recommended Next Platform-Evolution Priorities

1. Create the first actual release manifest object referencing:
   - Block 3.1 baseline;
   - Block 3.2 archive;
   - Block 3.4 archive;
   - current verification status.
2. Import or explicitly govern production-only tools by priority:
   - referenced by admin/API;
   - mutating runtime;
   - provisioning/identity/policy related;
   - rollback/safety related.
3. Mark all remaining production-only tools as `runtime_local_pending_lineage` until resolved.
4. Keep deploy model file-based for now.
5. Do not introduce CI/CD or packaging before provenance is reliable.

## Final Verdict

Track 7 improves release explainability, but does not make deployment fully reproducible yet.

V7 now has:

- a provenance vocabulary;
- a release manifest spec;
- a release verification gate;
- a read-only lineage checker;
- a clear production-only tool governance model.

V7 still does not have:

- a clean release object;
- full repo/runtime convergence;
- reproducible rebuild from repo alone.

That is the honest current state.
