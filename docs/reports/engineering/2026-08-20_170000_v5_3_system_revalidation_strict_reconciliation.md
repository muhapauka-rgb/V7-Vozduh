Mission: `V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1`
Run nonce: `v53_complete_health_test_stability_20260820`

# V5.3 strict system-revalidation reconciliation

Status: `ACTIVE_MISSION_REOPENED; NO_ARCHITECTURE_TERMINAL; NO_RUNTIME_EFFECT`

## Current truth

Fresh CPS Section 0 names this Mission as `MISSION_ADMITTED`, keeps the
automatic FAST consumer on `HOLD_PENDING_SYSTEM_LEVEL_REVALIDATION`, and names
`EXECUTE_V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS` as the exact active
action. The earlier Phase-E terminal is historical/provisional input only.

## Reconciliation of prior evidence

| Current Program requirement | Prior Atlas result | Classification | Exact residual |
| --- | --- | --- | --- |
| Every mechanism owner/producer/output/consumer/decision role | seven aggregate evidence-family rows | `PARTIAL` | mechanism-by-mechanism Atlas |
| Failure-class coverage | selected examples only | `MISSING` | complete class-to-owner matrix |
| Decision influence graph and four contracts | described prose only | `MISSING` | source, target, recovery, post-switch edges |
| Execution order and latency | configured values plus limited tests | `PARTIAL` | scenario timelines and controlled timings |
| Cadence/timeout/retry/persistence by role | several static values | `PARTIAL` | state/role model with measured or bounded rationale |
| Serial/parallel dependency model | lock-scope observation only | `PARTIAL` | full dependency DAG and pressure analysis |
| Stability/history placement | high-level owner grouping | `PARTIAL` | temporal signal inventory and fast/precomputed/deep placement |
| Mandatory commercial comparison | Google/Envoy/FRR patterns only | `MISSING` | field-by-field Envoy, HAProxy, Google, FRR, Cisco, Fortinet, MikroTik rows |
| Three concrete candidates and weighted selection | B+C re-asserted before complete comparison | `INVALIDATED` | evidence-derived candidates and critical-gate comparison |

Result: the prior `V7_HEALTH_TEST_STABILITY_TARGET_ARCHITECTURE_REVALIDATED_WITH_BOUNDED_MEASUREMENT_RESIDUAL` is not a consumable weighted architecture terminal. It is retained as partial evidence only.

## Reused valid evidence

- Matrix is the existing per-egress service/path owner; it has 14 declared
  service probes, an atomic writer lock and canonical failure-event output.
- Telegram sentinel is a fast producer bridge into the same Matrix owner, not
  a second event or failover authority.
- Quality compaction owns bounded EMA/ring projections; raw history is not a
  lawful synchronous planner input.
- Planner owns target/capacity/freshness gates and fails closed for unknown,
  stale or mismatched facts.
- Runtime snapshot proves only past deployed topology because its embedded host
  clock conflicts with the snapshot envelope; it cannot prove current timing.

## Independent CT-M0F test status

The controlled suite currently reports `112/114`. The two failures are in
`test_ct_m0f_active_service_failure_binding_requires_accounted_live_owner` and
`test_ct_m0f_standing_source_selection_reuses_controlled_pool_owner`. They
exercise CT-M0F fixture/contract inputs (missing current users registry and an
incomplete execution-source registry), not V5.3 health architecture. Class:
`AFFECTS_ONLY_UNRELATED_CT_M0F_FIXTURE` for analysis; it becomes
`AFFECTS_DEPLOYMENT_OF_CHANGED_SHARED_OWNER` only if a later V5.3 patch changes
that shared autoswitch owner. No test was skipped or weakened.

## Exact next executable action

Continue the admitted Atlas in this order: enumerate mechanism records and
failure classes; trace decision/time/dependency graphs; make safe controlled
measurements; complete primary-source field benchmark; then build candidates
and make one weighted decision. No comparator implementation or automatic FAST
consumer admission is currently legal.

## Atlas evidence pass 1 — exact existing mechanisms

