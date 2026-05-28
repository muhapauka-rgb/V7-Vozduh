# E14 Operator Overview State Model

## Purpose

The operator overview needs one top-level state derived from many governance
objects. This state must be explainable, deterministic, and conservative.

## Top-Level States

| State | Meaning |
|---|---|
| `SAFE` | Runtime checks clean, no selected moves, no active blockers, no stale critical evidence. |
| `CONDITIONAL` | Runtime clean but action requires explicit approval, capacity limit, generation token, or known blocker remains. |
| `BLOCKED` | A required safety gate fails or execution is disallowed. |
| `STALE` | Critical live truth is missing, expired, conflicting, or historical-only. |
| `DEGRADED` | Service or target health reduced, but no immediate unsafe mutation observed. |
| `REPLAY_RISK` | Token, generation, selected-move fingerprint, or approval replay risk exists. |
| `RESTORE_PENDING` | Restore lifecycle is active or delayed monitor not closed. |
| `MOVEMENT_PENDING` | A movement preview or approval exists but has not closed. |
| `CONTAINED` | Emergency containment is active after unexpected movement or hidden apply risk. |

## Derivation Order

Conservative precedence:

1. `CONTAINED`
2. `REPLAY_RISK`
3. `BLOCKED`
4. `STALE`
5. `RESTORE_PENDING`
6. `MOVEMENT_PENDING`
7. `DEGRADED`
8. `CONDITIONAL`
9. `SAFE`

Higher-precedence states win even if lower-level checks are clean.

## Derivation Rules

### SAFE

Requires:

- runtime health OK;
- selected moves count zero;
- hidden mover absent;
- planner/apply states expected;
- WireGuard/reserved target state consistent;
- no active restore or movement;
- evidence fresh.

### CONDITIONAL

Applies when:

- runtime is clean;
- larger cohort remains NO-GO or conditional;
- action requires separate approval;
- read-only UI is allowed but execution is not;
- target readiness GO exists but movement approval is absent.

### BLOCKED

Applies when:

- runtime checker fails;
- target readiness NO-GO;
- restore-settle NO-GO;
- selected moves exceed approved budget;
- rollback manifest missing for movement approval;
- hard capacity limit would be exceeded.

### STALE

Applies when:

- evidence expired;
- source is historical-only for current action;
- registry hash drifted;
- generation changed after preview;
- conflicting current sources exist.

### DEGRADED

Applies when:

- target/service quality degraded;
- pressure exists but no approved action exists;
- target is recovering;
- route quality reduced but checks still pass.

### REPLAY_RISK

Applies when:

- token consumed or expired but referenced by approval;
- selected-move fingerprint mismatch;
- planner/apply generation mismatch;
- approval replay attempt detected;
- nonzero budget lacks immutable generation binding.

### RESTORE_PENDING

Applies when:

- rollback/keep decision is open;
- planner restore open;
- restore-settle open;
- apply restore open;
- delayed monitor not closed.

### MOVEMENT_PENDING

Applies when:

- movement preview exists;
- movement approval is pending or approved but unconsumed;
- forward movement has occurred but rollback/keep not decided.

### CONTAINED

Applies when:

- emergency apply hold/containment is active;
- unexpected movement has been detected;
- hidden mover has been detected;
- containment review is not closed.

## Aggregation Semantics

The overview state includes:

- state;
- headline;
- blocker list;
- affected users count;
- targets touched;
- blast radius summary;
- safe next action;
- evidence freshness;
- linked detail objects.

## Blast Radius Summary

For pending or active operations:

- max users that can move;
- exact users if count is 10 or less;
- from/to targets;
- reserved targets touched;
- route classes touched;
- rollback scope;
- delayed monitoring scope.

## Escalation Semantics

- `SAFE` can become `CONDITIONAL` when an approval is required.
- `CONDITIONAL` becomes `STALE` when evidence expires.
- `STALE` becomes `BLOCKED` when action is attempted.
- `REPLAY_RISK` always blocks mutating action.
- `CONTAINED` remains until explicit closeout.

## Operator State Verdict

The overview state model gives the future UI a single conservative truth while
preserving drill-down into exact gates and evidence.

