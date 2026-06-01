# PROGRAM Z7.1 - Ownership Wiring Reality Audit Report

Project: V7 Vozduh  
Branch target: v7-next  
Date: 2026-06-02  
Mode: READ ONLY reality audit  
Evidence directory: `z7_1-evidence`

## Executive Verdict

The Runtime Orchestrator Program exists only partially in working code.

Runtime mechanics are real and owned by `tools/v7-users-autoswitch`, but the end-to-end ownership wiring is not yet connected:

```text
Runtime -> Operation -> Audit -> Closure
PARTIAL -> PARTIAL -> PARTIAL -> PARTIAL
```

The most important gap is that `operation_id` exists in operator/governance/historical layers, but is not present in `tools/v7-users-autoswitch`. Therefore live autoswitch plans, selected moves, execution results, verification results, rollback results, and terminal runtime outcomes are not yet bound to canonical runtime operations.

## Discovery Gate Result

Inventory was completed before any implementation planning.

| Area | Reality |
|---|---|
| Ownership wiring | PARTIAL |
| Lifecycle wiring | PARTIAL |
| Operation wiring | PARTIAL |
| Audit wiring | PARTIAL |
| Closure wiring | PARTIAL |
| Rollback wiring | PARTIAL |
| Runtime recheck wiring | PARTIAL |
| Selected-move wiring | PARTIAL |
| Restore-barrier wiring | PARTIAL |
| `operation_id` wiring | PARTIAL in operator/governance, MISSING in autoswitch runtime |

## What Already Exists in Working Code

### Runtime owner

`tools/v7-users-autoswitch` already owns:

- planning,
- selected move calculation,
- `planner_generation_id`,
- restore barrier reading,
- generation clearance checks,
- selected move hash calculation,
- guarded apply,
- `v7-user-switch` execution,
- route verification,
- rollback-on-verify-fail,
- JSON runtime output.

Classification: REUSE, EXTEND.

### Scheduler

The autoswitch systemd timer/service remains the canonical scheduler.

Classification: REUSE.

### Audit owner

`tools/runtime-support/v7-audit-log` exists and writes canonical audit events. It supports metadata and `request_id`, but does not have a first-class `operation_id` field.

Classification: REUSE, EXTEND.

### Closure owner

Admin closure model exists in `admin/v7-admin-api` with JSONL closure records, `closure-set`, closure states, and Admin audit.

Classification: REUSE, EXTEND.

### Operator operation model

`admin_core/operator_observability.py` exposes historical/read-only operation lineage by `operation_id`, including operation detail, audit search, audit export preview, execution governance preview, and rehearsal preview.

Classification: REUSE.

### Governance packet model

`admin_core/operator_execution.py` can validate packets, run zero-move runtime rechecks, and write append-only governance/audit records with `operation_id`, `approval_id`, and `packet_id`.

Classification: REUSE, EXTEND.

## Phase Findings

### Phase 1 - Operation Identity Wiring

`operation_id` exists in:

- operator execution governance records,
- operator observability historical operation summaries,
- Admin operator endpoints,
- P2.7 candidate/governance/rehearsal surfaces.

`operation_id` does not exist in:

- `tools/v7-users-autoswitch`,
- `tools/runtime-support/v7-audit-log` as first-class field,
- `tools/runtime-support/v7-rollback-last-change`.

Status: PARTIAL.

### Phase 2 - Runtime to Operation Wiring

Autoswitch outputs runtime facts, but not canonical operation identity.

| Runtime Fact | Existing | Bound to `operation_id` |
|---|---:|---:|
| selected moves | yes | no |
| selected move hash | yes, internal/guard detail | no |
| planner generation | yes | no |
| restore barrier status | yes | no |
| apply result | yes | no |
| verification result | yes | no |
| rollback result | yes | no |
| terminal runtime state | partial as result/reason | no |

Status: PARTIAL/MISSING.

### Phase 3 - Operation to Audit Wiring

Connected:

- Admin action audit to `v7-audit-log`.
- Closure-set audit to `v7-audit-log`.
- Generic rollback audit to `v7-audit-log`.
- Operator execution governance audit includes `operation_id`.

Missing:

- Autoswitch terminal runtime result to `v7-audit-log` with `operation_id`.
- First-class runtime operation audit event.

Status: PARTIAL.

### Phase 4 - Operation to Closure Wiring

Connected:

- Admin closure store and closure-set endpoint.
- Closure metadata attaches to Admin proposal/evidence/runtime/release/trust/drift objects.

Missing:

- Autoswitch runtime operation id as closure object id.
- Automatic or explicit link from autoswitch terminal runtime result to closure.

Status: PARTIAL.

### Phase 5 - Rollback Wiring

Connected:

- Autoswitch rollback-on-verify-fail.
- Generic rollback primitive.
- Admin rollback preview/apply.
- Admin direct-switch rollback on proxy failure.

Missing:

- Rollback lineage bound to `operation_id`.

Duplicated:

- Autoswitch rollback, generic rollback, Admin rollback apply, and Admin manual rollback are multiple rollback paths.

