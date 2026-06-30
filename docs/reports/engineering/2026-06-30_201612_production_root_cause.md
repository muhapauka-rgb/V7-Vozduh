# Production Readiness Root Cause

Дата: 2026-06-30 20:16:12

## Symptoms

Production Phase stopped with `UNSAFE_DEPLOY`.

Reported blockers:

- `dirty_workspace`
- `runtime_critical_dirty`
- `local_remote_commit_mismatch`
- `runtime_local_commit_mismatch`
- `github_truth_check_failed`
- `production_runtime_not_at_deployable_current_truth`
- deployable mismatches:
  - `tools/v7-users-autoswitch`
  - `admin/v7-admin-api`

Earlier sandbox-only symptom:

- `github_remote_unreadable`
- `canonical_branch_missing_on_remote`

After network-enabled read-only verification, GitHub was readable and `origin/Updatesystem` existed.

## Grouped Symptoms

### Group 1: Local Source Truth Boundary

Symptoms:

- `dirty_workspace`
- `runtime_critical_dirty`
- local truth `NO-GO`
- safe deploy `github_truth_check_failed`

Immediate cause:

- Git worktree contains runtime-critical uncommitted deployable changes.

Root cause:

- L3 production candidate has not been sealed into a clean canonical source state.

Responsible owner:

- `tools/v7-truth-check`
- `tools/v7_sync_lib.classify_deployable_changes`
- canonical source branch: `Updatesystem`

Executable fix:

- Create one clean canonical production candidate commit containing the intended L3 deployable changes and required documentation/test evidence.

Verification:

- `tools/v7-truth-check --all --json`
- Expected local blockers removed:
  - `dirty_workspace`
  - `runtime_critical_dirty`

Expected result:

- Local truth can progress from `LOCAL_NO_GO` to local clean state.

### Group 2: Remote Truth Boundary

Symptoms:

- `local_remote_commit_mismatch`
- `github_truth_check_failed`
- GitHub truth `NO-GO`

Immediate cause:

- Local branch `Updatesystem` is at `ad773ab2ad37af6211d2df25122e32fea3542f90`.
- Remote `origin/Updatesystem` is at `0092efcb45fbde0493cc9c475b0dec1af21eec4f`.

Root cause:

- Canonical remote branch has not been advanced to the local production candidate.

Responsible owner:

- `tools/v7-truth-check.github_check`
- canonical remote: `https://github.com/muhapauka-rgb/V7-Vozduh.git`
- canonical branch: `Updatesystem`

Executable fix:

- Push the sealed production candidate commit to `origin/Updatesystem`.

Verification:

- `git ls-remote https://github.com/muhapauka-rgb/V7-Vozduh.git refs/heads/Updatesystem`
- `tools/v7-truth-check --all --json`

Expected result:

- GitHub truth no longer reports `local_remote_commit_mismatch`.

### Group 3: Production Runtime Boundary

Symptoms:

- `runtime_local_commit_mismatch`
- convergence `NOT_ALIGNED`
- `production_runtime_not_at_deployable_current_truth`
- deployable mismatches:
  - `tools/v7-users-autoswitch`
  - `admin/v7-admin-api`

Immediate cause:

- Runtime snapshot reports production runtime commit `37dca8564fee0206b0f524b870f147f4767bdc06`.
- Local production candidate is newer.
- Production hashes differ for deployable files.

Root cause:

- Production runtime has not yet been safely deployed to the canonical source truth.

Responsible owner:

- `tools/v7-safe-deploy`
- `tools/v7_sync_lib.safe_deploy_plan`
- `tools/v7-convergence-status`
- `tools/v7_sync_lib.convergence_status`

Executable fix:

- After local and GitHub truth pass, run the existing safe deploy command:
  - `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`

Verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

Expected result:

- Production runtime commit and deployable hashes align with canonical source truth.

## Root Causes

Minimum root cause set:

1. Local production candidate is not sealed into a clean commit.
2. Remote canonical branch is behind the local production candidate.
3. Production runtime is behind canonical deployable source truth.

These are sequential promotion-boundary failures, not architecture defects.

## Responsible Owners

- Local source truth: `tools/v7-truth-check.local_check`
- Remote truth: `tools/v7-truth-check.github_check`
- Deploy safety: `tools/v7-safe-deploy`
- Deploy mechanics: `tools/v7_sync_lib.safe_deploy_plan`
- Runtime convergence: `tools/v7-convergence-status`

## Minimal Execution Order

1. Seal local source truth.
2. Push canonical branch.
3. Rerun truth.
4. Run safe deploy.
5. Rerun truth.
6. Rerun convergence.
7. Resume L3 Production Phase.

## Expected GO Condition

Production readiness can become `GO` only when:

- local workspace is clean;
- runtime-critical dirty files are gone;
- `origin/Updatesystem` equals local production candidate;
- production runtime commit and deployable hashes equal canonical source truth;
- truth returns `PASS`;
- convergence returns `PASS`;
- safe deploy dry-run returns `PASS`.

## SMALLEST_EXECUTABLE_NEXT_STEP

Create one canonical production candidate commit from the current intended L3 changes, then rerun:

`tools/v7-truth-check --all --json`
