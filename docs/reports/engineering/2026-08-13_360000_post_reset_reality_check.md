# POST_RESET_REALITY_CHECK_REPORT

Status: `POST_RESET_REALITY_CHECK_COMPLETE`

## 1. Purpose

Bounded read-only verification that the completed `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`, its `FINAL_ARCHITECTURE_MAP`, deployed Runtime and observable production behavior still describe the same system. This report creates no Program, architecture, owner, Runtime, state surface or correction cycle and performs no mutation, deployment, refactor or deletion.

Evidence boundary: fresh `tools/v7-truth-check --all --json`; fresh read-only `tools/v7-safe-deploy --json` production hash/delta; production snapshot `.v7/runtime_convergence_snapshot.json` collected `2026-08-13T10:53:32Z`; existing M8/M9 production apply/fallback/kernel evidence; deployed unit definitions and current source caller/effect inspection. Deep evidence remains with those owners and is not copied here.

## 2. Checked surfaces

- primary routing dependency boundary;
- allowlisted active/inactive production services and timers;
- every deployed routing-capable writer in the canonical package;
- M10 legacy exceptions and Engineering Plane dependencies;
- Assignment, Health, Policy, Capacity, Authority, Routing and Verification state;
- channel admission inputs, freshness and invalidation;
- final map and canonical document status;
- cleanup and natural-traffic residual.

## 3. Expected architecture

```text
CONTROL PLANE
assignments + Matrix/quality/runtime health + policy + capacity + Authority
                              |
                              v
DATA PLANE
v7-routing-sync -> nft user/class maps -> fwmark class routes -> interface -> verify
                              |
                              v
ENGINEERING PLANE (async only)
OMP / Reports / Polygon / Learning / Replay / campaigns
```

Governed autoswitch, per-user switch, Packet/lease/barrier and rollback are explicit bounded exceptions. They are not a continuously active second primary routing loop.

## 4. Actual production reality

Fresh truth result: `FULLY_ALIGNED`, CPS consistency `PASS`, zero contradictions, production Runtime truth `KNOWN`, production access `READY`. Local and GitHub point to `d8a2fa436123bd176522974f9861a2cfc376bbb2`; deployed copied-binary basis remains `b343732248f7f1c25d414c1e140e698d42d1cf62`. The difference is classified `DOCS_ONLY_MISMATCH`, `deployment_required=false`.

Fresh production hashes match the canonical package for `v7-routing-sync`, `v7-user-switch`, `v7-users-autoswitch`, `v7_sync_lib.py`, Routing Core, operator execution, Matrix/quality/sentinel tools, admin/read models and deployed systemd definitions. No runtime binary delta exists.

### Active process/timer evidence

| Process / unit | Purpose | Owner | Layer | Real consumer | Observed status / disposition |
| --- | --- | --- | --- | --- | --- |
| `v7-service-matrix-refresh.timer` | refresh current service/health evidence | Matrix owner | Control Plane | health/admission and governed Planner gates | `active (waiting)`; `KEEP_CONTROL_PLANE` |
| `v7-admin-api.service` | operator/read-model presentation and explicit actions | admin/read-model owners | Control/Engineering presentation | operator/API consumers | `active (running)`; `KEEP_CONTROL_PLANE` |
| `v7-users-autoswitch.service` | explicit governed planning/apply invocation | autoswitch/execution owners | Legacy exception | manual or exact governed action | `inactive (dead)`, approved manual mode; `FALLBACK_ONLY` |
| `v7-users-autoswitch.timer` | former periodic autoswitch entry | autoswitch owner | Legacy exception | no admitted primary consumer | enabled definition but `inactive (dead)`; `DISABLED`, must not become primary |
| intelligence snapshot refresh service/timer | prepared engineering/read-model snapshots | intelligence owners | Engineering Plane | Planner/read models when explicitly called | units not loaded in current snapshot; CLI exists; `KEEP_ENGINEERING`, not background primary |
| `v7-routing-sync` | reconcile/apply class dataplane | routing writer | Data Plane | kernel/client forwarding | executable deployed with matching hash; invoked for explicit reconciliation/restart, not a second daemon; `KEEP_RUNTIME` |

The allowlisted production truth contains no active autoswitch scheduler and explicitly reports `scheduler_inactive_approved_manual_mode=true`. No second primary routing loop was observed.

## 5. Matches

### Primary Runtime boundary

