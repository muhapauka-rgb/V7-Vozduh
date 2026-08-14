# RS6 Desired-State Residual and Non-Runtime Admission Correction

**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**CPS stage / exact successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `RS6_PHYSICAL_MINIMIZATION_NOT_READY; SAFETY_RESIDUAL_CONFIRMED`  
**Runtime / Production / Authority effects:** `NONE / NONE / NONE`

## Decision-relevant recheck

Fresh read-only truth on `2026-08-14` is `FULLY_ALIGNED`: workspace and
GitHub are at `a1b529a0`; Runtime's deployable code is at `d8a4eb29`, with
the sole difference a documentation-only report. Safe-deploy preflight found
the eleven previously recovered RS6 source/unit artifacts byte-identical to
their live counterparts. There is therefore no pending artifact deployment
and no basis to count provenance recovery as physical package reduction.

The remaining recovery residual is live, not historical:

```text
v7-path-guard-repair.timer
  -> v7-path-guard-repair
  -> v7-routing-sync = OK
  -> v7-path-sanity-check = FAIL (v7_path_risk)
  -> user_policy_routes = desired_state_unknown
```

The path-sanity state was fresh at observation. The saved desired-state
projection was stale, and its current direct read-only producer exited with
status `1`; the health service remained running because its loop continues
after that child failure. The Matrix state separately remains an old failed
direct-egress observation. Neither fact is a proof of end-user-path failure,
but together they block removal, disablement or package exclusion of the
recovery path.

## Root cause and owner-boundary result

The current, hash-equal `v7-user-desired-state` source has two coupled
correctness defects in the observed warning/failure branch:

1. `warn()` can return the false status of its conditional assignment after
   the aggregate result is already `WARN`; under `set -e` this aborts the
   checker before its terminal `V7_USER_DESIRED_STATE=...` line.
2. A later route-get mismatch assigns `WARN` over an already detected `FAIL`,
   so severity is not monotonic.

This is a Control/Recovery safety observation, not a permissible generic RS7
simplification item. Existing health/state and recovery/path-safety owners
retain the component. Re-entry requires one owner-backed correctness Mission
with: a fail-closed severity test matrix, preserved route/health semantics,
consumer and rollback proof, a fresh Matrix observation, and only then the
existing deploy/Runtime validation. No change to the helper, service, timer,
routing, state, Production or Authority was made here.

## Admission-contract correction

The existing RS7 lifecycle binding had an implementation-only restriction to
`MANAGEMENT_PLANE`, although its Program contract allows bounded non-Runtime
Engineering simplification. It now accepts exactly `MANAGEMENT_PLANE` or
`ENGINEERING_PLANE` when the existing packet proves Runtime, Production and
Authority impact are all `NONE`. `CONTROL_PLANE`, `DATA_PLANE`, recovery and
Authority-boundary work still fails closed through their current owners.

This permits a future fully evidenced `v7_sync_lib.py` Engineering-interface
candidate to use the existing lifecycle; it does not create a Mission, alter
CPS, authorize the desired-state repair, or broaden the current RS6 frontier.

## Validation and delta

```text
Focused lifecycle tests: 40 PASS
Local CPS/OMP consistency: PASS
GitHub / workspace / Runtime truth: FULLY_ALIGNED
CPS frontier changed: 0
```

| Surface | Before | After | Delta |
| --- | --- | --- | --- |
| Product/runtime source | unchanged | unchanged | `0` lines/files/services/timers changed for the recovery residual |
| RS7 admission validator | Management-only | Management + Engineering non-Runtime scopes | one scope guard generalized; Control/Data/Recovery remain blocked |
| Tests | existing Admin lifecycle cases | plus Engineering acceptance and Control rejection | `+2` cases |
| Runtime deployment | all recovered RS6 artifacts hash-equal | hash-equal | `0` deployment delta |

**Next frontier:** retain `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; do not
advance CPS. The smallest material re-entry is an existing-owner safety
admission for the desired-state helper and stale Matrix evidence, not physical
cleanup and not a generic RS7 Mission.
