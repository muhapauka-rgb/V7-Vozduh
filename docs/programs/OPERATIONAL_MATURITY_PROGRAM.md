# V7 Operational Maturity Program

Status: `ACTIVE`
Program: `Operational Maturity`
Created: 2026-06-25
Version: `3.0`
V2.1 baseline reference commit: `7687d506a4a14bf6aed39aa15efd00462b96d980`
Runtime architecture certification commit: `39c46ed379ff4a2ccadb84a49a0dd9dcd2de579b`

This document is the primary program source for V7 implementation work. It replaces roadmap-driven development, phase-first development, free-form implementation ideas, and architecture-first continuation with optimization-driven production implementation.

Roadmaps, reports, ADRs, and reference files remain evidence and context. This program decides the current system state, highest bottleneck, highest leverage action, authority boundary, reality limit, next best action, and whether Codex may continue automatically.

V3 operating question:

```text
What implementation gives the highest production leverage right now?
```

V2.1 adds architectural minimalism, semantic reuse, a new-owner gate, architecture duplication detection, and an explicit optimization engine. V2.2 adds Safety-Bounded Authority: trust decides autonomy tier, safety decides bounded action. V2.3 adds Kernel and State Split: permanent operating rules live in Kernel/OMP, volatile current state lives in Current Program State. V3.0 closes architecture-first work and activates implementation-first optimization. OMP always wins over free-form implementation ideas.

## 1. Project Vision

V7 is an event-driven autonomous routing control plane that protects user connectivity by observing production reality, selecting safe routes through existing owners, acting only under certified authority, verifying outcomes, and learning from real evidence.

This vision is immutable unless a future ADR explicitly supersedes it.

## 2. Program Principles

1. Reality First.
2. Discover -> Reuse -> Extend -> Implement.
3. No duplicate owners.
4. No duplicate planners.
5. No duplicate governance.
6. No synthetic evidence.
7. Tests before certification.
8. Certification before next phase.
9. Documentation after implementation.
10. Continue automatically when possible.

Operational meaning:

- Reports preserve evidence.
- Canonical reference preserves current truth.
- ADRs preserve decisions.
- This program preserves what V7 does next.

## 2.1. Kernel and State Split

V7 separates permanent operating rules from volatile current state.

| Layer | File | Purpose |
| --- | --- | --- |
| V7 Kernel | `docs/reference/V7_KERNEL.md` | Permanent Codex operating contract. |
| OMP | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Scheduler and optimizer. |
| Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Volatile current bottleneck, HLA, packet, authority boundary, metrics, stop reason, and next automatic action. |
| Canonical Reference | `docs/reference/V7_CANONICAL_REFERENCE.md` | Current system truth. |
| SYSTEM_MAP | `docs/reference/SYSTEM_MAP.md` | Owner/topology map. |
| ADRs | `docs/decisions/` | Accepted decisions. |
| Reports | `docs/reports/` | Evidence and history. |
| Runtime | production/runtime state | Reality and final verification. |

Current volatile state lives in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

OMP must not become a dumping ground for every packet or state update.

Long packet/state payloads belong in Current Program State. OMP should keep only scheduler/optimizer rules and pointers unless scheduler meaning changes.

`Continue OMP` means: read Kernel, read OMP, read Current Program State, execute the optimizer loop, continue through safe work, and stop only at an allowed stop condition.

## 2.1.1. Implementation Phase Rule

Architecture Phase is complete.
Research Phase is complete.
Decision Model is complete.
Runtime Model is complete.
System Architecture is complete.

From V3.0 forward, OMP optimizes implementation, not architecture.

The implementation optimizer asks:

```text
What implementation gives the highest production leverage right now?
```

OMP must not ask:

```text
What architecture is missing?
```

Architecture redesign, planner redesign, governance redesign, execution redesign, Runtime redesign, new truth sources, synthetic evidence, and new owners are forbidden unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

Implementation-first means:

1. choose the highest production-leverage implementation;
2. reuse the existing owner;
3. extend the existing owner only when required;
4. implement the smallest safe increment;
5. test;
6. verify;
7. certify;
8. update Current Program State;
9. update OMP only if optimizer meaning changed;
10. continue automatically until an allowed stop condition.

Reference program: `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`.
Reference model: `docs/reference/V7_IMPLEMENTATION_MODEL.md`.

## 2.2. Safety-Bounded Authority Model

V7 must not wait for global self-trust before every small governed action.

V7 separates:

- Knowledge Maturity
- Execution Authority

Knowledge Maturity controls autonomy tier progression.

Execution Authority controls whether an exact bounded action may happen.

Core rule:

```text
Trust decides autonomy tier.
Safety decides bounded action.
```

Knowledge Maturity answers:

```text
How autonomous may V7 become?
```

Execution Authority answers:

```text
May this exact bounded action happen now?
```

`70/70/70` remains the hard floor for `TIER_2+` and autonomous progression.

It is not a universal blocker for a `TIER_1` governed one-user operator-reviewed canary.

A `TIER_1` governed action may be considered only when:

- exact packet exists;
- target user is bound;
- target channel is bound;
- rollback target exists;
- restore barrier preview is ready;
- verification plan is ready;
- outcome closure plan is ready;
- learning path is connected;
- blast radius is bounded;
- policy allows the action;
- truth/convergence pass;
- explicit operator approval exists.

This model does not authorize restore-barrier writes, runtime apply, user movement, rollback apply, daemon/timer enablement, authority expansion, floor changes, synthetic evidence, or new owners.

## 2.3. Background Builds Knowledge, Runtime Spends Knowledge

Background systems may perform expensive work:

- service intelligence;
- quality snapshots;
- prediction;
- trust;
- suitability;
- recovery;
- history;
- learning;
- evidence inventory.

