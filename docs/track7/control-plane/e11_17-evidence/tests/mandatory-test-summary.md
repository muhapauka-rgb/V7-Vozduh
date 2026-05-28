# E11.17 Mandatory Test Summary

## Passed

- `tools/v7-run-tests`: PASS, 91 tests.
- Targeted autoswitch, diagnose, restore-settle, and target-readiness tests:
  PASS, 42 tests.
- `tools/v7-control-plane-governance-check --pretty`: PASS.
- `tools/v7-second-canary-target-readiness --pretty`: PASS, target readiness
  GO for `wireguard-1779454504-c43409`, execution still false.
- `tools/v7-second-canary-target-readiness --json`: PASS.
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS, gate GO.
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS, gate GO.
- `tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`:
  PASS with known partial-lineage warnings only.
- `tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`:
  PASS with known dirty-worktree/runtime-manifest warnings only.
- `py_compile` for Python governance/autoswitch/readiness/restore-settle test
  tools: PASS.
- `bash -n tools/v7-run-tests tools/v7-egress-diagnose`: PASS.
- `git diff --check`: PASS.
- Credential leak scan across E11.17 report/evidence/touched tools/docs: PASS.

## Notes

`tools/v7-egress-diagnose` is a Bash script, not Python, so it is validated by
`bash -n` rather than `py_compile`.
