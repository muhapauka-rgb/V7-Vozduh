# Recovery stability hardening program section

**Date:** 2026-09-01  
**Mission:** `V7_RECOVERY_STABILITY_HARDENING_PROGRAM_SECTION`  
**Type:** Program-contract edit only  
**Result:** `PROGRAM_CONTRACT_REGISTERED; IMPLEMENTATION_NOT_ADMITTED`

## Why added

Recent ordinary recovery observations established a product gap: V7 can
recover a user automatically, yet a later current recovery can be delayed or
blocked by residue from an earlier incident, cooldown, target decision,
operation or terminal projection.  A single successful recovery therefore is
not evidence that the recovery lifecycle stays correct as time and scope
change.

No Runtime mechanism, client assignment, route, Matrix generation, timer,
Authority, Candidate, Packet, Lease or Barrier was changed by this Mission.

## Contract added

The Program now requires `RECOVERY_STABILITY_CONSUMED` before the final
seven-second product SLO can close.

The binding law is:

```text
CURRENT FAILED OR PROFILE-UNSUITABLE SOURCE
+ CURRENT AFFECTED ENABLED USERS
+ CURRENT LAWFUL TARGET
+ NO ACTIVE EXACT CONFLICT
= CURRENT RECOVERY OBLIGATION OR ACTIVE GOVERNED RECOVERY
```

If this law is false, the existing Runtime diagnostics must expose
`RECOVERY_OBLIGATION_MISSING`.

## Current truth versus history

Fresh Matrix, current assignments/profile requirements, target health and
capacity, Authority, active exact operation ownership and current route state
override historical incident/closure rows, old `NO_SAFE_TARGET`, prior
cooldown, prior target choice and Learning.

History remains useful for audit, learning, exact-once protection and proof of
an active exact safety conflict.  It cannot make a failed channel healthy,
remove current users from scope or suppress a new lawful recovery.

An active safety block must match the current source/action generation and the
same identity or exactly overlapping scope, and must have a current non-expired
operation, Lease, Barrier or rollback dependency.  A completed or unrelated
operation is not such a block.

## Re-entry and exact-once

Exact-once applies to the same completed route mutation, not indefinitely to a
continuing incident.  New scope, newly eligible target, disappeared blocker or
fresh relevant Matrix generation requires new reconciliation.

Every `STOP_SAFE` must identify its current blocker, owner, scope, re-entry
condition and next existing reconciliation owner.  Re-entry is level-triggered
only by an existing relevant event; it is not a busy polling loop.

## Acceptance plan

The later implementation phase must complete:

1. current-truth precedence audit;
2. level-triggered reconciliation and STOP_SAFE re-entry;
3. stranded-recovery diagnostic through existing owners;
4. historical live-gate classification and cleanup;
5. deterministic 50-transition soak, then 100-transition soak;
6. five consecutive, preferably ten, approved live operator bad-placement
   cycles without an intervening repair;
7. real Matrix-to-S11 evidence for all applicable cases.

Required sequences include changed scope under a continuing incident, stale
`NO_SAFE_TARGET` becoming obsolete, cooldown on fresh confirmed failure,
restart reconstruction, two independent failures, multi-target recovery,
exact conflict completion, stale Lease/Barrier cleanup and target-pin
isolation.

## Safety and authority

The phase reuses Matrix, health loop, `users.registry`, Planner, Authority,
Candidate/Packet/Lease/Barrier, execution control, route writer and
Core-primary.  It creates no new operational owner or truth source.

Codex may repair generic implementation defects, test, deploy and observe. It
must not perform a user-specific recovery, choose a source/target, construct
an incident or governed transaction, call the route writer, or advance a
live recovery on V7's behalf.  Bounded live cycles use only explicitly approved
controlled/test profiles; a lawful target requires zero stranded users.

## Relationship to the 7-second SLO

The clocks remain unchanged:

```text
T_FIRST_VALID_FAILURE_OBSERVATION
-> T_GLOBAL_ALL_AFFECTED_RECOVERED
P95 <= 7000 ms; maximum <= 8000 ms
```

Stability and latency are independent:

- recovery in 20 seconds may be stability PASS but latency FAIL;
- a user left stranded with a healthy target is stability FAIL regardless of
  elapsed time.

Final Program closure now requires both `RECOVERY_STABILITY_CONSUMED` and
`GLOBAL_ALL_AFFECTED_RECOVERY_SLO_CONSUMED`, followed by the existing N11
residue closure.

## Files changed

- `docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`

## Verification

- `git diff --check`: PASS.
- `tests.unit.test_v7_sync_tools` plus
  `tests.unit.test_omp_program_execution_reconciliation`: PASS, 68 tests.
- `tools/v7-truth-check --all --json`: PASS; CPS/OMP current pointer,
  completion contract, ownership and Runtime convergence remain aligned.
- The broader 77-test run that also includes the historical V5.3 lifecycle
  binding fixtures retains two unrelated failures in
  `test_atomic_admission_allows_read_only_execution` and
  `test_phase_g_no_parallelism_is_consumed_into_existing_t0_t11_track`.  They
  report existing CPS historical-phase expectation divergence, not a failure
  of the new document contract; this Mission neither changed their Runtime
  behavior nor waived them.

## Exact next frontier

No implementation is admitted by this document Mission.  When the existing
CPS/OMP reconciliation owner admits the next work, it must begin with the
current-truth precedence audit and map all current recovery gates to their
existing owners before modifying any Runtime behavior.
