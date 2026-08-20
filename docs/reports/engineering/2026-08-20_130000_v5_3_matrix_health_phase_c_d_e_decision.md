Mission ID: `V7_MATRIX_HEALTH_PHASE_C_D_E_DECISION_V1`
Run Nonce: `v53_matrix_health_decision_20260820`

# V5.3 Matrix Health Phase C/D/E Decision

Status: `READ_ONLY_V5_3_MISSION_COMPLETE_CONSUMED`

## Activation and reused reality

`cpsgen_SFA_V53_DECISION_5ECFBB08DE7BDF52` was atomically projected through
the existing CPS writer to `cpsgen_SFA_V53_ADMITTED_5ECFBB08DE7B` with
`CURRENT_EXECUTION_MISSION_STATE=MISSION_ADMITTED`. The existing lifecycle
binding then returned `MISSION_EXECUTION_ALLOWED`. Classification:
`ADMISSION_HANDLER_EXISTS_BUT_NOT_CONNECTED`; the smallest repair connected
the existing V5.3 read-only projection to the existing OMP/CPS lifecycle.

The following current evidence was reused as `RESULT_REUSED_VALID`: Product
Evolution arbitration; empty ordinary incident scope; Stage 48 lane-local
`CONTROLLED_SUBSTRATE_BLOCKED` at `11<48`; V5.3 admission readiness. No Runtime,
route, user, policy or production state was changed.

## Phase A/B compact baseline

The existing Matrix owner runs 14 protocol/service checks per enabled egress,
up to eight service checks in parallel within one egress, while
`v7-service-matrix-refresh-all` traverses enabled egresses serially. Current
topology evidence is seven egresses, therefore one full generation is 98
service probes. Normal cadence is 15 minutes plus bounded jitter; hard failure
requires three samples/persistence, while the Telegram sentinel and legally
consumable passive errors can produce earlier suspicion. The Matrix owns the
atomic row, episode persistence and canonical service-failure observation;
Planner/capacity owners separately own target suitability and route choice.
Raw history remains in existing event/history/quality owners.

The tester already supports `--services=<exact comma-separated subset>` and
preserves the same writer lock, row schema, path fingerprint, persistence and
event producer. The missing capability is placement/wiring of that existing
subset at the refresh-all source/target boundary, not a new probe engine.

## Phase C — mature mechanism comparison

| Platform/mechanism | Confirmation, state and consumer | V7 disposition and consequence |
| --- | --- | --- |
| Envoy active HTTP/gRPC/L3-L4 plus passive outlier/ejection | Protocol-aware active thresholds; passive timeouts/resets/application errors; healthy/degraded/ejected eligibility; recovery thresholds/backoff. | `ADAPT`: reuse V7 protocol-specific Matrix and passive signal; add FAST confirmation and keep DEEP Matrix. Do not copy proxy-specific cluster truth. |
| HAProxy `fall/rise`, `inter/fastinter/downinter` | Consecutive failure removes a server; consecutive success restores it; transition/down cadence may differ. | `ADAPT`: preserve V7 persistence and conservative recovery, add role/state-aware cadence under Matrix owner. |
| Google Cloud health checks | Backend/protocol-compatible probes, healthy/unhealthy thresholds, backend eligibility. | `REUSE`: confirms protocol-aware evidence and eligibility separation; cloud distributed prober topology is rejected. |
| FRRouting BFD | Lightweight liveness at negotiated interval × detection multiplier; routing protocols consume BFD state. | `REUSE/REJECT`: reuse measurement→state→consumer separation; do not use BFD as application/service truth. |
| Cisco BFD + IP SLA/Object Tracking | BFD liveness or SLA measurement produces tracked state consumed by routing; dampening protects flaps. | `ADAPT`: compact current state and routing-consumer separation; no new route authority. |
| FortiGate Performance SLA | Active/passive evidence, latency/jitter/loss, multiple checks, member usable/unusable and path-selection effect. | `ADAPT`: reuse existing quality/capacity/history owners as compact target-suitability input; no raw-history hot-path scan. |
| MikroTik gateway checks/recursive routes | ARP/ICMP/BFD or remote-host reachability changes gateway state; distance/recursive route selects path; multiple hosts reduce false failure. | `ADAPT`: bounded path plus service confirmation; reject single-host generic ping as sufficient service proof. |

