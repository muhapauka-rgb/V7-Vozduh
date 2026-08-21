# V5.3 bounded FAST active-cohort execution tournament

Date: 2026-08-21 21:00 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Block: `BOUNDED_FAST_ACTIVE_COHORT_EXECUTION_DESIGN_AND_POLYGON_TOURNAMENT`  
Terminal: `PREDEPLOY_FAST_OPTIMIZATION_REQUIRED_WITH_EXACT_RESIDUAL`

## SUMMARY

The execution tournament found and implemented the smallest controlled FAST
probe limit that completes 1,000 distinct active source/service contracts in
one pass: **C8**, eight concurrent read-only probes. It completes the fully
healthy controlled 1,000-contract pass in `29.436 s`; C4 needs `34.618 s`, C2
`56.792 s`, and serial `70.932 s`.

However, this is not yet permission to deploy. The actual `v7-health` loop is
`work -> sleep 30`, not a fixed 30-second start-to-start timer. Its legacy
diagnostic/state tail runs in the same process after the FAST phase. Therefore
the next producer observation, required for the second-sample failure gate,
can be delayed by that tail. A fast first pass alone does not prove a bounded
Failure to T0 clock. No safe existing-owner publication/next-cycle isolation
was found in this block without introducing an unmanaged background lifecycle
or a second truth surface. FAST remains held.

## INPUT_TERMINAL

Input terminal was `PRE_DEPLOY_FAST_OPTIMIZATION_REQUIRED`. Already-fixed
scope remains enabled user -> current source -> exact service contract;
the temporary work set is explicitly not persisted, registered or treated as
truth. Candidate B remains controlled-only: two fresh producer samples plus
one targeted Matrix corroboration. Production persistence and recovery are
unchanged.

## ACTIVE_CONTRACT_EXECUTION_MODEL

`v7-egress-diagnose` now builds one immutable in-process
`ACTIVE_FAST_CONTRACT_SET` from the existing `users.registry`,
`service-preferences.json` and egress registry. A row is exactly
`(active source, exact canonical service contract)`. It is held in a temporary
directory and removed before the process exits. It is not an owner, registry,
queue, watcher or durable state.

Only probe workers run concurrently. Each worker calls the existing Matrix
checker with `--probe-observation-only`: it returns exact service evidence but
does not make an ephemeral or canonical Matrix write. The parent alone applies
repeat/cooldown logic and invokes the existing Matrix receiver, so Matrix
writes, episode transition and event decisions remain serialized.

## FAST_VS_LEGACY_PHASE_ISOLATION

The normal diagnostic owner already starts its FAST phase before the broad
legacy diagnose loop. Controlled C8 proves that unrelated slow contracts do
not block a completed contract's producer consequence. A regression creates a
slow contract and a simultaneous failing one; the failure reaches the receiver
before the slow contract completes.

But normal `v7-health.service` runs history, stability, load, diagnose,
state-merge/save and only then `sleep 30`. Its next FAST phase is therefore
not scheduled from the prior FAST phase. This is the exact remaining
deadline-isolation defect.

## TOURNAMENT_CANDIDATES

| Model | Scope | Result |
| --- | --- | --- |
| S / C1 | one read-only probe | baseline |
| C2 | at most two probes | too slow at 1,000 |
| C4 | at most four probes | too slow at 1,000 |
| C8 | at most eight probes | first passing one-pass limit |
| C16 | not retained | C8 passed; wider scope is unnecessary |

Full Matrix cross-egress parallelism remains unchanged and unadmitted.

## 7_50_100_1000_RESULTS

| Active contracts | C1 | C2 | C4 | C8 | C8 meets one-pass 30 s? |
| ---: | ---: | ---: | ---: | ---: | --- |
| 7 | baseline not retested | n/a | n/a | 1.043 s | yes |
| 50 | baseline not retested | n/a | n/a | 2.197 s | yes |
| 100 | baseline not retested | n/a | n/a | 4.101 s | yes |
| 1,000 | 70.932 s | 56.792 s | 34.618 s | 29.436 s | yes |

