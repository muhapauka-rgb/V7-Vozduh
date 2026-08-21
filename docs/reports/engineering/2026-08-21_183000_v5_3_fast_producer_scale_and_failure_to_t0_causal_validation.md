# V5.3 FAST producer: scale and Failure to T0 causal validation

Date: 2026-08-21 18:30 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Bounded block: `FAST_PRODUCER_SCALE_AND_FAILURE_TO_T0_CAUSAL_VALIDATION`  
Terminal: `PRE_DEPLOY_FAST_OPTIMIZATION_REQUIRED`

## SUMMARY

The pre-deploy gate is not passed and FAST was not deployed. The producer was
corrected in place: it builds one active `egress -> exact-service-contract`
view per cycle, observes only current user-serving sources, and coalesces users
with the same source and service set. This removes the false
`users x profiles x services` cost.

It does not solve a separate real limit: 1,000 simultaneously active distinct
source/contracts still take `80.357 s` in the controlled producer surface. The
existing 30-second health service retains a serial broad diagnostic tail. There
is no admitted existing scheduling/concurrency contract that can safely make
that a <=30-second production cycle. The exact residual is therefore a bounded,
failure-domain-safe execution model for a genuinely 1,000-active cohort.

The causal experiment also established duplicate confirmation latency: the
producer has two repeated observations and current Matrix then adds three
samples/180 seconds. Current policy reaches canonical failure at roughly
`210.341-240.341 s`; the controlled owner-backed candidate reaches it at
`30.341-60.341 s` while retaining a targeted Matrix corroboration. The
candidate exists only as an explicit Polygon observation override. Production
policy, recovery, routes, clients, cadence and automatic FAST are unchanged.

## INPUT_IMPLEMENTATION

Input commit: `84fbf0b6`. Reused chain:

```text
existing v7-health 30-second service
 -> v7-egress-diagnose -> v7-service-matrix-test exact subset
 -> v7-service-matrix-refresh-all shadow receiver
 -> existing Matrix writer, episode and persistence owner
```

The health service arguments and cadence were not changed. The new
`--fast-producer-only` surface is controlled-observation-only: explicit output
and existing receiver are mandatory, normal diagnostic state is not overwritten
by default, and it is not connected to systemd.

## PRODUCER_EXECUTION_DAG

```text
users.registry + service-preferences.json
 -> enabled current-source filter
 -> distinct(source, sorted exact services) contract coalescing
 -> interface-up -> exact profile probe -> two producer observations
 -> exact existing Matrix receiver -> targeted Matrix probe/persistence
 -> canonical FAILURE CONFIRMED (T0), or STOP_SAFE/no event
```

Before this block, the normal loop also walked every `egress.registry` row,
reparsed user/profile data per egress, and ran broad diagnostics serially.
Exact probes are network/checker subprocess work; discovery and `awk` lookups
are process work; Matrix writes are serialized but not held during probes.

## 1000_EGRESS_ROOT_CAUSE

The previous `131.709 s` is classification **D, combination**, not the cost of
one ordinary FAST decision. It used 1,000 synthetic active distinct
source/profile contracts, included broad per-egress traversal/reparsing and
serial probe startup, and normal invocation also has the broad legacy tail.
It is not just a harness artifact: after repair, a genuinely 1,000-active
distinct cohort still has a real serial limit of `80.357 s`.

## SCOPE_AND_DEDUP_MODEL

FAST scope is enabled users' `current` source egresses only. For each source,
the minimum set of exact sorted service contracts is built once. Cold,
unassigned, disabled, drained and certification-only registry rows get no
profile FAST observation. A source with no profile contract can use the
existing global required-services fallback.

10,000 users on one source with the same `google,telegram` contract yield one
probe, not 10,000: `0.672 s`, one active source, one contract, one observation.
A 1,000-row registry with only seven active contracts yielded `1.410 s` and
seven observations. These are controlled Polygon facts, not live capacity
claims.

## CODE_CHANGES

- `tools/v7-egress-diagnose`: precompute active contracts once, deduplicate by
  `(source, exact services)`, perform that decision-critical pass before legacy
  diagnostics, export counts, and provide a guarded controlled-only surface.
- The controlled surface can pass an exact Matrix persistence candidate only to
  the existing observation-only shadow receiver.
- `tools/v7-service-matrix-refresh-all`: forwards that candidate only for a
  valid shadow trigger and forwards its existing event directory to the checker.
  This fixes a failure-path defect where controlled writes could use the default
  production event path after Matrix state had been written.
- Failed receiver calls now preserve their true non-zero exit code.

No owner, Runtime, planner, queue, registry, database, scheduler, Authority,
route or client operation was added or changed.

## SCALE_BEFORE_AFTER

