# P5.1 Reality Audit

## Scope

P5.1 answers one question: where is the real runtime truth for a future P5 retry?

This block is discovery-only. No P5 action was rerun.

## Repository Search Result

Repository search covered:

- runtime state
- state files
- registry readers
- users registry
- egress registry
- selected moves
- runtime hashes
- runtime snapshots
- runtime support tools
- operator execution
- runtime observability

## Expected Runtime Truth Sources

The repository consistently expects runtime state under:

`/opt/v7/egress/state`

Primary references:

- `admin/v7-admin-api`: `STATE_DIR = /opt/v7/egress/state` by default
- `admin_core/operator_execution.py`: runtime recheck reads `users.registry`, `egress.registry`, and selected-move files from `state_dir`
- `tools/runtime-support/v7-state-json`: builds `v7-state.json` from `/opt/v7/egress/state`
- `tools/runtime-support/v7-state-stale-check`: validates freshness of `summary.state`, `egress-status.state`, and `v7-state.json`
- `tools/v7-runtime-contract-validate`: treats `users.registry` and `egress.registry` as required runtime contract files
- `tools/v7-users-autoswitch`: reads registries, `v7-state.json`, service/capacity files, and selected moves from `STATE_DIR`

## Live Checks Performed

Local direct path check:

`/opt/v7`

Result:

`No such file or directory`

Public admin health check:

`https://v7-admin.195-2-79-116.sslip.io/health`

Result:

- status: `OK`
- auth_configured: `true`
- local_only: `true`

Unauthenticated runtime API checks:

- `/api/state`: `401 unauthorized`
- `/api/runtime/fingerprint`: `401 unauthorized`

No authenticated admin login was performed because P5.1 is discovery-only and login can create audit/session side effects.

## Historical Artifacts

The repository contains many old evidence snapshots and temporary state fixtures.

They are not runtime truth for P5.1 because the prompt forbids old reports, cached reports, fixtures, and historical artifacts as runtime truth.

## Verdicts

- reality_audit_complete=true
- expected_runtime_truth_path=/opt/v7/egress/state
- live_runtime_truth_available=false
- old_reports_used_as_truth=false
- fixtures_used_as_truth=false
