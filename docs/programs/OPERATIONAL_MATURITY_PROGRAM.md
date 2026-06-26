# V7 Operational Maturity Program

Status: `ACTIVE`
Program: `V7.OMP.FINAL.PRODUCTION_PROGRAM`
Created: 2026-06-25
Version: `4.0`
V2.1 baseline reference commit: `7687d506a4a14bf6aed39aa15efd00462b96d980`
Runtime architecture certification commit: `39c46ed379ff4a2ccadb84a49a0dd9dcd2de579b`

This document is the permanent production operating program for V7. It replaces roadmap-driven development, phase-first development, free-form implementation ideas, and architecture-first continuation with continuous production maturity evolution.

Roadmaps, reports, ADRs, and reference files remain evidence and context. The complete autonomy roadmap lives inside this OMP. No additional roadmap document is required to drive V7 from current `TIER_1` governed autonomy to full production autonomy.

This program decides the current system state, highest bottleneck, highest leverage action, normalized authority class, reality limit, next best action, authority evolution recommendation, and whether Codex may continue automatically.

V4 operating questions:

```text
What implementation gives the highest production leverage right now?
What authority tier is certified by real outcomes?
What safe work can continue before an allowed stop condition?
```

V2.1 adds architectural minimalism, semantic reuse, a new-owner gate, architecture duplication detection, and an explicit optimization engine. V2.2 adds Safety-Bounded Authority: trust decides autonomy tier, safety decides bounded action. V2.3 adds Kernel and State Split: permanent operating rules live in Kernel/OMP, volatile current state lives in Current Program State. V3.0 closes architecture-first work and activates implementation-first optimization. V4.0 finalizes OMP as the permanent Production Program and integrates autonomy maturity, implementation, authority evolution, continuous optimization, and continuous knowledge evolution into one operating loop. OMP always wins over free-form implementation ideas.

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
| Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Volatile current bottleneck, HLA, packet, normalized authority class, metrics, stop reason, and next automatic action. |
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

From V4.0 forward, OMP is the single permanent production execution program for V7.

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

These files are supporting implementation references under OMP. They are not separate roadmap authorities.

## 2.1.2. Permanent Production Maturity Ladder

OMP owns the complete autonomy roadmap.

No additional roadmap document is required.

| Tier | Name | Scope | Status |
| --- | --- | --- | --- |
| 0 | Architecture foundation | Architecture, Research, Decision Model, Runtime Model, System Architecture. | `COMPLETE` |
| 1 | Governed implementation | Implementation, existing owner integration, testing, certification, production deployment, one-user governed canary, outcome closure, learning. | `ACTIVE` |
| 2 | Low-risk autonomous execution | Only actions proven safe; only bounded blast radius; rollback mandatory; verification mandatory; learning mandatory; no authority expansion without certification. | `LOCKED_UNTIL_CERTIFIED` |
| 3 | Small-batch autonomy | Multiple bounded users/actions only after Tier 2 evidence proves safety, rollback, verification, and learning. | `FUTURE_CERTIFIED_STEP` |
| 4 | Operational autonomy | Runtime performs routine production actions automatically inside certified policy and blast-radius limits. | `FUTURE_CERTIFIED_STEP` |
| 5 | Production autonomy | Operator supervises; Runtime operates; OMP optimizes production leverage and safety. | `FUTURE_CERTIFIED_STEP` |
| 6 | Authority evolution | After every certified outcome, OMP evaluates whether authority should remain unchanged, shrink, or be proposed for expansion. | `PERMANENT_RULE` |
| 7 | Continuous implementation | OMP continuously searches for highest implementation leverage; Codex continuously implements until a stop condition. | `PERMANENT_RULE` |
| 8 | Continuous optimization | OMP continuously searches for performance, simplicity, reuse, latency, runtime cost, readability, testability, and operability improvements. | `PERMANENT_RULE` |
| 9 | Continuous knowledge evolution | Research Framework continues forever; only proven production engineering principles may change V7; research informs OMP. | `PERMANENT_RULE` |
| 10 | Production evolution | Runtime -> Outcome -> Learning -> OMP -> Implementation -> Runtime. | `PERMANENT_RULE` |

Tier progression is evidence-gated.

No tier expands authority automatically.

## 2.1.3. Authority Evolution Rule

After every successful certified outcome, OMP must evaluate:

1. can authority remain unchanged;
2. can authority shrink;
3. should authority expansion be proposed.
4. can packet-level approval be retired for the certified action class.

OMP may recommend authority expansion.

OMP must never silently expand authority.

Authority expansion requires explicit operator approval or certified policy approval.

If expansion is needed before safe continuation, OMP must stop at `ENGINEERING_AUTHORITY`.

Authority shrink may be recommended when verification, rollback, learning, or real outcomes show increased risk.

Packet-level approval is not the permanent product model.

The durable authority object is the Action Class.

Packets are runtime execution artifacts. They are fresh, bounded, validated, and ephemeral. A packet may execute only when it belongs to an already approved Action Class or when the class is still `GOVERNED_ONLY` and the operator explicitly approves the exact packet as a temporary governed fallback.

OMP must treat packet staleness as evidence that packet approval does not scale. Packet approval is acceptable for early governed proof, but it must be eliminated class-by-class after certification and explicit authority approval.

## 2.1.3.1. Authority Boundary Normalization

OMP must never expose raw `AUTHORITY_BOUNDARY` as the primary status.

Raw `AUTHORITY_BOUNDARY` is a legacy technical compatibility detail only. OMP must normalize it into one of two authority classes before reporting status, updating Current Program State, or asking for operator action.

| Authority Class | Meaning | Examples | OMP Status | Engineering Behavior |
| --- | --- | --- | --- | --- |
| `ENGINEERING_AUTHORITY` | Implementation cannot continue because engineering approval is required. | Authority expansion; new action class; new runtime capability; new autonomous policy; blast-radius expansion. | `Engineering Approval Required` | Engineering work pauses until approval or rejection. |
| `OPERATIONAL_AUTHORITY` | Engineering is complete, implementation is ready, Runtime is ready, and only one production operation requires approval. | Approve exact packet; approve exact rollback; approve exact production action. | `Production Action Ready` | Engineering continues after the production action is approved/rejected and closed. |

Authority classification rules:

| Raw blocker or situation | Normalized result |
| --- | --- |
| Exact packet approval | `OPERATIONAL_AUTHORITY` |
| Exact rollback approval | `OPERATIONAL_AUTHORITY` |
| Exact production action approval | `OPERATIONAL_AUTHORITY` |
| Authority expansion | `ENGINEERING_AUTHORITY` |
| New action class approval | `ENGINEERING_AUTHORITY` |
| New runtime capability approval | `ENGINEERING_AUTHORITY` |
| New autonomous policy approval | `ENGINEERING_AUTHORITY` |
| Blast-radius expansion | `ENGINEERING_AUTHORITY` |
| Implementation defect | `UNSAFE_IMPLEMENTATION` |
| Real-world evidence required | `REAL_WORLD_LIMIT` |

Current Program State must store:

- `authority_class`;
- `authority_reason`;
- `authority_owner`;
- `required_action`.

If the class is `ENGINEERING_AUTHORITY`, OMP must output:

```text
Status
Engineering Approval Required

Reason
...

Next engineering task
...
```

If the class is `OPERATIONAL_AUTHORITY`, OMP must output:

```text
Status
Production Action Ready

Authority
Operational

Packet
...

Required operator action
...
```

## 2.1.4. Autonomy Promotion Engine

The Autonomy Promotion Engine is the permanent OMP rule for how action classes become autonomous.

It governs action classes, not individual packets.

It is not runtime apply.
It is not authority expansion.
It is not packet execution.
It is not a new planner, governance layer, execution path, runtime owner, truth source, or authority engine.

The engine reuses OMP, Current Program State, Runtime Model, existing packet/restore/rollback/verification/outcome/learning owners, truth/convergence, ADRs, and certified reports.

Machine-readable Action-Class Runtime Enablement state is exposed through the existing read-only owners:

- `admin_core/autonomy_trust_acceleration.py::build_action_class_runtime_enablement_model`;
- `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only`;
- `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle`.

These surfaces may classify, map, and recommend. They must not move users, write restore barriers, execute apply, expand authority, create evidence, create planners, create governance, create execution, or create truth sources.

Operator authority must evolve from:

```text
Approve Action Class
  -> Approve Authority Expansion
  -> Approve Product Policy
  -> Operator Supervision Only
```

`Approve Packet` remains only a temporary `GOVERNED_ONLY` fallback while an action class is not yet certified for class approval.
It is not the primary OMP authority model.

Every certified outcome must trigger Autonomy Promotion evaluation.

OMP must automatically ask:

```text
Can this action class move to the next autonomy state?
```

If yes, OMP must prepare a class promotion or authority expansion recommendation.

If no, OMP must state the exact missing evidence, verification, rollback/no-rollback quality, blast-radius certification, safety gate, freshness gate, anti-flap certification, learning quality, trust gap, authority policy, runtime owner path, or duplication blocker.

After every certified action class, OMP must also ask:

```text
Can packet approval for this class be permanently eliminated?
```

If yes, OMP must prepare an Authority Promotion recommendation that moves the class toward runtime capability.

If no, OMP must state the exact missing evidence that still requires packet-level governed fallback.

An action class may become autonomous only if all are true:

- real outcomes exist;
- verification passed;
- rollback/no-rollback path certified;
- blast radius certified;
- safety gates certified;
- freshness gates certified;
- anti-flap certified;
- authority policy approved;
- runtime path exists through existing owners;
- no duplicate planner, governance, execution, or truth is introduced.

Promotion is based only on:

- real outcomes;
- verification;
- rollback quality;
- safety;
- blast radius;
- learning;
- trust;
- authority policy.

Promotion must never be based on synthetic evidence.
Promotion must never be based on reports alone.

Autonomy Promotion loop:

```text
Observe
  -> Collect Outcomes
  -> Verify
  -> Measure
  -> Evaluate
  -> Recommend Promotion
  -> Operator approves CLASS
  -> Runtime capability updated
  -> Runtime generates fresh packets inside policy
  -> Future packets execute only when they match approved class authority
```

Action class states:

| State | Meaning |
| --- | --- |
| `NOT_CERTIFIED` | The class lacks enough evidence, certification, owner wiring, safety, freshness, rollback/no-rollback, blast-radius, learning, trust, or authority basis. |
| `GOVERNED_ONLY` | Temporary proof state. The class can be prepared or executed only as a governed action with explicit packet-level authority while class evidence is still insufficient. |
| `CERTIFIED_FOR_CLASS_APPROVAL` | The class has enough real evidence for OMP to recommend operator approval of the class, but Runtime must not execute it autonomously yet. |
| `CERTIFIED_FOR_BOUNDED_AUTONOMY` | The class has enough evidence and approved authority policy for bounded autonomous execution to be proposed. This still does not silently enable Runtime. |
| `AUTONOMOUS_RUNTIME` | Runtime may execute this class automatically inside explicitly approved policy, authority, blast-radius, freshness, safety, rollback/no-rollback, verification, and learning bounds. Packet-level operator approval is retired for the class. |

Canonical Action Classes:

- single-user failover;
- two-user failover;
- small batch movement;
- channel hard failure;
- channel degradation;
- recovery admission;
- service failover;
- rollback;
- packet generation;
- verification;
- outcome closure;
- learning refresh;
- other classes only if discovered through existing owners and added without duplicate planner, governance, execution, truth, or runtime ownership.

Action-class ladder:

| Action class | Current status | Required evidence | Required verification | Required rollback | Required blast radius | Required authority | Action class state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Single-user governed candidate failover | TIER_1 governed path exists; one approved leased governed canary outcome has been executed, verified, closed, and learned from; fresh packets still stop at authority. | More real candidate suitability outcomes, service/user outcome, closure record, learning record, source confidence. | Immediate post-move service/user/channel verification plus truth/convergence. | Rollback target or certified no-rollback decision for the class, not only one packet. | Exactly one user. | Explicit operator approval for each exact packet until class approval exists. | `GOVERNED_ONLY` |
| 2. Two-user failover | Not certified. | Multiple successful one-user governed outcomes across comparable conditions. | Per-user and cohort verification. | Per-user rollback/no-rollback path. | Two bounded users only. | Class approval and authority expansion recommendation. | `NOT_CERTIFIED` |
| 3. Five-user failover | Not certified. | Certified two-user outcomes plus stronger candidate/source confidence. | Per-user, cohort, and service verification. | Batch rollback/no-rollback path. | Five bounded users only. | Class approval and authority expansion recommendation. | `NOT_CERTIFIED` |
| 4. Channel hard-fail failover | Read-only/event path exists; autonomous apply not certified. | Real hard-fail events, verified impact, successful governed failover outcomes. | Failure detection, target safety, post-failover service reachability. | Restore or alternate safe route certification. | Bounded affected users or cohort. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 5. Channel degradation failover | Read-only degradation evidence exists; autonomous apply not certified. | Real degradation events, freshness, anti-flap, recovery stage, governed outcomes. | Degradation confirmation and post-move improvement. | Restore/no-rollback decision with anti-flap protection. | Bounded affected users or cohort. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 6. Service-specific failover | Service matrix and service evidence exist; autonomous apply not certified. | Real service-specific failures and successful governed service-targeted outcomes. | Service reachability before/after action. | Service-safe rollback/no-rollback path. | Users affected by the service only. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 7. Recovery admission | Read-only recovery and anti-flap overlays exist. | Real recovery observations, no-flap windows, successful gradual admission outcomes. | Recovery stability and service/user quality checks. | Re-drain or no-rollback decision. | One channel, cohort, or bounded user set per policy. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 8. Small batch movement | Future certified step. | Certified one/two/five-user outcomes with strong suitability, safety, rollback, and learning. | Batch verification and per-user exception handling. | Batch rollback/no-rollback path. | Small certified batch only. | Class approval and authority expansion recommendation. | `NOT_CERTIFIED` |
| 9. Rollback | Existing rollback owner and previews exist; autonomous rollback apply is not broadly certified. | Real rollback/no-rollback outcomes and failure cases. | Post-rollback service/user/channel verification. | Rollback itself must be bounded and idempotent. | Same or smaller than failed action. | Explicit rollback authority or certified policy. | `GOVERNED_ONLY` |
| 10. Packet generation | Existing packet owner exists and is read-only/generation-safe. | Packet identity stability, selected move hash stability, lease behavior, stale invalidation. | Packet validation and identity checks. | N/A unless execution follows. | N/A until packet is executed. | Existing governed packet policy. | `GOVERNED_ONLY` |
| 11. Verification | Existing verification and truth/convergence owners exist. | Real verification results across executed actions. | Verification must prove action effect or inconclusive state. | N/A unless rollback follows. | N/A. | Existing verification policy. | `GOVERNED_ONLY` |
| 12. Outcome closure | Existing feedback/outcome owners exist. | Verified real outcomes and closure records. | Closure completeness and learning eligibility. | N/A. | N/A. | Existing outcome policy. | `GOVERNED_ONLY` |
| 13. Learning refresh | Existing learning/snapshot owners exist. | Verified outcome records only. | Refresh output and truth/convergence. | N/A. | N/A. | Existing learning policy. | `GOVERNED_ONLY` |

Runtime enablement end state:

```text
Certified Action Class
  -> Authority Promotion Recommendation
  -> Operator or certified policy approval
  -> Runtime capability
  -> Fresh packet generated immediately before execution
  -> Packet validated against approved class
  -> Execute or stop safely
```

Packet approval is not the promotion endpoint.
Runtime capability is the promotion endpoint.

Runtime must never depend on a long-lived packet approval for an autonomous or class-approved action.
Runtime must generate or consume a fresh packet immediately before execution and verify:

