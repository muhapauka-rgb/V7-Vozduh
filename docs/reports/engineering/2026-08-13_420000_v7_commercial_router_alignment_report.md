# V7 Commercial Router Alignment Report

Status: `RT2_PR2B_COMMERCIAL_ROUTER_ALIGNMENT_AUDIT_PASS_READ_ONLY`

Scope: existing OMP §28.9 `RT2-PR2B COMMERCIAL ROUTER ARCHITECTURE BENCHMARK AND V7 ALIGNMENT AUDIT`. This consumes PR1 baseline, PR2 package audit, PR2A code-responsibility audit and M10 benchmark. It is comparison and classification only: no code, CPS, Runtime, production, service/timer, routing, cleanup or Authority change occurred.

## 1. Purpose and reference model

The purpose is not vendor imitation. It is to compare stable responsibility boundaries—decision state, forwarding programming, health/admission, failover/recovery and operations—against V7's proven reality, then identify only evidence-backed simplification work.

| Reference | Relevant architectural pattern | Boundary used for V7 comparison |
| --- | --- | --- |
| Junos | Routing Engine owns routing/control state; Packet Forwarding Engine owns packet lookup/forwarding. Active forwarding state is copied to the forwarding engine, which can keep forwarding during a control-plane disruption. | narrow forwarding plane, explicit control state, install/error verification |
| Cisco IOS XR | Manageability, protocol/application, infrastructure/RIB and hardware-abstraction layers are distinct. RIB chooses best routes and installs them to forwarding line cards; the OFA layer programs the dataplane from RIB/LSD state. | management/control/dataplane placement and one direction of programming |
| FRRouting | Protocols supply best routes to Zebra/RIB; Zebra derives FIB and programs the kernel or FPM. A dataplane queue/plugin offloads FIB programming and has explicit installation/debug visibility. | single routing ownership, desired-to-kernel projection, replacement/reconciliation semantics |
| Linux routing | Userspace configures and observes route objects through rtnetlink; the kernel owns forwarding execution. | narrow userspace-to-kernel adapter and observable applied state |
| Cloudflare Load Balancing | Monitors produce health observations; pools aggregate endpoint availability; steering excludes unhealthy targets and handles failover. | health freshness/admission and failure containment only—not router/RIB implementation |

