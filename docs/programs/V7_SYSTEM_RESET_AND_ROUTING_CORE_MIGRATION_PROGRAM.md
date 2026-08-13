# V7 System Reset and Routing Core Migration Program

Program ID: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

Status: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`

Program owner: existing `OMP` development-plane orchestrator.

Volatile state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md` (`CPS`).

Production authority: existing legacy V7 Runtime and Authority owners; unchanged.

First executable phase: `RESET-M0`.

Exact successor: `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`.

## 1. Purpose and Boundary

This Program is the temporary top-level engineering priority for a full V7 architectural reset and safe migration to a minimal Routing Core. It is not another repair of the current routing path, an immediate rewrite, a Runtime, a second CPS, Planner, Authority owner, registry, queue, watcher, scheduler, store, or truth source. Execution remains inside the existing OMP/CPS lifecycle.

All existing Programs remain until `RESET-M0/RESET-M1` gives each exactly one disposition: `KEEP_PERMANENT`, `KEEP_AS_ACCEPTANCE_CONTRACT`, `MERGE`, `COMPLETE_AND_CLOSE`, `LEGACY_ONLY`, `REDESIGN`, or `REMOVE`. Nothing transfers automatically into V7 vNext.

### Reset Overhead, Necessity and Temporary-Lifecycle Laws

Permanent engineering law: `RESET_OVERHEAD_BUDGET`. Reset is a temporary audit/migration activity, not a new permanent V7 subsystem. Without irreducible necessity it must not create a permanent Runtime, Planner, owner, registry, store, queue, scheduler, watcher, service, timer, state surface, truth owner, reconciliation framework or audit framework. Priority is `EXISTING_OWNER_OR_TOOL -> EXISTING_REPORT_OR_DOCUMENT_PROJECTION -> TEMPORARY_ANALYSIS_SCRIPT -> NEW_CODE_ONLY_IF_IRREDUCIBLY_REQUIRED`. Every Reset-only artifact records purpose, owner, production/non-production class, expected lifetime and `RETAIN`, `MERGE`, `ARCHIVE`, or `DELETE` disposition. Reset tooling never automatically becomes a production component, Runtime dependency or canonical truth owner.

Law: `LOGICAL_OUTPUT_NOT_PHYSICAL_SYSTEM`, with the reporting constraint `LOGICAL_OUTPUT_NOT_DOCUMENTATION_EXPLOSION`. A manifest, matrix, graph, ledger or other required logical output does not imply a separate physical file, document, generator, service, registry, database, framework, state surface or owner. Multiple audit projections must reuse the minimum existing artifacts that preserve coverage, traceability, evidence, owner mapping and disposition; no artifact may be created merely to re-present knowledge already preserved by an existing owner.

Law: `PRESERVE_REQUIRED_BEHAVIOR_NOT_LEGACY_STRUCTURE`. Reset preserves required product semantics, safety, Authority, rollback/recovery, verification, capacity, freshness, anti-flap and compatibility behavior. It does not preserve a legacy class, file, owner, Planner, matrix, snapshot, workflow, state structure or implementation topology merely because that structure exists. Before migration, prove the product intent is necessary, whether it must execute synchronously, whether a dedicated owner is necessary, whether an existing owner can absorb it, and whether a simpler representation preserves the behavior.

Law: `QUESTION_NECESSITY_BEFORE_OPTIMIZING_IMPLEMENTATION`. Before redesign/refactor ask, in order: does the behavior need to exist; must it execute before traffic recovery; does it require a dedicated owner; can an existing owner absorb it; can it be derived or asynchronous; only then redesign implementation. Do not optimize or elegantly rewrite a mechanism that can be removed.

Law: `EVIDENCE_DEPTH_PROPORTIONAL_TO_RISK`, also expressed as `NECESSARY_DEPTH_WITHOUT_UNIFORM_DEPTH`. Audit coverage is exhaustive, but evidence depth is proportional to production, safety, Authority, migration and deletion risk. Route mutation and rollback/recovery mechanisms require maximum depth. An obvious test-only helper or historical renderer/document helper requires sufficient identity, reachability, classification and disposition evidence, not a production-runtime-level investigation. This proportionality reduces bureaucracy; it never permits a coverage gap.

Law: `DEFAULT_OUTCOME_OF_RESET = SYSTEM_SHRINK_NOT_CODE_REORGANIZATION`. One coupled component replaced by several equally coupled components is not success. Track LOC/files/owners/state surfaces/processes/timers/hot-path stages added and removed. Temporary growth is legal only when necessary for safe migration and paired with an exact later shrink disposition.

## 2. Consumed Reality and Verdict

The Program consumes the owner-backed routing reality audit as its opening basis:

- successful forward path approximately `58.761588 s`;
- kernel mutation plus visibility approximately `0.878 s`;
- no-action lifecycle approximately `288.9-321.9 s`;
- direct executable surface approximately `41,821 LOC`;
- reachable routing/safety/governance surface approximately `85,859 LOC`;
- at least 9 producer-consumer hops before kernel apply;
- at least 17 state surfaces read before apply;
- at least 6 durable writes before apply;
- current user writer has O(N) behavior.

Accepted verdict: `ROUTING_REALITY_AUDIT_CONSUMED_VERDICT_B_MINIMAL_CORE_BESIDE_LEGACY_RECOMMENDED`. It may be reopened only by material new evidence.

## 3. Legacy Hot-Path Freeze

Program-level engineering rule: `LEGACY_V7_ROUTING_HOT_PATH = FROZEN_FOR_CAPABILITY_GROWTH`.

