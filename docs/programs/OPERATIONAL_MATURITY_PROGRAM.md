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

`Continue OMP` means: execute the complete Engineering Control Loop through existing owners until an allowed stop condition.

### Continue OMP Engineering Control Loop

Status: `CANONICAL`

`Continue OMP` is the single default engineering command for V7.

It must not be interpreted as only:

```text
Continue the backlog.
```

It means:

```text
Execute the complete Engineering Control Loop.
```

The loop is:

```text
Engineering Context Resolver
  -> Knowledge Consumption
  -> Re-open Evaluation
  -> OMP Execution
  -> Implementation / Audit / Certification / Verification
  -> Engineering Report
  -> Knowledge Promotion
  -> Current Program State Update
  -> OMP Update
  -> Continue OMP
```

Step responsibilities:

| Step | Required behavior | Existing owner |
| --- | --- | --- |
| Engineering Context Resolver | Classify task, resolve minimum context, load only required owners. | `docs/reference/V7_CONTEXT_RESOLVER.md` |
| Knowledge Consumption | Read Product Specification, Canonical Reference, SYSTEM_MAP, Audit Knowledge State, Current Program State, OMP, current Backlog item, and Runtime Model only if runtime relevant. | Knowledge Plane / OMP |
| Re-open Evaluation | Determine whether knowledge is already verified, still current, stale, confidence-limited, or re-opened by trigger. | Knowledge Plane / Canonical Reference / relevant owner |
| OMP Execution | Determine highest production-leverage existing backlog item; reuse existing owners; do not redesign. | OMP |
| Implementation | Implement only existing backlog work when implementation is the resolved action. | Implementation Backlog + existing code owner |
| Verification | Run relevant tests, truth, convergence, runtime verification, documentation consistency, or knowledge consistency only when required by task class. | OMP + relevant verification owner |
| Certification | Certify only when required by OMP capability, policy, action class, or production maturity. | OMP + certification owner |
| Engineering Report | Create a Russian Engineering Report after every meaningful engineering action. | OMP report lifecycle |
| Knowledge Promotion | Extract durable knowledge from reports and update canonical owners when needed. | Canonical owner + Canonical Reference + SYSTEM_MAP |
| Current Program State Update | Update only when execution state, bottleneck, authority class, maturity, current task, or stop condition changes. | Current Program State |
| OMP Update | Update only when optimizer, capability, command, stop, or maturity semantics change. | OMP |

Every future engineering task should begin with `Continue OMP` unless the operator explicitly requests a narrower action.

No future engineering work should bypass:

```text
Engineering Context Resolver
  -> Knowledge Plane
  -> OMP
```

unless explicitly requested by the operator.

Automatic stop conditions:

| Condition | Stop meaning |
| --- | --- |
| Operator authority required | Stop with exact engineering or operational authority decision. |
| Runtime apply required | Stop before apply or irreversible production action. |
| Production movement required | Stop before user movement. |
| Architecture contradiction discovered | Stop through Architecture Closed by Default and Root Cause Engine. |
| Canonical owner missing | Stop with Need New Owner audit result; default remains `FALSE`. |
| Re-open trigger fired | Stop or branch into the existing owner re-audit path. |
| Product contradiction discovered | Stop and map to Product Specification owner. |

Automatic continue conditions:

| Condition | Continue behavior |
| --- | --- |
| Only implementation remains | Continue through existing backlog item. |
| Only documentation remains | Continue through existing canonical owner or report lifecycle. |
| Only integration remains | Continue through existing owner integration. |
| Only certification remains | Continue through existing certification path. |
| Only verification remains | Continue through relevant verification owner. |
| Only knowledge promotion remains | Continue through canonical update path. |

This command creates no new owner, planner, governance layer, runtime path, truth source, roadmap, backlog, daemon, timer, apply authority, or user movement authority.

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

## 2.1.6. Decision Explainability

Decision Explainability is the permanent OMP capability for explaining existing decisions before any operator approval request.

It is an explainability layer only.
It does not change decision making.
It does not create a new planner.
It does not create new governance.
It does not create a new Runtime owner.
It does not create a new execution path.
It does not approve packets, approve action classes, expand authority, write restore barriers, apply, roll back, move users, create evidence, or lower floors.

Purpose:

The operator must approve a decision, not a packet.

Before any approval request, Runtime / OMP must explain the decision in human language using existing decision, evidence, policy, safety, rollback, and authority owners.

Operator explanations must be written only in Russian.

Every approval request must answer:

1. Почему вообще рассматривается переключение?
2. Почему именно сейчас?
3. Почему выбран именно этот пользователь?
4. Почему текущий канал считается недостаточно хорошим?
5. Почему выбран именно этот целевой канал?
6. Какие проверки уже прошли успешно: Hard Failure, Soft Degradation, Freshness, Recovery Admission, Blast Radius, Rollback, Anti-Flap, Authority, State Change Cost, Net Benefit?
7. Почему система считает, что лучше переключить, чем оставить как есть?
8. Что произойдет, если ничего не делать?
9. Что произойдет после переключения?
10. Какие риски остаются?
11. Почему Runtime уверен в этом решении?
12. Какое Production Value ожидается?
13. Какой Capability Progress даст успешное выполнение?

Operator view order:

```text
Причина
  -> Доказательства
  -> Ожидаемая польза
  -> Риски
  -> Approve / Reject
```

Language rules:

| Surface | Language |
| --- | --- |
| Operator explanations | Russian only |
| Engineering Reports | Russian only |
| Canonical documents | Existing document language |
| Code comments | Existing project language |

Definition of Done:

Decision Explainability is `COMPLETE` only when the operator can understand every approval request without reading source code and can honestly answer:

```text
Да, я понимаю, почему система хочет сделать именно это.
```

Completion criteria:

- every approval request includes the Russian decision explanation fields listed above;
- explanations are generated from existing evidence owners, not invented;
- every safety gate result is shown as passed, failed, unknown, or not applicable;
- alternatives are explained, including why keeping current state was not selected;
- expected production value and capability progress are shown;
- remaining risk is shown before Approve / Reject;
- no explanation can authorize runtime action by itself;
- missing evidence produces `STOP_SAFE`, not persuasive text.

Current status:

`IN_PROGRESS`.

Current progress:

`20.0%`.

Blocking backlog items:

`A3`, `A6`, `B1`, `B4`, `B13`, `B15`, `B17`, `C2`.

Completion prediction:

Decision Explainability completes after the operator approval surface explains current packet/class/policy decisions in Russian, ties every explanation to existing evidence, shows safety/risk/value before approval, and has been validated by real governed outcomes and operator review.

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
| `REPORTS` | Execution history and historical evidence only. | Certified reports and engineering reports under `docs/reports/engineering/`. | Not project documents; never planning, never backlog, never roadmap, never canonical owner. |
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

### Architecture Closed by Default

Status: `PERMANENT_ENGINEERING_PRINCIPLE`.

The V7 architecture is complete by default.

Every newly discovered problem, idea, regression, optimization, or improvement must first be treated as one of:

- unfinished implementation;
- missing integration;
- missing certification;
- missing runtime consumption;
- missing read-model consumption;
- missing production evidence;
- missing authority maturity;
- missing capability progress;
- missing backlog completion;
- missing canonical-owner update.

Architecture evolution is the last resort.

Before proposing an architectural extension, OMP must prove that the existing:

- OMP;
- Runtime Model;
- Product Specification;
- Canonical Policies;
- Implementation Backlog;
- Canonical Owners;
- SYSTEM_MAP;
- Canonical Reference;

cannot own the finding through reuse, extension, integration, certification, read-model consumption, runtime consumption, authority maturity, or production evidence.

Required Architecture Closed by Default output for meaningful work:

| Field | Required value |
| --- | --- |
| `architecture_closed_by_default` | `PASS`, `FAIL`, or `NOT_APPLICABLE_WITH_REASON`. |
| `first_classification` | `UNFINISHED_IMPLEMENTATION`, `MISSING_INTEGRATION`, `MISSING_CERTIFICATION`, `MISSING_RUNTIME_CONSUMPTION`, `MISSING_READ_MODEL_CONSUMPTION`, `MISSING_PRODUCTION_EVIDENCE`, `MISSING_AUTHORITY_MATURITY`, `MISSING_CAPABILITY_PROGRESS`, `MISSING_BACKLOG_COMPLETION`, `MISSING_CANONICAL_UPDATE`, or `FUNDAMENTAL_ARCHITECTURE_GAP_PROVEN`. |
| `existing_owner_mapping` | Existing OMP capability, backlog item, canonical owner, runtime section, policy, reference section, or `NONE_PROVEN_AFTER_AUDIT`. |
| `architecture_extension` | Default `FALSE`; may become `TRUE` only after complete audit proves reuse and extension impossible. |

If the gate fails, OMP must not redesign V7. It must return to the existing owner/backlog/capability path.

### Production Scale First

Status: `PERMANENT_ENGINEERING_PRINCIPLE`.

Production Scale First is an OMP execution discipline.

The canonical source is `V7_PRODUCT_SPECIFICATION.md` -> `Product Scale Model`.

Product Scale Model defines the product-level non-functional requirement.

Product Scale Objectives define the long-term optimization target.

Production Scale First is the execution gate that applies that product truth to every OMP decision.

Every future audit, implementation, test, report, policy change, runtime change, evidence model change, learning change, read model, UI/API data-loading change, storage change, background job, canonical update, and OMP decision must answer:

```text
Will this remain efficient, safe, and maintainable at 10,000+ users and 100+ channels?
```

Scale target:

- `10,000+` users;
- `100+` channels;
- millions of runtime decisions;
- long-lived evidence, telemetry, reports, and learning history.

OMP Production Scale First gate:

| Check | Required answer |
| --- | --- |
| Algorithmic complexity | State expected complexity. Avoid `O(N^2)` behavior and full rescans where possible. Prefer `O(1)`, `O(log N)`, bounded scans, incremental updates, indexes, and summaries. |
| Runtime path safety | Runtime must remain thin. Expensive work belongs to background jobs, pre-aggregation, read models, or offline analysis. Runtime consumes prepared and certified data. |
| Storage discipline | Store evidence once and derive summaries. Avoid duplicate durable data and unbounded growth without retention or compaction strategy. Distinguish hot, warm, and cold data where relevant. |
| Read-model discipline | UI, API, and operator views must use summaries, indexes, and drill-down. Normal views must not read massive raw histories. |
| Evidence and learning scale | Do not require full enumeration of all user-to-channel combinations as a permanent autonomy condition. Prefer representative action-class evidence, risk segmentation, blast radius, rollback/no-rollback proof, and learning quality. Enumeration metrics may remain useful signals but must not become non-scalable promotion blockers unless explicitly justified. |
| Reporting discipline | Engineering reports are compact evidence. Durable knowledge goes to canonical owners. Large raw outputs should be referenced or summarized, not duplicated into reports. |
| Indexing and query discipline | Every new persistent data shape must declare its expected lookup pattern. Data that can grow with users, channels, or time must declare an indexing or aggregation strategy. |
| Resource budget | Consider CPU, memory, disk, IO, latency, and write amplification before implementation is considered complete. |

Production scale validation questions:

1. Does runtime cost grow with user count?
2. Does storage grow without bounds?
3. Does CPU cost grow linearly?
4. Does memory growth remain controlled?
5. Can reports grow indefinitely?
6. Can telemetry be aggregated?
7. Can read models be precomputed?
8. Are indexes sufficient?
9. Can expensive work move out of Runtime?
10. Will this still be operationally efficient at production scale?

If the answer proves the proposal is not suitable for production scale, OMP must redesign the implementation approach through existing owners before implementation. It must not lower scale expectations.

Every OMP audit, implementation, report, and backlog decision must evaluate compliance with Product Scale Model. If a proposed solution creates linear or worse growth with users, channels, or time, it must be justified, bounded, indexed, aggregated, or redesigned through existing owners before implementation.

Every future implementation must explicitly state whether it moves V7 toward Product Scale Objectives or away from them.

Required OMP output for meaningful work:

| Field | Required value |
| --- | --- |
| `production_scale_first` | `PASS`, `FAIL`, or `NOT_APPLICABLE_WITH_REASON`. |
| `scale_impact` | Whether the change is bounded or grows with users, channels, or time. |
| `runtime_path_impact` | `NONE`, `READ_MODEL_ONLY`, `RUNTIME_CALCULATION`, or `HEAVY_RUNTIME_CALCULATION_FORBIDDEN`. |
| `storage_index_plan` | Existing summary, existing index, proposed extension through an existing owner, or no persistent data. |
| `resource_budget` | Expected CPU, memory, disk, IO, latency, and write-amplification impact. |
| `evidence_model_scale` | Representative action-class evidence or a justified enumeration signal. |
| `product_scale_objectives_direction` | `TOWARD`, `AWAY`, or `NEUTRAL_WITH_REASON`. |
| `need_new_owner` | Default `FALSE`; if `TRUE`, prove through the New Owner Gate. |
| `need_new_backlog_item` | Default `FALSE`; if `TRUE`, prove through the Backlog Consistency Audit. |

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
| Law 11 | Production Scale First. Every change must remain efficient, safe, and maintainable at `10,000+` users and `100+` channels. Runtime stays thin; scale work belongs to read models, indexes, background jobs, summaries, and existing owners. |
| Law 12 | Architecture Closed by Default. V7 architecture is complete unless a complete audit proves that existing OMP capabilities, backlog items, runtime model, product specification, canonical policies, canonical owners, SYSTEM_MAP, and Canonical Reference cannot own the finding. |

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

Before creating any new owner, backlog item, policy, runtime path, architectural element, knowledge model, planner, engine, pipeline, API, CLI, storage, snapshot, or truth source, OMP must prove:

```text
Need New Owner = TRUE
Need New Backlog Item = TRUE
Architecture Extension = REQUIRED
```

`Need New Owner` may be true only when existing semantic coverage is insufficient.

If semantic coverage is sufficient, creation is forbidden.

Permanent OMP engineering rule:

```text
Discover
-> Verify
-> Map
-> Reuse
-> Extend Existing
-> Implement
-> Certify
```

Before proposing any new owner, backlog item, policy, runtime path, planner, governance layer, execution path, truth source, or architectural element, OMP must first audit and map the finding to existing canonical ownership.

Required mapping order:

1. OMP Capability
2. Implementation Backlog
3. Canonical Owner
4. Runtime Model
5. Canonical Policy
6. Canonical Reference
7. SYSTEM_MAP or ADR if ownership or decision meaning is involved

Default verdicts:

| Field | Default |
| --- | --- |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Architecture Extension | `LAST_RESORT` |

If an existing owner, capability, backlog item, policy, model, or reference covers the finding, OMP must:

- map the finding to that owner;
- continue through the existing OMP;
- extend the existing owner only;
- avoid creating new architecture, owner, backlog item, policy, runtime path, planner, governance, execution, or truth source.

Only after complete mapping proves no existing canonical owner or backlog item can cover the finding may OMP propose `CREATE_NEW`. That proposal must include proof of impossible reuse and must stop for explicit operator review.

Permanent queue rule:

OMP remains the single execution program.

Implementation Backlog remains the single engineering queue.

Reports, policies, reference documents, architecture documents, and canonical knowledge never generate implementation work directly. They may only update canonical owners or the existing Implementation Backlog through OMP.

Required gate output:

| Field | Required |
| --- | --- |
| Desired capability | Clear capability statement. |
| Existing semantic coverage | Percent and evidence. |
| OMP Capability mapping | Existing capability or `NONE_PROVEN`. |
| Implementation Backlog mapping | Existing backlog item or `NONE_PROVEN`. |
| Canonical Owner mapping | Existing canonical owner or `NONE_PROVEN`. |
| Runtime Model mapping | Existing runtime section or `NONE_PROVEN`. |
| Canonical Policy mapping | Existing policy or `NONE_PROVEN`. |
| Canonical Reference mapping | Existing canonical section or `NONE_PROVEN`. |
| Reuse candidate owners | List. |
| Extension strategy | How existing owners can be extended. |
| Merge strategy | How duplicate/overlapping owners can be merged. |
| Need New Owner | `TRUE` or `FALSE`. |
| Need New Backlog Item | `TRUE` or `FALSE`. |
| Architecture Extension | `NONE`, `EXTEND_EXISTING`, or `LAST_RESORT`. |
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
| Tier B | `0` | `21` | `PENDING` |
| Tier C | `0` | `7` | `PENDING` |
| Tier D optional | `0` | `6` | `OPTIONAL` |
| Overall actionable | `2` | `34` | `ACTIVE` |

Implementation maturity:

```text
5.9%
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
| Implementation | `5.9` | `100` | `20` |
| Testing | `34` | `100` | `10` |
| Production Deployments | `100` | `100` | `10` |
| Production Outcomes | `10` | `100` | `15` |
| Certification | `22` | `100` | `15` |
| Authority Evolution | `15` | `100` | `10` |
| Production Autonomy | `0` | `100` | `10` |
| Implementation Backlog Completion | `5.9` | `100` | `10` |

Production Maturity:

```text
Current: 24.0%
Target: 100%
Remaining: 76.0%
```

Backlog:

```text
Tier A: 2 / 6 complete
Tier B: 0 / 21 complete
Tier C: 0 / 7 complete
Tier D: 0 / 6 optional complete
Overall: 3 / 34 actionable complete
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
5.9%

Certification
22%

Autonomy
0%

Production Maturity
24.0%

Overall Status
ENGINEERING_COMPLETE / PRODUCTION_IN_PROGRESS

Current Focus
IMPLEMENTATION

Backlog
Tier A
2 / 6
Tier B
0 / 21
Tier C
0 / 7
Tier D
0 / 6 optional
Overall
3 / 34 complete

Current Tier
TIER_1_GOVERNED

Highest Priority Task
A3 fix: preserve approved locked selected moves through the existing autoswitch intelligence snapshot gate.

Status
Unsafe Implementation

Authority
None

Required Action
Implement A3_FIX_APPROVED_PLAN_LOCK_SNAPSHOT_GATE_CONSUMPTION_IN_EXISTING_AUTOSWITCH_OWNER.

Engineering
BLOCKED_BY_OWNER_DEFECT

Runtime
FAIL_CLOSED_BEFORE_MOVEMENT

Packet
APPROVED_AND_CONSUMED

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

## 2.12.3. Capability Management

OMP is capability-oriented.

Tasks are the execution unit.

Capabilities are the maturity unit.

OMP must always know:

1. what capability is currently being built;
2. how complete it is;
3. what blocks completion;
4. which backlog items belong to it;
5. when it becomes `COMPLETE`;
6. when it becomes `LOCKED`;
7. when future work is forbidden unless a re-open trigger is present.

No capability may remain permanently `IN_PROGRESS`.

Every capability record must contain:

- Capability Name;
- Purpose;
- Ideal Target State;
- Current State;
- Current %;
- Target %;
- Definition of Done;
- Completed Criteria;
- Remaining Criteria;
- Blocking Backlog Items;
- Expected Completion Point;
- Canonical Owner;
- Production Value;
- Autonomy Impact;
- Current Status;
- Re-open Triggers.

Capability status values:

| Status | Meaning |
| --- | --- |
| `IN_PROGRESS` | The capability has unfinished Definition of Done criteria or unfinished required backlog items. |
| `COMPLETE` | Every Definition of Done criterion has completion evidence. |
| `LOCKED` | The capability is complete, canonical, and future engineering is prohibited unless a re-open trigger is present. |

General capability rules:

1. Every backlog item must belong to at least one capability.
2. OMP must maintain `Capability -> Backlog Items -> Current % -> Remaining % -> Expected Completion`.
3. OMP must calculate capability progress from Definition of Done criteria and existing backlog status.
4. OMP must not invent work to fill a capability.
5. OMP must use only the existing backlog, existing policies, existing Runtime, and existing canonical knowledge.
6. After every completed backlog item, OMP must update capability progress in Current Program State.
7. If a Definition of Done becomes satisfied, OMP must mark the capability `COMPLETE`, then `LOCKED`, then update Canonical Reference.
8. Locked capabilities may be reopened only if production evidence disproves the capability, architecture materially changes, or the operator explicitly requests reopening.
9. Capability Progress Reports are historical engineering reports only; they must never become a second backlog or roadmap.
10. Every capability must define how Runtime, OMP, operators, or knowledge owners behave when the capability reaches `100%`.

