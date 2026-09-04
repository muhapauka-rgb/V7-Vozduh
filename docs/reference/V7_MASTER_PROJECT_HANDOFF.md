# V7 Vozduh — Master Project Handoff

**Status:** `CURRENT_HANDOFF_REFERENCE`
**Purpose:** self-contained working memory for a new engineering context, not a short report. It deliberately preserves enough causal history that a new agent need not reconstruct this project from chats.
**Reconstructed:** 2026-08-18
**Architecture owner:** `docs/reference/V7_CANONICAL_REFERENCE.md`
**Topology owner:** `docs/reference/SYSTEM_MAP.md`
**Volatile current-state owner:** `docs/programs/V7_CURRENT_PROGRAM_STATE.md` (CPS)
**Evidence rule:** reports are historical evidence; they are not live Runtime truth.

## Read this first

This document explains V7 and the reason for its current shape. It is not a
new Runtime, Planner, queue, registry, Authority, or source of truth. Before
any action, read CPS Section 0 and verify the exact current successor.

Resolution order:

```text
Current CPS for volatile state
  > Canonical Reference for durable meaning
  > SYSTEM_MAP for owner topology
  > fresh owner-backed Runtime observation
  > Engineering reports and historical evidence
  > this handoff
```

Facts are marked **CURRENT**, **HISTORICAL**, **SUPERSEDED**, or **PENDING
PROOF**. A report, test, commit, deployment, screenshot, or graph is never by
itself proof of a caller, consumer, Runtime effect, production effect, or
Authority grant.

---

# 1. Project essence

V7 Vozduh is a multi-egress Internet/VPN routing system. A client has one
stable ingress, while V7 selects among independent egress channels. It keeps a
sticky assignment while a channel is healthy, detects a real loss of
usability, selects a healthy lawful target for only the affected users, changes
routing safely, and verifies that traffic actually recovered.

```text
BAD / UNUSABLE CHANNEL
  -> FAST CONFIRMED FAILURE
  -> AFFECTED USERS
  -> HEALTHY, LAWFUL TARGET
  -> SAFE SWITCH
  -> VERIFIED CLIENT TRAFFIC RECOVERY
```

The egress families historically used by V7 include VLESS Reality / sing-box,
AmneziaWG, WireGuard, OpenVPN, and Direct/RU where relevant. A live TCP socket
or ping is not enough to call a channel healthy: V7 needs current service,
routing, capacity, policy, and safety evidence appropriate to the action.

The principal product KPI is:

```text
T0 FAILURE CONFIRMED -> T11 CLIENT TRAFFIC RECOVERED
```

It is **not** the time to create reports, OMP receipts, learning records, or
historical evidence. Those may consume the result after the switch.

---

# 2. Product philosophy and non-negotiables

| Law | Practical meaning |
| --- | --- |
| Stability before movement | A healthy sticky assignment is retained; a nominally better target is not a reason to churn. |
| Fail closed | Unknown, stale, conflicting, or incomplete facts cannot cause a blind route mutation. |
| No flap | Hard failure, soft degradation, recovery, cooldown, user freeze, target block and pair-reversal are distinct controls. Recovery is deliberately slower than failure. |
| One owner | Every durable responsibility has one existing owner; hidden duplicate truth is forbidden. |
| Evidence of real effect | Code/tests/reports/deployments are insufficient without actual caller, consumer and outcome evidence. |
| Engineering outside Runtime | OMP, reports, Polygon, replay, learning, campaigns and audits cannot synchronously gate a live switch. |
| Controlled is not natural | Controlled L7 evidence is useful but cannot be presented as natural L8 production evidence. |
| Do not wait unnecessarily | A blocked external proof does not pause an independent safe and admitted work item. |

Packet, lease, restore barrier, rollback, verification and Authority are not
bureaucratic layers. They prevent stale actions, duplicate/concurrent movement,
unsafe partial changes, wrong targets, unrecoverable state, and uncontrolled
blast radius. Simplification removes redundant work **around** them; it does
not delete a safety contract just because it has multiple steps.

---

# 3. Scale and product target

The primary future-scale target is **10k+ users / 50+ egresses**. Larger
claims require fresh owner-backed proof.

Implications:

1. Health processing must scale by egress and role, never by all users per
   sample.
2. Routing state must use semantic classes/buckets where applicable, not an
   O(N) per-user rewrite for a channel event.
3. Work per decision is bounded to the affected cohort and action class.
4. The hot path must not scan the full historical universe to answer a current
   question.
5. Target freshness, capacity, policy, Authority, rollback and verification
   remain necessary even for a small cohort.

---

# 4. Architecture planes