Allowed: critical production fixes; security/safety fixes; migration-required fixes; comparison instrumentation; and removal of proven duplication required for migration safety.

Forbidden: new routing capabilities in the legacy hot path; new OMP/Polygon/Certification pre-cutover stages; expanded legacy orchestration; new owners/stores/queues/watchers/schedulers without irreducible proof; or CT-M0F continuation by enlarging the legacy execution chain.

This freeze is not a Runtime mutation. Current production remains legacy and operational as the fallback.

## 4. Fundamental Product Contract

`FAILED_OR_UNUSABLE_SOURCE -> determine affected users/cohort -> read current lawful healthy targets -> select target -> bounded route change -> verify kernel visibility -> verify target payload -> finish traffic recovery`.

Anything not required to safely execute this contract before apply/verify is a candidate for the asynchronous or post-action plane.

Primary diagnostic question: `WHY_DID_V7_FAIL_TO_REALIZE_ITS_OWN_PRODUCT_CONTRACT?`

The reset must prove why Programs/Capabilities could claim implementation, completion, or certification while this contract remained unrealized; identify the exact link where Engineering Intent stopped becoming product behavior; explain why Mission Completion, Behavior Propagation, Intent Gap, Necessity, OMP, and related safeguards did not prevent complexity growth; identify the mechanisms that produced local progress without end-to-end product progress; and change those mechanisms before they can enter vNext.

No Program, Capability, Mission, or implementation is successful unless its intended contribution reaches a real consumer and product effect, or an explicit lawful independent terminal. Tests, deploys, reports, certification labels, and documentation are evidence classes, not proof of realized intent.

## 5. Target Boundaries

### Routing Core / Data Plane

Minimal path: `OBSERVE -> STATE -> PLAN -> APPLY -> VERIFY`.

Architectural budget: approximately 5-7 focused modules, 2,500-5,000 LOC, one long-lived Runtime process unless audit proves better, 3-5 compact state surfaces, zero OMP/report/Learning/Replay/Maturity calls before apply, zero full historical reconciliation, no broad Matrix refresh when a compatible fresh health receipt exists, and no Python/process startup between decision and apply where practical. Initial production gate is `<3 s`; prepared warm target is `<1 s`; design must support 10k+ users and 50+ egresses.

### Control Plane

Preserve only required policy, Authority envelope, identity, capacity, current egress health, freshness, blast radius, cooldown/anti-flap, circuit breaker, and rollback/forward-recovery inputs. Engineering workflows must not execute synchronously before ordinary certified failover.

### Engineering Plane

OMP, Polygon, Learning, Replay, Engineering Reports, Production Maturity, certification history, and CPS program/capability progression consume Runtime receipts/outcomes asynchronously. Law: `ENGINEERING_PLANE_MUST_NOT_BE_REQUIRED_SYNCHRONOUS_ROUTING_HOT_PATH`. OMP decides engineering work, owners, verification, deployment safety, intent closure, and next development frontier; it never decides the runtime egress for user X.

### Legacy V7

Legacy remains policy/evidence source, acceptance corpus, comparison oracle, exception path, migration fallback, and historical/control-plane consumer. Removal from the primary path is incremental, never big-bang.

## 6. RESET-M0 System Reality, Program Intent and Product Contract Audit

Canonical phase name: `RESET-M0 — SYSTEM_REALITY_PROGRAM_INTENT_AND_PRODUCT_CONTRACT_AUDIT`.

Inventory every active or current-looking V7 Program, Capability, and major Runtime/Control/Engineering owner. For each prove the chain:

`INTENDED -> DOCUMENTED -> IMPLEMENTED -> REAL PRODUCER -> REAL NON-TEST CALLER -> REAL CONSUMER -> CONSUMPTION VERIFIED -> BEHAVIOR CHANGED -> PRODUCT EFFECT -> LEGAL TERMINAL / NEXT CONSUMER`.

Record what the object was intended to do for the product; what exists; real caller and consumer; exact output consumed; behavior and user/Runtime effect; exact broken link; why existing completion gates allowed the break; why development continued without product effect; current blocker; and root-cause class. Root-cause classes are `MISSING_IMPLEMENTATION`, `MISSING_INTEGRATION`, `DISCONNECTED_CONSUMER`, `WRONG_OWNERSHIP`, `WRONG_ABSTRACTION`, `DUPLICATED_RESPONSIBILITY`, `MISPLACED_PRE_CUTOVER_WORK`, `STALE_HISTORICAL_DEPENDENCY`, `OVERENGINEERING`, `OBSOLETE_REQUIREMENT`, `PROCESS_GOVERNANCE_FAILURE`, and `FUNDAMENTAL_ARCHITECTURE_DEFECT`.

Every object receives one factual Intent Reality verdict: `INTENT_REALIZED`, `PARTIALLY_REALIZED`, `IMPLEMENTED_NOT_CONSUMED`, `CONSUMED_NO_PRODUCT_EFFECT`, `WRONG_ARCHITECTURAL_PLACEMENT`, `OBSOLETE`, `NOT_NEEDED`, or `UNKNOWN_REQUIRES_OWNER_EVIDENCE`.

The audit must explicitly cover OMP, Service Failure Automation, CT-M0F, Polygon/FSSE, L7/L8, Authority evolution, Learning, Replay, Production Maturity, AEP/external re-entry, certification Programs, CAP-U01-U22, backlog remnants, and every CPS/OMP portfolio entry. Existence is not proof of necessity.

### RESET Audit Completeness and Boundedness Law

