# PROGRAM Z6.6 - Runtime Operation Model Design Report

Project: V7 Vozduh
Branch target: `v7-next`
Mode: READ ONLY operation semantics design
Date: 2026-06-02

## Executive Verdict

The canonical Runtime Operation model is defined as a semantic envelope around existing V7 artifacts.

Canonical operation identity:

`operation_id`

`operation_id` is not a new storage object, API, database design, or runtime owner. It is the semantic identity that connects existing planner, selected-move, restore-barrier, execution, rollback, audit, and closure facts.

All other identifiers are lineage identifiers:

- `proposal_id`;
- `contract_id`;
- `approval_id`;
- `packet_id`;
- `event_id`;
- `record_hash`;
- selected-move hash/count;
- planner generation;
- runtime snapshot hash;
- restore-barrier identifiers;
- audit linkage;
- closure key;
- evidence IDs.

## Evidence Directory

`z6_6-evidence`

- `00_identity_discovery.md`
- `01_operation_like_objects.md`
- `02_canonical_operation_model.md`
- `03_operation_attributes_and_timeline.md`
- `04_relationship_noop_lineage_models.md`
- `05_readiness_truth_audit.md`
- `06_final_verdicts.md`

## 1. Existing Identity Discovery

| Identifier | Owner | Scope | Truth Source | Reuse |
|---|---|---|---|---|
| `operation_id` | operator observability / operator execution packets | operation-like lineage | reports, operator packets, observability | canonical semantic operation identity |
| `proposal_id` | Admin proposal model | proposal input | proposal records | linked input |
| `contract_id` | Admin execution contract model | execution contract/draft | execution contract model | contract lineage |
| `event_id` | Admin execution event model | execution event | execution event model | event lineage |
| `approval_id` | operator execution packet | approval/replay boundary | operator execution records | approval lineage/replay key |
| `packet_id` | operator packet | packet | packet evidence | packet lineage |
| `record_hash` | operator execution audit chain | audit record integrity | operator execution audit | audit-chain lineage |
| `planner_generation_id` | autoswitch | planner input generation | autoswitch generation status | runtime generation lineage |
| selected-move hash | autoswitch / operator recheck | selected move set | autoswitch plan/recheck | selected-move fingerprint |
| `runtime_snapshot_hash` | operator recheck | runtime snapshot | operator recheck | snapshot lineage |
| restore-barrier identifiers | autoswitch/Admin | barrier clearance/generation | barrier interpreted by autoswitch | barrier lineage |
| closure key | Admin closure model | closure object | closure records | closure lineage |
| audit object/request fields | `v7-audit-log` | audit linkage | audit JSONL | audit linkage |
| evidence IDs | Admin/operator evidence | evidence references | evidence model | evidence lineage |

## 2. Existing Operation-Like Objects

| Object | Operation-Like Strength | Limitation | Reuse |
|---|---|---|---|
| Proposal | reason, users, target, evidence, `proposal_id` | does not execute | pre-operation intent |
| Execution contract | status model, users/targets, rollback manifest, `contract_id` | preview-only/non-authoritative today | contract lineage |
| Approval packet | `operation_id`, `approval_id`, hashes, expiry, approvals | zero-move/currently limited | approval lineage |
| Selected move set | runtime-selected scope and hash | not full operation | operation scope/fingerprint |
| Autoswitch plan/apply | runtime owner facts and terminal outcome | not linked to audit/closure yet | runtime operation facts |
| Restore barrier | admission/denial/generation context | not operation by itself | barrier lineage |
| Audit event | canonical event evidence | not operation by itself | audit evidence |
| Closure record | lifecycle closure | not runtime truth | closure evidence |
| Historical operation summary | `operation_id`, report lineage, evidence refs | historical/read-only | historical lineage |

Partial operation object exists, but not complete:

- `operation_id` exists in operator/historical contexts.
- autoswitch plan/apply contains runtime facts.
- canonical operation model must connect them without creating duplicate truth.

## 3. Canonical Operation Definition

A Runtime Operation is one bounded runtime decision lifecycle.

It is:

- owned by `tools/v7-users-autoswitch` for runtime facts;
- identified semantically by `operation_id`;
- scoped by users/targets/selected moves or no-op reason;
- linked to planner generation and runtime fingerprints;
- linked to restore-barrier context when relevant;
- linked to execution/verification/rollback outcomes;
- linked to canonical audit evidence;
- linked to closure record.

Runtime Operations include:

