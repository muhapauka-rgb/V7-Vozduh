# E14 Operation Lineage Model

## Purpose

Lineage lets an operator replay an operation deterministically: what was
planned, what was approved, what was executed, what was blocked, what moved,
what was rolled back, and what evidence proved closeout.

## ID Model

| ID | Purpose |
|---|---|
| `operation_id` | Top-level governed lifecycle. |
| `approval_id` | Human approval contract. |
| `preview_id` | Read-only movement preview. |
| `movement_id` | Single user movement lineage row. |
| `rollback_manifest_id` | Rollback plan and verification scope. |
| `restore_id` | Restore lifecycle identity. |
| `monitor_id` | Delayed monitoring lifecycle. |
| `planner_generation_id` | Planner output identity. |
| `apply_generation_id` | Apply consumption identity. |
| `restore_generation_id` | Restore lifecycle generation. |
| `token_id` | Generation clearance or replay protection token. |
| `evidence_id` | Immutable evidence object. |

## Operation Phases

```text
draft
previewed
approval_pending
approved
held
movement_in_progress
observing
rollback_or_keep_pending
rollback_in_progress
planner_restore
restore_settle
apply_restore
delayed_monitoring
closed_clean
closed_blocked
contained
```

## Deterministic Replay

Replay requires:

- operation timeline;
- state hashes before approval;
- selected-move fingerprint;
- approval contract;
- generation token;
- movement lineage;
- switch-history refs;
- rollback manifest;
- restore lineage;
- delayed monitor samples;
- final mutation statement.

Replay distinguishes:

- planned movement;
- approved movement;
- executed movement;
- unexpected movement;
- blocked movement;
- rollback movement;
- no-op apply.

## Movement Lineage

Each movement row links:

- `movement_id`;
- `operation_id`;
- `approval_id`;
- user;
- from target;
- to target;
- selected-move fingerprint;
- switch-history event;
- route verification;
- rollback target;
- approved yes/no;
- classification if unapproved.

## Rollback Lineage

Rollback lineage links:

- forward operation;
- rollback approval;
- rollback manifest;
- per-user rollback target;
- execution order;
- route verification;
- runtime checker evidence;
- delayed monitor closeout.

## Evidence Lineage

Evidence metadata includes:

- evidence id;
- source path or tool;
- block id if historical;
- state source;
- collected_at;
- valid_until;
- supersedes/superseded_by;
- raw ref;
- summary hash.

Raw evidence should never be the only way to understand an operation.

## Target Lineage

Target lineage tracks:

- reservation state changes;
- readiness samples;
- capacity changes;
- target occupancy;
- pressure states;
- approved target use;
- blocked assignment attempts.

## Planner/Apply Lineage

Planner/apply lineage tracks:

- timer states;
- planner generation;
- selected-move set;
- apply generation;
- consumed token;
- apply outcome;
- recompute vs consume-approved behavior;
- journal refs.

## Replay Prevention

Replay is rejected when:

- token is consumed;
- token is expired;
- state hash drifted;
- planner generation changed;
- selected-move fingerprint changed;
- selected-move count exceeds budget;
- allowed users/targets differ;
- restore barrier id differs;
- approval is revoked.

## Operator Trust Model

The operator sees:

- current phase;
- approved scope;
- actual outcome;
- evidence freshness;
- replay status;
- safe next action.

The operator can drill down to raw evidence, but should not need raw evidence
to trust the phase verdict.

## E20 Execution Rehearsal Lineage

E20 adds preview-only immutable execution audit semantics:

- immutable approval ids;
- immutable execution ids;
- immutable denial ids;
- immutable replay rejection ids;
- append-only record hashes;
- previous-hash chain;
- denial lifecycle lineage;
- containment denial lineage.

This model is deterministic preview data only. It does not write a production
audit database and does not enable runtime execution.

## E21 Approval Packet Lineage

E21 requires the first real operator-driven action to create lineage before
runtime mutation:

- approval_created;
- approval_confirmed;
- runtime_recheck_passed or runtime_recheck_denied;
- approval_record_persisted;
- execution_stopped_before_runtime_mutation.

Any replay, stale runtime state, generation mismatch, hash mismatch, or approval
expiry creates a denial record instead of execution.

## E22 Audit Lineage Result

E22 writes append-only JSONL audit records for packet execution attempts. The
local run produced denial lineage:

- DENY_PACKET_INVALID for an invalid selected-move hash attempt;
- DENY_STALE_RUNTIME for missing live runtime registries;
- DENY_REPLAY for replaying the same approval id.

Each record includes `previous_record_hash` and `record_hash`, with runtime,
user, and routing mutation flags set to false.