The Reset audit must be exhaustive without becoming perpetual. It begins from one immutable, timestamped `RESET_AUDIT_SCOPE_SNAPSHOT` of the repository, deployed Runtime surface, systemd units/timers, state surfaces, canonical Programs, owners, entrypoints and production configuration identities. Every discovered object receives a stable audit identity and exactly one disposition; no production-relevant file, function, class, CLI, service, timer, call edge, state read/write, process launch, probe, lock, policy check, Authority gate, route effect, verifier, rollback path, recovery path or real consumer may silently disappear from the audit.

The mandatory coverage chain is:

`REPOSITORY/PRODUCTION INVENTORY -> ENTRYPOINT REACHABILITY -> FUNCTION/CALL EDGE -> OWNER/RESPONSIBILITY -> STATE/EFFECT -> REAL CALLER -> REAL CONSUMER -> PRODUCT CONTRACT CONTRIBUTION -> DISPOSITION -> SUCCESSOR/TERMINAL`.

The audit produces one coverage manifest with total/disposed/unresolved counts and explicit lists of `UNREACHABLE`, `DYNAMICALLY_RESOLVED`, `EXTERNAL_OWNER_BOUND`, `UNKNOWN_REQUIRES_OWNER_EVIDENCE`, and `NOT_PRODUCTION_RELEVANT` objects. `RESET-M0/M0B/M0C` cannot complete while any scoped object lacks a disposition or an exact owner-backed residual. Dynamic imports, shell dispatch, systemd invocation, subprocess edges, generated configuration, plugin/adapter resolution and production-only callers must be checked semantically rather than only by text-name matching.

Exhaustive does not mean repeated. Law: `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER`. A valid audited object is reused as `RESULT_REUSED_VALID`; it is re-opened only when its content hash, caller/consumer graph, production deployment identity, owner, state/effect contract, Runtime role, or canonical requirement materially changes. Each phase works from the same scope snapshot plus a bounded delta ledger. New discoveries are appended as deltas; they do not restart completed inventory.

Mandatory bounded outputs are `RESET_PORTFOLIO_INTENT_REALITY_MATRIX`, `RESET_CODE_REACHABILITY_AND_RESPONSIBILITY_MANIFEST`, `RESET_PRODUCER_CONSUMER_AND_STATE_EFFECT_GRAPH`, `RESET_DUPLICATION_DEAD_LEGACY_DISPOSITION_MATRIX`, `RESET_UNKNOWN_AND_EXTERNAL_RESIDUAL_REGISTER`, and `RESET_AUDIT_COVERAGE_LEDGER`. These are projections through existing document/report owners, not new Runtime stores, registries or truth owners.

Law: `REPORT_DEPTH_WITHOUT_REPORT_BLOAT`. Audit evidence must increase decision confidence, not documentation volume. `EVIDENCE_COMPLETENESS` and `REPORT_SIZE` are independent: complete evidence may remain in linked artifacts, generated projections, or existing evidence owners without copying intermediate data into the Master Audit Report. For each material conclusion the Master report preserves only conclusion, evidence basis, owner, disposition, residual and next action. The same information must not be repeated across summary, matrix, graph, table and appendix unless the representation changes decision context.

Dynamic compression applies: already owner-backed valid findings are consumed, not ceremonially re-audited. Independent criteria continue when another object is external or unknown. An audit phase stops the whole Program only when no independent scoped criterion can proceed safely.

Audit mutation law: `STRICT_AUDIT_MUTATION_SEPARATION`. RESET-M0/M0B/M0C execute `DISCOVER -> VERIFY -> CLASSIFY -> DISPOSITION`, not `PATCH -> REFACTOR -> DELETE -> MIGRATE` merely because a defect is found. Only a critical production, security or safety fix, or the minimum unblock required to continue the audit, may become a separately recorded side repair with exact owner, impact and return to the parent Reset Mission. Audit findings themselves grant no Runtime, routing, deletion, migration or Authority effect.

### Deep Relationship Reality Audit

Inventory alone is insufficient. RESET-M0/M0B/M0C/M1/M1B must reconstruct and verify the real multi-layer system relationships:

`PRODUCT GOAL -> PROGRAM INTENT -> CAPABILITY/MISSION -> OWNER -> PROCESS/ENTRYPOINT -> FILE/MODULE -> FUNCTION/CALL EDGE -> INPUT/STATE -> DECISION/EFFECT -> OUTPUT -> REAL CONSUMER -> BEHAVIOR CHANGE -> PRODUCT RESULT -> NEXT CONSUMER/TERMINAL`.

For every relationship record source identity, target identity, relationship type, producer, consumer, transport/call mechanism, schema or argument contract, direction, sync/async placement, blocking behavior, state read/write, side effect, freshness/invalidation, error/timeout behavior, retry/idempotency, ownership, real non-test evidence, and whether the edge is required for the fundamental Product Contract.

Relationship types must include direct function call, import, subprocess, shell, systemd unit/timer, file/JSON/JSONL state exchange, database/configuration, network/API/probe, signal/wakeup, generated artifact, manual/operator handoff, Authority decision, Runtime effect, verification, rollback/recovery, report/document reference, and Program/CPS/OMP successor projection.

The audit must detect and explain: orphan producers; outputs without consumers; consumers without valid producers; dead or unreachable branches; circular dependency; duplicated responsibility; multiple writers; hidden sync work; stale or contradictory projections; implicit manual bridges; caller/consumer identity drift; wrong sequencing; retry storms; no-progress loops; historical evidence acting as current truth; engineering/control-plane work in the Runtime path; and functions whose local terminal fails to activate the required next consumer.