Capability Dashboard must be printed in OMP Status:

```text
Capability Dashboard

Capability | Current % | Ideal % | Remaining % | Current Maturity | Production Impact | Autonomy Impact | Blocking Backlog Items | Completion Prediction
Movement Protection | 35.7% | 100% | 64.3% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A3, A5, A6, B3, B4, B5, B8, B10, B16, B19, B21, C7 | Complete after movement stability, rollback, recovery, blast, anti-flap, routing mode, slow-start, and pool-health criteria are satisfied.
Runtime Eligibility | 28.6% | 100% | 71.4% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A6, B17, B18, C1, C6 | Complete after Runtime can decide execute-or-stop from certified gates.
Authority Evolution | 40.0% | 100% | 60.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A3, A4, A5, A6, B11, B12, B13, B16, B21, C3, C4 | Complete after action classes and delegated policy can replace repeated packet approval.
Rollback | 42.9% | 100% | 57.1% | IN_PROGRESS | VERY_HIGH | HIGH | A3, B15, B16, C5 | Complete after rollback/no-rollback class evidence and authority are certified.
Recovery Admission | 25.0% | 100% | 75.0% | IN_PROGRESS | HIGH | HIGH | B8, B9, B10 | Complete after recovered channels are reintroduced through certified readiness and slow-start.
Learning | 40.0% | 100% | 60.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A3, A4, B5, B13 | Complete after real outcomes reliably improve future decisions.
Production Readiness | 24.0% | 100% | 76.0% | IN_PROGRESS | VERY_HIGH | HIGH | Remaining actionable backlog and certification | Complete at PRODUCTION_AUTONOMY_CERTIFIED.
Production Autonomy | 0.0% | 100% | 100.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A3, A4, A5, A6, B10, B12, B16, C4 | Complete when Runtime operates inside certified policy and operator supervises.
Knowledge System | 100.0% | 100% | 0.0% | LOCKED | HIGH | MEDIUM_HIGH | None | Complete and locked under canonical knowledge rules.
Observability | 30.0% | 100% | 70.0% | IN_PROGRESS | HIGH | MEDIUM_HIGH | B1, B4, B9, B13, B15, B17, C2 | Complete when operators and OMP can inspect all safety/runtime evidence without mutation.
Decision Explainability | 20.0% | 100% | 80.0% | IN_PROGRESS | HIGH | HIGH | A3, A6, B1, B4, B13, B15, B17, C2 | Complete when every approval request explains the decision in Russian before Approve / Reject, using existing evidence owners only.
Implementation Discipline | 100.0% | 100% | 0.0% | COMPLETE | VERY_HIGH | MEDIUM | None | Complete while Backlog remains the only live queue.
Engineering Knowledge Preservation | 100.0% | 100% | 0.0% | LOCKED | HIGH | MEDIUM | None | Complete and locked while reference/report/ADR roles remain normalized.

Current Capability
Movement Protection

Current Backlog Item
A3

Completion Prediction
Movement Protection completes after rollback/no-rollback certification, soft degradation certification, recovery admission certification, blast-radius certification, anti-flap certification, central policy arbitration, AUTO/PINNED/MANUAL routing mode, runtime-certified slow start, and pool-health semantics are complete.

Blocking Items
A3, A5, A6, B3, B4, B5, B8, B10, B16, B19, B21, C7
```

Initial capability registry:

