# V7 Master Project Handoff

Status: `CANONICAL_ENTRY_POINT`

Handoff state: `CURRENT_SYNCHRONIZED_FOR_SEAMLESS_NEW_CHAT_CONTINUATION`

Last synchronized: `2026-08-18`

Live volatile state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, Section 0

Active Program contract: `docs/programs/V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM.md`

This is the single handoff/context document for a new ChatGPT/Codex context. It is
not a second current-state owner. Any current value below is either a dated snapshot
or a pointer to its canonical owner. CPS Section 0 wins whenever this document and
live state differ. Engineering Reports are historical evidence only.

Do not create another handoff, parallel roadmap, Program, Runtime, Planner, queue,
scheduler, Authority, or truth source merely to continue from this document.

## 0. Current Continuation Snapshot — 2026-08-18

This is a dated continuation pointer, not a second live-state owner. Read CPS
Section 0 first; then revalidate the live VLESS facts below before any mutation.

### Immediate product frontier

The immediate objective is a genuine, bounded automatic move of one **enabled
managed** user from a failed source to an existing healthy target through the
existing path:

```text
Planner -> Packet -> lease -> restore barrier -> apply -> verify
```

OMP, reports, learning, replay, analytics and certification history are not part
of the client-switching KPI or a synchronous dependency of that path.

### VLESS lane: current verified state

Read-only verification on `2026-08-18` established the following:

- VLESS is an existing `controlled-certification` source, not an ordinary
  production-assignment pool.
- Its active eligible-user count is zero: the only assigned certification record
  is disabled. The Admin channel view independently reports zero users.
- Its controlled-source reservation is expired.
- The existing governed preflight returned `STOP_SAFE` without writing a
  Candidate, Packet, lease, route, restore barrier or user movement.

Therefore **do not** directly edit registry rows, reclassify a disabled record as
a live user, create a duplicate channel, or reuse an old Packet/lease/Authority
decision. Those operations would manufacture a test condition rather than perform
automatic failover for an actual client.

### Exact legal terminal and re-entry

Current lane-local terminal:

`STOP_SAFE_NO_ELIGIBLE_LIVE_VLESS_USER`

Exact next owner-backed frontier:

`EXISTING_CONTROLLED_CERTIFICATION_OWNER_FRESH_PREPARATION_AUTHORITY`

The existing controlled-certification owner must first supply a fresh valid
lifecycle: one enabled managed identity plus a non-expired exact reservation.
Only then may the existing Planner select a healthy target and execute the
one-user transaction. This prerequisite is a state/Authority boundary, not a
reason to add a new owner, Runtime, Planner, queue, registry or truth source.

Engineering evidence for this snapshot is local-only:

`/private/tmp/v7-hot-path-reports-local/V7_VLESS_AUTOMATIC_FAILOVER_ELIGIBILITY_REPORT_2026-08-18_1135_MSK.md`

### New-chat entry sequence

1. Read `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, Section 0.
2. Read this Section 0 and the local Engineering Report above.
3. Run the existing read-only governed preflight to revalidate the exact current
   VLESS eligibility; never infer it from a previous report.
4. If the controlled owner has produced the fresh lifecycle, continue through
   the existing bounded transaction owners only. Otherwise preserve the terminal
   and work on independent admitted engineering tracks; do not wait by adding
   audit machinery.

## 1. Project Purpose

V7 is a unified VPN/routing control plane. It accepts users through a stable entry,
uses multiple egress/channel types, detects failure, degradation and recovery,
selects a lawful healthy target, performs bounded failover, verifies kernel routing
and target-bound payload, and preserves capacity, freshness, stability, anti-flap,
rollback and Authority semantics.

Long-term scale target: at least `10,000` users and `50` egresses, with an
architecture that can continue to scale beyond those bounds.

The fundamental product contract is:

```text
FAILED_OR_UNUSABLE_SOURCE
  -> current affected users/cohort
  -> current lawful healthy targets
  -> target selection
  -> bounded route change
  -> kernel visibility
  -> exact target-bound payload verification
  -> traffic recovery
