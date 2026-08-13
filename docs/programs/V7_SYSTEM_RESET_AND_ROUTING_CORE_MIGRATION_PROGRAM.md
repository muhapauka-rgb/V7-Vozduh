# V7 System Reset and Routing Core Migration Program

Program ID: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

Status: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`

Program owner: existing `OMP` development-plane orchestrator.

Volatile state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md` (`CPS`).

Production authority: current CPS-backed production Authority state `CORE_PRIMARY_FOR_124_COMPATIBLE_PRODUCTION_USERS_WITH_EXACT_LEGACY_FALLBACK`; this reconciliation does not change Authority.

## Current Program State

Current completed scope: `RESET-M0 -> RESET-M10 COMPLETE`.

Current CPS frontier: `PROGRAM_COMPLETE`; current CPS successor: `NONE_RESET_PROGRAM_TERMINAL`.

Current contract frontier: `RESET-M10 COMPLETE`. CPS consumed the owner-backed whole-production-surface correctness invalidator; M0-M9 evidence remained complete and was not rerun. The final architecture is reconciled through existing canonical owners, with no new Runtime, owner, state or Authority.

### Historical Program Entry Point

First executable phase at Program creation: `RESET-M0`.

Historical exact successor: `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`.

## 1. Purpose and Boundary

This Program is the temporary top-level engineering priority for a full V7 architectural reset and safe migration to a minimal Routing Core. It is not another repair of the current routing path, an immediate rewrite, a Runtime, a second CPS, Planner, Authority owner, registry, queue, watcher, scheduler, store, or truth source. Execution remains inside the existing OMP/CPS lifecycle.

All existing Programs remain until `RESET-M0/RESET-M1` gives each exactly one disposition: `KEEP_PERMANENT`, `KEEP_AS_ACCEPTANCE_CONTRACT`, `MERGE`, `COMPLETE_AND_CLOSE`, `LEGACY_ONLY`, `REDESIGN`, or `REMOVE`. Nothing transfers automatically into V7 vNext.

### Reset Overhead, Necessity and Temporary-Lifecycle Laws

Permanent engineering law: `RESET_OVERHEAD_BUDGET`. Reset is a temporary audit/migration activity, not a new permanent V7 subsystem. Without irreducible necessity it must not create a permanent Runtime, Planner, owner, registry, store, queue, scheduler, watcher, service, timer, state surface, truth owner, reconciliation framework or audit framework. Priority is `EXISTING_OWNER_OR_TOOL -> EXISTING_REPORT_OR_DOCUMENT_PROJECTION -> TEMPORARY_ANALYSIS_SCRIPT -> NEW_CODE_ONLY_IF_IRREDUCIBLY_REQUIRED`. Every Reset-only artifact records purpose, owner, production/non-production class, expected lifetime and `RETAIN`, `MERGE`, `ARCHIVE`, or `DELETE` disposition. Reset tooling never automatically becomes a production component, Runtime dependency or canonical truth owner.

Law: `LOGICAL_OUTPUT_NOT_PHYSICAL_SYSTEM`, with the reporting constraint `LOGICAL_OUTPUT_NOT_DOCUMENTATION_EXPLOSION`. A manifest, matrix, graph, ledger or other required logical output does not imply a separate physical file, document, generator, service, registry, database, framework, state surface or owner. Multiple audit projections must reuse the minimum existing artifacts that preserve coverage, traceability, evidence, owner mapping and disposition; no artifact may be created merely to re-present knowledge already preserved by an existing owner.

Law: `PRESERVE_REQUIRED_BEHAVIOR_NOT_LEGACY_STRUCTURE`. Reset preserves required product semantics, safety, Authority, rollback/recovery, verification, capacity, freshness, anti-flap and compatibility behavior. It does not preserve a legacy class, file, owner, Planner, matrix, snapshot, workflow, state structure or implementation topology merely because that structure exists. Before migration, prove the product intent is necessary, whether it must execute synchronously, whether a dedicated owner is necessary, whether an existing owner can absorb it, and whether a simpler representation preserves the behavior.

Law: `QUESTION_NECESSITY_BEFORE_OPTIMIZING_IMPLEMENTATION`. Before redesign/refactor ask, in order: does the behavior need to exist; must it execute before traffic recovery; does it require a dedicated owner; can an existing owner absorb it; can it be derived or asynchronous; only then redesign implementation. Do not optimize or elegantly rewrite a mechanism that can be removed.

Permanent law: `EXISTING_CAPABILITY_DISCOVERY_BEFORE_IMPLEMENTATION`. New implementation is forbidden until evidence proves that the required capability is absent or that existing behavior and ownership cannot be safely reused, merged, simplified, moved or deduplicated. This law unifies and strengthens the existing OMP Architecture Closed by Default, New Owner Gate, necessity, owner-reuse and duplication controls; it creates no discovery framework, registry, owner, process, document class or approval layer.

Mandatory sequence:

`REQUIREMENT -> EXISTING CAPABILITY SEARCH -> EXISTING OWNER IDENTIFICATION -> EXISTING PRODUCER/CONSUMER ANALYSIS -> REUSE POSSIBILITY -> MERGE POSSIBILITY -> SIMPLIFICATION POSSIBILITY -> MOVE/REMOVE DUPLICATE POSSIBILITY -> ONLY THEN NEW IMPLEMENTATION`.

Before creating or materially extending any code, function, class, file, owner, service, timer, process, state surface, adapter, registry, workflow or architecture component, the implementing Mission must answer through existing repository, owner, test, service, state and contract evidence:

1. Which existing function, module, service or owner already provides all or part of the behavior?
2. Which real producer and consumer already participate, and is the missing link integration rather than implementation?
3. Which existing state surface already contains or can derive the required fact?
4. Which existing Authority, policy, verification, rollback and assignment mechanisms apply?
5. Can the existing owner be reused, merged, simplified or extended without duplicating responsibility?
6. Can existing complexity be removed or moved asynchronous instead of adding another layer?

Required logical evidence record: `REQUESTED_CAPABILITY`, `SEARCHED_EXISTING_SURFACES`, `FOUND_EXISTING_COMPONENTS`, `EXISTING_PRODUCER`, `EXISTING_CONSUMER`, `EXISTING_STATE_AND_AUTHORITY_PATH`, `REUSE_DECISION`, `MERGE_DECISION`, `SIMPLIFICATION_OR_REMOVAL_DECISION`, `WHY_EXISTING_IS_NOT_SUFFICIENT`, and `NEW_COMPONENT_JUSTIFICATION`. It belongs in the existing Mission or concise Engineering Report and must not cause documentation explosion.

Default decision order: `REUSE -> MERGE -> SIMPLIFY -> MOVE -> REMOVE_DUPLICATE -> NEW_IMPLEMENTATION`. New implementation is legal only when existing behavior is absent or provably insufficient, responsibility cannot be lawfully moved into an existing owner, and the proposed component reduces net system complexity. `EXISTING_CAPABILITY + NEW_DUPLICATE_IMPLEMENTATION = ARCHITECTURE_ERROR` by default; overlap requires convergence to one behavior owner, one truth source and one responsibility.

Runtime rule: before adding anything to the Data Plane or Control Plane, explicitly search for and reuse the existing channel-health model, policy validation, Authority boundary, verification, rollback and assignment mechanisms. A second version is forbidden without a proven incompatible semantic boundary and net simplification.

Reset/Codex execution rule: every implementation Mission from RESET-M0 through RESET-M10 and every future change begins with terminal `SEARCH_EXISTING_BEFORE_IMPLEMENTATION`, covering repository code, current owners, functions, tests, services, state surfaces and documentation/contracts. Implementation may not begin from the assumption that a capability is missing. Proposals for a new mechanism, layer, manager or orchestrator fail closed to `EXISTING_CAPABILITY_DISCOVERY_REQUIRED` until the evidence record passes.

Permanent architectural law: `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_MODEL`. Every V7 Program, owner, module, file, service, timer, state surface and Runtime component must declare `PURPOSE`, `OWNER`, `LIFECYCLE`, `INPUTS`, `OUTPUTS`, `REAL_CONSUMERS`, `ALLOWED_DEPENDENCIES`, `FORBIDDEN_DEPENDENCIES` and `REMOVAL_CONDITION`. Implementation existence is not necessity evidence. A component remains admitted only when `PURPOSE + REAL_CONSUMER + REAL_PRODUCT_EFFECT` is proven or when an exact safety, Authority, historical-evidence or migration exception is owner-backed.

Responsibility placement is exclusive: `DATA_PLANE`, `CONTROL_PLANE`, `ENGINEERING_PLANE`, `LEGACY_EXCEPTION` or `REMOVE`. Data Plane owns route application, forwarding-state mutation, client switching and effect verification; it forbids OMP, Reports, Learning, Polygon, Programs, roadmap, development history, maturity and certification-lifecycle dependencies. Control Plane owns channel health/state, policy, capacity, Authority, constraints and preparation of decisions. Engineering Plane owns OMP, Reports, Polygon, Learning, Replay, Research, Analytics and certification history and is forbidden from synchronous client switching.

Mandatory `DELETE_TEST`: for every component ask `WHAT_HAPPENS_IF_WE_DELETE_THIS?` and classify the result as `PRODUCT_BREAK`, `SAFETY_OR_AUTHORITY_BREAK`, `HISTORICAL_EVIDENCE_LOSS`, `OPERATOR_CONVENIENCE_LOSS`, or `NO_MATERIAL_EFFECT`. `NO_MATERIAL_EFFECT` requires `REMOVE` or `ARCHIVE` disposition unless an owner-backed invalidator proves otherwise; convenience alone cannot admit a component to the primary Runtime.

Program lifecycle rule: every Program declares purpose, lifecycle (`PERMANENT`, `TEMPORARY`, `MIGRATION_ONLY`, `COMPLETED`), completion condition and removal/archive condition. A temporary or completed Program and its machinery cannot become a permanent Runtime dependency merely because its artifacts remain. State-surface responsibility rule: every state surface proves necessity, owner, writer, readers, real consumer, product effect, freshness, invalidation and lifecycle, then receives exactly one disposition: `KEEP_AUTHORITATIVE`, `MERGE`, `DERIVE`, `ASYNC_ONLY`, `LEGACY_ONLY` or `REMOVE`.

Permanent architectural law: `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH`. Current truth is separated by responsibility and no layer may own another truth class:

- `RUNTIME TRUTH`: live assignments, health, policy state, Authority state and routing state remain owned by their existing Runtime/Control Plane owners; CPS owns volatile Program/execution state. Architecture documents and Engineering Reports cannot make a Runtime decision or grant Authority.
- `ARCHITECTURE TRUTH`: current component ownership, responsibility boundaries, dependencies, plane placement and production Runtime boundary remain owned by the existing Canonical Reference and `SYSTEM_MAP` topology owners. `FINAL_ARCHITECTURE_MAP` is their reconciled current projection and onboarding reference, not a new owner, Runtime state, Authority source, CPS or independent truth source.
- `HISTORICAL EVIDENCE`: Engineering Reports, completed Programs, experiments and migration records explain why decisions were made and what occurred; they do not define current Runtime behavior, execution state or architecture unless their result is promoted into the existing canonical owner.

