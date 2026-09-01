# Simplification-first engineering law and recovery specialization

**Date:** 2026-09-01
**Mission:** `V7_SIMPLIFICATION_FIRST_ENGINEERING_LAW_AND_RECOVERY_SPECIALIZATION`
**Type:** Contract/program edit only
**Result:** `SIMPLIFICATION_FIRST_CONTRACT_REGISTERED; NO_RUNTIME_EFFECT`

## Why

V7 has accumulated recovery repairs around historical state, compatibility
paths, locks and asynchronous evidence. A locally working fix is insufficient
when it leaves a duplicate decision path or a stale current-looking blocker
that later prevents the normal Runtime from recovering a user.

## Reused placement

The change extends existing OMP responsibility-realignment, safe-removal,
migration, complexity and recovery-stability contracts. It creates no new
Program, Runtime, Matrix, Planner, queue, registry, watcher, state surface,
evidence database or execution authority.

## Binding law

Every material change now follows:

```text
discover owner/caller/consumer
-> reuse
-> simplify/remove/collapse/narrow/defer
-> add only essential missing logic
```

Normal fixes are expected to preserve or lower the affected structural
complexity. An increase is allowed only for a current safety/product gap that
existing owners cannot express, with an explicit owner, consumer, regression
proof and retirement/migration condition.

## Safety guardrails

- Safe deletion still requires current caller/consumer migration, replacement
  proof and regression evidence.
- A required fallback or rollback remains until its trigger and exit condition
  are complete; a current owner must verify that exit condition.
- Temporary migration complexity must have a bounded cutover and old-path
  removal condition.
- Second related exception requires review; a third requires an existing-owner
  state-model review before another branch.
- Document-only work records complexity as `NOT_APPLICABLE` with reason.

## Recovery specialization

`RECOVERY_SIMPLIFICATION_FIRST_LAW` requires an existing-owner test for stale
historical gates, duplicated incident interpretation, stale handoffs/pins,
overlong transaction lifetimes, lock scope, pre-S11 passive work and repeated
STOP_SAFE exceptions before adding a recovery branch.

`RECOVERY_HOT_PATH_COMPLEXITY` remains a compact report/test projection. It is
not a new durable Runtime state surface. It records only dimensions affected by
one repair and preserves the existing normal law: `DELTA <= 0`.

## Interrupted Stability protection

The already admitted `RECOVERY_STABILITY_FOUNDATION` is not reset or treated as
completed. Its next implementation step begins with Program/CPS/OMP/Git/deploy
/Runtime reconciliation. Missing GitHub or Runtime visibility is classified as
`OBSERVATION_UNAVAILABLE`; it never silently resets current CPS truth.

## Files changed

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`

## Runtime and production effect

None. No Matrix execution, Authority decision, Planner call, Candidate,
Packet, Lease, Barrier, route mutation, user movement, timer or service change
occurred in this Mission.

## Next action

Run the already admitted `RECOVERY_STABILITY_FOUNDATION` resume reconciliation,
then repair only a proven generic lifecycle defect through the existing normal
V7 Runtime caller. No manual client recovery is valid evidence.