Runtime must remain thin.

Runtime path:

```text
Event
  -> Current State
  -> Knowledge Snapshot
  -> Policy
  -> Safety Check
  -> Packet
  -> Execute or Stop
  -> Verify
  -> Rollback if needed
  -> Outcome Closure
  -> Learning
```

Runtime must not perform broad audits, broad historical recomputation, or heavy analytics in the event path.

Scaling rule:

V7 must scale to `10,000+` users by precomputing knowledge into compact read models.

Adding users must not linearly increase event-time decision latency.

## 2.4. Architectural Laws

These laws are immutable unless a future ADR explicitly supersedes them:

| Law | Rule |
| --- | --- |
| Law 1 | Reality First. |
| Law 2 | Reuse before Extend. |
| Law 3 | Extend before Create. |
| Law 4 | No duplicate systems. |
| Law 5 | No duplicate owners. |
| Law 6 | No duplicate planners. |
| Law 7 | No duplicate governance. |
| Law 8 | No duplicate execution. |
| Law 9 | No synthetic evidence. |
| Law 10 | Every implementation must increase at least one of: Knowledge, Decision Quality, Outcome Quality, Learning Quality, Operational Maturity, or Automation. Otherwise the implementation should not exist. |

## 2.5. Project Philosophy

V7 is not allowed to become larger unless it first becomes smarter.

This means new architecture is a last resort. The default posture is to make existing owners more capable, more connected, more explainable, and more mature.

## 2.6. Architectural Minimalism

Immutable project law:

A new architectural component may appear only after proving that existing architecture cannot provide the same capability through extension.

Creation priority:

```text
Reuse
  -> Extend
  -> Merge
  -> Implement
  -> Create New
```

New components are forbidden until reuse, extension, and merge options have been explicitly evaluated.

## 2.7. Semantic Reuse Audit

Before every implementation, OMP must execute this audit:

| Step | Requirement | Output |
| --- | --- | --- |
| 1 | Find existing owners. | Owner list. |
| 2 | Find semantically equivalent owners, regardless of name. | Semantic owner list. |
| 3 | Find combinations of existing owners that together already implement the desired capability. | Composition strategy. |
| 4 | Estimate semantic coverage. | Coverage %, owner list, reuse strategy, extension strategy. |
| 5 | Allow new owner only if semantic coverage is insufficient. | `Need New Owner = TRUE/FALSE`. |

Current semantic reuse audit for OMP V2.1:

| Field | Current Value |
| --- | --- |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | Canonical reference, SYSTEM_MAP, certified reports, ADRs |
| Composition strategy | Extend existing OMP and update reference pointers only |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as the permanent program owner |
| Extension strategy | Add V2.1 optimizer/minimalism/gate/detector sections in place |
| Need New Owner | `FALSE` |

Current semantic reuse audit for OMP V2.2:

| Field | Current Value |
| --- | --- |
| Desired capability | Add Safety-Bounded Authority as the operating model for separating Knowledge Maturity from Execution Authority. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | `docs/reference/V7_ENGINEERING_PRINCIPLES.md`, Canonical Reference, SYSTEM_MAP, Autonomy Blueprint, Ideal Autonomous Routing Model, Knowledge Quality Model, ADR-V7-SAFETY-BOUNDED-AUTHORITY |
| Composition strategy | Extend existing OMP in place and align it with the existing principles/reference/ADR documents. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as execution authority; reuse principles/reference/ADR as meaning sources. |
| Extension strategy | Add Safety-Bounded Authority, background/runtime split, safe automatic preparation rule, and Codex execution contract to OMP. |
| Need New Owner | `FALSE` |

Current semantic reuse audit for OMP V2.3:

| Field | Current Value |
| --- | --- |
| Desired capability | Separate permanent Codex operating contract and volatile OMP state from stable scheduler/optimizer rules. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | OMP, Canonical Reference, SYSTEM_MAP, ADRs, handoff files, Engineering Principles |
| Composition strategy | Extend OMP in place, add Kernel as the permanent Codex operating contract, add Current Program State as volatile program state, and keep runtime/code owners unchanged. |
| Semantic coverage | `100%` for documentation/control-plane structure |
| Reuse strategy | Reuse OMP as scheduler/optimizer; reuse handoff/current snapshot values as state evidence; reuse reference/ADR map for truth. |
| Extension strategy | Add Kernel/State split section, add pointers, and move volatile packet/state details out of OMP into `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Need New Runtime Owner | `FALSE` |

Latest semantic reuse audit for optimizer iteration `2026-06-25`:

| Field | Current Value |
| --- | --- |
| Desired capability | Validate the current highest leverage action and execute any safer maturity-gaining portion before authority boundary. |
| Existing owners found | `v7-autonomy-trust-evidence-inventory`, `v7-governed-canary-dry-run-cycle`, `v7-egress-quality-compact`, `v7-service-matrix-refresh-all`, `v7-intelligence-snapshot-refresh`, existing packet/restore/verification/outcome/learning owners. |
| Semantic equivalent owners | Existing service matrix / quality snapshot owners cover service verification and freshness; existing governed canary dry-run covers packet/restore/outcome/learning preview; existing inventory covers OMP recalculation. |
| Composition strategy | Recalculate with inventory, challenge with governed dry-run, execute only existing service/quality/snapshot refresh owners, then recalculate. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse production owners as-is; no new CLI, API, storage, read model, planner, governance, execution, or truth source. |
| Extension strategy | None required for the safe portion. |
| Need New Owner | `FALSE` |

Current semantic reuse audit for OMP V3.0:

| Field | Current Value |
| --- | --- |
| Desired capability | Transition V7 from architecture-first continuation to implementation-first production leverage optimization. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | `docs/reference/V7_SYSTEM_ARCHITECTURE.md`, `docs/reference/V7_RUNTIME_MODEL.md`, `docs/reference/V7_DECISION_MODEL.md`, `docs/reference/V7_ENGINEERING_PRINCIPLES.md`, `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md`, relevant ADRs |
| Composition strategy | Extend OMP in place, add `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`, add `docs/reference/V7_IMPLEMENTATION_MODEL.md`, and preserve existing owner boundaries. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as implementation optimizer; reuse Current Program State as volatile implementation state; reuse existing runtime/planner/knowledge/learning owners for code work. |
| Extension strategy | Add implementation-first question, implementation classes, implementation prioritization, implementation optimizer, and first production-leverage implementation task. |
| Need New Owner | `FALSE` |

## 2.8. New Owner Gate

Before creating any new owner, knowledge model, planner, engine, pipeline, API, CLI, storage, snapshot, or truth source, OMP must prove:

```text
Need New Owner = TRUE
```

`Need New Owner` may be true only when existing semantic coverage is insufficient.

If semantic coverage is sufficient, creation is forbidden.

Required gate output:

| Field | Required |
| --- | --- |
| Desired capability | Clear capability statement. |
| Existing semantic coverage | Percent and evidence. |
| Reuse candidate owners | List. |
| Extension strategy | How existing owners can be extended. |
| Merge strategy | How duplicate/overlapping owners can be merged. |
| Need New Owner | `TRUE` or `FALSE`. |
| Decision | `REUSE`, `EXTEND`, `MERGE`, or `CREATE_NEW`. |

Current gate result:

| Field | Current Value |
| --- | --- |
| Need New Owner | `FALSE` |
| Reason | OMP V2.1 is fully expressible by extending the existing OMP document and existing reference pointers. |

## 2.9. Architectural Duplication Detector

After every implementation, OMP must check for duplication across:

- duplicate owners;
- duplicate planners;
- duplicate governance;
- duplicate execution;
- duplicate lifecycle;
- duplicate APIs;
- duplicate CLI;
- duplicate knowledge models;
- duplicate routing logic;
- duplicate learning logic;
- duplicate truth sources;
- duplicate evidence collectors;
- duplicate packet builders;
- duplicate decision surfaces;
- duplicate maturity models.

Detector verdicts:

| Verdict | Meaning |
| --- | --- |
| `NONE` | No duplication detected. |
| `MERGE_REQUIRED` | Overlap exists and a safe merge path should be implemented. |
| `REMOVE_DUPLICATION` | Duplication is unsafe or already harmful and must be removed. |

If duplication exists and safe merge is possible, implement the merge before adding more capability.

Current detector result:

| Field | Current Value |
| --- | --- |
| Duplicate owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth sources | `NONE` |
| Duplicate maturity models | `NONE` |
| Verdict | `NONE` |

## 2.10. Implementation Prioritization Rules

OMP must choose implementation work in this order:

| Priority | Class | Rule |
| --- | --- | --- |
| A | Existing owner implementation | Implement missing behavior inside the existing owner first. |
| B | Existing owner integration | Connect existing owners when the behavior already exists but is disconnected. |
| C | Existing owner optimization | Improve correctness, safety, speed, or clarity inside an existing owner. |
| D | Read-model improvements | Add read-only fields or summaries that help existing owners decide, stop, verify, or learn. |
| E | Testing | Add focused tests for implemented behavior, state transitions, safety, idempotency, and stop reasons. |
| F | Certification | Certify the implemented behavior with truth, convergence, and project-specific verification. |

Never redesign architecture unless implementation evidence proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 2.11. Implementation Classes

Every future implementation task must be classified as exactly one primary implementation class:

| Class | Meaning |
| --- | --- |
| `IMPLEMENT_RUNTIME` | Runtime lifecycle, wakeup, stop, idempotency, verification, rollback, OMP notification, or runtime preview behavior through existing owners. |
| `IMPLEMENT_BACKGROUND` | Background knowledge, snapshots, intelligence, trust, suitability, prediction, service, route, capacity, or evidence processing. |
| `IMPLEMENT_READ_MODEL` | Read-only surfaces that expose state, decisions, safety, authority, verification, learning, or operator visibility. |
| `IMPLEMENT_TEST` | Tests, fixtures, regression coverage, state-machine coverage, or safety/idempotency coverage. |
| `IMPLEMENT_VERIFICATION` | Verification logic, read-only checks, convergence gates, truth checks, readiness checks, or post-action validation. |
| `IMPLEMENT_OBSERVABILITY` | Lifecycle ids, stage visibility, stop reasons, audit records, operator traces, or non-truth-source observability. |
| `IMPLEMENT_UI` | Operator-facing UI work that consumes existing truth/read models without becoming a decision owner. |
| `IMPLEMENT_DOCUMENTATION` | Documentation required by an implementation, never a substitute for implementation. |
| `IMPLEMENT_CERTIFICATION` | Certification reports, truth/convergence confirmation, and release readiness after implemented behavior. |

Documentation-only tasks may support implementation, but they are not the implementation optimizer target unless documentation is the actual highest production-leverage work.

## 2.12. Implementation Optimizer

OMP optimizes Production Leverage.

Production Leverage means the expected improvement to production autonomy, safety, verifiability, learning, operator effectiveness, or implementation readiness per unit of risk and effort.

Ranking inputs:

1. current bottleneck;
2. current authority boundary;
3. current reality limit;
4. existing owner availability;
5. production safety;
6. expected maturity gain;
7. implementation effort;
8. reversibility;
9. testability;
10. truth/convergence impact;
11. whether the task moves V7 toward Production Autonomy without crossing forbidden boundaries.

Current implementation optimizer result:

| Field | Current Value |
| --- | --- |
| Highest implementation leverage task | `IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW` |
| Implementation class | `IMPLEMENT_RUNTIME` |
| Exact owner | Governed Canary Knowledge-Gated Dry-Run Cycle / Runtime Model composition |
| Exact module | `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle` |
| Exact files | `admin_core/operator_execution_pipeline.py`, `tools/v7-governed-canary-dry-run-cycle`, focused tests for the governed canary dry-run cycle and runtime lifecycle read-only output |
| Implementation status | `DEPLOYED_CERTIFIED_READ_ONLY_RUNTIME_LIFECYCLE_PREVIEW` |
| Certification report | `docs/reports/V7_IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW_CERTIFICATION_REPORT.md` |
| Truth/convergence | Truth `PASS`; convergence `ALIGNED`; runtime commit `50188d9030d651213b5d06b528fed446889c17bc`. |
| New highest implementation leverage task | `IMPLEMENT_PREVIEW_TO_MATERIALIZED_PACKET_BINDING` |
| Stop boundary | `UNSAFE_IMPLEMENTATION`: operator approval exists for the exact preview packet, but the executable packet materialized by existing owners did not preserve the approved preview selected-move hash; no restore-barrier write, apply, user movement, or rollback apply may occur until this binding is deterministic and certified. |

## 2.13. Implementation Program Loop

Implementation program loop:

```text
Read OMP
  -> Read Current Program State
  -> Choose highest implementation leverage
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Test
  -> Verify
  -> Truth
  -> Convergence
  -> Certification
  -> Update Current Program State
  -> Update OMP
  -> Continue automatically