Forbidden dependencies are `ENGINEERING REPORT -> RUNTIME DECISION`, `HISTORICAL DOCUMENT -> CURRENT ARCHITECTURE TRUTH`, and `OLD PROGRAM DOCUMENT -> PRODUCTION BEHAVIOR`. The lawful improvement direction is `RUNTIME OUTCOME -> ENGINEERING ANALYSIS -> OWNER-BACKED ARCHITECTURE IMPROVEMENT -> EXISTING CANONICAL OWNER UPDATE`; analysis alone has no Runtime or Authority effect.

Every scoped architecture-bearing document receives exactly one logical status: `CURRENT_ARCHITECTURE_OWNER`, `HISTORICAL_EVIDENCE` or `OBSOLETE_REFERENCE`. Status is a classification in existing canonical/report artifacts, not a registry or document framework. A document without reconciled status cannot be used as current architecture truth. Before creating an architecture map, system diagram, model or truth document, `EXISTING_CAPABILITY_DISCOVERY_BEFORE_IMPLEMENTATION` must search the Canonical Reference, `SYSTEM_MAP`, current architecture projection and their owners; law: `UPDATE_EXISTING_ARCHITECTURE_TRUTH_BEFORE_CREATE_NEW_ARCHITECTURE_ARTIFACT`. A new artifact is legal only when those owners cannot represent a proven necessary distinction and the ordinary necessity gate passes.

Permanent engineering law: `END_TO_END_CHANGE_COMPLETION_GATE`. A change is complete only when its full lifecycle is owner-backed and consumed:

`STARTING STATE -> TARGET STATE -> TRANSITION -> REAL CONSUMER MIGRATION -> VALIDATION -> OLD SURFACE DISPOSITION -> CLEANUP OR OWNER-BACKED EXCEPTION -> NEXT CONSUMER CONSUMPTION -> FINAL OWNER CONFIRMATION`.

`NEW_PATH_WORKS != CHANGE_COMPLETE`. Every material implementation or migration must identify the starting and final files/functions, existing final owner, producer, real consumers, services, timers, state surfaces, configuration, dependencies and Authority boundary; prove how every real consumer moves; validate production behavior and required rollback/recovery; and disposition every superseded surface as exactly one of `KEEP_REQUIRED`, `MERGE`, `ARCHIVE`, `DELETE` or `LEGACY_EXCEPTION`. A new owner, consumer, flow or state surface is never presumed by the target state and remains subject to `EXISTING_CAPABILITY_DISCOVERY_BEFORE_IMPLEMENTATION` and the existing New Owner Gate.

`NO_UNDISPOSITIONED_ORPHANED_SURFACE_AFTER_CHANGE`: a producer without a consumer, consumer without a producer, owner without responsibility, state without a lawful reader, reader without a current owner, service without purpose, timer without a consumer, file without lifecycle, configuration without Runtime usage, obsolete import/startup dependency or silently duplicated old/new path is an `ORPHANED_SURFACE` until dispositioned. Historical evidence, recovery-only state, dormant fallback, external-owner-bound surfaces and bounded migration checkpoints may remain only through an explicit owner, real purpose, lifecycle, consumer/re-entry condition and removal/review condition; they are not automatic deletion targets.

Migration chain closure requires `OLD FUNCTION -> OLD CONSUMERS IDENTIFIED -> NEW OR REUSED FUNCTION READY -> REAL CONSUMERS MIGRATED -> OLD CONSUMERS REMOVED OR EXCEPTED -> OLD FUNCTION DISPOSITIONED`. An old path that still silently works is incomplete unless admitted as an explicit `LEGACY_EXCEPTION` with owner, caller/consumer, safety purpose and removal condition. Cleanup covers code, imports, processes, startup dependencies, state writers/readers, services, timers, configuration, deploy/monitoring surfaces, documentation references and ownership; historical evidence is archived or marked historical rather than erased.

Audit-only phases RESET-M0/M0B/M0C and disposition/design phases RESET-M1/M1B comply by proving complete coverage, decision and disposition; `STRICT_AUDIT_MUTATION_SEPARATION` forbids physical cleanup as an audit side effect. Implementation and migration phases RESET-M2 through RESET-M10, and all future material V7 changes, require evidence-gated physical cleanup after validation or an exact retained exception. Cleanup never precedes the required fallback, rollback, recovery, Authority or consumer-migration gates and creates no cleanup framework, registry, audit system or new owner.

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

Each later phase `RESET-M2` through `RESET-M10` produces its own concise phase Engineering Report linked back to the Master Audit findings and forward to its exact successor. `CONCISE` means compact but evidence-complete: each phase report states what changed, which intent closed, supporting evidence, owner, residual and successor. For every material change it also preserves one logical closure record: `OLD_STATE`, `NEW_STATE`, `TRANSITION`, `VALIDATION`, `CLEANUP_PERFORMED`, `REMOVED_SURFACES`, `RETAINED_EXCEPTIONS`, `FINAL_OWNER`, `FINAL_CONSUMER`, `NEXT_CONSUMER_CONSUMPTION` and `RESIDUAL`. These fields reuse existing evidence and do not require a separate table, file or generator. The report links to, and does not repeat, the full Master Audit Report. At Program completion, one coherent `V7_SYSTEM_RESET_PROGRAM_COMPLETION_REPORT` must reconcile every original Program purpose, phase contract, Master Audit root cause, preserve/exclude decision, migration gate, latency/complexity target, production effect, legacy retirement disposition and system-shrink metric against real owner-backed results.