| Capability | Purpose | Current % | Target % | Current Status | Canonical Owner | Production Value | Autonomy Impact | Blocking Backlog Items | Expected Completion Point | Re-open Triggers |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| Movement Protection | Prevent chaotic user movement while preserving fast reaction to real failures. | `35.7` | `100` | `IN_PROGRESS` | OMP, Movement Protection Model, Runtime Model, Canonical Policy Library | `VERY_HIGH` | `VERY_HIGH` | `A3`, `A5`, `A6`, `B3`, `B4`, `B5`, `B8`, `B10`, `B16`, `B19`, `B21`, `C7` | All Movement Protection DoD criteria complete or explicitly `NOT_APPLICABLE`. | Production evidence disproves behavior; planner/runtime architecture materially changes; explicit operator request. |
| Runtime Eligibility | Decide whether Runtime may execute or must stop using certified gates. | `28.6` | `100` | `IN_PROGRESS` | Runtime Model, OMP, delegated policy preview, action-class enablement owners | `VERY_HIGH` | `VERY_HIGH` | `A2`, `A6`, `B17`, `B18`, `C1`, `C6` | Action-class runtime eligibility arbitration is implemented and freshness/reporting semantics are certified. | Runtime architecture changes; production eligibility failure; explicit operator request. |
| Authority Evolution | Move from packet approval to bounded class/policy authority without silent expansion. | `40.0` | `100` | `IN_PROGRESS` | OMP, Authority policy, Runtime Model, action-class ladder | `VERY_HIGH` | `VERY_HIGH` | `A3`, `A4`, `A5`, `A6`, `B11`, `B12`, `B13`, `B16`, `B21`, `C3`, `C4` | Certified class evidence supports authority recommendation and operator/certified policy approval. | Authority incident; operator policy change; explicit authority expansion/shrink request. |
| Rollback | Guarantee safe compensation or certified no-rollback behavior for production actions. | `42.9` | `100` | `IN_PROGRESS` | Restore barrier, rollback manifest, Runtime Model, execution feedback | `VERY_HIGH` | `HIGH` | `A3`, `B15`, `B16`, `C5` | Rollback/no-rollback class evidence and automatic rollback authority are certified. | Failed rollback; verification failure pattern; explicit operator request. |
| Recovery Admission | Admit recovered channels safely without oscillation or premature scale. | `25.0` | `100` | `IN_PROGRESS` | Recovery admission owner, service matrix, quality compact, blast-radius/action-class ladder | `HIGH` | `HIGH` | `B8`, `B9`, `B10`, `D2`, `D3` | Repeated real readiness evidence, observation windows, and runtime-certified slow start are complete. | Recovery incident; service evidence changes; explicit operator request. |
| Learning | Convert real outcomes into future decision quality without synthetic evidence. | `40.0` | `100` | `IN_PROGRESS` | Feedback/learning owner, OMP, Canonical Reference | `VERY_HIGH` | `VERY_HIGH` | `A3`, `A4`, `B5`, `B13` | Representative real outcomes and metric reliability support promotion recommendations. | Learning regression; synthetic evidence risk; explicit operator request. |
| Production Readiness | Make V7 deployable, operable, verifiable, and certifiable as a production system. | `24.0` | `100` | `IN_PROGRESS` | OMP, Production Maturity Model, Implementation Backlog | `VERY_HIGH` | `HIGH` | `A1`-`A6`, `B11`, `B14`, `B21`, `C7`, optional `D1`-`D6` only if scope changes | Production Maturity reaches `100%` and outputs `PRODUCTION_AUTONOMY_CERTIFIED`. | Production safety incident; deploy model change; explicit operator request. |
| Production Autonomy | Enable Runtime to operate inside certified authority while operator supervises. | `0.0` | `100` | `IN_PROGRESS` | OMP, Runtime Model, Authority Evolution, action-class promotion | `VERY_HIGH` | `VERY_HIGH` | `A3`, `A4`, `A5`, `A6`, `B10`, `B12`, `B16`, `C4` | Bounded autonomy and then production autonomy are certified by real outcomes and approved authority. | Autonomy incident; authority policy change; explicit operator request. |
| Knowledge System | Preserve verified project knowledge and prevent repeated rediscovery. | `100.0` | `100` | `LOCKED` | Canonical Reference, Context Resolver, Research Framework, Policy Library, Document Lifecycle | `HIGH` | `MEDIUM_HIGH` | None current. | Current knowledge owners remain canonical and read-only under document lifecycle rules. | Industry consensus changes; `FUNDAMENTAL_ARCHITECTURE_GAP`; explicit operator request. |
| Observability | Expose enough read-only truth for operators, OMP, Runtime, and certification. | `30.0` | `100` | `IN_PROGRESS` | Admin read models, trust/evidence inventory, truth/convergence | `HIGH` | `MEDIUM_HIGH` | `B1`, `B4`, `B9`, `B13`, `B15`, `B17`, `C2` | Read-only evidence shows eligibility, rollback, stale reads, promotion quality, and runtime readiness. | Operator cannot diagnose; evidence disagreement; explicit operator request. |
| Decision Explainability | Explain existing Runtime / OMP decisions to the operator before any approval request. | `20.0` | `100` | `IN_PROGRESS` | OMP, Current Program State, Runtime Model, evidence read models | `HIGH` | `HIGH` | `A3`, `A6`, `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Every approval request explains reason, evidence, expected value, risks, alternatives, and capability impact in Russian before Approve / Reject. | Operator cannot understand approval reason; explanation contradicts evidence; explicit operator request. |
| Implementation Discipline | Ensure work flows only through Backlog, Priority Model, tests, truth, convergence, deployment, and certification. | `100.0` | `100` | `COMPLETE` | OMP, Implementation Backlog, Implementation Priority Model, Current Program State | `VERY_HIGH` | `MEDIUM` | None current. | OMP + Backlog + Current Program State remain sufficient for execution. | Backlog loses single-queue authority; operator requests process change. |
| Engineering Knowledge Preservation | Freeze certified reference knowledge and keep reports/ADRs from becoming roadmaps. | `100.0` | `100` | `LOCKED` | Document Lifecycle, Canonical Reference, SYSTEM_MAP | `HIGH` | `MEDIUM` | None current. | Reference, report, ADR, policy, and backlog roles remain normalized. | Reference contradiction; material architecture change; explicit operator request. |

Ideal Target State by capability:

| Capability | Ideal Target State |
| --- | --- |
| Movement Protection | Runtime evaluates current state, candidate quality, failure/degradation, freshness, recovery, blast radius, rollback, anti-flap, authority, State Change Cost, and Net Benefit before any movement; it moves only when `NET_BENEFIT > CHANGE_COST`, otherwise it keeps the current state. |
| Runtime Eligibility | Runtime consumes prepared certified decisions and fresh evidence, then returns `EXECUTE` or `STOP_SAFE`; it never invents decisions, bypasses policy, or mutates from stale/unknown evidence. |
| Authority Evolution | Operators approve policy, class, or authority boundaries; Runtime self-approves only operational decisions inside approved bounds; authority expansion never happens silently. |
| Rollback | Every production action has rollback ready or certified no-rollback semantics before execution; verification failure leads to rollback or explicit safe stop through existing owners. |
| Recovery Admission | Recovered channels re-enter through repeated readiness evidence, observation windows, bounded blast radius, and runtime-certified slow start instead of immediate full trust. |
| Learning | Only real observed outcomes update knowledge, confidence, suitability, promotion readiness, and future decisions; synthetic evidence is never accepted. |
| Production Readiness | V7 is deployable, testable, observable, certifiable, and operationally safe; OMP can move from implementation through certification and authority evolution to production autonomy. |
| Production Autonomy | Runtime executes certified action classes inside delegated policy; the operator supervises, approves expansion, and handles exceptional cases. |
| Knowledge System | Canonical Reference, SYSTEM_MAP, Context Resolver, Research Framework, Policy Library, and Document Lifecycle preserve verified knowledge and prevent rediscovery or duplicate owners. |
| Observability | Operators, OMP, and Runtime can inspect liveness, degradation, recovery, rollback, stale reads, eligibility, promotion readiness, and evidence quality without mutation. |
| Decision Explainability | Operators receive a Russian, evidence-linked explanation of every approval request before Approve / Reject; the explanation covers reason, timing, user, source, target, passed gates, alternatives, risks, confidence, production value, and capability progress. |
| Implementation Discipline | OMP always selects the highest unfinished backlog item, uses existing owners, verifies with tests/truth/convergence, marks completion, recalculates capability progress, and continues or stops only at allowed boundaries. |
| Engineering Knowledge Preservation | Durable knowledge is promoted from reports into canonical owners; reports remain evidence, ADRs remain decisions, references remain knowledge, and Backlog remains the only engineering queue. |

Definition of Done by capability:

| Capability | Definition of Done | Completed Criteria | Remaining Criteria |
| --- | --- | --- | --- |
| Movement Protection | Hard Failure certified; Soft Degradation certified; Recovery Admission certified; Freshness integrated; Rollback certified; Blast Radius certified; Anti-Flap certified; Stickiness implemented; Minimum Improvement Threshold implemented; State Change Cost Model implemented; Central Policy Arbitration implemented; `AUTO` / `PINNED` / `MANUAL` routing implemented; Runtime-certified Slow Start implemented; Pool Health semantics completed or explicitly `NOT_APPLICABLE`. | Hard Failure classification; Freshness integration; Stickiness; Minimum Improvement Threshold; State Change Cost Model. | Soft Degradation certification; Recovery Admission certification; Rollback certification; Blast Radius certification; Anti-Flap certification; Central Policy Arbitration; `AUTO` / `PINNED` / `MANUAL`; Runtime-certified Slow Start; Pool Health semantics. |
| Runtime Eligibility | Freshness windows exist; owner-issued freshness exists; authority, blast, rollback, anti-flap, verification, and learning gates are arbitrated; stale read reporting is preserved; bounded stale allowance is decided by action class. | Runtime Model; A2 freshness windows. | A6 arbitration; B17 stale-read reporting; B18 owner lease extension; C1 fail-open/fail-closed; C6 bounded stale allowance. |
| Authority Evolution | Operational and engineering authority are separated; packet approval is retired class-by-class; class approval and delegated policy approval require certified evidence; authority never expands silently. | Authority normalization; action-class ladder; packet approval classified as temporary governed fallback. | A3-A5 evidence; A6 eligibility; B11 isolation; B12 staged promotion; B13 metric reliability; B16 rollback authority; B21 user mode; C3/C4 authority constraints. |
| Rollback | Restore barrier works; rollback manifest exists; exact selected move identity is preserved; rollback/no-rollback evidence is certified; automatic rollback authority is certified only after reliable verification. | Restore barrier; rollback manifest; exact packet/lease identity path. | A3 class evidence; B15 containment/forward-fix classification; B16 automatic rollback authority; C5 compensation semantics. |
| Recovery Admission | Recovered channels require repeated real success/readiness evidence; post-admission observation exists; slow-start recovery is runtime-certified. | Recovery admission read model; limited recovery blast radius. | B8 certification; B9 observation windows; B10 slow-start progression. |
| Learning | Only real observed outcomes feed learning; outcome closure exists; representative evidence exists; metric reliability supports promotion recommendations. | Real-only learning rule; feedback owner; outcome closure path. | A3/A4 real outcomes; B5 attribution; B13 metric reliability. |
| Production Readiness | Implementation, deploy, tests, truth, convergence, certification, outcomes, authority, and autonomy reach Production Maturity `100%`. | Engineering Maturity `100%`; safe deployment owner; truth/convergence; A1/A2 complete. | Remaining actionable backlog; production outcomes; certification; authority evolution; autonomy certification. |
| Production Autonomy | Runtime acts automatically only inside approved policy and certified action classes; operator supervises; production autonomy is certified. | Product and Runtime models define target; runtime automation remains disabled. | Class evidence; runtime eligibility; authority approval; rollback certification; bounded autonomy; production autonomy certification. |
| Knowledge System | Context Resolver, Research Framework, Canonical Policy Library, Canonical Reference, SYSTEM_MAP, and Document Lifecycle preserve verified knowledge without creating duplicate owners. | All listed knowledge owners exist and are canonical. | None current. |
| Observability | Operators and OMP can inspect liveness, degradation, recovery, rollback, stale reads, runtime eligibility, promotion readiness, and evidence quality without mutation. | Truth/convergence; admin read models; evidence inventory; service matrix. | B1/B4/B9/B13/B15/B17/C2 observability/read-model items. |
| Decision Explainability | Every approval request explains the decision in Russian before Approve / Reject; explanations are generated from existing evidence owners; safety gates show passed/failed/unknown/not applicable; alternatives and keep-current-state reasoning are visible; expected Production Value, Capability Progress, and remaining risk are shown; missing evidence stops safely instead of producing persuasive text. | OMP owns the capability; Russian-only operator explanation requirements; Russian-only Engineering Report requirements. | A3/A6/B1/B4/B13/B15/B17/C2 must provide enough evidence/read-model coverage for complete operator-facing explanations and real governed validation. |
| Implementation Discipline | OMP always selects highest unfinished backlog item, updates Current Program State, runs tests/truth/convergence, marks DONE, recalculates, and continues or stops only at allowed stop conditions. | Backlog; Priority Model; Root Cause Engine; normalized authority; document lifecycle; capability framework. | None current. |
| Engineering Knowledge Preservation | Certified reference knowledge is frozen; reports and ADRs remain evidence; only Backlog drives implementation. | Canonical Reference; Document Lifecycle; SYSTEM_MAP ownership; no-reaudit triggers. | None current. |

## 2.12.3.1. Master Integration Program

Status: `MASTER_INTEGRATION_PROGRAM_COMPLETE`

Purpose:

Turn existing completed V7 capabilities into one coherent production operating system through existing owners only.

This program does not create a new owner, new roadmap, new architecture, new planner, new governance, new execution path, new Runtime owner, new truth source, new policy, or duplicate backlog.

Source facts:

- `SYSTEM_INVENTORY_COMPLETE`;
- `SYSTEM_INTEGRATION_ANALYSIS_COMPLETE`;
- `docs/reference/SYSTEM_MAP.md` -> `Master Integration Atlas`;
- `docs/reference/V7_CANONICAL_REFERENCE.md` -> `MASTER_SYSTEM_INTEGRATION_AUDIT_PART_1` and `MASTER_SYSTEM_INTEGRATION_AUDIT_PART_2`.

Execution rule:

OMP must execute integration by selecting the highest unfinished existing backlog item that closes the next required integration in the Master Integration Atlas.

Every integration task must map to:

```text
Existing owner
  -> Existing capability
  -> Existing backlog item
  -> Integration action
  -> Expected production result
```

Need New Backlog Item:

`FALSE`

Reason:

All discovered integration work maps to existing backlog items. No mathematically unavoidable new backlog item was found.

Execution groups:

| Group | Purpose | Existing owner | Related backlog | Expected result |
| --- | --- | --- | --- | --- |
| Product Layer Integration | Make Business Objectives the primary operating language before technical artifacts. | Product Specification, Decision Explainability, Observability | `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Product Owner and operator see business reason, evidence, risk, value, and result first. |
| Policy Integration | Convert canonical policy rules into runtime-readable gate decisions. | Canonical Policy Library, OMP, Runtime Model | `A6`, `B19`, `B20`, `C1`, `C6` | Policies become executable eligibility inputs without new policy owners. |
| Capability Integration | Keep capability maturity, backlog, Current Program State, and OMP status synchronized. | OMP, Current Program State, Implementation Backlog | Existing mapped backlog | Capability progress updates after every real implementation/certification outcome. |
| Runtime Integration | Connect Runtime Model semantics to existing read models and guarded execution owners. | Runtime Model, action-class enablement, delegated policy preview | `A6`, `B17`, `B18`, `C1`, `C6` | Runtime can produce one `EXECUTE` or `STOP_SAFE` result from certified gates. |
| Runtime Explainability | Explain decisions in Russian before approval using existing evidence. | OMP, Decision Explainability, read models | `A3`, `A6`, `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Operator approves decisions, not opaque packets. |
| Operator Experience | Keep engineering details secondary, read-only, and expandable. | Product Specification, UI/read-model owners, OMP | `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Operator interface uses business language first. |
| Certification | Close rollback/no-rollback, blast-radius, recovery, anti-flap, and authority evidence. | OMP, Backlog, policy owners | `A3`, `A4`, `A5`, `B8`, `B10`, `B12`, `B13`, `B16` | Action classes become eligible for authority promotion. |
| Production Evidence | Feed only real observed outcomes into learning and promotion. | Feedback/learning owners, OMP | `A3`, `A4`, `B5`, `B13` | Promotion decisions are based on real outcomes, not synthetic evidence. |
| Autonomy Readiness | Move from governed packet fallback to class/policy authority. | OMP, Runtime Model, Authority Evolution | `A3`, `A4`, `A5`, `A6`, `B10`, `B12`, `B16`, `C4` | Runtime can eventually operate certified routine actions inside approved policy. |