```

Stop only at:

- `AUTHORITY_BOUNDARY`
- `REAL_WORLD_LIMIT`
- `UNSAFE_IMPLEMENTATION`
- `FUNDAMENTAL_ARCHITECTURE_GAP`

Latest optimizer iteration duplication result `2026-06-25`:

| Field | Current Value |
| --- | --- |
| Duplicate owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate knowledge | `NONE` |
| Duplicate lifecycle | `NONE` |
| Duplicate API | `NONE` |
| Duplicate CLI | `NONE` |
| Duplicate read model | `NONE` |
| Verdict | `NONE` |

Latest OMP V2.2 duplication result:

| Field | Current Value |
| --- | --- |
| Duplicate owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth sources | `NONE` |
| Duplicate architecture | `NONE` |
| Verdict | `NONE` |

Latest OMP V2.3 duplication result:

| Field | Current Value |
| --- | --- |
| Duplicate runtime owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth sources | `NONE` |
| Duplicate architecture | `NONE` |
| Documentation split | `V7_KERNEL` and `V7_CURRENT_PROGRAM_STATE` are control-plane documentation owners, not runtime/code owners. |
| Verdict | `NONE` |

## 3. Program States

| State | Meaning |
| --- | --- |
| `NOT_STARTED` | Phase is known but no implementation or verification has begun. |
| `ACTIVE` | Phase is the current work item and may proceed under the stop conditions below. |
| `BLOCKED` | Phase hit an allowed stop condition. |
| `CERTIFIED` | Phase passed tests, truth, convergence, and evidence review. |
| `COMPLETED` | Phase is certified and its results are absorbed into reference/program state. |

## 4. Current Program

`Operational Maturity`

Purpose:

Move V7 from architecture-complete / authority-bound autonomy to production maturity through continuous bottleneck reduction.

The program no longer asks "what is the next phase?" first and no longer asks "what architecture is missing?" first.

The program asks:

```text
Current System State
  -> Current Highest Bottleneck
  -> Current Highest Implementation Leverage
  -> Current Authority Boundary
  -> Current Real World Limit
  -> Next Best Action
