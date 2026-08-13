# RESET-M10 Runtime Simplification and Final Architecture Engineering Report

Status: `RESET_M10_COMPLETE`

This is the single decision-oriented M10 report. It reuses the M0-M9 coverage ledger, Master Audit, production promotion/retirement evidence and canonical owners; it does not restart the repository audit or create an inventory, Runtime, owner, state surface or truth source.

## RESET-M10.1 — Architecture responsibility audit

| Scoped surface | Placement | Existing owner | Real consumer / product effect | Lifecycle and final disposition |
| --- | --- | --- | --- | --- |
| nft `user_class` / `class_egress`, six fwmark rules and six route tables | `DATA_PLANE_REQUIRED` | `tools/runtime-support/v7-routing-sync` plus Linux nft/ip owners | production client packets; applies forwarding state | continuously active `KEEP`; remove only after a proven replacement |
| `v7-routing-sync` Core-primary apply, verify and fallback | `DATA_PLANE_REQUIRED` | existing routing writer | kernel forwarding and restart/recovery | primary `KEEP`; legacy builder retained only as explicit fallback |
| users/egress registries and assignments | `CONTROL_PLANE_REQUIRED` | existing Assignment owners | Core class membership and current-egress resolution | `KEEP`; volatile facts are not copied into reports |
| service Matrix, route-class fitness, quality and tunnel/runtime probes | `CONTROL_PLANE_REQUIRED` | existing Matrix/quality/runtime-health owners | target admission and Planner safety gates | `KEEP`; asynchronous observation, never forwarding authority |
| policy, capacity and delegated action-class contract | `CONTROL_PLANE_REQUIRED` | existing policy/capacity/Authority owners | bounds legal target selection and user movement | `KEEP`; fail closed when stale or absent |
| `admin_core/routing_core.py` | `CONTROL_PLANE_REQUIRED` | existing Routing Core decision owner | effect-free decision comparison and bounded Core semantics | `KEEP`; no dataplane effect by itself |
| governed Packet/lease/barrier, `v7-user-switch`, verification and rollback | `LEGACY_EXCEPTION` | existing execution/Authority/verification owners | bounded user movement and recovery when explicitly admitted | `fallback_only`; not a primary forwarding dependency; removal requires equivalent Authority, rollback and crash-recovery proof |
| `tools/v7-users-autoswitch` | `LEGACY_EXCEPTION` | existing Planner/autoswitch owner | manual/governed fallback, certification and exact action-class execution | installed but timer inactive; `NOT PRIMARY`, `NOT CORE DEPENDENCY`, retained for safety/compatibility |
| Matrix refresh, Telegram sentinel and quality collection | `CONTROL_PLANE_REQUIRED` | existing observation owners | fresh health facts and failure events | asynchronous `KEEP`; no synchronous Core apply dependency |
| OMP, CPS reconciliation, Reports, Polygon, Learning, Replay and campaigns | `ENGINEERING_PLANE_REQUIRED` | existing OMP/evidence/learning owners | engineering continuation, audit, certification and improvement | `engineering_only`; forbidden in live forwarding decisions |
| historical Programs and M0-M9 reports | `ENGINEERING_PLANE_REQUIRED` | existing document/evidence owners | explanation and prior decision evidence | `HISTORICAL_EVIDENCE`; never live Runtime or architecture truth |
| 124 per-user source rules and 124 per-user route tables | `REMOVE` | former legacy routing writer | no remaining primary consumer | already physically removed by M9; fallback can reconstruct them only during explicit recovery |
| active `v7-users-autoswitch.timer` as primary movement loop | `REMOVE` | former automation surface | no admitted primary consumer | already inactive/manual; must not be re-enabled as a parallel primary path |

`DELETE_TEST` result: deleting the Core dataplane breaks production forwarding; deleting current Assignment/Policy/Authority/Health inputs breaks lawful decisions; deleting governed fallback loses required rollback/recovery semantics. OMP/history/report surfaces can be absent from the production routing process without changing forwarding and are therefore physically excluded from the primary dependency graph. No scoped component remains unclassified and no duplicate primary routing owner remains.

## RESET-M10.2 — Industry benchmark

The benchmark is principle-only:

- Junos separates the Routing Engine from the Packet Forwarding Engine and updates forwarding without interrupting packet flow. V7 conforms through Control Plane owners preparing state and the nft/ip Data Plane applying it.
- IOS XR separates protocol/RIB functions from a hardware-abstraction layer that programs the dataplane, and favors a leaner architecture with optional components packaged by role. V7 conforms by keeping the minimal Core adapter primary and classifying engineering/governed surfaces outside it.
- FRRouting separates protocol daemons from zebra/dataplane coordination. V7 uses the same responsibility boundary, not FRR code or protocol topology.
- Linux rtnetlink/FIB contracts distinguish control messages from kernel forwarding state. V7's nft/ip writer and post-apply verification are the bounded adapter to that state.