Execution order:

| Order | Existing owner | Existing backlog | Integration work | Expected capability | Expected production impact | Expected maturity increase |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Restore barrier, rollback manifest, governed execution, feedback/learning | `A3` | Certify class-level rollback/no-rollback evidence for governed candidate movement. | Rollback; Learning; Authority Evolution; Movement Protection | First real class evidence toward retiring packet approval. | High Production Maturity and Authority Evolution gain. |
| 2 | OMP promotion engine, feedback/learning, outcome leverage model | `A4` | Materialize representative outcome evidence for the first action class. | Learning; Authority Evolution; Production Readiness | Gives promotion decisions enough real evidence. | High autonomy and production evidence gain. |
| 3 | Action-class ladder, planner budgets, capacity/load gates | `A5` | Certify class-level blast-radius evidence beyond one-user guard. | Movement Protection; Authority Evolution; Runtime Eligibility | Allows safe scope reasoning for next authority step. | High safety and authority gain. |
| 4 | OMP, delegated policy preview, action-class runtime enablement, Runtime Model | `A6` | Implement action-class runtime eligibility arbitration using certified gates. | Runtime Eligibility; Production Autonomy | Converts separated gates into one execute-or-stop decision. | Very high runtime/autonomy gain. |
| 5 | Service matrix, quality compact, trust/outcome stores | `B5` | Complete observed degradation attribution using active and passive evidence. | Learning; Movement Protection; Observability | Improves quality of soft-degradation decisions. | Medium-high production gain. |
| 6 | Recovery admission, service/route/readiness models | `B8` | Certify recovery admission with repeated real success/readiness evidence. | Recovery Admission; Movement Protection | Prevents premature recovery movement. | High stability gain. |
| 7 | Blast-radius/action-class ladder | `B10` | Define runtime-certified recovery slow-start as V7 progression. | Recovery Admission; Production Autonomy | Enables bounded recovery re-entry. | High autonomy and stability gain. |
| 8 | Action-class ladder, OMP | `B12` | Implement next action-class stage only after certification evidence exists. | Authority Evolution; Production Autonomy | Advances class authority without silent expansion. | High autonomy gain. |
| 9 | Trust/confidence, freshness, rollback, eligibility | `B13` | Certify metric reliability for automated promotion recommendations. | Learning; Observability; Authority Evolution | Prevents bad promotion from weak metrics. | High safety gain. |
| 10 | Runtime Model, execution packet partial-failure policy | `B15` | Expose containment/forward-fix classification. | Rollback; Observability; Decision Explainability | Makes rollback alternatives visible and explainable. | Medium-high safety gain. |
| 11 | Autoswitch rollback-on-verify-fail, OMP authority gates | `B16` | Certify automatic rollback authority after reliable verification evidence. | Rollback; Production Autonomy; Authority Evolution | Enables safe rollback inside policy. | Very high runtime safety gain. |
| 12 | Runtime eligibility, truth/convergence, read-only inventory | `B17` | Preserve stale-read reporting while blocking mutation. | Runtime Eligibility; Observability; Decision Explainability | Improves operator trust without unsafe action. | Medium production gain. |
| 13 | Execution lease, runtime snapshot, intelligence snapshots | `B18` | Extend owner-issued version/lease pattern where available. | Runtime Eligibility; Freshness | Strengthens safe present-tense execution. | High safety gain. |
| 14 | Service signal thresholds, recovery admission, movement protection | `B19` | Centralize hysteresis and state-change-cost vocabulary. | Movement Protection; Runtime Eligibility | Prevents oscillation and noisy movement. | High stability gain. |
| 15 | OMP, planner, runtime eligibility | `B20` | Encode hard-failure override rule for anti-flap arbitration. | Movement Protection; Runtime Eligibility | Allows fast failure reaction without false oscillation. | High safety and recovery gain. |
| 16 | User registry, policy, planner, admin surface | `B21` | Implement explicit per-user `AUTO` / `PINNED` / `MANUAL` routing mode. | Movement Protection; Authority Evolution; Production Readiness | Makes user movement intent explicit. | Medium-high operational safety gain. |
| 17 | Runtime Model, OMP, planner gates | `C1` | Record fail-open/fail-closed behavior per action class. | Runtime Eligibility | Makes stop/continue semantics explicit. | Medium safety gain. |
| 18 | Trust/confidence model, shadow autonomy | `C2` | Use probabilistic suspicion only as advisory evidence. | Decision Explainability; Observability | Prevents weak signals from becoming unsafe actions. | Medium safety gain. |
| 19 | OMP, operator authority | `C3` | Define break-glass authority as audited exceptional operator policy. | Authority Evolution | Keeps emergency paths bounded and explicit. | Medium authority safety gain. |
| 20 | OMP, blast-radius gates | `C4` | Keep all-at-once promotion unavailable for current action classes. | Production Autonomy; Authority Evolution | Prevents unsafe expansion. | Medium safety gain. |
| 21 | Runtime Model, rollback policy | `C5` | Preserve rollback as operational compensation rather than transaction rollback. | Rollback | Clarifies safe recovery semantics. | Medium safety gain. |
| 22 | Freshness actionability, OMP stop rules | `C6` | Decide bounded stale allowance by action class. | Runtime Eligibility; Freshness | Avoids unsafe stale mutation while preserving useful reads. | Medium-high runtime gain. |
| 23 | Planner capacity/load, action-class ladder | `C7` | Map pool max-ejection/minimum-health semantics to V7 capacity and blast bounds. | Movement Protection; Production Readiness | Prevents over-evacuation and pool instability. | Medium-high stability gain. |

Dependency rule:

1. `A3` must precede `A4`, `A5`, `A6`, `B12`, and `B16`.
2. `A4` and `B13` must precede authority expansion recommendations.
3. `A6` must precede runtime autonomy readiness.
4. `B8` must precede `B10`.
5. `B16` must not be enabled before rollback/no-rollback evidence and verification reliability exist.
6. `C3` and `C4` are authority guardrails, not runtime enablement.

Parallel work:

The only safe parallel work is read-only observability/explainability work that does not mutate runtime, authority, policy, users, restore barrier, or evidence:

- `B1`, `B4`, `B15`, `B17`, `C2`;
- documentation-only clarifications `C1`, `C4`, `C5` when they do not change runtime behavior.

Runtime validation:

Runtime may consume only:

- Canonical Policies;
- Certified Action Classes;
- Delegated Autonomy Policy;
- Runtime Eligibility;
- Authority;
- Freshness;
- Rollback;
- Verification;
- Learning.

Runtime must never consume raw Product Owner text, raw Business Objectives, subjective operator wishes, packet approval as durable policy, or unverified report-only knowledge.

Product Owner experience target:

Product Owner interacts only with:

- Business Objectives;
- Business Status;
- Business Risk;
- Business Profile;
- Business Results;
- Business Exceptions.

Product Owner must never be required to understand packets, planner, lease, rollback internals, blast-radius internals, routing algorithms, runtime internals, or protocol engineering.

Operator experience target:

Operator UI must use business language first. Engineering details are secondary, read-only, expandable, and never the primary operating language.

OMP normalization:

After this program, normal operation must require only:

- `Status`;
- `Continue OMP`;
- `Approve authority expansion`;
- `Production Action`.

OMP must not request a new roadmap, new integration plan, or new semantic audit for already mapped work.

Master verification:

| Verification item | Result |
| --- | --- |
| Duplicate owners | `NONE_FOUND` |
| Duplicate permanent documents | `NONE_CREATED` |
| Duplicate policies | `NONE_FOUND` |
| Duplicate capabilities | `NONE_FOUND` |
| Duplicate truth sources | `NONE_FOUND` |
| Orphan knowledge | `NONE_FOUND` |
| Orphan capability | `NONE_FOUND` |
| Orphan backlog | `NONE_FOUND` |
| Disconnected integration | `NONE_UNMAPPED`; remaining gaps map to existing backlog/capabilities |

## 2.12.4. Movement Protection Target State

Purpose:

Define the final runtime behavior for Movement Protection after all required backlog items are complete.

This is the Definition of Done.

This is not an implementation plan.

This section does not create a new planner, Runtime owner, governance owner, execution owner, truth source, or document owner.

Movement Protection target state:

Users must not experience chaotic oscillation while V7 still reacts quickly to real production failures.

Runtime must prefer stability unless changing state has proven production value greater than transition cost.

Final Runtime decision pipeline:

```text
User
  -> Current Channel
  -> Candidate Discovery
  -> Hard Failure
  -> Soft Degradation
  -> Freshness
  -> Recovery Admission
  -> Blast Radius
  -> Rollback Readiness
  -> Anti-Flap
  -> Authority
  -> State Change Cost Evaluation
  -> Net Benefit Evaluation
  -> Worth Changing State?
  -> YES
  -> Execution
  -> Verification
  -> Outcome
  -> Learning
  -> Planner Improvement
```

Runtime pipeline stage contract:

| Stage | Purpose | Owner | Required evidence | Possible outputs | Interaction with previous stage | Interaction with next stage |
| --- | --- | --- | --- | --- | --- | --- |
| User | Identify the exact subject whose state may change. | User registry, planner/autoswitch owner, admin read models. | User identity, current assignment, org/group policy, manual/pinned state when implemented. | `USER_ELIGIBLE`, `USER_INELIGIBLE`, `USER_PINNED`, `USER_MANUAL_REVIEW`. | Starts the pipeline from a concrete production subject. | Passes subject constraints to Current Channel. |
| Current Channel | Preserve known current state before considering movement. | `tools/v7-users-autoswitch`, registry readers, Movement Protection Model. | Current egress/channel, recent movement history, sticky score, current-channel health. | `CURRENT_STABLE`, `CURRENT_SUSPECT`, `CURRENT_FAILED`, `CURRENT_UNKNOWN`. | Receives user constraints. | Defines baseline for Candidate Discovery and future net benefit comparison. |
| Candidate Discovery | Find valid target candidates without deciding to move yet. | Planner/autoswitch, service matrix, quality compact, route reality. | Candidate channels, service suitability, capacity/load, fallback availability, route reality. | `CANDIDATES_AVAILABLE`, `NO_SAFE_CANDIDATE`, `CANDIDATE_SET_UNKNOWN`. | Uses current channel as baseline. | Passes candidate set to failure/degradation gates. |
| Hard Failure | Detect complete failure requiring fast reaction. | `POLICY_001_HARD_FAILURE`, liveness/event evidence, service matrix, planner/autoswitch. | Liveness failure, explicit down/unavailable evidence, repeated failed checks, route/service hard-fail classification. | `HARD_FAILURE`, `NO_HARD_FAILURE`, `INSUFFICIENT_LIVENESS_EVIDENCE`. | Evaluates current and candidates discovered upstream. | If hard failure exists, Soft Degradation must not weaken the need to protect availability. |
| Soft Degradation | Detect meaningful degradation without treating noise as failure. | `POLICY_002_SOFT_DEGRADATION`, quality compact, service matrix, planner/autoswitch. | Active/passive degradation evidence, trend thresholds, service objective mapping, attribution evidence. | `SOFT_DEGRADATION`, `NO_DEGRADATION`, `NOISY_OR_ATTRIBUTION_UNKNOWN`. | Refines Hard Failure result; does not override proven hard failure. | Passes degradation severity to Freshness. |
| Freshness | Prove evidence is current enough for the action risk. | `POLICY_008_FRESHNESS`, Runtime Model, delegated policy preview, execution lease. | Owner-issued freshness fields, age, TTL/window, snapshot generation, lease/version where available. | `FRESH`, `STALE_READ_ONLY`, `UNKNOWN_FRESHNESS`, `STOP`. | Validates evidence from failure/degradation stages. | Only fresh or explicitly allowed evidence may continue to Recovery Admission. |
| Recovery Admission | Prevent premature use of recovered channels. | `POLICY_003_RECOVERY_ADMISSION`, recovery admission owner, service matrix, quality compact. | Repeated successful checks, readiness state, recovery cooldown, observation window, limited recovery blast radius. | `RECOVERY_ADMITTED`, `RECOVERY_HOLD`, `RECOVERY_UNKNOWN`, `RECOVERY_NOT_RELEVANT`. | Uses fresh evidence and candidate set. | Passes admitted candidate constraints to Blast Radius. |
| Blast Radius | Bound the size and scope of possible change. | `POLICY_006_BLAST_RADIUS`, action-class ladder, planner budgets, OMP. | Selected move count, action class, authority budget, capacity/load, org/cohort/service scope. | `WITHIN_BLAST_RADIUS`, `BLAST_RADIUS_EXCEEDED`, `SCOPE_REQUIRES_AUTHORITY`. | Uses candidate and recovery eligibility. | Defines maximum allowed movement before rollback and anti-flap checks. |
| Rollback Readiness | Confirm the system can compensate or has certified no-rollback semantics. | `POLICY_007_ROLLBACK`, restore barrier, rollback manifest, execution feedback. | Rollback target, restore barrier readiness, rollback manifest, selected-move identity, no-rollback certification where applicable. | `ROLLBACK_READY`, `NO_ROLLBACK_CERTIFIED`, `ROLLBACK_NOT_READY`, `STOP`. | Uses bounded action scope. | Only rollback-ready or certified no-rollback actions may proceed to Anti-Flap. |
| Anti-Flap | Block repeated oscillation and unsafe rapid reversals. | `POLICY_009_ANTI_FLAP`, movement protection owner, anti-flap read model. | Cooldown, freeze, pair reversal, target block, oscillation history, anti-flap window. | `ANTI_FLAP_PASS`, `COOLDOWN_ACTIVE`, `FREEZE_ACTIVE`, `REVERSAL_BLOCKED`, `TARGET_BLOCKED`. | Uses rollback-safe action candidate. | Passes stable candidate to Authority. |
| Authority | Verify the action is allowed without expanding authority silently. | `POLICY_004_AUTHORITY`, OMP, Runtime Model, action-class authority. | Operational/engineering authority class, action-class state, delegated policy, operator approval when required. | `AUTHORITY_PASS`, `OPERATIONAL_AUTHORITY_REQUIRED`, `ENGINEERING_AUTHORITY_REQUIRED`, `AUTHORITY_DENIED`. | Uses anti-flap-safe candidate and blast-radius scope. | Only authorized candidates may reach State Change Cost Evaluation. |
| State Change Cost Evaluation | Calculate the cost of changing from current state to target state. | Movement Protection Model, planner/autoswitch, OMP, Runtime eligibility owners. | Stickiness, threshold, recent movement penalty, cooldown, freeze, reversal risk, rollback risk, verification uncertainty, expected user impact, confidence floors. | `CHANGE_COST`, `KEEP_CURRENT_STATE`, `COST_UNKNOWN_STOP`. | Uses authority-cleared candidate and current-state baseline. | Supplies cost to Net Benefit Evaluation. |
| Net Benefit Evaluation | Compare expected benefit against transition cost. | Planner/autoswitch, Decision Model, Runtime Model, Movement Protection Model. | Candidate score delta, service benefit, failure severity, confidence, suitability, prediction confidence, user impact, rollback risk. | `NET_BENEFIT`, `NET_BENEFIT_NOT_PROVEN`, `KEEP_CURRENT_STATE`. | Consumes explicit change cost. | Only proven benefit can reach Worth Changing State. |
| Worth Changing State? | Make the final movement/no-movement decision. | Runtime Model executing Decision Model output through existing owners. | `NET_BENEFIT`, `CHANGE_COST`, authority, freshness, rollback, anti-flap, blast-radius results. | `EXECUTE`, `KEEP_CURRENT_STATE`, `STOP_SAFE`. | Compares net benefit to change cost. | If `EXECUTE`, passes exact bounded action to Execution. |
| Execution | Perform only the approved/certified movement through existing owners. | Existing execution/autoswitch owners. | Exact selected move, packet/lease identity when governed, rollback readiness, authority clearance. | `EXECUTED`, `NOOP_EXPLICIT_SAFE_STOP`, `EXECUTION_FAILED`. | Receives final execute decision. | Immediately triggers Verification. |
| Verification | Prove the action worked or failed. | Verification owner, service matrix, user/service checks, truth/convergence. | Post-action service/user/channel evidence, verification result, runtime truth. | `VERIFY_PASS`, `VERIFY_FAILED`, `ROLLBACK_REQUIRED`. | Observes execution outcome. | Feeds Outcome and rollback if required. |
| Outcome | Close the action with real observed result only. | Feedback/outcome owner, OMP, Current Program State. | Real verification, movement result, rollback/no-rollback classification, user impact. | `OUTCOME_CLOSED`, `OUTCOME_INCOMPLETE`, `REAL_WORLD_LIMIT`. | Consumes verification evidence. | Feeds Learning. |
| Learning | Convert outcome into future decision quality. | Feedback/learning owner, Canonical Reference where canonical meaning changes, OMP. | Real outcome, verification, rollback result, suitability correctness, trust/confidence deltas. | `LEARNING_UPDATED`, `NO_LEARNING_WITHOUT_REALITY`. | Uses closed outcome only. | Feeds Planner Improvement. |
| Planner Improvement | Improve future recommendations without rewriting architecture. | Planner/autoswitch, OMP, Implementation Backlog, knowledge owners. | Learned outcome, updated confidence/trust/suitability, canonical constraints. | `PLANNER_IMPROVED`, `BACKLOG_ITEM_UPDATED`, `NO_CHANGE`. | Uses learning from real outcomes. | Closes the loop back to Candidate Discovery for future decisions. |

State Change Cost canonical runtime principle:

Changing state has a cost.

Runtime must evaluate not only:

```text
Is another channel better?
```

Runtime must also evaluate:

```text
Is changing state worth the cost?
```

The State Change Cost must include at minimum:

- stickiness;
- minimum improvement threshold;
- recent movement penalty;
- cooldown;
- freeze;
- pair reversal;
- target block;
- rollback risk;
- verification uncertainty;
- expected user impact;
- planner confidence;
- prediction confidence;
- suitability confidence.

Canonical comparison:

```text
NET_BENEFIT = expected production value of the candidate movement.
CHANGE_COST = operational cost and risk of changing state.

Runtime may continue only if:

NET_BENEFIT > CHANGE_COST
```

If `NET_BENEFIT <= CHANGE_COST`, Runtime must output:

```text
KEEP_CURRENT_STATE
```

If `CHANGE_COST` cannot be calculated safely, Runtime must output:

```text
COST_UNKNOWN_STOP
```

Movement Protection completion behavior:

Movement Protection becomes `COMPLETE` only when Runtime satisfies all of the following:

- does not move because of tiny score differences;
- does not oscillate;
- does not undo its own actions repeatedly;
- does not chase temporary noise;
- reacts quickly to real failures;
- keeps users stable whenever stability is better than optimization;
- automatically prefers `stay` unless a move has proven production value;
- every movement has measurable expected benefit greater than transition cost.

World-practice comparison:

| Mature system family | Matching production principle | V7 target-state match | Backlog owner if incomplete |
| --- | --- | --- | --- |
| Cisco | Liveness evidence, protocol/object tracking, hold-down/dampening, bounded failover. | Matches through hard-failure classification, cooldown, movement protection, blast-radius and rollback gates. | `A5`, `B19`, `C7` for remaining centralized/pool semantics. |
| Juniper | BFD/liveness, damping, timers, routing policy, explicit operational controls. | Matches through liveness/freshness gates, cooldown/dampening, authority separation, and state-change cost. | `A6`, `B19` for arbitration and vocabulary consolidation. |
| Cloudflare | Health checks, fallback pools, consecutive success/failure, pool health, traffic safety. | Matches through hard failure, recovery admission, freshness, blast radius, rollback, and pool-health target semantics. | `B8`, `B10`, `C7`. |
| Google SRE | Avoid cascading failure, verify changes, rollback before trust, canary, gradual recovery, learn from outcomes. | Matches through rollback, verification, learning, action-class promotion, and real-outcome-only certification. | `A3`, `A4`, `B13`, `B16`. |
| Kubernetes | Desired/current state separation, readiness, probes, rollout bounds, reconciliation, backoff. | Matches through Runtime executing prepared decisions, freshness/readiness, recovery admission, anti-flap, and stop-safe semantics. | `A6`, `B8`, `B9`, `B10`, `C1`, `C6`. |
| Envoy | Outlier detection, ejection, max ejection percent, min health, active health checking, circuit breaking. | Matches through degradation/anti-flap target state and V7-native capacity/blast bounds; proxy-specific max-ejection/min-health mapping remains partial. | `B3`, `B4`, `B5`, `B6`, `C7`. |