```

## 5. Current System State

This section must be recalculated after every certification from canonical reference, system map, ADRs, and latest certified reports.

| Maturity Area | Current State | Evidence |
| --- | --- | --- |
| Architecture maturity | `ARCHITECTURE_COMPLETE` | Final system architecture synthesis: remaining architectural weaknesses `0`; optional improvements are not implementation blockers. |
| Knowledge maturity | `ADVANCED_BUT_NOT_AUTONOMY_COMPLETE` | Knowledge quality model exists; safety is autonomy-grade; several knowledge classes still need real outcomes, service/user/SLA fit depth, client observation, cohort/SLA scale, and aging/retirement. |
| Decision maturity | `READY_UNTIL_AUTHORITY_BOUNDARY` | Planner, knowledge-to-decision, governed dry-run, packet preview, restore/rollback preview, and self-stop are connected. |
| Outcome maturity | `REAL_OUTCOMES_REQUIRED` | Candidate outcome gap remains `72`; missing candidate outcomes are not hidden, they have not happened yet. |
| Learning maturity | `CONNECTED_AFTER_OUTCOME` | Feedback, outcome closure, trust evolution, and learning refresh owners exist and are connected, but need real governed/manual outcomes. |
| Suitability maturity | `HIGHEST_BOTTLENECK` | Suitability cannot become autonomy-grade without more real candidate outcomes and stronger candidate source confidence. |
| Authority maturity | `AUTHORITY_BOUNDARY_REACHED` | Production governed dry-run reaches exact authority boundary before restore-barrier write or apply. |
| Operational maturity | `IMPLEMENTATION_OPTIMIZATION_ACTIVE` | OMP V3.0 optimizes production leverage through existing-owner implementation; no daemon, no autonomous apply, no user movement. |

## 6. Current Highest Bottleneck

Exactly one bottleneck:

`Suitability`

Why this bottleneck is highest right now:

| Evidence | Meaning |
| --- | --- |
| Missing candidate outcomes: `72` | The main weak object is real candidate suitability evidence. |
| Maximum projected current suitability remains below TIER_2 even after current missing outcomes | More rows alone are not enough; correctness/source confidence must improve too. |
| Architecture missing classes: none | The limiting factor is not architecture. |
| Governed dry-run reaches `AUTHORITY_BOUNDARY` | The limiting factor is not disconnected planner/packet/restore/learning owners. |
| Confidence/trust/prediction are also below floor | They matter, but suitability is the bottleneck that specifically requires real candidate outcome closure. |

Recompute rule:

After every certification, classify bottlenecks across `Architecture`, `Knowledge`, `Decision`, `Outcome`, `Learning`, `Suitability`, `Prediction`, `Authority`, `Operational`, and `Scale`. Select exactly one class based on the largest maturity gain that cannot be obtained by already-certified safe automation.

## 7. Current Highest Implementation Leverage

Implementation:

`IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW`

This is implementation work, not research and not architecture.

Definition:

Implement read-only Runtime lifecycle output inside the existing governed canary dry-run cycle so the completed Runtime Model becomes executable, inspectable, testable, idempotency-aware, and certifiable without apply or user movement.

Exact owner:

`Governed Canary Knowledge-Gated Dry-Run Cycle / Runtime Model composition`

Exact module:

`admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle`

Exact files:

- `admin_core/operator_execution_pipeline.py`
- `tools/v7-governed-canary-dry-run-cycle`
- focused tests for governed dry-run runtime lifecycle output

Why this is first:

| Criterion | Result |
| --- | --- |
| Production leverage | Highest safe implementation leverage before any authority-bound apply. |
| Existing owner reuse | Uses the existing governed canary dry-run cycle and Runtime Model composition. |
| Architecture risk | None; architecture is complete and unchanged. |
| Runtime safety | Read-only lifecycle preview only; no apply, no user movement, no daemon, no timer. |
| Bottleneck relevance | Prepares the exact runtime path needed to produce future governed real outcomes safely after authority. |
| Testability | State machine, stop reasons, idempotency, stale packet, duplicate work, verification, rollback, outcome, learning, and OMP notification can be tested without mutation. |
| Certification path | Truth and convergence can certify no runtime mutation and no user movement. |

Required read-only lifecycle fields:

- lifecycle id;
- decision id;
- operation id;
- packet id;
- idempotency key fingerprint;
- current state generation;
- selected move hash;
- runtime stage;
- stage owner;
- input generation;
- stop reason;
- authority status;
- packet freshness;
- duplicate work status;
- loop guard status;
- verification status;
- rollback status;
- outcome status;
- learning status;
- OMP notification status.

Expected implementation order:

1. Add read-only lifecycle output to existing governed canary dry-run cycle.
2. Add focused tests for lifecycle state machine, stop conditions, idempotency key, stale packet, duplicate work, and OMP notification fields.
3. Add read-only verification for the lifecycle output.
4. Certify with truth and convergence.
5. Update Current Program State.

The old bottleneck action, governed candidate suitability outcome closure, remains the highest real-outcome action but crosses `AUTHORITY_BOUNDARY`.
The current implementation-first optimizer therefore chooses the highest safe implementation that prepares that path without crossing the boundary.

## 8. Current Authority Boundary

| Field | Current Value |
| --- | --- |
| Current authority level | `READ_ONLY_AND_GOVERNED_PREVIEW` |
| Current stop reason | `AUTHORITY_BOUNDARY` |
| Boundary location | Before restore-barrier write, runtime apply, and user movement. |
| Current exact runtime posture | No autonomous apply, no user movement, no daemon enablement. |
| Next authority expansion | Explicit operator approval or rejection for the exact governed packet. |

Current production evidence:

- governed dry-run reaches `AUTHORITY_BOUNDARY`;
- packet preview is ready;
- restore/rollback preview is ready;
- verification plan is ready;
- outcome closure plan is ready;
- learning path is connected;
- `apply=false`;
- `users_moved=0`;
- `runtime_mutation=false`.

## 9. Current Reality Limit

Current limit:

`REAL_CANDIDATE_OUTCOMES_HAVE_NOT_HAPPENED`

What cannot honestly improve much more without more real-world activity:

| Limit | Evidence |
| --- | --- |
| Candidate suitability correctness | Missing candidate outcomes are current user -> candidate-channel pairs that require governed/manual action before they can become evidence. |
| Candidate source confidence | Existing consumed candidate outcomes are not strong enough to certify autonomy-grade suitability. |
| TIER_2 suitability | Even converting all current missing outcomes at current assumptions does not guarantee floor closure. |
| Client observation / cohort / SLA depth | These remain future/scale enrichments, not current architecture blockers. |

What does not require new architecture:

- planner;
- governance preview;
- packet generation;
- restore/rollback preview;
- verification plan;
- outcome closure;
- feedback;
- learning refresh;
- truth/convergence.

## 10. Program Optimizer

After every completed implementation, Codex must recalculate:

1. Current system state.
2. Current highest bottleneck.
3. Current highest implementation leverage.
4. Current authority boundary.
5. Current reality limit.
6. Next best action.
7. Whether automatic continuation is allowed.

Optimizer rules:

| Condition | Program Response |
| --- | --- |
| Highest implementation leverage is read-only | Continue automatically. |
| Highest implementation leverage is safe existing-owner implementation with no runtime apply | Continue automatically. |
| Highest implementation leverage requires restore-barrier write | Stop at `AUTHORITY_BOUNDARY`. |
| Highest implementation leverage requires runtime apply | Stop at `AUTHORITY_BOUNDARY`. |
| Highest implementation leverage requires user movement | Stop at `AUTHORITY_BOUNDARY`. |
| Highest implementation leverage requires authority expansion | Stop at `AUTHORITY_BOUNDARY`. |
| Highest implementation leverage requires more users/channels/services/reality | Stop at `REAL_WORLD_LIMIT`. |
| Highest implementation leverage would create duplicate planner/governance/execution/truth | Stop at `UNSAFE_IMPLEMENTATION`. |
| Certified reports reveal a fundamental missing owner | Stop at `FUNDAMENTAL_ARCHITECTURE_GAP`. |

Safety-Bounded Authority split rule:

When the highest leverage action requires real outcomes, Codex must split it into:

| Portion | Work | Program Response |
| --- | --- | --- |
| Safe automatic preparation | Refresh evidence; refresh packet preview; verify restore/rollback preview; verify verification plan; verify outcome closure plan; verify learning path; update OMP; present exact authority decision. | Continue automatically. |
| Authority-bound execution | Restore-barrier write; runtime apply; user movement; rollback apply; daemon/timer enablement; authority expansion. | Stop at `AUTHORITY_BOUNDARY`. |

The safe automatic portion continues automatically.

The authority-bound execution portion stops at `AUTHORITY_BOUNDARY`.

## 11. Implementation Optimization Target

The current target is no longer `Current Phase` and no longer `Architectural Completeness`.

The current optimization target is:

`Highest Production Leverage per unit risk`

OMP must rank potential targets across:

- runtime implementation;
- background implementation;
- read-model improvements;
- verification;
- observability;
- testing;
- UI;
- documentation required by implementation;
- certification.

Current optimization target:

| Field | Current Value |
| --- | --- |
| Optimization target | `IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW` |
| Target class | `IMPLEMENT_RUNTIME` |
| Gain type | Runtime implementation readiness, stop/idempotency/verification/OMP notification visibility, testability, and certification readiness |
| Risk | Low; read-only output in existing owner |
| Effort | Medium |
| Authority | Does not cross `AUTHORITY_BOUNDARY`; must stop before restore-barrier write, apply, user movement, daemon/timer, event consumer mutation, or authority expansion |
| Safe automatic portion | Refresh exact governed packet preview, verify restore/rollback preview, verify outcome closure plan, present exact authority decision |

Latest optimization iteration `2026-06-25`:

| Field | Current Value |
| --- | --- |
| Recalculation source | Production `v7-autonomy-trust-evidence-inventory` after service/quality/snapshot refresh. |
| Challenged action | `Governed candidate suitability outcome closure`. |
| Best lower-risk challenger | `Service verification and quality snapshot refresh`. |
| Safe portion executed | `v7-egress-quality-compact`, `v7-service-matrix-refresh-all`, `v7-intelligence-snapshot-refresh`. |
| Runtime apply | `FALSE` |
| Users moved | `0` |
| New owner created | `FALSE` |
| New planner/governance/execution/truth | `FALSE` |
| Post-refresh maturity score | `84.167` |
| Post-refresh largest floor gap | `Suitability`: current `29.11`, gap `40.89` to floor `70`. |
| Post-refresh candidate gap | `72` missing candidate outcomes, coverage ratio `0.5385`. |
| Post-refresh dry-run verdict | `AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY`. |
| Post-refresh packet state | Packet preview ready; restore/rollback preview ready; verification plan ready; outcome closure plan ready; learning path connected. |
| Optimizer conclusion | Safe challenger completed; final HLA remains governed candidate suitability outcome closure and stops at `AUTHORITY_BOUNDARY`. |

## 12. Architecture Health

Maintain continuously:

| Metric | Current Value | Evidence |
| --- | --- | --- |
| Architecture Completeness | `100% fundamental / future optional extensions remain` | Final architecture certification reports no fundamental missing classes. |
| Knowledge Completeness | `PARTIAL_FOR_AUTONOMY` | Knowledge objects exist; real outcome depth remains insufficient. |
| Reuse Ratio | `100%` | Current OMP V2.1 upgrade reuses existing OMP/reference owners and creates no new owner. |
| Extension Ratio | `100%` | Current capability is delivered by extending existing documents in place. |
| Duplicate Ratio | `0% known introduced` | Duplication detector verdict is `NONE`. |
| Automation Ratio | `84.167%` | Autonomous knowledge growth program maturity score. |
| Authority Ratio | `BOUNDARY_REACHED / NOT_EXPANDED` | Governed dry-run reaches authority boundary; no apply authority granted. |
| Operational Maturity | `OPTIMIZATION_ACTIVE` | OMP now drives bottleneck optimization rather than fixed phases. |

## 13. Self-Improvement Loop

Every implementation must follow:

```text
Discover
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Verify
  -> Truth
  -> Convergence
  -> Certification
  -> OMP Update
  -> Optimization Recalculation
  -> Continue
