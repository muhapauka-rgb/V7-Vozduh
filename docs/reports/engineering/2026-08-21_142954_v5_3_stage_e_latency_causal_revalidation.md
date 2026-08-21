# V5.3 Stage E — latency-causal revalidation of the provisional B+C architecture

Date: `2026-08-21`
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`
Mission: existing V5.3 T0–T11 track; no new Program, Mission, owner or Runtime

## 1. Result

The provisional `TARGET_ARCHITECTURE_MODEL_B_PLUS_C_POST_TOURNAMENT_REVALIDATED`
was revalidated against the causal question: can a passive/FAST signal plus a
bounded service subset reach T0 and start the existing governed recovery before
the full DEEP Matrix completes?

Terminal selected:

```text
B_PLUS_C_LATENCY_CAUSAL_PROOF_PASS
```

This is an Engineering/Polygon proof of the stated timing and safety
conditions, not production maturity and not permission to enable automatic
FAST. The existing Full Matrix remains the safe fallback and production
baseline.

## 2. What was reused

No new vendor survey or Stages B–D rerun was performed. Reused evidence:

- `2026-08-21_100109_v5_3_bottleneck_to_mature_pattern_synthesis.md`
- `2026-08-21_101349_v5_3_stage_c_candidate_failure_matrix_polygon.md`
- `2026-08-21_101600_v5_3_stage_d_polygon_scale_tournament.md`
- `2026-08-21_102100_v5_3_post_tournament_architecture_decision.md`
- `2026-08-21_102900_v5_3_stage_f_before_after_t0_t11_proof.md`
- `2026-08-21_103000_v5_3_stage_g_production_boundary_and_closure.md`

The timing model also reuses the measured spans recorded by the existing
Matrix/controlled-comparison reports: Full Matrix about `85.675 s` and the
governed transaction about `0.023675 s`. Failure-to-signal cadence is modelled
as the configured `900 s`, not Python execution time.

## 3. Method and frozen criteria

`tests/unit/test_v5_3_latency_causal_revalidation.py` is a deterministic,
test-only virtual-clock harness. Every candidate runs the same 12 scenarios:

`HARD_CHANNEL_DOWN`, `TUNNEL_UP_INTERNET_DEAD`,
`TELEGRAM_PERSISTENT_FAILURE`, `REQUIRED_SERVICE_FAILURE`,
`TRANSIENT_FALSE_ALARM`, `PARTIAL_DEGRADATION`, `STALE_OR_UNKNOWN_STATE`,
`CONFLICTING_GENERATION`, `FAILURE_RECOVERY_FAILURE`, `CLEAN_RECOVERY`,
`TARGET_UNAVAILABLE`, `CAPACITY_OR_POLICY_DENIAL`.

The predeclared pass rule was at least 50% reduction in both selected
`FAILURE -> T0` and `T0 -> T11` clocks, with no safety invariant regression.
Fast confirmation is modelled as three samples at four-second spacing; recovery
uses the existing conservative 180-second persistence. These values are
candidate rule changes, not production configuration.

Candidates:

| Candidate | Signal | Evidence | Barrier in this run |
| --- | --- | --- | --- |
| A full/improved Matrix | cadence | full Matrix | full baseline |
| B FAST + DEEP existing owner | cadence | bounded subset | wait for Full DEEP |
| C passive escalation existing Matrix | passive where available | subset + passive | wait for Full DEEP |
| B+C provisional | passive + bounded subset | subset when sufficient | governed recovery may begin; Full runs async/fallback |

## 4. Causal timing result (seconds)

The following rows are representative positive cases. `F->T0` includes signal
delay, confirmation/persistence; `T0->T11` includes the governed transaction
and any selected Full barrier.

| Scenario | A F->T0 | B F->T0 / T0->T11 | C F->T0 / T0->T11 | B+C F->T0 / T0->T11 |
| --- | ---: | ---: | ---: | ---: |
| Hard channel down | 1165.675 | 912.000 / 85.699 | 16.000 / 85.699 | **16.000 / 0.024** |
| Tunnel up, Internet dead | 1165.675 | 912.000 / 85.699 | 16.000 / 85.699 | **16.000 / 0.024** |
| Telegram persistent failure | 1165.675 | 912.000 / 85.699 | 16.000 / 85.699 | **16.000 / 0.024** |
| Required service failure | 1165.675 | 912.000 / 85.699 | 912.000 / 85.699 | **912.000 / 0.024** |
| Clean recovery | 1165.675 | 1088.000 / 85.699 | 192.000 / 85.699 | **192.000 / 0.024** |

For passive-visible failures, B+C improves the modelled `FAILURE -> T0` by
`98.63%` versus A and `T0 -> T11` by `99.97%` versus the current passive/full
barrier path. For required-service failure, passive evidence is absent: the
900-second cadence remains, while removing only the post-T0 Full barrier still
reduces `T0 -> T11` to the governed transaction.

## 5. Safety and barrier result

- Partial degradation and transient false alarm do not produce a switch.
- Stale/unknown state, conflicting generation, target unavailability and
  capacity/policy denial remain `STOP_SAFE`; no client movement is modelled.
- Recovery is deliberately slower than failure confirmation and does not reuse
  the fast failure threshold.
- The Full barrier is scenario-specific: it may be bypassed only when the
  passive signal, bounded subset, freshness, generation, target readiness and
  policy checks are all coherent. Otherwise Full DEEP or STOP_SAFE remains.
- The Full Matrix is retained as asynchronous confirmation/fallback; it is not
  deleted, disabled or demoted as the production safety path.

## 6. Mature-pattern revalidation

The measured causal roles still align with the previously documented mature
patterns: HAProxy fall/rise confirmation, Envoy passive escalation, BFD/Cisco
liveness separation, Fortinet quality/eligibility and Google/HAProxy/Envoy
target eligibility. The V7 consequence is not “replace Matrix”; it is to keep
one Matrix truth while allowing a bounded, role-specific early confirmation
lane and preserving deep confirmation for ambiguous evidence.

## 7. Production boundary and residual

No production route, timer, client, Runtime, Matrix cadence or automatic FAST
consumer changed. No natural ordinary failure was manufactured. Exact action
context and real client-recovery evidence remain unknown; Stage G therefore
remains `STOP_SAFE` for production execution.

The next implementation residual is to express the scenario-specific barrier
and persistence policy in the existing Matrix/health/Planner owners, first in
shadow and controlled Polygon lanes, with Full fallback and rollback proof.
Only after those owner-backed checks can a separate admission decision consider
an automatic FAST consumer.

## 8. Verification

Passed:

- causal revalidation harness: `8/8` tests;
- existing candidate failure-matrix harness: `5/5`;
- controlled Matrix comparison: `6/6`;
- operator execution pipeline: `50/50`;
- decision-lifecycle binding: `8/8`.

The broad service-failure evolution suite reported `7` pre-existing CPS
consistency failures against the post-tournament CPS snapshot
(`CURRENT_COMPLETION_*`, frontier and standing-policy expectations). This turn
did not alter those owners or tests; the failure is retained as a separate
reconciliation item and is not used as evidence for FAST or production
maturity. `tools/v7-truth-check --continue-omp --json` returned `PASS` with no
runtime, routing, authority or user-movement effects.

## 9. Canonical conclusion

The Stage E causal gate is consumed as
`B_PLUS_C_LATENCY_CAUSAL_PROOF_PASS`, while
`V5_3_AUTOMATIC_FAST_CONSUMER_STATUS=HOLD_PENDING_EXPLICIT_PHASE_H_ADMISSION`
and the production STOP_SAFE boundary remain unchanged.

Exact next step: implement the bounded scenario-specific barrier policy in the
existing Matrix owners in a shadow/Polygon lane, then repeat the same 12-case
matrix with owner-backed state, Full fallback and independent Runtime evidence.
