# P5.1 Runtime Audit

## Live Runtime Inspection

Checked local path:

`/opt/v7`

Result:

`No such file or directory`

Checked derived expected path:

`/opt/v7/egress/state`

Result:

`No such file or directory`

Checked public admin health:

`/health`

Result:

- service reachable
- status `OK`
- auth configured
- runtime API authentication required

Checked unauthenticated runtime APIs:

- `/api/state`: `401 unauthorized`
- `/api/runtime/fingerprint`: `401 unauthorized`

## Runtime Contract Validation

Command:

`python3 tools/v7-runtime-contract-validate --state-dir /opt/v7/egress/state`

Result:

- status: `fail`
- critical_count: `2`
- missing: `/opt/v7/egress/state/egress.registry`
- missing: `/opt/v7/egress/state/users.registry`

## Stale Check

Command:

`tools/runtime-support/v7-state-stale-check`

Result:

- `summary.state` missing
- `egress-status.state` missing
- `v7-state.json` missing
- `V7_STALE_RESULT=FAIL`

## Verdicts

- runtime_audit_complete=true
- live_runtime_files_accessible=false
- runtime_api_accessible_without_auth=false
- authenticated_runtime_api_used=false
- runtime_truth_source_certified=false
- safe_to_rerun_p5=false