| Plane | Responsibility | Main existing components | May do | Must not do |
| --- | --- | --- | --- | --- |
| **Management Plane** | Guarded operator and Admin interfaces. | `admin/v7-admin-api`, `admin_core.operator_views`, diagnostic views. | Present state; call an already guarded operator workflow. | Select a live target, bypass auth/RBAC/CSRF/safe-mode, or write routes. |
| **Control Plane** | Health, source scope, policy, capacity, admission, decision semantics, recovery and Authority inputs. | Matrix/service-health, L3 projection, Planner/policy/assignment/capacity owners. | Produce fresh decision facts. | Own forwarding or make reports into Runtime truth. |
| **Data Plane** | Narrow forwarding apply, kernel state, visibility and verification. | `admin_core/routing_core.py`, `v7-routing-sync`, nft maps, fwmark rules, class route tables. | Apply an already lawful bounded decision and verify it. | Run OMP/history/learning/campaigns or a parallel planner. |
| **Engineering Plane** | OMP, CPS lifecycle, reports, Polygon, research, replay, learning, audits and certification. | OMP, CPS reconciliation, report owners, Polygon. | Observe outcomes asynchronously and improve the system. | Be a synchronous prerequisite for live forwarding or self-grant Authority. |

Allowed dependency:

```text
Control fresh facts -> bounded decision -> Data apply -> kernel/user verification
Engineering <- asynchronous outcome/evidence
```

Forbidden dependency:

```text
failure -> OMP / reports / history / learning / campaign -> routing
```

`FINAL_ARCHITECTURE_MAP` is a decision/onboarding projection. It is not a new
CPS, Runtime state store, owner, or Authority source. `SYSTEM_MAP` owns its
compact current topology.

---

# 5. Routing Core Reset — why it happened

## Historical legacy reality

| Historical measure | Observation | Consequence |
| --- | ---: | --- |
| Successful governed forward path | ~58.76 s | Too slow for a failure response. |
| Kernel mutation plus visibility | ~0.878 s | Kernel apply was not the primary bottleneck. |
| No-action lifecycle | ~289–322 s | Even no-move work accumulated excessive orchestration. |
| Direct executable surface | ~41.8k LOC | Too much mutable logic sat close to routing. |
| Reachable routing/safety/governance surface | ~85.9k LOC | Excess surface amplified ownership and latency risk. |
| Pre-apply producer/consumer hops | >=9 | Too many synchronous handoffs before apply. |
| Pre-apply state surfaces | >=17 | Reconciliation/staleness risk grew with every surface. |
| Durable writes before apply | >=6 | Coordination work dominated a narrow operation. |
| Historical routing pattern | O(N) user-registry/routing work where applicable | Not compatible with future scale. |

### Causal verdict

```text
legacy routing was slow
  -> measurement proved kernel apply was fast
  -> orchestration, governance, history and repeated reconciliation were slow
  -> introduce a minimal Routing Core beside legacy
  -> migrate only through evidence and freeze legacy capability growth
  -> make class routing primary
  -> optimise above Data Plane without deleting necessary safety
```

The durable laws are:

```text
LEGACY_V7_ROUTING_HOT_PATH = FROZEN_FOR_CAPABILITY_GROWTH
NEW_CORE_EARNS_AUTHORITY_THROUGH_EVIDENCE
```

**CURRENT:** Reset M0–M10 are complete according to CPS and Canonical
Reference. Old text claiming RESET-M0 was next is **SUPERSEDED**; never reopen
the Reset sequence without an exact invalidation trigger.

---

# 6. Core-primary current architecture

The primary data-plane boundary is intentionally narrow:

```text
Assignment + exact Policy/Authority facts
  -> Routing Core decision representation
  -> v7-routing-sync
  -> nft class map / fwmark rule / class route table
  -> kernel visibility and route verification
```

`admin_core/routing_core.py` represents bounded Core semantics;
`/usr/local/bin/v7-routing-sync` is the class-routing apply/restart owner. nft
membership provides address-to-class indexing. It is not one routing decision
per user.

| Primary routing object class | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Individualized/class routing objects | 248 | 12 | -236 (-95.2%) |

The retained 124-member nft map is required membership indexing, not 124 route
tables or decisions. A class target switch remains one bounded class-table
update.

**CURRENT production authority:**

```text
CORE_PRIMARY_FOR_124_COMPATIBLE_PRODUCTION_USERS_WITH_EXACT_LEGACY_FALLBACK
```

The governed `v7-users-autoswitch` / `v7-user-switch` / Packet / lease /
barrier chain is a bounded fallback/Authority exception. It cannot regain
parallel continuous primary routing authority without new evidence and legal
promotion.

---

# 7. Current failover hot path

The intended synchronous product chain is:

```text
FAILURE SIGNAL
  -> canonical current health/source event
  -> current affected scope
  -> ordinary-only bounded selection where applicable
  -> Candidate
  -> Packet
  -> lease
  -> restore barrier
  -> route apply
  -> route visibility
  -> selected-user / required-route verification
  -> service verification
  -> CLIENT TRAFFIC RECOVERED
  -> minimal durable terminal
```

| Stage | Owner role | Why it exists |
| --- | --- | --- |
| Matrix failure episode | Existing Matrix health/event owner | Converts confirmed failure into one canonical current fact. |
| Current affected scope | Existing L3/current-scope owner | Bounds users; prevents a global scan/move. |
| Candidate | Existing policy/Planner owner | Binds source, target, cohort, policy and fresh facts. |
| Packet | Existing governed execution owner | Freezes exact scoped intent; blocks widening/staleness. |
| Lease | Existing lease owner | Prevents duplicate/concurrent execution. |
| Restore barrier | Existing recovery owner | Fences apply and preserves recoverability. |
| Apply | Routing Core or explicit governed writer | One lawful mutation boundary. |
| Verification | Existing route/service/user verification owners | Proves traffic effect rather than process exit. |
| Minimal terminal | Existing lifecycle owner | Records outcome without turning history into a prerequisite. |