`PRIMARY_RUNTIME_BOUNDARY_REALITY_PASS`.

The actual primary forwarding owner consumes Assignment plus exact Core-promotion Policy/Authority and applies/validates nft/ip state. OMP, Reports, Learning, Replay, Polygon, campaigns, Production Maturity and historical reconciliation are absent from `v7-routing-sync` imports, inputs and apply/verify chain. Matrix and quality are asynchronous Control Plane producers; they do not forward traffic.

### Routing writer ownership

`ONE_PRIMARY_ROUTING_WRITER_PASS`.

| Component | Can mutate routing? | Why / owner | Primary or exception |
| --- | --- | --- | --- |
| `v7-routing-sync` | `YES` | exact Core promotion, atomic nft class apply, ip class route/rule apply, verify and fallback; routing writer owner | `PRIMARY` |
| nft/ip kernel | `YES` | forwarding-state executor consumed by routing writer | `PRIMARY DATAPLANE` |
| `v7-user-switch` | `YES` | exact bounded user assignment/route transaction | `EXCEPTION`; callable only through explicit governed/manual action |
| `v7-users-autoswitch` | `YES` only with apply path | Planner plus Authority/Packet/lease/barrier/verification gates | `EXCEPTION`; service/timer inactive |
| `legacy_sync` inside routing sync | `YES` | deterministic fallback restoration | `FALLBACK_ONLY`, not concurrently active primary |
| Matrix, quality, sentinel, OMP, Reports and Learning | `NO` | observation/engineering producers only | not writers |

Multiple mutation-capable binaries exist by design, but only one is primary; all others have an exact inactive, governed or fallback boundary.

### Engineering Plane isolation

`ENGINEERING_PLANE_ISOLATION_REALITY_PASS`.

OMP/CPS/report/learning/replay functions have real engineering consumers and no import/call edge into the Core dataplane apply. Production failure evidence can be consumed by the governed action path, but Report, Learning and History are post-action outputs rather than prerequisites. Neither forbidden chain `Runtime -> OMP -> routing decision` nor `failure -> Report/Learning/History -> switch` was found.

## 6. Mismatches

No architecture/runtime mismatch was found inside the canonical deploy allowlist and available production truth.

Evidence limitation, not an observed mismatch: the production truth owner exposes a bounded command allowlist rather than an unrestricted host-wide `systemctl list-units`, process and cron census. Therefore this report proves absence of a second primary loop across every canonical/deployed V7 owner and known unit, but does not claim omniscience about unrelated or unregistered host jobs. Owner: existing production truth/convergence owner. Impact: audit completeness wording only; current runtime verdict remains PASS. Correction path if independent evidence appears: extend the existing read-only truth owner after owner review, then targeted recheck; do not reopen Reset automatically.

## 7. Legacy exceptions

| Component | Why retained / real consumer | Owner | Not-primary proof | Removal condition |
| --- | --- | --- | --- | --- |
| `v7-users-autoswitch` | governed fallback, certification, exact action-class execution | Planner/autoswitch and execution owners | deployed hash matches; service and timer inactive/manual | equivalent Authority, rollback, verification and recovery semantics proven in production |
| `v7-user-switch` | bounded per-user apply/rollback primitive | Assignment/execution owner | no continuous unit; reached only by explicit governed/manual transaction | no remaining governed/fallback consumer and replacement semantics proven |
| Packet/lease/barrier and operator execution | fencing, exact Authority, stale/duplicate suppression, crash/rollback safety | operator-execution Authority owner | no forwarding without explicit transaction; not a primary daemon | equivalent safety proof under the same Authority owner |
| old Planner logic | target evaluation and governed exception path | Planner owner | autoswitch loop inactive; Core forwarding does not import it | no fallback/certification consumer and owner-backed retirement |
| `v7_sync_lib.py` | deploy/truth/CPS/OMP engineering lifecycle | deploy/truth and OMP owners | deployed library is not imported by `v7-routing-sync` | split/remove only if existing consumers disappear; size alone is insufficient |
| `legacy_sync` | exact deterministic Core fallback | routing writer | invoked only when exact Core Authority is absent or fallback is explicit | alternative verified fallback/recovery owner exists |

`LEGACY_EXCEPTION_REALITY_PASS`.

## 8. State and channel-health reality