| ID | Producer -> state -> consumer | Exact decision effect | Timing/order and disposition |
| --- | --- | --- | --- |
| `M01_MATRIX_HTTP_PROFILE` | Matrix `run_curl_check` -> service-matrix rows -> Planner service gates | persistent required service failure excludes target/source; 13 profile checks | up to 8 parallel workers; 3–30s configured timeout; `REUSE_FAST` for exact required subset, `REUSE_DEEP` for full set |
| `M02_MATRIX_TELEGRAM_MULTI_ENDPOINT` | Matrix 9-endpoint TCP checker -> Matrix row -> Planner Telegram gate | exact path Telegram failure blocks required target | endpoint probes parallel, 1–4s per endpoint; `REUSE_FAST` |
| `M03_TELEGRAM_SENTINEL` | Sentinel -> same Matrix row/event -> Matrix wake/Planner | rapid suspicion and canonical-event bridge, never a second failover owner | 4s configured timer plus grace/persistence; `REUSE_FAST` |
| `M04_PATH_IDENTITY` | Matrix path fingerprint -> reuse-or-verify consumer | proves egress path/profile equality, not user route | mismatch forces full verifier; component reads parallel; `REUSE_FAST` |
| `M05_FAILURE_EPISODE` | Matrix episode builder -> event ledger -> passive/L3 consumer | continuity, incident and recovery identity | atomic serial state write; `REUSE_PRECOMPUTED` |
| `M06_QUALITY_WINDOWS` | quality compactor -> bounded EMA/ring -> Planner quality gate | target stability/quality admission and ranking, not immediate rescue | 5m/1h/24h/7d projections; `REUSE_PRECOMPUTED` |
| `M07_CAPACITY_RESERVE` | Planner live state -> capacity decision -> target gate | excludes hard/full/reserve-ineligible target | no network probe; `REUSE_FAST` |
| `M08_ROUTE_KERNEL_VERIFY` | Planner route verifier -> governed apply verification | proves exact client route and post-switch recovery; Matrix cannot replace it | after candidate only; `REUSE_FAST` post-switch |
| `M09_FRESHNESS_UNKNOWN` | Planner freshness classifier -> candidate blocker | stale required evidence blocks; unknown required evidence blocks | fresh 900s, stale 3600s, expired 7200s; `REUSE_FAST` |
| `M10_PERSISTENCE_COOLDOWN` | Planner persistence/cooldown -> candidate gate | blocks flap and one-sample failover | 3 samples or 180s; 180s cooldown; `REUSE_FAST` |
| `M11_INCIDENT_SCOPE` | Matrix event -> L3/passive -> current route scope | proves current affected scope before action | bounded event ledger read; `REUSE_PRECOMPUTED` |
| `M12_RECOVERY_RECONCILIATION` | recovery receipts + route truth -> passive reconciliation | governs source re-admission only with exact newer receipts | deferred, raw history never fast-path; `REUSE_DEEP` |

All 14 Matrix services are classified: `google` is channel-health-required,
`telegram` egress-path-required, and the remaining 12 are channel-profile-
required. They are not collapsed into one generic HTTP signal.

## Failure-class coverage pass 1

| Class | First actual producer | Confirming set / effect | Gap |
| --- | --- | --- | --- |
| Process/interface/tunnel | runtime diagnosis plus Matrix `NOT_STARTED` | runtime/interface state + Matrix failure; target excluded | source-event timeline pending |
| Tunnel up/no Internet, DNS, required service | Matrix HTTP/TCP probes | persistence then source incident / target block | controlled timing pending |
| Partial censorship/degradation | service-class Matrix rows | transient degrades; persistent blocks | threshold comparison pending |
| Loss/latency/jitter/stability | quality windows | target gate/ranking only | must not start rescue alone |
| Capacity/unsuitable target | Planner capacity/reservation/policy/route gates | target exclusion | owner mapping complete |
| Stale/unknown/conflicting truth | freshness and path-generation checks | fail closed or full reverify | precedence graph pending |
| Post-switch no recovery | route/kernel verification and outcome/rollback | verification failure blocks/quarantines/rolls back | controlled timeline pending |

## Decision-influence graph — pass 1

```text
Matrix HTTP/TCP + Telegram sentinel
 -> service-matrix.json / canonical event
 -> freshness + persistence classifier
 -> SOURCE_CONFIRMATION / TARGET_EXCLUSION

quality compact + stability projection
 -> compact 1h/current facts
 -> Planner quality gate
 -> TARGET_EXCLUSION or RANKING_MODIFIER

capacity/reserve + policy/role + current route scope
 -> Planner candidate gates
 -> TARGET_EXCLUSION / APPLY_ELIGIBILITY

path fingerprint + exact user route/kernel verification
 -> full reverify or governed verifier
 -> POST_SWITCH_VERIFICATION / ROLLBACK_GATE

recovery receipts + current route truth
 -> passive reconciliation
 -> RECOVERY_GATE
```

`SOURCE_FAILURE_CONTRACT`: source Matrix evidence plus persistence and current
affected scope; quality/history cannot substitute for the confirmed failure.
Unknown or stale required service truth is fail-closed.