Outside the KPI:

```text
OMP receipt, reports, history, learning, replay, analytics,
campaigns, certification tail, extended evidence projections
```

These are asynchronous consumers. They may not select, authorise, gate, or
delay a fresh Runtime switch.

---

# 8. Failure detection and health architecture

## Current verified reality

| Check | Cadence / trigger | Current owner/output | Role |
| --- | --- | --- | --- |
| Telegram fast sentinel | every 4 s; 1 s timeout; 14 s sustained-failure threshold | Existing Matrix input/event owner | Fast Telegram-specific confirmation input, not route writer. |
| Full service Matrix | every 15 min plus up to 60 s random delay | Matrix current state and passive event capture | Deep diagnosis, service quality and broad current state. |
| Per-egress service test | Matrix invokes `v7-service-matrix-test`, 14 services | Atomic Matrix row update | Protocol/application reachability. |
| Target health/capacity | Existing Matrix, quality and capacity owners | Planner admission input | Lawful target selection, not source detector. |

The full Matrix currently iterates enabled egresses serially. Within an egress,
services already run bounded-parallel (maximum eight workers). Recent production
receipts for seven egresses measured **54.314–80.153 s wall**, ~7–8 s CPU and
~100 MiB peak RSS; the slowest egress took ~17–19 s. The long wall/low CPU
ratio and near-sum of egress times prove network waits and serial egress
traversal, not a need for uncontrolled inner parallelism.

## Fast + deep target model — PENDING IMPLEMENTATION

```text
existing fast protocol-specific source signal
  -> existing Matrix confirmation and canonical failure episode
  -> current affected ordinary scope
  -> existing decision/execution path

full Matrix, quality/capacity detail, OMP, reports, learning, replay
  -> existing asynchronous owners
```

No second Matrix, watcher, daemon, queue, Planner, state store, event type or
route writer is warranted. The next bounded admission is:

```text
V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1
```

It must prove an existing minimal service subset and role-scoped egress set,
single Matrix writer, current source/target truth, persistence/anti-flap,
stale-evidence fail-closed behavior and full-Matrix fallback.

## Health semantics

Logical admission is:

```text
UNKNOWN -> PROBING -> HEALTHY -> DEGRADED -> UNUSABLE -> RECOVERING -> HEALTHY
```

It is a non-stored `EGRESS_ADMISSION_STATE` projection from fresh transport,
required-service, traffic-quality and capacity facts.

| State | Meaning | Consequence |
| --- | --- | --- |
| `WORKING` / `HEALTHY` | Fresh relevant evidence supports use. | Candidate may consider it only if policy/capacity/Authority also pass. |
| `DEGRADED` | Partial or service-specific warning. | Not itself an automatic ordinary move. |
| `NOT_WORKING` / `UNUSABLE` | Hard failure meets existing persistence rules. | May publish a canonical Matrix episode. |
| `UNKNOWN` | Missing/stale/conflicting/timed-out evidence. | Fail closed; never invent a failure. |
| `RECOVERING` | Improved evidence under recovery safeguards. | Needs existing recovery/anti-flap admission before reuse. |

---

# 9. Hot-path accelerations already implemented

This table preserves causal history. Measurement is historical unless a fresh
owner revalidates it; do not repeat closed audits ceremonially.

| Problem -> observation | Change | Why safe | Result/status |
| --- | --- | --- | --- |
| Full passive-event history read before bounded work. | Bounded event-ledger tail reading and existing consumption compaction. | Same newest logical window; exact re-entry retained. | Execution ledger ~3439 -> ~158 ms (-95.4%); L3+ledger ~3822 -> ~251 ms (-93.4%). Implemented/deployed. |
| L3 retained history grew; stale in-memory data could overwrite reconciled state. | Persist compaction before reconciliation; bounded passive source window. | No new state/owner; reconciliation sees current L3. | L3 27.27 -> 10.43 MiB (-61.8%); consumptions 37,783 -> 1,997 (-94.7%). Implemented/deployed. |
| Repeated all-incident and parent reconciliation. | Current-state/outcome filtering and retained-history compaction. | Required safety rechecks retained. | All-incident refresh ~8307 -> ~292 ms (-96.5%); parent reconciliation ~10912 -> ~3278 ms (-70%). |
| Advisory planning repeated a scope check without consumer. | Remove proven redundant entry recheck; retain post-plan safety checks. | Exact consumer proof; not a planner bypass. | Removed ~12 s span; retained post-plan recheck ~9.489 s. |
| OMP/certification work mixed with Runtime predecessor. | Direct-L3-first, passive-reconciliation deferral, receipt-bound OMP decoupling. | OMP still consumes outcome asynchronously. | Event-only consumer moved from historic ~70–91 s / ~1–1.5 GiB to ~0.9–1.8 s / ~100 MiB where hot-path-only applies. |
| Mixed ordinary/certification scope. | Accounting repair, scope generation/revalidation, selection fence and bounded ordinary cohort. | Certification cannot leak to generic path. | Current proven bound is max 4 where current policy supports it. |
| Redundant pre-Planner refresh. | Removed only from direct path. | Existing decision/target checks remain. | Bounded exact-user snapshot near ~173 ms where evidenced. |
| Writer/verifier ambiguity. | Bounded failure classification. | Writer and verification owners unchanged. | Better STOP_SAFE diagnosis; no claimed move. |