Every Program/component/function must be evaluated both locally and in context. A locally correct function may still receive `WRONG_ARCHITECTURAL_PLACEMENT`, `DUPLICATED_RESPONSIBILITY`, `CONSUMED_NO_PRODUCT_EFFECT`, or `REMOVE_CANDIDATE` when its surrounding relationship does not contribute lawfully to the Product Contract. Conversely, a small or rarely called function cannot be removed when it closes a necessary safety, compatibility, recovery, Authority or legacy-exception edge.

The required relationship result is not merely a diagram. It must reconcile intended, documented, static, configured and observed production relationships; mark every mismatch; identify the last responsible broken link; and trace every kept product behavior to a complete end-to-end consumer chain. Terminal: `DEEP_PROGRAM_COMPONENT_FUNCTION_RELATIONSHIP_GRAPH_PROVEN`.

### Master Audit Report and Self-Review Closure

All RESET-M0 through RESET-M1B findings must be assembled into one coherent, readable existing-type Engineering Report: `V7_SYSTEM_RESET_MASTER_AUDIT_REPORT`. It is a decision instrument and historical evidence, not a storage dump or new state owner. Canonical decisions and current successor remain promoted to their existing owners. Deep evidence may stay linked in existing artifacts, generated projections or evidence owners; the Master report must remain compact enough to expose conclusions, evidence basis, owner, disposition, residual and next action without duplicating raw intermediate material.

The Master Audit Report must contain:

1. executive verdict and exact root causes;
2. scope snapshot, methodology, evidence classes and limitations;
3. Product Contract and Intent-vs-Reality results;
4. Program/Capability/Mission portfolio and dispositions;
5. real Program/component/process/file/function relationship graph and narrative paths;
6. production entrypoints, processes, timers and dynamic-dispatch paths;
7. state surfaces, owners, readers/writers, locks, probes and durable effects;
8. hot path, control plane, engineering plane and legacy boundaries;
9. duplication, dead code, obsolete files, oversized owners and removal candidates;
10. deep root-cause analysis of OMP/development-system failure;
11. safety/Authority/rollback/verification semantics that must remain;
12. what will be reused, merged, simplified, redesigned, retired or deleted;
13. baseline complexity and latency, expected shrink and unresolved residuals;
14. exact RESET-M2/M3 inputs and recommended execution order;
15. appendices or linked machine-readable evidence sufficient to account for every scoped object and edge.

The report must be understandable without reading thousands of source files. Each conclusion must link to exact evidence and distinguish `MEASURED`, `OBSERVED_PRODUCTION`, `STATIC_PROVEN`, `CONFIGURED`, `INFERRED`, `HISTORICAL`, `UNKNOWN`, and `REQUIRES_EXTERNAL_OWNER` evidence. Tables and diagrams summarize; they must not hide unresolved rows.

Before audit completion, execute the internal quality self-review:

`REPORT -> CHECK FAILED OR UNPROVEN CRITERIA ONLY -> TARGETED RECHECK -> FINALIZE`.

Self-review checks contradictions, criterion coverage, evidence presence, root-cause correctness and the `Product Contract -> evidence -> disposition` chain. It repeats only for exact missing, contradictory, weak or uncovered criteria and is bounded by `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER`; it must not create a new audit loop or restart valid work. Every original Program goal, phase criterion and mandatory output receives `PROVEN_COMPLETE`, `PROVEN_NOT_APPLICABLE`, or `EXACT_RESIDUAL_WITH_OWNER_AND_SUCCESSOR`. `UNKNOWN` without an investigation record and successor is not closure.

Superficial completion is forbidden. A report is not complete merely because it is long, all headings exist, tools ran, counts were produced, or a diagram renders. Completion requires traceable evidence from surface inventory down to root cause and back up to product intent, zero unexplained coverage gaps, reconciled contradictions, explicit limitations, and an exact next implementation/disposition frontier. Terminals: `RESET_MASTER_AUDIT_REPORT_GOAL_COVERAGE_RECONCILED` and `RESET_MASTER_AUDIT_REPORT_FINAL_SELF_REVIEW_PASS`.

Each later phase `RESET-M2` through `RESET-M9` produces its own concise phase Engineering Report linked back to the Master Audit findings and forward to its exact successor. `CONCISE` means compact but evidence-complete: each phase report states what changed, which intent closed, supporting evidence, owner, residual and successor. It links to, and does not repeat, the full Master Audit Report. At Program completion, one coherent `V7_SYSTEM_RESET_PROGRAM_COMPLETION_REPORT` must reconcile every original Program purpose, phase contract, Master Audit root cause, preserve/exclude decision, migration gate, latency/complexity target, production effect, legacy retirement disposition and system-shrink metric against real owner-backed results.

The final Program Completion Report runs the same goal/coverage/contradiction/root-cause/product-trace self-review over the complete `RESET-M0 -> RESET-M9` lifecycle. Every original goal receives `PROVEN_ACHIEVED`, `PROVEN_NOT_APPLICABLE`, or `NOT_COMPLETE_EXACT_RESIDUAL`; the last verdict forbids Program completion. It must distinguish code, test, caller, consumer, deployed Runtime, production behavior, user effect, Authority, rollback/recovery and physical deletion evidence. Final report terminal: `RESET_PROGRAM_COMPLETION_REPORT_ALL_GOALS_OWNER_BACKED_PASS`.

### RESET-M0B Code Reality and Complexity Audit

`RESET-M0B — CODE_REALITY_AND_COMPLEXITY_AUDIT` is an internal phase, not a Program. It audits the complete production-relevant code surface, not only the measured failover path.

