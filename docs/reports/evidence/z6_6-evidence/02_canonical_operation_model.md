# Canonical Runtime Operation Model

## Definition

A Runtime Operation is the canonical semantic envelope for one bounded runtime decision lifecycle.

It connects:

- planner;
- selected moves or no-op/denial reason;
- restore barrier;
- runtime recheck;
- execution;
- verification;
- rollback;
- audit;
- closure.

It does not introduce a new runtime owner, storage source, API, or orchestrator.

## What Is a Runtime Operation

| Case | Runtime Operation? | Boundary |
|---|---:|---|
| single user movement | yes | one operation scope with one user and target |
| multi-user movement | yes | one operation scope with multiple users/targets or batch |
| rollback | yes | branch of original operation or separate operation if independently invoked |
| no-op cycle | yes when runtime owner makes explicit scheduled/operator-triggered decision | selected_moves=0 or blocked/denied with reason |
| replay denial | yes | terminal operation attempt with replay reason |
| restore-barrier denial | yes | terminal denial/no-op with barrier lineage |
| policy denial | yes | terminal denial/no-op with policy lineage |
| trust denial | yes | terminal denial/no-op with trust lineage |
| capacity denial | yes | terminal denial/no-op with capacity lineage |
| proposal only | no | pre-operation intent |
| passive signal/evidence only | no | supporting evidence |
| closure record only | no | closure state only |
| audit event only | no | audit evidence only |

## Operation Identity

Canonical semantic identity:

`operation_id`

Required properties:

- stable across planner, execution, rollback, audit, and closure;
- not replaced by proposal/approval/contract/hash IDs;
- survives audit;
- survives closure;
- survives rollback;
- survives replay detection as the operation context while `approval_id` remains replay key;
- may be generated from existing operation-like lineage in future implementation, but this report does not define generation code.

## Operation Scope

Scope is the bounded subject of the operation:

- operation type;
- runtime owner;
- affected users;
- source/current targets;
- target egresses;
- selected move count/hash;
- no-op or denial reason;
- planner generation;
- restore-barrier context;
- runtime snapshot/fingerprints;
- rollback scope if applicable.

## Operation Lifetime

Starts when:

- runtime owner starts a scheduled decision cycle with apply/runtime intent; or
- Admin/operator intent is approved or bounded for runtime owner decision; or
- rollback is invoked with known scope; or
- a no-op/denial decision is explicitly produced by runtime owner.

Ends when:

- terminal runtime state exists;
- audit evidence is sufficient;
- closure owner records closure.

## Operation Lineage

Lineage links all non-primary identities:

- `proposal_id`;
- `contract_id`;
- `approval_id`;
- `packet_id`;
- `event_id`;
- selected-move hash/count;
- planner generation;
- runtime snapshot hash;
- restore-barrier generation/token/hash/count fields;
- audit event linkage;
- closure key;
- rollback result identifiers;
- evidence IDs.

## Operation Freshness

Freshness is not identity. It describes whether the operation can still be trusted for action/closure:

- runtime snapshot freshness;
- planner generation freshness;
- selected-move hash freshness;
- approval expiry;
- restore-barrier clearance expiry;
- audit completeness freshness;
- closure state freshness.

## Operation Ownership

| Layer | Owner |
|---|---|
| runtime facts | `tools/v7-users-autoswitch` |
| execution | `tools/v7-users-autoswitch` |
| selected moves | `tools/v7-users-autoswitch` |
| audit | `tools/runtime-support/v7-audit-log` |
| closure | `admin/v7-admin-api` + `admin_core/operator_observability.py` |
| proposal/approval surface | Admin/operator components |
| low-level movement primitive | `v7-user-switch` under runtime owner/operator boundary |
| generic rollback primitive | `tools/runtime-support/v7-rollback-last-change` under rollback boundary |

