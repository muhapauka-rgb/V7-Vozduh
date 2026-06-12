# OA.1 Operator Approved Autonomy Certification Report

Проект: V7 Vozduh

Дата: 2026-06-12

Режим: read-only certification. OA.1 не двигал пользователей, не запускал apply, не менял routing, не включал autonomy и не создавал новый planner/governance/execution path.

## 1. Executive Summary

Финальный вердикт: `NEEDS_ONE_MORE_COMPONENT`.

V7 уже почти готова к Operator Approved Autonomy.

Система умеет готовить почти всё:

- наблюдение;
- анализ;
- planner candidate;
- packet evidence;
- rollback preview;
- restore barrier readiness;
- verification plan;
- feedback preview;
- trust/recommendation evidence;
- operator decision surface.

Но роль оператора ещё нельзя честно свести к одной кнопке `Approve / Reject`.

Причина:

`canonical_operator_approved_execution_controller_missing`

Сейчас есть preview/rehearsal surfaces и approval intent, но нет одного canonical controller, который после одного операторского APPROVE безопасно вызывает существующую цепочку:

`fresh planner -> packet -> recheck -> restore barrier -> governed apply -> verify -> rollback readiness -> feedback -> trust refresh -> closure`

## 2. Operator Decision Audit

По EXEC.2_4 и EXEC.5_6 оператор/governance фактически принимал решения в нескольких точках:

| Area | Current responsibility |
|---|---|
| Packet | выбрать свежий planner result и создать packet |
| Restore barrier | разрешить generation-bound clearance |
| Apply | явно запустить governed apply |
| Rollback | решить, нужен ли rollback; rollback readiness была подготовлена |
| Feedback | материализовать execution feedback и обновить snapshots |

Что система уже делает сама:

- считает кандидатов;
- строит selected move hashes;
- проверяет runtime recheck;
- формирует rollback manifest;
- делает verification;
- формирует feedback schemas;
- обновляет trust/planner evidence.

Evidence: `OA1_EVIDENCE/operator_decision_audit.md`.

## 3. Automation Candidate Audit

| Operator action | Classification |
|---|---|
| Read planner output | PREPARE_AUTOMATICALLY |
| Choose/reject proposed movement | APPROVE_ONLY |
| Generate packet evidence | PREPARE_AUTOMATICALLY |
| Review blast radius | PREPARE_AUTOMATICALLY |
| Review trust/risk | PREPARE_AUTOMATICALLY |
| Write restore barrier clearance | APPROVE_ONLY |
| Invoke guarded apply | APPROVE_ONLY |
| Verification | PREPARE_AUTOMATICALLY |
| Rollback readiness | PREPARE_AUTOMATICALLY |
| Rollback apply | KEEP_MANUAL |
| Feedback materialization | PREPARE_AUTOMATICALLY |
| Operator-free execution | UNSAFE_TO_AUTOMATE |

Evidence: `OA1_EVIDENCE/automation_candidate_audit.md`.

## 4. Packet Automation Review

Packet automation is mostly ready.

Evidence from code and reports:

- `tools/v7-operator-execution-packet` is the packet tool;
- `admin_core/operator_execution.py` owns approved plan lock and runtime recheck;
- EXEC.2_4 and EXEC.5_6 generated fresh packets successfully;
- packet contains allowed users, allowed targets, selected move budget and rollback manifest;
- packet itself does not grant apply authority.

Verdict:

`packet_preparation_automation_ready=true`

## 5. Restore Barrier Automation Review

Restore barrier readiness is structurally ready, but live clearance must remain governed.

Evidence:

- `admin_core/operator_execution.py` owns `runtime_recheck`;
- `append_restore_barrier_clearance` writes canonical clearance;
- EXEC.2_4 and EXEC.5_6 proved fresh restore barrier clearance works;
- dry-run/autonomous model exposes `restore_barrier_readiness`;
- current dry-run evidence keeps `restore_barrier_written_now=false`.

Verdict:

`restore_barrier_preparation_ready=true`

`restore_barrier_live_write_requires_operator_approval=true`

## 6. Execution Automation Review

Execution path is certified, but not one-click productized.

Certified owner:

`tools/v7-users-autoswitch --mode guarded --apply --verify`

Current evidence:

- one-user execution certified;
- 2-user execution certified;
- 5-user execution certified;
- current full planner batch of 8 users certified;
- rollback packet/dry-run certified;
- feedback materialization certified.

But admin/operator surfaces still show production execution actions as disabled/preview-only in this mode.

Verdict:

`execution_path_certified=true`

`single_operator_approval_execution_path_exists=false`

## 7. Approval Model

Required final approval boundary:

Operator sees:

- why move;
- why now;
- users and targets;
- risk;
- trust impact;
- blast radius;
- rollback plan;
- expected outcome;
- exact execution owner;
- exact feedback/closure path.

Operator has exactly two choices:

- `APPROVE`
- `REJECT`

On `REJECT`:

- write denial/closure only;
- no runtime mutation.

On `APPROVE`:

- call existing owners only;
- stop on any unknown or mismatch;
- never reselect users;
- never replace targets;
- never bypass restore barrier;
- never bypass guarded apply;
- never create new truth source.

Missing component:

`canonical operator-approved execution controller`

Evidence: `OA1_EVIDENCE/approval_model_required_component.md`.

## 8. Shadow Autonomy Simulation

Current autonomous dry-run evidence:

- `autonomous_dry_run=true`
- `preview_only=true`
- `read_only=true`
- `candidate_count=1`
- `packet_draft.would_prepare_packet=true`
- `feedback_preview` includes outcome/trust/prediction/recommendation/closure
- `apply_executed=false`
- `users_moved=0`
- `routing_changed=false`
- `autonomy_enabled=false`
- `execution_allowed_now=false`

Current dry-run also reports:

- `canary_autonomy_ready=false`
- `single_blocker=confidence_too_low`

Interpretation:

This blocks autonomous canary execution, not the existence of an operator-approved review mode.

For OA.1, the stronger blocker is product/control-plane shape:

the system cannot yet complete the loop after exactly one operator Approve action.

Evidence:

- `OA1_EVIDENCE/shadow_autonomy_simulation_current.json`
- `OA1_EVIDENCE/decision_surface_operator_approval_readiness.json`

## 9. Certification

Can V7 safely operate as:

`Observe -> Analyze -> Plan -> Prepare -> Operator Approves -> Execute -> Verify -> Learn`

without manual engineering work?

Answer:

Not yet.

V7 can prepare the decision and evidence, but it does not yet expose one canonical governed approval controller that turns a single operator approval into the full existing execution loop.

Certification result:

`NEEDS_ONE_MORE_COMPONENT`

## 10. Next Step

Recommended next program:

`OA2_CANONICAL_OPERATOR_APPROVED_EXECUTION_CONTROLLER_DESIGN_AND_PREVIEW_ONLY_IMPLEMENTATION`

Scope:

- design and implement preview-only single approval controller;
- reuse existing owners;
- no apply;
- no user movement;
- no autonomy enablement;
- prove APPROVE/REJECT state machine;
- prove reject writes closure only;
- prove approve would call packet/recheck/barrier/apply/verify/feedback in order;
- keep live execution disabled until certified.

## 11. Final Verdict

| Verdict | Value |
|---|---|
| final_verdict | `NEEDS_ONE_MORE_COMPONENT` |
| operator_approved_autonomy_ready | `false` |
| review_ready | `true` |
| packet_preparation_ready | `true` |
| restore_barrier_preparation_ready | `true` |
| execution_path_certified | `true` |
| feedback_path_certified | `true` |
| single_approve_reject_boundary_exists | `false` |
| single_blocker | `canonical_operator_approved_execution_controller_missing` |
| users_moved_by_oa1 | `0` |
| apply_executed_by_oa1 | `false` |
| routing_changed_by_oa1 | `false` |
| autonomy_enabled | `false` |
| new_planner_created | `false` |
| new_governance_created | `false` |
| new_execution_path_created | `false` |
| SAFE_NEXT_STEP | `OA2_CANONICAL_OPERATOR_APPROVED_EXECUTION_CONTROLLER_DESIGN_AND_PREVIEW_ONLY_IMPLEMENTATION` |

Core answer:

V7 is ready to prepare operator-approved autonomy decisions.

V7 is not yet ready to operate with the operator reduced to exactly one Approve / Reject action.

One missing component remains: a canonical one-action operator-approved execution controller that reuses the existing governed execution chain.