These results do **not** prove a fresh ordinary `T0 -> T11` receipt. Recent
observed source scopes were not actionable ordinary work; no synthetic user
movement was fabricated.

---

# 10. Governed execution safety model

```text
Candidate -> Packet -> lease -> restore barrier -> apply -> verify -> rollback/closure
```

| Contract | Prevents | Simplification rule |
| --- | --- | --- |
| Candidate | Wrong source/target/cohort or stale policy facts. | Remove duplicate discovery, never make an ad hoc target selector. |
| Packet | Later branch widening/reinterpreting action. | Keep immutable exact intent. |
| Lease | Concurrent/replayed movement. | Avoid redundant pre-work; retain mutual exclusion. |
| Restore barrier | Unsafe interleaving or partial recovery. | Keep fencing while moving noncritical history outside. |
| Apply | Multiple route writers. | One existing writer for the action class. |
| Verification | Command exit falsely treated as traffic recovery. | Verify kernel path and required user/service outcome. |
| Rollback/closure | Stranded client or hidden partial failure. | Keep recovery/terminal consumer; reports remain post-action. |
| Authority | Engineering convenience expands action class/blast radius. | Never self-issued by code, OMP, Polygon, or report. |

---

# 11. Ordinary users versus certification scope

| Class | Meaning | Lawful use |
| --- | --- | --- |
| **Ordinary** | Real customer assignment eligible for the defined automatic action class. | Product failover and client-recovery KPI once all owners pass. |
| **Certification** | Controlled engineering identity/scenario. | Controlled L7 proof via existing controlled-production and Authority owners. |

A source can contain both. The ordinary denominator counts ordinary identities
only. A controlled marker does not globally relabel all historical scope.
Before Packet, the fence must show:

```text
selected identity is ordinary for this action class
  OR explicitly approved controlled certification
```

If a generic ordinary selection contains certification, it stops safe before
Packet. The max-four ordinary bound is not a general licence to move four
arbitrary users.

## CURRENT VLESS eligibility, 2026-08-18

Fresh owner-backed observation found VLESS is a controlled-certification source,
not an ordinary assignment pool. Its sole assigned identity is disabled, Admin
showed zero users, and its controlled reservation is expired. The existing
governed preflight correctly returned:

```text
STOP_SAFE_NO_ELIGIBLE_LIVE_VLESS_USER
```

No Packet, lease, barrier, route, user movement or Authority change occurred.
The required predecessor is a fresh existing controlled-source lifecycle with
an enabled managed identity, unexpired exact reservation and independent
Authority approval. Direct registry editing/revival would create synthetic
assignment and is forbidden.

### SUPERSEDED VLESS conflict

CPS captured on 2026-08-14 includes an older VLESS line with `affected=40`.
Fresh 2026-08-18 Runtime observation is certification-only with zero enabled
eligible users. Do not average the two. The old line is
`SUPERSEDED_OR_REVALIDATION_REQUIRED` for present VLESS eligibility until CPS
publishes a coherent fresh projection.

---

# 12. Polygon and controlled L7

Polygon is an Engineering Plane scenario selector and controlled validation
corpus. It is not a Runtime executor, truth source, Packet/lease/barrier owner,
failure detector or Authority issuer.

```text
Polygon scenario selection
  -> existing Controlled Production owner
  -> independent Authority decision
  -> fresh Matrix/current state
  -> Candidate -> Packet -> lease -> barrier -> apply -> verify
  -> controlled receipt plus rollback/restoration where required
```

`L7 controlled != L8 natural`. A consumed natural exact-once incident cannot
be replayed as fresh production movement. Do not repair a bad source merely to
manufacture a timing proof. Current controlled work must follow the latest
controlled owner’s exact blocker/successor, including one-user substrate,
shared failure-domain and duplicate-domain constraints.

---

# 13. No-unnecessary-waiting

Natural L8 absence does not prevent read-only profiling, lawful controlled L7,
replay/emulation labelled non-natural, tests, or independent bounded code work.
It never permits fake natural evidence, reuse of consumed incidents, moving an
ordinary customer only for timing proof, self-approved Authority, scope
expansion, or bypassing unknown ownership. A real wait is legal only when no
independent safe frontier remains.

---

# 14. Responsibility map