```

No future prompt may bypass OMP. OMP always wins over free-form implementation ideas.

## 14. Automatic Continuation Rule

Codex must continue automatically while the highest leverage action does not require:

1. restore-barrier write;
2. runtime apply;
3. user movement;
4. authority expansion.

Codex must continue automatically through:

1. docs/reference updates;
2. ADR updates;
3. read-only verification;
4. truth/convergence checks;
5. inventory refresh;
6. quality/service/snapshot refresh;
7. existing-owner implementation;
8. tests;
9. duplication detection;
10. OMP recalculation;
11. packet preview refresh;
12. restore/rollback preview verification;
13. outcome closure plan verification;
14. learning path verification.

Codex must stop only at:

1. `AUTHORITY_BOUNDARY`;
2. `REAL_WORLD_LIMIT`;
3. `UNSAFE_IMPLEMENTATION`;
4. `FUNDAMENTAL_ARCHITECTURE_GAP`.

If the highest leverage action crosses authority boundary, Codex must:

1. stop before the boundary;
2. update this OMP;
3. report exact reason;
4. wait for explicit operator authority for the exact action.

Implementation loop for every future task:

```text
DISCOVER
  -> REUSE
  -> EXTEND
  -> IMPLEMENT
  -> VERIFY
  -> CERTIFY
  -> UPDATE OMP
  -> RECALCULATE BOTTLENECK
  -> CONTINUE
