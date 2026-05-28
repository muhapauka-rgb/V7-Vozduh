# E13 Observability Model

## Purpose

Observability must make governed orchestration explainable. It should show
lineage and decisions, not just metrics.

## Timeline View

Every operation has a timeline:

1. preview generated;
2. approval created;
3. generation token issued;
4. timer state changed if applicable;
5. movement executed if applicable;
6. rollback or keep decision;
7. planner restore;
8. restore-settle samples;
9. apply restore;
10. delayed monitor samples;
11. final verdict.

Each timeline event includes:

- timestamp;
- actor/system source;
- state hash;
- generation id;
- selected-move count;
- evidence link;
- mutation statement if any.

## Operation Replay

Operation replay is a read-only reconstruction:

- what was approved;
- what actually happened;
- what was blocked;
- what moved;
- what did not move;
- rollback result;
- delayed monitoring result.

Replay must distinguish planned, approved, executed, blocked, and observed
states.

## Movement Lineage

For each user movement:

- user;
- from target;
- to target;
- reason;
- approved operation id;
- selected-move fingerprint;
- rollback target;
- switch-history row;
- route verification.

Unapproved movement is marked as an incident lineage, not folded into normal
history.

## Restore Lineage

Restore lineage links:

- rollback/keep decision;
- planner restore;
- restore-settle gate;
- apply restore;
- restore barrier;
- generation clearance;
- delayed monitor closeout.

Restore is incomplete until delayed monitoring is clean or explicitly blocked.

## Generation Lineage

Generation lineage links:

- planner generation;
- selected-move fingerprint;
- generation token;
- token expiry/consumption;
- apply generation;
- replay rejection events;
- mismatch reasons.

This is summarized in the UI and expandable to raw contract JSON.

## Planner/Apply Lineage

Planner/apply lineage shows:

- planner timer state;
- apply timer state;
- latest planner output;
- latest apply outcome;
- whether apply recomputed or consumed approved generation;
- journal evidence;
- timer overlap warnings.

## Selected Moves Lineage

Selected moves are tracked as a sequence:

- count;
- fingerprint;
- candidates total;
- blocked reasons;
- budget;
- generation id;
- state source.

This prevents `selected_moves=0` from being interpreted without context.

## Target Pressure Lineage

Target pressure is summarized:

- service signal pressure;
- rebalance pressure;
- failover pressure;
- target capacity pressure;
- reservation pressure.

Pressure is not an approval. It is evidence that may generate a preview.

## Delayed Movement Lineage

Delayed movement monitoring stores:

- sample id;
- registry hash;
- switch-history count;
- selected moves;
- hidden mover scan;
- runtime checks;
- target readiness;
- verdict.

The UI shows the sample chain and lets raw evidence expand from each sample.

## Search And Archive

Searchable keys:

- operation id;
- block id;
- user;
- target;
- generation token;
- selected-move fingerprint;
- rollback manifest;
- report title;
- mutation statement.

Archive rules:

- final reports remain canonical;
- evidence bundles remain linked;
- superseded evidence is labeled;
- raw command output is kept behind evidence viewer.

## Summary Vs Detail

Overview summary:

- status;
- affected users;
- blockers;
- next safe action.

Expandable detail:

- exact evidence;
- raw JSON;
- journal slices;
- registry rows.

The operator should never need to read raw logs to understand whether an
operation is safe, but raw logs must be one click away for audit.

