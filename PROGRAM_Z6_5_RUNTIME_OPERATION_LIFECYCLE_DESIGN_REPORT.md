# PROGRAM Z6.5 - Runtime Operation Lifecycle Design Report

Project: V7 Vozduh
Branch target: `v7-next`
Mode: READ ONLY lifecycle semantics design
Date: 2026-06-02

## Executive Verdict

The final Runtime Operation Lifecycle is defined as a semantic lifecycle over existing components, not a new API, storage model, or runtime owner.

Runtime Operation truth is owned by:

`tools/v7-users-autoswitch`

Audit truth is owned by:

`tools/runtime-support/v7-audit-log`

Closure truth is owned by:

`admin/v7-admin-api` + `admin_core/operator_observability.py`

The lifecycle has three distinct layers:

1. Runtime terminal state.
2. Audit completion state.
3. Closure completion state.

`COMPLETED` does not mean `CLOSED`. `ROLLED_BACK` does not mean `CLOSED`. Runtime terminal states must become `AUDITED` before they can become lifecycle `CLOSED`.

## Evidence Directory

`z6_5-evidence`

- `00_gate0_state_discovery.md`
- `01_operation_object_and_boundaries.md`
- `02_target_state_machine.md`
- `03_state_ownership_and_terminal_states.md`
- `04_audit_closure_rollback_noop_relationships.md`
- `05_end_to_end_timeline_and_gap_impact.md`
- `06_final_verdicts.md`

## 1. Discovery of Existing States

| Model | Existing States | Owner | Z6.5 Use |
|---|---|---|---|
| Execution contracts | `DRAFT`, `PRECHECKED`, `APPROVED`, `SCHEDULED`, `VALIDATED`, `RECHECKED`, `EXECUTING`, `VERIFYING`, `OBSERVING`, `ROLLBACK_READY`, `ROLLING_BACK`, `COMPLETED`, `FAILED_CLOSED`, `ROLLED_BACK`, `REPLAY_DENIED`, `CANCELLED`, `EXPIRED` | Admin read model | Reuse as base runtime operation vocabulary. |
| Execution events | `EXECUTION_*`, `VERIFICATION_*`, `ROLLBACK_*`, `REPLAY_DENIED` | Admin read model | Reuse as event vocabulary. |
| Closure states | `OPEN`, `VERIFIED`, `CLOSED`, `EXPIRED` | Admin closure owner | Reuse as closure layer, not runtime terminal layer. |
| Proposal states | `DRAFT`, `OBSERVED`, `ACTIVE`, `REVIEW_REQUIRED`, `EXPIRED`, `SUPERSEDED`, `CLOSED` | Admin proposal model | Reuse as pre-operation/input state. |
| Evidence states | `OPEN`, `OBSERVING`, `VERIFIED`, `CLOSED`, `STALE` | Admin evidence model | Reuse as evidence state only. |
| Gates/checks | `PASS`, `FAIL`, `REVIEW_REQUIRED`, `UNKNOWN`, `READY`, `BLOCKED`, `READY_WITH_REVIEW`, `NOT_READY` | Admin gates/readiness | Reuse as admission evidence. |
| Operator execution verdicts | `PACKET_VALID`, `DENY_PACKET_INVALID`, `DENY_STALE_RUNTIME`, `DENY_HASH_MISMATCH`, `ALLOW_RECORD_ONLY`, `DENY_REPLAY`, `DENY_RUNTIME_ACTION_UNSUPPORTED` | operator execution support | Reuse as recheck/supporting verdicts. |
| Autoswitch outcomes | `applied=false` reasons, or `applied=true` per-move results | Runtime owner | Reuse as runtime outcome source. |

No new lifecycle model may ignore these concepts.

## 2. Lifecycle Object Discovery

Current reality:

- Proposal is not a runtime operation by itself.
- Execution packet/contract is not a runtime operation by itself while preview-only.
- Selected move is not a full operation by itself.
- Restore barrier is not an operation by itself.
- Audit event is not an operation by itself.
- Closure record is not an operation by itself.

A Runtime Operation is the semantic composition of:

- bounded intent or scheduled runtime cycle;
- runtime owner decision;
- selected moves or no-op/denial reason;
- runtime outcome;
- rollback outcome if applicable;
- audit evidence;
- closure record.

## 3. Target Operation Model

A Runtime Operation is:

- a bounded runtime decision lifecycle;
- owned by `tools/v7-users-autoswitch` for runtime truth;
- scoped to one runtime decision set;
- associated with zero or more selected moves;
- associated with terminal runtime outcome;
- auditable through `v7-audit-log`;
- closable through Admin/operator closure.

Runtime Operations include:

- single user movement;
- multi-user movement;
- rollback;
- cancelled movement;
- failed movement;
- no-op decision;
- selected_moves=0 scheduled/apply cycle;
- policy/trust/capacity/restore-barrier denial;
- replay denial.

Not Runtime Operations by themselves:

- proposal only;
- evidence bundle only;
- audit event only;
- closure record only;
- passive health signal only.

## 4. Operation State Machine

Canonical states:

- `CREATED`
- `PLANNED`
- `REVIEW_REQUIRED`
- `APPROVED`
- `DENIED`
- `READY`
- `EXECUTING`
- `VERIFYING`
- `ROLLBACK_READY`
- `ROLLING_BACK`
- `COMPLETED`
- `FAILED_CLOSED`
- `ROLLED_BACK`
- `REPLAY_DENIED`
- `CANCELLED`
- `EXPIRED`
- `AUDITED`
- `CLOSED`

Successful movement:

`CREATED` -> `PLANNED` -> `REVIEW_REQUIRED` -> `APPROVED` -> `READY` -> `EXECUTING` -> `VERIFYING` -> `COMPLETED` -> `AUDITED` -> `CLOSED`

Autonomous no-op:

`CREATED` -> `PLANNED` -> `COMPLETED` -> `AUDITED` -> `CLOSED`

Denied/blocked no-op:

`CREATED` -> `PLANNED` -> `DENIED` -> `AUDITED` -> `CLOSED`

Failure with rollback:

`CREATED` -> `PLANNED` -> `APPROVED` -> `READY` -> `EXECUTING` -> `VERIFYING` -> `ROLLBACK_READY` -> `ROLLING_BACK` -> `ROLLED_BACK` -> `AUDITED` -> `CLOSED`

Failure without successful rollback:

`CREATED` -> `PLANNED` -> `APPROVED` -> `READY` -> `EXECUTING` -> `VERIFYING` -> `FAILED_CLOSED` -> `AUDITED` -> `CLOSED`

Cancelled/expired:

`CREATED` -> `PLANNED` -> `CANCELLED` -> `AUDITED` -> `CLOSED`

`CREATED` -> `PLANNED` -> `EXPIRED` -> `AUDITED` -> `CLOSED`

## 5. State Ownership

| State | Primary Owner | Runtime Owner | Audit Owner | Closure Owner |
|---|---|---|---|---|
| `CREATED` | Admin/scheduler/runtime cycle source | Autoswitch if scheduled | `v7-audit-log` if recorded | Admin closure |
| `PLANNED` | Runtime owner | Autoswitch | optional until terminal | Admin closure after terminal |
| `REVIEW_REQUIRED` | Admin gates | Autoswitch supplies facts | optional | Admin closure |
| `APPROVED` | Admin/operator governance | Autoswitch consumes | required before closure | Admin closure |
| `DENIED` | Runtime owner or Admin gates | Autoswitch if runtime denial | required for closure | Admin closure |
| `READY` | Runtime owner | Autoswitch | optional until execution | no direct closure unless cancelled/expired |
| `EXECUTING` | Runtime owner | Autoswitch | should record execution start | no |
| `VERIFYING` | Runtime owner | Autoswitch | should record verification start | no |
| `ROLLBACK_READY` | Runtime owner | Autoswitch | should record failure/rollback need | no |
| `ROLLING_BACK` | Runtime owner or rollback primitive under owner | Autoswitch for movement | should record rollback start | no |
| `COMPLETED` | Runtime owner | Autoswitch | required before closure | Admin closure |
| `FAILED_CLOSED` | Runtime owner | Autoswitch | required before closure | Admin closure |
| `ROLLED_BACK` | Runtime owner/rollback primitive | Autoswitch for movement rollback | required before closure | Admin closure |
| `REPLAY_DENIED` | Runtime owner/recheck support | Autoswitch/operator support | required before closure | Admin closure |
| `CANCELLED` | Admin/runtime owner | Autoswitch if runtime cancel | required before closure | Admin closure |
| `EXPIRED` | Admin/runtime owner | Autoswitch if runtime expiry | required before closure | Admin closure |
| `AUDITED` | Audit owner | runtime facts source | `v7-audit-log` | Admin closure next |
| `CLOSED` | Closure owner | immutable runtime facts | audit reference required | Admin/operator closure |

## 6. Terminal States

| Terminal State | Meaning | Requirements | Evidence Required | Audit Required | Closure Required |
|---|---|---|---|---|---|
| `COMPLETED` | Runtime completed successfully or intentional no-op | runtime outcome; verification if movement | plan/apply/no-op/verification | yes before close | yes |
| `FAILED_CLOSED` | Runtime failed and contained | failure result; no unsafe forward continuation | failure output, containment, rollback status | yes | yes |
| `ROLLED_BACK` | Runtime reverted to rollback target | rollback completed and verified where applicable | rollback result, target, verification | yes | yes |
| `DENIED` | Execution did not occur because denied | denial reason and no movement | gate/recheck/barrier/policy/trust/capacity reason | yes | yes if operation intent existed |
| `REPLAY_DENIED` | Replay/duplicate denied | replay detection | approval/operation/replay key | yes | yes |
| `CANCELLED` | Cancelled before terminal execution | actor/source/reason | cancellation reason | yes | yes |
| `EXPIRED` | Intent/approval/lifecycle expired | expiry timestamp/source | expiry/freshness evidence | yes | yes |