- action class match;
- authority match;
- policy match;
- subject and target class match;
- freshness;
- safety;
- rollback/no-rollback readiness;
- verification readiness;
- blast-radius bounds;
- no duplicate planner, governance, execution, or truth.

Stop rule:

If Autonomy Promotion requires runtime apply, exact restore-barrier write, exact user movement, or exact rollback apply, OMP must stop at `OPERATIONAL_AUTHORITY`.

If Autonomy Promotion requires class approval, authority expansion, product policy approval, daemon/timer enablement, event-consumer mutation, new runtime capability, autonomous policy approval, or blast-radius expansion, OMP must stop at `ENGINEERING_AUTHORITY`.

OMP must never silently enable runtime automation.

Current first certifiable Action Class:

`single-user governed candidate failover`

Current promotion state:

`GOVERNED_ONLY`

Current promotion target:

`CERTIFIED_FOR_CLASS_APPROVAL`

Evidence needed for next promotion state:

- more real one-user governed candidate outcomes across comparable conditions;
- repeated successful verification and outcome closure;
- certified rollback/no-rollback behavior for the class, not only one packet;
- sustained blast-radius, safety, freshness, and anti-flap certification;
- stronger suitability and source confidence;
- explicit operator approval for the class before any packet-level approval can be removed.

Current runtime automation enabled:

`NO`

Current machine-readable path status:

`PARTIAL`

The path exists as a read-only registry, packet-to-action-class mapping, authority-to-action-class mapping, runtime capability view, promotion recommendation, and enablement readiness check through existing owners. It is not yet autonomous runtime authority.

## 2.1.5. Delegated Autonomy Policy Model

Delegated Autonomy Policy is the permanent model for replacing repetitive operator approval.

The operator approves bounded policy.
V7 may self-approve operational decisions only inside that approved policy.
V7 may not approve expansion of the policy.

Delegated Autonomy Policy is not runtime apply.
It is not user movement.
It is not authority expansion.
It is not a new planner, governance layer, execution path, runtime owner, truth source, or packet owner.

The policy must define:

- allowed action classes;
- max users per action;
- allowed failure types;
- required freshness;
- required verification;
- required rollback or certified no-rollback path;
- required anti-flap state;
- required suitability, trust, confidence, and prediction floors;
- max blast radius;
- cooldown;
- stop conditions;
- automatic downgrade rules;
- required reporting after action.

Autonomy modes:

| Mode | Meaning |
| --- | --- |
| `MANUAL_PACKET_APPROVAL` | Temporary early governed fallback. Operator approves exact fresh packets. |
| `CLASS_APPROVAL` | Operator approves durable action classes, but Runtime does not execute autonomously. |
| `DELEGATED_AUTONOMY` | Operator approves bounded policy; V7 may make operational decisions inside policy. |
| `PRODUCTION_AUTONOMY` | Operator supervises; Runtime performs routine certified work inside policy. |

Current default policy:

| Field | Value |
| --- | --- |
| Policy id | `dap_default_tier1_readonly` |
| Policy state | `NOT_APPROVED` |
| Current mode | `CLASS_APPROVAL` |
| Target mode | `DELEGATED_AUTONOMY` |
| Allowed first class | `single-user governed candidate failover` |
| Max users per action | `1` |
| Runtime apply enabled | `NO` |
| Authority expanded | `NO` |

Runtime may execute automatically only if all are true:

1. action belongs to an approved policy;
2. action class is certified, or policy explicitly allows governed learning mode;
3. fresh packet is generated immediately before execution;
4. packet matches policy;
5. rollback is ready;
6. verification is ready;
7. anti-flap passes;
8. blast radius is within policy;
9. evidence is not stale;
10. failure mode is known.

If any condition fails, Runtime must stop safely.

Self-approval rule:

- V7 may approve operational decisions inside approved policy.
- V7 may not approve policy expansion.
- V7 may not silently increase blast radius.
- V7 may not silently add new action classes.
- V7 may recommend expansion, but it cannot grant expansion.

Machine-readable Delegated Autonomy Policy state is exposed through the existing read-only owners:

- `admin_core/autonomy_trust_acceleration.py::build_delegated_autonomy_policy_preview`;
- `admin_core/autonomy_trust_acceleration.py::build_delegated_autonomy_runtime_eligibility`;
- `admin_core/autonomy_trust_acceleration.py::build_action_class_runtime_enablement_model`;
- `tools/v7-autonomy-trust-evidence-inventory --delegated-autonomy-policy-only`;
- `tools/v7-autonomy-trust-evidence-inventory --delegated-autonomy-eligibility-only`;
- `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only`.

Current implementation status:

`READ_ONLY_PREVIEW_AND_ELIGIBILITY_CHECK_ONLY`

Current automation state:

`NO_RUNTIME_AUTOMATION_ENABLED`

## 2.1.6. Canonical Policy Library Rule

The Canonical Policy Library is the permanent source for operational behavior policy:

```text
docs/policies/
```

Before implementing or changing any operational behavior, OMP must ask:

```text
Does a Canonical Policy already exist?
```

Decision rule:

| Answer | OMP action |
| --- | --- |
| `YES` | Reuse the policy. |
| `PARTIAL` | Extend the policy through the complete methodology. |
| `NO` | Execute the complete World Research methodology before implementation. |

Complete policy methodology:

```text
DISCOVER
  -> FULL WORLD RESEARCH
  -> KNOWLEDGE NORMALIZATION
  -> INDUSTRY CONSENSUS DETECTION
  -> INDUSTRY DISAGREEMENT DETECTION
  -> CANONICAL POLICY INTERACTION AUDIT
  -> REALITY AUDIT
  -> V7 FIT ANALYSIS
  -> REUSE EXISTING V7 OWNERS
  -> CANONICAL POLICY
  -> IMPLEMENTATION
  -> VERIFICATION
  -> CERTIFICATION
  -> OMP INTEGRATION
```

Operational implementation before certification is forbidden.
The `IMPLEMENTATION` lifecycle step may prepare code or documentation only after a canonical policy exists; runtime enablement waits for `CERTIFICATION` and OMP integration.

After Stage 4 `V7 FIT ANALYSIS`, implementation is driven by:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md
```

OMP must choose the highest-priority unfinished backlog item.
OMP must not create a new roadmap document for policy implementation.
After a backlog item is completed, OMP must mark it `DONE`, recalculate priority, and continue.

## 2.1.7. Document Lifecycle Rule

Permanent document lifecycle owner:

```text
docs/reference/V7_DOCUMENT_LIFECYCLE.md
```

Document classes:

| Class | Purpose | Examples | OMP rule |
| --- | --- | --- | --- |
| `REFERENCE` | Permanent knowledge. | System Architecture, Runtime Model, Decision Model, Kernel, Context Resolver, Canonical Policy Library. | Frozen after certification; OMP does not edit during normal implementation. |
| `PROGRAMS` | Drive execution. | OMP, Implementation Program, Current Program State. | Live and updated when execution or optimizer state changes. |
| `IMPLEMENTATION` | The only engineering queue. | Implementation Backlog, Implementation Priority Model. | OMP selects work only from the backlog. |
| `REPORTS` | Historical evidence only. | Certified reports. | Never planning, never backlog, never roadmap. |
| `ADR` | Permanent decisions. | Accepted ADRs. | Read-only decision constraints, never queue. |

Permanent rules:

1. Reference documents are frozen after certification.
2. The Canonical Policy Library is frozen after Stage 4 V7 Fit Analysis.
3. OMP must never generate implementation work from policy documents.
4. OMP generates implementation work only from:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
```

5. After every implementation:

```text
Update backlog
  -> Update Current Program State
  -> Update OMP
  -> Continue
```

6. OMP must never ask:

```text
What should I implement?
```

It must always read:

```text
Highest unfinished backlog item
```

7. Reports never generate implementation.
8. Policies never generate implementation.
9. Architecture never generates implementation.
10. Only the Implementation Backlog generates implementation.
11. When the backlog becomes empty, OMP must answer:

```text
IMPLEMENTATION_COMPLETE
```