```

Tests, reports, deploys, certification labels and maturity percentages do not prove
this contract. Completion requires a real producer, non-test caller, consumer,
verified behavior change and product effect, or an explicit lawful terminal.

## 2. Truth and Owner Order

Use this order to resolve context:

1. this handoff for purpose, decisions and startup routing;
2. CPS Section 0 for volatile current state and exact successor;
3. active Program for execution and completion contracts;
4. OMP for engineering/development-plane laws;
5. Canonical Reference for durable product truth;
6. SYSTEM_MAP for owner topology;
7. Canonical Architecture Knowledge for accepted historical architecture knowledge;
8. Engineering Reports only as dated evidence.

Canonical owners:

| Concern | Owner |
| --- | --- |
| Live volatile state | `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, Section 0 |
| Active Reset contract | `docs/programs/V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM.md` |
| Engineering orchestration laws | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Durable product truth | `docs/reference/V7_CANONICAL_REFERENCE.md` |
| Owner topology | `docs/reference/SYSTEM_MAP.md` |
| Locked historical architecture knowledge | `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` |
| Historical evidence | `docs/reports/engineering/` |

## 3. Current Architectural Reality

Accepted evidence: `docs/reports/engineering/2026-08-13_083000_v7_routing_failover_reality_audit_and_architecture_verdict.md`.

The production-path audit established:

| Metric | Accepted result |
| --- | --- |
| Successful forward path | approximately `58.761588 s` |
| Kernel route mutation plus visibility | approximately `0.878 s` |
| No-action lifecycle | approximately `288.9-321.9 s` |
| Direct executable surface | approximately `41,821 LOC` |
| Reachable routing/safety/governance surface | approximately `85,859 LOC` |
| Producer-consumer hops before kernel apply | at least `9` |
| State surfaces read before apply | at least `17` |
| Durable writes before apply | at least `6` |
| Current per-user writer | `O(N)` registry rewrite behavior |

Accepted verdict:

`ROUTING_REALITY_AUDIT_CONSUMED_VERDICT_B_MINIMAL_CORE_BESIDE_LEGACY_RECOMMENDED`

Linux/kernel route mutation is not the dominant bottleneck. The dominant cost and
failure surface is orchestration, governance, historical reconciliation, broad
probing and evidence machinery synchronously surrounding the route change.

## 4. Current Strategic Decision

Endless incremental enlargement of the legacy routing hot path is not the final
architecture strategy. The approved direction is:

```text
FREEZE LEGACY HOT PATH
  -> full System Reset
  -> audit Programs / OMP / owners / code / state surfaces
  -> determine why intended behavior did not become product behavior
  -> preserve useful contracts and evidence
  -> design Minimal Routing Core
  -> effect-free shadow
  -> certification user
  -> one ordinary user
  -> bounded cohorts
  -> Core primary
  -> legacy retirement and physical system shrink
```

This is not a big-bang rewrite. Legacy V7 remains the production routing fallback,
control plane and evidence/acceptance corpus until migration is independently proven.

Program-level rule:

`LEGACY_V7_ROUTING_HOT_PATH = FROZEN_FOR_CAPABILITY_GROWTH`

Allowed legacy changes are limited to critical production fixes, safety/security
fixes, migration-required fixes, migration comparison instrumentation, and proven
deduplication/simplification required for safe migration. New legacy routing
capabilities are forbidden.

## 5. Active Program

Program ID: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

Program file: `docs/programs/V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM.md`

The Program is the primary engineering frontier through the existing OMP/CPS
lifecycle. Its status and exact phase must always be read from CPS Section 0 and the
Program owner; this handoff must not invent a later state.

### Current-state snapshot

Snapshot read on `2026-08-13` from CPS Section 0, whose recorded capture timestamp is
`2026-08-09T10:08:46+00:00`:

| Field | Snapshot value |
| --- | --- |
| Current primary Program | `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1` |
| Current phase | `RESET-M0` |
| Exact successor | `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION` |
| Current stop | `NONE` |
| External input required | `FALSE` |
| Current production Runtime | `LEGACY_V7_RUNTIME_UNCHANGED` |
| Routing Core implementation | `NOT_IMPLEMENTED; RESET-M3/M4 NOT REACHED` |
| Authority | existing legacy Authority unchanged; no Core Authority granted |
| Migration effects | `NONE` |

On any later read, replace this snapshot mentally with fresh CPS Section 0.

## 6. Reset Phase Structure

| Phase | Purpose |
| --- | --- |
| `RESET-M0` | System Reality / Program Intent / Product Contract Audit |
| `RESET-M0B` | Code Reality and Complexity Audit |
| `RESET-M0C` | Duplication / Dead Code / Legacy Surface Audit |
| `RESET-M1` | Program Portfolio Disposition |
| `RESET-M1B` | OMP / Development-System Failure Analysis |
| `RESET-M2` | Truth Owner and State Surface Collapse |
| `RESET-M3` | V7 vNext Architecture, Minimal Routing Core Contract and Negative Contract |
| `RESET-M4` | Effect-Free Shadow Core and Complexity Gate |
| `RESET-M5` | Decision Equivalence and Polygon Validation |
| `RESET-M6` | Certification User and One Ordinary User Production Proof |
| `RESET-M7` | Bounded Cohort / Constant-Time Architecture |
| `RESET-M8` | Core Primary Promotion |
| `RESET-M9` | Legacy Retirement / System Shrink / Program Cleanup |

These are phases of the existing Program, not separate Programs.

## 7. Central Reset Question

`WHY_DID_V7_FAIL_TO_REALIZE_ITS_OWN_PRODUCT_CONTRACT?`

Reset must establish, with owner-backed evidence:

- why Programs or Capabilities could be implemented, completed or certified while
  the fundamental routing contract remained slow or ineffective;
- where Intent stopped becoming real behavior;
- where outputs lacked consumers or consumers failed to change behavior;
- where local completion left parent/product intent open;
- where governance, OMP, reports and tests created local progress without product
  progress;
- where repeated `Reuse Existing Owner` expanded oversized coupled owners;
- whether `Architecture Closed by Default` concealed a systemic architecture defect;
- whether Capability/WIP/Future Dependency protections preserved failed structures;
- why Intent Gap, Mission Completion and Behavior Enforcement did not stop this
  outcome earlier.

## 8. Program Portfolio Disposition

Every existing or current-looking Program receives exactly one disposition:

- `KEEP_PERMANENT`
- `KEEP_AS_ACCEPTANCE_CONTRACT`
- `MERGE`
- `COMPLETE_AND_CLOSE`
- `LEGACY_ONLY`
- `REDESIGN`
- `REMOVE`

Do not copy an entire Program into vNext merely because some contracts are useful.
For example, CT-M0F latency/Time/SLO contracts may remain acceptance contracts while
legacy-specific orchestration becomes `LEGACY_ONLY` or `REDESIGN`.

## 9. OMP Role and Audit

OMP remains the development-plane orchestrator. Its correct future responsibility is:

- identify what does not work;
- identify the necessary engineering change and existing owner;
- define verification and safe deployment;
- prove Engineering Intent closure;
- produce the next development frontier.

OMP must not synchronously decide which egress should receive user X during a live
routing event. That belongs to Routing Core.

`RESET-M1B` must audit OMP assumptions including `Architecture Closed by Default`,
historical architecture-complete claims, Planner/runtime redesign restrictions,
Capability Maturity Protection, Engineering Work In Progress Protection, and
Approved Future Dependency Protection. Owner-backed Reset evidence may supersede a
legacy development assumption only through `RESET_OMP_CONTRACT_CONFLICT`. Actual
safety, Authority, rollback, verification and production-mutation boundaries remain
mandatory.

## 10. Target V7 vNext Architecture

### Routing Core / Data Plane

```text
OBSERVE -> STATE -> PLAN -> APPLY -> VERIFY
```

Target budget:

- approximately `5-7` focused modules;
- approximately `2,500-5,000 LOC`;
- preferably one long-lived Runtime process unless evidence proves a better model;
- `3-5` compact state surfaces;
- no OMP, reports, Learning, Replay or Maturity in the pre-apply path;
- no broad historical reconciliation;
- no full Matrix refresh when a compatible fresh receipt exists;
- avoid Python/process startup chains between decision and apply;
- first production target `<3 s`;
- prepared warm path target `<1 s`.

### Control Plane

The control plane owns policy and Authority envelopes, identity, health/capacity,
freshness, blast radius, cooldown, anti-flap and rollback/recovery constraints.

### Engineering Plane

OMP, Polygon, reports, Learning, Replay, Production Maturity and certification
history consume Runtime outcomes asynchronously.

Permanent boundary:

`ENGINEERING_PLANE_MUST_NOT_BE_REQUIRED_SYNCHRONOUS_ROUTING_HOT_PATH`

### Legacy V7

Legacy remains a policy/evidence source, acceptance corpus, migration comparison
input and bounded exception/fallback path until retirement. It is evidence, not an
unconditional oracle.

## 11. Routing Core Negative Contract

Future Routing Core must not synchronously:

- call OMP or progress CPS Programs;
- generate Engineering Reports;
- execute Polygon, Learning or Replay;
- calculate Production Maturity;
- reconcile historical incidents or broad certification history;
- execute broad inventory/Matrix refresh when a fresh compatible receipt exists;
- execute engineering campaigns;
- spawn long Planner subprocess chains;
- generate expanded post-action evidence before traffic recovery.

The default placement for any new capability is outside Core. Admission into the
hot path requires proof that post-apply/asynchronous execution cannot preserve safety.

## 12. Complexity and System Shrink

`FILE_SIZE_IS_A_SIGNAL_NOT_A_VERDICT`.

Large elements receive a semantic disposition based on responsibility, coupling,
callers and lifecycle:

- `KEEP_COHESIVE`
- `SPLIT_BY_RESPONSIBILITY`
- `MERGE_DUPLICATE_RESPONSIBILITY`
- `EXTRACT_LEGACY_BOUNDARY`
- `REMOVE_DEAD_CODE`
- `REWRITE_WITH_CORE`
- `REVIEW_AFTER_MIGRATION`

Mechanical splitting without semantic complexity reduction is forbidden.

Permanent simplification law:

`MINIMUM_SYSTEM_SURFACE_WITH_FULL_FUNCTION_PRESERVATION`

Preferred order: `REUSE -> MERGE -> SIMPLIFY -> REMOVE -> EXTEND`.

Each Reset phase records `BEFORE / AFTER / DELTA` for production LOC, routing
hot-path LOC, Core LOC, runtime modules/owners/processes/timers, state surfaces,
pre-apply hops and durable writes, lock domains and critical-path subprocesses.
System shrink is a Program success dimension, not cosmetic cleanup.

## 13. CT-M0F Disposition

CT-M0F is retained as knowledge/evidence and acceptance contract, not as the future
architecture:

- retain latency definitions and Time-owner spans;
- retain meaningful controlled-sample rules;
- retain initial `p95 <= 3 s`, no valid sample `>5 s`, and prepared `<1 s` gates;
- remote client/device/application recovery remains deferred without a client agent
  and does not block server-controlled Core engineering;
- do not enlarge the frozen legacy hot path with CT-M0F execution machinery.

## 14. Historical Lessons To Preserve

The following are accepted historical lessons, not templates that must be copied:

- a 4-second Telegram sentinel bridge produced canonical service-failure events;
- the ordinary consumer is `v7-autoswitch-planner.timer/service`;
- `v7-users-autoswitch.timer` is an intentionally inactive legacy apply path;
- a duplicate legacy Planner was removed from the critical path;
- CT-M0F certification fallback was separated from ordinary event-only failover;
- revision-aware active-incident obligation consumption was repaired;
- source-scope-zero reconciliation was repaired generically.

These repairs demonstrate the orchestration complexity supporting Reset.

## 15. Migration Safety and Authority

Migration sequence:

```text
Legacy authority
  -> Shadow Core with zero effects
  -> classified decision comparison
  -> certification user
  -> one ordinary user
  -> bounded cohort
  -> Core primary
  -> legacy hot-path retirement
```

For every legacy/Core divergence classify `LEGACY_CORRECT`, `CORE_CORRECT`,
`BOTH_LEGAL`, `BOTH_WRONG`, or `INSUFFICIENT_EVIDENCE` using current policy,
product truth and owner-backed evidence.

`NEW_CORE_EARNS_AUTHORITY_THROUGH_EVIDENCE`.

Core does not inherit production Authority merely because it is smaller, faster or
passes tests. No Runtime, routing, user, Authority or migration effect exists before
the corresponding Program phase and independent gates admit it.

## 16. RESET-M9 Retirement Goal

After Core-primary promotion, every legacy file, function, module, CLI, service,
timer, state surface, owner, Program and reconciliation path receives exactly one of:

- `STILL_REQUIRED`
- `LEGACY_EXCEPTION_REQUIRED`
- `MERGE`
- `DELETE`

Retirement is not complete when unused code merely becomes uncalled. Track LOC,
files, owners, processes, timers, state surfaces, hops and duplicate responsibilities
physically removed while retaining required historical evidence.

## 17. OMP Continuation and Reports

- Internal safe work must not require repeated manual `Continue` messages.
- A side repair must return to its parent Mission.
- A temporary external condition is not automatically an operator boundary.
- A no-progress loop is an engineering defect.
- Only irreducible external, Authority or safety input may return control.
- Reset must not autonomously resume frozen legacy capability growth.

After every meaningful audit, implementation, verification, test, deploy,
certification or investigation, create one concise report in
`docs/reports/engineering/`. Reports are historical evidence only; durable knowledge
must be promoted to its canonical owner.

## 18. NEW_CHAT_STARTUP_SEQUENCE

1. Read this handoff.
2. Read CPS Section 0 for the fresh volatile state and exact successor.
3. Read `docs/programs/V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM.md`.
4. Read only the OMP rules relevant to the current Reset phase.
5. Read Canonical Reference and SYSTEM_MAP only as needed to resolve owners/truth.
6. Reuse valid audit knowledge; do not repeat audits without an invalidation trigger.
7. Do not continue CT-M0F legacy optimization unless Reset explicitly routes it.
8. Do not implement Routing Core before RESET-M3/M4 contracts permit it.
9. Continue from the exact current Reset successor in CPS.
10. Preserve legacy production safety while migration is incomplete.

For the `2026-08-13` snapshot, the next action is RESET-M0 only:

`EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`

It is an audit/disposition phase. It must not mutate routing, users, Runtime,
Authority, migration state or implement Core.

## 19. DO_NOT_REDISCOVER

Accepted facts unless owner-backed invalidation is proven:

- routing reality audit verdict is Variant B: Minimal Core beside legacy;
- the accepted complexity findings are `58.761588 s` forward, `0.878 s` kernel plus
  visibility, `288.9-321.9 s` no-action, `41,821/85,859 LOC`, at least 9 pre-apply
  hops, 17 state surfaces and 6 durable writes, plus an `O(N)` writer;
- the legacy routing hot path is frozen for capability growth;
- `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1` is the active primary
  engineering Program;
- the target is a small `OBSERVE -> STATE -> PLAN -> APPLY -> VERIFY` Core;
- migration is incremental, not big-bang;
- OMP and the Engineering Plane stay outside routine routing hot path;
- complexity reduction and physical system shrink are completion requirements;
- no Routing Core has yet been implemented or granted production Authority.

## 20. Handoff Completion Check

A new context reading this handoff, CPS Section 0 and the active Reset Program can
determine the product purpose, the legacy architecture failure, preserved production
boundaries, frozen scope, target architecture, OMP role, current phase, exact next
action, forbidden actions and accepted non-repeatable knowledge.

Handoff terminal:

`V7_MASTER_PROJECT_HANDOFF = CURRENT_SYNCHRONIZED_FOR_SEAMLESS_NEW_CHAT_CONTINUATION`
