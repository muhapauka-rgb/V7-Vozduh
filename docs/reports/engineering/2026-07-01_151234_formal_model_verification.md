# Formal Model Verification

Status: `COMPLETE`
Mode: `READ_ONLY_FORMAL_MODEL_VERIFICATION`
Code modified: `NO`
Runtime modified: `NO`
Planner modified: `NO`
OMP modified: `NO`

## Question

Does the current V7 execution model define one unique legal execution path, or can two correct implementations produce different legal decisions from the same world state?

## Formal State Machine

The L3 execution model is a deterministic fail-closed state machine.

```text
IDLE
  -> WAKE
  -> OBSERVE
  -> CLASSIFY
  -> WORLD_READY
  -> PLAN_READY
  -> WAITING_AUTHORITY
  -> READY
  -> EXECUTING
  -> VERIFYING
  -> ROLLBACK | LEARNING
  -> REPORTING
  -> SLEEP | SUSPENDED
```

Legal stop transitions:

```text
Any missing, stale, contradictory, unauthorized, unsafe, or materially changed mandatory fact
  -> STOP_SAFE
```

Legal execution transition:

```text
READY
  -> EXECUTING
```

`READY` exists only when all mandatory L3 entry, authority, identity, and readiness gates pass.

## Formal World Facts

Observable world facts only:

| Symbol | Meaning |
| --- | --- |
| `U` | exact user subject exists and is assigned to current channel `C` |
| `C_FAILED` | current assigned channel `C` is failed for this user/service context |
| `RS_FAILED` | required services for `U` fail on `C` |
| `T_SAFE` | at least one target `T` passes service, route, load, quality, policy, and suitability gates |
| `FRESH` | required evidence is inside L3 freshness bounds |
| `AUTH_L3` | current authority permits `EMERGENCY_FAILOVER_AUTONOMY` / `FAILOVER` / `CURRENT_CHANNEL_FAILED` for the scope |
| `ONE_USER` | selected scope is exactly one user for the first validation rung |
| `IDENTITY_OK` | selected move hash, user, source, target, operation, packet/transaction identity match |
| `RESTORE_OK` | restore barrier / clearance generation matches selected decision |
| `ROLLBACK_OK` | rollback or certified no-rollback is ready before apply |
| `VERIFY_OK` | route/target/required-service verification is ready |
| `BLAST_OK` | blast radius and execution budget are inside certified scope |
| `MP_OK` | movement protection / anti-flap / cooldown / circuit breaker allow this emergency action |

## Formal Truth Graph

```text
U + C_FAILED + RS_FAILED + FRESH
  -> AFFECTED_USER_ON_FAILED_CURRENT_CHANNEL

AFFECTED_USER_ON_FAILED_CURRENT_CHANNEL + T_SAFE
  -> L3_ACTION_CANDIDATE

L3_ACTION_CANDIDATE
  -> PLAN_READY

PLAN_READY + AUTH_L3 + ONE_USER + IDENTITY_OK + RESTORE_OK
  + ROLLBACK_OK + VERIFY_OK + BLAST_OK + MP_OK
  -> EXECUTION_READY

EXECUTION_READY
  -> EXECUTE_ONE_USER

not(EXECUTION_READY)
  -> STOP_SAFE
```

## Formal Execution Graph

```text
World facts
  -> Observation truth
  -> L3 entry truth
  -> Decision candidate
  -> Authority truth
  -> Runtime readiness truth
  -> EXECUTION_READY or STOP_SAFE
  -> Execute or no mutation
  -> Verify
  -> Rollback / Success
  -> Terminal outcome
  -> Learning
```

## Legal Action Derivation

For one-user L3 failover:

```text
LEGAL_EXECUTE_L3(U, C, T) :=
  U
  AND C_FAILED
  AND RS_FAILED
  AND T_SAFE
  AND FRESH
  AND AUTH_L3
  AND ONE_USER
  AND IDENTITY_OK
  AND RESTORE_OK
  AND ROLLBACK_OK
  AND VERIFY_OK
  AND BLAST_OK
  AND MP_OK
```

Then:

```text
if LEGAL_EXECUTE_L3 == true:
  unique legal runtime action = EXECUTE_ONE_USER
else:
  unique legal runtime action = STOP_SAFE / no mutation
```

Therefore, at the Runtime execution boundary, two correct implementations cannot disagree on `EXECUTE` vs `STOP_SAFE` for identical truth values.

## Determinism Proof

The model is deterministic for the execution boundary because:

1. L3 Entry Conditions require all mandatory facts; any false or unknown entry condition is `STOP_SAFE`.
2. Autonomous Runtime Readiness defines `EXECUTION_READY` as the only state that may execute.
3. Runtime Model states Runtime spends prepared knowledge and stops when an owner cannot prove eligibility, authority, safety, verification, or rollback readiness.
4. L3 Readiness Contract says any failed mandatory gate produces `STOP_SAFE`.
5. L3 Execution Contract forbids silent replacement of selected move, user, source, target, authority, rollback, verification, or packet/transaction identity.

Thus:

```text
same world facts + same authority/readiness facts
  -> same EXECUTION_READY truth value
  -> same legal execute-or-stop action
```

## Multiple Legal Paths

### Case: Planner -> FAILOVER and Runtime -> STOP_SAFE

This can be correct only if these are different model states:

```text
PLAN_READY
  -> Runtime checks authority/readiness
  -> STOP_SAFE
```

It is not correct if `FAILOVER` is treated as already proving `EXECUTION_READY`.

Formal rule:

```text
FAILOVER is a decision vocabulary item.
FAILOVER != EXECUTION_READY.
```

The model forbids:

```text
Planner FAILOVER
  -> Execute
```

unless all L3 entry/readiness/authority/identity/restore/rollback/verification facts compose to `EXECUTION_READY`.

## Ambiguity Audit

| Concept | Canonical meaning | Implementation meaning checked | Classification |
| --- | --- | --- | --- |
| `FAILOVER` | Decision vocabulary: move affected users away from failing channel | `move_type == failover` | Single meaning if used as proposal; ambiguous if treated as execution permission |
| `CURRENT_CHANNEL_FAILED` | Current assigned channel failed for affected user/service context | L3 allowed reason / incident family | Single canonical meaning |
| `CURRENT_EGRESS_NOT_ELIGIBLE` | Planner reason that current channel is not eligible | Used as reason for failover candidate | Broader than L3 current-channel-failed truth |
| `REQUIRED_SERVICE_FAILURE` | Required services fail on current channel for affected user | `_emergency_failover_move_evidence()` requires `current_failures` | Single canonical meaning |
| `WAKE` | Starts observation | `_l3_wake_decision()` accepts inferred or external wake | Single meaning; not execution authority |
| `INCIDENT` | Operator-visible lifecycle context | L3 incident context | Single meaning; not execution authority |
| `EXECUTION_READY` | Composite authority + live gates + identity + restore readiness truth | emergency gate `ok` plus apply gates | Single meaning |

## Model Completeness

| Property | Result |
| --- | --- |
| Complete | `YES` for one-user L3 execute/stop boundary |
| Deterministic | `YES` for `EXECUTE` vs `STOP_SAFE` |
| Ambiguous | `NO` at execution boundary |
| Underspecified | `NO` for legal execution; target ranking is delegated to the single Planner owner |
| Overspecified | `NO` |
| Self-contradictory | `NO` |

Target choice is not a second Runtime path. The model delegates candidate ranking to the single Planner/Autoswitch owner. Once selected, Runtime must preserve that target identity or stop.

## Implementation Conformance

| Component | Conformance | Evidence |
| --- | --- | --- |
| Authority | `CONFORMS` | `tools/v7-users-autoswitch::_emergency_failover_authority_gate()` requires L3 authority, one-user production validation envelope, restore barrier, rollback, verification, budget, and wake evidence. |
| Runtime readiness | `CONFORMS` | Emergency gate returns `bounded` only when all blockers are empty; otherwise selected moves are cleared and execution cannot reach apply. |
| Execution identity | `CONFORMS` | `admin_core/operator_execution.py::selected_moves_from_plan()` and `approved_plan_lock_from_selected()` preserve identity and semantic fields; restore barrier carries the approved lock. |
| Execution apply | `CONFORMS` | `tools/v7-users-autoswitch.apply()` refuses apply when selected moves are absent or approved lock blocks. |
| Verification | `CONFORMS` | L3 model requires verification; current L3 gate blocks if verification is not enabled. |
| Planner | `PARTIALLY_CONFORMS / FIRST DIVERGENCE` | `_decision_for_user()` can produce `move_type = failover` with reason `current_egress_not_eligible`; L3 model requires failed current channel plus required-service failure for L3 emergency execution. |

## First Implementation Divergence

The first divergence is Planner classification:

```text
current_egress_not_eligible
  -> move_type = failover
```

This is broader than:

```text
CURRENT_CHANNEL_FAILED
  + REQUIRED_SERVICE_FAILURE
  -> L3 failover candidate
```

Runtime correctly rejects the candidate later if required-service failure is not proven.

## Counterexamples

### Counterexample 1: High confidence should execute

Rejected. Autonomous Runtime states confidence never grants execution. Readiness is required.

### Counterexample 2: Wake accepted should execute

Rejected. Wake may start observation and may not grant execution.

### Counterexample 3: Authority exists should execute

Rejected. Policy 004 says permission does not prove operational safety or runtime eligibility.

### Counterexample 4: Planner failover and Runtime STOP_SAFE are both final legal actions

Rejected. They are both correct only if `FAILOVER` is a proposal and `STOP_SAFE` is the result of failed execution eligibility. They cannot both be final legal runtime actions for the same `EXECUTION_READY` truth.

### Counterexample 5: Multiple safe targets make the model ambiguous

Rejected at Runtime boundary. Candidate ranking is owned by the single Planner owner; once selected, Runtime preserves selected identity or stops. Different target ranking implementations would be Planner conformance issues, not a second legal Runtime execution path.

## Final Proof

Proof A:

```text
The model is deterministic.
Implementation violates it.
```

More precisely:

The Runtime/Authority/Execution implementation conforms to the deterministic model by stopping unless `EXECUTION_READY` is proven. The first implementation divergence is that Planner can label a move as `failover` from the broader fact `current_egress_not_eligible`, while the L3 formal model requires the narrower same-subject emergency facts `CURRENT_CHANNEL_FAILED` and `REQUIRED_SERVICE_FAILURE` before a candidate may be treated as L3-executable.

## Final Verdict

```text
MODEL_DETERMINISTIC_IMPLEMENTATION_WRONG
```
