# V5.3 T0–T11 — proven bottleneck to mature-system pattern synthesis

Date: 2026-08-21 10:01 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Stage: **B — mature-system synthesis**  
Status: `SYNTHESIS_CONSUMED; CANDIDATE_TOURNAMENT_NOT_STARTED`

## Purpose and evidence boundary

This is a synthesis of already collected V7 measurements and the existing
Envoy, HAProxy, Google Cloud, FRR/BFD, Cisco, Fortinet and MikroTik material.
It is not a new generic vendor survey and it does not select an architecture.
The former `TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT` and
`TARGET_ARCHITECTURE_MODEL_B_PLUS_C` remain candidate inputs only.

Measured V7 facts used here:

- the latest full Matrix cycle was `85.675 s` lifecycle / `87.192 s` wall time;
- seven egresses were traversed serially, with 14 service checks per egress;
- the planned Matrix cadence is 15 minutes plus up to 60 seconds jitter;
- the existing exact subset reduced checks `14 → 3` (`78.6%`) and controlled
  probe time by about `56–75%`, depending on the isolated measurement surface;
- bounded caller timing showed short/full elapsed reduction of `74.6%` and
  check reduction of `78.6%`;
- the synthetic Candidate→T11 fixture was milliseconds and is not production
  latency evidence.

## Synthesis matrix

| Proven V7 bottleneck | Mature mechanism that addresses it | Why it fits this bottleneck | Existing V7 owner | Decision | Candidate/tournament implication | Falsifying measurement |
| --- | --- | --- | --- | --- | --- | --- |
| Long discovery wait from 15-minute cadence | HAProxy normal/transition/down intervals; Envoy passive outlier signal; FRR/Cisco BFD-style fast liveness; existing Telegram sentinel | A cheap signal can accelerate suspicion while normal/deep cadence remains intact | Matrix owner plus existing sentinel; OMP/Planner remain consumers | **ADAPT**: event-accelerated bounded confirmation; **REJECT** copied BFD timings and any new scheduler | Candidate dimension: normal/transition/degraded cadence with passive escalation | Compare event-to-confirmation delay, false alarms and probe budget against current 15-minute baseline; reject if passive escalation adds duplicate or unstable events |
| Serial full traversal of ~86 s across egresses | HAProxy role/transition intervals; Envoy active checks with bounded outlier handling; role-based probe cohorts in mature load balancers | Decision-critical source/hot-target checks need not wait for every cold/deep egress | Existing Matrix refresh-all and Matrix test; no new owner | **ADAPT**: exact source/hot-target subset; **REJECT** unmeasured cross-egress parallelism as the first fix | Candidate dimension: bounded hot cohort and deferred DEEP; concurrency tested separately | At 7/50/100/1000 egresses measure T0→confirmation, total probes, external pressure, lock/RSS; reject if savings disappear or failure domains couple |
| 14 checks per egress when only required services decide the path | Google protocol-aware health checks; Envoy protocol-specific active checks; Fortinet multiple SLA checks | Required service evidence is more precise than a generic ping and cheaper than the full profile | Matrix `--services` selector and existing writer/schema | **REUSE/ADAPT** exact service subset; **REJECT** generic single-host ping | All candidates must preserve full Matrix fallback and compare short/full on the same failure matrix | Short/full disagreement, missed required-service failure, or subset false positive causes automatic fallback and candidate exclusion |
| Failure confirmation can wait for persistence (3 samples/180 s) | HAProxy `fall/rise`; Google sequential healthy/unhealthy thresholds; Envoy ejection/recovery thresholds | Explicit fall/rise makes failure and recovery asymmetry measurable instead of implicit | Matrix episode/persistence; Planner cooldown | **ADAPT** existing persistence to explicit state/role thresholds; no copied vendor numbers | Candidates must expose healthy/suspect/down/recovering transitions | Replay single timeout, burst, persistent failure and recovery; reject if FP/FN or recovery delay worsens beyond baseline |
| Source health and target readiness are different questions | Google backend eligibility; Cisco IP SLA/Object Tracking; Fortinet SLA member usability; MikroTik gateway→route separation | A failed source must not imply that any target is ready; target requires freshness, role, capacity and quality | Matrix health; Planner/capacity/reserve/policy/route owners | **REUSE** separation; **REJECT** Matrix-owned route selection | Candidate contract must have separate source-confirmation and target-admission gates | Inject healthy source with stale/unknown target, capacity shortage or policy mismatch; any target admission is failure |
| Quality/stability evidence can be slow and noisy | Fortinet Performance SLA latency/loss/jitter; Envoy degraded/ejected/outlier state; HAProxy transition/hold-down | Quality should classify/deprioritize and prevent flapping, not synchronously scan raw history | Existing quality compactor, stability projections and Planner | **ADAPT** compact current projections; **REJECT** raw-history hot-path scan and quality-only rescue | Candidate dimension: degraded/recovering state and target ranking; not a new health truth | Compare quality-only degradation, hard failure and recovery scenarios; reject if quality can trigger rescue without hard confirmation or if raw-history cost grows with users |
| Stale, unknown or conflicting data can produce unsafe decisions | Google eligibility gates; Cisco tracked-state dependency; mature systems with unhealthy/unknown exclusion | Eligibility must fail closed when required evidence is not fresh or coherent | Existing Planner freshness/path-generation gates and full fallback | **REUSE** fail-closed semantics; **REJECT** last-known-good promotion without freshness | Every candidate must carry freshness, generation and conflict predicates into the same Matrix/Planner path | Replay stale, expired, generation mismatch and conflicting rows; any route/apply eligibility is a candidate failure |
| Recovery/re-admission risks flapping | HAProxy `rise`; Envoy ejection backoff/recovery; Cisco dampening; MikroTik route distance recovery | Recovery must require newer repeated success and readiness, more conservative than failure | Existing Matrix recovery receipts, Planner cooldown and reconciliation | **ADAPT** explicit recovering/rise/re-admission state; **REJECT** immediate one-probe return | Candidate must compare failure speed against recovery safety and preserve quarantine/cooldown | Fail → one success → fail and fail → repeated success; reject early re-admission, oscillation or lost recovery receipt |
| Passive signals can become a second health/event system | Envoy passive outlier detection; Cisco object tracking; Telegram sentinel as existing bridge | Passive evidence is valuable for early suspicion, but canonical state must remain single-writer | Existing sentinel → Matrix owner → canonical event; Planner consumer | **REUSE/ADAPT** escalation only; **REJECT** direct route action or duplicate event family | Candidate must prove passive signal coalesces into existing Matrix episode and event | Burst passive errors with healthy active probes; reject duplicate episodes, direct route action or disagreement without full fallback |

