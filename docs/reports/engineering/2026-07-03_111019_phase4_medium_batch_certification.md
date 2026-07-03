# Phase 4 MEDIUM_BATCH Certification

Timestamp: 2026-07-03 11:10:19 Asia/Bangkok

## Certification Phase

Current Program Phase: Phase 4 MEDIUM_BATCH Certification

Terminal State: PASS

## Source

Controlled incident source:

`wireguard-1779454504-c43409`

Controlled source interface:

`v7e06a394c478`

## Preconditions

Canonical ladder:

- CANARY = 1
- SMALL_BATCH = 5
- MEDIUM_BATCH = 10
- LARGE_BATCH = 25
- XLARGE_BATCH = 50
- FULL_INCIDENT = remaining affected users on the same active incident

Authority observed:

- authorized_l3_budget = POOL
- budget ceiling = 25

Certification pool at start:

- 11 certification users assigned to `wireguard-1779454504-c43409`

Controlled degradation owner:

`/usr/local/bin/v7-egress-set-state wireguard-1779454504-c43409 maintenance --controlled-certification --apply`

Guard evidence:

- `V7_EGRESS_GUARD=OK`
- reason = `assigned_certification_users_scoped`
- assigned certification users: `10.7.0.16` through `10.7.0.26`

## Executed Command

Existing governed owner path:

`/usr/local/bin/v7-governed-canary-dry-run-cycle --max-users 10 --approved-source wireguard-1779454504-c43409 --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --pretty`

Production payload:

`/tmp/v7_phase4_medium_batch_after_metadata_fix_20260703T063801.json`

## Result

Top-level governed result:

- final_verdict = `L3_PRODUCTION_PROVEN`
- transaction_status = `COMPLETED`
- command_rc = 0
- apply_executed = true
- users_moved = 10

Runtime transition owner:

`admin_core/operator_execution_pipeline.py`

Runtime consumer:

`tools/v7-users-autoswitch --apply --verify`

Selected move count:

10

## Selected Users

All selected users had:

`current_egress == wireguard-1779454504-c43409`

Selected moves:

- `10.7.0.16`: `wireguard-1779454504-c43409` -> `awg0`
- `10.7.0.17`: `wireguard-1779454504-c43409` -> `vless`
- `10.7.0.18`: `wireguard-1779454504-c43409` -> `awg0`
- `10.7.0.19`: `wireguard-1779454504-c43409` -> `vless`
- `10.7.0.20`: `wireguard-1779454504-c43409` -> `awg3`
- `10.7.0.21`: `wireguard-1779454504-c43409` -> `awg0`
- `10.7.0.22`: `wireguard-1779454504-c43409` -> `vless`
- `10.7.0.23`: `wireguard-1779454504-c43409` -> `awg3`
- `10.7.0.24`: `wireguard-1779454504-c43409` -> `awg0`
- `10.7.0.25`: `wireguard-1779454504-c43409` -> `vless`

No unrelated source was selected.

## Remaining Users

Remaining user on controlled source after MEDIUM_BATCH:

- `10.7.0.26`

Remaining count:

1

## Verification

Post-run route verification after restoring controlled source:

`V7_USER_ROUTE_CHECK=OK`

Observed for remaining user:

- `10.7.0.26` registry matches assignment.
- table `1024` default route uses `v7e06a394c478`.
- route_get uses `v7e06a394c478`.

## Rollback

No rollback was required for the 10 moved users in the governed batch result.

## Controlled Source Restoration

After certification evidence was captured, the controlled source was restored:

`/usr/local/bin/v7-egress-set-state wireguard-1779454504-c43409 enabled --apply`

Result:

- `V7_EGRESS_SET_STATE=OK`
- interface `v7e06a394c478` restored
- route-check OK

## Phase Verdict

Phase 4 MEDIUM_BATCH: PASS

## Automation Debt Delta

Closed:

- Phase 4 no longer requires manual interpretation of certification metadata after the `_load_users()` metadata merge fix.

Created:

- Manual extraction of `operator_execution_pipeline` transition evidence from the governed payload.

Classification:

- Workflow Debt: bounded certification evidence extraction should become a single governed certification report command.

## Workflow Debt Delta

Created:

- Manual sequence: controlled degrade -> governed batch run -> payload parse -> source restore -> route verification.

Terminal classification for now:

`BLOCKED_BY_FUTURE_CAPABILITY`

Required future pipeline candidate:

Certification phase executor should run this workflow as one governed command and emit a phase report.

## Current Capability State

Certified:

- CANARY
- SMALL_BATCH
- MEDIUM_BATCH

Not yet certified:

- LARGE_BATCH
- XLARGE_BATCH
- FULL_INCIDENT

## Next Phase

Begin Phase 5 LARGE_BATCH certification.

Immediate next task:

Run Certification Pool Sufficiency decision for a 25-user controlled batch.