```

This replaces phase-first and roadmap-first thinking with optimization-first thinking.

## 15. OMP Execution Contract For Codex

Codex must not ask:

```text
what phase should I execute?
```

Codex must:

1. read OMP;
2. recalculate current bottleneck;
3. find safe automatic portion;
4. execute safe portion through existing owners;
5. verify;
6. certify;
7. update OMP, reference, system map, or ADR if meaning changed;
8. recalculate;
9. continue;
10. stop only at an allowed stop condition.

If blocked by `AUTHORITY_BOUNDARY`, Codex must output:

- exact packet;
- exact action;
- exact user;
- exact source;
- exact target;
- exact rollback target;
- exact command shape that must not run without approval;
- exact approval question.

This contract is constrained by Safety-Bounded Authority:

```text
Trust decides autonomy tier.
Safety decides bounded action.
```

## 16. Program Health

| Health Dimension | Current Value | Notes |
| --- | --- | --- |
| Architecture completeness | `COMPLETE` | Fundamental architecture exists; future extensions remain optional/scale-related. |
| Knowledge completeness | `PARTIAL_FOR_AUTONOMY` | Knowledge objects exist but real outcome depth is insufficient for autonomy-grade suitability. |
| Cycle automation % | `84.167` | Autonomous knowledge growth program certified 12 cycles and maturity score `84.167`. |
| Authority maturity | `BOUNDARY_REACHED` | Safe preparation reaches authority boundary; apply authority is not granted. |
| Operational maturity | `OPTIMIZATION_ACTIVE` | OMP now optimizes bottleneck reduction rather than executing a fixed roadmap. |
| Remaining architecture uncertainty | `NONE_FUNDAMENTAL` | Partial classes are future/scale/authority extensions, not missing architecture. |
| Current optimization velocity | `AUTHORITY_BOUNDARY_AFTER_SAFE_REFRESH` | Safe service/quality/snapshot refresh completed through existing owners; real candidate outcome gain needs exact authority. |

## 17. Historical Phase Anchor

`GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE`

Source:

- `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`
- `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`
- `docs/reference/SYSTEM_MAP.md`

Reason:

The final architecture certification says V7 has no fundamental architecture gap. The governed dry-run reaches `AUTHORITY_BOUNDARY` with packet preview, restore/rollback preview, verification plan, outcome closure plan, and learning path connected. The next maturity gain requires real governed candidate outcome evidence.

## 18. Historical Objective

Use existing owners to create and close one real governed candidate outcome only after explicit operator authority.

The phase must:

1. reuse the existing planner;
2. reuse the existing governed packet owner;
3. reuse the existing restore barrier;
4. reuse the existing rollback preview;
5. reuse the existing verification plan;
6. reuse the existing feedback/outcome closure owner;
7. reuse the existing learning refresh owner;
8. re-evaluate confidence, trust, prediction, and suitability after outcome closure.

No autonomous apply is approved by this program state.

## 19. Success Criteria

| Criterion | Required State |
| --- | --- |
| Exact packet authority | Explicit operator approval exists for the exact packet before any restore-barrier write or apply. |
| Runtime safety | No movement occurs before authority; no hidden daemon or timer apply is enabled. |
| Existing owners | Planner, packet, restore barrier, rollback, feedback, learning, and truth/convergence owners are reused. |
| Real outcome | The candidate outcome is observed after a real governed/manual action, not synthesized. |
| Closure | Outcome, verification, rollback/no-rollback decision, feedback, and learning are recorded through existing paths. |
| Certification | Tests, `tools/v7-truth-check --all --json`, and `tools/v7-convergence-status --json` pass after the phase. |
| Documentation | Canonical reference, system map, ADRs, and this program are updated when meaning changes. |

## 20. Stop Conditions

Only these stop conditions are allowed:

1. `AUTHORITY_BOUNDARY`
2. `REAL_WORLD_LIMIT`
3. `UNSAFE_IMPLEMENTATION`
4. `FUNDAMENTAL_ARCHITECTURE_GAP`

Current blocker:

`AUTHORITY_BOUNDARY`

Details:

- production governed dry-run stops before restore-barrier write or apply;
- explicit operator approval is required for the exact packet;
- confidence, trust, prediction confidence, and suitability are still below autonomous maturity needs;
- candidate outcome gap remains real-world evidence, not missing architecture.

## 21. Phase History

| Phase | Certified Result | State | Evidence |
| --- | --- | --- | --- |
| Canonical Reference Base | Reference and ADR system created | `COMPLETED` | `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md` |
| Reference First Rule | Future audits must read reference before re-auditing | `COMPLETED` | `docs/decisions/ADR-005-reference-first-rule.md` |
| Event-Driven Autonomy Contract | Timer-only movement rejected; event-driven model accepted | `COMPLETED` | `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md` |
| Knowledge Quality Model | Data/signal/knowledge/action authority separated | `COMPLETED` | `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md` |
| Autonomous Routing Foundation | Fit, outcome, recovery, anti-flap, freshness models exposed read-only | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md` |
| Knowledge To Decision Integration | Routing knowledge can influence read-only decisions without apply | `COMPLETED` | `docs/reports/V7_KNOWLEDGE_TO_DECISION_INTEGRATION_REPORT.md` |
| Decision To Outcome To Learning Integration | Outcome quality and learning path connected | `COMPLETED` | `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md` |
| Highest Leverage Outcome Growth | Verdict `MIXED_PATH`; suitability needs real candidate outcomes | `COMPLETED` | `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md` |
| Autonomy-Grade Suitability Program | Suitability growth requires real candidate outcome closure | `COMPLETED` | `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md` |
| Autonomous Knowledge Growth Program | 12 cycles verified; maturity score `84.167`; boundary remains authority | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_KNOWLEDGE_GROWTH_PROGRAM_REPORT.md` |
| Autonomous Routing Evolution Program | TIER_2 remains blocked by confidence/trust/prediction/suitability and real outcomes | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md` |
| Maximum Reality Knowledge Extraction | `72` candidate outcomes are not hidden; they require governed/manual action | `COMPLETED` | `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md` |
| Final Autonomous Routing Architecture Certification | Superseded by final system synthesis: `ARCHITECTURE_COMPLETE`; optional improvements remain non-blocking | `CERTIFIED` | `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`, `docs/reference/V7_SYSTEM_ARCHITECTURE.md`, `docs/decisions/ADR-V7-SYSTEM-ARCHITECTURE.md` |
| Governed Canary Knowledge-Gated Dry-Run Cycle | Production reaches `AUTHORITY_BOUNDARY`; no apply, no movement | `CERTIFIED` | `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md` |

