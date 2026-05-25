# V7 Vozduh — Track 7.1 First Actual Release Manifest Object Report

Generated: 2026-05-23

## Scope

Track 7.1 created the first actual release manifest object.

No runtime sync was performed.
No production-only tools were imported or deleted.
No deployment model was changed.
No routing/datapath/autoswitch/Trusted RU/Gosuslugi behavior was touched.

## 1. Release Object Structure

Created directory:

```text
releases/v7-runtime-20260523T174503Z/
```

Files:

- `release-manifest.json`
- `release-summary.md`
- `verification.json`
- `warnings.json`
- `runtime-linkage.json`
- `production-only-tools.json`

The object is a provenance snapshot, not a deploy artifact.

## 2. Runtime Lineage References

Linked Block 3.1 deploy baseline:

- `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/checksums.sha256`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/unit-summary.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/contract-summary.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/runtime-summary.md`

Linked Block 3.2 archive:

- `/root/v7-backups/usr-local-bin-archive/20260523T122936Z/archive-manifest.json`

Linked Block 3.4 archive:

- `/root/v7-backups/usr-local-bin-archive/20260523T124646Z/archive-manifest.json`

Linked repo governance:

- `docs/track7/RELEASE_LINEAGE_AND_PROVENANCE.md`
- `docs/track4/RUNTIME_GOVERNANCE_REGISTRY.md`
- `docs/track5/endpoint-inventory.json`
- `docs/track5/EXTRACTION_GATE.md`
- `docs/track6/SENSITIVE_STATE_ACCESS_MAP.md`

No giant runtime snapshots were copied into the repo.

## 3. Source Snapshot

Captured:

- branch: `codex/integratsiya-tunelya`
- commit: `a0e689c67ef7d47e7f04e5c30e5430acd05752cb`
- dirty: `true`
- initial status lines observed: `53`
- validation status lines observed after release object creation: `55`

This is not a clean production release commit.

The release object intentionally records dirty-state risk rather than pretending the source tree is clean.

## 4. Production-Only Snapshot

Known state from Block 3.3:

| Class | Count |
|---|---:|
| Unknown active-like tools | 117 |
| Repo-known unknown tools | 14 |
| Production-only unknown tools | 103 |
| Referenced unknown tools | 90 |
| Unreferenced unknown tools | 27 |

`production-only-tools.json` records:

- aggregate counts;
- governance classes;
- default lineage status: `runtime_local_pending_lineage`;
- 20 named deeper-inspection tools from Block 3.3;
- 83 unlisted production-only tools as `not_locally_enumerated`.

Important honesty note:

Track 7.1 cannot claim per-tool lineage for all 103 tools because the live runtime manifest is linked by reference and not locally available. This remains a release warning and reproducibility blocker.

## 5. Verification Snapshot

Local verification:

```bash
tools/v7-run-tests
```

Result:

- PASS;
- 28 tests discovered and passed;
- py_compile OK.

Release object validation:

```bash
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty
```

Result:

- release object ready: `true`;
- missing required files: `0`;
- warnings remain:
  - runtime manifest missing locally / not supplied;
  - source worktree dirty;
  - known 103 production-only tools require lineage;
  - archive manifests missing locally / not supplied.

Compile:

```bash
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/sanitize.py admin_core/time.py admin_core/registry_readers.py admin_core/events.py tools/v7-release-lineage-check
```

Result:

- PASS.

Live runtime verification:

- not run in Track 7.1;
- no live mutation was performed;
- live checks must be run before any deploy acceptance.

## 6. Warning / Risk Model

Release object warnings:

- `source_worktree_dirty`
- `103_production_only_tools_pending_lineage`
- `runtime_manifest_not_copied_locally`
- `live_runtime_checks_not_run`
- `sensitive_state_hardening_pending`
- `admin_monolith_coupling_risk`

These warnings are not cosmetic. They define the remaining release trust boundary.

## 7. Runtime Linkage Summary

```text
Runtime baseline: linked
Archive lineage: linked
Endpoint inventory: linked
Extraction gate: linked
Production-only lineage: incomplete
Deployment reproducibility: medium/high risk
```

## 8. Exact Files Created

Created:

- `releases/v7-runtime-20260523T174503Z/release-manifest.json`
- `releases/v7-runtime-20260523T174503Z/release-summary.md`
- `releases/v7-runtime-20260523T174503Z/verification.json`
- `releases/v7-runtime-20260523T174503Z/warnings.json`
- `releases/v7-runtime-20260523T174503Z/runtime-linkage.json`
- `releases/v7-runtime-20260523T174503Z/production-only-tools.json`
- `TRACK7_1_FIRST_RELEASE_OBJECT_REPORT.md`

Changed:

- `tools/v7-release-lineage-check`
  - added `--release-dir` validation support.

## 9. Validation Results

Release object validation:

```text
release_object=releases/v7-runtime-20260523T174503Z ready=True missing=0
```

JSON load validation:

- all required release JSON files load successfully through `tools/v7-release-lineage-check`.

Local test/compile gate:

- PASS.

## 10. Whether Release Object Is Operationally Trustworthy

Operationally useful: yes.

Why:

- it links the current known runtime baseline;
- it links archive lineage;
- it links endpoint inventory and extraction gate;
- it records source state and verification results;
- it makes warnings explicit instead of hiding them.

Commercial release trustworthy: partial only.

Why not complete:

- source tree is dirty;
- 103 production-only tools still lack full repo lineage;
- live manifests are linked by path, not locally imported;
- live runtime checks were not run for this Track;
- sensitive-state hardening remains pending.

## 11. Remaining Reproducibility Blockers

1. Import or govern all 103 production-only tools.
2. Import/copy or read-only validate live runtime manifest into release object context.
3. Create a clean source commit for future release objects.
4. Run live runtime verification before marking any release deploy-accepted.
5. Continue sensitive-state hardening after service-user confirmation.
6. Keep admin monolith containment under endpoint contract gate.

## Final Verdict

Track 7.1 achieved the first actual release object.

It reduces deployment ambiguity, but it does not make V7 fully reproducible yet.

The honest status is:

```text
release object: present
runtime lineage: linked
release provenance: partial
production-only lineage: incomplete
commercial reproducibility: not yet
```