`TARGET_READINESS_CONTRACT`: fresh path/service evidence, enabled/eligible
role, policy/reservation, capacity/reserve, quality/stability and no safety
quarantine. A healthy Matrix row cannot substitute for capacity or exact role.

`RECOVERY_READMISSION_CONTRACT`: newer exact recovery receipts matched to the
same egress generation plus current route truth. A historical success or an
unrelated service recovery is forbidden substitution.

`POST_SWITCH_RECOVERY_CONTRACT`: exact user policy-table/kernel route plus
governed service verification/outcome. Matrix path evidence alone is forbidden
as a user-traffic success claim.

## Controlled evidence pass 1

Eight isolated tests passed in `1.655s`: exact service-subset validation,
probe-before-lock ordering, Matrix merge-lock scope and all five quality
compactor lifecycle-lock cases. Classification: `DETERMINISTIC_REPLAY_MEASURED`
for lock/ownership behavior, not a production latency value. The tests prove
that network probes are not serialized behind the Matrix writer and that the
quality writer respects the same lifecycle lock; they do not measure external
endpoint duration, production CPU/RSS, or live timer cadence.

## Primary-source commercial benchmark — field pass 1

| Platform/mechanism | Documented mechanism | Current V7 equivalent / disposition | Architecture consequence |
| --- | --- | --- | --- |
| Envoy active health + outlier detection | active checks and passive error/timeout/reset ejection can coexist; degraded differs from ejected | Matrix active probes + sentinel/passive event bridge; `ADAPT` the separation, not Envoy defaults | fast suspicion may accelerate confirmation but cannot become a second truth owner |
| HAProxy checks | normal, transition and down intervals; `fall`/`rise`; active and passive checks; health check duration visible | Matrix persistence and recovery receipts are equivalent in intent but lack role-state timing measurements; `ADAPT` measurement, no copied intervals | retain asymmetric failure/recovery and publish actual duration before numeric cadence change |
| Google Cloud health checks | protocol-aware probes, sequential success/failure thresholds, eligibility for new traffic | Matrix service classes + Planner target gates; `REUSE` the protocol/threshold/eligibility separation | service reachability does not prove client policy-table path |
| FRR/Cisco BFD | transport liveness detects loss by negotiated interval × multiplier | interface/transport signals are only a fast suspicion layer; `REJECT` direct BFD-default adoption | V7 needs service/target/route proof beyond tunnel liveness |
| Cisco IP SLA + object tracking | tracked reachability/route/interface state is consumed by PBR route choice | existing Planner consumes distinct Matrix, route, capacity and role outputs; `REUSE` producer-to-consumer topology | preserve one explicit consumer boundary; no report-driven route action |
| FortiGate Performance SLA | active/passive/prefer-passive measures latency, jitter, loss; multiple checks avoid a single-server conclusion; failed SLA removes route eligibility | quality compact + Matrix multi-service evidence; `ADAPT` failure-domain review and measured quality placement | quality may exclude/re-rank target; cannot alone force source rescue |
| MikroTik gateway check/recursive route/BFD | gateway result is a nexthop fact consumed by route selection; periodic ICMP/ARP and BFD options are distinct | V7 path/route facts remain separate from Matrix service facts; `REUSE` separation | do not promote gateway reachability into complete Internet/service health |

Primary URLs: Envoy health checking and outlier docs; HAProxy health-check docs;
Google Cloud Load Balancing health-check concepts; FRR BFD; Cisco BFD and IP
SLA object tracking; Fortinet Link Health Monitor; MikroTik IP Routing/BFD.

## Controlled measurement pass 2 — isolated non-production Matrix run

The existing Matrix owner was invoked against a fresh temporary state directory
and a deliberately nonexistent interface. No V7 Runtime state, route, client,
or production Matrix file was read or written. Results are therefore
`CONTROLLED_MEASURED`, not production availability evidence.

| Variant | Exact services | Parallel probe/wall span | durable write span | process CPU | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Full | 14 | `50.699 ms` | `8.852 ms` | `46.886 ms` user+system | all probes correctly failed through isolated interface |
| Exact subset | 3 | `12.729 ms` | `7.173 ms` | `16.131 ms` user+system | same safe failure class |

The controlled probe-phase reduction was `74.9%`; selected probe count fell
`78.6%`. The durable atomic merge is nearly constant, so it cannot be claimed
as the source of the improvement. This result proves the existing selector and
parallel Matrix owner can reduce bounded work; it does **not** prove live
Internet latency, service health, production CPU/RSS, or a lawful automatic
consumer. Re-entry for production timing is a fresh coherent existing Runtime
observation, not a new measurement owner.