| State | Owner/writer | Readers / real consumer | Lifecycle result |
| --- | --- | --- | --- |
| Assignment | users registry / Assignment owner | Routing Core, routing sync, governed Planner | current -> bounded mutation -> reconciliation; no duplicate owner observed |
| Health | Matrix, service test, quality and runtime probe owners | admission/Planner/admin consumers | refreshed asynchronously; generation/freshness bound |
| Policy | `/etc/v7/policy.json` policy owner | Core promotion and governed gates | exact hash/schema/scope; fail closed |
| Capacity | registry/load/capacity owners | target eligibility and governed Planner | fresh bounded decision; unknown blocks selection |
| Authority | policy plus operator-execution audit | apply gates | exact contract/transaction; no self-expansion |
| Routing | nft/ip kernel via `v7-routing-sync` | production packets and verification | apply -> verify; deterministic fallback |
| Verification | routing sync/kernel plus governed verifier | executor, truth and outcome owners | PASS/STOP/rollback terminal |

No orphan or competing current truth was found in these surfaces. Historical reports are evidence only; CPS is volatile state; Canonical Reference/SYSTEM_MAP own current architecture.

`CHANNEL_HEALTH_MODEL_REALITY_PASS`: existing eligibility logic composes transport/interface evidence, required service Matrix/route-class fitness, quality/stability and capacity/load constraints. It enforces freshness and source-generation binding; stale/missing facts stop or return unknown. Ping/TCP reachability alone cannot satisfy service suitability, quality and capacity gates and therefore cannot produce full admission.

## 9. Final map and cleanup verification

`FINAL_ARCHITECTURE_MAP_REALITY_ALIGNMENT_PASS` within the stated production-truth boundary.

Every mapped canonical deploy component exists with matching production hash. Active Matrix/admin surfaces have the documented Control Plane consumers. Autoswitch remains inactive/manual. The primary Core adapter and fallback binaries match the production package. No missing mapped owner or unexpected canonical runtime dependency was found.

Cleanup dispositions:

- `KEEP`: Core class dataplane, assignments, Policy/Authority, health observation and verification.
- `LEGACY_EXCEPTION`: governed autoswitch/user switch/Packet/lease/barrier/rollback and deterministic fallback.
- `ARCHIVE`: completed Programs and reports; none is live architecture or Runtime truth.
- `DISABLED`: periodic autoswitch timer.
- `REMOVE_CANDIDATE`: none admitted by this check; evidence limitations cannot authorize deletion.

Existing M9 proof remains current evidence that 124 legacy source rules and 124 legacy per-user primary routes were removed and Core verification/fallback passed. No new evidence invalidated it. No orphaned migration tail or hidden old primary path was observed.

## 10. Operational residuals and next actions

1. Natural traffic: the earlier limitation remains—no natural client packet arrived during the bounded nft counter window. This does not invalidate installed class maps, marked route proof, M6 payload proof, fallback proof or current architecture. A future ordinary packet may be observed read-only by the existing routing/kernel verification owner to confirm a class counter increment and selected interface. Do not generate traffic, move users or reopen Reset solely to obtain it.
2. Host-wide census: available production truth is bounded to canonical V7 units/commands. Recheck only if the existing truth owner gains an owner-approved host-wide read-only census or independent evidence names an unregistered V7 process/job.
3. Autoswitch timer: preserve inactive/manual state. Any proposal to enable it is a new operational decision requiring current Policy/Authority/safety review; this report grants none.

Recommended successor: `NONE`. Monitor through existing production truth and ordinary health owners. Re-enter only on an exact mismatch, material safety/correctness gap or owner-backed invalidator.

## Completion

- `PRIMARY_RUNTIME_BOUNDARY_REALITY_PASS`
- `ONE_PRIMARY_ROUTING_WRITER_PASS`
- `ENGINEERING_PLANE_ISOLATION_REALITY_PASS`
- `LEGACY_EXCEPTION_REALITY_PASS`
- `STATE_OWNER_REALITY_PASS`
- `CHANNEL_HEALTH_MODEL_REALITY_PASS`
- `FINAL_ARCHITECTURE_MAP_REALITY_ALIGNMENT_PASS`
- `NO_OBSERVED_ORPHANED_MIGRATION_TAILS`
- `NATURAL_TRAFFIC_OBSERVATION_RESIDUAL_NON_BLOCKING`
- `POST_RESET_REALITY_CHECK_COMPLETE`

Runtime effects = `NONE`.

Production effects = `NONE`.

Authority effects = `NONE`.

Reset terminal remains `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`.
