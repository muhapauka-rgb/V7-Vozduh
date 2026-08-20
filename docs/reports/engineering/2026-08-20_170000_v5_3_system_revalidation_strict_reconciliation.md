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

## Execution-order and latency graph — pass 1

| Scenario | Ordered critical path | Blocking law / evidence class |
| --- | --- | --- |
| Hard source service failure | Matrix/sentinel observation -> persistence -> atomic Matrix state/event -> bounded current source-scope projection -> existing direct handoff/Planner -> fresh candidate gates -> governed verifier -> route/traffic verification | probe fanout is parallel; Matrix merge is serial; raw history and OMP/report tails are deferred. Cadence, external endpoint wait and persistence remain `STATIC_ONLY` for production latency. |
| Tunnel alive, Internet dead | Matrix path-bound HTTP/TCP probe -> same persistence/event path -> exact target gates | interface presence is insufficient; service path confirmation is mandatory. |
| Partial service failure | exact profile-service row -> transient degradation + bounded target-only recheck, or persistent failure -> target/source block | one non-required/limited endpoint cannot substitute for required service; no blanket tunnel failover. |
| Quality degradation | compactor -> current compact 1h fact -> Planner quality/stability gate/ranking | background precompute, never synchronous raw-history scan or autonomous source-rescue trigger. |
| Passive error burst | Sentinel/passive Matrix publication -> canonical Matrix event -> existing Matrix consumer | duplicate events coalesce through episode identity; consumer tails are deferred from fresh action path. |
| Target preparation | current Matrix/path identity + role/policy + capacity/reserve + quality + safety -> Planner candidate | gates are serial by causality after read snapshot; Matrix evidence does not replace role/capacity. |
| Recovery/readmission | newer same-generation Matrix recovery receipts + current route truth -> passive reconciliation | serial exact matching; unrelated service recovery and old generation are rejected. |
| Post-switch verification | exact policy-table/kernel route -> service/traffic verifier -> outcome; failure -> existing rollback/quarantine | post-switch only; cannot be moved before source/target decision and cannot be replaced by Matrix path evidence. |

Detected placements: `SERIAL_STATE_COMMIT` is necessary for the canonical Matrix
write; `PARALLEL_PROBING` already applies inside the Matrix; quality/history and
OMP tails are correctly `DEFERRED_BACKGROUND`; user-route verification is a
necessary `SERIAL_CONFIRMATION`. No evidence currently supports a claim that
the full deep Matrix runs before a simple confirmed source decision on the
runtime hot path; this must be retained as a caller-level measurement item.

## Cadence, timeout, retry and persistence — complete role table

| Role | Existing owner and configured bounds | What it may establish | What it must not establish |
| --- | --- | --- | --- |
| Broad baseline | `v7-service-matrix-refresh.timer`: 15 min plus up to 60 s jitter; Matrix probe timeout default 8 s, bounded to 3–30 s | periodic service/path observation for every enabled egress | a recent full sweep is not an exact user-route proof |
| Fast Telegram suspicion | `v7-telegram-sentinel.timer`: 4 s, 1 s accuracy; per endpoint timeout 2 s by default | a rapid Telegram-path observation written through the Matrix | an independent incident, candidate, or route action |
| Matrix failure continuity | Matrix / Planner: 3 samples **or** 180 s | a persistent service failure eligible for an event/decision consumer | one transient timeout must not remove a route |
| Planner freshness | 900 s fresh, 3,600 s stale, 7,200 s expired | whether required evidence can be used at all | an old successful row cannot make a target eligible |
| Planner retry/cooldown | one retry per incident; 180 s cooldown | bounded recovery from a failed governed attempt | repeated speculative switching |
| Quality history | compactor timer 5 min with 30 s accuracy; windows 5 min/1 h/24 h/7 d | bounded current quality/stability fact for target gate/ranking | raw history cannot run synchronously in a failure reaction |
| Health summaries | existing health loop every 30 s | diagnostic and state projections | it is not a substitute for Matrix path evidence |
| Writer contention | Matrix/sentinel/quality lifecycle lock: 90 s default wait; actual mutation atomic | one coherent Matrix generation | probes must not hold the writer lock while waiting on the network |

The values are existing safety bounds, not copied commercial defaults. The
only directly measured timing remains the isolated Matrix run above. Production
duration distributions, queue/wait time and probe count by real timer run are
not present in the current read-only Runtime evidence.

## Dependency and pressure model — complete pass

```text
parallel: [selected HTTP services up to 8 workers]
parallel: [Telegram endpoints]
parallel: [path-fingerprint component reads]
      \                         |                         /
       \------------------------v------------------------/
                 serial: canonical Matrix lock + atomic write
                                  |
                 serial: failure episode / current scope
                                  |
       parallel reads: [freshness, role, capacity, quality, safety]
                                  |
              serial: candidate decision / governed authority gate
                                  |
              serial: exact user route + traffic verification
                                  |
         deferred: history compaction, receipts, OMP/report processing
```

Pressure is therefore bounded in three different places: Matrix fan-out is
at most eight service workers (and Telegram endpoints use their own bounded
fan-out); one short writer section protects the sole Matrix state; and the
governed per-user path is serial only after the candidate exists. A full
history scan, a second state write, or a second planner on the upper path
would violate this graph. The measured subset result shows that the parallel
probe section is the only demonstrated reducible portion; it does not justify
removing the atomic merge or later safety checks.

## Stability and history placement — complete inventory

| Signal family | Canonical placement | Fast use | Deep/passive use | Prohibited shortcut |
| --- | --- | --- | --- | --- |
| Current Matrix service row and path fingerprint | `service-matrix.json`, Matrix owner | exact required-service and same-generation gate | full profile re-verification | use a row from another path/generation |
| Failure episode and source scope | Matrix event / bounded current scope | persistence and current source confirmation | incident/recovery audit | reconstructing unbounded event history in a decision |
| Latency, loss, jitter and stability | compacted quality EMA/rings | fresh bounded target eligibility/ranking | 5m/1h/24h/7d trend interpretation | turn quality alone into automatic source rescue |
| Capacity, reserve, role and policy | current Planner state | candidate exclusion/admission | audit explanation | infer any of them from a successful probe |
| User route/kernel result | governed verifier output | post-switch only | receipt/rollback analysis | infer user success from egress Matrix health |
| Recovery receipts | exact generation-bound receipt chain | none before exact match | passive re-admission | admit from historical success or unrelated recovery |

## Commercial comparison — completed field mapping

| Platform | Active/passive evidence | Threshold/state model | History/observability | Relevant V7 adoption decision |
| --- | --- | --- | --- | --- |
| Envoy | HTTP, gRPC and L3/L4 active checks; passive outlier detection | configurable failure/success thresholds; degraded is distinct from unhealthy | health event logging; cached pass-through protects a service from probe load | `ADAPT`: preserve active Matrix plus passive/sentinel distinction and separate degraded from excluded; no new owner |
| HAProxy | active TCP/HTTP and passive connection/HTTP errors | `inter`, `fastinter`, `downinter`, `fall`, `rise` | checks continue while down and state returns only after successes | `ADAPT`: retain V7's asymmetric persistence/recovery; measure before changing cadence numbers |
| Google Cloud Load Balancing | protocol-specific health probes | consecutive success/failure thresholds gate eligibility for new traffic | distributed probes and health state are separate from application routing policy | `REUSE`: protocol evidence, threshold and traffic-eligibility are separate; Matrix cannot prove a user route |
| FRRouting / Cisco BFD | transport-session liveness | negotiated interval × detection multiplier | rapid peer/session state, not application service state | `REJECT` as a direct decision default: it can be only a suspicion input in V7 |
| Cisco IP SLA / object tracking | active reachability probes consumed by tracked routing policy | tracked object changes route eligibility | operation statistics and route/object state remain distinct | `REUSE`: explicit producer-to-consumer contract; do not let a report become a route command |
| FortiGate Performance SLA | active, passive and prefer-passive link measurements | latency, jitter, loss and multiple health targets drive eligibility | SLA history/quality is distinct from link selection | `ADAPT`: multi-failure-domain quality review; V7 quality stays a target gate/ranker |
| MikroTik recursive gateway checks / BFD | gateway reachability, ARP/ICMP and BFD are distinct mechanisms | a route's next-hop fact is separate from wider service reachability | routing state, check mechanism and BFD role remain explicit | `REUSE`: keep next-hop, path service and user route as three separate facts |