| Cluster | Current owner/component | Input -> output | Mutation | Plane | Why it exists |
| --- | --- | --- | --- | --- |
| Fast signal | `tools/v7-telegram-sentinel` | TCP observations -> Matrix input | Matrix path only | Control | Fast Telegram evidence; never route writer. |
| Matrix health | `v7-service-matrix-refresh-all` / `v7-service-matrix-test` | probes -> Matrix/events | Matrix state under existing lock | Control | Canonical health/current failure fact. |
| Current scope | L3/runtime projection owner | event -> bounded scope | L3 projection | Control | Prevents global user selection. |
| Decision | Existing Planner/policy/assignment owners | scope/health -> Candidate/stop | owner-defined decision state | Control | Lawful source-target-action binding. |
| Routing Core | `admin_core/routing_core.py` | class decision -> Core plan | representation | Data | Narrow class routing semantics. |
| Route writer | `v7-routing-sync` | Core apply -> nft/ip/kernel | yes | Data | Single primary class-routing writer. |
| Governed fallback | autoswitch/user-switch/operator execution | action -> Packet/lease/barrier/apply | yes, exact contract | Control/Data exception | Retains governed safety/fallback. |
| Verification | route/service/user owners | apply -> outcome | terminal evidence as owned | Data/Control | Proves real effect. |
| Admin | `admin/v7-admin-api`, views owners | query/action -> operator response | guarded only | Management | Interface, not routing authority. |
| Controlled source | existing controlled-cert owner | scenario -> controlled eligibility | controlled lifecycle | Engineering/Control | Lawful L7 substrate. |
| Polygon | existing Polygon owner | corpus -> scenario selection | no direct runtime mutation | Engineering | Controlled proof, not execution. |
| OMP | OMP program owner | evidence/programs -> engineering lifecycle | no route authority | Engineering | Continuation/simplification discipline. |
| CPS | `V7_CURRENT_PROGRAM_STATE.md` | legal transition -> volatile frontier | state projection | Engineering | Single volatile program-state owner. |
| Canonical docs | Canonical Reference / SYSTEM_MAP | conclusions -> durable meaning/topology | docs only | Engineering | Permanent architecture knowledge. |
| Reports | report owners | evidence -> historical record | no Runtime authority | Engineering | Provenance only. |

---

# 15. State ownership map

| State | Writer | Reader | Purpose | Hot path | Historical status |
| --- | --- | --- | --- | --- | --- |
| Matrix current state/service episodes | Matrix owner | policy/scope/Planner | Fresh health/failure | required source fact | current plus receipts |
| L3 projection | L3/autoswitch owner | direct handoff/decision | current affected scope/lifecycle | current scope only | compacted retained history |
| Service-failure ledger | event owner | bounded consumers | event/re-entry provenance | bounded tail only | historical retained |
| Execution events/outcomes | execution owner | closure/learning | outcome lineage | minimal terminal | historical retained |
| Closure records | closure owner | re-entry/learning | completion/re-entry | not generic precondition | historical retained |
| Routing/kernel state | Data writer/kernel | verifiers | actual forwarding | apply/verify | operational |
| Registry/assignment | registry owner | policy/Planner/Admin | identity/stickiness | input only | durable current |
| Packet/lease/barrier | governed owners | apply/rollback | exact action/fencing | governed action | receipts retained |
| CPS | current-state owner | OMP/engineering | volatile frontier | never routing fact | older snapshots historical |
| References/reports | document owners | engineers | durable/history knowledge | never runtime state | reference/evidence |

Current state answers a present decision. Immutable history answers why and
supports exact re-entry. Evidence completeness never requires copying all
history into a current hot-path document.

---

# 16. Evidence and truth hierarchy

1. **Fresh Runtime observation** — actual present process/state under its owner.
2. **CPS** — active programme/frontier/successor.
3. **Canonical Reference** — durable architectural meaning.
4. **SYSTEM_MAP** — owner topology.
5. **Engineering reports** — historical evidence and before/after results.
6. **Generated graph** — navigation only, never caller/state/effect proof.

Before reuse, an existing owner must classify an object as:

```text
VALID | REVALIDATION_REQUIRED | HISTORICAL | SUPERSEDED | RETIRED | NOT_APPLICABLE_WITH_REASON
```

Knowledge maturity does not grant execution Authority. A deployed hash does
not prove runtime consumption. Polygon evidence does not become Natural L8.

---

# 17. Mission, OMP and CPS model

```text
candidate discovery
  -> existing-owner admission
  -> CPS atomic projection where required
  -> MISSION_EXECUTION_ALLOWED
  -> implementation
  -> validation
  -> consumer migration and residue closure
  -> BEFORE / AFTER / DELTA
  -> safe deploy when applicable
  -> controlled or production observation
  -> Engineering Report
  -> exact successor
```

An admitted Mission proceeds through its full internal lifecycle without
returning after every micro-step. Stop only at real safety, Product Contract,
Authority, ownership, missing-evidence or exact external-dependency boundary.

Unrelated residuals do not globally freeze a bounded Mission. Each residual is
classified:

```text
RELATED_TO_MISSION -> block
ORTHOGONAL_TO_MISSION -> continue only with isolation proof
```

This does not claim the predecessor phase complete and does not bypass CPS.
OMP orchestrates Engineering work; it is not a production switch process.

---

# 18. Reuse-first and simplification laws

```text
SEARCH EXISTING
  -> REUSE
  -> MERGE
  -> SIMPLIFY
  -> MOVE
  -> REMOVE DUPLICATE
  -> CREATE ONLY IF A PROVEN GAP REMAINS
```

Controlling rules include:

- `EXISTING_CAPABILITY_DISCOVERY_BEFORE_IMPLEMENTATION`;
- `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER`;
- `END_TO_END_MIGRATION_CLOSURE`:
  `CURRENT -> TARGET -> TRANSITION -> NEW CONSUMER -> VALIDATION -> OLD PATH CLOSED`;
- `NO_REMOVAL_WITHOUT_CONSUMER_AND_RESIDUE_PROOF`;
- `NO_UNDISPOSITIONED_ORPHANED_SURFACE`;
- `PRESERVE_REQUIRED_BEHAVIOR_NOT_LEGACY_STRUCTURE`;
- `FILE_SIZE_IS_A_SIGNAL_NOT_A_VERDICT`;
- risk-proportional evidence depth;
- `REPORT_DEPTH_WITHOUT_REPORT_BLOAT`;
- physical removal is distinct from logical Runtime exclusion;
- meaningful changes record files/functions/dependencies/state/runtime/routing
  before/after/delta.

No generic split of `v7_sync_lib.py`, broad autoswitch rewrite, Core v2,
parallel Planner, health truth, queue, or worker is justified by size or taste.
It needs an existing-owner gap and admitted real consumer proof.

---

# 19. Completed work that is not the current frontier

| Work | Status | Do not restart because |
| --- | --- | --- |
| Reset M0–M10 / Core-primary migration | Complete in CPS/Canonical Reference | Reuse final architecture; reopen only on exact invalidation. |
| Evidence-repository retention cleanup | Done; optional future cleanup | Retention must not replace system optimisation. |
| Admin transparent wrapper collapse | Done | Useful Mission proof, no direct failover-latency result. |
| Small Admin wrapper removals | Done where consumer proof passed | Not a generic deletion campaign. |
| Broad `v7_sync_lib.py` split | Not generically admitted | Size/mixed history alone do not justify it. |
| Broad autoswitch rewrite | Not admitted | Needs measured migration proof. |
| Legacy package deletion | Later only after consumer migration | Runtime exclusion is not deletion. |

---

# 20. Known test/fixture debt

Some historical service-failure suites encode old CPS/frontier assumptions.
They can fail unchanged against a baseline. Classify failures precisely:

| Failure | Treatment |
| --- | --- |
| Violates current behavior or Mission contract | Regression blocker. Stop/repair/revert. |
| Expects a superseded CPS state and reproduces unchanged on baseline | Record as historical fixture debt; keep focused target validation. |
| Reveals unknown caller, writer, consumer, safety or Authority edge | Real blocker until owner-backed resolution. |

Never blanket-waive failures, but never turn a stale unrelated fixture into an
infinite block on a proven bounded change.

---

# 21. Current performance board

| Segment | Historical/current measurement | Status | Next work |
| --- | --- | --- | --- |
| Telegram detection | 4 s cadence + 14 s threshold + 1 s probe | Fast signal only for Telegram | Preserve confirmation; measure lawful event. |
| Generic / Google / VLESS detection | full Matrix 15 min + random delay, then serial 54–80 s sweep | Principal detection frontier | Fast source/target Matrix admission. |
| Event-only consumer | historic ~70–91 s/~1–1.5 GiB; hot-only ~0.9–1.8 s/~100 MiB | Major downstream improvement | Re-measure on fresh ordinary action. |
| Passive history | large full scans -> bounded/compacted | Improved | Reuse. |
| Certification advisory | 57–63 s; prepared decision ~23 s plus materialization | Slow but non-actionable work | Do not generic-bypass without lineage proof. |
| Current-state snapshot | near ~173 ms where evidenced | Improved segment | Include in full receipt. |
| Candidate / Packet / lease / barrier | existing safety chain, no fresh eligible VLESS action | Pending proof | Observe only lawful fresh action. |
| Route apply/visibility | historical kernel ~0.878 s; Core primary | Current architecture, fresh receipt pending | Measure selected action. |
| User/service verification | product-required | pending eligible action | Pending proof | Observe selected action. |
| Background finalization | old lifecycle could be minutes | separated where hot-only applies | Outside KPI | Keep asynchronous. |

No generic programme percentage is a latency proof. A real result is a fresh
segment-by-segment `T0 -> T11` receipt.

---

# 22. Do not do

- Do not put OMP, reports, history, learning, replay, campaign or analytics
  into the synchronous switching path.
- Do not create another Core, Planner, Matrix, health truth, queue, worker,
  registry or Runtime merely to defer work.
- Do not use controlled certification users as ordinary users.
- Do not call current Matrix certification-only status terminal closure for all
  historic incidents.
- Do not repair a bad egress to manufacture a performance proof.
- Do not replay consumed natural events as new production movement.
- Do not bypass Admin/auth/CSRF/RBAC/safe-mode/Authority or safe deploy owners.
- Do not count a report/commit/test/deploy as Runtime completion.
- Do not treat logical Runtime exclusion as physical file deletion.
- Do not wait for natural evidence while independent controlled/read-only work
  is legally ready.

---

# 23. New-context startup procedure

1. Read this handoff.
2. Read CPS Section 0: capture active programme, stage, successor, Mission and
   generation.
3. Read Canonical Reference and SYSTEM_MAP for the scope.
4. Verify freshest owner-backed Runtime observation; do not use old reports as
   live state.
