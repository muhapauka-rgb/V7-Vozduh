# E11.18 Mandatory Test Summary

## Passed

- `tools/v7-run-tests`: PASS, 91 tests.
- Targeted autoswitch, diagnose, restore-settle, and target-readiness tests:
  PASS, 42 tests.
- `tools/v7-control-plane-governance-check --pretty`: PASS.
- `tools/v7-second-canary-target-readiness --pretty`: PASS, WireGuard target
  GO, execution still false.
- `tools/v7-second-canary-target-readiness --json`: PASS.
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS, gate GO.
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS, gate GO.
- `tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`:
  PASS with known partial-lineage warnings only.
- `tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`:
  PASS with known dirty-worktree/runtime-manifest warnings only.
- `py_compile` for governance/autoswitch/readiness/restore-settle tools:
  PASS.
- `bash -n tools/v7-run-tests tools/v7-egress-diagnose`: PASS.
- `git diff --check`: PASS.
- Credential leak scan across E11.18 report/evidence/touched tools/docs: PASS.

## Read-Only Note

E11.18 did not run live `v7-users-autoswitch` on runtime state because that
planner persists dynamic load summary even without `--apply`. Current selected
moves were computed on a local copy of `/opt/v7/egress/state`.
