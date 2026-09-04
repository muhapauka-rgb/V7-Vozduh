# V7_RECOVERY_CONSUMER_WALL_TIME_FULL_ATTRIBUTION_AND_P0_REMOVAL

## Verdict

- `CONSUMER_WALL_FULLY_ATTRIBUTED = PASS`.
- Latest reconstructable automatic action has `UNACCOUNTED_WALL = 20.070 ms` (`0.062%`), below both `100 ms` and `1%` limits.
- The earlier approximately `115 s` unexplained P0 is consumed; no current receipt contains an unexplained multi-second envelope.
- Duplicate pre-governed advisory/passive work is removed and live-proven.
- The additional governed Python process/import envelope (approximately `3.607 s` in the latest applicable pre-change receipt) is removed from the persistent ordinary Runtime path.
- `RECOVERY_LATENCY_SLO = NOT_CONSUMED`: after the final fingerprint there has not yet been an actionable ordinary incident with an affected ordinary user.
- Current Program frontier remains `RECOVERY_LATENCY_SLO`.

## Final fingerprint and Runtime truth

- Local/GitHub/deployed commit: `090e801961b5a426dc53a844a7b28d4c3e9e68e0`.
- Safe-deploy manifest: `deploy-z8-14-Updatesystem-090e801-20260904T083829`.
- `v7-health.service = active`, start `2026-09-04 08:38:47 MSK`, persistent Matrix `READY`.
- Runtime hashes:
  - `v7-health-loop`: `c8777978763b866eec9e029871b46e95a8394ed6dfc61d0ccfb693f12405cdbd`;
  - `v7-service-matrix-refresh-all`: `f6f909bc2c25933d3d428bb28f6b8eb7a5124a95aa4429c8bd0480def4c6dfc0`.
- New owner/daemon/queue/timer/watcher/registry/truth source: `0`.

## Proven automatic provenance

The production origin remains:

`v7-health.service -> persistent Matrix consumer -> existing autoswitch/Planner owner -> existing governed executor -> route writer -> required-service S11`.

Codex did not choose a user, source, target, incident or route; did not invoke the recovery consumer or route writer; and did not manually advance Candidate/Packet/Lease/Barrier/Apply.

## Exclusive consumer wall attribution

Latest fully reconstructable automatic action before the final process-hop repair:

| Exclusive envelope | Duration |
|---|---:|
| Matrix consumer entry -> governed dispatch | 16,290.556 ms |
| governed child envelope | 16,148.358 ms |
| governed result parse | 0.782 ms |
| post-child reconciliation/return | 2.292 ms |
| remaining scheduler/wrapper boundary | 20.070 ms |
| **consumer wall** | **32,462.058 ms** |

`UNACCOUNTED_WALL = 20.070 ms`. Pre-dispatch terminal returns are also closed by the same monotonic envelope. The receipt uses mutually exclusive monotonic boundaries; its parts reconcile to the consumer wall.

## P0 removal sequence

### 1. Duplicate pre-governed chain

Measured before repair:

| Stage | Duration |
|---|---:|
| fresh profile-obligation advisory | 7,025.804 ms |
| passive consumer before handoff | 3,476.629 ms |
| post-passive current-scope lookup | 294.548 ms |
| duplicate service-failure advisory | 5,279.590 ms |
| **duplicate chain** | **16,076.571 ms** |

Cause: one failed source could expose several service incident IDs. A valid Matrix source binding was rejected by singleton cardinality, causing passive processing and a second advisory in the same unchanged generation.

Repair through existing owners:

- bind the exact fresh Matrix-selected source incident;
- revalidate current Matrix scope;
- reuse the first valid advisory result;
- suppress passive capture and duplicate advisory for the unchanged binding.

Fresh live automatic VLESS action after this repair:

- `T0 -> complete = 16.838 s`;
- consumer entry -> S11 `15.948 s`;
- pre-governed `3.526 s`;
- one advisory `3.228 s`;
- passive/second advisory `0`.

Therefore the measured duplicate pre-governed P0 is live-consumed.

### 2. Hidden governed process envelope

The same live receipt measured:

- governed child envelope `12.971 s`;
- named governed stages approximately `9.364 s`;
- hidden process/import/wrapper envelope approximately `3.607 s`.

Cause: the persistent Matrix owner synchronously spawned and initialized another Python process for the already-existing governed executor.

Repair at `090e8019`:

- the persistent health owner prewarms the existing governed module/parser once;
- ordinary Runtime invokes the same existing `execute_governed_transaction` owner in-process;
- current state, Authority, Planner, Candidate, Packet, Lease, Barrier, route writer and S11 checks remain unchanged;
- the historical subprocess remains only as a fail-closed compatibility fallback;
- every result records `governed_runtime_invocation.mode` and fallback reason;
- no durable cache or second Runtime truth was introduced.

Engineering proof:

- focused in-process test proves `EXISTING_OWNER_IN_PROCESS`, `new_runtime_process_created = false`, and zero subprocess calls;
- direct affected test: `PASS` (`1.089 s` test execution); full focused repair set: `41 PASS` plus `2` relevant service-failure regressions;
- cached module/parser load: first `17.084 ms`, repeated access `0.038 ms`, with no Runtime state read;
- health owner restarted with the exact deployed files and reports persistent Matrix `READY`.

This is engineering evidence for removal of the process hop. It is not substituted for a fresh ordinary product SLO receipt.

## Apply/verification attribution now exposed

The latest applicable pre-change receipt had:

- Apply/verification approximately `7.596 s`;
- route-writer wall approximately `3.815 s`;
- required-service verification approximately `1.746 s`.

The health receipt now safely projects the route writer's numeric `writer_stage_timings_ms`. This makes the next valid receipt distinguish route-lock wait, Core-primary work, kernel visibility and verification instead of treating route-writer wall as one opaque span. This change is observability-only.

## Fresh incident reconciliation after final deploy

Fresh Runtime inspection after `090e8019` found a real current VLESS service incident:

- VLESS YouTube/Google/Google Auth/Instagram observations are confirmed failed/continuing;
- Matrix failure episode began at `2026-09-04 08:25:02 MSK`;
- two registry rows reference VLESS, but one is disabled and the only enabled row is `certification_user=1`, group `polygon-l7-canary`;
- enabled ordinary users on VLESS: `0`;
- the three current ordinary test clients are assigned to healthy WireGuard/AWG3 sources and their current required-service placement is satisfied;
- no post-restart `V7_HEALTH_RECOVERY_CONSUMER_RECEIPT` exists.

Result: the incident is real, but there is no affected ordinary scope. Starting or manufacturing an ordinary transaction would violate owner provenance. The event receives no ordinary recovery or SLO credit.

## Structural delta

Before:

`Matrix -> advisory -> passive -> duplicate advisory -> external Python governed process -> executor`.

After:

`Matrix -> one advisory -> bounded current revalidation -> same governed owner in persistent Runtime`.

- duplicate advisory executions: `2 -> 1`;
- passive subprocess on valid unchanged handoff: `1 -> 0`;
- governed Python process hop on persistent ordinary path: `1 -> 0`;
- durable state/owner/scheduler surfaces added: `0`;
- compatibility subprocess retained only as fail-closed fallback with explicit receipt provenance.

The implementation adds bounded compatibility and timing code, but reduces the executed synchronous architecture by three process/work links. Structural growth is justified and bounded; operational orchestration is shorter.

## Regression and deploy

- Focused affected tests: `41 PASS`.
- Relevant service-failure regressions: `2 PASS`.
- One broader legacy test still fails only because it constructs `AutoswitchPlanner` through `__new__` without current parser arguments; it is outside the changed Runtime path and not masked as a pass.
- Safe-deploy gate: `PASS`.
- GitHub publication and independent deployed fingerprint alignment: `PASS`.
- Intended legacy timer state and single Matrix/Planner owner invariants remained unchanged.

## Final disposition

- `CONSUMER_WALL_FULLY_ATTRIBUTED = PASS`.
- `LARGEST_UNEXPLAINED_P0 = NONE`.
- `DUPLICATE_PRE_GOVERNED_CHAIN = CONSUMED`.
- `PERSISTENT_RUNTIME_GOVERNED_PROCESS_HOP = ENGINEERING_CONSUMED_AND_DEPLOYED`.
- `FRESH_POST_FIX_ORDINARY_SLO_PROOF = WAITING_FOR_NATURAL_ACTIONABLE_ORDINARY_EVENT`.
- `RECOVERY_LATENCY_SLO = NOT_CONSUMED`.

The next lawful action is automatic: on the next fresh owner-backed ordinary affected scope, V7 itself must produce the receipt. That receipt will verify `EXISTING_OWNER_IN_PROCESS`, zero fallback count, full route-writer stage attribution, every member S11 and total T0-to-all-affected-recovered. No manual operational transition is admissible.
