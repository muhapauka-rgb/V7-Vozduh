# Controlled Production Certification Program Execution

Timestamp: 2026-07-03 00:19:26 +0700
Mode: EXECUTION
Canonical source: `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`

## Summary

Executed the Controlled Production Certification Program through the current phase.

Terminal state: `PHASE3_PASS`

Capability earned: `SMALL_BATCH_CERTIFIED`

Production result:

- Existing governed owner executed Stage 1 with `--max-users 5`.
- Selected users: `10.7.0.6`, `10.7.0.8`, `10.7.0.9`, `10.7.0.10`, `10.7.0.11`.
- Source: `openvpn-1779388847-d2ad7c`.
- Targets: `vless`, `awg3`.
- Runtime Apply: `APPLIED`.
- Verification: `PASS` for all 5.
- Rollback: `NOT_REQUIRED`.
- Users moved: `5`.
- Remaining users on failed source after certification: `10.7.0.12`, `10.7.0.13`, `10.7.0.15`.
- Incident `dd5b6289529f22197e6694a7` remains `OPEN`, which is correct because affected users remain.

No new Runtime, Planner, Authority, Restore Barrier owner, Wake owner, Packet owner, execution path, truth source, or broad automation was created.

## Phase Results

| Phase | Terminal state | Evidence |
| --- | --- | --- |
| Phase 0 Program Complete | `PASS` | Canonical program exists and includes Execution Priority Law. |
| Phase 1 Owner Mapping | `PASS` | Existing owners reused; no duplicate owner required. |
| Phase 2 CANARY Stability | `PASS` | Real governed one-user successes exist; consumer sync gaps are Synchronization Debt, not capability blockers under Execution Priority Law. |
| Phase 3 SMALL_BATCH Certification | `PASS` | Production governed batch moved 5 users with verification PASS and rollback NOT_REQUIRED. |

## Blocker Found And Resolved

Initial Phase 3 production run after canonical ladder deployment selected 5 moves but applied only 1.

Root cause:

`tools/v7-users-autoswitch` still had hard CANARY behavior in the existing execution path:

- `_emergency_failover_authority_gate()` limited an approved production-validation envelope to `max_users_per_run=1`.
- `_l3_execution_eligibility()` required exactly one selected move.

This was an implementation defect in the existing owner, not a need for new architecture.

## Implementation

Changed files:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Exact owner/function changed:

- `tools/v7-users-autoswitch::_emergency_failover_authority_gate`
- `tools/v7-users-autoswitch::_l3_execution_eligibility`

Correction:

- Approved production-validation envelopes now use the already-approved batch scope from Approved Plan Lock / Restore Barrier / Authority budget.
- Ordinary emergency failover without an approved envelope remains bounded by policy `max_users_per_run=1`.
- Runtime eligibility now allows `1..approved_scope` selected moves only when Approved Plan Lock and Restore Barrier validate the batch.

Commit:

- `03405df1bfb01a3c91825987795639311f45da3b` (`Allow approved governed L3 batch apply`)

GitHub:

- Pushed to `origin/Updatesystem`.

## Tests

Local tests:

- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_packet`
- Result: `178 tests OK`

Full unit discovery:

- `python3 -m unittest discover tests/unit`
- Result: `669 tests OK`

Compile:

- `python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_governed_canary_cli.py tests/unit/test_operator_execution_packet.py`
- Result: `PASS`

New regression coverage:

- Emergency failover without approved envelope remains single-user bound.
- Approved production-validation envelope preserves 5 selected moves through Runtime Apply.
- Runtime eligibility reports `approved_batch_scope=true` for approved batch execution.

## Safe Deploy

Pre-deploy safe-deploy:

- Blockers: `[]`
- Production delta: `tools/v7-users-autoswitch`
- GitHub truth: `PASS`

Deploy:

- Command: `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json`
- Result: `PASS`
- Production impact before certification: no automatic batch expansion; no users moved by deploy.

Post-deploy verification:

- Production `/usr/local/bin/v7-users-autoswitch` sha256 matched local/GitHub:
  `7d7bf7e3434325975666f63c2365c2b4853c9304679082c51844d14d17bb97ff`

## Production Certification

Command:

```text
/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 5 --pretty
```

Result:

| Field | Value |
| --- | --- |
| final_verdict | `L3_PRODUCTION_PROVEN` |
| transaction_status | `COMPLETED` |
| requested_max_users | `5` |
| authorized_l3_budget | `25` |
| authority_class | `POOL` |
| selected_move_count | `5` |
| apply selected count | `5` |
| users_moved | `5` |
| verification_result | `PASS` |
| rollback_result | `NOT_REQUIRED` |
| Runtime terminal_state | `APPLIED` |
| Runtime terminal_reason | `selected_moves_applied` |

Runtime eligibility:

- `approved_batch_scope=true`
- `approved_selected_move_count=5`
- `max_allowed_selected_moves=5`
- `checked_moves=5`
- `blockers=[]`
- `new_execution_path_created=false`

Per-user result:

| User | From | To | Apply | Route verify | Service verify | Rollback |
| --- | --- | --- | --- | --- | --- | --- |
| `10.7.0.6` | `openvpn-1779388847-d2ad7c` | `vless` | `0` | `0` | `0` | `not attempted` |
| `10.7.0.8` | `openvpn-1779388847-d2ad7c` | `awg3` | `0` | `0` | `0` | `not attempted` |
| `10.7.0.9` | `openvpn-1779388847-d2ad7c` | `vless` | `0` | `0` | `0` | `not attempted` |
| `10.7.0.10` | `openvpn-1779388847-d2ad7c` | `awg3` | `0` | `0` | `0` | `not attempted` |
| `10.7.0.11` | `openvpn-1779388847-d2ad7c` | `vless` | `0` | `0` | `0` | `not attempted` |

Post-run read-only production state:

- Remaining users on failed source: `3`
- Remaining users: `10.7.0.12`, `10.7.0.13`, `10.7.0.15`
- Active incident: `dd5b6289529f22197e6694a7`
- Incident status: `OPEN`
- Incident terminal_outcome: `SUCCESS`

## Automation Debt

Created:

- `manual_safe_deploy`
- `manual_stage1_certification_command`
- `manual_post_run_state_check`

Closed/classified:

- `manual_safe_deploy`: `INTENTIONALLY_MANUAL` because production deploy remains an existing safety-governed operator action.
- `manual_stage1_certification_command`: `INTENTIONALLY_MANUAL` because Stage 1 certification must not auto-promote or auto-run future stages.
- `manual_post_run_state_check`: `AUTOMATION_CANDIDATE` for future report/passport projection, not a capability blocker.

Unclassified manual work: `0`.

## Workflow Debt

Created:

- `stage1_certification_workflow`: tests -> commit/push -> safe-deploy plan -> safe-deploy apply -> production certification -> post-run evidence extraction -> report/CPS update.

Classification:

- `PIPELINE_CANDIDATE`

Reason:

The workflow is repeatable for Phase 4 and later. It should be investigated as a governed certification pipeline candidate, but it must not block Phase 3 capability recognition because capability producers completed successfully.

Unclassified workflow debt: `0`.

## Synchronization Debt

Created:

- Certification History / Passport / OMP / Production Maturity projections may need durable consumer synchronization after this capability event.

Classification:

- `SYNCHRONIZATION_DEBT`

Reason:

Capability producers completed successfully. Under Execution Priority Law, documentation consumers do not block capability recognition unless an existing safety owner proves synchronization is required first.

## Current Capability State

`SMALL_BATCH_CERTIFIED`

Stage 1 is certified for the active failed-source incident under existing governed path.

Production global behavior remains unchanged:

- No larger batch automatically enabled.
- No FULL_INCIDENT execution.
- No broad automation.
- No authority bypass.
- No Restore Barrier bypass.
- No Runtime bypass.

## Next Phase

`PHASE4_MEDIUM_BATCH_CERTIFICATION`

Required next action:

Run Phase 4 precheck. If Authority budget permits `MEDIUM_BATCH=10`, execute only through the existing governed owner and stop/demote on any verification, rollback, Runtime, Restore Barrier, or Authority failure.

