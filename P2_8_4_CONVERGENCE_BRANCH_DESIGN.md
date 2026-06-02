# P2.8.4 Convergence Branch Design

Project: V7 Vozduh
Block: P2.8.4

## Proposed Branch

`convergence/admin-api-2026-05`

No branch was created in this block.

## Branch Purpose

Prepare a reviewed Admin API source that reconciles:

- runtime-only execution read APIs
- local P2.2-P2.7 preview/candidate work
- `origin/Updatesystem` development baseline
- release/default branch governance constraints

## Branch Scope

In scope:

- `admin/v7-admin-api`
- targeted unit tests
- P2 convergence documentation
- route inventory and proof files

Out of scope:

- runtime deploy
- systemd changes
- user movement
- routing/autoswitch/policy/killswitch mutations
- branch default changes

## Branch Rules

1. Base from `origin/Updatesystem`.
2. Apply reviewed package waves only.
3. Preserve runtime-only execution read APIs or document a reviewed replacement.
4. Keep runtime state/config out of Git unless secret-safe and explicitly approved.
5. Require route inventory before and after each package.
6. Require fail-closed tests for read-only execution/candidate surfaces.

## Branch Lifecycle

1. Planning complete.
2. Future branch creation block.
3. Package wave commits.
4. Verification.
5. Review.
6. Release candidate decision.
7. Separate deployment block if approved.

## Exit Criteria

- Admin API hash is certified for convergence branch.
- Runtime-only API preservation is proven.
- Local-only package tests pass.
- Documentation and branch policy are complete.
- Deploy manifest is ready but not executed.

convergence_branch_defined=true