- single user movement;
- multi-user movement;
- rollback;
- no-op cycle;
- replay denial;
- restore-barrier denial;
- policy/trust/capacity denial;
- cancellation/expiry when operation intent existed.

Not Runtime Operations by themselves:

- proposal only;
- passive signal/evidence only;
- audit event only;
- closure record only;
- selected-move hash alone;
- restore-barrier state alone.

## 4. Operation Identity Model

Operation Identity:

- canonical semantic identity is `operation_id`.

Operation Scope:

- operation type;
- runtime owner;
- source/actor;
- affected users;
- source/current targets;
- target egresses;
- selected move count/hash;
- no-op/denial reason;
- planner generation;
- restore-barrier context;
- runtime snapshot/fingerprints;
- rollback scope.

Operation Lifetime:

- starts when scheduled runtime cycle, operator intent, approved action, rollback action, or explicit no-op/denial becomes bounded for runtime owner decision;
- ends after runtime terminal state, sufficient audit, and closure record.

Operation Lineage:

- all non-operation IDs attach to `operation_id` as lineage references.

Operation Freshness:

- freshness is metadata, not identity;
- approval expiry, runtime snapshot freshness, planner generation freshness, selected-move freshness, barrier clearance expiry, audit completeness, and closure state can all affect whether operation can proceed or close.

Operation Ownership:

- runtime facts: `tools/v7-users-autoswitch`;
- audit facts: `v7-audit-log`;
- closure facts: Admin/operator observability;
- proposal/approval facts: Admin/operator components.

What uniquely identifies an operation:

`operation_id` plus immutable semantic scope: runtime owner, operation type, created time/source, selected-move/no-op scope, and lineage references.

What survives audit:

- `operation_id`;
- terminal state;
- audit linkage;
- selected-move/no-op scope;
- actor/source;
- affected users/targets.

What survives closure:

- `operation_id`;
- closure key/record;
- closure actor/reason/timestamp;
- terminal runtime and audit references.

What survives rollback:

- original `operation_id`;
- rollback branch/result;
- rollback target/scope;
- rollback audit/closure lineage.

What survives replay detection:

- `operation_id` as operation context;
- `approval_id` as replay key;
- record hash chain as replay/audit proof.

## 5. Operation Attributes

Mandatory semantic attributes:

- `operation_id`;
- `created_at`;
- `runtime_owner`;
- `operation_type`;
- `source`;
- `scope`;
- `selected_move_count`;
- `selected_move_hash`;
- `runtime_state`;
- `runtime_verdict` after terminal;
- `audit_verdict` before closure;
- `closure_verdict` for lifecycle end.

Conditional attributes:

- `planner_generation_id`;
- `runtime_snapshot_hash`;
- `proposal_id`;
- `contract_id`;
- `approval_id`;
- `packet_id`;
- restore-barrier lineage;
- rollback state/verdict/scope;
- audit refs;
- closure ref;
- evidence refs.

## 6. Operation Timeline Model

An operation accumulates history as ordered semantic facts.

Planner attaches:

- planner generation;
- selected move count/hash;
- candidate/no-op/denial reason;
- policy/trust/capacity/barrier inputs.

Execution attaches:

- execution start;
- selected moves executed;
- command/result summary;
- affected users/targets;
- verification requirement/result.

Rollback attaches:

- rollback reason;
- rollback scope;
- rollback target;
- rollback result;
- rollback verification/containment.

Audit attaches:

- action/component;
- object linkage;
- actor/source;
- result;
- timestamp;
- request/object identifiers;
- before/after hashes when relevant.

Closure attaches:

- closure object key;
- closure state;
- closure reason;
- closure actor;
- closure timestamp;
- audit reference;
- runtime terminal state reference.

## 7. Relationship Model

| Relationship | Direction | Authority | Dependency | Owner |
|---|---|---|---|---|
| Operation <-> Proposal | operation references proposal as input | proposal advisory | optional | Admin proposal owner |
| Operation <-> Selected Moves | operation includes selected count/hash | runtime authority | required for movement/no-op proof | autoswitch |
| Operation <-> Restore Barrier | operation references barrier if it affected admission | runtime barrier authority | conditional | autoswitch validates, Admin observes |
| Operation <-> Runtime Outcome | terminal state derives from runtime owner | runtime authority | required | autoswitch |
| Operation <-> Rollback | operation links rollback branch/result | runtime/rollback authority | conditional | autoswitch / rollback primitive |
| Operation <-> Audit | operation links canonical audit evidence | audit authority | required before closure | `v7-audit-log` |
| Operation <-> Closure | operation links closure record | closure authority | required for lifecycle close | Admin/operator closure |

