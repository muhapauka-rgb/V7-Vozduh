# V7 ordinary recovery: exact Core-primary delta, rollback and concurrency

Mission: `V7_ORDINARY_RECOVERY_EXACT_CORE_PRIMARY_DELTA_ROLLBACK_AND_BOUNDED_CONCURRENCY`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Date: 2026-09-03  
Runtime effect: none.  User movement: 0.  Route, Matrix, Planner, Authority,
Packet, Lease, Barrier, timer and production configuration changes: none.

## Current facts

`v7-user-switch` remains the sole route writer.  Its outer Linux `flock`
holds the mutation, canonical registry write, normal full Core-primary rebuild
and local post-Apply observation in one critical section.  Required-service
verification and S11 are already after the writer returns.

Normal ordinary one-user recovery still uses the full Core-primary path and a
whole-registry preimage.  The existing exact primitive is real but deliberately
narrow:

| Existing path | Scope | Current safety meaning |
| --- | --- | --- |
| operator profile rebind | one user | explicit operator-only Data-plane delta |
| emergency failover cohort | 2--4 users, one target | existing bounded ordinary-cohort contract |
| normal ordinary one-user recovery | one user | full Core-primary rebuild and global rollback coupling |

The exact cohort path stages per-member canonical changes, performs one
Core-primary member delta, keeps whole-system Core-primary verification, and
can roll back its own staged members.  It has not proved interleaving with a
later independent commit.  Therefore it is not silently extended to ordinary
one-user recovery.

## Exact rollback and operation-control result

The required A/B invariant remains unproven:

```text
A commit -> B commit -> A required-service failure -> rollback A
```

Current code cannot credit the expected result because the operation-control
owner persists one closed operation window in one canonical file.  All current
Authority and execution validation require `max_concurrent_transactions = 1`.
Two distinct Packet/Lease/Barrier operations cannot coexist without a minimal,
separately-proven evolution of that existing owner.  No such evolution was
implemented by this Mission.

The Program and OMP now record
`RECOVERY_EXACT_AFFECTED_SET_MUTATION_AND_ROLLBACK_LAW` as
`CANDIDATE_EVALUATION_ONLY`.  It leaves serial Apply, current Authority and
the active CPS frontier unchanged.

## Fidelity and scale boundary

The existing 10/50/100 Polygon evidence remains preparation-only; it does not
run the route writer, actual `flock`, Core-primary/nft mutation, or rollback.

An isolated Docker Linux attempt was made after the local Docker engine became
reachable.  The disposable containers remained in `Created` state and never
started; they were deleted immediately.  Production read-only SSH was also
attempted and denied by public-key authentication.  Consequently no
Linux-equivalent route-writer interleaving evidence exists for this checkout.

The correct result is:

```text
EXACT_ROLLBACK_ISOLATION = NOT_CERTIFIED
OPERATION_CONTROL_SINGLE_WINDOW_BOUNDARY = PROVEN_BY_CURRENT_IMPLEMENTATION
PRODUCTION_CONCURRENCY_NOT_CERTIFIED
```

The serial production path remains the only admitted path.  No queue,
scheduler, new lock manager, route writer, registry, rollback store or manual
recovery seam was introduced.

## Regression and truth

| Check | Result |
| --- | --- |
| `tests.unit.test_v7_user_switch` + `test_v7_routing_sync_core` + OMP document index | 38 PASS |
| Full `tests.unit.test_service_failure_automation_evolution` | 145 PASS |
| `v7-truth-check --all --json` CPS/OMP consistency | PASS |
| Runtime/GitHub deployment convergence | NO-GO: remote unreadable and live hashes unavailable from this environment |

One stale regression expectation was corrected: it now verifies that a
historical receipt preserves whichever CPS frontier is active, rather than a
retired hard-coded frontier name.  This changes no Runtime behaviour.

## Exact next frontier

Retain `max_concurrent_transactions = 1` and serial route mutation.  Re-enter
only when an existing Linux-equivalent substrate can execute the actual route
writer/Core-primary/nft path, or when production read-only access is restored.
Then prove A/B rollback isolation first.  Only after that proof may the
existing operation-control owner be evaluated for a bounded two-operation
representation; it must not be implemented or activated beforehand.