Primary sources: [Envoy active health](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/health_checking),
[Envoy passive/outlier detection](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier),
[HAProxy health checks](https://www.haproxy.com/documentation/haproxy-configuration-tutorials/reliability/health-checks/),
[Google Cloud health concepts](https://cloud.google.com/load-balancing/docs/health-check-concepts),
[FRRouting BFD](https://docs.frrouting.org/en/latest/bfd.html),
[Cisco BFD](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/routing/configuration-guide/routing-config-cisco8000/bfd-wrapper/information-about-bfd.html),
[Cisco IP SLA Object Tracking](https://www.cisco.com/c/en/us/support/docs/smb/switches/cisco-550x-series-stackable-managed-switches/smb5793-configure-ip-sla-tracking-for-ipv4-static-routes-on-an-sg550.html),
[FortiGate Performance SLA](https://docs.fortinet.com/document/fortigate/7.0.5/administration-guide/943037/monitor-performance-sla),
[MikroTik recursive WAN failover](https://help.mikrotik.com/docs/spaces/ROS/pages/26476608/Failover%2BWAN%2BBackup).

AWS is `BENCHMARK_NOT_REQUIRED_DUPLICATE_PATTERN`; no unresolved mechanism
class remains. Juniper/Arista/Palo Alto/Ubiquiti are likewise not required.

Phase C terminal:
`MATURE_HEALTH_AND_COMMERCIAL_ROUTING_MECHANISM_COMPARISON_CONSUMED`.

## Required mechanism answers

1. Hard path failure is detected by lightweight protocol/path liveness or
   passive connection failure, then confirmed by thresholds/persistence.
2. Transport liveness and application health are separate evidence classes;
   a connected socket cannot prove the required service.
3. Passive timeouts, resets and protocol errors accelerate suspicion and may
   trigger bounded active confirmation.
4. DOWN requires a hard signal or consecutive/persistent failures, not one
   ambiguous sample.
5. Recovery requires fresh protocol-appropriate success, usually repeated.
6. Recovery is more conservative because premature re-entry re-exposes users
   and creates oscillation; failure may need to protect users quickly.
7. Mature systems use normal, transition, down and event-accelerated cadence.
8. They retain compact current health/eligibility between probes.
9. Recent instability affects backoff, degraded/recovering state and priority.
10. Fall/rise asymmetry, hold-down, ejection backoff and dampening prevent flap.
11. A recovered path passes rise/readiness gates before ordinary eligibility.
12. Active source answers “must users be rescued”; a standby answers “can it
    safely receive them now”.
13. Cold standby does not need the same full cadence; hot targets need bounded
    fresh readiness, and cold targets may use slower DEEP checks.
14. Current health changes eligibility/priority; it does not itself own route
    selection.
15. Probe owner measures, Matrix/state owner confirms, Planner/routing owner
    selects and applies under existing Authority.
16. Latency/jitter/loss classify degraded suitability and quality; they are not
    substitutes for hard reachability.
17. Probing scales by role, cached/compact state, passive evidence, subsets and
    slower DEEP cadence—not by users.
18. Bound the budget by services × eligible role cohort × cadence, with caps
    and escalation only on suspicion.
19. UNKNOWN/stale/conflicting evidence fails closed for new target admission
    and cannot manufacture a source failure.
20. FAST consumes compact current projections; raw history stays background.

## Phase D — V7 role and stability model

The existing Matrix row remains the only health store and canonical service
failure observation owner. Its state model is interpreted as:

| State | Entry and use |
| --- | --- |
| `UNKNOWN` | Missing/stale/conflicting required evidence; target admission closed. |
| `PROBING` | Bounded confirmation in progress; no new positive eligibility. |
| `HEALTHY` | Fresh required path/service evidence and applicable suitability pass. |
| `DEGRADED` | Reachable but quality, partial-service or recent-instability concern; deprioritized/limited. |
| `UNUSABLE` | Confirmed hard/path/required-service failure; source rescue eligible and target excluded. |
| `RECOVERING` | Fresh success after failure but rise/stability/readiness confirmation incomplete. |

Role contracts:

- `ACTIVE_SOURCE`: FAST path/service subset plus passive escalation; enough to
  prove a material required-service failure for its assigned ordinary scope.
- `ELIGIBLE_HOT_TARGET`: bounded fresh path + protocol-required subset plus
  precomputed quality/capacity/policy/reserve suitability.
- `COLD_UNUSED_TARGET`: slow DEEP/background Matrix; accelerated only when it
  becomes a candidate.
- `ENGINEERING_CERTIFICATION_ONLY`: full/deep evidence by the existing
  certification owner, never ordinary routing eligibility.

Evidence placement:

- FAST: current transport/path liveness, minimal protocol/service subset,
  legally consumable passive signal and current scope identity.
- Precomputed: temporal stability, freshness, quality/capacity/policy/reserve
  and target suitability fingerprints from existing owners.
- DEEP/background: all 14 services, broad quality diagnostics, raw event/
  egress history and trend derivation.
- Engineering/Learning only: long-horizon causal learning and certification
  evidence unless an existing owner projects a bounded current fact.

`SOURCE_HEALTH_NOT_EQUAL_TARGET_READINESS` is preserved. Immediate health,
persistence, recovery, short/medium stability and long-term history remain
separate. Raw history is transformed by existing background owners into a
compact current stability projection; FAST never scans it. Failure is
fast-confirmed, recovery uses conservative repeated success/readiness and
UNKNOWN remains fail-closed.

Phase D terminal:
`V7_ROLE_AND_STABILITY_HEALTH_MODEL_CANDIDATE_CONSUMED_BY_PHASE_E`.

## Phase E — formal architecture decision

| Model | Verdict | Reason |
| --- | --- | --- |
| A: improved full Matrix | Reject | Retains 14×egress synchronous probe volume and serial cross-egress detection; poor 50/1000-egress economics. |
| B: FAST + DEEP under Matrix owner | Select | Reuses the existing subset, writer, state/event and fallback while separating decision-critical evidence from diagnostics. |
| C: existing-signal escalation | Merge into B | Passive signals should accelerate bounded Matrix confirmation, not become another event/health system. |

Decision: `TARGET_ARCHITECTURE_MODEL_B_PLUS_C`.

- FAST boundary: active sources and hot targets only, exact role-aware service
  subset, passive-triggered confirmation, same Matrix write/event owner.
- DEEP boundary: full 14-service generation, cold targets, broad quality,
  diagnostics, Engineering/Learning and fallback.
- Source contract: required protocol/service failure + persistence + ordinary
  affected scope.
- Target contract: fresh path/service subset + compact stability, quality,
  capacity, policy, reserve and role facts.
- Stability/recovery: current 5m/1h or equivalent compact projection from
  existing owners; conservative rise/re-entry, no raw scan.
- Canonical owner: `tools/v7-service-matrix-test.update_matrix`; Planner and
  routing remain consumers, not health writers.
- Passive contract: suspicion/escalation only until the existing Matrix owner
  confirms and emits the canonical event.
- Fallback: current full Matrix.
- Invalidate on: subset false-negative/false-positive against full Matrix,
  stale target readiness, probe-budget breach, lock/state regression, changed
  required services, or lost source/target identity.

Terminal: `V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED`.

## Scale and probe economy

Let `E` be enabled egresses and `H` the bounded hot cohort. Current DEEP cost is
`14E` service attempts/generation. Selected FAST uses two service attempts per
active source/hot target in the first residual (one global HTTP reachability
check plus Telegram protocol-specific check); DEEP remains `14E` but at the
existing background cadence. Target-readiness non-network facts are compact
reads and do not add service probes.

| Egresses | Current full generation | FAST when H=min(E,4) | Reduction on decision path | DEEP background |
| ---: | ---: | ---: | ---: | ---: |
| 7 | 98 | 8 | 91.8% | 98 |
| 50 | 700 | 8 | 98.9% | 700 |
| 100 | 1,400 | 8 | 99.4% | 1,400 |
| 1,000 | 14,000 | 8 | 99.94% | 14,000 |

If all egresses temporarily become hot, FAST is `2E` (14, 100, 200, 2,000),
still 85.7% below full service volume. Expected detection is passive-event or
FAST cadence plus persistence; worst case is bounded by FAST timeout × two
parallel services per selected egress plus persistence windows, not `14E`
service attempts. Cross-egress caps 2/4 remain a later measured optimization:
after role/subset reduction, concurrency is not the first residual and cannot
be used to hide external probe volume.

Scale verdict: `PASS_ARCHITECTURE`; 1,000-egress stress requires sharded/slow
DEEP scheduling before production scale, but does not invalidate the FAST
decision because the hot cohort and probe budget are bounded.

## First implementation residual and migration blueprint

`FIRST_IMPLEMENTATION_RESIDUAL_CONFIRMED=CONNECT_EXISTING_EXACT_SERVICE_SUBSET_AND_EXACT_EGRESS_SELECTION_TO_REFRESH_ALL_FAST_SOURCE_TARGET_PATH`

The retained Mission identity is
`V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1` because the evidence
selects its contract but narrows the first change to existing-subset wiring.

Migration:

```text
CURRENT serial refresh-all -> TARGET exact egress + exact service subset mode
-> existing refresh-all and matrix-test owners change
-> existing Matrix/Planner consumers read unchanged row/event schema
-> focused selection/command/writer/persistence tests
-> full Matrix is safe fallback
-> no full synchronous refresh is removed until comparison proves equivalence
-> residue check for duplicate writer/event/health truth
-> before/after attempts, wall time, CPU/RSS, event and state-schema delta
```

Read-only Mission consumer result:
`READ_ONLY_V5_3_MISSION_COMPLETE_CONSUMED`. The exact successor is the bounded
implementation Mission above; Stage 48 remains an independent blocked lane.