For every production-relevant file/module/service, and for every function/class reachable from a production entrypoint or dynamically loaded production configuration, capture LOC, function/class count, distinct responsibilities, callers, consumers, dependencies, state reads/writes, side effects, subprocesses, locks, network calls, durable writes, Runtime/hot-path/legacy role, owner-backed change history, duplicate/dead/unreachable/manual/test/historical behavior, asynchronous candidates, and pre-cutover necessity. Non-reachable functions remain listed with evidence; absence from a static call graph alone is not deletion proof.

Permanent rule: `FILE_SIZE_IS_A_SIGNAL_NOT_A_VERDICT`. Large files receive one semantic disposition: `KEEP_COHESIVE`, `SPLIT_BY_RESPONSIBILITY`, `MERGE_DUPLICATE_RESPONSIBILITY`, `EXTRACT_LEGACY_BOUNDARY`, `REMOVE_DEAD_CODE`, `REWRITE_WITH_CORE`, or `REVIEW_AFTER_MIGRATION`. Splitting is allowed only for independently proven responsibilities, change reasons, consumers, or lifecycles. Mechanical growth from one large file into more coupled LOC is forbidden; semantic/system complexity must decrease.

### RESET-M0C Duplication, Dead Code and Legacy Surface Audit

`RESET-M0C — DUPLICATION_DEAD_CODE_AND_LEGACY_SURFACE_AUDIT` is an internal phase, not a Program. Audit duplicate Planner/selection/policy/health/capacity/Matrix/snapshot/inventory/fingerprint/state-projection/serialization/reconciliation/verification/closure/report/evidence/adapter/safety logic.

For every function/module/service/CLI answer `WHO_CALLS_THIS_IN_REAL_NON_TEST_OPERATION?` and classify it as `CURRENT_PRODUCT_REQUIRED`, `ASYNC_ENGINEERING_REQUIRED`, `LEGACY_EXCEPTION_REQUIRED`, `TEST_SUPPORT_ONLY`, `MANUAL_ONLY`, `HISTORICAL_ONLY`, `DUPLICATED`, `UNREACHABLE`, `NO_LIVE_CONSUMER`, or `REMOVE_CANDIDATE`. Audit creates owner-backed dispositions only; it deletes nothing.

No removal may be inferred from age, file size, naming, lack of unit tests, or one missing static caller. A later merge/delete requires: complete caller/consumer and dynamic-dispatch proof; production/runtime/config/package/systemd reachability proof; preserved necessary semantics mapped to a surviving owner; affected replay/tests/Polygon corpus; rollback or restoration plan; no unresolved external consumer; and an observable post-change shrink delta. Historical evidence may be archived or retained outside active Runtime packaging, but must not be destroyed when it remains necessary for audit, legal, learning, regression or Authority provenance.

## 7. RESET-M1 Program Portfolio Disposition

Disposition applies independently when necessary to Program intent, policy, acceptance contract, Runtime implementation, engineering orchestration, and historical evidence. `KEEP_AS_ACCEPTANCE_CONTRACT` preserves useful goals, SLOs, verification, or acceptance criteria without migrating execution machinery. CT-M0F latency/Time contracts may receive this disposition while legacy orchestration is `LEGACY_ONLY` or `REDESIGN`.

### RESET-M1B OMP and Development-System Failure Analysis

`RESET-M1B — OMP_AND_DEVELOPMENT_SYSTEM_FAILURE_ANALYSIS` is an internal, owner-evidence-driven root-cause audit, not a Program and not a presumption that OMP is good or bad.

It must explain why the development system allowed complexity growth without the primary Product Contract; which rules were documentary versus executed; which local completion contracts lost the parent/product intent; where owner reuse became indefinite extension of oversized owners; where Architecture Closed by Default obscured systemic defects; where WIP/maturity/future-dependency protections preserved obsolete constructions; where tests/reports/deploy/certification produced false progress; where OMP entered Runtime routing lifecycle; and why Intent Gap, Mission Completion Evidence Gate, and Behavior Enforcement did not stop the failure.

Every relevant OMP law receives `KEEP`, `SIMPLIFY`, `REDESIGN`, `SCOPE_DOWN`, `SUPERSEDE_FOR_RESET`, or `REMOVE`. Explicitly audit Architecture Closed by Default, Architecture Phase Complete, redesign prohibitions, Capability Maturity Protection, Engineering WIP Protection, and Approved Future Dependency Protection.

Distinguish `REAL_SAFETY_PROTECTION` from `LEGACY_DEVELOPMENT_PROTECTION`. Real safety, Authority, production mutation, rollback, and verification protections remain mandatory. A legacy development protection may be superseded only after owner-backed proof that it blocks correction of the architectural cause and after exact supersession rules are recorded before any merge/remove action.

If current reset evidence conflicts with a historical OMP architectural assumption, materialize `RESET_OMP_CONTRACT_CONFLICT` and resolve it in RESET-M1B before Core implementation. A historical `Architecture Complete` claim cannot by itself prohibit an owner-backed correction approved by this Reset Program.

## 8. RESET-M2 Truth Owner and State Surface Collapse

Retain one authoritative owner for each live runtime fact: user assignment, egress health, capacity, active policy, Authority generation, incident/failure generation, target health receipt, active operation/lease, kernel route state, verification result, and outcome.

For every surface ask `DOES_THIS_STATE_SURFACE_NEED_TO_EXIST_AT_ALL?` and record writer, readers, real product consumer, decisions depending on it, source truth, derivability, freshness/invalidation, sync/async need, and migration necessity.

