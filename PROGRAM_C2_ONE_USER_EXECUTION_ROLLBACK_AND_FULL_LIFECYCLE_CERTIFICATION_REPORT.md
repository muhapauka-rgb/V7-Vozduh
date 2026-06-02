# PROGRAM C.2 — One User Execution, Rollback and Full Lifecycle Certification Report

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Runtime owner: `tools/v7-users-autoswitch`

Evidence folder: `program_c2_evidence`

## Scope

Program C.2 certified the complete production lifecycle for one user:

Operation -> Execution -> Verification -> Audit -> Closure -> Rollback -> Rollback Audit -> Rollback Closure.

Budget was respected:

- one selected user: `10.0.0.2`
- one forward movement: `awg3 -> vless`
- one rollback: `vless -> awg3`
- no batch movement
- no route mutation outside the existing user-switch primitive
- no planner or policy override
- no alternate execution path

## Discovery Gate

Fresh truth checks passed:

- pre-runtime work: `final_verdict=PASS`, `convergence_status=FULLY_ALIGNED`
- final post-rollback: `final_verdict=PASS`, `convergence_status=FULLY_ALIGNED`

Runtime truth, state truth, runtime provenance, and runtime access were known.

Evidence:

- `program_c2_evidence/post_deploy_truth_check.txt`
- `program_c2_evidence/final_truth_check_after_rollback.txt`

## Duplication Audit

| Area | Certified owner/path | Verdict |
| --- | --- | --- |
| Runtime owner | `tools/v7-users-autoswitch` | single owner |
| Planner | `tools/v7-users-autoswitch` | single planner |
| Forward execution | `tools/v7-users-autoswitch --apply --verify` | single execution path |
| Approval/clearance | `tools/v7-operator-execution-packet` + `admin_core/operator_execution.py` | single clearance path |
| Rollback execution | `tools/v7-users-autoswitch --rollback-packet --apply --verify` | single rollback owner |
| Audit | `/opt/v7/audit/audit.jsonl` via `v7-audit-log` | single runtime audit path |
| Closure | `closure_target` emitted by `tools/v7-users-autoswitch` | single runtime closure path |

Rejected/unused paths:

- direct manual `v7-user-switch`
- generic `v7-rollback-last-change --apply`
- Admin broad rollback endpoint
- break-glass execution

## Blocker Closure

The first forward apply attempt returned `NOOP` because the restore-barrier clearance generation drifted between pre-exec and apply.

Root cause:

- `v7-state.json` was still part of stable `planner_generation_id`.
- It is fast runtime telemetry and changed between clearance and apply.
- The selected move hash/count were unchanged, but generation mismatch correctly stopped execution.

Fix:

- Moved dynamic runtime telemetry into `volatile_inputs`.
- Stable generation now remains authority-oriented: registries, service preferences, policy, org policy.
- Selected move hash/count remain the fail-closed guard for actual movement changes.

Validation:

- `tests.unit.test_v7_users_autoswitch_policy` PASS, 24 tests.
- full `unittest discover tests` PASS, 174 tests.

Evidence:

- `program_c2_evidence/phase3_generation_drift_after_noop.json`
- `program_c2_evidence/test_v7_users_autoswitch_policy_after_generation_fix.txt`
- `program_c2_evidence/test_full_unittest_discover_after_generation_fix.txt`

## Forward Lifecycle

Fresh C.2 pre-execution certification passed:

- `clearance_allowed=true`
- `clearance_verdict=RESTORE_BARRIER_CLEARANCE_WRITTEN`
- `pre_selected_moves=1`
- `pre_clearance_ok=true`
- `pre_guard_reason=restore_barrier_clearance_budget_and_generation_ok`
- selected move hash: `ef70877188c72befad38d84bfdbb334923fa855bc096182c80e48cbc7382a9f8`

Forward execution result:

- operation id: `runtime_autoswitch_5fae520f1ec8c089649c61d0`
- selected user: `10.0.0.2`
- movement: `awg3 -> vless`
- terminal state: `APPLIED`
- terminal reason: `selected_moves_applied`
- verify rc: `0`
- audit emitted: true
- closure state: `VERIFIED_READY`

Post-forward registry:

- `ip=10.0.0.2 current=vless table=100 enabled=1`

