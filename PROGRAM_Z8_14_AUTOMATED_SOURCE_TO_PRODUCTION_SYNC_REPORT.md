# PROGRAM Z8.14 — Automated Source-To-Production Sync And Deployment Pipeline Report

Project: V7 Vozduh

Branch: Updatesystem

Report date: 2026-06-02

## Executive Verdict

Z8.14 implemented a permanent source-to-production sync toolchain around the existing `tools/v7-truth-check` gate.

No new truth source was created. The new tools reuse the existing runtime convergence manifest and runtime snapshot model.

## Implemented Tools

| Tool | Purpose | Mutation level |
| --- | --- | --- |
| `tools/v7-sync-status` | Read-only local/GitHub/runtime convergence status | Read-only |
| `tools/v7-safe-commit` | Fail-closed commit helper with runtime-critical dirty classification | Local git commit only with `--apply` |
| `tools/v7-safe-push` | Canonical branch push helper; rejects force-style arguments | GitHub push only with `--apply` |
| `tools/v7-safe-deploy` | Approved-binary deploy/provenance helper with backup manifest path | Production deploy only with confirmation |
| `tools/v7-release-sync` | End-to-end release gate: status, tests, commit, push, deploy, truth check | Composite, confirmation gated |

## Reuse / Extension Map

| Component | Classification | Reason |
| --- | --- | --- |
| `tools/v7-truth-check` | REUSE | Existing source-of-truth gate for workspace, branch, GitHub, runtime snapshot, state truth |
| `docs/track7/runtime-convergence/V7_TRUTH_MANIFEST.json` | REUSE | Canonical branch/workspace/runtime manifest |
| `z8_11-evidence/runtime_convergence_snapshot.json` | EXTEND | Runtime provenance remains snapshot-backed; safe deploy can refresh deploy identity |
| `/opt/v7/deploy-manifest.json` | EXTEND | Existing copied-binary deployment provenance target |
| `/opt/v7/runtime-linkage.json` | EXTEND | Existing runtime-to-source linkage target |
| Existing rollback/runtime mutation tools | DO NOT TOUCH | Z8.14 forbids restore barrier, planner, policy, route, and user movement mutation |

## Local Toolchain Design

`v7-safe-commit`:

- requires an explicit commit message
- blocks unknown/runtime-critical dirtiness unless `--allow-runtime-critical` is present
- treats report/evidence dirtiness as documentation-only through the existing truth classification
- does not branch-switch, merge, pull, clean, delete, or reset

`v7-safe-push`:

- pushes only `origin HEAD:Updatesystem`
- rejects `--force`, `-f`, `--force-with-lease`, `--delete`, and `--mirror`
- validates canonical branch and remote before push
- allows normal fast-forward publish when the remote commit is an ancestor of local HEAD

`v7-safe-deploy`:

- deploys only the approved binary set:
  - `tools/v7-users-autoswitch` -> `/usr/local/bin/v7-users-autoswitch`
  - `tools/runtime-support/v7-audit-log` -> `/usr/local/bin/v7-audit-log`
  - `admin/v7-admin-api` -> `/usr/local/bin/v7-admin-api`
- creates a production backup root before manifest refresh/replacement
- writes deploy manifest, runtime linkage, and release manifest
- never runs autoswitch apply
- never mutates users, routes, planner, policy, or restore barrier state
- requires `--confirm DEPLOY_V7_APPROVED` for production mutation
- requires explicit admin restart flag if the admin binary changes

`v7-release-sync`:

- runs status, unit tests, safe commit, safe push, safe deploy, and final truth check
- requires `--confirm RELEASE_SYNC_APPROVED` for apply mode
- uses `v7-safe-deploy` internally for production mutation

## Test Coverage

Added `tests/unit/test_v7_sync_tools.py`.

Covered cases:

- runtime-critical dirty files require explicit approval
- documentation-only report dirtiness is non-blocking
- force-style push flags are rejected
- deploy manifest includes safety flags
- runtime linkage records copied-binary model
- release manifest requires rollback manifest
- approved deploy file list is limited to known runtime binaries
- deploy delta reports binary hash match/mismatch state
- source scan rejects unsafe push/autoswitch apply tokens in wrapper tools

## Validation Run

Commands executed locally:

- `env PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7_sync_lib.py tools/v7-sync-status tools/v7-safe-commit tools/v7-safe-push tools/v7-safe-deploy tools/v7-release-sync`
- `python3 -m unittest tests/unit/test_v7_sync_tools.py tests/unit/test_v7_truth_check.py`
- `python3 tools/v7-safe-commit --message 'Z8.14 sync pipeline dry run' --allow-runtime-critical --json`
- `python3 tools/v7-safe-push --json`
- `python3 tools/v7-safe-deploy --json`

Results:

- py_compile: PASS
- unit tests: PASS, 30 tests
- safe commit dry-run: PASS
- safe push dry-run before commit: expected NO-GO because runtime-critical tools were still uncommitted
- safe deploy dry-run before commit: expected NO-GO because GitHub/local truth could not pass while tools were uncommitted

## Publish And Production Sync Result

First publish commit:

`3c6303316606ce76993439e82be35b300aef143e`

GitHub push:

- `origin/Updatesystem`: `3c6303316606ce76993439e82be35b300aef143e`
- push mode: `v7-safe-push --apply`
- force push: not used

Production safe deploy:

- tool: `v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot`
- deploy id: `deploy-z8-14-Updatesystem-3c63033-20260602T154529`
- deployment required: `false`
- approved binary hashes matched production
- backup root created before manifest refresh
- service restart: not executed
- autoswitch apply: not executed
- user movement: not executed
- routing mutation: not executed
- restore barrier mutation: not executed

Final truth gate after production provenance refresh:

- `python3 tools/v7-truth-check --all --json`: PASS
- convergence status: `FULLY_ALIGNED`
- runtime access status: `READY`
- runtime truth status: `KNOWN`
- state truth status: `KNOWN`
- sync status: `SYNCED`

## Safety Confirmation

Not executed:

- autoswitch apply
- user movement
- routing mutation
- restore barrier mutation
- planner mutation
- policy mutation
- destructive cleanup
- force push
- service restart

## Final Verdicts

safe_commit_tool_created=true

safe_push_tool_created=true

safe_deploy_tool_created=true

release_sync_tool_created=true

sync_status_tool_created=true

tests_created=true

tests_pass=true

github_sync_verified=true

production_sync_verified=true

truth_check_all_pass=true

force_push_possible=false

blind_deploy_possible=false

backup_manifest_required=true

runtime_mutation_blocked=true

safe_to_retry_Z9=true

## Required Finalization

Completed:

1. Commit the toolchain and report with `v7-safe-commit`.
2. Push `Updatesystem` with `v7-safe-push`.
3. Refresh production provenance with `v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot`.
4. Run `v7-truth-check --all --json`.
5. Verify `v7-sync-status --json` returns `SYNCED`.