Primary sources consulted: [Envoy health checking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking),
[HAProxy health checks](https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/),
[Google Cloud health-check concepts](https://cloud.google.com/load-balancing/docs/health-check-concepts),
[FRR BFD](https://docs.frrouting.org/en/stable-7.5/bfd.html),
[Cisco BFD](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bfd/configuration/15-2s/iro-bfd-15-2s-book/iro-bfd-cfg.html),
[Cisco IP SLA object tracking](https://www.cisco.com/c/en/us/support/docs/ip/service-level-agreements-sla/15114-ipslatrack.html),
[FortiGate Link Health Monitor](https://docs.fortinet.com/document/fortigate/latest/administration-guide/580649/link-health-monitor),
and [MikroTik IP Routing](https://help.mikrotik.com/docs/spaces/ROS/pages/59965508/First+Time+Configuration).

## Candidate architecture and weighted result — provisional, not consumable

Critical gates for every candidate are: one Matrix truth owner; no action on
unknown/stale/conflicting evidence; full Matrix retained; Planner still owns
target eligibility; route verification remains post-switch; and no client or
route is changed by a probe.

| Candidate | Safety 30 | Decision completeness 20 | Time potential 15 | Load 10 | Stability/history 10 | Observability 10 | Change scope 5 | Total /100 | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A. Full 14-service Matrix for every relevant reaction | 30 | 20 | 2 | 2 | 10 | 8 | 5 | 77 | safe baseline, but does not use the proven bounded selector |
| B. Exact required-service subset, with full Matrix on any uncertainty or disagreement | 30 | 19 | 14 | 9 | 10 | 9 | 4 | 95 | strongest direct architecture candidate |
| C. Telegram suspicion -> B only after Matrix publication, with full Matrix on ambiguity | 30 | 19 | 15 | 10 | 10 | 9 | 4 | 97 | preferred staged composition; sentinel is a producer bridge, never a second authority |

The scores are an auditable architecture comparison, not production performance
claims. Candidate C is preferred because it adds an earlier bounded signal
without changing the canonical decision path. It remains conditional on B's
strict fallback: a missing, stale, mismatched, or contradictory required row
must run/retain the full Matrix and must not allow a target or a switch.

## Fresh Runtime and deploy observation

At `2026-08-20`, read-only Runtime verification first found the Matrix timer
active but identified `runtime_local_commit_mismatch`: Runtime was at
`edd97966`, while the admitted Mission binding was at `1d89b531`. The existing
`v7-safe-deploy` preflight independently verified the published `Updatesystem`
head and permitted deployment. The approved safe deployment completed, and a
fresh read-only check then proved `RUNTIME_ALIGNED`, matching local and Runtime
commit `1d89b531`; authoritative binary hashes match and
`v7-service-matrix-refresh.timer` is active/waiting. The historical automatic
switch scheduler remains intentionally inactive in approved manual mode.

This proves the real Matrix timer/caller and the deployed Mission-recognition
logic. It proves neither a live short-versus-full duration distribution nor a
live automatic FAST consumer: CPS still holds that consumer, as required.

An additional bounded read of existing production state found seven Matrix
egress rows with exactly fourteen service rows each; the state timestamp was
`2026-08-20T14:21:41.265165+00:00`. This proves that the deployed Matrix
catalogue is present at Runtime. The most recent compact refresh summary was
instead a capture-only certification-scope deferral (`elapsed_sec=0.001`,
`total=0`, `candidate_or_execution_forbidden=true`), so it is explicitly **not**
misrepresented as a fourteen-service duration sample. No identifier, route,
client, raw service result or secret was read.

The focused V5.3 owner/lock/quality tests pass. The broader selected run is
`112/114`: the same two pre-existing CT-M0F fixture failures described above
remain. They were neither skipped nor altered and do not change the Matrix
catalogue, lock, persistence or deployed-caller observations.

## Polygon controlled evidence — no passive wait

Following the explicit request not to wait for a natural incident, the existing
read-only Polygon entrypoint (`tools/v7-truth-check --omp-scenario-execution`)
was invoked through its real Planner, invariant oracle and OMP result consumer.
It completed all four relevant controlled cases:

| Polygon case | Result | What was proved | Forbidden effects |
| --- | --- | --- | --- |
| `SINGLE_CHANNEL_FAILURE` | `PASS` | a hard channel failure retains route-reachability, blast-radius and legal-terminal invariants | all false; preview only |
| `STALE_TELEMETRY_MUTATION_DENIAL` | `PASS`, legal `STOP_SAFE` | stale/unknown data is denied rather than turned into a move | all false; preview only |
| `CORRELATED_CHANNEL_GROUP_FAILURE` | `PASS` | correlated failures retain containment and capacity limits | all false; preview only |
| `CAPACITY_BOUNDARY` | `PASS` | no eligible user is left without a safe route and no authority is expanded | all false; preview only |

Every case was consumed by the existing `OMP_PROGRAM_EXECUTION_RECONCILIATION`
consumer. The direct Scenario Results identify the real Planner as their
decision owner and declare `ENGINEERING_SCENARIO_EVIDENCE`; they explicitly
forbid production mutation, routing mutation, user movement, packet execution,
rollback apply, restore-barrier writes, Authority expansion and production
maturity credit. Thus Polygon replaces the avoidable wait for a safety-class
test, not the requirement for an honest Matrix timing measurement.

The Polygon corpus/harness suite was also exercised. Its principal isolation,
invariant, replay and forbidden-effect tests pass. Two existing selective-
invalidation expectation failures remain: the live dependency compiler now
also includes `PHASE6V4_PARTIAL_APPLY_CIRCUIT_BREAKER` beside the older expected
`LEASE_CONFLICT`, and its current continuation points to `PARTIAL_PARTITION`
where the old fixture expects `NONE`. These are a stale Polygon test-contract
expectation versus current dependency/continuation behaviour; no test was
weakened and no Matrix, route or client effect follows from them. They block an
unqualified claim of full Polygon-suite green, but not the four successful
direct controlled Scenario Results above.

## Exact current blocker and re-entry

`BLOCKER_V53_PRODUCTION_COMPARATIVE_MATRIX_TELEMETRY_ABSENT` is critical to the
final system-level weighted terminal. The existing production Matrix output
does not retain a comparable short/full timing timeline in its compact durable
summary, and the approved Runtime read-only view exposes timer status,
provenance and redacted catalogue counts rather than child probe timings.
Moreover, CPS lawfully holds the automatic subset consumer, so manufacturing a
production subset run would write Matrix state/events merely to obtain a
benchmark. Consequently, the required production comparison of elapsed time,
executed check count, error/load and short/full decision agreement cannot be
stated truthfully. The isolated run is deliberately insufficient for that
claim. Polygon closes the avoidable controlled safety-evidence wait; it cannot
and must not fabricate a production Matrix duration or a service response.

Existing owner for re-entry: `tools/v7-service-matrix-refresh-all` and its
existing Matrix writer, observed through the existing `tools/v7-truth-check`
Runtime-verification boundary. Exact safe re-entry condition: obtain one or
more bounded, read-only, redacted results from real already-scheduled Matrix
runs for both the existing full path and the opt-in exact subset, without
changing users, routes, policy, timers or the FAST-consumer hold; then compare
the seven required measures and either consume Candidate C or retain A.

Status remains `ACTIVE_MISSION_REOPENED; NO_ARCHITECTURE_TERMINAL;
NO_AUTOMATIC_FAST_CONSUMER`. No Program, CPS, routing or client state was
changed by this Mission work.

## Controlled Matrix comparison through the existing Polygon boundary

The existing Matrix CLI was exercised in a disposable local state directory
against an ephemeral controlled HTTP/TCP response surface. It used the real
Matrix selection, parallel-probe, persistence and atomic-writer code. The
test has no production state directory, production endpoint, route, user,
policy or Runtime dependency. macOS does not expose the Linux-only TCP
interface-binding socket option; the isolated TCP socket binding was therefore
explicitly bypassed **only in the test**, while HTTP still used the local
loopback interface. This is controlled functional and cost evidence, not an
egress-path certification.

| Variant | Result | Selected / successful checks | probe span | write span | CPU | Decision equivalence |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Full Matrix | `OK` | 14 / 14 | `41.284 ms` | `6.946 ms` | `39.261 ms` | healthy / no failure |
| Exact `telegram,google,google_auth` | `OK` | 3 / 3 | `9.793 ms` | `6.549 ms` | `11.750 ms` | same healthy / no failure |

In this healthy controlled case, the probe critical path was `76.3%` shorter,
selected work was `78.6%` lower and measured process CPU was `70.1%` lower.
The atomic write remains close to constant. The test is retained as
`tests/unit/test_v5_3_matrix_controlled_comparison.py`; it asserts the exact
14-versus-3 count, all-healthy outputs and use of the existing Matrix CLI
entrypoint. A matching isolated all-failure case was already measured above.
Together they prove selection and outcome equivalence only for controlled
all-healthy and all-failed conditions; mixed, stale and conflicting truth is
covered by Polygon safety scenarios and still requires full fallback.

## Complete internal mechanism cards

The cards below are the internal Health/Test/Stability inventory. `unknown`
means deliberately unmeasured rather than assumed. All data paths are existing
owners; no card creates a new state surface.

| ID / role | Owner; producer -> stored state -> consumer | Trigger, cadence and freshness | What it proves / does not prove | Effect, placement and cost/risk |
| --- | --- | --- | --- | --- |
| `HC-01` source/target | Matrix HTTP checker: `run_curl_check` -> `service-matrix.json` -> Planner service gate | Matrix timer 15 min + up to 60 s jitter; 3–30 s probe timeout, default 8 s; fresh/stale/expired at 900/3600/7200 s | path-bound HTTP reachability for one service; does **not** prove a client route, capacity or every service class | persistent required failure excludes a source/target; up to 8 probes parallel, then one serial write; measured Matrix CPU/wall above; false negative if service set is incomplete |
| `HC-02` source/target | Matrix Telegram TCP checker -> Telegram Matrix row -> Planner Telegram gate | Matrix cadence; endpoint timeout 1–4 s; all required endpoint samples needed | Telegram transport reachability through the path; does **not** prove generic web reachability or user route | required Telegram failure blocks relevant target/source; endpoint fan-out parallel; duplicate signal may overlap sentinel |
| `HC-03` source/target | Matrix path fingerprint -> Matrix row -> reuse/full verifier | each Matrix observation; bounded component commands up to 5 s | path and egress identity generation equality; does **not** prove an individual policy-table route | mismatch forces full re-verification; component reads parallel; cost is bounded command fan-out, CPU/RAM not separately measured |
| `HC-04` source | Telegram sentinel -> same Matrix row/event -> existing Matrix consumer | 4 s timer, 1 s accuracy; 2 s endpoint timeout; persistence threshold handed to Matrix | fast Telegram suspicion, then a canonical Matrix observation; does **not** own a separate incident or a switch | may accelerate confirmation only; probes parallel, Matrix merge serial; false positive is contained by persistence/fallback |
| `HC-05` source/recovery | Matrix episode builder -> Matrix row plus event JSONL -> passive consumer/Planner | every Matrix/sentinel write; 3 samples or 180 s; recovery requires newer matching observation | continuity, persistence, source incident and recovery identity; does **not** prove a target is ready | creates canonical failure/recovery event only after threshold; serial atomic write; duplicate suppression prevents repeated incident starts |
| `HC-06` source/engineering | `v7-service-matrix-refresh-all` -> compact refresh summary/event -> passive and governed consumers | active system timer; full normally, exact subset only when an existing caller requests it | existing caller has completed a Matrix lifecycle; does **not** grant a candidate or authority | selects existing probe rows and preserves full fallback; orchestrator cost includes children and consumers, separately unmeasured |
| `HC-07` target | quality compactor -> `egress-quality-summary.json` and bounded ring -> Planner quality gate | 5 min timer, 30 s accuracy; max 2,000 ring items; quality freshness policy 900 s | bounded latency/loss/jitter/stability projection; does **not** prove an immediate source failure | excludes or ranks target; writer shares lifecycle lock and is deferred from hot action path; CPU/RAM unknown |
| `HC-08` target | Planner load/capacity reader -> current load summary -> candidate gates | request-time read; policy reserve 15%, hard/soft bounds configured | target has capacity/reserve under current policy; does **not** prove service reachability | target exclusion only; no network probe; stale/incorrect load can be fail-closed rather than inferred from Matrix |
| `HC-09` target | Planner role, organization and reservation gates -> candidate -> governed executor | request-time, exact current policy/state | role, policy, reservation and safety eligibility; does **not** prove Matrix health | target exclusion/admission; serial after snapshot; no independent state writer |
| `HC-10` all decision roles | Planner service freshness/classification -> candidate gate | 900/3600/7200 s evidence bands; revalidation budget 5 s | whether a Matrix fact is usable; does **not** turn stale success into healthy state | blocks unknown/stale/conflicting evidence and requests bounded recheck; cheap read, no network unless existing revalidation applies |
| `HC-11` source | current failed-source scope -> bounded Matrix/event projection -> direct handoff/Planner | event-driven read after Matrix publication | present affected source scope; does **not** select a target | prevents no-user/zero-scope reaction; bounded event tail read; raw user history prohibited |
| `HC-12` post-switch | user route/kernel verifier -> governed outcome/rollback record -> recovery consumer | only after candidate and governed apply; verification timeout 5 s in emergency policy | exact client policy-table/kernel route and outcome; does **not** prove a whole egress healthy | verifies, rolls back or quarantines; necessarily serial; cost is action-specific and not a Matrix probe cost |
| `HC-13` recovery | exact recovery receipts + current route truth -> recovery/re-admission owner | after newer same-generation healthy Matrix result | an incident may be reconciled/re-admitted; does **not** accept historical success | passive/deep only; exact receipt matching serial; false positive risk is contained by generation matching |
| `HC-14` engineering | Polygon scenario corpus -> Planner/invariant oracle -> OMP scenario consumer | explicit bounded request; deterministic replay | safety rules under controlled failure/capacity/stale-data cases; does **not** prove production latency or grant production credit | engineering-only, all mutation effects forbidden; bounded local CPU/RAM are not production measurements |
| `HC-15` diagnostic | 30 s health/state summary loop -> diagnostic projections -> operators/other existing readers | 30 s loop | aggregate process/interface/history diagnostic context; does **not** substitute for Matrix path fact | diagnostic/background only; never a direct failover authority; detailed cost unknown |

Cross-card storage and duplication rules: `service-matrix.json` is the only
service/path fact; Matrix event JSONL is the only failure-episode history;
quality summary/ring is the bounded stability projection; Planner candidate,
Packet and outcome owners are separate. Telegram sentinel must write through
`HC-02/HC-05`, never alongside them. Fast reads are `HC-01/02/03/08/09/10/11`;
precomputed reads are `HC-05/07`; deep/passive work is `HC-13`; Polygon and
the health loop are engineering/diagnostic only.

## Complete failure taxonomy and action law

| Failure class | First signal -> confirmation | Decider and allowed result | Forbidden shortcut | Recovery condition |
| --- | --- | --- | --- | --- |
| Process/interface/tunnel absent | runtime/interface state or Matrix `NOT_STARTED` -> fresh Matrix/path observation | existing Matrix/Planner may exclude affected egress | interface presence alone is not Internet health | fresh same-generation path/service observation |
| Tunnel alive, no Internet | Matrix HTTP/TCP service failure -> persistence | Matrix failure episode, then source action path if scope exists | do not treat tunnel state as recovery | required service/path row recovers with current identity |
| DNS failure | required HTTP probe failure/diagnostic detail -> relevant service/persistence confirmation | Matrix/Planner source or target block | do not infer from an unrelated TCP success | fresh required-service success |
| Single service failure | one service row -> service/role relevance and persistence | degradation penalty or block according to required role | no blanket egress failure from non-required service | same service, same generation, newer success |
| Partial censorship/access | service-class rows -> required profile confirmation | route-class-specific target/source effect | do not replace profile evidence with generic `healthy=true` | profile-required rows return healthy |
| Telegram transport loss | sentinel or Matrix TCP -> Matrix persistence | canonical Matrix event and relevant target/source block | sentinel cannot switch clients directly | newer Telegram Matrix recovery receipt |
| Latency/loss/jitter degradation | compactor bounded projection -> quality threshold/freshness | ranking/exclusion of target | quality cannot trigger source rescue alone | fresh compact quality passes threshold |
| Capacity/saturation | load/reserve fact -> Planner load gate | target exclusion | successful Matrix row cannot override capacity | current reserve/load passes policy |
| Role/policy/reservation mismatch | Planner current state -> role/org/reservation gate | target exclusion | Matrix cannot make a forbidden role eligible | current policy and reservation match |
| Flapping | episode continuity/persistence/cooldown -> Planner gate | suppress repeated actions | one sample may not remove route | sustained recovery plus cooldown/receipt law |
| Stale data | freshness classifier -> bounded revalidation or block | fail closed / full recheck | old success cannot admit target | current evidence within 900 s |
| Unknown/conflicting data | missing or mismatched generation/fingerprint -> block | fail closed / full reverify | selecting a "best guess" target | coherent current generation across required facts |
| Recent recovery | recovery receipt -> current route truth | passive readmission only | historical recovery cannot reopen channel | newer exact-generation receipt and route truth |
| Post-switch failure | user route/kernel verifier -> governed outcome/rollback | rollback, quarantine or stop-safe | Matrix success cannot claim client recovered | exact client route and traffic verification passes |

## Cadence and bottleneck classification

| Mechanism | Current cadence reason | Evidence class | Bottleneck finding / safe optimization law |
| --- | --- | --- | --- |
| Full Matrix | 15 min + jitter | historical safety baseline; live timer proven, real run timing absent | broad probe span is reducible only when an existing exact selector is lawful; retain full fallback |
| Telegram sentinel | 4 s | explicit fast-suspicion safety requirement | rapid signal already separate from full Matrix; never add a second decision owner |
| Matrix persistence | 3 samples or 180 s | anti-flap safety requirement | not safely removable; optimise observation before threshold, not the threshold itself |
| Matrix writer | atomic serial merge | consistency requirement | write span is near constant in controlled runs; do not parallelize state mutation |
| Quality compactor | 5 min | bounded history/precompute requirement | keep out of immediate action path; do not scan raw history |
| Health loop | 30 s | diagnostic historical cadence | no proof it belongs in a failover hot path; retain diagnostic-only classification |
| Planner freshness | request-time read, 900/3600/7200 s | safety requirement | cheap gate; stale data requires block/recheck, not caching extension |
| Route verification | after governed candidate/apply | safety requirement | serial by causality; cannot be replaced by Matrix and cannot move before target decision |

Measured bottlenecks are now: Matrix network-probe fan-out is the only
demonstrated reducible segment; durable Matrix merge is small/constant in both
all-failure and all-healthy isolated runs; fresh evidence/capacity/policy gates
are bounded reads; raw history and OMP tails are already deferred. Production
CPU/RAM and real endpoint latency remain unknown, deliberately not estimated.

## Internal gap register

| Gap | Current behaviour and impact | Evidence / risk | Candidate solution, not yet a decision |
| --- | --- | --- | --- |
| G1: per-run production timing absent | compact Runtime summary omits child probe timings and counts | prevents a production speed claim | expose a bounded redacted existing-owner timing projection, without a new store |
| G2: mixed service outcomes not yet Matrix-compared in controlled Polygon | healthy and all-failed cases agree; partial role-specific equivalence is not yet exercised | a subset could omit a decisive required class if selection law is wrong | controlled Matrix cases for required-service failure, methodology-limited HTTP and stale generation |
| G3: cadence rationale partly historical | full Matrix 15 min is configured, but no measured production distribution explains its value | changing cadence blindly risks detection delay or load | measure through existing Matrix output before any numeric change |
| G4: non-Matrix CPU/RAM unknown | quality, Planner and verifier have no comparable live resource sample | cannot rank their optimisation value honestly | bounded read-only observation through their existing outputs |
| G5: Polygon stale expectation drift | two selective-invalidation fixtures expect superseded continuation/dependency sets | prevents declaring the entire Polygon test collection green | reconcile test contracts separately; no Runtime/Matrix effect |

The smallest remaining internal Atlas action is `G2`: add controlled Matrix
cases for partial required-service failure, HTTP methodology limit and stale
generation, prove that short/full selection either agrees or lawfully falls
back to full Matrix, then update this report and recompute whether the internal
Atlas is complete enough for the external-comparison phase.

## Controlled Matrix decision-equivalence completion

`G2` is now closed through the existing Matrix CLI test surface and existing
Polygon stale-telemetry scenario. The controlled Matrix cases are intentionally
one-observation cases: they prove classification and preservation of the
correct decisive row, while `HC-05` remains solely responsible for persistence.

| Controlled case | Full Matrix | Exact subset | Correct common decision |
| --- | --- | --- | --- |
| all required services healthy | `OK`, 14/14 | `OK`, 3/3 | healthy observation; no failure |
| `google` required service returns 503 once | `WARN`, retained `google=FAIL` | `WARN`, retained `google=FAIL` | no immediate action; await 3 samples or 180 s persistence |
| `google_auth` returns 403 methodology limit | `HTTP_LIMITED`, `ok=true` | `HTTP_LIMITED`, `ok=true` | reachable-but-limited observation; do not manufacture a failure episode |
| stale/unknown telemetry | existing Polygon `STALE_TELEMETRY_MUTATION_DENIAL=PASS` | no selection allowed | `STOP_SAFE`; full re-verification only through existing owner |

The new focused suite (`5/5 PASS`) verifies all three Matrix cases plus the
existing subset validation and HTTP-methodology rule. It confirms that a short
selection does not weaken one-sample persistence, turn an HTTP limitation into
a failure, or bypass stale-data denial. It is still deliberately unable to
claim real remote endpoint latency, production interface binding, production
CPU/RAM or automatic FAST consumption.

Internal Atlas readiness is therefore `READY_FOR_MATURE_COMMERCIAL_BENCHMARK`
for the design/comparison phase: all discovered decision-relevant mechanism
families, owners, consumers, failure classes, source/target/recovery/post-
switch boundaries, timing/cadence/parallelism placement and controlled Matrix
equivalence cases are now recorded. `G1`, `G3`, `G4` and `G5` remain measured
or test-contract residuals for later implementation/deploy evidence; none
requires waiting for a natural event and none permits FAST enablement.

Next frontier: perform the mature-platform comparison against this fixed
internal baseline, then return to a single weighted architecture decision. No
runtime change, automatic FAST consumer or client movement is admitted by this
transition.

## Mature-platform benchmark — verification against the complete Atlas

This pass is a design comparison, not a transfer of vendor defaults.  It used
only the vendors' primary technical documentation and asks one question of
each mechanism: which existing V7 owner should retain the equivalent fact and
where must V7 reject a superficially similar shortcut?

| Pattern verified from mature platforms | Existing V7 equivalent | Decision for V7 |
| --- | --- | --- |
| Envoy combines active HTTP/gRPC/L3-L4 checks with passive outlier evidence, configurable success/failure thresholds, an identity check and a distinct degraded state. It also documents caching when many probes could burden a service. | `HC-01`/`HC-02` active Matrix rows, `HC-04` passive Telegram suspicion, `HC-03` path identity and `HC-05` persistence. | `ADAPT`: keep active and passive evidence separate until Matrix makes one canonical row/event; keep identity and a degraded/methodology-limited result distinct from a failure episode. No new fast owner or cache is justified. |
| HAProxy keeps probing after a server is removed and restores it only after the success threshold; it separates normal, transition and down intervals and supports checks across multiple endpoints. | `HC-05` persistence/recovery plus the existing full Matrix comparator. | `REUSE`: asymmetric failure/recovery is already present. The controlled `503` test proves one sample remains a warning. Do not copy a numeric interval before V7 measures its own live distribution. |
| Google Cloud computes backend state from separately configurable consecutive probe results, makes health state govern new-request eligibility, and supports protocol-specific probes. | Matrix service classes plus `HC-10` freshness and `HC-08/09` target admission. | `REUSE`: probe result, eligibility and traffic action must remain separate. A healthy Matrix row cannot itself prove a client route or authorize movement. |
| FRR BFD and RouterOS BFD/check-gateway deliberately model peer/next-hop liveness; their detection time is negotiated interval times multiplier. RouterOS keeps next-hop state separate from the route and recommends multiple monitored hosts to reduce a single-host conclusion. | interface/path signal and `HC-03` identity, separate from service and user-route facts. | `REJECT` as a complete-health decision: liveness can be a fast suspicion only. `ADAPT` the explicit failure-domain rule: no one gateway/service result may stand in for a profile or user route. |
| Cisco IP SLA/Object Tracking consumes a tracked measurement in routing policy, rather than treating a raw probe as a route mutation. | Matrix -> current source scope -> existing Planner -> governed verifier. | `REUSE`: preserve the explicit producer-to-consumer boundary. A report, probe or sentinel cannot become a direct route command. |
| FortiGate SD-WAN separates active, passive and prefer-passive measurement; records latency, jitter and loss; uses multiple check servers; applies failure/recovery thresholds; then removes only a failed member from eligibility. | `HC-07` quality/stability, `HC-01/02` service facts, and `HC-08/09` candidate gates. | `ADAPT`: V7's quality history stays a target filter/ranker and V7 retains multi-service/failure-domain confirmation. It must not turn quality alone into source rescue. |

Primary sources: [Envoy health checking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking),
[HAProxy health checks](https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/),
[Google Cloud health-check concepts](https://cloud.google.com/load-balancing/docs/health-check-concepts),
[FRR BFD](https://docs.frrouting.org/en/stable-7.5/bfd.html),
[Cisco IP SLA object tracking](https://www.cisco.com/c/en/us/support/docs/ip/service-level-agreements-sla/15114-ipslatrack.html),
[FortiGate Link Health Monitor](https://docs.fortinet.com/document/fortigate/latest/administration-guide/580649/link-health-monitor),
[MikroTik IP Routing](https://help.mikrotik.com/docs/spaces/ROS/pages/328084/IP%2BRouting) and
[MikroTik BFD](https://help.mikrotik.com/docs/spaces/ROS/pages/331612210/routing%2Bbfd).

The comparison closes no numerical V7 cadence or threshold: those remain V7
evidence questions, not imported vendor settings.  It confirms the internal
Atlas architecture rather than adding a missing mechanism.

## Weighted system decision — ready for existing OMP consumption

The full-Matrix baseline is still the safe fallback, but it is not the best
normal reaction once an existing caller has an exact affected source, exact
candidate egresses and the known minimum profile-service set.  The controlled
comparison shows the only measured saving is the probe fan-out.  All other
decision gates retain their existing order and owners.

| Alternative | Safety and meaning | Measured work | Operational decision |
| --- | --- | --- | --- |
| A — full Matrix for every reaction | safe; broad diagnostic coverage; no selector use | 14 services; `41.284 ms` controlled healthy probe span | retain as baseline, comparison and automatic fallback |
| B — exact source/target plus profile subset, then full Matrix on uncertainty or mismatch | preserves Matrix state, persistence, freshness, Planner and verifier; tested against healthy, one required failure and HTTP limitation | 3 services; `9.793 ms`; 76.3% shorter controlled probe span, 78.6% fewer selected checks and 70.1% less local process CPU | selected core architecture |
| C — existing passive protocol signal escalates only into B | adds earlier suspicion but no truth, incident, candidate or execution owner | no separate Matrix probe claim; its cost is intentionally not added to B | selected only as B's existing optional producer bridge |

**System decision:** `TARGET_ARCHITECTURE_MODEL_B_PLUS_C`, subject to the
existing system-level consumer.  The implementation is not an autonomous
FAST schedule: it is the smallest existing Matrix refresh call with exact
`--egresses` and `--services`, made only by an already-authoritative source /
target selection caller.  It must retain these hard laws:

1. empty selection remains the full Matrix;
2. missing, stale, identity-mismatched or conflicting facts deny selection;
3. a short/full disagreement triggers the full Matrix and records its reason;
4. one sample still cannot create a failure action; and
5. Matrix neither chooses a target nor moves a client.

The existing `tools/v7-service-matrix-refresh-all` already exposes exactly
that bounded call shape and reports `BOUNDED_EXACT_SUBSET_REFRESH`; the
existing `tools/v7-service-matrix-test` owns duplicate rejection, bounded
parallel probing and the sole durable Matrix merge.  There is currently no
admitted automatic role-aware caller, which is correct while the CPS hold is
in force.

## Current reconciliation and exact continuation

`tools/v7-truth-check --all --json` initially found a real document-level
contradiction: OMP's active-Mission report pointer still named the superseded
fast-subset implementation report.  The OMP pointer was minimally corrected
to the CPS-owned active Atlas report, without changing CPS, Runtime, Matrix,
routes or users.  The same full check now returns `CPS consistency PASS`,
`local PASS` and `Runtime PASS`.  The only remaining whole-check blocker is
independent GitHub verification (`github_remote_unreadable` / missing remote
branch view), not an Atlas or Polygon blocker; no remote publication was
attempted.

The wider OMP fixture bundle then exposed one additional historical-test
assumption: its synthetic RS6 case silently inherited today's empty live
incident, so it could no longer prove the historical owner-backed successor
it claims to exercise.  The fixture now supplies its own explicit non-empty
scope and its existing Matrix consumer.  This is test isolation, not a
Runtime change.  Final focused evidence: 3 controlled full/subset Matrix
cases + 2 existing Matrix laws + 43 OMP reconciliation cases = **48/48 PASS**.
The prior stale-fixture residual `G5` is closed; the only remaining Atlas
measurement residuals are `G1` production per-run timing, `G3` live cadence
distribution and `G4` non-Matrix resource cost.  None permits automatic FAST
enablement or needs a natural external event to be represented faithfully.

One caller-level defect was also found and repaired: the existing `Continue
OMP` entrypoint recognised the old V5.3 decision Mission but did not recognise
the current system-level Atlas Mission before falling through to a generic
historical product frontier.  The repaired order now acknowledges the active
Atlas first, returns its existing consumer and preserves all forbidden effects.
The new regression test proves this exact precedence.  The final focused run
is **49/49 PASS**, and a live read-only `Continue OMP` now returns
`ACTIVE_V5_3_SYSTEM_REVALIDATION_PREEMPTS_GENERIC_OMP`, with zero Runtime,
route, user, authority or production-maturity effect.

## Publication and Runtime verification

Commit `a6abfa14` (`v7: retain active health atlas in omp`) was independently
verified on the canonical `Updatesystem` remote branch and deployed through
the existing `v7-safe-deploy` allowlist.  Deployment refreshed only the
approved `v7_sync_lib.py` Runtime support module; it did not start the
autoswitch scheduler, alter a route or move a user.  Fresh full truth check:
GitHub `PASS`, local `PASS`, Runtime `RUNTIME_ALIGNED`, Runtime deploy commit
`a6abfa140bc411dbfd58898b5cf1da9018181d5a`, no blockers.  A post-deploy
read-only `Continue OMP` returned the Atlas as the real consumer and all
forbidden effects remained `false`.

The exact current frontier remains the admitted read-only Atlas.  Its next
consumer must atomically consume this weighted result through the existing
OMP/CPS lifecycle before `V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1`
can be admitted.  Until then the deployment stays exactly as it is: opt-in
selectors available, full Matrix fallback active, automatic FAST role consumer
held, and no client movement.

## Correction and deep mature-platform benchmark — 2026-08-20

### Status correction

The short vendor tables above are retained as `INITIAL_MECHANISM_PATTERN_BENCHMARK`
only.  They were useful discovery evidence, but were not a uniform lifecycle
comparison.  Therefore neither the earlier heading *"Commercial comparison —
completed field mapping"* nor the earlier provisional `B+C` weighted result
may be consumed as a Phase C or Phase E terminal.  This correction is material:
the comparison had not yet tested every platform against the same questions
about cadence, stale evidence, passive escalation, failure domains, quality
and decision placement.

This section is the strict replacement benchmark.  It uses primary vendor
documentation only. `NOT_DOCUMENTED` means precisely that the cited primary
documentation does not define the field; it is not an inference that the
product lacks the mechanism.  Vendor defaults are context, never V7 settings.
No Runtime code, Matrix state, OMP/CPS state, client, route, schedule or
automatic consumer was changed.

### Comparison contract and source dispositions

Every row below is measured against the same lifecycle:

```text
observation -> suspicion -> confirmation -> current state
-> eligibility consequence -> recovery confirmation/re-admission
-> compact stability/quality projection -> existing decision consumer
```

| Primary reference / mechanism | Disposition | Why it remains in the strict comparison |
| --- | --- | --- |
| Envoy active health, outlier detection and health filter | `RESULT_REUSED_VALID` | active/passive, immediate drain, degraded state, identity, event history and probe-economy pattern |
| HAProxy health and passive checks | `RESULT_REUSED_VALID` | explicit normal/transition/down cadence, failure/recovery asymmetry, multi-endpoint and passive error threshold |
| Google Cloud Load Balancing health checks | `RESULT_REUSED_VALID` | independent prober, protocol checks, state threshold and new-connection eligibility pattern |
| FRRouting BFD | `RESULT_REUSED_VALID` | exact bounded transport-liveness model and route-protocol consumer separation |
| Cisco IP SLA / Object Tracking / BFD | `RESULT_REUSED_VALID` | measurement -> tracked object -> route consumer pattern; not an application-health architecture |
| FortiGate Link Health / SD-WAN passive measurement | `RESULT_REUSED_VALID` | active/passive/prefer-passive, quality, re-entry and per-member eligibility pattern |
| MikroTik gateway checks / recursive failover / BFD | `RESULT_REUSED_VALID` | gateway fact, two-timeout rule, route consumer and multiple-host failure-domain pattern |
| AWS ELB/NLB, Juniper and other vendors | `BENCHMARK_NOT_REQUIRED_DUPLICATE_PATTERN` | no named uncovered V7 decision remains after the seven mandatory mechanism classes; adding brands would not make the comparison deeper |

### Uniform field matrix: signal, cadence and state

| Platform / mechanism | Signal and failure domain | Healthy / suspect / down / recovery cadence | Failure and recovery confirmation | Passive escalation, degraded and conflict semantics | Freshness / unknown semantics in source |
| --- | --- | --- | --- | --- |
| Envoy | HTTP, gRPC, L3/L4 and service identity per upstream member | check interval is configurable; separate state-specific cadence is `NOT_DOCUMENTED` on the overview page | configurable failures-to-unhealthy and successes-to-healthy; immediate failure header can drain an active-checked host | outlier detection is passive; degraded is a separate response state; active/passive conflict resolution is `NOT_DOCUMENTED` | cache gives deliberately eventual rather than per-request current view; explicit stale/unknown lease is `NOT_DOCUMENTED` |
| HAProxy | TCP/HTTP; multiple endpoints may form one check and either failure fails it | normal `inter`, transitional `fastinter`, down `downinter`; defaults to `2s` for `inter` | `fall` failures remove from rotation; `rise` successes restore; defaults shown are 3 and 2 | observes live L4/L7 errors with `error-limit`/`on-error`; active checks continue when down and perform recovery confirmation | explicit age/unknown lease is `NOT_DOCUMENTED` |
| Google Cloud | protocol-specific backend probe, implemented by multiple dedicated probers | shared check interval and timeout, default 5s; state-specific accelerated cadence is `NOT_DOCUMENTED` | separately configurable sequential healthy and unhealthy thresholds; defaults 2/2 | passive error signal, degraded tier and active/passive arbitration are `NOT_DOCUMENTED` | probe result is current managed backend state; source does not define a consumer-visible stale/unknown lease |
| FRR BFD | peer/session transport liveness only, not an application service | negotiated/control interval; fixed status-specific cadence is not the BFD model | remote transmit interval × detection multiplier; default example is 300ms × 3 = 900ms | BFD passive mode avoids initiating packets until peer control traffic; no service degraded or passive application error concept | current BFD peer status and counters; no service-evidence freshness model |
| Cisco IP SLA + Object Tracking | scheduled reachability/response measurement consumed by a tracking object and route policy | operation frequency/timeout are configured; role-state cadence is `NOT_DOCUMENTED` in the cited configuration guide | tracked object changes state from measurement; generic application recovery/stale model is `NOT_DOCUMENTED` | no comparable passive application escalation in this mechanism | tracker is current derived state; explicit stale lease is `NOT_DOCUMENTED` |
| FortiGate SD-WAN | active probes or live TCP-session measurement; application/path-specific quality may differ on same link | active interval configurable; passive uses live traffic; `prefer-passive` activates probes after three minutes without traffic | `failtime` failed replies and `recoverytime` successful replies; documented defaults are 5/5 in the link monitor reference | active, passive and prefer-passive modes; passive measures latency/jitter/loss from real traffic; quality breach affects that member | passive metric timestamp exists operationally; a universal unknown/stale failover rule is `NOT_DOCUMENTED` |
| MikroTik RouterOS | gateway ARP/ICMP/BFD; recursive monitored hosts distinguish next-hop availability from route choice | ICMP/ARP gateway check every 10s, 10s timeout | two timeouts make the gateway unreachable; reply resets counter; BFD has its own negotiated detector | no passive application-error escalation in the gateway checker | gateway reachability is current next-hop fact; stale application evidence is outside mechanism scope |

### Uniform field matrix: decision placement, quality, budget and scale

| Platform / mechanism | Eligibility and routing consequence | Quality/history / partial degradation | Probe economy, parallelism and scale | Synchronous versus precomputed | Exact V7 comparison decision and invalidation trigger |
| --- | --- | --- | --- | --- |
| Envoy | unhealthy host is excluded from load balancing; immediate failure can exclude it | explicit degraded state and health event log; no route-policy history model | cached pass-through is recommended for a large mesh to avoid overwhelming the service; exact concurrency budget is `NOT_DOCUMENTED` | health state is precomputed per upstream member and consumed by load balancing | `ADAPT`: preserve Matrix active rows plus passive suspicion, identity and methodology-limited/degraded distinction. **Invalidate** if one Matrix service row is ever allowed to imply source rescue or target admission by itself. |
| HAProxy | thresholded state removes/restores a server in rotation | transition/down state plus active recovery; passive live errors need traffic | multi-endpoint one-check composition; primary tutorial gives no fleet-size formula or bounded worker budget | ongoing health state controls rotation, rather than a synchronous full check at each request | `ADAPT`: measure role-state cadence before any V7 timing change; retain persistence/recovery. **Invalidate** if a cadence proposal has no live V7 duration, load and false-state evidence. |
| Google Cloud | healthy backend may receive new connections; unhealthy is ineligible, existing connection not immediately terminated | detailed healthy/unhealthy/timeout/draining states; history/ranking is out of scope | redundant probers; check setting is shared by backend service; source does not publish a V7-comparable per-tenant budget | managed backend health is precomputed; connection decision consumes it | `REUSE`: Matrix signal, target eligibility and user movement remain three distinct consumers. **Invalidate** if “healthy” is used as proof of a client route or capacity. |
| FRR BFD | routing protocol can consume session loss; it is not a service routing decision | no latency/jitter/loss or service history | subsecond control traffic configurable; passive mode can reduce needless initiation; no V7-size model | peer status is precomputed and consumed by BGP/routing daemon | `REJECT` as a service-health verdict; `REUSE` only as a bounded transport suspicion input. **Invalidate** if V7 treats link liveness as application or target-readiness proof. |
| Cisco IP SLA + Object Tracking | tracked status, rather than raw probe, controls static-route installation/withdrawal | response-time threshold exists; rich application quality/ranking is out of scope | operator-defined frequency/timeout; no universal fleet-scale model in cited source | scheduled measurement produces tracked state; route consumes the tracker | `REUSE`: preserve `Matrix -> existing state -> Planner/verifier`, never probe -> route mutation. **Invalidate** if a producer gains a direct route-apply path. |
| FortiGate SD-WAN | removes only the affected member from SD-WAN eligibility and re-admits after recovery | latency/jitter/loss and per-application passive metrics; partial degradation can choose a different member | passive reduces active probe traffic; prefer-passive has an explicit idle fallback; exact cross-fleet concurrency ceiling is `NOT_DOCUMENTED` | measurement produces member/SLA state then policy chooses members | `ADAPT`: existing quality/stability remains target filter/ranker; use existing Matrix/quality owners only. **Invalidate** if quality alone causes source rescue, or one application metric represents all services. |
| MikroTik RouterOS | gateway result affects a next-hop; route priority/failover then consumes that fact | multiple monitored hosts reduce single-host conclusion; no quality-history ranking | periodic per-gateway probes and BFD; no documented 10/100/1000 scale budget | gateway state is maintained separately from route selection | `REUSE`: retain path, service and user-route as distinct facts; require independent target confirmation. **Invalidate** if a single gateway or monitor host decides profile-wide health. |

### What the benchmark actually establishes

1. **The system is not only testing Matrix services.**  Mature designs split
   at least four evidence families: transport/gateway liveness; service
   reachability; passive real-traffic errors; and quality/stability history.
   V7 already has owners for each family (`HC-01..HC-10`); their conclusions
   must remain separate until the existing Matrix/Planner chain consumes them.

2. **Stability is not background noise.**  HAProxy and Google use asymmetric
   failure/recovery confirmation. FortiGate uses both confirmation and a
   quality history. MikroTik's multiple monitored hosts prevent one external
   target from deciding a whole path. V7's existing persistence, recovery,
   freshness and quality owners are therefore confirmed in principle, but
   their production distributions are still unmeasured.

3. **Passive evidence is an accelerator, not a replacement for proof.**
   Envoy/HAProxy/FortiGate use traffic-derived evidence, but only within a
   bounded state/eligibility model. In V7, the existing sentinel/passive
   producer can create suspicion; it cannot create a second truth, choose a
   server, or switch a client.

4. **A short check must consume precomputed current facts.**  Every relevant
   platform separates ongoing observation from the later routing/load-balancing
   decision. V7 must not reconstruct raw history synchronously in a FAST path.
   Its existing compact Matrix, quality and recovery projections are the only
   lawful input surface.

5. **No vendor source supplies a safe V7 number.**  Intervals from milliseconds
   to minutes reflect radically different topology, probe count, traffic and
   failure domains. They prove the *need to measure differentiated cadence*,
   not a right to copy a `2s`, `5s`, `10s` or BFD timer into V7.

### Strict V7 gap ledger and Phase-C consumption status

| Required comparison field | Result against the complete V7 Atlas | Existing owner / disposition | Required evidence before any architecture decision |
| --- | --- | --- | --- |
| Service, channel and route layers | separated in V7; no new mechanism proven | Matrix, path/route verifier, Planner — `REUSE` | preserve three distinct proofs in each candidate |
| Failure/recovery threshold and hysteresis | V7 has persistence/recovery rules, but not role-state production distributions | Matrix/recovery owner — `ADAPT` measurement only | G1/G3 timing, false-state and flap distribution |
| Healthy/suspect/down/recovering cadence | current global cadence known; role-specific adaptive law not measured | existing timer/Matrix owner — `TARGETED_GAP_RESEARCH_REQUIRED` | controlled and real scheduled-run cost for source, hot target, cold target and recovering roles |
| Passive escalation | a lawful producer exists; scope, age and conflict contract need explicit candidate comparison | existing sentinel/Matrix bridge — `ADAPT` | receipt provenance, expiry and conflict fallback test; no new event owner |
| Degraded and conflicting evidence | methodology-limited outcome exists; complete multi-signal degraded contract not yet selected | existing Matrix/quality owners — `TARGETED_GAP_RESEARCH_REQUIRED` | candidate must say deny, retain, or full-fallback for every conflict |
| Freshness/unknown/stale | V7's deny gates are stricter than documented vendor overviews | Matrix freshness owner — `REUSE` | retain no-failover-on-unknown test in every candidate |
| Multiple targets/failure domains | service and candidate gating exist; quantified correlation policy remains a design residual | Matrix/quality/Planner — `ADAPT` | explicit independent-monitor/failure-domain test matrix |
| Quality/history affects eligibility versus ranking | current quality owner exists; safe immediate-admission use must be chosen | quality/Planner owners — `TARGETED_GAP_RESEARCH_REQUIRED` | prove quality is filter/ranker and never sole source-failure trigger |
| Probe budget, bounded parallelism, 10/100/1000 scale | bounded parallelism exists; no V7 model at those sizes | Matrix owner — `TARGETED_GAP_RESEARCH_REQUIRED` | Phase F cost model: checks, critical path, lock wait, CPU/RSS, errors, timeout pressure |
| Precomputed versus synchronous work | architecture supports it; candidate assignment is not yet made | existing Matrix/history/quality owners — `ADAPT` | map each input to FAST, compact current projection, DEEP, or engineering-only |
| Source failure, target readiness, recovery and post-switch verification | owners are already distinct | Matrix, Planner, verifier/recovery — `REUSE` | every candidate must preserve all four consumer contracts |

**Phase C conclusion:** mandatory platform and mechanism coverage is now
strict and field-by-field; the earlier claim of completed comparison is
corrected.  But `MATURE_HEALTH_AND_COMMERCIAL_ROUTING_MECHANISM_COMPARISON_CONSUMED`
is **not** emitted yet, because the benchmark has identified unresolved V7
measurement/candidate-consumption fields above.  This is not an external wait:
they can be exercised through the existing Polygon and controlled Matrix
boundaries.  The full Matrix remains the safe fallback and the automatic FAST
consumer remains held.

### Exact next step in the whole plan

Plan position: **Phase C source evidence is complete; Phase C consumption and
Phase D are next; Phase E architecture selection and Phase F scale validation
remain after them.**

The exact smallest executable next action is:

```text
Using the existing Matrix, quality, recovery, Planner and Polygon owners,
derive three concrete role-aware candidates (A current improved full Matrix,
B fast-plus-deep under Matrix, C existing passive signal escalates through
Matrix). For each, map source/hot-target/cold-target/degraded/recovering roles,
state age/conflict/full-fallback behavior, and assign every input to FAST,
compact precomputed, DEEP or engineering-only. Then exercise the conflict,
failure-domain and bounded-scale cases on Polygon; do not change Runtime,
route, client or automatic FAST admission.
```

Sources: [Envoy health checking](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking),
[HAProxy health checks](https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/),
[Google Cloud health-check concepts](https://cloud.google.com/load-balancing/docs/health-check-concepts),
[FRRouting BFD](https://docs.frrouting.org/en/stable-7.5/bfd.html),
[Cisco reliable static routing using Object Tracking](https://www.cisco.com/c/en/us/td/docs/ios/dial/configuration/guide/15_0s/dia_15_0s_book/dia_rel_stc_rtg_bckup.pdf),
[FortiGate passive WAN health measurement](https://docs.fortinet.com/document/fortigate/latest/administration-guide/208103/passive-wan-health-measurement),
[FortiGate link-monitor reference](https://docs.fortinet.com/document/fortigate/7.4.10/cli-reference/320711343/config-system-link-monitor),
and [MikroTik WAN backup](https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover%2BWAN%2BBackup).

## Independent candidate-direction audit — 2026-08-20

The three directions in the preceding next step were rechecked against the
current Program rather than assumed correct. They are not an arbitrary choice:
the Program requires that the final Phase-E comparison include these three
models. No fourth direction is lawful or useful unless measurement proves all
three insufficient without adding another health truth or Runtime ecosystem.

| Required candidate | Correct meaning for this Mission | What would make it an invalid candidate |
| --- | --- | --- |
| `MODEL_A_CURRENT_IMPROVED_FULL_MATRIX` | The existing full Matrix remains the normal confirmation path, with the existing freshness, persistence, quality, capacity, route verification and recovery gates. It is the safety and cost baseline, not a discarded legacy implementation. | Calling it a control case without testing source, target, recovery and post-switch behaviour; removing the full fallback. |
| `MODEL_B_FAST_PLUS_DEEP_UNDER_EXISTING_MATRIX_OWNER` | An already-authoritative caller supplies exact affected source/eligible targets and required profile services; the existing Matrix performs only the bounded confirmation, retains the canonical write and falls back to full Matrix on empty, stale, unknown, identity-mismatched or conflicting input. DEEP remains diagnostic, quality, capacity and history work under existing owners. | A new fast owner, raw-history scan in the immediate path, manual server choice, or short check deciding a client move. |
| `MODEL_C_EXISTING_SIGNAL_ESCALATION_THROUGH_MATRIX_OWNER` | An existing passive/protocol signal may create only timely suspicion and request Model-B/Matrix confirmation. It remains separately comparable at first so that its detection benefit and false-escalation cost can be measured. After proof it may be merged into B, never promoted to a second event or switching system. | Passive signal directly declaring a failure, choosing a target, or bypassing Matrix persistence, freshness, Planner and verifier gates. |

### Audit result

The directions are therefore **correct, necessary and sufficiently distinct
for comparison**, with two safeguards:

1. Model C is an escalation *mode*, not a competing routing model. It is kept
   separate only until the measurement says whether it improves Model B safely.
2. Model B+C is not selected in advance. The older `B+C` statement remains
   historical/provisional and cannot decide implementation or automatic FAST
   admission.

The previous exact-next-action wording is superseded by this complete one:

```text
For each of A, B and C, use only existing Matrix, quality, recovery, Planner,
verifier and Polygon owners to define all seven roles: ACTIVE_SOURCE,
ELIGIBLE_HOT_TARGET, COLD_UNUSED_TARGET, DEGRADED, UNUSABLE, RECOVERING and
ENGINEERING_CERTIFICATION_ONLY. Map transport, service, passive, stability and
target-suitability evidence to FAST, compact precomputed, DEEP or
engineering-only placement. State source, target, recovery and post-switch
contracts; cadence/timeout/parallelism/persistence; failure/recovery
thresholds; stale/unknown/conflict/full-fallback handling; expected detection
latency and false-positive/false-negative risk; probe cost at current, 50 and
1,000 egresses; owner reuse, migration risk and rollback.

Then run only the existing Polygon/controlled-Matrix cases that distinguish A,
B and C: conflicting evidence, correlated failure domain, stale/unknown denial,
target readiness, recovery flap and bounded scale. No Runtime, route, client,
timer or automatic FAST-consumer change is admitted by this comparison.
```

This audit changed no system behaviour. It only corrects the candidate
evaluation contract before any architecture decision.