## 7. Audit Relationship

Audit must be written for:

- execution start and completion;
- execution failure;
- verification start/completion/failure;
- rollback start/completion/failure;
- denial/cancel/expiry/replay denial;
- closure state change.

Audit is complete when canonical `v7-audit-log` evidence can identify:

- operation identity/scope;
- runtime owner;
- actor/source;
- terminal state;
- affected users/targets or explicit no-op scope;
- selected-move hash/count or no-op/denial reason;
- rollback state if applicable;
- timestamp.

Audit is insufficient when:

- only stdout/journal exists for movement;
- only markdown report exists for current operation;
- selected moves/no-op reason is missing;
- rollback state is unknown;
- closure record exists without terminal runtime outcome.

Audit blocks closure when terminal runtime state exists but canonical audit evidence is missing or incomplete.

## 8. Closure Relationship

Closure may begin when:

- runtime terminal state exists; or
- operation intent was denied, cancelled, or expired.

Closure may finish when:

- terminal state is known;
- audit is sufficient;
- rollback is terminal or not applicable;
- closure actor and reason are present.

Closure can exist after rollback and after failure.

Closure can be reopened semantically by the closure owner with a later closure record, and that reopening must be audited.

Runtime Operation closure should not become `CLOSED` without runtime outcome or denial/cancel/expiry reason.

## 9. Rollback Relationship

Rollback begins when:

- verification fails and rollback is configured/available;
- runtime owner declares forward state unsafe;
- governed generic rollback is invoked with known scope.

Rollback ends when:

- rollback target is restored and verified; or
- generic rollback returns success with post-check evidence; or
- rollback fails and operation becomes `FAILED_CLOSED`.

Rollback is terminal as `ROLLED_BACK` or `FAILED_CLOSED`.

Rollback blocks closure if required but unknown, missing, failed without containment evidence, or unaudited.

## 10. No-Op Operations

No-op cases include:

- `selected_moves=0`;
- restore-barrier block;
- policy block;
- trust block;
- capacity block;
- dry-run;
- observe mode;
- autoswitch disabled;
- generation/hash/count mismatch;
- replay denial.

No-op is a Runtime Operation when runtime owner made a scheduled or operator-triggered decision.

No-op is not a Runtime Operation when it is only passive evidence.

No-op can close as:

- `COMPLETED` for ordinary intentional empty/no-op;
- `DENIED` for blocked/denied no-op;
- `REPLAY_DENIED` for replay no-op.

No-op audit must include reason, selected-move count/hash, blocker source, owner, timestamp, and scope.

## 11. End-to-End Operation Timeline

Final lifecycle:

runtime decision -> runtime terminal -> audit completion -> closure completion.

The runtime owner does not close operations. The closure owner does not determine runtime truth. The audit owner records canonical events.

## 12. Orchestrator Gap Impact

Already exists:

- planner;
- selected moves;
- restore-barrier validation;
- execution;
- verification;
- local movement rollback;
- audit sink;
- closure model.

Missing or partial:

- semantic operation identity across artifacts;
- terminal-state mapping from autoswitch apply result;
- guaranteed audit event for every runtime terminal state;
- no-op audit/closure coverage;
- global runtime recheck across manual paths;
- restore-barrier lifecycle audit linkage;
- closure blockers for insufficient audit/rollback evidence.

Needs ownership wiring only:

- runtime outcome -> audit event;
- audit event -> closure eligibility;
- selected moves/no-op reason -> operation timeline;
- rollback result -> terminal state and closure.

Requires future implementation only if Z6.6 authorizes it:

- any actual wiring, API, storage, event emission, or runtime mutation.

## 13. Truth Source Audit

No duplicate lifecycle truth:

- lifecycle is semantic composition of runtime terminal state, audit evidence, and closure record.

No duplicate operation truth:

- no new storage/API operation truth is created by Z6.5.

No duplicate closure truth:

- closure truth remains Admin closure records/operator observability.

No duplicate rollback truth:

- movement rollback truth remains runtime owner; generic rollback primitive supplies command result only.

No duplicate audit truth:

- audit truth remains `v7-audit-log`.

## 14. Final Verdicts

runtime_operation_model_defined=true

state_machine_defined=true

terminal_states_defined=true

audit_relationship_defined=true

closure_relationship_defined=true

rollback_relationship_defined=true

no_op_model_defined=true

lifecycle_truth_source_defined=true

implementation_scope_understood=true

safe_to_continue_to_Z6_6=true

## 15. Z6.6 Boundary

Z6.6 may proceed only if it preserves the semantic separation:

- runtime terminal state;
- audit completion;
- closure completion.

This report does not authorize implementation, API creation, storage creation, runtime mutation, deploy, service restart, route mutation, user movement, merge, or force push.