All rows are the same controlled local response surface: 1,000 active unique
contracts, exact healthy service subsets, zero receiver/writer calls. C8 is
the smallest tested cap passing the 30-second one-pass criterion.

## PER_CONTRACT_LATENCY

For C8 / 1,000: first completed contract `657 ms`, p50 `14.757 s`, p95
`27.568 s`, maximum `28.969 s`; total owner return, including bounded result
aggregation and cleanup, was `29.436 s`. Thus no contract waited for all 1,000
to complete before its own probe result was available.

## FAILURE_DOMAIN_PRESSURE

The controlled global cap is exactly eight checker processes and no more.
There is no canonical failure-domain field in the existing input owners, so no
new derived domain registry or fabricated per-domain limiter was introduced.
The cap itself bounds probe, socket and endpoint pressure; same-source work is
already deduplicated by exact contract. A future domain limiter requires an
existing authoritative domain mapping, not inference in this producer.

## RESOURCE_RESULTS

Measured execution counters for C8/1,000: maximum concurrent probes `8`,
checker starts `1,000`, receiver invocations `0`, Matrix writes `0`, event
writes `0`. The controlled fixture does not represent production CPU/RSS,
open-FD or remote-endpoint capacity, so none are claimed as production values.

## WRITER_SAFETY

Probe workers have no Matrix write path. The existing parent performs all
state/trigger consequences serially; the existing Matrix receiver still owns
its writer lock. A dedicated test proves `--probe-observation-only` creates no
matrix file or second writer. Existing receiver/writer integration tests remain
the proof for the later targeted canonical confirmation.

## DUPLICATE_AND_GENERATION_SAFETY

The worker layer is read-only. Parent-side stable trigger identity, existing
cooldown and one receiver invocation remain unchanged. Unknown/stale/conflict
probe output still becomes STOP_SAFE and does not wake Matrix. Partial or
ambiguous evidence retains Full fallback. No worker can overwrite a generation,
emit an event or create a duplicate incident.

## WINNER

**C8 is the one-pass controlled winner.** It is the first cap meeting the
30-second pass deadline, while C4 misses it by `4.618 s`. C8 is accepted only
as an explicit controlled capability in the existing owner; normal invocation
continues at serial C1 and the systemd source is untouched.

## CODE_DIFF

- `tools/v7-egress-diagnose`: temporary active contract work set, controlled
  `--fast-producer-concurrency 1..8`, streaming result collection, serial
  consequence processing, per-contract timing telemetry and interface reuse.
- `tools/v7-service-matrix-test`: `--probe-observation-only`, a read-only probe
  result mode used only before the separate canonical receiver confirmation.
- tests cover bounded cap, rejection outside controlled mode, streaming past an
  unrelated slow contract, no second Matrix write and legacy failure safety.

No systemd source, production timer, automatic FAST flag, route, user, Matrix
owner, planner, queue, registry or truth source was changed.

## CANDIDATE_B_FAILURE_POLICY

Candidate B remains the existing controlled/shadow contract:

```text
two fresh same-scope producer observations
 -> exact existing Matrix receiver
 -> one targeted Matrix corroboration
 -> canonical failure candidate
```

The explicit controlled persistence override is guarded by observation-only
shadow trigger validation. The universal production 3-sample/180-second
default was not changed. B is never used for partial ambiguity, quality-only
degradation, stale/unknown/conflict, target-not-ready or recovery.

## FAILURE_TO_T0

Within one C8 pass, per-contract result p95 is `27.568 s`; a completed exact
failure can reach the parent receiver without waiting for remaining contracts.
The earlier controlled Candidate B causal model remains `30.341-60.341 s`
only when two producer phases are actually available on the expected cadence.

That condition is not yet proven for the normal health service because it
sleeps after its whole serial tail. Therefore production-like Failure to T0 is
still `UNKNOWN`; no reduction from the old canonical model is claimed.

## T0_TO_T11

The existing governed Polygon transaction is unchanged: fresh target state
gives the prior synthetic T0 to T11 result `0.023675 s`. Stale, conflicting,
unavailable or capacity-denied target state remains STOP_SAFE/Full revalidation.
No downstream architecture was reopened.