5. Find exact invalidation triggers; reuse already closed evidence otherwise.
6. State `CURRENT FACTUAL STATE`, `CURRENT BLOCKER`, `NEXT EXECUTABLE ACTION`,
   owner, re-entry condition and needed evidence.
7. Execute an admitted scope through closure; otherwise do only the smallest
   required admission/reconciliation.
8. Save one compact Engineering Report after meaningful work; update an
   existing canonical owner only when durable meaning changed; compute next
   frontier.

---

# 24. Current active programme, blockers and next action

This is a startup summary, **not a substitute for live CPS/runtime checks**.

```ini
ACTIVE_PROGRAM = V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1
CURRENT_STAGE = RS6_RUNTIME_PACKAGE_MINIMIZATION
CURRENT_CPS_SUCCESSOR = EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION
CURRENT_CPS_FRONTIER = ADMITTED_READY_READ_ONLY:V7_OMP_BDP_65CB2232971BC224D937140C_V1
ACTIVE_MISSION = V7_OMP_BDP_65CB2232971BC224D937140C_V1
MISSION_STATE = ADMITTED_READY_READ_ONLY (CPS snapshot 2026-08-14; revalidate)

CURRENT_PRODUCT_FRONTIER = lawful acceleration of FAILURE CONFIRMED -> CLIENT TRAFFIC RECOVERED
CURRENT_RUNTIME_BLOCKER = generic/Google/VLESS detection still depends on 15-minute full Matrix cadence plus serial egress probing
CURRENT_EXTERNAL_BLOCKER = VLESS has zero enabled eligible live user and expired controlled reservation; fresh existing lifecycle plus independent Authority are required
CURRENT_VLESS_ELIGIBILITY = STOP_SAFE_NO_ELIGIBLE_LIVE_VLESS_USER
CURRENT_VLESS_CPS_40_USER_CLAIM = SUPERSEDED_OR_REVALIDATION_REQUIRED

NEXT_EXECUTABLE_ACTION = V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1
NEXT_ACTION_OWNER = existing Matrix/service-health and source/target eligibility owners
PARALLEL_READY_ACTIONS = independent RS6 read-only or Engineering/Management work only after owner/conflict check
NATURAL_EVIDENCE_PENDING = fresh lawful ordinary L8 failure-to-client-recovery receipt; never manufacture it
CONTROLLED_EVIDENCE_STATE = controlled L7 only through existing Controlled Production owner plus independent Authority; current VLESS lane remains STOP_SAFE
```

The next action is admission only. It must prove the existing Matrix owner can
use a minimal protocol-specific service subset for active ordinary sources and
eligible targets, while preserving one Matrix writer, existing failure event,
persistence/anti-flap, stale fail-closed behavior, no O(N user) loop and full
Matrix fallback. If not, stop safe with exact missing owner/evidence and
re-entry condition; do not build a second health system.

---

# 25. Provenance

This handoff synthesizes rather than copies:

- `docs/reference/V7_CANONICAL_REFERENCE.md` — durable meaning/truth hierarchy;
- `docs/reference/SYSTEM_MAP.md` — planes and owner topology;
- `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` — locked knowledge;
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md` — live CPS snapshot;
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` — OMP/admission/simplification laws;
- Reset program and `V7_SYSTEM_RESET_CONSOLIDATED_3_PRODUCTION_MIGRATION_AND_COMPLETION.md` — Core causal history and 248 -> 12 measured routing-object shrink;
- hot-path baseline, cost-tree and current-state-compaction reports — observed
  latency, OMP separation and deployed reductions;
- local 2026-08-18 VLESS eligibility and detection/health optimisation evidence.

When sources have different current-looking claims, this document labels old
claims `SUPERSEDED` or `REVALIDATION_REQUIRED` rather than averaging them.

---

# 26. 2026-09-04 — Agentic Engineering And Code Optimization Delta

**Update mode:** `ADDITIVE`
**Old handoff content removed:** `NO`
**Evidence status:** local read-only Engineering evidence; CPS/Canonical
acceptance is not inferred from a report or proof alone.

## CURRENT — product frontier supersession

Section 24 is preserved as its stated 2026-08-14 CPS snapshot. Its active
programme, RS6 stage and Matrix-probe successor are:

```text
SUPERSEDED_BY_CURRENT_FACT:
ACTIVE_PROGRAM = V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1
CURRENT_PROGRAM_EXECUTION_FRONTIER = V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE
CURRENT_EXECUTION_MISSION_STATE = MISSION_ACTIVE
CURRENT_COMPLETION_CONTRACT = RECOVERY_LATENCY_SLO_PRODUCT_CONTRACT
```

The current product clock remains the CPS/contract-owned recovery interval
from `T_FIRST_VALID_FAILURE_OBSERVATION` to the last affected required S11.
Agentic Engineering and Code Optimization work neither replace nor execute
this product frontier.

## CURRENT — agentic Engineering direction

Do not build a separate Agent System. The governing sequence is:

```text
DISCOVER -> REUSE -> EXTEND -> IMPLEMENT
```

AI-assisted roles are bounded Execution/Review profiles inside the existing
OMP Engineering boundary. They are not owners, Programs, Planners,
Coordinators, CPS frontiers, truth sources, Runtime services or persistent
agents. The durable chain remains:

```text
Product goal -> V7 Program -> CPS/OMP -> current frontier
  -> bounded profile -> code/test/evidence -> existing completion/residual consumer
```

The existing-owner capability audit verdict was
`EXTEND_EXISTING_EXECUTION_CONTRACT`: no new Coordinator, Agent Frontier,
Function Graph owner, Program, OMP/CPS, Runtime truth owner or persistent
state was admitted.

## CURRENT — bounded profile evidence

The original admitted profile remains `GPT_DECISION_REVIEW`. It binds exact
Mission/run/profile/input/repository identity, a read-only tool class and the
existing completion consumer. Its independent-review proof level remains
`SCHEMA_CONTEXT_SEPARATION_ONLY`; model-level independence and external
tool/time/step/retry enforcement are not proven.

`CODE_OPTIMIZATION` is now also a bounded `READ_ONLY` profile type. It has no
source/CPS/Runtime/production/user/route mutation capability, no successor
admission capability and no self-certification capability. It requires exact
`ARCHITECTURE_REVIEW` and `EVIDENCE_REVIEW` records over the same immutable
output. A general `CODEX_IMPLEMENTATION`, Safety Review or UI Delivery profile
is **INTENDED_NOT_IMPLEMENTED** unless a later current contract admits it.

## CURRENT — responsibility-subgraph evidence

`derive_responsibility_subgraph` is a current on-demand derived-evidence
producer under the existing Engineering/OMP completion boundary. Its only
admitted pilot domain is:

```text
ORDINARY_SERVICE_FAILURE_GOVERNED_RECOVERY_EXECUTION
```

The result is non-canonical, discardable and non-authorizing, with CPS,
Runtime, Production and Authority effect `NONE`. It is bounded to five source
surfaces and, in the current proof, contained 34 nodes, 58 direct static edges
and 439 retained unknown references. Unknown dynamic/state/lock/process facts
are not invented.

The completion binding now validates the exact domain, repository,
subgraph/result fingerprints, generated time, expiry and freshness status.
Expired or mismatched evidence stops safe. No BDP Mission or CPS projection is
created by this local proof.

`responsibility_subgraph_structural_delta` is an on-demand structural baseline
and review input only. `CONTINUOUS_ANTI_REGROWTH_ACTIVE` is **NOT_PROVEN**:
there is no background scanner, watcher, daemon, graph service, persistent
registry or automatic signal consumer.

## CURRENT — first Code Optimization audit

`V7_CODE_OPTIMIZATION_EXECUTION_PROFILE_AND_FIRST_DOMAIN_AUDIT_V1` executed as
a local read-only contract proof. It correctly applies `ZERO_OR_ONE` candidate
selection rather than forcing a cleanup target.

```text
PROFILE/REVIEW/COMPLETION CONTRACT = PASS
SUBGRAPH BINDING = PASS
CPS/RUNTIME/PRODUCTION/AUTHORITY EFFECT = NONE
FIRST COUNTERFACTUAL CANDIDATE COUNT = 0
SUBSTANTIVE DOMAIN AUDIT TERMINAL = INSUFFICIENT_EVIDENCE
```

Canonical Reference, SYSTEM_MAP and Runtime Model confirm durable topology but
do not currently provide a complete, current, domain-specific ordinary-recovery
causal spine through the exact required S11 terminal. The audit therefore does
not infer semantic necessity, redundancy, supersession, compatibility removal,
caller/consumer behavior or a counterfactual path from static reachability.

`V7_CODE_OPTIMIZATION_FIRST_COUNTERFACTUAL_PROOF_AND_BOUNDED_CLEANUP_V1` is
**NOT_ADMITTED**. The exact next action for Code Optimization is not cleanup:
the existing canonical owner must provide or revalidate the current
ordinary-recovery causal spine and exact S11 facts. Until then, cleanup
selection is `STOP_SAFE_TO_BE_RESPONSIBILITY_AMBIGUOUS`.

## PRESERVED — optimization law

The optimization unit is a responsibility subgraph, not a file. A large file
is a hotspot signal only. Reachable, consumed, behaviorally effective and
semantically necessary are distinct claims. A future cleanup can be considered
only after caller/consumer/state/behavior evidence and an equivalent
Control-versus-Counterfactual proof preserve required safety, route/kernel
truth, required-service S11, rollback, re-entry and a current compatibility
consumer where applicable. Tests alone are insufficient.

## Continuation rule

For any new context: read CPS first, then this handoff, Canonical Reference,
SYSTEM_MAP and current OMP. Treat the reports listed below as historical
evidence, not current truth. Recompute the exact CPS successor before action.

Relevant 2026-09-04 evidence:

- `docs/reports/engineering/2026-09-04_v7_agent_capability_existing_owner_audit_and_admission_decision.md`
- `docs/reports/engineering/2026-09-04_v7_omp_bounded_execution_profile_identity_and_completion_binding_v1.md`
- `docs/reports/engineering/2026-09-04_v7_existing_discovery_owner_domain_responsibility_subgraph_producer_v1.md`
- `docs/reports/engineering/2026-09-04_v7_code_optimization_execution_profile_and_first_domain_audit_v1.md`
