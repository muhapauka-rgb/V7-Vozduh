# Engineering Report: Decision Commit Contract Addendum

## Summary

Addendum к Decision Commit Point Behavior Contract завершен.

Код, Runtime, OMP, Backlog, owners и architecture не изменялись.

Добавлены три недостающих production-grade invariants:

1. Decision Commit Authority Contract
2. Commit Idempotency Contract
3. Commit Abort Contract

Вердикт:

`COMMIT_CONTRACT_ADDENDUM_COMPLETE`

## Action Performed

Прочитаны и сопоставлены:

- Decision Commit Point Behavior Contract Audit;
- Decision Commit Point Phase 0 Safety Audit;
- Master Implementation Justification Audit;
- Master Decision Ownership Audit;
- Runtime Model;
- Decision Model;
- OMP;
- Canonical Reference;
- SYSTEM_MAP.

Новые canonical owners или backlog items не созданы.

## 1. Decision Commit Authority Contract

Decision Commit means:

```text
The selected decision identity is fixed.
```

Decision Commit does not mean:

```text
Runtime may execute.
```

### Commit Owner

Existing implementation owner:

```text
admin_core/operator_execution_pipeline.py
```

Existing CLI orchestration owner:

```text
tools/v7-governed-canary-dry-run-cycle
```

Existing canonical owners:

- Decision Model;
- Runtime Model;
- OMP;
- Canonical Reference.

### Commit Authorizer

Decision Commit may be authorized only by existing read-only decision/pre-authority gates:

- OMP current task permits governed A4 flow;
- action class is known and mapped;
- current state can be read;
- decision surface exists;
- candidate selection is valid;
- pre-authority safety gates needed for READY preview pass;
- authority class is known;
- packet preview can be derived;
- rollback/no-rollback expectation is known;
- verification requirement is known.

### Gates Required Before Commit

Before commit, these must pass:

- task/context resolution;
- current state availability;
- candidate discovery;
- hard/soft failure or candidate reason classification;
- freshness sufficient for decision preparation;
- action-class mapping;
- subject/source/target selection;
- selected move hash generation;
- authority tier/generation read;
- rollback/no-rollback readiness preview;
- verification plan preview;
- blast-radius budget preview;
- no duplicate active execution lease for the same operation;
- no non-authority stop condition.

### Veto Owners

These existing owners may veto commit:

- Current Program State owner;
- OMP;
- Decision Model / decision surface owner;
- Runtime Model gate semantics;
- Policy 004 Authority;
- Policy 005 Action-Class Promotion;
- Policy 006 Blast Radius;
- Policy 007 Rollback;
- Policy 008 Freshness;
- Policy 009 Anti-Flap;
- Movement Protection owner;
- packet/lease owner;
- verification owner.

### Owners That Must Not Mutate Decision After Commit

After commit, these owners may validate but must not mutate the committed decision:

- Runtime;
- packet owner;
- execution lease owner;
- governed dry-run CLI;
- autoswitch/apply owner;
- restore barrier owner;
- verification owner;
- learning/outcome owner.

### GOVERNED_ONLY Rule

Decision Commit is allowed under current `GOVERNED_ONLY`.

It only freezes the selected decision identity.

It does not retire packet approval.

It does not grant execution authority.

Execution still requires:

```text
exact packet approval
  -> lease
  -> restore barrier
  -> live validation
  -> apply gate
  -> verification
```

## 2. Commit Idempotency Contract

Repeated commit for the same semantic Decision Snapshot must be idempotent.

Required rule:

```text
same semantic decision -> same committed decision id
different material decision -> new decision or STOP_SAFE
repeated commit -> no mutation, no duplicate lease, no duplicate operation
```

### Semantic Sameness Fields

These fields define the same semantic decision:

- action class;
- subject/user or approved subject scope;
- source channel;
- target channel;
- rollback target or no-rollback classification;
- selected move hash;
- authority tier;
- authority generation;
- blast-radius unit and budget;
- decision reason / failure family;
- service/user/policy fit class;
- verification requirement;
- material source/snapshot identity required for decision validity.

### Fields That Must Not Affect Committed Decision Identity

These fields must not create a new committed decision id by themselves:

- packet id;
- packet creation timestamp;
- preview timestamp;
- execution metadata;
- report path;
- non-material freshness timestamp changes;
- non-material source hash drift;
- diagnostic fields;
- JSON formatting/order;
- lease id;
- restore-barrier clearance id;
- operator prompt text;
- engineering report metadata.

### Material-Change Fields

These fields force a new decision or `STOP_SAFE`:

- subject/user or scope changes;
- source channel changes;
- target channel changes;
- rollback target changes;
- no-rollback classification changes;
- selected move hash changes;
- action class changes;
- authority tier/generation changes;
- blast-radius eligibility changes;
- rollback readiness changes;
- verification prerequisite changes;
- destination becomes ineligible;
- source becomes ineligible;
- failure/recovery family materially changes;
- policy generation changes;
- material state/source keys change.