Status: PARTIAL/DUPLICATED.

### Phase 6 - Restore Barrier Wiring

Connected:

- Autoswitch reads restore barrier.
- Autoswitch enforces generation token, generation match, selected move hash, selected move count, and clearance expiry.
- Admin/operator read adapters expose barrier status.

Missing:

- Restore-barrier lifecycle bound to `operation_id`.

Status: PARTIAL.

### Phase 7 - Runtime Recheck Wiring

Connected:

- Autoswitch performs runtime guard checks before apply.
- Operator execution packet path performs zero-move runtime recheck using registry hashes, selected move hash, and `runtime_snapshot_hash`.

Missing:

- Shared `operation_id` lineage across autoswitch recheck and operator recheck.

Status: PARTIAL.

## Full Wiring Map

```text
Runtime
  Owner: tools/v7-users-autoswitch
  Status: PARTIAL
  Missing: operation_id

Operation
  Owner: canonical operation_id model in operator/governance surfaces
  Status: PARTIAL
  Missing: live autoswitch binding

Audit
  Owner: tools/runtime-support/v7-audit-log
  Status: PARTIAL
  Missing: autoswitch terminal operation audit event

Closure
  Owner: admin/v7-admin-api + admin_core/operator_observability.py
  Status: PARTIAL
  Missing: autoswitch operation closure object binding
```

## Connected / Partial / Missing

| Orchestrator Component | Status |
|---|---|
| Scheduler -> runtime owner | CONNECTED |
| Runtime owner -> selected moves | CONNECTED |
| Runtime owner -> selected move hash | PARTIAL |
| Runtime owner -> planner generation | CONNECTED |
| Runtime owner -> restore barrier | CONNECTED |
| Runtime owner -> runtime recheck | PARTIAL |
| Runtime owner -> execution | CONNECTED |
| Runtime owner -> verification | CONNECTED |
| Runtime owner -> rollback | CONNECTED |
| Runtime owner -> `operation_id` | MISSING |
| `operation_id` -> operator observability | CONNECTED |
| `operation_id` -> governance audit | CONNECTED |
| `operation_id` -> live runtime audit | MISSING |
| live runtime audit -> closure | MISSING |
| Admin closure object model | CONNECTED |
| generic rollback -> audit | CONNECTED |
| generic rollback -> `operation_id` | MISSING |

## Duplication Audit

| Area | Risk |
|---|---|
| Duplicate operation flows | MEDIUM |
| Duplicate lifecycle flows | MEDIUM |
| Duplicate audit flows | MEDIUM |
| Duplicate closure flows | LOW/MEDIUM |
| Duplicate rollback flows | HIGH |
| Duplicate selected-move flows | MEDIUM |
| Duplicate operation identities | MEDIUM |
| Duplicate orchestrator wiring | MEDIUM/HIGH if Admin/direct/draft paths are promoted |
| Duplicate ownership wiring | MEDIUM |

Verdict:

Planned wiring would duplicate existing work if it creates new owners or truth sources. It would not duplicate existing work if it only wires existing autoswitch runtime facts into existing `operation_id`, `v7-audit-log`, and Admin closure models.

## Implementation Readiness

No work required:

- scheduler,
- runtime owner,
- selected move calculation,
- selected move hash primitive,
- planner generation primitive,
- restore barrier enforcement,
- audit sink,
- closure store,
- operator observability.

Ownership consolidation only:

- Admin direct user switch,
- Admin rollback apply,
- generic rollback,
- execution contract/event store,
- operator packet recheck,
- draft planner scheduler.

Minimal code later:

- autoswitch `operation_id` binding,
- autoswitch output lineage fields,
- runtime terminal audit event,
- closure object binding,
- rollback/break-glass operation metadata.

Significant code should be avoided unless later proven necessary:

- new orchestrator,
- new scheduler,
- new execution engine,
- new rollback engine,
- new operation store,
- new audit sink,
- new closure store.

## Truth Source Audit

| Truth Source | Verdict |
|---|---|
| Operation truth | Existing `operation_id` model should be reused; not yet runtime-connected |
| Lifecycle truth | Fragmented; autoswitch terminal result plus audit plus closure not yet wired |
| Audit truth | `v7-audit-log` remains canonical |
| Closure truth | Admin closure model remains canonical |
| Rollback truth | Autoswitch owns normal rollback; generic rollback is break-glass primitive |
| Lineage truth | Partial; operator/governance lineage exists, runtime lineage missing |

## Final Verdicts

```text
operation_wiring_understood=true
audit_wiring_understood=true
closure_wiring_understood=true
rollback_wiring_understood=true
restore_barrier_wiring_understood=true
runtime_recheck_wiring_understood=true
implementation_readiness_understood=true
safe_to_continue_to_Z7_2=true
```

## Safety Statement

Z7.1 performed no implementation, no refactor, no API creation, no storage creation, no runtime mutation, no routing mutation, no user movement, no autoswitch apply, no deploy, no service restart, no systemd modification, no timer modification, no cleanup, no deletion, no merge, and no force push.