World-practice verdict:

The target state fully matches mature production engineering principles at the model level.

No new owner is required.

No new document is required.

No new backlog item is required.

Remaining real engineering gaps are already represented in the Implementation Backlog:

| Remaining gap | Existing backlog item |
| --- | --- |
| Rollback/no-rollback production certification | `A3`, `B16` |
| Soft Degradation certification and mapping | `B3`, `B4`, `B5`, `B6`, `B7` |
| Recovery Admission certification | `B8`, `B9`, `B10` |
| Blast Radius certification and scope | `A5`, `B14` |
| Anti-Flap certification and arbitration | `B19`, `B20` |
| Central Policy Arbitration | `A6` |
| Per-user `AUTO` / `PINNED` / `MANUAL` routing mode | `B21` |
| Runtime-certified Slow Start Recovery | `B10` |
| Pool Max-Ejection / Minimum-Health semantics | `C7` |

Movement Protection Definition of Done:

Movement Protection is `COMPLETE` only when all are true:

1. all required Movement Protection backlog items are `DONE`;
2. all runtime behaviors listed in this target state are implemented through existing owners;
3. all relevant production certifications pass;
4. real production evidence confirms stable behavior;
5. Production Maturity reflects completion;
6. Canonical Reference records the completed capability;
7. OMP marks Movement Protection `COMPLETE`, then `LOCKED`.

Movement Protection remains `IN_PROGRESS`.

Current estimated Movement Protection completion:

```text
35.7%
```

Backlog-to-capability coverage:

| Backlog item | Capability ownership |
| --- | --- |
| `A1` | Movement Protection; Runtime Eligibility; Knowledge System |
| `A2` | Runtime Eligibility; Movement Protection; Recovery Admission |
| `A3` | Rollback; Movement Protection; Learning; Authority Evolution |
| `A4` | Learning; Authority Evolution; Production Readiness; Production Autonomy |
| `A5` | Movement Protection; Authority Evolution; Runtime Eligibility |
| `A6` | Runtime Eligibility; Authority Evolution; Movement Protection; Production Autonomy |
| `B1` | Observability; Knowledge System; Movement Protection |
| `B2` | Runtime Eligibility; Movement Protection |
| `B3` | Movement Protection; Observability |
| `B4` | Movement Protection; Observability |
| `B5` | Movement Protection; Learning; Observability |
| `B6` | Movement Protection; Runtime Eligibility |
| `B7` | Runtime Eligibility; Movement Protection |
| `B8` | Recovery Admission; Movement Protection |
| `B9` | Recovery Admission; Observability |
| `B10` | Recovery Admission; Movement Protection; Production Autonomy |
| `B11` | Authority Evolution; Runtime Eligibility; Production Readiness |
| `B12` | Authority Evolution; Production Autonomy; Implementation Discipline |
| `B13` | Authority Evolution; Learning; Observability |
| `B14` | Authority Evolution; Movement Protection; Production Readiness |
| `B15` | Rollback; Observability |
| `B16` | Rollback; Authority Evolution; Production Autonomy |
| `B17` | Runtime Eligibility; Observability |
| `B18` | Runtime Eligibility |
| `B19` | Movement Protection; Runtime Eligibility |
| `B20` | Movement Protection; Runtime Eligibility |
| `B21` | Movement Protection; Authority Evolution; Production Readiness |
| `C1` | Runtime Eligibility; Authority Evolution |
| `C2` | Knowledge System; Observability |
| `C3` | Authority Evolution |
| `C4` | Authority Evolution; Production Autonomy |
| `C5` | Rollback |
| `C6` | Runtime Eligibility |
| `C7` | Movement Protection; Production Readiness |
| `D1` | Production Readiness; Movement Protection, only if substrate scope changes |
| `D2` | Recovery Admission, only if provider lifecycle becomes product scope |
| `D3` | Recovery Admission, only if DNS failover becomes product scope |
| `D4` | Authority Evolution, only if distributed operator control becomes product scope |
| `D5` | Movement Protection, only if split-traffic routing becomes product scope |
| `D6` | Movement Protection, only if routing-protocol ownership becomes product scope |

Engineering Report Lifecycle:

Engineering Reports are not project documents.

Engineering Reports are execution history.

Therefore the rule:

```text
Do NOT create a new document
```

does not apply to Engineering Reports.

Engineering Reports must be created automatically after every meaningful engineering action.

Engineering Reports must be written only in Russian.

Project documents include only:

- `REFERENCE`;
- `PROGRAMS`;
- `POLICIES`;
- `ADR`;
- `BACKLOG`;
- `PRODUCT`;
- `SYSTEM MAP`;
- `CANONICAL REFERENCE`;
- Runtime Model;
- Decision Model.

Engineering Reports belong only to:

```text
docs/reports/engineering/
```

They are historical evidence.

They never become:

- backlog;
- roadmap;
- canonical owner;
- reference document.

Report types:

| Type | Trigger | Purpose | Length |
| --- | --- | --- | --- |
| Type 1: Engineering Report | Automatically after implementation, audit, semantic audit, test, verification, deploy, truth, convergence, certification, runtime investigation, root cause analysis, capability progress change, or production action. | Historical engineering evidence. | Short. |
| Type 2: Milestone Report | Automatically only when a capability becomes `COMPLETE`, a capability becomes `LOCKED`, a major certification completes, a Production Maturity milestone is reached, or an autonomy tier is promoted. | Summarize an engineering milestone. | Detailed. |

After every meaningful engineering action, OMP must create and save an engineering report as historical evidence.

Applicable actions:

- implementation;
- semantic audit;
- testing;
- verification;
- certification;
- deploy;
- truth;
- convergence;
- runtime investigation;
- root cause analysis;
- production action;
- capability progress update.

Report location:

```text
docs/reports/engineering/
```

Filename format:

```text
YYYY-MM-DD_HHMMSS_<topic>.md
```

Engineering Report must include:

- Summary;
- Action Performed;
- Objective Observations;
- Engineering Conclusions;
- Business Objective affected;
- Capability affected;
- Backlog affected;
- Canonical knowledge affected;
- Production impact;
- User impact;
- Почему система приняла именно такое решение;
- Почему решение считается безопасным;
- Почему решение считается полезным;
- Почему система НЕ выбрала альтернативные варианты;
- Impact on Runtime;
- Impact on OMP;
- Impact on Backlog;
- Impact on Capability;
- Impact on Production;
- Capability Progress;
- Backlog Progress;
- Production Maturity;
- Canonical Knowledge;
- Evidence: tests, truth, convergence, deploy, production outcome where applicable;
- Next Step;
- Re-audit Rule.

Milestone Report must include:

- Capability;
- Reason for milestone;
- What became `COMPLETE`;
- What became `LOCKED`;
- Canonical knowledge created;
- Production impact;
- Autonomy impact;
- Lessons learned;
- Remaining capabilities.

Reports are historical evidence only.

Reports must never become a roadmap, planner, governance layer, execution owner, truth source, or second implementation queue.

Canonical update workflow:

If durable knowledge is discovered during any meaningful engineering action, Codex must update the appropriate existing canonical owner before the work is considered complete:

- `docs/reference/V7_CANONICAL_REFERENCE.md` for system truth;
- `docs/reference/SYSTEM_MAP.md` for ownership/topology changes;
- `docs/decisions/` ADR only when project meaning changes;
- `docs/reference/V7_RUNTIME_MODEL.md` only when Runtime semantics change by explicit approved design;
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` when OMP operating behavior changes.

Durable knowledge must never remain only inside reports.

Knowledge Plane Operationalization:

The Knowledge Plane is operational, but it is not a new owner, roadmap, truth source, audit registry, planner, governance layer, execution path, or runtime subsystem.

It is the daily consumption contract across existing owners:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Implementation Backlog
  -> Runtime Model
  -> Implementation
```

Production rule:

| Concept | Meaning | Owner |
| --- | --- | --- |
| Knowledge State | Current durable knowledge state for future engineering and Codex work. | Canonical Reference + SYSTEM_MAP + OMP knowledge workflow. |
| Engineering Reports | Historical evidence only. | `docs/reports/engineering/`. |
| Current Program State | Current runtime/program situation. | `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Canonical Reference | Durable project truth. | `docs/reference/V7_CANONICAL_REFERENCE.md`. |
| OMP | Execution program. | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`. |
| Implementation Backlog | Single engineering queue. | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`. |

Mandatory engineering workflow:

```text
Read Product Specification
  -> Read Audit Knowledge State
  -> Read Canonical Reference
  -> Read Current Program State
  -> Read OMP
  -> Read Implementation Backlog
  -> Determine:
       Already known?
       Still valid?
       Re-open required?
       Implementation required?
  -> Continue only through existing owner / existing backlog path
```

Mandatory audit workflow:

```text
Read Audit Knowledge State
  -> Check Confidence
  -> Check Freshness
  -> Check Re-open Triggers
  -> Reuse Existing Knowledge
  -> Audit Only Unknown Knowledge
  -> Update Canonical Owners when durable knowledge changes
  -> Update Audit Knowledge State
  -> Create Historical Engineering Report
```

Mandatory implementation workflow:

```text
Read Knowledge Plane
  -> Implement existing backlog item
  -> Verify
  -> Certify when required
  -> Engineering Report
  -> Canonical Update if durable knowledge changed
  -> Knowledge State Update
  -> Current Program State Update
  -> OMP Update
```

Mandatory certification workflow:

```text
Certification
  -> Update Knowledge State
  -> Update Capability State
  -> Update Production State
  -> Update Current Program State
  -> Create Historical Evidence