## FAILURE_TO_T11

The bounded one-pass C8 result reconnects to the existing Polygon only as a
conditional model. `Failure to T11 = Failure to T0 + 0.023675 s` if the next
producer phase is deadline-bounded and target state is fresh. The first
condition is the unresolved residual, so production-like Failure to T11 stays
`UNKNOWN`.

## RECOVERY_INVARIANTS

Recovery remains the existing conservative Matrix rise/cooldown/re-admission
path. `fail -> one healthy observation -> fail` does not gain early
re-admission from C8 or Candidate B. No recovery threshold changed.

## FULL_MATRIX_ROLE

Full Matrix remains deep/background observation, disagreement fallback and the
required path for stale, conflicting, ambiguous/partial or target-readiness
uncertainty. C8 only accelerates bounded suspicion probes and cannot select a
target, switch traffic or alter a route.

## REGRESSION_RESULTS

- focused changed suite: `52/52 PASS`;
- new parallel/streaming and no-second-writer regressions: PASS;
- full service-failure suite: `95` run, `93 PASS`, with the two known unrelated
  CT-M0F failures in standing-source and active-binding tests, unchanged from
  the preceding block;
- shell syntax and whitespace checks: PASS.

Existing producer tests cover transient/repeated/DNS/multi/partial/unknown,
duplicate cooldown and actual receiver/writer paths. Existing causal suites
cover stale, conflict, target unavailable, capacity denial and recovery.

## FINAL_PREDEPLOY_GATE

| Cohort | Before serial | C8 controlled | Delta | one-pass <=30 s |
| ---: | ---: | ---: | ---: | --- |
| 7 | 1.774 s prior baseline | 1.043 s | -41% | yes |
| 50 | 4.237 s prior baseline | 2.197 s | -48% | yes |
| 100 | 9.433 s prior baseline | 4.101 s | -57% | yes |
| 1,000 | 70.932 s | 29.436 s | -58% | yes |

| Scenario | current confirmation model | C8 plus B | T0 to T11 | Failure to T11 |
| --- | --- | --- | --- | --- |
| exact persistent eligible failure | 210-240 s controlled model | 30-60 s only if next phase bounded | 0.023675 s synthetic | conditional / not production-proven |
| stale, conflict, partial, target unavailable | STOP_SAFE/Full | unchanged | STOP_SAFE/Full | no action |

## FINAL_TERMINAL

```text
PREDEPLOY_FAST_OPTIMIZATION_REQUIRED_WITH_EXACT_RESIDUAL
```

One-pass C8, worker safety, streaming semantics and Candidate B controlled
policy pass. The terminal remains non-pass only because the existing health
loop cannot yet guarantee the second producer phase after 30 seconds while its
legacy tail is still active. This is a measured lifecycle defect, not a request
for more generic research or a reason to enlarge C8.

## NEXT_STAGE

`EXISTING_V7_HEALTH_FAST_PHASE_PUBLICATION_AND_NEXT_PHASE_DEADLINE_ISOLATION`:
using the same health/diagnose/Matrix owners, establish a safe single-writer
way to publish an already completed FAST phase and begin the next FAST phase on
deadline without background orphan work, a second state surface, timer, queue
or new owner. Then measure two consecutive C8 phases and the full
Failure -> T0 -> T11 controlled path. Controlled deploy remains prohibited
until that exact successor passes.

## CANONICAL_KNOWLEDGE_CHANGES

- temporary `ACTIVE_FAST_CONTRACT_SET` is execution memory only, never truth;
- C8 is the smallest passing controlled one-pass model for 1,000 active exact
  contracts; probe cap is eight and Matrix consequences stay serialized;
- first completed result is streamed, rather than waiting for the batch;
- `v7-health` currently sleeps after all work, so successive FAST phase timing
  remains unproven; automatic FAST remains held.

## PRODUCTION_EFFECT

None. No deploy, systemd alteration, automatic FAST enablement, route change,
client movement, canonical persistence-default change or recovery-policy change
was made.