Evidence:

- `program_c2_evidence/phase1b_phase2b_pre_execution_summary.json`
- `program_c2_evidence/phase3b_forward_apply_summary.json`
- `program_c2_evidence/phase3b_forward_apply.raw.json`
- `program_c2_evidence/phase4_user_registry_after_forward.txt`

## Rollback Lifecycle

Rollback packet:

- schema: `c2.autoswitch-rollback-packet.v1`
- packet id: `rbpkt_9e7416678481ecb3910fb26b`
- source operation id: `runtime_autoswitch_5fae520f1ec8c089649c61d0`
- rollback owner: `tools/v7-users-autoswitch`
- selected user: `10.0.0.2`
- rollback movement: `vless -> awg3`
- selected move hash linked to forward operation.

Rollback execution result:

- rollback operation id: `runtime_rollback_fe2e8a8f25e5ba79ff98835b`
- terminal state: `ROLLBACK_COMPLETED`
- terminal reason: `operation_scoped_rollback_completed`
- verify rc: `0`
- rollback audit emitted: true
- rollback closure state: `VERIFIED_READY`

Post-rollback registry:

- `ip=10.0.0.2 current=awg3 table=100 enabled=1`

Evidence:

- `program_c2_evidence/phase7_rollback_preparation_summary.json`
- `program_c2_evidence/phase7_rollback_packet.raw.json`
- `program_c2_evidence/phase8_rollback_apply_summary.json`
- `program_c2_evidence/phase8_rollback_apply.raw.json`
- `program_c2_evidence/phase9_user_registry_after_rollback.txt`
- `program_c2_evidence/phase9_post_rollback_route_check_tail.txt`

## Audit And Closure Certification

Canonical audit file:

- `/opt/v7/audit/audit.jsonl`

Forward audit:

- object id: `runtime_autoswitch_5fae520f1ec8c089649c61d0`
- result: `APPLIED`
- selected move hash present
- planner generation present
- runtime snapshot hash present

Rollback audit:

- object id: `runtime_rollback_fe2e8a8f25e5ba79ff98835b`
- result: `ROLLBACK_COMPLETED`
- source operation id linked
- rollback packet id linked
- selected move hash linked

No duplicate runtime audit path was used.

Evidence:

- `program_c2_evidence/phase5_audit_file_inventory.txt`
- `program_c2_evidence/phase5_phase10_audit_lineage_search.txt`
- `program_c2_evidence/phase6_phase11_governance_lifecycle_tail.txt`

## Full Lifecycle Verdict

The certified chain is complete:

1. Operation created: `runtime_autoswitch_5fae520f1ec8c089649c61d0`
2. Execution completed: `APPLIED`
3. Verification completed: route check OK
4. Audit emitted: `/opt/v7/audit/audit.jsonl`
5. Closure emitted: `VERIFIED_READY`
6. Rollback packet generated: `rbpkt_9e7416678481ecb3910fb26b`
7. Rollback completed: `runtime_rollback_fe2e8a8f25e5ba79ff98835b`
8. Rollback audit emitted: `/opt/v7/audit/audit.jsonl`
9. Rollback closure emitted: `VERIFIED_READY`
10. User restored: `10.0.0.2 current=awg3`

## Autonomy Readiness

Autonomy was not performed.

Readiness is confirmed because the runtime owner can now:

- plan a selected move,
- consume governance clearance,
- execute one bounded move,
- verify,
- emit audit,
- emit closure,
- generate operation-scoped rollback packet,
- execute rollback through the same runtime owner,
- verify rollback,
- emit rollback audit,
- emit rollback closure.

## Final Verdicts

| Verdict | Value |
| --- | --- |
| `one_user_execution_completed` | true |
| `operation_created` | true |
| `operation_lineage_valid` | true |
| `audit_created` | true |
| `audit_lineage_valid` | true |
| `closure_created` | true |
| `closure_lineage_valid` | true |
| `rollback_completed` | true |
| `rollback_lineage_valid` | true |
| `rollback_audit_valid` | true |
| `rollback_closure_valid` | true |
| `full_operation_lifecycle_certified` | true |
| `autonomy_readiness_confirmed` | true |
| `safe_to_continue_to_PROGRAM_D` | true |

Final status: PASS.