## Common owner and state contract

All candidate variants must preserve this topology:

```text
probe/passive producer
→ existing Matrix writer and row/episode state
→ freshness/persistence/quality projections
→ existing Planner target/route gates
→ existing Candidate/Packet/Lease/Barrier/Apply/Verification path
```

The Matrix remains the canonical health writer. Planner remains the owner of
target suitability and route choice. Quality/history remain compact background
projections. Route/kernel and post-switch verification remain separate from
Matrix health. No candidate may add an owner, Runtime actor, queue, watcher,
registry, state store, cadence scheduler or source of truth.

## Candidate inputs produced by this synthesis

This matrix produces three neutral candidate families for the next block:

1. **Candidate A — improved full Matrix:** retain full observation and improve
   thresholds/state semantics without a decision-path subset.
2. **Candidate B — bounded FAST + DEEP under existing Matrix owner:** exact
   source/hot-target subset for the decision path, full Matrix as fallback and
   background/deep evidence for cold/broad diagnostics.
3. **Candidate C — passive-escalation variant:** existing passive signals
   accelerate bounded confirmation through Matrix, without a second event or
   health owner.

Role-aware/adaptive behavior is a dimension to measure across A–C. It becomes
a separate candidate only if the tournament proves A–C insufficient and the
new variant still reuses the same owners and state surface.

## Rejected shortcuts

- Do not change the 15-minute timer merely because it is visible; first measure
  event-accelerated confirmation and its budget.
- Do not claim cross-egress parallelism is the solution; it is a measured
  tournament dimension with lock, network and failure-domain constraints.
- Do not treat a healthy tunnel, one ping, quality history or a synthetic
  millisecond transaction as proof of service or client recovery.
- Do not allow short results, passive signals or stale data to bypass full
  fallback, Planner gates or post-switch verification.

## Stage B conclusion and exact next step

Stage B synthesis is complete as an Engineering input. It has not selected a
winner and has not authorized implementation.

Exact next step: build the shared Polygon failure-matrix harness for Candidates
A/B/C, beginning with one synthetic client and the ordinary-failure chain
`T0 → Matrix → source/target gates → Candidate → Packet → Lease → Barrier →
Apply → Verification → T11`. Record the falsifying measurements listed above
and keep the full Matrix as the canonical fallback.

## Sources reused

- `docs/reports/engineering/2026-08-21_020500_v5_3_t0_t11_timing_breakdown_and_bottleneck.md`
- `docs/reports/engineering/2026-08-20_170000_v5_3_system_revalidation_strict_reconciliation.md`
- `docs/reports/engineering/2026-08-20_130000_v5_3_matrix_health_phase_c_d_e_decision.md`
- `docs/reports/engineering/2026-08-20_225000_v5_3_system_level_weighted_architecture_decision.md`
- `docs/reports/engineering/2026-08-20_223000_v5_3_matrix_probe_economy_polygon_revalidation.md`
- `docs/reports/engineering/2026-08-20_224000_v5_3_matrix_comparison_controlled_caller_receipt.md`

## Verification

- Documentation and evidence synthesis only; no code, timer, Matrix, Runtime,
  route or client state changed.
- `git diff --check` passed; `python3 tools/v7-truth-check --continue-omp
  --json` passed with no authority, Runtime, routing or user effect.
- Architecture selection, automatic FAST enablement and production deploy are
  not authorized by this report.
