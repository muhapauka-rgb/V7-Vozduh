# V5.3 N9 Full Scale and Critical Path Tournament

Date: 2026-08-23 (Europe/Moscow)  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Phase: `N9 FULL_SCALE_AND_CRITICAL_PATH_TOURNAMENT`  
Runtime commits: `d24c7b66`, `63fd4128`, `b8d16492`  
Safe deploys: `deploy-z8-14-Updatesystem-d24c7b6-20260823T173301`, `deploy-z8-14-Updatesystem-63fd412-20260823T174458`, `deploy-z8-14-Updatesystem-b8d1649-20260823T175055`

## Terminal

`N9_COMPLETE`; next phase is `N10_BOUNDED_ORDINARY_ROLLOUT`.

The mandatory `7/50/100/1000 egress x 250/500/10000 users x one/few/many profile` grid passed all 36 cells. Health work is proportional to active sources, distinct declared profile contracts, bounded hot targets and active incidents, not to the raw user count. Full Matrix remains the staggered DEEP/fail-safe fallback.

## Implemented existing-owner changes

- `v7-egress-diagnose`: one-pass interface inventory and batched local-state writes; no per-user liveness probe.
- `v7-users-autoswitch`: exact profile-required services are separated from best-effort ranking services. Prepared class rows reference globally deduplicated target/service contracts instead of embedding duplicates.
- `v7-service-matrix-test`: before opening sockets, the N3 role computes its physical timeout bound. A role exceeding five seconds starts zero FAST probes and returns `NO_5S_PROFILE_SERVICE_ROLE_CAPACITY`; the existing staggered DEEP Full Matrix is retained.
- `v7-service-matrix-refresh-all`: path-only profiles retain their official Planner-selected target.
- prepared top-H selection is rebuilt for changes to membership, topology, policy, required-service routing, capacity or anti-flap state and periodically within 300 seconds. A new Matrix observation updates target readiness but does not force an O(N) Planner rebuild.
- the one existing `v7-health.service` owner separates FAST starts by 250 ms, gives background roles lower CPU priority and admits only one slow role at a time. No timer, daemon, queue, cache, registry, state owner or Matrix writer was added.

## Mandatory scale evidence

| Case | Prepared classes | Deduplicated hot contracts | Projection size | Build time | Peak temporary allocation |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1000 egress / 10000 users / one profile | 1,000 | 4 | 1,104,599 B | 706.346 ms | 5,541,967 B |
| 1000 / 10000 / few profiles | 3,000 | 12 | 3,334,006 B | 781.867 ms | 16,569,156 B |
| 1000 / 10000 / many profiles | 10,000 | 40 | 11,148,460 B | 989.046 ms | 49,545,200 B |

Across all 36 cells:

- maximum projection size: `11,148,460 B`;
- maximum construction time: `989.046 ms` on the local Polygon host;
- maximum temporary allocation: `49,545,200 B`;
- 1,000-source local HARD inventory: `117.855 ms`, zero one-second deadline miss;
- concurrency caps: other-service `128`, hot target `16`, DEEP `16`;
- modeled maximum Matrix writer/lock rate: `3.911/s`, batched by role rather than by user;
- `1000 x 14 x 1-second` HTTP probing remains forbidden.

Worst many-profile demand contains 12,000 other-service probes per five-second pass. Its physical bound is 47 seconds at C128, so it is correctly rejected before opening sockets and routed to staggered DEEP. This is a capacity truth, not a false FAST success.

The modeled maximum network rate is `1029.156 probes/s` only in the deliberately adversarial case where all 1,000 active sources declare Telegram critical; it consists primarily of one rotating Telegram endpoint per declared source plus `13.6/s` bounded hot-target and `15.556/s` DEEP work. For path-only profiles the application-probe component is zero and only `15.556/s` staggered DEEP remains. Modeled upper traffic bound for the adversarial case is about `4.41 MB/s`. These are conservative model bounds, not packet-capture measurements.

## Production before/after

Before deadline isolation, simultaneous role startup and repeated Planner work produced 35 deadline misses in a short observation window. Observed maxima reached HARD `1.551 s`, Telegram `2.458 s`, hot target `3.909 s`, other required `4.926 s`, hot-target other `6.373 s`, DEEP `6.073 s`; an earlier Planner projection took `16.4 s` and the service peaked near `384.2 MiB`.

After the final deployed isolation, a continuous 126-cycle sample reported:

| Production role | Samples | P50 | P95 | Max | Non-zero exits |
| --- | ---: | ---: | ---: | ---: | ---: |
| HARD | 126 | 128 ms | 327 ms | 524 ms | 0 |
| Telegram-required | 126 | 428 ms | 736 ms | 1,113 ms | 0 |
| prepared hot-target PATH | 122 | 429 ms | 800 ms | 1,162 ms | 0 |
| hot-target other required | 24 | 1,079 ms | 2,554 ms | 2,714 ms | 0 |
| source other required | 19 | 654 ms | 1,670 ms | 1,670 ms | 0 |
| prepared Planner projection reuse | 3 | 1,052 ms | 1,154 ms | 1,154 ms | 0 |
| staggered DEEP slice | 1 | 4,680 ms | 4,680 ms | 4,680 ms | 0 |

The sample had four skipped one-second hot-target starts and one skipped Telegram start while a preceding invocation was still completing. This makes the worst effective observation gap approximately two seconds and remains inside the Program's HARD/PATH/Telegram P95 `<=3 s`, max `<=5 s` law. It is recorded rather than hidden. Nine background invocations were intentionally deferred instead of overlapping another slow role; DEEP still completed and its 900-second coverage horizon remains intact.

Final service snapshot: active, about `23.7 MiB` current memory, `138.2 MiB` peak in the sampled lifecycle. The prior Full and Telegram timers remained disabled/inactive. No route or Authority changed and no client was moved by N9.

## Tests and falsification

- `228` focused autoswitch, role-health, pre-ready, DEEP, causal and scale tests: PASS.
- `185` autoswitch policy tests included in the focused set: PASS.
- Python compile with isolated pycache: PASS.
- `git diff --check`: PASS.
- Stable selection reuse remains valid across Matrix observation changes.
- User-membership change invalidates reuse and forces a rebuild.
- Unknown/stale/conflicting data remains fail-closed; over-budget N3 begins zero FAST probes.
- Production hashes matched the deployed `v7-users-autoswitch` and `v7-health-loop` files; GitHub/current branch equality passed in safe deploy.

## Production effect and limits

Production now uses bounded role-based health and target readiness through the existing Matrix/Planner owners. N9 does not claim T11 client telemetry, an ordinary natural failure, or completion of N10/N11. The current two-vCPU host meets the measured current seven-egress workload, but the 1,000-source adversarial Telegram case is an explicit capacity boundary and would require endpoint sharding/budget admission or more compute before production admission; the tournament does not pretend otherwise.

## Exact next step

Execute N10 in the existing Polygon/production certification substrate: controlled single identity, one ordinary-like certification case, then a small bounded certification cohort with pre-bound rollback. Do not manufacture an ordinary-user failure and do not claim T11 without independent client telemetry. After N10, run N11 whole-system zero-residue reconciliation.