The final Program Completion Report runs the same goal/coverage/contradiction/root-cause/product-trace self-review over the complete `RESET-M0 -> RESET-M10` lifecycle. Every original goal receives `PROVEN_ACHIEVED`, `PROVEN_NOT_APPLICABLE`, or `NOT_COMPLETE_EXACT_RESIDUAL`; the last verdict forbids Program completion. It must distinguish code, test, caller, consumer, deployed Runtime, production behavior, user effect, Authority, rollback/recovery and physical deletion evidence. Final report terminal: `RESET_PROGRAM_COMPLETION_REPORT_ALL_GOALS_OWNER_BACKED_PASS`.

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

### RESET-M10 — POST_RESET_SYSTEM_SHRINK_AND_RUNTIME_SIMPLIFICATION

RESET-M10 is a bounded final phase of this existing Program, not a new Program, roadmap, owner, CPS, Runtime, Planner, queue, store, truth source or architecture cycle. M0-M9 evidence remains valid and ordered. The owner-backed invalidator for the previous completion scope is that M9 proved kernel/dataplane shrink, while whole-production software/control-plane shrink lacks complete `BEFORE / AFTER / DELTA` evidence.

Every M10 implementation proposal is governed first by `EXISTING_CAPABILITY_DISCOVERY_BEFORE_IMPLEMENTATION`; M10 may not create a replacement merely because the existing surface is large or historically named.

#### RESET-M10.1 — Architecture Responsibility Audit

Apply `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_MODEL` to every scoped current component and answer `WHERE_DOES_THIS_BELONG?` with exactly one of `DATA_PLANE_REQUIRED`, `CONTROL_PLANE_REQUIRED`, `ENGINEERING_PLANE_REQUIRED`, `LEGACY_EXCEPTION` or `REMOVE`. For each, prove purpose, real consumer, product effect, lifecycle and removal condition; run `DELETE_TEST`; trace allowed/forbidden dependencies; and reconcile duplicate responsibility to one owner or an exact owner-backed exception.

This is a bounded projection through the existing M10 Engineering Report and prior Reset coverage ledger, not a new audit framework or inventory restart. `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER` applies.

OMP receives a mandatory boundary audit: OMP is `SYSTEM_DEVELOPMENT_ENGINE`, never `RUNTIME_ROUTING_COMPONENT`. It may analyze problems, select engineering work, map owners, verify changes and improve the system; it may not select a production egress, switch a user, make Runtime health decisions or mutate the dataplane. After stabilization, classify which OMP surfaces remain necessary Engineering Plane tooling and which can be reduced, package-separated, archived or removed.

Every Program receives the Program lifecycle classification, and every state surface receives the state responsibility disposition defined by the global law. This prevents temporary audit, migration or development machinery from silently becoming a permanent production dependency.

Purpose: restore the simple product system `UNUSABLE CHANNEL -> AFFECTED CLIENTS -> HEALTHY CHANNEL SET -> POLICY DECISION -> FAST SWITCH -> VERIFY`, not merely reduce LOC or remove old code. After successful Core migration and legacy-primary retirement, physically reduce the remaining production surface while establishing an explicit `DATA PLANE / CONTROL PLANE / ENGINEERING PLANE` boundary. The disposition order is `REMOVE -> MERGE -> PACKAGE-SEPARATE -> SIMPLIFY`. The controlling question is: `WHY_DOES_A_LARGE_PART_OF_THE_OLD_SYSTEM_STILL_SURROUND_THE_SMALL_ROUTING_CORE_AFTER_SUCCESSFUL_MIGRATION?`

Permanent law: `PRESERVE_SEMANTICS_REMOVE_IMPLEMENTATION`. Preserve required product behavior, safety, Authority, rollback, verification, recovery and compatibility semantics. Do not automatically preserve old files, classes, owners, processes, timers, CLIs, Program machinery or orchestration topology.

Permanent final-gate law: `PRIMARY_SYSTEM_SURFACE_REDUCTION_AS_FINAL_GATE`. `PRIMARY_SYSTEM_SURFACE_REDUCED` applies to the complete production system surface, not only kernel routing. Its evidence compares production LOC, active Runtime LOC, executable files, services, timers, subprocesses, owners, state surfaces, producer-consumer hops, durable writes, locks and routing-specific complexity before and after M10.

#### RESET-M10.2 — Industry Routing Architecture Benchmark

Before optimization, compare current V7 placement against architectural principles from mature routing systems without copying their implementation. Primary benchmark evidence is limited to official Junos Routing Engine/Packet Forwarding Engine separation, Cisco IOS XR control/data-plane and hardware-abstraction boundaries, FRRouting protocol-daemon/zebra/dataplane coordination, and Linux rtnetlink/FIB programming and verification contracts. The benchmark is a bounded Engineering Report section, not a new research Program, framework, owner or permanent artifact.

The benchmark evaluates these V7 boundaries:

- `DATA PLANE`: route application, forwarding-state mutation, fast failover and effect verification only. It must not know history, reports, Learning, Programs, audit or Production Maturity.
- `CONTROL PLANE`: channel state, policy, best-path selection, capacity, constraints, Authority and preparation of the bounded decision.
- `ENGINEERING PLANE`: OMP, Reports, Polygon, Learning, Replay, analysis and system improvement. It must not participate synchronously in client switching.

Every current V7 component receives exactly one architectural placement: `DATA_PLANE_REQUIRED`, `CONTROL_PLANE_REQUIRED`, `ENGINEERING_PLANE_REQUIRED`, `LEGACY_EXCEPTION` or `REMOVE`. Placement requires its real caller, consumer, state/effect contract, synchronous/asynchronous position and removal/replacement evidence.