No benchmark requires a new daemon, protocol suite, owner or abstraction. Material boundary comparison is complete: V7 has explicit decision, apply and engineering responsibilities; the retained governed executor is an owner-backed safety exception outside primary forwarding.

## RESET-M10.3 — CHANNEL_HEALTH_MODEL

`EGRESS_ADMISSION_STATE` is a logical projection of existing facts, not stored state. Its owner is the existing Matrix/quality/runtime-health composition consumed by existing policy/capacity/Planner gates.

| State | Required existing evidence | New-client admission | Existing-client use | Legal successor |
| --- | --- | --- | --- | --- |
| `UNKNOWN` | missing, stale or generation-unbound transport/service/quality/capacity evidence | forbidden | retain only under current fail-closed policy; probe required | `PROBING` |
| `PROBING` | current observation owner is collecting a generation | forbidden | no new movement; current traffic is not proof of eligibility | `HEALTHY`, `DEGRADED`, `UNUSABLE` |
| `HEALTHY` | interface/transport usable; required service fitness acceptable; quality within policy; lawful spare capacity; facts fresh | allowed inside Policy and Authority | allowed | `DEGRADED`, `UNUSABLE`, `PROBING` after invalidation |
| `DEGRADED` | transport exists but one or more service/quality/capacity criteria are marginal | forbidden unless exact policy explicitly admits degraded use | may continue only within existing safety policy while a healthy alternative is evaluated | `HEALTHY`, `UNUSABLE`, `PROBING` |
| `UNUSABLE` | hard transport failure or required service/quality/capacity gate fails | forbidden | evacuation candidate; mutation still requires Policy, Authority, rollback and verification | `RECOVERING`, `PROBING` |
| `RECOVERING` | fresh positive samples after unusable state, but hold-down/persistence not yet satisfied | forbidden | not a target; existing use only under recovery policy | `HEALTHY`, `DEGRADED`, `UNUSABLE` |

Freshness and invalidation remain defined by the producing Matrix/quality/runtime/policy owners. A source-generation change, stale timestamp, interface/route change, service regression, capacity breach, policy change or Authority expiry returns admission to `UNKNOWN`/`PROBING`. Ping or TCP alone cannot yield `HEALTHY`. This composes `TRANSPORT_HEALTH + SERVICE_HEALTH + TRAFFIC_QUALITY + CAPACITY_HEALTH`; it neither replaces nor duplicates their owners.

## RESET-M10.4 — FINAL_PRIMARY_RUNTIME_BOUNDARY

The deployed primary graph is:

```text
users/egress assignments + exact Core-promotion policy
                         |
                         v
             v7-routing-sync (210 LOC)
                         |
                         v
            nft class maps + ip rules/tables
                         |
                         v
              production client traffic
                         |
                         v
                 kernel verification
```

Admitted decision dependencies are the existing Health Receipt, Policy, Authority, Assignment, Dataplane and Verification contracts. OMP, Reports, Learning, Replay, History, campaigns and certification are absent from the continuous forwarding graph. The current Core-primary apply consumes assignments and the exact promotion contract; movement to a different assignment remains separately gated by the existing governed executor. This preserves Authority instead of inventing an unapproved class-wide switch authority.

## RESET-M10.5 — Engineering Plane extraction

Packaging classes are now explicit:

- `runtime_required`: `v7-routing-sync`, registry readers, exact Core-promotion policy, nft/ip and verify.
- `control_plane_async`: Matrix/quality/runtime observation and existing policy/capacity/Authority facts.
- `fallback_only`: `v7-users-autoswitch`, `v7-user-switch`, Packet/lease/barrier, rollback/recovery and expanded verification. They remain installed because their safety semantics have real consumers, but their services do not own primary forwarding and the autoswitch timer remains inactive/manual.
- `engineering_only`: OMP/CPS reconciliation functions in `v7_sync_lib.py`, Polygon, reports, Learning, Replay, campaign/certification and historical closure machinery.

The large files were not mechanically split: size alone does not justify a new package owner. Their production admission is narrowed by caller and service state, which physically excludes Engineering Plane code from the running primary process without duplicating it.

## RESET-M10.6 — Fast and reconciliation paths

```text
FAST FORWARDING PATH
prepared assignments/policy -> v7-routing-sync -> nft/ip -> verify

GOVERNED FAILURE ACTION
failure event -> prepared Matrix health -> Planner/policy/Authority gates
-> bounded user switch -> verify/rollback -> Core membership reconciliation

ASYNC RECONCILIATION
periodic probes -> Matrix/quality -> audit/outcome -> OMP/reports/learning
```

