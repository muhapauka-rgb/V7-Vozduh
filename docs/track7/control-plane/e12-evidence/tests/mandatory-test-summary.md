# E12 Mandatory Test Summary

All E12 mandatory tests completed.

## Passed

- `tools/v7-run-tests`: PASS, 96 tests.
- Targeted reservation / diagnose / autoswitch policy / restore barrier /
  restore-settle / target-readiness / planner/apply generation /
  delayed-movement / replay-resistance tests: PASS, 47 tests.
- `py_compile` for Python governance tools: PASS.
- `bash -n` for relevant shell scripts: PASS.
- `tools/v7-control-plane-governance-check --pretty`: PASS.
- `tools/v7-second-canary-target-readiness --pretty`: PASS.
- `tools/v7-second-canary-target-readiness --json`: PASS.
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS.
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS.
- `tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`: PASS with known partial-lineage warnings.
- `tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`: PASS with known partial-lineage warnings.
- `git diff --check`: PASS.

## Known Warnings

- Runtime/repo convergence remains partial.
- Release lineage remains partial because the runtime manifest is not supplied
  locally and the source worktree is dirty.

These warnings are documented blockers for productization, not regressions from
E12 generation-token hardening.
