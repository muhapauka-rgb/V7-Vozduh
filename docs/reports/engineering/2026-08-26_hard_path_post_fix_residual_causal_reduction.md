# HARD path post-fix residual causal reduction

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
**Mission:** `V7_HARD_PATH_POST_FIX_RESIDUAL_CAUSAL_REDUCTION`  
**State:** instrumentation implemented locally and verified; publication and
controlled evidence are the next gated step

## Owner decision and scope

The prior `HARD_PATH_3S_2VCPU_ARCHITECTURE_EXHAUSTED` terminal remains
historical evidence.  The owner authorizes exactly this bounded causal
reduction mission.  It may instrument the existing path, repair only a
measured and falsified safe recurring cause, publish/deploy that repair, and
run certification-only Polygon evidence.

It does not authorize an SLO change, VDS resize, a new owner, Runtime,
Planner, timer, weakened S11 semantics, or ordinary-user movement.  No other
closed work is reopened.  The only valid outcomes are
`HARD_PATH_RUNTIME_SLO_CONVERGENCE_CONSUMED` and
`HARD_PATH_POST_FIX_RESIDUAL_EXHAUSTED`.

## Frozen starting evidence

The previous homogeneous, S11-preserving certification-only series on
fingerprint `ba7161f5f0eeb959fb193b7ec94370185f686e6ba0fe7d80b695c6727a926cd3`
was: `2696.992`, `4114.938`, `4449.524`, `4893.144`, `5014.885` ms.  Its
nearest-rank P95 is `5014.885 ms`; every sample remains in the new comparison
as historical baseline only.

## Fresh baseline capture

| Item | Observation |
|---|---|
| Local / published commit | `d26d62f109fd1cc1d48e4ec9624665b77d5a878e` on `Updatesystem` |
| Deployed performance code | `e4106fd647978adf481d78201ed10a183a130fcb`; health-loop SHA-256 `71968c7094a410f6c6c8ffe65def0424c6b156ddda6a83c18b4b3d4f0722c746` |
| Health service | active; invocation `ce3856ca2c28464f8e9146ebe3b18f8d` |
| Legacy standalone timers | Matrix inactive; Telegram inactive, as intended |
| Runtime owners at snapshot | one health-loop daemon; one Matrix projection-refresh child; no route-writer child |
| Canonical state fingerprints | `egress.registry` `e42bd1a3…`; `users.registry` `0c7c422c…` |
| Prepared projection | fresh; produced `2026-08-26T06:35:04.854131+00:00`; no world-model rebuild or registry scan |
| Synthetic evidence scope | certification-only identity `10.7.0.124`; five prior reservations each have a terminal cleanup record |
| Ordinary-user scope | no ordinary movement is admitted or observed in the baseline |

## Initial observation, not a root cause

The health journal records `hot_target` deadline misses caused by a previous
`hot_target` invocation still running, and `other_required` is deferred while
`planner_projection` runs.  This is a candidate for causal analysis only.
It is not yet evidence that a lower-priority role delays the HARD path, so no
scheduler change is admitted from this observation alone.

## Implemented diagnostic surface

The implementation retains the existing health-loop, Matrix consumer, Planner
and governed route writer.  It adds no state store, timer, route writer or
decision path.  It records evidence only:

- the split from canonical T0 to health-owner dispatch and from that dispatch
  to Matrix entry, together with process CPU, scheduler wait, context-switch
  and load observations;
- the existing route writer's lock wait, control validation, kernel mutation,
  assignment-state write, registry commit, audit and post-apply observation
  spans;
- the resulting spans are attached to the pre-existing controlled performance
  evidence only when the exact HARD path runs.

The legacy combined timing fields remain intact, so no consumer is migrated
or reinterpreted by this diagnostic change.

## Verification before publication

| Check | Result |
|---|---|
| Shell syntax for the governed route writer | PASS |
| Python compilation of all changed Runtime owners | PASS |
| Route-writer policy suite | PASS, 200 tests |
| V5.3 lifecycle binding suite | PASS, 8 tests |
| Expanded V5.3 regression | PASS; sandbox socket restriction was avoided by the existing isolated test environment |
| CPS/OMP live-pointer reconciliation | PASS; only expected local-unpublished/remote-readability blockers remain |

The lifecycle fixture was corrected to model a single synthetic atomic CPS
state across the live section, registry and protected WIP.  It does not alter
production state or relax any validator.

## Next measurement

Publish the diagnostic-only change through the safe deploy gate, prove local,
GitHub and Runtime alignment, then obtain one controlled valid sample.  Its
full timeline decides whether any recurring, safe cause over 100 ms exists;
there is no performance patch before that causal comparison.
