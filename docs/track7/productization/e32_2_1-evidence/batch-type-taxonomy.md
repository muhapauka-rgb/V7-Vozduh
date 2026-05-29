# E32.2.1 Batch Type Taxonomy

batch_type_taxonomy_defined=true

## Batch Types

### OPERATOR_MOVEMENT_BATCH

Purpose:

Move an exact approved user set from known source targets to one approved destination target.

Allowed use:

- bounded operator-driven movement;
- capacity-certified target migration;
- first proof of a class or production-pool controlled movement.

Forbidden use:

- autoswitch execution;
- hidden movement;
- implicit candidate expansion;
- movement outside the packet scope.

Required gates:

- approval packet;
- execution-time recheck;
- capacity gate;
- restore-settle;
- runtime checkers;
- rollback manifest.

Rollback behavior:

Default rollback to original source target per user.

### ROLLBACK_BATCH

Purpose:

Return a previously moved exact user set to known rollback targets.

Allowed use:

- default rollback after proof;
- containment after failed verification;
- return from stale/degraded/expired capacity state.

Forbidden use:

- expansion beyond known rollback scope;
- movement to new destination targets;
- non-containment optimization.

Required gates:

- exact rollback manifest;
- route table mapping;
- no blast-radius expansion;
- runtime safety checks where available.

Rollback behavior:

This batch is itself rollback.

### EVACUATION_BATCH

Purpose:

Move users off a target that must be drained.

Allowed use:

- target degradation;
- target expiration;
- operator-requested target emptying.

Forbidden use:

- unbounded redistribution;
- autoswitch-style target selection without policy;
- moving users to uncertified destinations.

Required gates:

- evacuation plan;
- allowed destination set;
- capacity gates for receiving targets;
- rollback or containment strategy.

Rollback behavior:

Rollback may be per-user original target or containment target depending on incident type.

### CAPACITY_REBALANCE_BATCH

Purpose:

Redistribute users between certified targets to satisfy capacity or policy constraints.

Allowed use:

- production-pool capacity balancing after policy engine certification;
- controlled operator-approved rebalance.

Forbidden use:

- replacing autoswitch apply without governance;
- using uncertified or stale targets;
- exceeding reservation or policy caps.

Required gates:

- policy engine approval;
- capacity availability;
- reservation ledger;
- exact user set;
- audit lineage.

Rollback behavior:

Rollback returns each user to the pre-batch source target unless containment is safer.

### STAGED_MIGRATION_BATCH

Purpose:

Move a larger planned migration through ordered sub-batches.

Allowed use:

- staged production-pool rollout;
- CLASS_20/50/100 proof programs;
- low-risk migration sequencing.

Forbidden use:

- collapsing stages into unbounded execution;
- continuing after a failed stage without recertification;
- skipping observation and restore-settle gates.

Required gates:

- per-stage approval packet;
- per-stage capacity gate;
- stage stop condition;
- cumulative audit lineage.

Rollback behavior:

Rollback may be per-stage or whole-plan depending on the migration contract.

### CONTAINMENT_BATCH

Purpose:

Perform minimum necessary safe action to reduce risk during failure.

Allowed use:

- rollback after failed verification;
- isolate users from revoked target;
- resolve exact known unsafe placement.

Forbidden use:

- opportunistic optimization;
- target expansion;
- non-essential movement.

Required gates:

- incident or failure trigger;
- exact affected user set;
- no blast-radius expansion;
- audit record.

Rollback behavior:

Containment may not have a normal rollback if it is already the safer terminal state; this must be explicit.

## Taxonomy Verdict

Batch type taxonomy is defined and preserves the certified governance boundary.