and stop.

World research must include all relevant successful systems and must not stop after the first example.
Required sources include, where applicable: Cisco, Juniper, Arista, Cloudflare, Google, Google SRE, Google Traffic Engineering, Netflix, AWS, Azure, GCP, Kubernetes, Envoy, Istio, Linkerd, HAProxy, NGINX, Meta, Microsoft, Apple, OpenBSD PF, Linux routing, BGP, OSPF, IS-IS, MPLS, SD-WAN, IETF RFCs, academic papers, production postmortems, large-scale distributed systems, operator best practices, community consensus, and any other highly relevant industry source.

Consensus detection must record:

- consensus;
- strength of consensus;
- supporting systems.

Disagreement detection must record:

- why disagreement exists;
- tradeoffs;
- when each approach is used.

Reality audit must compare world practice against:

- current V7 architecture;
- current Runtime;
- current Product Specification;
- current OMP;
- current implementation.

V7 fit analysis must evaluate:

- compatibility;
- performance;
- safety;
- operator burden;
- autonomy;
- learning;
- scalability;
- complexity;
- reuse potential.

Allowed policy decisions:

- `REUSE`;
- `ADAPT`;
- `REJECT`.

Innovation rule:

V7 may innovate only after proving:

- no stable world consensus exists;
- or world consensus does not fit V7 architecture.

Otherwise:

```text
Reuse world knowledge.
```

Initial first policy selected for research was:

`POLICY_001_HARD_FAILURE`

Current Canonical Policy Library state:

`V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`

Current policy lifecycle stop:

```text
POLICY_001_HARD_FAILURE
POLICY_002_SOFT_DEGRADATION
POLICY_003_RECOVERY_ADMISSION
POLICY_004_AUTHORITY
POLICY_005_ACTION_CLASS_PROMOTION
POLICY_006_BLAST_RADIUS
POLICY_007_ROLLBACK
POLICY_008_FRESHNESS
POLICY_009_ANTI_FLAP
  -> DISCOVER
  -> FULL WORLD RESEARCH
  -> KNOWLEDGE NORMALIZATION
  -> INDUSTRY CONSENSUS DETECTION
  -> CANONICAL POLICY INTERACTION AUDIT
  -> REALITY AUDIT
  -> V7 FIT ANALYSIS
  -> IMPLEMENTATION BACKLOG READY
  -> STOP
```

Next allowed lifecycle stage:

`IMPLEMENTATION_BACKLOG_EXECUTION`

Runtime behavior remains unchanged.
Authority remains unchanged.
No policy implementation is enabled.

## 2.1.8. Research And Architecture Gating Rules

Research changes implementation only through:

```text
Research
  -> Decision Model
  -> OMP
  -> Implementation
```

Research must not create architecture directly.

Architecture changes require a real implementation to prove `FUNDAMENTAL_ARCHITECTURE_GAP`.

Otherwise:

```text
Reuse
  -> Extend
  -> Implement
```

## 2.2. Safety-Bounded Authority Model

V7 must not wait for global self-trust before every small governed action.

V7 separates:

- Knowledge Maturity
- Execution Authority

Knowledge Maturity controls autonomy tier progression.

Execution Authority controls whether an approved action class may execute a fresh bounded packet now.

Core rule:

```text
Trust decides autonomy tier.
Safety decides whether a fresh packet inside approved authority may execute.
```

Knowledge Maturity answers:

```text
How autonomous may V7 become?
```

Execution Authority answers:

```text
May this action class execute this fresh bounded packet now?
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

For `GOVERNED_ONLY`, the explicit approval may still be packet-level because the class is not certified yet.
For `CERTIFIED_FOR_CLASS_APPROVAL`, `CERTIFIED_FOR_BOUNDED_AUTONOMY`, or `AUTONOMOUS_RUNTIME`, OMP must prefer class authority and policy authority over repeating packet approval.

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
  -> Action-Class Authority
  -> Fresh Packet
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
| Desired capability | Validate the current highest leverage action and execute any safer maturity-gaining portion before the normalized authority gate. |
| Existing owners found | `v7-autonomy-trust-evidence-inventory`, `v7-governed-canary-dry-run-cycle`, `v7-egress-quality-compact`, `v7-service-matrix-refresh-all`, `v7-intelligence-snapshot-refresh`, existing packet/restore/verification/outcome/learning owners. |
| Semantic equivalent owners | Existing service matrix / quality snapshot owners cover service verification and freshness; existing governed canary dry-run covers packet/restore/outcome/learning preview; existing inventory covers OMP recalculation. |
| Composition strategy | Recalculate with inventory, challenge with governed dry-run, execute only existing service/quality/snapshot refresh owners, then recalculate. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse production owners as-is; no new CLI, API, storage, read model, planner, governance, execution, or truth source. |
| Extension strategy | None required for the safe portion. |
| Need New Owner | `FALSE` |

Historical semantic reuse audit for OMP V3.0:

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

Current semantic reuse audit for OMP V4.0:

| Field | Current Value |
| --- | --- |
| Desired capability | Finalize OMP as the permanent production operating program and single execution program without creating a separate roadmap owner. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`, `docs/reference/V7_IMPLEMENTATION_MODEL.md`, `docs/reference/V7_SYSTEM_ARCHITECTURE.md`, `docs/reference/V7_RUNTIME_MODEL.md`, `docs/reference/V7_DECISION_MODEL.md`, `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, Canonical Reference, SYSTEM_MAP, relevant ADRs |
| Composition strategy | Extend OMP in place; keep Implementation Program and Implementation Model as supporting references; keep volatile packet and metrics in Current Program State. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as the production operating program; reuse Current Program State as volatile state; reuse existing research, decision, runtime, planner, governance, execution, truth, evidence, and learning owners. |
| Extension strategy | Add production maturity ladder, authority evaluation, continuous optimization, continuous knowledge evolution, and permanent command surface to OMP. |
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
2. current authority class;
3. current reality limit;
4. existing owner availability;
5. production safety;
6. expected maturity gain;
7. implementation effort;
8. reversibility;
9. testability;
10. truth/convergence impact;
11. whether the task moves V7 toward Production Autonomy without crossing forbidden boundaries.

Canonical Policy Library Stage 4 adds a permanent backlog-backed selection rule:

```text
Read Implementation Backlog
  -> Apply Implementation Priority Model
  -> Select highest-priority unfinished item
  -> Semantic Reuse Audit
  -> Reuse existing owner
  -> Implement
  -> Test
  -> Verify
  -> Truth
  -> Convergence
  -> Certification if required
  -> Mark backlog item DONE
  -> Recalculate backlog
  -> Continue
```

The implementation backlog is:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
```

The priority model is:

```text
docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md
```

OMP must not select implementation work by document order.
OMP must select by production leverage.
If the highest item crosses authority, real-world, unsafe-implementation, or fundamental-architecture boundaries, OMP stops with the exact stop condition and may choose the next highest item only when the blocked item cannot progress.

Current backlog progress:

| Scope | Complete | Total | Status |
| --- | ---: | ---: | --- |
| Tier A | `2` | `6` | `ACTIVE` |
| Tier B | `0` | `20` | `PENDING` |
| Tier C | `0` | `7` | `PENDING` |
| Tier D optional | `0` | `6` | `OPTIONAL` |
| Overall actionable | `2` | `33` | `ACTIVE` |

Implementation maturity:

```text
6.1%
```

Estimated remaining effort:

```text
Moderate
```

Next backlog item:

```text
A3
```

## 2.12.1. Engineering and Production Maturity

Permanent maturity model:

```text
docs/reference/V7_PRODUCTION_MATURITY_MODEL.md
```

OMP must track two independent maturity dimensions:

1. `ENGINEERING MATURITY`
2. `PRODUCTION MATURITY`

Engineering Maturity measures completed engineering knowledge.

Production Maturity measures production readiness.

Engineering completion does not imply production autonomy.

Production Maturity must increase only through real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy.

Backlog completion must increase only Production Maturity.