The first path continuously forwards without the second or third. The governed failure action remains necessary because current Authority is per bounded action, not an implicit class-wide grant. Reports, Learning, Replay, maturity, full inventory and historical reconciliation occur only after/outside apply. Thus the slow Engineering path is not a forwarding prerequisite and no Authority bypass was introduced.

## RESET-M10.7 — Dataplane adapter

Disposition: `KEEP_SIMPLIFIED_EXISTING_ADAPTER`.

The former primary chain built per-user route objects. The current chain is `Core owner -> v7-routing-sync -> nft/ip -> kernel`: one Python process, one lock domain, one atomic nft transaction, six class rules/tables and explicit verification/fallback. Replacing the 210-line adapter would add ownership and migration risk without lowering the synchronous level count. Fencing (single routing lock), idempotent replacement, atomic nft apply, exact Authority, fallback restoration and verify remain intact.

## RESET-M10.8 — Final complexity and cleanup audit

Two baselines are stated to avoid claiming that classification deletes installed fallback code:

| Metric | Pre-Core legacy primary | M10 entry | Final | Final vs legacy |
| --- | ---: | ---: | ---: | ---: |
| primary individualized kernel routing objects | 248 | 12 | 12 | -236 (-95.2%) |
| primary routing processes per reconciliation | legacy Planner/writer chain | 1 | 1 | reduced to one adapter process |
| primary routing adapter LOC | large legacy execution path (23,639-line autoswitch surface admitted) | 210 | 210 | legacy surface excluded from primary |
| active primary autoswitch timers | 1 legacy concept | 0 | 0 | -1 |
| primary pre-apply Engineering Plane hops | multiple audit/reconciliation gates | 0 | 0 | removed |
| primary pre-apply durable writes | Packet/history/closure chain | 0 | 0 | removed |
| primary lock domains | multiple governed domains | 1 routing lock | 1 | bounded |
| primary critical-path subprocess layers | Planner -> writer -> scripts -> kernel | adapter -> nft/ip | adapter -> nft/ip | reduced |
| Reset-added Runtime owners/processes/timers/state surfaces | 0 | 0 | 0 | 0 |

M10 entry-to-final LOC is deliberately `0`: the already deployed minimal adapter was correct, and rewriting it for a numerical delta would violate reuse-first and safety. Whole-production reduction is the combination of M9 physical deletion and M10 proof that 23,639-line autoswitch, 25,380-line synchronization/engineering library, OMP/report/history/campaign surfaces and inactive timers are `LEGACY_SURFACE_NOT_ADMITTED_TO_FINAL_RUNTIME`. They remain installed only where an exact manual/governed safety, deploy/truth or engineering consumer exists.

Cleanup dispositions:

- `STILL_REQUIRED`: compact Core dataplane, assignments, health observation, policy/capacity/Authority, verify.
- `LEGACY_EXCEPTION_REQUIRED`: governed per-user execution, rollback, fallback and recovery; owner-backed removal condition is equivalent bounded Authority plus production rollback/crash proof.
- `ARCHIVE`: historical Programs/reports remain evidence and are not loaded by Runtime.
- `DELETE`: legacy primary kernel objects and any active parallel autoswitch timer; both are absent from final primary state.

`NEW_ARCHITECTURE_COMPLETE = PASS`; `OLD_ARCHITECTURE_CLOSED = PASS`. No superseded import, service, timer, state writer, config entry or old/new primary pair remains undispositioned. The fallback is explicit, not an orphan.

## RESET-M10.9 — FINAL_ARCHITECTURE_MAP

### Runtime and data flow

```text
CONTROL PLANE                                         DATA PLANE
Matrix/quality/runtime health -> EGRESS_ADMISSION_STATE
Assignments + Policy + Capacity + Authority
                    |                                      |
                    +--> bounded decision / current class -+
                                                           v
CLIENT TRAFFIC -> nft user_class -> class route -> interface -> VERIFY
                                                           |
                                                           v
                                                ASYNC OUTCOME/EVIDENCE
                                                           |
                                                           v
ENGINEERING PLANE: OMP / Reports / Polygon / Learning / Replay
```

The forbidden inverse dependency `failure -> reports/analysis -> routing` does not exist in primary forwarding.

### Ownership matrix