### Side-Effect Rule

Decision Commit before lease must be side-effect free with respect to runtime:

- no apply;
- no user movement;
- no restore-barrier write;
- no lease creation unless explicitly requested by the existing lease owner;
- no duplicate operation;
- no maturity increase;
- no A4 evidence increase;
- no authority expansion;
- no runtime automation.

Repeated commit may update only read-only diagnostic/reporting output if explicitly part of the reporting path.

It must not mutate Current Program State unless OMP explicitly records a changed stop/progress state.

## 3. Commit Abort Contract

If commit succeeds but live validation later fails, the result is:

```text
STOP_SAFE
```

### Abort Behavior

Commit + live validation failure means:

- no apply;
- no user movement;
- no synthetic outcome;
- no A4 production outcome credit;
- no authority increase;
- no runtime automation;
- no certification increase.

### Historical Status

The committed decision may remain historical engineering evidence:

- decision was selected;
- packet/lease may or may not have been created;
- live validation blocked execution;
- no production movement occurred.

It is not a production outcome.

It is not proof of safe execution.

It is not class promotion evidence except as stop/diagnostic evidence.

### Lease Status

If no lease exists:

```text
LEASE_NOT_CREATED
```

If lease exists and validation fails before apply:

```text
LEASE_CANCELLED
```

or

```text
LEASE_EXPIRED
```

or

```text
LEASE_INVALIDATED_BY_MATERIAL_STATE_CHANGE
```

depending on the existing packet/lease owner result.

### Terminal Status

Terminal stop status must be one of the existing stop classes:

- `STOP_SAFE`;
- `OPERATIONAL_AUTHORITY`;
- `UNSAFE_IMPLEMENTATION`;
- `REAL_WORLD_LIMIT`;
- exact existing owner-specific blocker.

For this addendum, the required conceptual status is:

```text
STOP_SAFE_BEFORE_APPLY
```

if live validation fails after commit but before mutation.

### Learning / Evidence Rule

Learning may record:

- stop reason;
- veto owner;
- failed live validation gate;
- committed decision id;
- packet id if packet existed;
- lease id if lease existed;
- no movement;
- no verification outcome;
- no rollback outcome unless rollback actually ran.

Learning must not record:

- successful production outcome;
- successful rollback/no-rollback outcome;
- action-class certification evidence;
- trust increase from commit alone;
- synthetic verification.

### Engineering Report Rule

Engineering report must record:

- committed decision id;
- whether packet existed;
- whether lease existed;
- veto owner;
- failed gate;
- whether apply executed (`NO`);
- users moved (`0`);
- A4 evidence impact (`NONE`);
- next OMP step.

## A4 Evidence Impact

Decision Commit does not increase A4.

A4 increases only from real governed production outcome evidence:

```text
apply or certified no-rollback operational outcome
  -> immediate verification
  -> outcome closure
  -> learning from observed reality
```

Commit-only, packet-only, lease-only, stop-only, approval-only, dry-run-only, and validation-failed records do not satisfy A4 production outcome evidence.

## Validation

Confirmed:

- no new owner required;
- no new backlog required;
- no new architecture required;
- existing behavior contract remains valid;
- Phase 1 may use this addendum as implementation constraint.

## Existing Owner Mapping

| Contract area | Existing owner |
| --- | --- |
| Commit semantics | Decision Model / `admin_core/operator_execution_pipeline.py` |
| Commit orchestration | `tools/v7-governed-canary-dry-run-cycle` |
| Authority gates | OMP / Policy 004 / Policy 005 |
| Packet / lease | `admin_core/operator_execution.py` |
| Live validation / apply gate | Runtime Model / `tools/v7-users-autoswitch` |
| Rollback / restore barrier | `admin_core/operator_execution.py` / `tools/v7-users-autoswitch` |
| Verification / learning | feedback and learning owners |
| Current state reporting | Current Program State / OMP |

Need New Owner:

`FALSE`

Need New Backlog:

`FALSE`

Need New Architecture:

`FALSE`

## Next Step

Phase 1 may implement only against this addendum and the existing Behavior Contract.

Implementation must start with tests proving:

- authority does not expand at commit;
- repeated commit is idempotent;
- abort after commit records STOP_SAFE and gives no A4 evidence credit;
- exact `GOVERNED_ONLY` approval remains strict.

## Re-audit Rule

Do not repeat this addendum unless:

- Decision Commit implementation changes materially;
- authority model changes materially;
- A4 evidence criteria change materially;
- packet/lease owner changes materially;
- production evidence disproves this contract;
- explicit operator request.

## Final Verdict

`COMMIT_CONTRACT_ADDENDUM_COMPLETE`