Every surface receives one disposition: `KEEP_AUTHORITATIVE`, `DERIVE_ON_DEMAND`, `DERIVED_ASYNC_ONLY`, `MERGE`, `LEGACY_READ_ONLY`, or `RETIRE`. CPS, OMP, and history cannot become sources of truth for pre-cutover routing scope. Core consumes current generation-bound Runtime truth and must not inherit the current 17+ surfaces by default.

## 9. Preserve / Exclude / Acceptance Matrix

Must preserve: policy and Authority semantics; identity/assignment truth; health/capacity; freshness/invalidation; anti-flap/cooldown; circuit breaker; blast radius; idempotency; rollback/forward recovery; route and payload verification; append-only evidence lineage.

Must not enter the new hot path: OMP scheduling; CPS progression; Reports; Production Maturity; Learning; Replay; Polygon; broad certification history; historical incident reconciliation; full Outcome Passport expansion; full Matrix when a compatible fresh receipt exists; percentile/campaign bookkeeping; broad inventory refresh.

Reuse as acceptance corpus: current tests, Polygon scenarios, failure classifications, Candidate/Packet lessons, rollback histories, controlled production outcomes, route/payload verifier fixtures, Time receipts, hidden O(N) guards, and production incidents.

## 10. RESET-M3 vNext Architecture and Minimal Core Contracts

Before code, specify only:

- `OBSERVE`: generation-bound health/capacity/failure inputs;
- `STATE`: runtime state required for decision/apply;
- `PLAN`: pure deterministic desired-assignment delta;
- `APPLY`: idempotent minimal kernel/assignment diff;
- `VERIFY`: route visibility and one exact payload path.

`CORE_POSITIVE_CONTRACT` is the five-stage contract above plus fresh generation; exact source/target identity; lawful target; capacity reserve; policy generation; bounded users/cohort; one active operation; idempotency; cooldown/anti-flap; compact lease/CAS; rollback/forward-recovery readiness; kernel visibility; and payload verification.

`CORE_NEGATIVE_CONTRACT`: Core must not synchronously execute OMP, progress CPS Programs, generate Engineering Reports, execute Polygon, run Learning/Replay/Production Maturity, reconcile historical incidents or broad certification history, run full Matrix/inventory with a compatible fresh receipt, perform engineering reconciliation or campaign bookkeeping, spawn Planner subprocess chains, materialize expanded Outcome/closure objects, or become an engineering scheduler.

Every future capability defaults outside Core. Pre-apply admission requires proof that safety needs live evaluation, stale/precomputed evaluation is unsafe, and omission can produce an incorrect route mutation.

### Core Time and Recovery Contract

The canonical server-controlled recovery clock is:

`FIRST_QUALIFYING_FAILURE_EVIDENCE -> EXACT_CLIENT_NETWORK_CONTEXT_TARGET_PAYLOAD_RECOVERY`.

RESET-M3 must define, before implementation, separate bounded spans for failure detection, state publication, prepared-decision validation, target selection, policy/Authority/safety validation, apply, kernel visibility and exact payload recovery. Lifecycle closure time remains a separate post-recovery metric and cannot substitute for traffic recovery. The `<3 s` production gate and `<1 s` prepared warm-path gate are end-to-end recovery gates, not route-visibility-only or kernel-counter gates.

The exact payload probe must execute in the certification/user routing context, use its policy/table/mark semantics, prove expected target egress identity and payload response, avoid the management/default path and stale socket/DNS reuse, and use an explicit timeout/retry contract.

### Single Writer, Fencing and Ownership Transfer Law

At any instant exactly one owner may mutate an assignment/route scope. Legacy and Core may observe and compare concurrently, but they must never both apply to the same scope. Every effectful operation requires a current generation, operation identity, fencing token or equivalent existing-owner CAS, and idempotency key. Promotion and fallback require an explicit atomic ownership transition. A stale Core action after fallback to Legacy, or stale Legacy action after Core admission, must be rejected before mutation.

Shadow mode has `effects=ZERO`. Certification, ordinary-user and cohort scopes are independently admitted. Failure of Core or loss of its lease cannot leave ambiguous writer ownership; the declared safe owner and route state must be recoverable from canonical Runtime truth.

### Apply-to-Closure Crash Boundary

Traffic recovery must not wait for expanded evidence, but a successful or partial kernel/assignment commit must create a compact durable receipt or be reconstructable from canonical generation plus kernel/assignment truth. That receipt creates one durable asynchronous closure obligation consumed by existing Engineering Plane owners for extended verification, Outcome, Replay, Learning, CPS/OMP projection and residual computation.

If the process fails after apply and before closure publication, restart reconciliation must classify the actual route/assignment state, resume verification or forward recovery/rollback, publish exactly one closure obligation, and prevent duplicate apply. `APPLY_SUCCEEDED_CLOSURE_LOST` is forbidden as an unowned terminal.

### Freshness and Degradation Decisions

For every health, capacity, policy, Authority, identity, membership and target receipt, RESET-M3 must define owner, generation, maximum age, invalidation triggers and one legal result: `USE_FRESH_PREPARED_RECEIPT`, `BOUNDED_SYNCHRONOUS_REVALIDATION`, `FALLBACK_TO_LEGACY`, or `STOP_SAFE`. Missing/stale inputs must not silently trigger broad Matrix/history reconciliation in Core and must not be accepted as current truth.

## 11. Routing Core Complexity Budget

Permanent law: `ROUTING_CORE_COMPLEXITY_BUDGET`.