Reference documents must never change Engineering Maturity after certification unless industry consensus changes, implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`, or the operator explicitly requests a reference update.

OMP must recalculate both maturity dimensions after every:

- implementation;
- deploy;
- truth;
- convergence;
- certification;
- production outcome;
- authority decision.

Engineering Maturity is the weighted total of:

- Architecture;
- Decision Model;
- Runtime Model;
- System Architecture;
- Research;
- Canonical Policies;
- OMP.

Production Maturity is the weighted total of:

- Implementation;
- Production Deployment;
- Testing;
- Certification;
- Authority Evolution;
- Production Outcomes;
- Production Autonomy;
- Implementation Backlog Completion.

Current engineering snapshot:

| Category | Current % | Target % | Weight |
| --- | ---: | ---: | ---: |
| Architecture | `100` | `100` | `15` |
| Decision Model | `100` | `100` | `15` |
| Runtime Model | `100` | `100` | `15` |
| System Architecture | `100` | `100` | `15` |
| Research | `100` | `100` | `15` |
| Canonical Policy Library | `100` | `100` | `15` |
| OMP | `100` | `100` | `10` |

Engineering Maturity:

```text
Current: 100.0%
Status: ENGINEERING_COMPLETE
```

Current production snapshot:

| Category | Current % | Target % | Weight |
| --- | ---: | ---: | ---: |
| Implementation | `6.1` | `100` | `20` |
| Testing | `34` | `100` | `10` |
| Production Deployments | `100` | `100` | `10` |
| Production Outcomes | `10` | `100` | `15` |
| Certification | `22` | `100` | `15` |
| Authority Evolution | `15` | `100` | `10` |
| Production Autonomy | `0` | `100` | `10` |
| Implementation Backlog Completion | `6.1` | `100` | `10` |

Production Maturity:

```text
Current: 21.5%
Target: 100%
Remaining: 78.5%
```

Backlog:

```text
Tier A: 2 / 6 complete
Tier B: 0 / 20 complete
Tier C: 0 / 7 complete
Tier D: 0 / 6 optional complete
Overall: 2 / 33 actionable complete
```

Current highest implementation task:

```text
A3: Certify class-level rollback/no-rollback evidence for governed candidate movement.
```

Estimated remaining effort:

```text
Moderate
```

Current autonomy tier:

```text
TIER_1_GOVERNED
```

Next milestone:

```text
35%: Runtime Eligibility Implemented
```

Milestones:

Engineering milestones finish at:

```text
ENGINEERING_COMPLETE
```

Production milestones finish at:

```text
PRODUCTION_AUTONOMY_CERTIFIED
```

| Production milestone | Meaning |
| ---: | --- |
| `20%` | First Implementation Certified |
| `35%` | Runtime Eligibility Implemented |
| `50%` | Implementation Half Complete |
| `65%` | Certification Half Complete |
| `80%` | Runtime Production Ready |
| `90%` | Bounded Production Autonomy |
| `100%` | Production Autonomy Certified |

## 2.12.2. V7 Production Status

OMP must print this block after every execution:

```text
V7 PRODUCTION STATUS

ENGINEERING

Architecture
100%

Research
100%

Policies
100%

Engineering Maturity
100.0%

PRODUCTION

Implementation
6.1%

Certification
22%

Autonomy
0%

Production Maturity
21.5%

Overall Status
ENGINEERING_COMPLETE / PRODUCTION_IN_PROGRESS

Current Focus
IMPLEMENTATION

Backlog
Tier A
2 / 6
Tier B
0 / 20
Tier C
0 / 7
Tier D
0 / 6 optional
Overall
2 / 33 complete

Current Tier
TIER_1_GOVERNED

Highest Priority Task
A3 fix: Bind operator approval context to execution lease creation.

Status
Unsafe Implementation

Authority
None

Required Action
Implement existing packet/lease owner fix before another approval

Estimated Remaining Work
Moderate

Expected Next Milestone
35%: Runtime Eligibility Implemented
```

Progress calculation must be automatic.
The displayed percentage must come from `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`.
Backlog progress must come from `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`.
Current volatile state must come from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

OMP must recalculate Production Status after:

- backlog completion;
- deploy;
- truth;
- convergence;
- certification;
- production outcome;
- authority decision.

Current focus values:

- `IMPLEMENTATION`
- `CERTIFICATION`
- `AUTHORITY`
- `AUTONOMY`
- `PRODUCTION`

Focus transition:

```text
IMPLEMENTATION
  -> CERTIFICATION
  -> AUTHORITY EVOLUTION
  -> PRODUCTION AUTONOMY
  -> CONTINUOUS IMPROVEMENT
```

Completion outputs:

| Condition | OMP output |
| --- | --- |
| Every mandatory implementation item is complete | `IMPLEMENTATION_COMPLETE` |
| Every certification is complete | `CERTIFICATION_COMPLETE` |
| Bounded autonomy is certified | `PRODUCTION_AUTONOMY_READY` |
| Production autonomy is certified | `PRODUCTION_AUTONOMY_CERTIFIED` |

Future normal operator commands:

- `Continue OMP`
- `Status`
- `Approve packet`
- `Approve authority expansion`

OMP must never request a new roadmap.
OMP must never request a new implementation plan.
OMP must continue using the existing backlog until completion.

Current implementation optimizer result:

| Field | Current Value |
| --- | --- |
| Highest implementation leverage task | `A3_FIX_APPROVAL_CONTEXT_TO_EXECUTION_LEASE_BINDING_IN_EXISTING_PACKET_OWNER` |
| Implementation class | `IMPLEMENT_CERTIFICATION` |
| Exact owner | Restore barrier, guarded autoswitch execution, verification, rollback, outcome closure, feedback/learning |
| Exact module | Canonical Policy Library Stage 4 implementation backlog |
| Exact files | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py` |
| Implementation status | `STOPPED_AT_UNSAFE_IMPLEMENTATION_AFTER_APPROVAL_CONTEXT_MISMATCH` |
| Backlog source | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` item `A3` |
| Priority model | `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md` |
| Truth/convergence | `PASS`: local, GitHub, and runtime aligned at commit `704ec9a2de66e10a5a677d5be1453463063de21e`. |
| New highest implementation leverage task | `A3_FIX_APPROVAL_CONTEXT_TO_EXECUTION_LEASE_BINDING_IN_EXISTING_PACKET_OWNER` |
| Stop boundary | `UNSAFE_IMPLEMENTATION`: operator approval for one packet allowed lease creation for a different packet before apply. |

Latest safe deployment result:

| Field | Current Value |
| --- | --- |
| Deployed commit | `704ec9a2de66e10a5a677d5be1453463063de21e` |
| Deploy id | `deploy-z8-14-Updatesystem-704ec9a-20260626T103417` |
| Deployed backlog items | `A1`, `A2`; A3 implementation safety fix |
| Safety | `restore_barrier_modified=false`; `routing_mutation_executed=false`; `user_movement_executed=false`; `autoswitch_apply_executed=false` |
| Truth | `PASS` |
| Convergence | `PASS`; `ALIGNED` |
| Current stop | `UNSAFE_IMPLEMENTATION`: approved packet was not consumed by lease creation; no apply or user movement occurred |

## 2.13. Implementation Program Loop

Future production implementation loop:

```text
Read Kernel
  -> Read OMP
  -> Read Current Program State
  -> Read Implementation Backlog
  -> Apply Implementation Priority Model
  -> Determine highest unfinished implementation leverage
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Deploy
  -> Truth
  -> Convergence
  -> Certification
  -> Update Current Program State
  -> Update OMP
  -> Mark backlog item DONE
  -> Recalculate backlog
  -> Authority Evaluation
  -> Continue
```

Stop only at:

- `OPERATIONAL_AUTHORITY`
- `ENGINEERING_AUTHORITY`
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
  -> Current Authority Class
  -> Current Real World Limit
  -> Next Best Action
```

## 5. Current System State

This section must be recalculated after every certification from canonical reference, system map, ADRs, and latest certified reports.