```

Knowledge promotion workflow:

```text
Temporary Investigation
  -> Engineering Report
  -> Verified
  -> Canonical Owner
  -> Audit Knowledge State
  -> OMP Consumption
  -> Future Codex / Future AI Agent Consumption
```

Knowledge invalidation workflow:

| Trigger | Existing owner responsible for invalidation decision |
| --- | --- |
| Runtime Model changes | Runtime Model owner + OMP + SYSTEM_MAP. |
| Product changes | Product Specification owner + Canonical Reference. |
| Policy changes | Canonical Policy Library + OMP. |
| Production evidence contradicts current knowledge | Current Program State + Production Maturity Model + OMP Root Cause Engine. |
| Implementation changes material behavior | Implementation Backlog owner + OMP + relevant code owner. |
| Operator decision changes approved boundary | OMP authority model + Current Program State. |
| Architecture changes | Architecture Closed by Default gate + Canonical Reference + SYSTEM_MAP. |
| Product Scale Model changes | Product Specification + Production Scale First gate. |

Knowledge consumption rule:

Future Codex and future AI agents must never start work by reading historical reports as current truth. Reports may be read only as supporting evidence after the Knowledge Plane identifies that evidence is required.

Future work must first consume:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Implementation Backlog
```

Then consume `Runtime Model`, implementation files, reports, ADRs, policies, or tools only when the resolved task requires them.

Knowledge Plane validation gate:

Every meaningful OMP action must answer:

1. Is this already known?
2. Which existing owner holds it?
3. Is the knowledge still fresh enough?
4. What confidence/certification state applies?
5. Does any re-open trigger apply?
6. Does durable knowledge need promotion from report to owner?
7. Is implementation required, and if yes, which existing backlog item owns it?
8. Need New Owner? Default `FALSE`.
9. Need New Backlog Item? Default `FALSE`.

If the answer cannot be mapped after complete audit, OMP may report a gap. Architecture extension remains the last resort.

Engineering Context Resolver integration:

Before any OMP engineering action, OMP must use `docs/reference/V7_CONTEXT_RESOLVER.md` as the Engineering Context Resolver.

Required ECR outputs:

| Field | Required value |
| --- | --- |
| `task_class` | One of Architecture, Knowledge, Product, Policy, Implementation, Runtime, Production, Certification, Audit, Scale, Bug, Investigation, Operator Request, Research. |
| `mandatory_context` | Minimum documents/owners required for the class. |
| `optional_context` | Only loaded if mandatory context cannot answer safely. |
| `forbidden_by_default_context` | Reports, packet state, runtime state, implementation files, or research that must not be loaded unless the class requires it. |
| `authoritative_owner` | Existing owner from SYSTEM_MAP / Canonical Reference. |
| `already_verified` | `YES`, `NO`, or `UNKNOWN`. |
| `still_current` | `CURRENT`, `STALE_RECHECK_REQUIRED`, `HISTORY_ONLY`, or `UNKNOWN`. |
| `reopen_required` | `TRUE` or `FALSE`, with trigger if true. |
| `implementation_required` | Existing backlog item or `NO`. |
| `certification_required` | Existing capability/policy/certification path or `NO`. |
| `runtime_investigation_required` | Existing runtime owner or `NO`. |
| `need_new_owner` | Default `FALSE`. |
| `need_new_backlog_item` | Default `FALSE`. |

For `Continue OMP`, ECR must resolve the default working set to:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Current Backlog Item
```

Nothing else is loaded unless OMP maps the current item to a specific owner or a re-open trigger fires.

Current implementation optimizer result:

| Field | Current Value |
| --- | --- |
| Highest implementation leverage task | `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS` |
| Implementation class | `IMPLEMENT_CERTIFICATION` |
| Exact owner | Restore barrier, guarded autoswitch execution, verification, rollback, outcome closure, feedback/learning |
| Exact module | Canonical Policy Library Stage 4 implementation backlog and existing governed canary transaction owner |
| Exact files | `tools/v7-governed-canary-dry-run-cycle`, `tests/unit/test_governed_canary_cli.py`, `admin_core/operator_execution.py`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py` |
| Implementation status | `A4_BOUNDED_EVIDENCE_COLLECTION_READY` |
| Backlog source | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` item `A4` |
| Priority model | `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md` |
| Truth/convergence | Commit `87c9d2fecec9a418cf9214d0b523f90ee4ecc0af` is local/GitHub/production aligned; full truth with network access is `PASS`. |
| New highest implementation leverage task | `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS` |
| Stop boundary | `OPERATIONAL_AUTHORITY`: bounded A4 evidence collection is ready, but production movement authority is required before any restore-barrier write or apply. |

Latest safe deployment result:

| Field | Current Value |
| --- | --- |
| Deployed commit | `87c9d2fecec9a418cf9214d0b523f90ee4ecc0af` |
| Deploy id | `deploy-z8-14-Updatesystem-87c9d2f-20260627T120908` |
| Deployed backlog items | `A1`, `A2`; A3 approval-to-execution lease binding fix; A3 approved plan lock snapshot-gate consumption fix; A3 real no-rollback outcome closure; A4 governed transaction feedback materialization; A4 bounded evidence collection mode |
| Safety | Bounded collection mode reuses existing one-user governed transaction owner, requires explicit confirmation, stops on the first failed gate, keeps runtime automation disabled, and does not expand authority. |
| Truth | Full `tools/v7-truth-check --all --json` with network access: `PASS`; local, GitHub, and production all at `87c9d2fecec9a418cf9214d0b523f90ee4ecc0af`. |
| Convergence | Runtime aligned; deploy delta empty; production CLI exposes `--execute-a4-bounded-evidence-collection`. |
| Current stop | `OPERATIONAL_AUTHORITY`: bounded A4 evidence collection can collect up to `68` successful one-user governed outcomes, but requires explicit approval before production movement; no synthetic evidence may be used |

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

The old bottleneck action, governed candidate suitability outcome closure, remains the highest real-outcome action. The approval-to-execution lease binding defect is fixed and deployed; the current blocker is now an unsafe implementation defect inside the existing autoswitch owner.
The current implementation-first optimizer must fix approved plan lock consumption through the intelligence snapshot gate before requesting another packet approval or attempting apply again.

## 8. Current Authority Class

| Field | Current Value |
| --- | --- |
| Current authority level | `NONE`; current stop is engineering safety, not authority. |
| Current stop reason | `UNSAFE_IMPLEMENTATION` |
| Boundary location | After approved packet consumption and restore-barrier clearance, before mutation inside `tools/v7-users-autoswitch` intelligence snapshot gate. |
| Current exact runtime posture | Restore-barrier clearance was written for the approved packet, guarded apply failed closed before movement, no autonomous apply, no daemon enablement. |
| Next authority action | None until the existing autoswitch owner preserves approved locked selected moves through the intelligence snapshot gate. |

Current production evidence:

- approval-to-execution lease binding fix is deployed and production truth/convergence pass;
- operator approved exact packet `pkt_preview_4eb137c926917c2761faadb4`;
- execution lease `execlease_19550ea3b6750ed163344f8a` preserved packet identity;
- restore-barrier clearance `rbclear_1951ca727830c155efc8cf0e` was written through the existing owner;
- guarded apply denied mutation with `approved_plan_lock_selected_moves_missing` and unsafe blocker `approved_plan_lock_snapshot_gate_stop_required`;
- selected moves were present before restore-barrier clearance and zero after the intelligence snapshot gate;
- no user movement, daemon, timer, or authority expansion occurred;
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
| `Continue OMP` | Execute the complete Engineering Control Loop: ECR -> Knowledge Plane -> re-open evaluation -> OMP execution -> implementation/audit/certification/verification -> Engineering Report -> knowledge promotion -> Current Program State/OMP update -> next highest-leverage action, until an allowed stop condition. |
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

- approval-to-execution lease binding is fixed, tested, deployed, and verified;
- operator approved exact packet `pkt_preview_4eb137c926917c2761faadb4`;
- selected move hash is `e1e09d2c95fc6c9b0b77e9ecaaf0def20e9759150eb35db8d70f95e107eb52cd`;
- user is `10.7.0.17`, move is `vless -> awg0`;
- restore-barrier clearance was written through the existing owner;
- guarded apply failed closed before movement because the existing autoswitch owner lost the approved selected move at the intelligence snapshot gate;
- no additional operator approval is useful until this owner defect is fixed;
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
| Current bottleneck | A4 representative real outcome evidence; production dry-run prepared packet `pkt_preview_79169161d388d83473ae732e` for one governed outcome. |
| Current highest leverage action | Stop at `OPERATIONAL_AUTHORITY`; execute only exact packet `pkt_preview_79169161d388d83473ae732e` if operator approves, otherwise keep A4 blocked without synthetic evidence. |
| Current reuse ratio | `100%`. |
| Current duplicate ratio | `0% known introduced`. |
| Current automation ratio | `84.167%`. |
| Current blockers | `OPERATIONAL_AUTHORITY`: exact TIER_1 governed production action approval is required before restore-barrier write or apply. A4 still requires additional real comparable outcomes, freshness recheck, class-level blast-radius evidence, authority policy approval, runtime policy binding, and hard-failure classification recheck before promotion. |
| Current maturity | Tier 0 `COMPLETE`; Tier 1 `ACTIVE`; A4 governed transaction workflow and feedback materialization are production-deployed; latest completed transaction moved one user and raised A4 evidence to `88 / 156` consumed outcomes. |
| Current runtime posture | No autonomous apply, no daemon enablement, and no authority expansion; A4 performed one explicitly approved governed movement, while the next A4 movement is stopped at operational authority. |
| Current next best action | Present exact approve/reject prompt for packet `pkt_preview_79169161d388d83473ae732e`; no apply, restore barrier, user movement, authority expansion, daemon/timer, or runtime automation without approval. |
| Last optimizer iteration | `2026-06-27`: governed transaction packet `pkt_preview_2b4c165055beb66d37b0581e` was executed for user `10.7.0.19 vless -> awg3`, verified successfully, closed as no-rollback outcome with feedback `execfb_dc570c36697ac0c9986d6661`, and updated A4 inventory to `88 / 156` consumed outcomes. |

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