| Responsibility | Canonical existing owner | Input -> output | Lifecycle |
| --- | --- | --- | --- |
| channel/service observation | Matrix/quality/runtime-health owners | probes -> fresh facts | Control Plane async |
| admission projection | same existing health owners composed with policy/capacity | facts -> `EGRESS_ADMISSION_STATE` | logical, not stored |
| assignments | existing Assignment owners | user/current egress -> class membership | Control Plane truth |
| routing decision semantics | existing Routing Core / governed Planner owners | admitted facts -> bounded decision | Control Plane |
| Authority | existing policy/operator-execution owners | contract -> legal effect envelope | Control Plane, fail closed |
| route apply | `v7-routing-sync` / Linux kernel | class map -> forwarding state | Data Plane primary |
| verification | existing routing/kernel and governed verification owners | installed state/outcome -> PASS/STOP | Runtime/Data Plane |
| engineering improvement | OMP and existing evidence/learning owners | async outcomes -> change decision | Engineering Plane only |

### Legacy exceptions and delete/revisit list

| Item | Status | Reason / removal condition |
| --- | --- | --- |
| `legacy_sync` builder | `LEGACY_EXCEPTION` | exact Core fallback; remove only after another proven recovery owner exists |
| `v7-users-autoswitch` + governed transaction | `LEGACY_EXCEPTION` | Authority/rollback safety; `NOT PRIMARY`, `NOT CORE DEPENDENCY`, temporary compatibility until equivalent production proof |
| inactive autoswitch service/timer files | `FUTURE_REVIEW` | manual recovery compatibility; timer must remain inactive |
| OMP/reports/history/campaigns | `KEEP` Engineering Plane | real engineering consumers; never Runtime dependencies |
| 248 legacy individualized kernel objects | `REMOVED` | M9 production deletion proof |
| Core class dataplane | `KEEP` | current production consumer and fallback evidence |

### Architectural truth reconciliation

- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`: `CURRENT_ARCHITECTURE_OWNER` only for volatile Runtime/program state.
- `docs/reference/V7_CANONICAL_REFERENCE.md` and `docs/reference/SYSTEM_MAP.md`: `CURRENT_ARCHITECTURE_OWNER` for durable architecture and topology.
- this report and all M0-M9 Engineering Reports: `HISTORICAL_EVIDENCE`.
- completed/superseded Program sections and older diagrams: `OBSOLETE_REFERENCE` when they claim current execution; their evidence remains historical.
- `FINAL_ARCHITECTURE_MAP` is this reconciled projection consumed into the Canonical Reference/SYSTEM_MAP; it is not Runtime state, CPS, Authority or a new owner.

No conflicting current architecture owner was found after the canonical updates. Future architecture changes update the existing Canonical Reference/SYSTEM_MAP before creating another artifact.

## Stage closure and final gates

| Stage | Consumed output | Result / successor |
| --- | --- | --- |
| M10.1 | exclusive placement ledger | PASS -> M10.2 |
| M10.2 | supported boundary benchmark | PASS -> M10.3 |
| M10.3 | owner-backed admission lifecycle | PASS -> M10.4 |
| M10.4 | minimum dependency graph | PASS -> M10.5 |
| M10.5 | package/caller isolation | PASS -> M10.6 |
| M10.6 | fast/governed/async path split | PASS -> M10.7 |
| M10.7 | retained minimal adapter with safety proof | PASS -> M10.8 |
| M10.8 | before/entry/final metrics and cleanup | PASS -> M10.9 |
| M10.9 | canonical final map and document reconciliation | PASS -> completion evaluation |

- `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_PASS = PASS`
- `PRIMARY_SYSTEM_SURFACE_REDUCED = PASS`
- `FINAL_RUNTIME_SIMPLIFICATION_PASS = PASS`
- `FINAL_ARCHITECTURE_MAP_COMPLETE = PASS`
- `END_TO_END_CHANGE_COMPLETION_PASS = PASS`
- `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS = PASS`
- `OLD_FAILURE_CAUSES_NOT_REINTRODUCED = PASS`

Self-review found no Authority expansion, no new Runtime/owner/state, no synchronous Engineering dependency, no hidden duplicate primary writer and no orphaned migration tail. Deep audit evidence remains linked rather than copied. The only retained large surfaces have exact governed fallback, deploy/truth or Engineering consumers and explicit removal conditions.

Runtime effects: `NONE_NEW; EXISTING_CORE_PRIMARY_BOUNDARY_CONFIRMED`.

Production effects: `NONE_NEW; EXISTING_CORE_PRIMARY_FOR_124_USERS_AND_M9_PHYSICAL_SHRINK_PRESERVED`.

Authority effects: `NONE; EXACT_EXISTING_PROMOTION_AND_BOUNDED_ACTION_CLASS_CONTRACTS_PRESERVED`.

Residual: `NONE_FOR_RESET_M10`.

Successor: `FINAL_RESET_PROGRAM_COMPLETION_RECONCILIATION`.

Terminal: `RESET_M10_POST_RESET_SYSTEM_SHRINK_AND_RUNTIME_SIMPLIFICATION_PASS`.