| Controlled cohort | Before | After | active / contracts / observations | receiver / writer |
| --- | ---: | ---: | --- | --- |
| 7 distinct active | 1.891 s | 1.774 s | 7 / 7 / 7 | 0 / 0 |
| 50 distinct active | 6.868 s | 4.237 s | 50 / 50 / 50 | 0 / 0 |
| 100 distinct active | 14.017 s | 9.433 s | 100 / 100 / 100 | 0 / 0 |
| 1,000 distinct active | 131.709 s | 80.357 s | 1,000 / 1,000 / 1,000 | 0 / 0 |
| 1,000 registry rows, 7 active | n/a | 1.410 s | 7 / 7 / 7 | 0 / 0 |
| 10,000 users, one contract | n/a | 0.672 s | 1 / 1 / 1 | 0 / 0 |

The 7/50/100 after values were rerun after the code change. The 1,000-active
after result is the same controlled fixture measured in this block; seriality
is independently shown by the owner DAG. CPU/RAM and production network use
are not claimed because the local response surface is not a production model.
Healthy process starts equal exact observations; no receiver/writer is called.

`FAST_PRODUCER_EXECUTION_COST_MODEL`:

```text
one profile-map parse + active-source selection
+ sum(distinct source/service-contract)[interface lookup + checker process]
+ sum(repeated failure only)[receiver + targeted Matrix write]
+ legacy broad diagnostic tail in normal health invocation
```

## FAILURE_TO_T0_CAUSAL_TRACE

The controlled chain used the real existing receiver and Matrix writer with a
deterministic exact-service failure. Owner-clock causal sequence:

| Point | Owner/evidence | consequence |
| --- | --- | --- |
| failure | controlled response surface | wait for next producer phase |
| T1 first sample | `v7-egress-diagnose` | count 1, `WAITING_REPEAT` |
| T3 second sample | same owner, 30-second cadence | stable exact receiver wake |
| T5 targeted probe | Matrix checker/writer | about 0.341 s in fixture |
| T6 persistence | canonical Matrix | current policy requires 3 receiver samples/180 s |
| T7 = T0 | canonical episode | `FAILURE CONFIRMED` only here |

Virtual-cycle outcomes: A/current first event at cycle 4; B/owner-backed at
cycle 2; C/intermediate at cycle 3. The second producer sample is the first
receiver invocation; A's extra delay is the Matrix stack, not producer delay.

## PHASE_ALIGNMENT

| Policy | Failure to T0 min | representative | max |
| --- | ---: | ---: | ---: |
| A current: producer 2 + Matrix 3 | 210.341 s | 225.341 s | 240.341 s |
| B candidate: producer 2 + targeted Matrix | 30.341 s | 45.341 s | 60.341 s |
| C intermediate: producer 2 + Matrix 2 | 120.341 s | 135.341 s | 150.341 s |

Current 60-second cooldown is inclusive at the boundary, producing effectively
90-second receiver repeats in the 30-second service. These are causal bounds,
not production SLOs.

## PRODUCER_CONFIRMATION_LATENCY

Two fresh exact producer observations cost `30-60 s` from failure
(representative `45 s`). First transient evidence never wakes Matrix. The
producer remains suspicion-only and does not select a target or call routing.

## MATRIX_CONFIRMATION_LATENCY

Under A, after producer confirmation Matrix adds about 180 seconds and the
targeted probe. Under B targeted canonical observation remains required but the
universal repeated failure persistence is not added. C retains one extra
bounded Matrix repeat.

## 180S_PERSISTENCE_REVALIDATION

| Policy | producer | Matrix after wake | first canonical failure cycle | result |
| --- | --- | --- | ---: | --- |
| A current | 2 samples | 3 samples / 180 s | 4 | safe, duplicate latency |
| B owner-backed | 2 samples | one targeted corroboration | 2 | controlled candidate |
| C intermediate | 2 samples | 2 Matrix samples / 60 s candidate | 3 | controlled candidate |

B is sufficient only for exact persistent failure classes after two fresh,
same-scope producer observations. It neither changes the canonical default nor
weakens stale/conflict/target gates.

## FAILURE_VS_RECOVERY_POLICY

Future `FAILURE_CONFIRMATION_POLICY` candidate: two fresh producer failures
plus targeted Matrix corroboration. `RECOVERY_READMISSION_POLICY` is unchanged:
existing Matrix rise, cooldown and re-admission decide recovery. Failure
persistence is not reused to speed recovery; fail-recover-fail is fresh.

## FP_FN_FLAP_RESULTS

All twelve required A/B/C virtual-clock scenarios ran: one/two-close transient,
persistent required, multi-decisive, DNS transient/persistent, partial,
healthy-after-one, fail-recover-fail, stale, conflicting generation and target
not ready. No candidate caused a false action or recovery-policy change.

