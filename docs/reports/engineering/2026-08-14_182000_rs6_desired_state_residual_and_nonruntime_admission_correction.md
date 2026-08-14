# RS6 Desired-State Residual and Non-Runtime Admission Correction

**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**CPS stage / exact successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `RS6_PHYSICAL_MINIMIZATION_NOT_READY; SAFETY_RESIDUAL_CONFIRMED`  
**Runtime / Production / Authority effects:** existing fail-closed
desired-state projection corrected / `NONE` / `NONE`
**Deployment effect:** the existing helper and its existing saver were
synchronized through the approved manifest; no service, timer, route, policy
or user operation was invoked.

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
The existing safe-deploy owner synchronized only this approved library after
the commit; post-deploy Runtime truth is aligned to `054bd117`.

## Validation and delta

```text
Focused lifecycle tests: 40 PASS
Local CPS/OMP consistency: PASS
GitHub / workspace / Runtime truth: FULLY_ALIGNED
CPS frontier changed: 0
Safe-deploy delta: one Engineering library; service/timer restart: 0
```

| Surface | Before | After | Delta |
| --- | --- | --- | --- |
| Product/runtime source | unchanged | unchanged | `0` lines/files/services/timers changed for the recovery residual |
| RS7 admission validator | Management-only | Management + Engineering non-Runtime scopes | one scope guard generalized; Control/Data/Recovery remain blocked |
| Tests | existing Admin lifecycle cases | plus Engineering acceptance and Control rejection | `+2` cases |
| Runtime deployment | previous admission library | existing admission library at `054bd117` | one approved Engineering library copied; no process/service/timer change |

**Next frontier:** retain `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; do not
advance CPS. The smallest material re-entry is an existing-owner safety
admission for the desired-state helper and stale Matrix evidence, not physical
cleanup and not a generic RS7 Mission.

## Execution addendum — fail-closed projection persistence

The owner-backed correction described above was subsequently executed as two
small, reversible commits: `49b55345` and `84550530`. It fixes only the
existing `v7-user-desired-state` and `v7-user-desired-state-save` chain:

```text
v7-user-desired-state
  -> terminal V7_USER_DESIRED_STATE=OK|WARN|FAIL
  -> existing v7-user-desired-state-save
  -> existing user-desired-state.state
  -> existing health/path-sanity readers
```

The checker no longer exits before its terminal line when more than one
warning occurs, and a later route-get warning cannot lower a prior `FAIL`.
The saver now persists a syntactically complete terminal projection even when
the checker returns `1` for a real `FAIL`, then preserves that non-zero exit
for the existing health lifecycle. No new writer, state surface, consumer,
service, timer, owner, routing operation or Authority path was added.

### Evidence and validation

| Check | Result |
| --- | --- |
| Focused fail-severity/persistence tests | `3 PASS` (`WARN`, monotonic `FAIL`, persisted `FAIL`) |
| Target CPS/OMP and deploy tests | `69 PASS` |
| Shell syntax and diff whitespace | `PASS` |
| Safe deploy | `deploy-z8-14-Updatesystem-8455053-20260814T121932`; no service/timer restart |
| Runtime/GitHub/CPS truth after deployment | `FULLY_ALIGNED` / `PASS` / CPS frontier unchanged |
| Direct read-only checker | terminal `V7_USER_DESIRED_STATE=FAIL` (real failure is now observable) |
| Existing saver invocation | `SAVE_EXIT=1`, fresh state with `errors=124`, `V7_USER_DESIRED_STATE=FAIL` |

The pre-existing saved projection had remained at `2026-08-13 13:47:07` with
`V7_USER_DESIRED_STATE=OK`. The corrected existing saver wrote a fresh
projection at `2026-08-14 12:21:25` with `FAIL`. This is a truthful state
refresh by the existing owner, not a routing, policy, user-movement or
Authority effect. The health service was active and its deployed `ExecStart`
and saver hash matched source; its observed loop cadence remains a separate
runtime-lifecycle residual and was not changed by this bounded correction.

### Before / after / delta

| Surface | Before | After | Delta |
| --- | --- | --- | --- |
| Checker terminal on warning/failure branch | could abort or downgrade `FAIL` | terminal always emitted; severity monotonic | fail-closed result restored |
| Saved desired-state projection after real `FAIL` | stale historical `OK` | fresh terminal `FAIL` persisted | existing writer completes its state contract |
| Runtime files/services/timers | existing | existing | `0` created/removed/restarted |
| Source/test change across both commits | baseline | 5 files touched | `+157 / -3` lines; one test file added |
| Routing / policy / user movement / Authority | unchanged | unchanged | `NONE` |

**Residual and exact re-entry:** `errors=124` is the actual desired-state
failure and still blocks any package removal. The stale/failed Matrix evidence
and the observed health-loop cadence require the existing health/recovery and
Matrix owners to provide fresh lifecycle evidence before a physical RS6
minimization decision. CPS remains at
`EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`; no RS6 completion or frontier
advance is claimed.

## Execution addendum — canonical Matrix path-safety reader

The Matrix timer and writer were not stale: the observed timer invocation ran
successfully and the canonical `service-matrix.json` was fresh. The stale
artifact was the legacy `service-matrix-refresh.state` reader in the existing
`v7-path-sanity-check`; it still contained a May `FAIL` while the canonical
Matrix reported current per-egress `OK`, `WARN` and `FAIL` facts. Other current
Control/Management consumers already use the canonical JSON.

Commit `12aa5271` makes the existing observer read that canonical JSON first,
aggregate its item statuses conservatively (`FAIL` > `WARN` > `OK`), and emit
`UNKNOWN` rather than fall back to a stale legacy `OK` when a present canonical
file is empty or malformed. The old state file remains a compatibility
fallback only when the canonical file is absent. This changes no Matrix writer,
timer, consumer, routing decision, recovery action, policy, user or Authority
boundary.

```text
Matrix timer -> v7-service-matrix-refresh-all -> service-matrix.json
  -> v7-path-sanity-check -> v7-path-sanity.state -> existing path guard reader
```

| Check | Result |
| --- | --- |
| New canonical precedence/fallback tests | `3 PASS` |
| Combined desired-state, path-sanity, CPS/OMP and deploy tests | `75 PASS` |
| Safe deploy | `deploy-z8-14-Updatesystem-12aa527-20260814T124841`; no restart |
| Direct existing path-sanity observation | canonical Matrix note present; `egress_service_matrix=FAIL` and `V7_PATH_SANITY=FAIL` |

The final `FAIL` is intentional and truthful: the fresh canonical Matrix has
at least one current failed egress and desired-state has real errors. The
change removes a stale input, not the safety residual. Physical delta is one
existing observer modified plus one test file: `+119 / -2` lines; files,
services, timers, state surfaces, routes, users and Authority boundaries
created/removed/changed: `0` except the observer's own refreshed diagnostic
projection. The remaining exact RS6 blocker is actual health/admission and
Matrix recovery evidence, not the former stale Matrix read path.
