# Runtime Operation Object and Boundaries

## Existing Reality

No single current object fully represents a Runtime Operation.

Current operation meaning is distributed across:

- proposal record;
- execution contract/draft;
- autoswitch plan JSON;
- selected moves;
- restore barrier state;
- runtime recheck/gate results;
- autoswitch apply result;
- verification result;
- rollback result;
- audit event;
- closure record;
- historical operation report.

## Target Semantic Object

A Runtime Operation is a semantic lifecycle, not a new storage object in this design.

A Runtime Operation is:

- a bounded runtime decision lifecycle owned by the runtime owner;
- initiated by a plan/proposal/manual intent/scheduled cycle;
- scoped to one runtime decision set;
- associated with zero or more selected moves;
- associated with a runtime outcome;
- auditable through `v7-audit-log`;
- closable through Admin/operator closure records.

## What Is a Runtime Operation

| Case | Is Runtime Operation? | Reason |
|---|---:|---|
| single user movement | yes | Runtime mutation with selected user/target and verification/rollback needs. |
| multi-user movement | yes | Same lifecycle with larger scope/blast radius. |
| autoswitch no-op cycle | yes, if apply requested or runtime decision is recorded | Runtime owner made a terminal decision. |
| selected_moves=0 due to no candidates | yes as no-op runtime operation when scheduled/apply cycle runs | Runtime cycle completed with no movement. |
| blocked by restore barrier | yes as denied/no-op runtime operation | Runtime owner actively denied execution due to barrier. |
| blocked by policy/trust/capacity | yes as denied/no-op runtime operation if evaluated by lifecycle gates | Decision has governance meaning and should be auditable/closable. |
| rollback of a movement | yes | Runtime lifecycle branch or separate rollback operation if triggered independently. |
| failed movement | yes | Runtime operation with failure terminal or rollback branch. |
| cancelled movement | yes | Operation intent existed and was cancelled before terminal runtime mutation. |
| expired approval/contract | yes if operation intent existed | Lifecycle terminated without execution. |
| proposal only | not yet | Pre-operation input unless bound to runtime owner lifecycle. |
| evidence bundle only | not by itself | Supporting evidence. |
| audit event only | not by itself | Evidence of operation/action, not the lifecycle. |
| closure record only | not by itself | Terminal administrative state, not runtime operation source. |

## Boundary Rule

The operation lifecycle starts when an intent or scheduled runtime cycle becomes bounded enough to produce a runtime decision:

- scheduled autoswitch cycle;
- Admin/operator-approved runtime-owner action;
- execution contract/draft promoted to runtime owner decision;
- rollback action with known scope;
- no-op/denial with explicit reason.

The operation lifecycle does not start from passive evidence alone.

## Operation Identity Semantics

This design does not define storage or API identity. Semantically, an operation must be identifiable by:

- runtime owner;
- operation kind;
- time;
- selected-move set or no-op reason;
- affected users/targets when applicable;
- restore-barrier/generation context when applicable;
- audit/closure references.