Every core change must state why it is mandatory pre-apply, why async/post-apply is insufficient, LOC delta, state-surface delta, process/hop delta, latency impact, and owner impact. Track Core LOC, total production LOC, active hot-path LOC, modules/files, owners, processes, timers, state surfaces, producer-consumer hops, synchronous durable writes, locks, subprocesses, probes, external process starts, and pre-apply stages. Every phase records `BEFORE`, `AFTER`, and `DELTA`. Complexity growth requires explicit necessity proof and demonstrated net system simplification or value. OMP, Polygon, Learning, and future Programs may not automatically add hot-path stages. Budget violation is an architecture-review boundary.

Permanent minimization law: `MINIMUM_SYSTEM_SURFACE_WITH_FULL_FUNCTION_PRESERVATION`; order of preference is `REUSE -> MERGE -> SIMPLIFY -> REMOVE -> EXTEND`. Preservation means required behavior and semantics, not automatic preservation of legacy implementation topology. A new file/owner/store/process requires proven necessity.

`SYSTEM_COMPLEXITY` is a factual metric set, not a scoring engine. Canonical fields are `production_loc`, `routing_hot_path_loc`, `routing_core_loc`, `runtime_module_count`, `runtime_owner_count`, `runtime_process_count`, `timer_count`, `state_surface_count`, `pre_apply_hop_count`, `pre_apply_durable_write_count`, `lock_domain_count`, and `critical_path_subprocess_count`. Reset reports show baseline/current/delta. Successful migration must physically reduce the primary system surface.

## 12. Migration Stages

1. Stage 0, Legacy Freeze: legacy remains production authority.
2. Stage 1, Shadow Core: identical inputs, zero effects, compare decisions.
3. Stage 2, Decision Equivalence: close explained divergence; canonicalize expected behavior where legacy is proven wrong.
4. Stage 3, Certification User: one existing governed certification user; measure latency, rollback, crash recovery.
5. Stage 4, One Ordinary User: one user inside an already permitted policy envelope.
6. Stage 5, Bounded Cohort: class/bucket semantics; no O(N) registry rewrite architecture.
7. Stage 6, Core Primary: only after production latency, correctness, rollback, crash/restart recovery, duplicate suppression, blast radius, capacity, verification, observability, and fallback gates pass.
8. Stage 7, Legacy Retirement: incrementally remove Matrix wake latency, duplicate Planner chains, repeated snapshots, synchronous OMP, per-user processes, global registry rewrites, synchronous expanded closure, and full service verification before recovery where evidence permits.

`NEW_CORE_EARNS_AUTHORITY_THROUGH_EVIDENCE`. Legacy fallback remains until the migration terminal is proven.

Migration gates must explicitly prove writer ownership, fencing, crash recovery across the apply/closure boundary, stale-input behavior, fallback ownership restoration and absence of duplicate effects before expanding from shadow to certification, ordinary user, cohort or Core-primary scope.

## 13. CT-M0F Disposition

Preserve and reuse latency definitions, Time owners/spans, meaningful valid-sample laws, `p95 <=3s` as the initial production gate, and `<1s` as prepared warm-path target. Classify legacy-specific topology/orchestration as `LEGACY_ONLY` or `REDESIGN` after audit. Remote client-agent work remains deferred and cannot block core engineering. CT-M0F may not enlarge the frozen legacy hot path.

## 14. Reset Execution Rules

Until RESET-M0 through RESET-M3 are complete, no other Program may begin new routing implementation. Natural L8 waits do not block reset. Polygon is limited to audit/scenario support without Runtime mutation. Critical production safety fixes remain allowed. Existing active Programs are neither deleted nor mass-rewritten; RESET-M0/M1 owns disposition.

RESET-M4 requires both a `FUNCTIONAL_GATE` and `COMPLEXITY_GATE`. Before implementation it locks the approximately 5-7 module, 2,500-5,000 LOC, one-process-unless-better-proven, 3-5-state-surface budget. Material excess triggers `WHY_DID_CORE_COMPLEXITY_EXCEED_BUDGET?` architecture review; legacy abstractions receive no automatic admission.

RESET-M5 treats legacy as evidence, not an unconditional oracle. Every divergence is classified `LEGACY_CORRECT`, `CORE_CORRECT`, `BOTH_LEGAL`, `BOTH_WRONG`, or `INSUFFICIENT_EVIDENCE` using current policy/truth, Product Contract, Polygon, and production evidence.

RESET-M6 separately measures detection, state update, selection, policy/safety validation, apply, kernel visibility, payload verification, and total server-controlled cutover, plus subprocesses, reads/writes, locks, probes, process starts, and O(N) work. Production PASS requires correctness, latency, and bounded complexity; CT-M0F/Time remains acceptance corpus.

RESET-M6 may not redefine the recovery clock established in RESET-M3. Initial production admission requires end-to-end `p95 <= 3 s` with no valid sample above the declared `5 s` hard ceiling under its exact contract. Samples cannot be repeated merely to accumulate evidence after the property is already proven.

RESET-M7 targets at least 10k users and 50 egresses using approved semantic classes/buckets, generation binding, bounded target/bucket commit, and exception overlays only where required. `CONSTANT_TIME` requires measured independence from user count inside declared bounds; O(N) global registry rewriting cannot be the cohort architecture.

RESET-M7 must prove the prepared compatible warm path end-to-end at `p95 < 1 s`, with an explicit hard ceiling, across the declared scale envelope. Evaluation without PASS is a residual, not Program completion. Cohort performance cannot be obtained by hiding per-user serialization, hashing, audit expansion, verification or registry rewriting behind another process.

