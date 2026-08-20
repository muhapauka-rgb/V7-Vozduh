Mission: `V5_3_SYSTEM_REVALIDATION_CONTRACT_CORRECTION_V1`

# V5.3 terminal precedence and observed-timing correction

Status: `COMPLETE; NO_RUNTIME_EFFECT`

## Change

Two narrow corrections were made in the existing Service Failure Automation
Evolution Program and existing OMP:

1. The old internal Phase-E decision is now explicitly an input only. It
   cannot enable an automatic FAST consumer. Only the newer system-level
   weighted decision may make that consumer eligible.
2. Decision-critical cadence, timeout, retry, persistence and serial-wait
   values must use observation or controlled measurement where it is safely
   executable. A source-code default alone cannot establish hot-path speed.

## Reused owners and proof

The existing CPS atomic reconciler and V5.3 lifecycle binding admitted the
already-authorized read-only system Atlas. No new Program, owner, Runtime,
Planner, state source or Authority was created. Atomic reread reported `PASS`;
the binding returned `MISSION_EXECUTION_ALLOWED` with no Runtime effect.

## Safety

No probe was started, no route changed and no client moved. The full Matrix
remains the fallback. Exact successor is owned by the admitted Atlas report:
`IMPLEMENT_V7_MATRIX_FAST_SUBSET_OBSERVATION_AND_FULL_COMPARATOR_V1`.