## 8. No-Op Operation Model

No-op operation receives `operation_id` when runtime owner makes an explicit decision.

| No-Op Case | Operation Identity | Audit | Closure | Terminal |
|---|---:|---:|---:|---|
| selected_moves=0 | yes | yes | yes | `COMPLETED` |
| policy denied | yes | yes | yes | `DENIED` |
| trust denied | yes | yes | yes | `DENIED` |
| capacity denied | yes | yes | yes | `DENIED` |
| restore barrier denied | yes | yes | yes | `DENIED` |
| replay denied | yes | yes | yes | `REPLAY_DENIED` |
| dry-run | conditional: operation only if lifecycle is recorded | conditional | conditional | `COMPLETED` or preview-only outside operation |
| observe mode | yes if recorded runtime decision | yes | yes | `COMPLETED` |
| passive evidence of zero selected moves | no | no | no | none |

No-op required lineage:

- `operation_id`;
- reason;
- selected_move_count=0;
- selected_move_hash;
- blocker source if denied;
- planner generation if planner participated;
- runtime terminal state;
- audit reference;
- closure reference when closed.

## 9. Operation Lineage Model

Minimum lineage requirements:

- operation id;
- operation type;
- runtime owner;
- source/actor;
- created timestamp;
- scope/no-op reason;
- selected-move count/hash;
- runtime terminal state;
- audit linkage before closure;
- closure linkage when closed.

Movement operation lineage:

- affected users;
- source/target egress;
- selected-move hash;
- verification result;
- rollback manifest/scope or explicit rollback-not-required reason.

Denied/no-op operation lineage:

- denial/no-op reason;
- blocking authority;
- proof no movement occurred.

Rollback lineage:

- rollback reason;
- rollback target;
- rollback result;
- post-rollback verification or failed-closed containment.

Future operator questions answered:

- What happened? Operation state/verdict.
- Why? Planner/no-op/denial/barrier/policy/capacity/trust reasons.
- Who decided? Runtime owner, scheduler/Admin/operator, approval lineage.
- What moved? Selected moves and affected users/targets.
- What was denied? Denial reason and blocking authority.
- What rolled back? Rollback scope/result.
- What closed? Closure record and audit reference.

## 10. Orchestrator Readiness Impact

Estimated operation model already exists: 55%.

Already exists:

- `operation_id` in operator contexts;
- proposal/contract/approval IDs;
- selected-move hashes;
- planner generation;
- runtime snapshot hashes;
- restore-barrier lineage fields;
- audit sink fields;
- closure object keys;
- historical operation summaries.

Needs ownership wiring only:

- autoswitch runtime cycle to `operation_id`;
- operation identity into audit linkage;
- operation identity into closure key;
- selected-move/generation/no-op reason into operation timeline;
- rollback result into operation timeline.

Requires future implementation:

- concrete ID generation logic;
- event emission;
- API/storage representation;
- runtime wiring;
- audit/closure enforcement.

Requires no work:

- owner selection;
- state machine semantics;
- lifecycle terminal definitions;
- audit/closure ownership anchors.

## 11. Truth Source Audit

No duplicate operation truth:

- Runtime Operation is a semantic envelope over existing facts.

No duplicate operation identity:

- canonical identity is existing `operation_id`.

No duplicate audit identity:

- audit remains `v7-audit-log`; execution event IDs remain event lineage.

No duplicate closure identity:

- closure remains Admin closure key/records.

No duplicate rollback identity:

- rollback remains operation-linked branch/result.

No duplicate lineage identity:

- lineage is a set of existing linked IDs, not a new competing ID.

## 12. Final Verdicts

runtime_operation_identity_defined=true

runtime_operation_scope_defined=true

runtime_operation_attributes_defined=true

runtime_operation_timeline_defined=true

runtime_operation_relationships_defined=true

runtime_operation_lineage_defined=true

no_op_operation_model_defined=true

operation_truth_source_defined=true

implementation_scope_understood=true

safe_to_continue_to_Z6_7=true

## 13. Z6.7 Boundary

Z6.7 may proceed only if it preserves:

- `operation_id` as canonical semantic operation identity;
- existing IDs as lineage, not replacement operation identities;
- autoswitch as runtime truth owner;
- `v7-audit-log` as audit truth owner;
- Admin/operator observability as closure truth owner.

This report does not authorize implementation, API creation, storage creation, runtime mutation, deploy, service restart, route mutation, user movement, merge, or force push.