Primary sources: [Junos Architecture Overview](https://www.juniper.net/documentation/us/en/software/junos/junos-overview/topics/concept/junos-software-architecture.html), [Junos forwarding-table continuity](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/show-pfe-data.html), [Cisco IOS XR architecture](https://www.cisco.com/c/en/us/products/collateral/ios-nx-os-software/ios-xr-software/datasheet-c78-743014.html), [Cisco IOS XR RIB monitoring](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/routing/configuration-guide/routing-config-cisco8000/implementing-and-monitoring-rib.html), [FRR Zebra](https://docs.frrouting.org/en/stable-7.2/zebra.html), [Linux rt-route Netlink](https://docs.kernel.org/next/networking/netlink_spec/rt_route.html), and [Cloudflare health/pool model](https://developers.cloudflare.com/load-balancing/understand-basics/health-details/).

## 2. Common mature-system patterns

| Question | Common pattern | V7 evaluation criterion |
| --- | --- | --- |
| Routing decision | A bounded Control Plane/RIB selects desired forwarding state from owned policy, topology and health facts. | no independent UI, report, health probe or legacy helper may silently become a second primary routing decision owner |
| Plane separation | Management requests/observes; Control decides; Data Plane forwards from installed state. Engineering improves asynchronously. | packet forwarding must not synchronously require OMP, report, learning, Polygon or replay |
| Health/admission | Probe/telemetry producers update freshness-bound state; policy consumes it to admit or exclude a target. | a signal is not movement authority; stale/partial state fails closed |
| Failover | detect -> update state -> select -> program forwarding -> verify. | each edge must have one owner, bounded scope and terminal |
| Recovery | retain a known good forwarding state; fence writers; reconcile install failure; roll back only through the safety owner. | recovery may be separate but must not become an unbounded parallel primary path |
| Scale | forwarding cardinality and synchronous work are bounded independently of operational history; RIB/FIB update and verification are observable. | V7 must retain class routing and avoid per-user primary rules/tables or O(N) hot-path reconciliation |

## 3. Reference-system comparison

| Reference | Routing decision / state owner | Management / Control / Data separation | Health, failover and recovery | Scaling conclusion |
| --- | --- | --- | --- | --- |
| Junos | Routing Engine maintains routing and forwarding tables; PFE uses a local forwarding copy. | management/routing operations remain on Routing Engine; PFE forwards packets. | PFE installation feedback can identify RIB/FIB discrepancy; local FIB preserves forwarding through control interruption. | data packet processing does not traverse management/routing processes per packet. |
| IOS XR | protocols/RIB select best routes; infrastructure layer exposes routing state; OFA programs hardware from that state. | CLI/YANG management, protocol layer, infrastructure/RIB and hardware abstraction are explicit. | RIB/forwarding comparison supports inconsistency troubleshooting. | modular layers and a common RIB avoid each API or protocol programming a separate forwarding truth. |
| FRR | Zebra owns RIB/FIB mediation; protocols do not individually own kernel programming. | protocol daemons -> Zebra -> kernel/FPM. | FIB programming is explicit; replace semantics and reconnection/full-table refeed support convergence. | a dedicated dataplane execution boundary avoids putting FIB work in every protocol path. |
| Linux | userspace requests routes; kernel FIB forwards. | rtnetlink is the control/configuration API, not the forwarding loop. | `getroute`, create and delete route operations make installed state observable. | kernel forwarding cardinality/lookup is separate from userspace workflow history. |
| Cloudflare-style LB | monitors/pools own endpoint health; steering chooses eligible pool/endpoint. | management configures monitors/pools; health observation informs steering; request path uses that decision. | health state excludes unhealthy endpoints; failover is bounded by pool/steering policy. | health aggregation and steering avoid every request needing engineering history. |

## 4. V7 current mapping and decisions

| Responsibility | Commercial pattern | V7 current implementation | Gap | Recommended action |
| --- | --- | --- | --- | --- |
| Health | dedicated observation updates freshness-bound health state | Matrix refresh, Telegram sentinel (`--no-autoswitch`), quality and health loops produce/control health facts | multiple producers and a health loop with several outputs need writer/reader fencing; not a duplicate primary router | `KEEP` producers; `SHRINK` only after per-state ownership map |
| Admission | policy/RIB consumes current health/capacity, not a bare probe | existing Matrix/quality + policy/capacity/Authority gates; `EGRESS_ADMISSION_STATE` is logical projection | current runtime package projection under-describes active path-guard and Direct chains | `KEEP`; reconcile existing package/topology truth |
| Routing decision | one Control Plane selects desired forwarding state | assignments, policy/capacity/Authority, Routing Core and governed planner paths | `v7-users-autoswitch` still co-locates planning, diagnostics, certification and fallback movement | `SHRINK` planner responsibilities; preserve exact governed decision owner |
| Dataplane apply | narrow adapter programs FIB/kernel from approved state | `v7-routing-sync` applies nft class maps and six fwmark/table classes under one lock | none proven in primary Core path | `KEEP`; do not create Core v2 or a second writer |
| Verification | applied FIB/kernel state and traffic outcome are independently checked | Core verify checks nft/ip state; PR1 real ordinary traffic counter remains unproven | kernel verification cannot substitute for user traffic outcome | `KEEP`; wait for ordinary traffic evidence without manufacturing it |
| Recovery | fenced bounded recovery with install/reconciliation proof | Packet/lease/barrier plus `v7-user-switch` fallback; path guard can call repair actions | active path guard is a hidden mutation-capable dependency relative to M10 description | `LEGACY_EXCEPTION`; reconcile scope/Authority/failure matrix before narrowing |
| Learning | asynchronous feedback, never forwarding prerequisite | OMP, Reports, Polygon, Learning and Replay are outside Core packet path | no primary-path violation found; large engineering modules co-locate concerns | `KEEP_ENGINEERING`; `SHRINK` interfaces, not add machinery |
| Engineering tooling | separate from live RIB/FIB and management operations | `v7_sync_lib.py` owns CPS/OMP/Polygon/deploy helpers | co-location increases audit/mutation blast radius | `MOVE/SHRINK` by existing interfaces after admission |
| Admin/control API | management layer issues guarded requests; it is not a routing engine | `admin/v7-admin-api` serves UI, read models and guarded actions | 16,528-line embedded UI plus route/action/config logic in one executable | `SHRINK` by presentation and route-group extraction; retain one guarded API boundary |

## 5. Correct existing decisions to preserve

- `v7-routing-sync` is a narrow, single-lock userspace-to-nft/ip adapter. It is V7's correct equivalent of a constrained FIB-programming boundary, not a decision engine.
- Primary forwarding uses six classes and nft membership rather than per-user primary rules/tables. This preserves the M7/M9 scale simplification.
- OMP, reports, Polygon, learning and replay are not synchronous Core forwarding dependencies.
- `operator_execution` owns packet/lease/barrier, exact action class, replay prevention and rollback compensation. This is a necessary safety boundary, not removable ceremony.
- Matrix/sentinel health signals remain evidence producers; sentinel deployment with `--no-autoswitch` preserves the rule that a fast observation is not itself movement Authority.

## 6. Gap and component placement analysis

| V7 surface | Mature-system placement | Current V7 reality | Classification | Future disposition |
| --- | --- | --- | --- | --- |
| `v7-users-autoswitch` | Control Plane decision plus separately bounded recovery; diagnostics outside routing engine | mixes event consumption, planning, fallback movement, rollback, certification and diagnostics | `RESPONSIBILITY_MIXING` | `SHRINK`; move diagnostics/certification to existing Engineering owner, retain fallback execution |
| `v7_sync_lib.py` | separate management/truth, orchestration, verification and release interfaces | CPS reconciliation, continuation, Polygon and deploy co-located | `RESPONSIBILITY_MIXING` | `MOVE/SHRINK` through existing public interfaces; no Runtime move |
| `admin/v7-admin-api` | Management Plane UI/API separate from control logic | UI rendering, read models, dispatch and component action adapters co-located | `RESPONSIBILITY_MIXING` | `SHRINK`; move presentation and route groups, retain guarded operator boundary |
| `v7-path-guard-repair` | recovery/repair subsystem with strict writer fence | timer may invoke sysctl, MSS, routing-sync, killswitch and Direct autosync | `HIDDEN_RUNTIME_DEPENDENCY`, `LEGACY_EXCEPTION` | `KEEP` pending authoritative failure/recovery matrix; no blind disable |
| Direct autosync | separate Direct-service control subsystem | timer updates Direct config/DNS and state | `CONTROL_PLANE`, not Routing Core | `KEEP_RUNTIME`; state its boundary in existing package truth |
| Matrix refresh / sentinel / health | health observation and admission inputs | several producers/consumers, with sentinel no-autoswitch | potential state-writer overlap, no proven duplicate forwarding writer | `KEEP`; first map writer fencing and output consumers |

## 7. Classification register

### KEEP

- Core dataplane adapter, class routing, explicit nft/ip verification and one routing lock.
- Existing Assignment/Policy/Capacity/Authority gates.
- `operator_execution` Packet/lease/barrier/rollback boundary.
- Matrix/sentinel observation model and Engineering Plane exclusion from forwarding.

### MERGE

No merge is admitted. Candidate review only: equivalent health-state writers and duplicated API/read-model shaping require evidence of same state, same consumer and same failure contract before consolidation.

### MOVE

- planner-hosted diagnostics/certification responsibilities -> existing Engineering Plane owner;
- embedded admin presentation -> existing UI/presentation boundary;
- `v7_sync_lib.py` responsibility groups -> existing CPS, continuation, Polygon and deploy interfaces.

### SHRINK

- `v7-users-autoswitch`: separate event/diagnostic/certification from governed fallback movement;
- `v7_sync_lib.py`: split public interfaces without multiplying truth owners;
- `admin/v7-admin-api`: separate UI asset and route groups;
- health loop: only after output-level ownership proof.

### REMOVE CANDIDATE

`NONE`. No reviewed surface satisfies all four requirements: no consumer, no product effect, no safety effect and no lifecycle obligation.

## 8. Recommended cleanup order (not executed)

```text
EXISTING OMP/CPS ADMISSION
  -> reconcile actual active runtime package/topology
  -> map health state writers/readers and path-guard recovery authority
  -> isolate one low-risk Engineering or UI responsibility group
  -> affected tests and existing promotion ladder
  -> safe deploy / observation / residue proof
  -> only then consider a separate function-level removal candidate
```

This sequence keeps the proven fast path intact and gives precedence to truth/recovery boundaries over LOC reduction.

## 9. Completion and residual

- Reference architecture model selected from primary vendor/kernel/operator documentation: `PASS`.
- Mature routing, health/failover and state/plane patterns compared to PR1/PR2/PR2A reality: `PASS`.
- V7 gap and simplification classification register created: `PASS`.
- No code, Runtime, production, CPS, Authority or cleanup operation performed: `PASS`.
- `COMMERCIAL_ROUTER_ALIGNMENT_AUDIT_PASS = PASS`.

Residual: `RT2-PR3` is still not admitted. Its prerequisites remain the existing OMP/CPS transaction, real ordinary traffic observation and runtime-package truth reconciliation. Vendor comparison is not an implementation authorization.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 145 -> +145` for this report; the OMP contract row is reported separately from program source.

Test LOC: `0 -> 0 -> 0`.

Files/functions/classes/entrypoints/dependency edges/state surfaces/runtime units/routing objects added, removed, moved or changed: `0` program changes; read-only classification only.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`
