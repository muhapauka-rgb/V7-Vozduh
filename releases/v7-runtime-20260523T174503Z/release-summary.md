# V7 Release Snapshot — v7-runtime-20260523T174503Z

This is the first actual V7 release manifest object.

It is not a deploy.
It is not CI/CD.
It is not a package boundary.

It is an honest provenance snapshot linking current source state, known runtime baselines, archive lineage, endpoint inventory, extraction gate, and known reproducibility warnings.

## Structure

Files:

- `release-manifest.json`
- `release-summary.md`
- `verification.json`
- `warnings.json`
- `runtime-linkage.json`
- `production-only-tools.json`

## Runtime Lineage References

Linked runtime baseline:

- `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/checksums.sha256`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/unit-summary.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/contract-summary.json`

Linked archives:

- `/root/v7-backups/usr-local-bin-archive/20260523T122936Z/archive-manifest.json`
- `/root/v7-backups/usr-local-bin-archive/20260523T124646Z/archive-manifest.json`

Linked repo governance:

- `docs/track7/RELEASE_LINEAGE_AND_PROVENANCE.md`
- `docs/track4/RUNTIME_GOVERNANCE_REGISTRY.md`
- `docs/track5/endpoint-inventory.json`
- `docs/track5/EXTRACTION_GATE.md`
- `docs/track6/SENSITIVE_STATE_ACCESS_MAP.md`

## Source Snapshot

- Branch: `codex/integratsiya-tunelya`
- Commit: `a0e689c67ef7d47e7f04e5c30e5430acd05752cb`
- Dirty: `true`
- Git status lines observed: `53`

Dirty-state note:

The release object captures ongoing V7 stabilization/containment/governance work. It is not a clean production release commit.

## Production-Only Snapshot

Known from Block 3.3:

- unknown active-like tools: `117`
- repo-known unknown tools: `14`
- production-only unknown tools: `103`
- referenced unknown tools: `90`
- unreferenced unknown tools: `27`

Per-tool names are only partially available locally. The 20 deeper-inspection tools are listed in `production-only-tools.json`; the remaining 83 require live manifest import or VPS read-only enumeration.

## Verification Snapshot

Local:

- `tools/v7-run-tests`: PASS, 28 tests and py_compile OK.
- `tools/v7-release-lineage-check --pretty`: PASS_WITH_WARNINGS.

Live:

- Not run in Track 7.1.

No live runtime mutation was performed.

## Runtime Linkage Summary

```text
Runtime baseline: linked
Archive lineage: linked
Endpoint inventory: linked
Extraction gate: linked
Production-only lineage: incomplete
Deployment reproducibility: medium/high risk
```

## Warning Model

Major warnings:

- dirty source tree;
- 103 production-only tools pending lineage;
- runtime manifests are linked by VPS path, not copied locally;
- live runtime checks not run;
- sensitive-state hardening pending;
- admin monolith coupling risk remains.

## Trust Verdict

Operationally useful: yes.

Commercial-release trustworthy: partial.

This object reduces deployment ambiguity, but it does not yet prove reproducible deployment. The main blocker remains production-only runtime tooling without repo lineage.