RESET-M9 canonical name is `LEGACY_RETIREMENT_SYSTEM_SHRINK_AND_PROGRAM_CLEANUP`. Every legacy file, function, module, CLI, service, timer, state surface, owner, Program, projection, and reconciliation path receives `STILL_REQUIRED`, `LEGACY_EXCEPTION_REQUIRED`, `MERGE`, or `DELETE`. Retirement is incomplete when unneeded permanent code merely becomes uncalled. Measure LOC/files/owners/processes/timers/state surfaces/hops/duplicate responsibilities removed while retaining necessary historical evidence.

## 15. Program Phases and Completion Contracts

| Phase | Contract | Exact successor |
| --- | --- | --- |
| `RESET-M0` | Immutable scope snapshot, exhaustive portfolio coverage ledger, exact broken links, Intent Reality verdicts and Program-to-product relationship coverage complete with no undisposed object. | `RESET-M0B` |
| `RESET-M0B` | Production entrypoint/function/dynamic-dispatch reachability, real cross-component call/state/effect graph and responsibility manifest complete with semantic large-file dispositions and baseline metrics. | `RESET-M0C` |
| `RESET-M0C` | Duplication/dead/legacy surface and broken/orphan/circular relationship dispositions complete without deletion; every removal candidate has semantic preservation and reachability evidence requirements. | `RESET-M1` |
| `RESET-M1` | Component-level Program portfolio dispositions accepted, including acceptance-only contracts. | `RESET-M1B` |
| `RESET-M1B` | OMP/development-system failure causes and exact protection supersession/conflict rules accepted; Master Audit Report reconciles every Program goal and scoped relationship, resolves contradictions, reaches root causes and passes final self-review. | `RESET-M2` |
| `RESET-M2` | One owner per necessary runtime fact and state-surface collapse dispositions complete. | `RESET-M3` |
| `RESET-M3` | vNext positive/negative contracts, exact recovery clock, freshness decisions, single-writer/fencing, apply-to-closure crash recovery, preserve/exclude matrix and complexity budget accepted before code. | `RESET-M4` |
| `RESET-M4` | Effect-free Shadow Core passes functional and complexity gates. | `RESET-M5` |
| `RESET-M5` | Classified decision equivalence and Polygon validation consumed without reproducing proven legacy defects. | `RESET-M6` |
| `RESET-M6` | Certification-user and one-user production correctness, latency and bounded-complexity proof consumed. | `RESET-M7` |
| `RESET-M7` | Bounded cohort, declared constant-time architecture and prepared compatible warm-path `p95 < 1 s` proven without hidden O(N) work. | `RESET-M8` |
| `RESET-M8` | Core-primary production promotion gates proven with safe fallback. | `RESET-M9` |
| `RESET-M9` | Legacy primary path retired, system physically shrunk, obsolete Programs/code merged/closed/deleted with evidence retained, and final Program Completion Report proves every RESET-M0-M9 goal owner-backed. | Program completion evaluation |

Every phase must identify exact intent, owner, evidence contract, completion contract, next consumer, exact successor, complexity impact, Product Contract impact, producer, output, real consumer, behavior/effect evidence, durable state projection, real cross-component/function relationships, and exact residual. Code/tests/reports alone do not close a phase. RESET-M0 through RESET-M1B cannot collectively close until the unified Master Audit Report passes goal coverage, contradiction, root-cause depth, Product Contract trace and final self-review gates.

## 16. Final Completion

Completion requires an owner-backed explanation of why old V7 failed its Product Contract and which architecture/process causes allowed it; a final self-reviewed Master Audit Report covering every Program goal and real Program/component/function relationship from surface inventory to root cause; proof those causes are absent from vNext; complete audit coverage with no silently lost production-relevant function or semantic contract; reconciled portfolio; obsolete Programs/code closed/merged/removed with necessary meaning preserved; proven redesigned/scoped OMP vNext role; one owner per necessary runtime fact; simple bounded hot path; active complexity budget; production Core primary; end-to-end `<3 s` gate proven; prepared compatible warm path `p95 < 1 s` proven; single-writer/fencing and atomic ownership transfer; rollback/forward recovery and apply-to-closure crash recovery; declared N-independent bounded cohort; retired legacy primary path; explicit exception/fallback; asynchronous Engineering Plane; compact CPS; no duplicated routing truth; and baseline/current/delta complexity evidence showing a smaller primary production surface.

Mandatory final gates: `OLD_FAILURE_CAUSES_NOT_REINTRODUCED = PASS`, `PRIMARY_SYSTEM_SURFACE_REDUCED = PASS`, and `RESET_PROGRAM_COMPLETION_REPORT_ALL_GOALS_OWNER_BACKED_PASS`.

Final terminal: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`.

## 17. Contract-Update Effect Record

This update strengthens only this existing Program contract and its canonical registration semantics. It does not execute RESET-M0/M0B/M0C/M1/M1B, audit code, change dispositions, create a Core, remove legacy, deploy, or change Runtime behavior, routing, users, Authority, migration, or production. Runtime effects: `NONE`. Production effects: `NONE`.

No further pre-execution contract expansion is allowed without a material safety gap, correctness gap or owner-backed invalidator. The next action remains RESET-M0.

Update terminal: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = RESET_PROGRAM_CONTRACT_READY_FOR_EXECUTION`.

This Section 17 terminal is the immutable historical result of the pre-execution contract update. It is superseded for live state only by the executed Program terminal `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`; the contract itself remains the evidence baseline and is not expanded.
