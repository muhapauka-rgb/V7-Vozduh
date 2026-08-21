# V5.3 profile-service and DNS suspicion producers — consolidated engineering report

Date: 2026-08-21 17:17 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Bounded block: `PROFILE_SERVICE_AND_DNS_SUSPICION_PRODUCER_IMPLEMENTATION`  
Terminal: `ACTION_RELEVANT_FAST_SIGNAL_COVERAGE_PARTIAL_WITH_EXACT_RESIDUAL`

## SUMMARY

The missing upstream producer side was implemented inside the existing
`v7-egress-diagnose` owner. It reads active source/profile assignments from
`users.registry` and service semantics from `service-preferences.json`, runs a
bounded exact profile observation through the existing Matrix checker, requires
repeated evidence, and then invokes the existing profile-aware Matrix shadow
receiver. DNS is classified only from DNS-specific checker evidence; generic
curl failure is not treated as DNS failure.

The existing Matrix writer remains the canonical health state. This is still
Engineering/shadow evidence: automatic FAST consumer, production T0/T11
authority, routing, and client movement remain disabled.

## INPUT_STATE

Previous terminal: `FAST_SIGNAL_COVERAGE_PARTIAL`. Previous exact residual:
`REQUIRED_SERVICE_FAILURE`, `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`,
`DNS_FAILURE`, `PARTIAL_CENSORSHIP`, `MULTI_SERVICE_FAILURE`.

Existing profile-aware receiver was already present in
`tools/v7-service-matrix-refresh-all`; this block added the missing upstream
producer and connected it to the existing 30-second health loop without
changing that loop's cadence.

## CODE_DIFF_SUMMARY

Changed:

- `tools/v7-egress-diagnose`: bounded profile/service observation, repeated
  failure gate, DNS-specific classification, profile/required/partial/multi
  class mapping, cooldown and stable trigger IDs, unknown-state STOP_SAFE, and
  invocation of the existing Matrix receiver.
- `systemd/v7-health.service` and `systemd/drafts/v7-health.service`: pass the
  existing Matrix checker/receiver paths to the unchanged 30-second health
  loop. No new timer or scheduler was added.
- `tests/unit/test_v7_egress_diagnose.py`: producer, second-profile, DNS,
  multi, partial, unknown, duplicate, and real receiver/writer tests.

No new owner, Runtime, planner, queue, watcher, registry, state database,
truth source, Authority, route action, or client operation was added.

## PROFILE_SERVICE_PRODUCER

The producer uses only profiles whose users are currently assigned to the
source. It does not contain a global hard-coded service list. It samples the
exact profile subset via the existing `v7-service-matrix-test` command with a
temporary observation file, then removes that temporary evidence. It invokes
the existing receiver only after the configured repeated-failure gate (shadow
default: two observations on the existing 30-second health cadence).

Class mapping:

- one repeated global-required failure → `REQUIRED_SERVICE_FAILURE`;
- one repeated profile-only failure → `OTHER_PROFILE_REQUIRED_SERVICE_FAILURE`;
- repeated degraded service → `PARTIAL_CENSORSHIP`;
- two or more decisive failures → `MULTI_SERVICE_FAILURE`.

A single miss remains `WAITING_REPEAT`; unknown, stale, missing, or conflicting
observation data remains `STOP_SAFE_UNKNOWN` and never wakes Matrix.

## DNS_PRODUCER

`dns_suspicion_producer` is a separate bounded family in the same existing
owner. It fires only when the Matrix checker reports DNS-specific evidence:
`DNS_FAILURE`, `Could not resolve`, or `name resolution`. Generic HTTP/curl
failure is excluded. It reuses the same exact profile subset and existing
Matrix receiver; it creates no DNS truth source.

## EXISTING_OWNERS_REUSED

`v7-egress-diagnose` → `v7-service-matrix-test` (bounded observation) →
`v7-service-matrix-refresh-all` (shadow receiver) → existing Matrix writer,
episode/generation and persistence. Planner and routing owners are not called.

## REAL_PRODUCER_RECEIVER_CHAIN

Polygon proved the full chain with an actual receiver and actual Matrix writer:

```text
synthetic profile failure
  → v7-egress-diagnose producer
  → existing profile-aware shadow receiver
  → v7-service-matrix-test
  → temporary canonical Matrix state in the Polygon
```

The production unit now carries the same producer arguments, but was not
deployed or admitted during this block.

## PROFILE_A_RESULT / PROFILE_B_RESULT

Two synthetic profiles with different service sets were exercised in one
source. The producer forwarded each profile identity separately and the
receiver resolved each profile's own services. No service list was duplicated
in producer code.

## REQUIRED_SERVICE_RESULT

Single failure: no wake on first sample. Repeated failure: bounded
`REQUIRED_SERVICE_FAILURE` suspicion and receiver invocation.

## PARTIAL_CENSORSHIP_RESULT

An isolated degraded service maps to `PARTIAL_CENSORSHIP` suspicion. It remains
observation-only and does not declare the entire source down.

## MULTI_SERVICE_RESULT

Two decisive failures in one profile map to `MULTI_SERVICE_FAILURE`, providing a
stronger confirmation candidate without hard-coding a production threshold.

## DNS_RESULT

Repeated DNS-specific failure maps to `DNS_FAILURE`. A generic HTTP failure does
not map to DNS. Cooldown suppresses duplicate receiver calls.

## CONFIRMATION_POLICY

```text
single/transient failure       → WAITING_REPEAT / no T0
repeated required failure      → bounded Matrix confirmation
multi decisive failure         → stronger bounded confirmation candidate
DNS-specific persistent failure→ bounded Matrix confirmation
ambiguous/partial disagreement → Full DEEP fallback remains available
stale/unknown/conflicting       → STOP_SAFE
recovery                        → existing conservative Matrix recovery path
```

No production threshold was changed. The two-sample setting is an engineering
shadow candidate, not automatic FAST authority.

## PERSISTENCE_REVALIDATION

The former Full cadence/persistence remains the safety fallback. The producer
uses repeated bounded observations at the existing 30-second health cadence;
failure and recovery are intentionally not made symmetric. The 180-second
Matrix persistence remains unchanged for canonical Matrix confirmation.

## BEFORE_AFTER_CAUSAL_TIMING

| Scenario | Before failure→signal | After failure→signal | Signal→T0 | Failure→T0 | T0→T11 | Fast probes |
|---|---:|---:|---:|---:|---:|---:|
| Required service | up to 900 s cadence wait + Full | ≤30 s after first sample, then targeted confirmation | not admitted | not measured | not measured | exact profile subset |
| Other profile service | up to 900 s cadence wait + Full | ≤30 s after first sample, then targeted confirmation | not admitted | not measured | not measured | exact profile subset |
| Partial censorship | up to 900 s cadence wait + Full | ≤30 s after first sample, graded | not admitted | not measured | not measured | exact profile subset |
| Multi-service | up to 900 s cadence wait + Full | ≤30 s after first sample, stronger candidate | not admitted | not measured | not measured | exact profile subset |
| DNS failure | up to 900 s cadence wait + Full | ≤30 s after first DNS-specific sample | not admitted | not measured | not measured | exact profile subset |

The 900-second value is the existing 15-minute cadence; no production timing
gain is claimed because automatic FAST and real T0/T11 execution remain held.

## FULL_MATRIX_ROLE

Full Matrix remains `ASYNC_DEEP_CONFIRMATION`, `DISAGREEMENT_FALLBACK`, and
`REQUIRED_BEFORE_ACTION` where the existing safety contract demands it. The
short producer path is not a route decision and cannot replace Full when state
is stale, unknown, conflicting, target readiness is unavailable, or evidence
disagrees.

## FP_FN_DUPLICATE_FLAP

- first transient miss: no wake;
- repeated evidence: one stable trigger ID;
- cooldown: duplicate receiver invocation suppressed;
- unknown/missing result: STOP_SAFE;
- no parallel duplicate run is created by the producer;
- production FP/FN rates are not yet claimed because this is not production
  admission.

## TARGET_READINESS

Unchanged. The producer never selects a target. Existing Planner state remains
the owner of target health, policy, capacity, generation and role readiness.

## SCALE_PROBE_ECONOMY

Synthetic bounded-run measurements with one profile per source and successful
observations:

| Egresses | Wall time | Profile observations | Receiver invocations |
|---:|---:|---:|---:|
| 7 | 1.891 s | 7 | 0 |
| 50 | 6.868 s | 50 | 0 |
| 100 | 14.017 s | 100 | 0 |
| 1000 | 131.709 s | 1000 | 0 |

The number of bounded observations is linear in active source/profile pairs;
there is no all-egress × all-service Matrix wake. These are Polygon
measurements, not production capacity guarantees.

## MATURE_PATTERN_CONFORMANCE

- HAProxy fall/rise: **ADAPT** — repeated sample gate; no production threshold
  admission.
- Envoy suspicion versus routing truth: **REUSE** — producer is suspicion-only;
  Matrix remains canonical.
- Fortinet service/SLA checks: **ADAPT** — profile-required exact subset.
- Cisco/BFD bounded liveness: **ADAPT** — current-source evidence has bounded
  meaning and duplicate control.
- Google target eligibility separation: **REUSE** — Planner/target owner is
  untouched.

## FROZEN_FAILURE_MATRIX

The five residual classes and regression paths were exercised by deterministic
producer tests; existing causal revalidation covers partial, stale/conflicting,
target-unavailable, capacity/policy, latency/degradation and recovery cases.
No natural production failure was manufactured.

## TESTS

- `tests.unit.test_v7_egress_diagnose`: **18/18 passed**.
- Combined fast-signal suite: **31/31 passed**.
- Existing autoswitch/causal/passive/sentinel suite: **209/209 passed**.
- Full service-failure episode suite: **90 tests; 2 known pre-existing CT-M0F
  failures**, unrelated to this block.
- `python3 tools/v7-truth-check --continue-omp --json`: **PASS**.

## FINAL_COVERAGE

| Failure class | Producer | Owner | Wake latency | Confirmation | Failure→T0 | Full role | Status |
|---|---|---|---|---|---|---|---|
| Required service | profile-service | existing Matrix | ≤30 s after first sample | exact profile subset | not admitted | fallback/deep | shadow-covered |
| Other profile required service | profile-service | existing Matrix | ≤30 s after first sample | exact profile subset | not admitted | fallback/deep | shadow-covered |
| DNS failure | DNS-specific branch | existing Matrix | ≤30 s after first sample | exact profile subset | not admitted | fallback/deep | shadow-covered |
| Partial censorship | profile-service | existing Matrix | ≤30 s after first sample | graded exact subset | not admitted | disagreement/full | shadow-covered |
| Multi-service failure | profile-service | existing Matrix | ≤30 s after first sample | exact profile subset | not admitted | fallback/deep | shadow-covered |
| Quality/loss/jitter | none | existing quality owner | ordinary cadence | Full | not admitted | background | intentionally degraded |
| Clean recovery / fail-recover-fail | none | existing Matrix | recovery cadence | conservative rise | not admitted | recovery-only | recovery-only |
| Stale/unknown/conflict | no producer | existing safety owners | immediate stop | Full/STOP_SAFE | not admitted | required safety | STOP_SAFE |

## FINAL_TERMINAL

```text
ACTION_RELEVANT_FAST_SIGNAL_COVERAGE_PARTIAL_WITH_EXACT_RESIDUAL
```

The engineering producers are implemented and shadow-proven, but production
FAST authority, production T0/T11 timing, FP/FN rates and production scale are
not admitted. The exact residual is now the production-boundary/admission
layer, not an unimplemented producer side.

## PRODUCTION_BOUNDARY

No production deploy, route change, client movement, timer change, threshold
change or automatic FAST enablement occurred. The health unit source now carries
the producer arguments for the next controlled deploy; this source change is
not itself production evidence.

## NEXT_STAGE

Run the controlled deployment/revalidation of the existing health unit, prove
fresh Runtime caller/consumer behavior, and then run the existing T0→T11
before/after proof on an allowed natural or governed controlled lane. Automatic
FAST admission remains a separate gate.

## CANONICAL_KNOWLEDGE_CHANGES

Update the existing CPS and Program to point to this report, preserve the
partial terminal, record that the five producer families are now implemented
in shadow, and set the exact successor to controlled deploy/revalidation.