## 22. Next Best Action

`IMPLEMENT_READ_ONLY_RUNTIME_LIFECYCLE_PREVIEW`

Program interpretation:

This is the first implementation-phase coding task. It is not research, architecture, planning, governance redesign, execution redesign, runtime redesign, apply, daemon work, timer work, or user movement.

The task implements production leverage by exposing the completed Runtime Model through the existing governed dry-run owner.

Safe automatic target:

```text
implement read-only Runtime lifecycle preview
  -> reuse governed_canary_knowledge_gated_dry_run_cycle
  -> emit lifecycle, stage, stop, idempotency, duplicate, loop, verification, rollback, learning, and OMP-notification status
  -> add focused tests
  -> verify no apply, no user movement, no runtime mutation
  -> run truth
  -> run convergence
  -> update Current Program State and OMP
```

The implementation target is:

```text
admin_core/operator_execution_pipeline.py
  -> governed_canary_knowledge_gated_dry_run_cycle
  -> tools/v7-governed-canary-dry-run-cycle
  -> focused governed dry-run lifecycle tests
```

If a restore-barrier write, apply, user movement, rollback apply, daemon, timer, event consumer mutation, authority expansion, or autonomous execution is required, stop at `AUTHORITY_BOUNDARY`.

## 23. Next Best Action Entry Criteria

| Entry Criterion | Required |
| --- | --- |
| Existing owner | Reuse `governed_canary_knowledge_gated_dry_run_cycle`; do not create a duplicate runtime owner. |
| Scope | Read-only lifecycle preview only. |
| Runtime model | Emit fields that map to `V7_RUNTIME_MODEL.md` lifecycle, state, stop, restart, duplicate, loop, idempotency, verification, rollback, learning, and OMP-notification semantics. |
| Apply path | Forbidden. No restore-barrier write, apply, rollback apply, or user movement. |
| Authority | Any action requiring operator approval stops at `AUTHORITY_BOUNDARY`. |
| Tests | Focused tests must prove the lifecycle output is read-only and idempotency-aware. |
| Safety | No daemon enablement, no timers, no event consumer mutation, no duplicate planner/governance/execution. |

## 24. Program Certification

| Field | Current Value |
| --- | --- |
| Completed phases | Canonical reference, reference-first rule, event-driven contract, knowledge quality, routing foundation, knowledge-to-decision, decision-to-outcome-to-learning, outcome leverage, suitability program, knowledge growth, routing evolution, maximum reality extraction, decision model, runtime model, system architecture. |
| Certified phases | Decision Model; Runtime Model; System Architecture; governed knowledge-gated dry-run cycle. |
| Current bottleneck | Preview-to-materialized executable packet binding after exact governed canary approval. |
| Current highest leverage action | `IMPLEMENT_PREVIEW_TO_MATERIALIZED_PACKET_BINDING`. |
| Current reuse ratio | `100%`. |
| Current duplicate ratio | `0% known introduced`. |
| Current automation ratio | `84.167%`. |
| Current blockers | `UNSAFE_IMPLEMENTATION`: approved preview packet `pkt_preview_fb70744bc51ad162b1727dcb` maps to the intended user and target, but current executable packet materialization produced a different selected-move hash. |
| Current maturity | Architecture complete; implementation phase active; read-only runtime lifecycle preview deployed and production-verified; autonomy cycles mature to exact packet authority boundary. |
| Current runtime posture | No autonomous apply, no user movement, no daemon enablement. |
| Current next best action | Implement or certify deterministic preview-to-materialized executable packet binding through existing owners before any exact packet execution. |
| Last optimizer iteration | `2026-06-25`: exact governed canary approval received, production preflight materialized a different executable selected-move hash, and OMP stopped at `UNSAFE_IMPLEMENTATION` before restore-barrier write or apply. |

## 25. Program Rule For Future Work

Before starting any future implementation task, Codex must treat this file as the first program source. If a prompt conflicts with this program, the optimizer wins unless the user explicitly changes the program through a new ADR/reference update.

OMP itself is a continuously learning system.

Every optimization decision
must later be evaluated
against the real outcome.

OMP is allowed to improve
its future prioritization
using only real historical evidence.

## 26. Current Volatile State Pointer

Current volatile state lives in:

`docs/programs/V7_CURRENT_PROGRAM_STATE.md`

That file owns the current bottleneck, HLA, authority boundary, reality limit, metrics, exact packet, stop reason, and exact approval question.

OMP owns the scheduler and optimizer rules.

When packet fields, metrics, or stop reason change, update `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Update OMP only when scheduler/optimizer meaning changes.