| Maturity Area | Current State | Evidence |
| --- | --- | --- |
| Architecture maturity | `ARCHITECTURE_COMPLETE` | Final system architecture synthesis: remaining architectural weaknesses `0`; optional improvements are not implementation blockers. |
| Knowledge maturity | `ADVANCED_BUT_NOT_AUTONOMY_COMPLETE` | Knowledge quality model exists; safety is autonomy-grade; several knowledge classes still need real outcomes, service/user/SLA fit depth, client observation, cohort/SLA scale, and aging/retirement. |
| Decision maturity | `READY_UNTIL_OPERATIONAL_AUTHORITY` | Planner, knowledge-to-decision, governed dry-run, packet preview, restore/rollback preview, and self-stop are connected. |
| Outcome maturity | `REAL_OUTCOMES_REQUIRED` | Candidate outcome gap remains `72`; missing candidate outcomes are not hidden, they have not happened yet. |
| Learning maturity | `CONNECTED_AFTER_OUTCOME` | Feedback, outcome closure, trust evolution, and learning refresh owners exist and are connected, but need real governed/manual outcomes. |
| Suitability maturity | `HIGHEST_BOTTLENECK` | Suitability cannot become autonomy-grade without more real candidate outcomes and stronger candidate source confidence. |
| Authority maturity | `OPERATIONAL_AUTHORITY_REACHED` | Production governed dry-run reaches exact packet approval boundary before restore-barrier write or apply. |
| Operational maturity | `PRODUCTION_PROGRAM_ACTIVE` | OMP V4.0 optimizes production leverage through existing-owner implementation and authority evolution; no daemon, no autonomous apply, no user movement without authority. |

## 6. Current Highest Bottleneck

Exactly one bottleneck:

`Suitability`

Why this bottleneck is highest right now:

| Evidence | Meaning |
| --- | --- |
| Missing candidate outcomes: `72` | The main weak object is real candidate suitability evidence. |
| Maximum projected current suitability remains below TIER_2 even after current missing outcomes | More rows alone are not enough; correctness/source confidence must improve too. |
| Architecture missing classes: none | The limiting factor is not architecture. |
| Governed dry-run reaches `OPERATIONAL_AUTHORITY` | The limiting factor is not disconnected planner/packet/restore/learning owners. |
| Confidence/trust/prediction are also below floor | They matter, but suitability is the bottleneck that specifically requires real candidate outcome closure. |

Recompute rule:

After every certification, classify bottlenecks across `Architecture`, `Knowledge`, `Decision`, `Outcome`, `Learning`, `Suitability`, `Prediction`, `Authority`, `Operational`, and `Scale`. Select exactly one class based on the largest maturity gain that cannot be obtained by already-certified safe automation.

## 7. Current Highest Implementation Leverage

Implementation:

`IMPLEMENT_AUTHORITY_BOUNDARY_APPROVAL_PROMPT`

This is implementation work, not research and not architecture.

Definition:

Emit a ready-to-copy exact operator approval prompt inside the existing governed canary dry-run cycle whenever the cycle stops at `OPERATIONAL_AUTHORITY` with a ready packet.

Exact owner:

`Governed Canary Knowledge-Gated Dry-Run Cycle / Runtime Model composition`

Exact module:

`admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle`

Exact files:

- `admin_core/operator_execution_pipeline.py`
- focused tests for governed dry-run authority-bound prompt output

Why this is first:

| Criterion | Result |
| --- | --- |
| Production leverage | Removes the last safe implementation gap before authority-bound governed canary execution. |
| Existing owner reuse | Uses the existing governed canary dry-run cycle and Runtime Model composition. |
| Architecture risk | None; architecture is complete and unchanged. |
| Runtime safety | Read-only approval prompt output only; no restore-barrier write, no apply, no user movement, no daemon, no timer. |
| Bottleneck relevance | Gives the operator an exact current packet command so the next real outcome can proceed only through explicit authority. |
| Testability | Authority boundary prompt emission, stale approval invalidation, unsafe stop suppression, and no-mutation guarantees can be tested without mutation. |
| Certification path | Truth and convergence can certify no runtime mutation and no user movement. |

Required approval prompt fields:

- packet preview id;
- decision id;
- operation id;
- selected move hash;
- user;
- current channel;
- target channel;
- rollback target;
- rollback manifest id;
- authority tier;
- authority status;
- allowed action;
- forbidden actions;
- final exact approval command text.

Expected implementation order:

1. Add read-only authority-bound approval prompt output to existing governed canary dry-run cycle.
2. Add focused tests for prompt emission, changed-packet invalidation, unsafe stop suppression, and no movement/apply.
3. Add read-only verification for the approval prompt output.
4. Certify with truth and convergence.
5. Update Current Program State.

The old bottleneck action, governed candidate suitability outcome closure, remains the highest real-outcome action, but the current blocker is earlier: approval context is not bound to execution lease creation.
The current implementation-first optimizer must fix the existing packet/lease owner before requesting another exact packet approval.

## 8. Current Authority Class

| Field | Current Value |
| --- | --- |
| Current authority level | `NONE_ACTIVE` |
| Current stop reason | `UNSAFE_IMPLEMENTATION` |
| Boundary location | Before active execution lease, restore-barrier write, runtime apply, and user movement. |
| Current exact runtime posture | No autonomous apply, no user movement, no daemon enablement. |
| Next authority action | None until approval-context-to-lease binding is fixed. |

Current production evidence:

- operator approval for one packet generated a different execution lease packet;
- unauthorized lease was cancelled;
- no approval prompt is currently valid;
- no restore-barrier clearance was written;
- no apply occurred;
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
4. Current authority class.
5. Current reality limit.
6. Next best action.
7. Whether automatic continuation is allowed.

Optimizer rules:

| Condition | Program Response |
| --- | --- |
| Highest implementation leverage is read-only | Continue automatically. |
| Highest implementation leverage is safe existing-owner implementation with no runtime apply | Continue automatically. |
| Highest implementation leverage requires exact restore-barrier write for an approved packet | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires exact runtime apply | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires exact user movement | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires exact rollback apply | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires authority expansion | Stop at `ENGINEERING_AUTHORITY`. |
| Highest implementation leverage requires new action class, new runtime capability, new autonomous policy, or blast-radius expansion | Stop at `ENGINEERING_AUTHORITY`. |
| Highest implementation leverage requires more users/channels/services/reality | Stop at `REAL_WORLD_LIMIT`. |
| Highest implementation leverage would create duplicate planner/governance/execution/truth | Stop at `UNSAFE_IMPLEMENTATION`. |
| Certified reports reveal a fundamental missing owner | Stop at `FUNDAMENTAL_ARCHITECTURE_GAP`. |

Safety-Bounded Authority split rule:

When the highest leverage action requires real outcomes, Codex must split it into:

| Portion | Work | Program Response |
| --- | --- | --- |
| Safe automatic preparation | Refresh evidence; refresh packet preview; verify restore/rollback preview; verify verification plan; verify outcome closure plan; verify learning path; update OMP; present exact authority decision. | Continue automatically. |
| Operational-authority execution | Exact restore-barrier write; exact runtime apply; exact user movement; exact rollback apply; exact production action. | Stop at `OPERATIONAL_AUTHORITY`. |
| Engineering-authority change | Authority expansion; new action class; new runtime capability; new autonomous policy; blast-radius expansion; daemon/timer enablement. | Stop at `ENGINEERING_AUTHORITY`. |

The safe automatic portion continues automatically.

The authority-bound portion stops at the normalized authority class: `OPERATIONAL_AUTHORITY` for exact production action approval, or `ENGINEERING_AUTHORITY` for capability/policy/authority expansion.

## 10.1. Root Cause Engine

OMP must run the Root Cause Engine before exposing any stop condition.

Raw blocker codes are technical details only. They must never be the primary result of an OMP stop.

Primary stop output must always be:

```text
Root Cause
  -> Owner
  -> Fix
  -> Expected Evidence
  -> Next Action
```

Root Cause Engine workflow:

```text
Blocker
  -> Root Cause Analysis
  -> Owner Attribution
  -> Implementation Classification
  -> Concrete Engineering Task
  -> Expected Completion Evidence
  -> Continue Decision
```

Required stop record:

| Field | Requirement |
| --- | --- |
| Root Cause | Concrete cause, not a generic blocker code. |
| Responsible owner | Exact existing owner, module, and function when known. |
| Why it happened | Specific mechanism that created the stop. |
| Why existing safety worked | Which gate prevented unsafe runtime behavior. |
| Can existing owner be extended? | `YES` or `NO`; default is `YES` unless proven otherwise. |
| Need New Owner | `FALSE` unless a proven `FUNDAMENTAL_ARCHITECTURE_GAP` requires a new owner. |
| Implementation Class | One of `BUG`, `OWNER_EXTENSION`, `CONFIGURATION`, `CERTIFICATION`, `REAL_WORLD_LIMIT`, `AUTHORITY`, `DOCUMENTATION`. |
| Concrete implementation task | Backlog-ready task, not a recommendation. |
| Expected completion evidence | Observable evidence required to close the task. |
| Automatic continuation | Whether OMP may continue automatically after the task completes. |

Automatic classification:

| Stop Condition | Primary Classification | OMP Meaning | Next Action |
| --- | --- | --- | --- |
| `UNSAFE_IMPLEMENTATION` | `BUG` or `OWNER_EXTENSION` | Existing implementation path is unsafe, incomplete, or loses required state. | Fix the responsible existing owner, test, deploy if required, then resume OMP. |
| `OPERATIONAL_AUTHORITY` | `AUTHORITY` | Engineering is complete and the next action is one exact production operation, such as packet execution, rollback, restore-barrier write, runtime apply, or user movement. | Produce exact approve/reject decision for the current production action. |
| `ENGINEERING_AUTHORITY` | `AUTHORITY` | Engineering cannot continue because capability, policy, authority, action-class, runtime, or blast-radius approval is required. | Produce exact engineering approval or authority expansion request. |
| Legacy raw `AUTHORITY_BOUNDARY` | normalize before output | Compatibility-only blocker code. | Convert to `OPERATIONAL_AUTHORITY` or `ENGINEERING_AUTHORITY` before reporting status. |
| `REAL_WORLD_LIMIT` | `REAL_WORLD_LIMIT` | The next maturity gain requires real production evidence that cannot be synthesized. | Identify exact real-world action or observation required. |
| `FUNDAMENTAL_ARCHITECTURE_GAP` | `OWNER_EXTENSION` or architecture review | Existing certified owners cannot satisfy the requirement. | Prove why reuse/extension is impossible before any architecture change. |

Root Cause Engine constraints:

- reuse existing owners first;
- never create a new planner;
- never create new governance;
- never create new execution;
- never create a new truth source;
- never treat reports, policies, or architecture documents as implementation queues;
- never expose only `UNSAFE_IMPLEMENTATION`, `REAL_WORLD_LIMIT`, legacy raw `AUTHORITY_BOUNDARY`, or `FUNDAMENTAL_ARCHITECTURE_GAP` as the OMP result.

Current Program State storage:

`docs/programs/V7_CURRENT_PROGRAM_STATE.md` must store:

- `root_cause`;
- `responsible_owner`;
- `authority_class`;
- `authority_reason`;
- `authority_owner`;
- `required_action`;
- `implementation_class`;
- `next_engineering_task`;
- `expected_completion_evidence`.

Continuation rule:

| Classification | Automatic Continuation |
| --- | --- |
| `BUG` | Continue after implementation, tests, deployment if required, truth, and convergence. |
| `OWNER_EXTENSION` | Continue if extension stays inside existing owner boundaries and does not require authority expansion. |
| `CONFIGURATION` | Continue if read-only or safe configuration update is authorized by existing policy. |
| `CERTIFICATION` | Continue until real evidence, authority, or unsafe implementation boundary is reached. |
| `REAL_WORLD_LIMIT` | Stop with exact required production evidence. |
| `AUTHORITY` with `OPERATIONAL_AUTHORITY` | Stop with exact approve/reject command for the current production action. |
| `AUTHORITY` with `ENGINEERING_AUTHORITY` | Stop with exact engineering approval or authority expansion decision. |
| `DOCUMENTATION` | Continue if documentation is the active backlog item and no runtime mutation occurs. |

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
| Optimization target | Current HIL in `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Target class | Volatile current state |
| Gain type | Determined by OMP after reading Current Program State |
| Risk | Determined by current packet, implementation task, normalized authority class, and stop condition |
| Effort | Determined by current OMP recalculation |
| Authority | Stop at `OPERATIONAL_AUTHORITY` before exact restore-barrier write, apply, user movement, rollback apply, or production action; stop at `ENGINEERING_AUTHORITY` before daemon/timer, event consumer mutation, runtime capability, autonomous policy, blast-radius, action-class, or authority expansion |
| Safe automatic portion | Continue only through work that remains inside existing owners and does not cross the current stop boundary |

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
| Post-refresh dry-run verdict | `AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY`; normalized OMP stop `OPERATIONAL_AUTHORITY`. |
| Post-refresh packet state | Packet preview ready; restore/rollback preview ready; verification plan ready; outcome closure plan ready; learning path connected. |
| Optimizer conclusion | Safe challenger completed; final HLA remains governed candidate suitability outcome closure and stops at `OPERATIONAL_AUTHORITY`. |

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
| Authority Ratio | `OPERATIONAL_AUTHORITY_REACHED / NOT_EXPANDED` | Governed dry-run reaches exact packet approval boundary; no apply authority granted. |
| Operational Maturity | `OPTIMIZATION_ACTIVE` | OMP now drives bottleneck optimization rather than fixed phases. |

## 13. Self-Improvement Loop

Every implementation must follow:

```text
Read Kernel
  -> Read OMP
  -> Read Current Program State
  -> Determine highest implementation leverage
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Deploy
  -> Truth
  -> Convergence
  -> Certification
  -> Update Current Program State
  -> Update OMP
  -> Authority Evaluation
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

1. `OPERATIONAL_AUTHORITY`;
2. `ENGINEERING_AUTHORITY`;
3. `REAL_WORLD_LIMIT`;
4. `UNSAFE_IMPLEMENTATION`;
5. `FUNDAMENTAL_ARCHITECTURE_GAP`.

Before stopping, Codex must run the Root Cause Engine and expose the structured stop record as the primary output.

If the highest leverage action crosses an authority gate, Codex must:

1. stop before the boundary;
2. update this OMP;
3. normalize the boundary into `OPERATIONAL_AUTHORITY` or `ENGINEERING_AUTHORITY`;
4. report root cause, responsible owner, expected evidence, and exact next action;
5. wait for explicit operator authority for the exact action or engineering approval.

Production program loop for every future task:

```text
READ KERNEL
  -> READ OMP
  -> READ CURRENT PROGRAM STATE
  -> DETERMINE HIGHEST IMPLEMENTATION LEVERAGE
  -> SEMANTIC REUSE AUDIT
  -> REUSE
  -> EXTEND
  -> IMPLEMENT
  -> DEPLOY
  -> TRUTH
  -> CONVERGENCE
  -> CERTIFICATION
  -> UPDATE CURRENT PROGRAM STATE
  -> UPDATE OMP
  -> AUTHORITY EVALUATION
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
5. deploy completed and tested changes when project policy requires deployment;
6. run truth and convergence;
7. certify;
8. update Current Program State;
9. update OMP, reference, system map, or ADR if meaning changed;
10. evaluate authority;
11. recalculate;
12. continue;
13. stop only at an allowed stop condition.

If blocked by any allowed stop condition, Codex must output the Root Cause Engine record first:

- root cause;
- responsible owner;
- exact module and function when known;
- why it happened;
- why existing safety worked;
- whether the existing owner can be extended;
- Need New Owner verdict;
- implementation class;
- concrete engineering task;
- expected completion evidence;
- whether OMP can continue automatically after completion.

If blocked by `OPERATIONAL_AUTHORITY`, Codex must also output:

- exact packet;
- exact action;
- exact user;
- exact source;
- exact target;
- exact rollback target;
- exact command shape that must not run without approval;
- exact approval question.

If blocked by `ENGINEERING_AUTHORITY`, Codex must also output:

- exact authority expansion, action class, runtime capability, autonomous policy, or blast-radius change;
- owner requesting the approval;
- why engineering cannot continue without it;
- what remains unchanged if approval is rejected;
- exact approve/reject question.

This contract is constrained by Safety-Bounded Authority:

```text
Trust decides autonomy tier.
Safety decides bounded action.
```

Permanent operator command surface:

| Command | Meaning |
| --- | --- |
| `Continue OMP` | Run the OMP production loop through all safe implementation, verification, deployment, truth, convergence, certification, update, and authority evaluation work until an allowed stop condition. |
| `Status` | Print the current `V7 PRODUCTION STATUS` block without changing runtime state. |
| `Approve packet` | Approve one exact `GOVERNED_ONLY` packet while packet-level fallback is still required. |
| `Approve authority expansion` | Approve a specific authority expansion only after OMP recommends it from certified evidence. |

These commands are sufficient for future production operation unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 16. Program Health

| Health Dimension | Current Value | Notes |
| --- | --- | --- |
| Architecture completeness | `COMPLETE` | Fundamental architecture exists; future extensions remain optional/scale-related. |
| Knowledge completeness | `PARTIAL_FOR_AUTONOMY` | Knowledge objects exist but real outcome depth is insufficient for autonomy-grade suitability. |
| Cycle automation % | `84.167` | Autonomous knowledge growth program certified 12 cycles and maturity score `84.167`. |
| Authority maturity | `OPERATIONAL_AUTHORITY_REACHED` | Safe preparation reaches production action approval; apply authority is not granted. |
| Operational maturity | `OPTIMIZATION_ACTIVE` | OMP now optimizes bottleneck reduction rather than executing a fixed roadmap. |
| Remaining architecture uncertainty | `NONE_FUNDAMENTAL` | Partial classes are future/scale/authority extensions, not missing architecture. |
| Current optimization velocity | `OPERATIONAL_AUTHORITY_AFTER_SAFE_REFRESH` | Safe service/quality/snapshot refresh completed through existing owners; real candidate outcome gain needs exact packet approval. |

## 17. Historical Phase Anchor

`GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE`

Source:

- `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`
- `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`
- `docs/reference/SYSTEM_MAP.md`

Reason:

The final architecture certification says V7 has no fundamental architecture gap. The governed dry-run reaches `OPERATIONAL_AUTHORITY` with packet preview, restore/rollback preview, verification plan, outcome closure plan, and learning path connected. The next maturity gain requires real governed candidate outcome evidence.

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

1. `OPERATIONAL_AUTHORITY`
2. `ENGINEERING_AUTHORITY`
3. `REAL_WORLD_LIMIT`
4. `UNSAFE_IMPLEMENTATION`
5. `FUNDAMENTAL_ARCHITECTURE_GAP`

Legacy raw `AUTHORITY_BOUNDARY` may appear in older reports or compatibility tool output, but OMP must normalize it before presenting status.

Current blocker:

`UNSAFE_IMPLEMENTATION`

Details:

- operator approved `pkt_preview_4eb137c926917c2761faadb4`;
- production lease creation generated different packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc`;
- unauthorized lease was cancelled before restore-barrier write or apply;
- route verification confirmed `10.7.0.17` remained on `vless`;
- fix existing packet/lease owner before another approval;
- no new owner is required.

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
| Governed Canary Knowledge-Gated Dry-Run Cycle | Production reaches legacy dry-run boundary; normalized OMP stop `OPERATIONAL_AUTHORITY`; no apply, no movement | `CERTIFIED` | `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md` |

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

If an exact restore-barrier write, apply, user movement, rollback apply, or production action is required, stop at `OPERATIONAL_AUTHORITY`.

If daemon, timer, event consumer mutation, autonomous execution, action-class expansion, blast-radius expansion, runtime capability expansion, autonomous policy approval, or authority expansion is required, stop at `ENGINEERING_AUTHORITY`.

## 23. Next Best Action Entry Criteria

| Entry Criterion | Required |
| --- | --- |
| Existing owner | Reuse `governed_canary_knowledge_gated_dry_run_cycle`; do not create a duplicate runtime owner. |
| Scope | Read-only lifecycle preview only. |
| Runtime model | Emit fields that map to `V7_RUNTIME_MODEL.md` lifecycle, state, stop, restart, duplicate, loop, idempotency, verification, rollback, learning, and OMP-notification semantics. |
| Apply path | Forbidden. No restore-barrier write, apply, rollback apply, or user movement. |
| Operational authority | Exact packet, rollback, restore-barrier, apply, or production action approval stops at `OPERATIONAL_AUTHORITY`. |
| Engineering authority | Authority expansion, action-class expansion, autonomous policy, runtime capability, daemon/timer, event-consumer mutation, or blast-radius expansion approval stops at `ENGINEERING_AUTHORITY`. |
| Tests | Focused tests must prove the lifecycle output is read-only and idempotency-aware. |
| Safety | No daemon enablement, no timers, no event consumer mutation, no duplicate planner/governance/execution. |

## 24. Program Certification

| Field | Current Value |
| --- | --- |
| Completed phases | Architecture foundation, Research Framework, Decision Model, Runtime Model, System Architecture, Implementation Phase activation, OMP Production Program integration. |
| Certified phases | Decision Model; Runtime Model; System Architecture; governed knowledge-gated dry-run cycle; OMP Production Program rule set. |
| Current bottleneck | Explicit authority for the current exact governed packet after the previous approval expired before apply and failed closed safely. |
| Current highest leverage action | `EXPLICIT_OPERATOR_APPROVAL_REQUIRED_FOR_THIS_PACKET`. |
| Current reuse ratio | `100%`. |
| Current duplicate ratio | `0% known introduced`. |
| Current automation ratio | `84.167%`. |
| Current blockers | Root Cause Engine output: operator approved `pkt_preview_4eb137c926917c2761faadb4`, but lease creation generated different packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc`; unauthorized lease was cancelled before restore-barrier write/apply; fix existing packet/lease owner before another approval. |
| Current maturity | Tier 0 `COMPLETE`; Tier 1 `ACTIVE`; read-only runtime lifecycle preview deployed and production-verified; preview-to-execution packet identity deployed and production-verified; execution lease deployed and production-verified; one approved leased governed canary outcome executed, verified, closed, and learned from. |
| Current runtime posture | No autonomous apply, no daemon enablement; last user movement was the explicitly approved one-user governed canary `10.7.0.5 vless -> awg0`. |
| Current next best action | Implement `A3_FIX_APPROVAL_CONTEXT_TO_EXECUTION_LEASE_BINDING_IN_EXISTING_PACKET_OWNER`; no approval prompt is valid until this fix is complete. |
| Last optimizer iteration | `2026-06-26`: operator approved `pkt_preview_4eb137c926917c2761faadb4`; production lease creation generated different packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc` with target `awg3`; OMP stopped before apply, cancelled the unauthorized lease, and route verification confirmed `10.7.0.17` remained on `vless`; no user was moved. |

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

That file owns the current bottleneck, HLA, normalized authority class, reality limit, metrics, exact packet, stop reason, and exact approval question.

OMP owns the scheduler and optimizer rules.

OMP also owns the permanent production maturity ladder, implementation loop, authority evaluation rule, continuous optimization rule, and research-to-implementation gate.

When packet fields, metrics, or stop reason change, update `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Update OMP only when scheduler/optimizer meaning changes.

## 27. Permanent Production Command Verdict

V7 can continue production evolution using only:

1. `Continue OMP`;
2. `Status`;
3. `Approve packet`;
4. `Approve authority expansion`.

No additional roadmap document is required.

This remains true unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.
