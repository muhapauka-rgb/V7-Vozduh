# Relationship, No-Op, and Lineage Models

## Relationship Model

| Relationship | Direction | Authority | Dependency | Ownership |
|---|---|---|---|---|
| Operation -> Proposal | Operation references proposal as input | Proposal is advisory/governance input | Operation may exist without proposal for scheduled cycles | Admin owns proposal; runtime owner owns operation facts |
| Proposal -> Operation | Proposal may produce/bind operation intent | Not execution authority | Requires runtime owner decision to become operation | Admin owns proposal state |
| Operation -> Selected Moves | Operation includes selected move count/hash and executed set | Runtime authority | Required for movement; empty hash for no-op | Autoswitch owns selected moves |
| Operation -> Restore Barrier | Operation references barrier/generation if it affected admission | Runtime barrier authority | Required when barrier blocks/clears/allows operation | Autoswitch validates; Admin observes/closes lifecycle |
| Operation -> Runtime Outcome | Operation terminal state derives from runtime owner | Runtime authority | Required before audit/closure | Autoswitch owns outcome |
| Operation -> Rollback | Operation references rollback branch or rollback operation | Runtime/rollback authority | Required when movement failed/unsafe or rollback invoked | Autoswitch owns movement rollback; generic primitive owns command result |
| Operation -> Audit | Operation references canonical audit evidence | Audit authority | Required before closure | `v7-audit-log` owns audit truth |
| Operation -> Closure | Operation references closure record | Closure authority | Requires terminal runtime state and sufficient audit | Admin/operator closure owns closure truth |

## No-Op Operation Model

No-op operation receives `operation_id` when runtime owner makes an explicit decision.

| No-Op Type | Runtime Operation? | Operation Identity? | Audit? | Closure? | Terminal State |
|---|---:|---:|---:|---:|---|
| `selected_moves=0` no candidates | yes for scheduled/apply runtime cycle | yes | yes | yes | `COMPLETED` |
| policy denied | yes | yes | yes | yes | `DENIED` |
| trust denied | yes | yes | yes | yes | `DENIED` |
| capacity denied | yes | yes | yes | yes | `DENIED` |
| restore barrier denied | yes | yes | yes | yes | `DENIED` |
| replay denied | yes | yes | yes | yes | `REPLAY_DENIED` |
| dry-run | yes if operator/scheduled lifecycle is recorded; otherwise preview only | conditional | conditional | conditional | `COMPLETED` or preview-only outside operation |
| observe mode | yes if runtime cycle makes recorded no-op decision | yes | yes | yes | `COMPLETED` |
| passive evidence showing no selected moves | no | no | no | no | none |

## No-Op Required Attributes

- `operation_id`;
- `operation_type=no_op` or denial-specific type;
- `runtime_owner`;
- `created_at`;
- `selected_move_count=0`;
- `selected_move_hash`;
- no-op reason;
- blocker source if denied;
- planner generation if planner participated;
- barrier/policy/trust/capacity lineage if applicable;
- runtime terminal state;
- audit reference;
- closure reference when closed.

## Operation Lineage Questions

Future operators must answer:

What happened?

- operation type, runtime terminal state, closure state.

Why?

- planner reasons, denial/no-op reason, barrier/policy/trust/capacity inputs.

Who decided?

- runtime owner, scheduler/Admin/operator actor, approval lineage.

What moved?

- selected moves, affected users, source/target egress, selected-move hash.

What was denied?

- denial state, denial reason, gate/barrier/recheck verdict.

What rolled back?

- rollback scope, target, result, verification/containment.

What closed?

- closure record, closure actor, reason, timestamp, audit reference.

## Minimum Lineage Requirements

Every Runtime Operation must have:

- `operation_id`;
- operation type;
- runtime owner;
- source/actor;
- created timestamp;
- scope/no-op reason;
- selected-move count/hash;
- runtime terminal state;
- audit linkage before closure;
- closure linkage when closed.

Movement operations additionally require:

- affected users;
- source and target egress;
- verification result;
- rollback manifest/scope or explicit rollback-not-required reason.

Denied/no-op operations additionally require:

- denial/no-op reason;
- blocking authority;
- proof no movement occurred or selected-move count/hash.

Rollback operations additionally require:

- rollback reason;
- rollback target;
- rollback result;
- post-rollback verification or failed-closed containment.