Benchmark references: [Junos OS Architecture Overview](https://www.juniper.net/documentation/us/en/software/junos/junos-overview/topics/concept/junos-software-architecture.html), [Cisco IOS XR Software](https://www.cisco.com/c/en/us/products/collateral/ios-nx-os-software/ios-xr-software/datasheet-c78-743014.html), [FRRouting Architecture Overview](https://docs.frrouting.org/en/latest/overview.html), and [Linux rt-route netlink specification](https://docs.kernel.org/next/networking/netlink_spec/rt_route.html).

#### RESET-M10.3 — Channel Health Model

Mandatory contract: `CHANNEL_HEALTH_MODEL`. Before any routing decision, the existing channel-health owners must produce one formal `EGRESS_ADMISSION_STATE` with the minimum lifecycle `UNKNOWN -> PROBING -> HEALTHY -> DEGRADED -> UNUSABLE -> RECOVERING -> HEALTHY`. For every state define owner, data source, freshness, invalidation, legal transitions, admission for new clients and continued use by existing clients. This contract consolidates existing health facts; it creates no new health owner or truth source.

Admission must separately account for `TRANSPORT_HEALTH` (tunnel/interface, handshake, transport reachability), `SERVICE_HEALTH` (required services, DNS, HTTPS/TLS and required endpoint checks), `TRAFFIC_QUALITY` (latency, packet loss, stability and degradation), and `CAPACITY_HEALTH` (available resource, lawful load and limits). Ping or TCP success alone never proves client eligibility. A channel is eligible only when the required owner-backed admission criteria are fresh and satisfied.

##### Routing Decision Minimality Contract

Permanent law: `ROUTING_DECISION_MINIMALITY`. Before a successful switch, synchronous work is limited to `failure evidence -> affected users -> healthy eligible targets -> policy validation -> bounded switch -> verification`. Reports, Learning, Replay, Production Maturity, historical reconciliation, full inventory refresh, campaign bookkeeping and expanded evidence generation are `POST_ACTION_ASYNC_WORK` and forbidden as pre-switch dependencies.

#### RESET-M10.4 — Final Primary Runtime Boundary

Mandatory output: `FINAL_PRIMARY_RUNTIME_BOUNDARY`. The target primary production graph contains only `routing runtime + health receipt consumer + policy reader + Authority adapter + dataplane adapter + verification`. Every other element is classified `engineering-only`, `fallback-only`, `historical` or `manual` and physically excluded from the primary Runtime dependency graph.

This phase establishes the boundary and applies `ROUTING_DECISION_MINIMALITY` to it. File size is a signal, not a split instruction; mechanical splitting and unproven new ownership are forbidden.

#### RESET-M10.5 — Engineering Plane Extraction

Apply responsibility-based compression after the Runtime boundary is defined. For `tools/v7_sync_lib.py`, classify CPS synchronization, OMP, Polygon, Service Failure history, deploy/truth and Runtime-support responsibilities by caller, lifecycle, change reason and existing owner. For `tools/v7-users-autoswitch`, retain only proven fallback apply, rollback, verification and safety semantics in the production boundary; isolate planning, history, OMP, campaign, Learning and reconciliation.

Every scoped implementation also receives packaging class `runtime_required` or `engineering_only`. The production package must not require OMP, Reports, Polygon, Learning, Replay, Production Maturity or historical reconciliation. No second Engineering Plane is created.

#### RESET-M10.6 — Fast Path / Reconciliation Path Separation

Prove the mandatory split:

- `FAST PATH`: `failure event -> prepared health receipt -> Routing Core -> switch -> verify`.
- `RECONCILIATION PATH`: `periodic scans -> audit -> reconciliation -> reports -> learning`.

The slow path cannot be a failover prerequisite. Full Matrix refresh, periodic inventory and historical reconciliation remain asynchronous; existing observation/reconciliation owners change only through an owner-backed `MERGE`, `ARCHIVE` or `DELETE` disposition.

#### RESET-M10.7 — Dataplane Adapter Simplification

Evaluate the reduction from `Core -> legacy writer -> scripts/processes -> kernel` to `Core -> minimal dataplane adapter -> kernel`. The goal is fewer synchronous levels between decision and forwarding state, not deletion of a writer by name. Replacement is legal only when measured complexity falls and fencing, idempotency, rollback and verification remain owner-backed; working architecture is not replaced for aesthetic purity.

#### Final V7 Target Architecture Acceptance Contract

The final architecture must prove:

- `Runtime`: one understandable routing Runtime, minimum necessary processes and no OMP/report/history dependency.
- `Control Plane`: channel health, policy, capacity, Authority and assignment state.
- `Engineering Plane`: OMP, Polygon, Reports, Learning and Replay, physically and synchronously separate from switching.

Final routing flow: `CHANNEL FAILURE -> AFFECTED CLIENTS -> HEALTHY CHANNEL SET -> POLICY DECISION -> FAST SWITCH -> VERIFY`, with no intermediate Engineering Plane system. Its implementation must retain the already accepted `OBSERVE -> STATE -> PLAN -> APPLY -> VERIFY` Core contract.

#### RESET-M10.8 — Final System Complexity Audit

Classify every production service, timer, startup dependency, subprocess launch, CLI, fallback layer, state surface and legacy adapter as `STILL_REQUIRED`, `LEGACY_EXCEPTION_REQUIRED`, `MERGE`, `ARCHIVE` or `DELETE`. Age is not evidence; removal requires caller/consumer, replacement semantics and rollback/recovery proof. Reconcile governed Packet/lease/barrier, `v7-users-autoswitch`, `v7-user-switch`, legacy fallback and old Planner surfaces so only required fallback, safety, rollback, verification and compatibility remain production-admitted.

Produce one concise existing-type Engineering Report with `BEFORE / AFTER / DELTA` for production LOC, Runtime LOC, executable files, services, timers, subprocess count, owners, state surfaces, pre-apply hops, durable writes, lock domains, routing-specific complexity and duplicated responsibilities. Separately count `LEGACY_SURFACE_NOT_ADMITTED_TO_FINAL_RUNTIME`, link every retained exception to a caller/consumer and preserve deep evidence in existing owners rather than create a new audit framework.

M10 physical shrink must prove both `NEW_ARCHITECTURE_COMPLETE` and `OLD_ARCHITECTURE_CLOSED`. The cleanup pass occurs only after the new path and its real consumers are validated; it checks superseded code, imports, services, timers, startup/configuration entries, state surfaces, writers/readers, owners, deploy/monitoring hooks and documentation references. Every remainder receives an explicit disposition, and no unclassified old routing path or orphaned surface may survive around the Core.

#### RESET-M10.9 — FINAL_ARCHITECTURE_MAP

Produce `FINAL_ARCHITECTURE_MAP` as one final decision-oriented section of the existing M10 Engineering Report. It is a generated projection of the already required M10 responsibility, dependency, flow, ownership and disposition evidence, not a new Runtime artifact, owner, truth source, registry, service, audit framework, file class or parallel document. Its test is whether a new engineer can understand the final V7 architecture, ownership and operating flow within minutes without treating historical reports as live architecture.

The map must contain:

1. `RUNTIME LAYER`: only continuously operating production components and the flow `CLIENT TRAFFIC -> ROUTING RUNTIME -> DATAPLANE APPLY -> VERIFY`; for each component record purpose, existing owner, input, output, real consumer and lifecycle.
2. `CONTROL PLANE LAYER`: health, admission state, policy, capacity, Authority, assignments and target eligibility, showing `CHANNEL HEALTH -> ADMISSION STATE -> POLICY -> TARGET SELECTION` and answering how a channel becomes eligible.
3. `ENGINEERING PLANE LAYER`: OMP, Reports, Polygon, Learning, Replay and Research; for each record purpose, real consumer, lifecycle and why it is outside Runtime. Engineering Plane may improve the system but may not participate synchronously in client switching.
4. `LEGACY EXCEPTION LAYER`: every retained exception with component, reason, existing owner and removal condition, explicitly marked `NOT PRIMARY`, `NOT CORE DEPENDENCY` and `TEMPORARY COMPATIBILITY` unless an owner-backed permanent safety obligation proves otherwise.
5. `FINAL RUNTIME DEPENDENCY GRAPH`: Runtime may depend only on the admitted Health Receipt, Policy, Authority, Assignment, Dataplane and Verification contracts; it must not depend on OMP, Reports, Learning, Replay, History, Campaigns or Certification.
6. `FINAL DATA FLOW`: `CHANNEL FAILURE -> AFFECTED CLIENTS -> HEALTHY CHANNEL SET -> POLICY DECISION -> FAST SWITCH -> VERIFY -> ASYNC OUTCOME`. The inverse dependency `CHANNEL FAILURE -> ENGINEERING SYSTEMS -> REPORTS/ANALYSIS -> ROUTING` is forbidden.
7. `OWNERSHIP MATRIX`: map Channel health to Control Plane, routing decision to Runtime, route apply to Data Plane, verification to Runtime/Data Plane, policy to Control Plane and engineering improvement to Engineering Plane, using the proven canonical owner name for each responsibility. Each responsibility has exactly one owner; the matrix creates none.
8. `DEPENDENCY RULES`: Control Plane inputs may feed Runtime decisions and Engineering Plane may consume Runtime observations/outcomes asynchronously; Engineering Plane decisions and Reports/history/Learning may not feed a live routing decision.
9. `FINAL DELETE/REVISIT LIST`: classify every mapped item as `KEEP`, `LEGACY_EXCEPTION`, `REMOVED` or `FUTURE_REVIEW`, with retained exceptions and future reviews linked to owner and removal/revisit condition.

The map reuses `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_MODEL`, `FINAL_PRIMARY_RUNTIME_BOUNDARY`, the M10 coverage ledger and final complexity dispositions. `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER` applies: it must not repeat evidence or reopen proven areas merely to draw the final view.

Before M10 completion, execute `ARCHITECTURAL_TRUTH_RECONCILIATION` through the existing M10 report and canonical owners. Prove that the map matches deployed Runtime, named owners match factual ownership, all production dependencies are represented, every legacy exception has its reason and removal condition, no conflicting document claims current architecture, and no historical Program/Report appears to be the live execution contract. Classify each scoped architecture-bearing document as `CURRENT_ARCHITECTURE_OWNER`, `HISTORICAL_EVIDENCE` or `OBSOLETE_REFERENCE`; promote the resulting current architecture only through the existing Canonical Reference/`SYSTEM_MAP` owners.

#### RESET-M10 Execution Order and Stage Contracts

M10 uses the existing OMP/CPS and concise Engineering Report lifecycle; this table is the complete internal dependency order, not a new management system. The existing Program/OMP owner coordinates every stage, while each referenced canonical component owner retains its existing responsibility and Authority boundary.

| Stage | Purpose | Inputs | Output | Owner | Completion criteria | Exact successor | Residual on failure |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RESET-M10.1` | Classify what exists, why it exists and where it belongs. | Reused Reset coverage ledger, current production graph, canonical owners. | Exclusive placement and responsibility disposition. | Existing Program/OMP coordinator plus each existing component owner. | Every scoped component has placement, owner, consumer, lifecycle and removal condition. | `RESET-M10.2` | Exact unclassified component or owner/evidence gap. |
| `RESET-M10.2` | Compare the classified V7 architecture with mature routing principles without copying implementations. | M10.1 placements and official benchmark references. | Bounded placement/architecture comparison. | Existing Program/OMP engineering owner. | Every material V7 boundary has a supported comparison or explicit non-applicability disposition. | `RESET-M10.3` | Exact unsupported boundary conclusion. |
| `RESET-M10.3` | Define why a channel is eligible. | Existing health, policy, capacity, Authority and assignment evidence. | Owner-backed `EGRESS_ADMISSION_STATE` contract. | Existing channel-health and related canonical owners. | Owner, freshness, invalidation, transitions and admission rules are complete. | `RESET-M10.4` | Exact missing health fact, transition, owner or consumer. |
| `RESET-M10.4` | Define the minimum primary production Runtime and routing-decision boundary. | M10.1-M10.3 dispositions and admission contract. | `FINAL_PRIMARY_RUNTIME_BOUNDARY` and allowed dependency graph. | Existing Routing Core, policy, Authority, assignment, dataplane and verification owners. | Runtime dependency graph is defined and Engineering Plane is excluded from live decisions. | `RESET-M10.5` | Exact unknown or forbidden Runtime dependency. |
| `RESET-M10.5` | Physically classify and extract engineering, fallback and historical responsibilities from Runtime packaging. | M10.4 boundary and current caller/consumer/package evidence. | `runtime_required`, `engineering_only`, `fallback_only` or `historical` classification and bounded changes. | Existing Runtime/component and Engineering Plane owners. | Every scoped dependency is classified and no Engineering Plane dependency remains production-required. | `RESET-M10.6` | Exact dependency not yet separated or safely retained. |
| `RESET-M10.6` | Separate fast failover from slow reconciliation. | M10.3 health receipt and M10.4-M10.5 Runtime boundary. | Proven fast-path and asynchronous reconciliation-path graph. | Existing Runtime, observation and reconciliation owners. | Slow path is not a failover dependency. | `RESET-M10.7` | Exact synchronous slow-path dependency. |
| `RESET-M10.7` | Reduce dataplane apply levels only when safety and net simplification are proven. | M10.4 boundary, current apply graph, fencing, rollback and verification evidence. | Retained or simplified dataplane adapter disposition. | Existing dataplane writer/adapter and verification owners. | Complexity falls without loss of fencing, idempotency, rollback or verification, or retention is justified. | `RESET-M10.8` | Exact safety/complexity criterion preventing simplification. |
| `RESET-M10.8` | Measure the final physical system after bounded changes. | M10.1 baseline and M10.3-M10.7 results. | Whole-production `BEFORE / AFTER / DELTA` and final dispositions. | Existing Program/OMP report owner consuming canonical evidence owners. | All required complexity dimensions and retained exceptions are reconciled. | `RESET-M10.9` | Exact unmeasured dimension, unknown dependency or unjustified residual. |
| `RESET-M10.9` | Project and canonically reconcile the already proven final architecture for decisions and onboarding. | M10.1-M10.8 evidence, final production graph and existing canonical architecture owners. | `FINAL_ARCHITECTURE_MAP` section plus canonical-owner reconciliation. | Existing Program/OMP report owner; Canonical Reference/`SYSTEM_MAP` owners remain authoritative. | `FINAL_ARCHITECTURE_MAP_COMPLETE = PASS` and `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS`. | M10 completion evaluation | Exact unmapped or conflicting component, owner, boundary, dependency, document status or legacy condition. |

No stage advances on headings, code, tests or report existence alone. Its report entry must state purpose, consumed inputs, output, owners, completion evidence, exact residual and successor. Failed or unproven criteria return only to their exact responsible stage; already proven stages are reused unless an exact invalidation trigger applies.

#### RESET-M10 Completion Contract

RESET-M10 completes only when owner-backed evidence proves all of:

1. `DATA PLANE / CONTROL PLANE / ENGINEERING PLANE` are explicitly classified and separated.
2. `CHANNEL_HEALTH_MODEL` is the single admission method for channel eligibility and composes transport, service, traffic-quality and capacity health.
3. The routing decision has no synchronous Engineering Plane dependency.
4. `FINAL_PRIMARY_RUNTIME_BOUNDARY` is defined and physically reflected in production packaging/dependencies.
5. Fast path and reconciliation path are separate.
6. Production Runtime surface is measurably reduced or every residual has an exact necessary owner-backed exception.
7. No hidden OMP, report, history, Learning, campaign or audit dependency remains in primary routing.
8. Final production flow conforms to `OBSERVE -> STATE -> PLAN -> APPLY -> VERIFY` and the product flow `failure -> affected clients -> healthy set -> policy -> fast switch -> verify`.
9. `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_PASS`: every retained component has exclusive plane placement, purpose, owner, consumer, product effect, lifecycle, dependency boundary and removal condition; every duplicate has one owner or an exact exception.
10. OMP is proven Engineering Plane only, every Program lifecycle is reconciled, and every state surface has one final responsibility disposition.
11. `FINAL_ARCHITECTURE_MAP_COMPLETE = PASS`: every production Runtime component is mapped, every responsibility has one understandable existing owner, every plane boundary is explicit, no unknown production or hidden Engineering Plane dependency remains, and every legacy exception has a reason and removal condition.
12. `END_TO_END_CHANGE_COMPLETION_PASS`: the new architecture and its real consumers are proven, the old architecture is closed or explicitly retained, no undispositioned orphaned surface or migration tail remains, the final owner/lifecycle is known, and every stage output is demonstrably consumed by its named next consumer.
13. `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS`: Runtime truth retains its factual owners, current architecture is reconciled through the existing Canonical Reference/`SYSTEM_MAP` owners and matches production, historical evidence is separate, no conflicting current architecture description remains, and future changes have one existing architecture owner to update.

M10 completion therefore requires together: physical reduction of the production surface; separation of Data Plane, Control Plane and Engineering Plane; an owner-backed `CHANNEL_HEALTH_MODEL`; a production-reflected `FINAL_PRIMARY_RUNTIME_BOUNDARY`; and a complete `FINAL_ARCHITECTURE_MAP`.

Completion evidence must include real caller/consumer and deployed production effects for physical changes; code, tests, reports, diagrams or classifications alone cannot close M10.

RESET-M10 forbids a new Core, unnecessary Core expansion, a new Program/audit framework/owner/Runtime/Planner/queue/store/truth source, OMP or Reports/Learning/Replay in the Runtime hot path, mass mechanical refactoring, or replacement of working architecture without necessity evidence.

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
| `RESET-M9` | Legacy primary path retired and kernel/dataplane surface physically shrunk with explicit fallback and evidence retained. | `RESET-M10` |
| `RESET-M10` | Remaining production software/control-plane surface is owner-classified and physically reduced or isolated; Engineering Plane is excluded from the primary Runtime graph; the new architecture is complete, the old architecture is closed or explicitly retained, and `FINAL_RUNTIME_SIMPLIFICATION_PASS`, `FINAL_ARCHITECTURE_MAP_COMPLETE`, `END_TO_END_CHANGE_COMPLETION_PASS` and `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS` are proven. | Program completion evaluation |

Every phase must identify exact intent, owner, evidence contract, completion contract, next consumer, exact successor, complexity impact, Product Contract impact, producer, output, real consumer, behavior/effect evidence, durable state projection, real cross-component/function relationships, and exact residual. Code/tests/reports alone do not close a phase. RESET-M0 through RESET-M1B cannot collectively close until the unified Master Audit Report passes goal coverage, contradiction, root-cause depth, Product Contract trace and final self-review gates.

## 16. Final Completion

Completion requires an owner-backed explanation of why old V7 failed its Product Contract and which architecture/process causes allowed it; a final self-reviewed Master Audit Report covering every Program goal and real Program/component/function relationship from surface inventory to root cause; proof those causes are absent from vNext; complete audit coverage with no silently lost production-relevant function or semantic contract; reconciled portfolio; obsolete Programs/code closed/merged/removed with necessary meaning preserved; proven redesigned/scoped OMP vNext role; one owner per necessary runtime fact; simple bounded hot path; active complexity budget; production Core primary; end-to-end `<3 s` gate proven; prepared compatible warm path `p95 < 1 s` proven; single-writer/fencing and atomic ownership transfer; rollback/forward recovery and apply-to-closure crash recovery; declared N-independent bounded cohort; retired legacy primary path; explicit required fallback; asynchronous and physically separated Engineering Plane; compact CPS; no duplicated routing truth; unnecessary owners/processes/state surfaces removed or isolated; and baseline/current/delta complexity evidence showing a smaller whole production Runtime surface, not only a smaller kernel/dataplane surface.

Mandatory final gates: `OLD_FAILURE_CAUSES_NOT_REINTRODUCED = PASS`, `PRIMARY_SYSTEM_SURFACE_REDUCED = PASS`, `FINAL_RUNTIME_SIMPLIFICATION_PASS = PASS`, `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_PASS = PASS`, `FINAL_ARCHITECTURE_MAP_COMPLETE = PASS`, `END_TO_END_CHANGE_COMPLETION_PASS = PASS`, `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS = PASS`, and `RESET_PROGRAM_COMPLETION_REPORT_ALL_GOALS_OWNER_BACKED_PASS`.

Final terminal: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`.

## 17. Contract-Update Effect Record

This update strengthens only this existing Program contract and its canonical registration semantics. It does not execute RESET-M0/M0B/M0C/M1/M1B, audit code, change dispositions, create a Core, remove legacy, deploy, or change Runtime behavior, routing, users, Authority, migration, or production. Runtime effects: `NONE`. Production effects: `NONE`.

No further pre-execution contract expansion is allowed without a material safety gap, correctness gap or owner-backed invalidator. The next action remains RESET-M0.

Update terminal: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = RESET_PROGRAM_CONTRACT_READY_FOR_EXECUTION`.

This Section 17 terminal is the immutable historical result of that pre-execution contract update. It was superseded for live state by the executed M0-M9 terminal; Section 18 records the later bounded correctness-gap amendment without rewriting this historical record.

## 18. RESET-M10 Contract-Amendment Effect Record

The whole-production-surface evidence gap is the material correctness invalidator permitting this bounded amendment. This update defines and internally orders RESET-M10 inside the existing Program and strengthens the final completion gate; it does not execute M10, reopen or reorder M0-M9 evidence, delete or refactor code, change Runtime, routing, production, Authority, owners or Core architecture, or automatically change CPS/current successor. CPS remains the sole volatile state owner and requires a separate owner-backed transition before any M10 execution.

Runtime effects: `NONE`. Production effects: `NONE`. Routing effects: `NONE`. Authority effects: `NONE`.

Reconciliation terminal: `RESET_PROGRAM_CONTRACT_RECONCILED_FOR_M10_EXECUTION`. No further pre-execution architectural expansion is legal without a material safety gap, correctness gap or owner-backed invalidator.