- transient and healthy-after-one: no canonical failure;
- two-close transient: may wake Matrix, healthy target probe creates no event;
- persistent/DNS/multi: B reaches its controlled canonical candidate earlier;
- partial, stale, unknown, conflict and target-not-ready: Full fallback or
  STOP_SAFE only;
- stable trigger IDs/cooldown retain one duplicate-safe wake.

This is Polygon safety evidence, not a production FP/FN rate.

## TARGET_READINESS_TIMING

Target readiness is outside Failure to T0. With fresh exact Planner state, the
existing Polygon governed T0 to T11 transaction is `0.023675 s`. With stale,
unknown, conflicting, unavailable or capacity-denied target state, the existing
owner returns STOP_SAFE/Full revalidation; timing is `UNKNOWN` and is not added
to the failure clock.

## T0_TO_T11_RESULT

The existing one-synthetic-client Polygon transaction remains connected and
unchanged: Candidate -> Packet -> Lease -> Barrier -> Apply fixture ->
Verification -> Feedback completed in `0.023675 s`. It is not a production
client-switching-time claim.

## FAILURE_TO_T11_RESULT

| Scenario family | A current | B candidate | C candidate |
| --- | ---: | ---: | ---: |
| hard/tunnel/required/other-profile/DNS/multi, target fresh | 210.365-240.365 s | 30.365-60.365 s | 120.365-150.365 s |
| partial/stale/conflict/target unavailable/capacity denial | STOP_SAFE/Full | STOP_SAFE/Full | STOP_SAFE/Full |

The old Full-only reference remains up to 900-second cadence phase plus the
observed `85.675 s` Full Matrix lifecycle, before governed downstream work.

## FULL_MATRIX_ROLE

Full Matrix remains live baseline, deep confirmation and disagreement fallback.
It is required for partial/ambiguous, stale, unknown, conflict, target-unready
or short/full-disagreeing evidence. FAST cannot route, select a target or
replace Planner readiness.

## MATURE_PATTERN_CONFORMANCE

- HAProxy: adapt fast fall / slower rise; recovery stays conservative.
- Envoy: reuse bounded suspicion then canonical confirmation, never action.
- Fortinet: adapt exact decision-critical service observation, not broad sweep.
- BFD/Cisco: adapt cheap liveness isolated from service truth.
- Google: reuse independently current target eligibility.

No vendor numeric default was copied.

## FINAL_DECISION

```text
PRE_DEPLOY_FAST_OPTIMIZATION_REQUIRED
```

Scope and user dedup are fixed and the causal/persistence evidence nominates B
for future controlled policy admission. This block cannot pass: 1,000 truly
active distinct contracts violate the 30-second execution rule, and the normal
health lifecycle has no admitted deadline-safe isolation from its serial tail.

## DEPLOYMENT_READINESS

Not ready. No controlled deploy, automatic FAST admission, policy/cadence/
timeout change, Matrix architecture change, route change or client movement
occurred. An existing-owner execution design must first prove 1,000 relevant
contracts meet the deadline without writer race, duplicate incident, network
storm or coupled failure domain.

## NEXT_STAGE

`BOUNDED_FAST_ACTIVE_COHORT_EXECUTION_DESIGN_AND_POLYGON_TOURNAMENT`: reuse
health/Matrix owners to determine whether bounded concurrency or an existing
owner-backed deadline-isolated lane can serve only active source/contracts, then
measure 7/50/100/1000 with writer, network, duplicate and failure-domain
invariants. Only PASS may re-enter `CONTROLLED_FAST_DEPLOY_AND_ADMISSION`.
This is the smallest existing V5.3 frontier, not a new Program or Mission.

## CANONICAL_KNOWLEDGE_CHANGES

- 1,000-row former timing is combined synthetic broad/serial cost, not ordinary
  FAST decision cost.
- FAST scope is active source plus exact service contract, never O(users).
- two producer samples plus current Matrix persistence duplicate failure delay;
  B is controlled-only.
- exact residual is safe execution for 1,000 genuinely active distinct
  contracts; automatic FAST remains held.

## TESTS_AND_LIMITS

- focused new/changed tests: `27/27 PASS` (dedup, output guard, receiver exit,
  persistence forwarding/guard and causal model);
- expanded relevant suite: 140 tests run, 138 PASS; two known pre-existing
  CT-M0F failures remain in
  `test_ct_m0f_standing_source_selection_reuses_controlled_pool_owner` and
  `test_ct_m0f_active_service_failure_binding_requires_accounted_live_owner`;
  they do not exercise these producer/receiver changes;
- shell syntax and whitespace checks: PASS.

All scale and causal facts are controlled Polygon evidence. Production
caller/consumer behavior, live resource use, T0-T11 distribution and
client-visible recovery remain unproven and are not claimed.
