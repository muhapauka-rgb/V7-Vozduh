# PROGRAM C - Governance Execution Rollback Autonomy And Failure Certification Report

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Mode: production read-only discovery plus one-user dry-run recheck
Evidence folder: `program_c_evidence`

## Executive Verdict

Program C cannot safely proceed to one-user execution.

Single proven external blocker:

`canonical_restore_barrier_clearance_writer_missing`

The live one-user candidate still exists, but `v7-users-autoswitch` correctly
selects zero moves because the current restore-barrier clearance is expired and
bound to an older planner generation. A fresh nonzero movement clearance would
require writing `/opt/v7/egress/state/autoswitch-restore-barrier.json`, but no
canonical active writer or lifecycle owner for this clearance was found.

Manual editing of the barrier would create a duplicate governance path and
bypass the ownership model, so it is not safe within Program C.

## Phase 0 - Fresh Runtime Read

`tools/v7-truth-check --all` returned:

- `current_branch=Updatesystem`
- `current_commit=25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`
- `remote_branch_commit=25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`
- `runtime_access_status=READY`
- `runtime_truth_status=KNOWN`
- `state_truth_status=KNOWN`
- `convergence_status=FULLY_ALIGNED`
- `final_verdict=PASS`
- warning: `documentation_dirty_ignored`

Runtime snapshot confirmed production has the expected autoswitch, audit, admin,
rollback, and restore-settle binaries. The current restore barrier is a stale
Z3.2 clearance:

- `block=PROGRAM_Z3_2`
- `allowed_user=10.7.0.16`
- `allowed_target=awg3`
- `clearance_max_selected_moves=1`
- `clearance_generation_id=c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- `approved_selected_moves_hash=f07989c421144d900cb3bc38621267282c0fcedb4477d83bdc2e25417bd18cae`
- `clearance_expires_at=2026-06-01T18:02:59.305408+00:00`

## Duplication Audit

| Area | Current finding | Verdict |
|---|---|---|
| Runtime owner | `systemd/v7-users-autoswitch.timer` -> `v7-users-autoswitch.service` -> `v7-users-autoswitch` | Single autoswitch runtime chain exists, but timer is currently inactive in production. |
| Planner | `tools/v7-users-autoswitch` | Single planner for this candidate. |
| Selected moves | `tools/v7-users-autoswitch.plan()` | Single live selected-move source for execution dry-run. |
| Governance owner | Contracts/read adapters exist; nonzero barrier clearance writer not found | Incomplete. |
| Rollback owner | Autoswitch has verify-failure rollback only; `v7-rollback-last-change` is broad latest-backup rollback | Not operation-scoped for Program C rollback. |
| Audit path | `v7-users-autoswitch` emits `v7-audit-log` only on `--apply` | Partial. |
| Closure path | `v7-users-autoswitch` returns `closure_target` owned by `admin/v7-admin-api` | Split owner; closure is not completed by autoswitch. |
| Autoswitch authority | `v7-users-autoswitch --apply` and Admin guarded apply endpoint | Movement-capable, but blocked by stale barrier. |

Rejected paths:

- Direct `v7-user-switch`: rejected as manual execution path.
- Manual barrier JSON edit: rejected as governance bypass and duplicate writer.
- `v7-rollback-last-change --apply`: rejected for Program C user rollback because it is broad latest-backup rollback, not operation-scoped rollback for the selected user.
- `v7-operator-execution-packet`: rejected for Program C execution because it is zero-movement/read-only or append-only governance record flow and reports `execution_allowed_now=false`.

## Phase 1 - Fresh Candidate Recheck

Fresh production one-user dry-run:

- command: `/usr/local/bin/v7-users-autoswitch --pretty --user 10.0.0.2`
- user: `10.0.0.2`
- current egress: `awg3`
- recommended target: `vless`
- action: `switch`
- move type: `failover`
- candidate moves total: `1`
- selected moves: `0`
- current planner generation: `7e4a8d35db41816050daa1798d2f38115d863acff7cf8647bacf1fbc7d739785`
- selected moves before restore-barrier guard: `1`
- candidate selected-move hash before guard: `ef70877188c72befad38d84bfdbb334923fa855bc096182c80e48cbc7382a9f8`
- terminal reason: `dry_run_restore_barrier_clearance_generation_expired`

Target rationale remains valid:

- `target_egress=vless`
- `service_aggregate_score=100.0`
- `best_available_pool=true`
- `pool_rank=1`
- `capacity_decision=capacity_available`
- projected target users: `3`
- projected soft limit: `21`
- projected hard limit: `27`

The fail-closed behavior is working: stale/expired generation clearance produces
zero selected moves and an explicit terminal reason.

## Root Cause

The execution blocker is not a planner bug and not a target eligibility bug.
It is a governance lifecycle ownership gap:

1. `v7-users-autoswitch` enforces nonzero restore-barrier clearance.
2. E12 rules require token, generation id, selected-move hash, expected count,
   budget, and expiry for nonzero clearance.
3. Admin and operator modules expose read-only previews/adapters.
4. `v7-operator-execution-packet` is zero-movement/read-only/record-only.
5. Production binary search found no command that owns creation of a fresh
   nonzero restore-barrier clearance.

Therefore Program C has no safe canonical way to refresh governance clearance
for the current `10.0.0.2 -> vless` movement.

## Fix Attempt Assessment

Fixing this within Program C is not safe because the only available practical
mutation would be a direct write to:

`/opt/v7/egress/state/autoswitch-restore-barrier.json`

That would violate the Program C safety boundary:

- no governance bypass;
- no duplicate execution path;
- no duplicate truth source;
- no manual execution chain;
- no unowned restore-barrier lifecycle mutation.

The safe remediation is a separate implementation block that creates or extends
one canonical restore-barrier clearance owner, then deploys and validates it
before retrying Program C.

## Phase Status

| Phase | Status | Reason |
|---|---|---|
| Phase 0 fresh runtime read | PASS | Truth check PASS and production snapshot captured. |
| Duplication audit | PASS_WITH_BLOCKER | Duplicate manual paths identified and rejected. |
| Phase 1 fresh governance clearance | BLOCKED | No canonical nonzero restore-barrier clearance writer found. |
| Phase 2 execution readiness | BLOCKED | Selected move hash/generation are fresh, but cannot be approved into barrier safely. |
| Phase 3 one-user execution | NOT_RUN | Execution before canonical clearance would bypass governance. |
| Phase 4 post execution certification | NOT_RUN | No execution. |
| Phase 5 audit certification | NOT_RUN | No apply audit emitted. |
| Phase 6 closure certification | NOT_RUN | Closure target remains split and no operation closure created. |
| Phase 7 rollback certification | NOT_RUN | No forward movement; rollback path also not operation-scoped. |
| Phase 8 post rollback certification | NOT_RUN | No rollback. |
| Phase 9 rollback audit and closure | NOT_RUN | No rollback. |
| Phase 10 autonomy validation | FAIL | Runtime chain cannot complete full clearance -> execution -> audit -> closure -> rollback lifecycle autonomously. |
| Phase 11 failure validation | PASS_PARTIAL | Current stale/expired clearance fails closed with selected moves `0` and explicit reason. |
| Phase 12 production readiness decision | NO-GO | Not ready for Program D. |

## Required Remediation Before Retry

1. Define the canonical owner for nonzero restore-barrier clearance.
2. Implement or extend exactly one writer for
   `/opt/v7/egress/state/autoswitch-restore-barrier.json`.
3. Bind the writer to E12 fields:
   `generation_token`, `clearance_generation_id`,
   `approved_selected_moves_hash`, `clearance_expected_selected_moves`,
   `clearance_max_selected_moves`, and `clearance_expires_at`.
4. Require exact approved user and target constraints.
5. Emit audit for clearance creation.
6. Define operation-scoped rollback ownership for the same movement.
7. Define closure completion ownership instead of only returning
   `closure_target`.
8. Deploy through the existing convergence gate.
9. Retry Program C from fresh truth check and fresh one-user dry-run.

## Evidence

- `program_c_evidence/phase0_truth_check.json`
- `program_c_evidence/phase0_runtime_snapshot.txt`
- `program_c_evidence/phase0_runtime_tool_sources.txt`
- `program_c_evidence/phase1_one_user_preclearance_dry_run.json`
- `program_c_evidence/phase1_production_clearance_writer_search.txt`
- `program_c_evidence/phase1_operator_execution_packet_source.txt`

## Final Verdicts

fresh_governance_clearance_created=false
one_user_execution_completed=false
operation_created=false
audit_created=false
closure_created=false
rollback_completed=false
rollback_audit_valid=false
rollback_closure_valid=false
full_operation_lifecycle_certified=false
autonomy_validated=false
fail_closed_validated=true
production_ready_for_program_d=false

final_result=EXTERNAL_BLOCKER
external_blocker=canonical_restore_barrier_clearance_writer_missing
