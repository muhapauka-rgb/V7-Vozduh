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

### Runtime Time Architecture Discipline

Status: `RT_PHASE_1_FULLY_COMPLETE`.

OMP consumes Runtime Time Architecture from `docs/reference/V7_RUNTIME_MODEL.md`.
OMP does not own a second time model.

RT Phase 1 implemented the permanent foundation:

| Step | Status | Canonical owner | Completion condition |
| --- | --- | --- | --- |
| `RT1` Canonical Time Architecture | `COMPLETE` | Runtime Model | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, and OMP/Certification planes are named and mapped to existing owners. |
| `RT2` Reaction Latency Model | `COMPLETE` | Runtime Model | Reaction Latency and all components are defined without numeric SLOs or runtime gates. |
| `RT3` Thin Runtime Path Contract | `COMPLETE` | Runtime Model | Runtime remains short, deterministic, lease-bound, fail-closed, and does only live safety work. |
| `RT4` Latency Ownership & Live/Precompute Matrix | `COMPLETE` | Runtime Model | Every current runtime path stage has owner, precompute/live classification, safety reason, future optimization path, and measurement field. |
| `RT5` Engineering Report Latency Requirement | `COMPLETE` | OMP Engineering Report Lifecycle | Every future meaningful engineering report must include Latency Impact. |
| `RT6` Phase 2 Automation-Time Contract | `COMPLETE` | Runtime Model + OMP | Phase 2 scope, dependencies, owners, safety conditions, and expected outputs are defined without implementation. |
| `RT7` Engineering Review Rule | `COMPLETE` | Runtime Model + OMP Engineering Report Lifecycle | Every future engineering activity must answer the Runtime Latency Engineering Review Checklist. |
| `RT8` Phase 2 Automation Contract | `COMPLETE` | Runtime Model + OMP | Phase 2 entry criteria, forbidden pre-entry behavior, complete item contracts, exit criteria, owners, dependencies, safety constraints, and success criteria are defined without implementation. |

OMP execution rule:

```text
Every future audit, implementation, verification, certification, deploy, production action, and OMP status update must preserve the thin runtime path.
```

Work Placement execution rule:

```text
Every future OMP task must identify the canonical execution plane for every meaningful computation it touches.
```

Required placement outputs:

| Field | Required value |
| --- | --- |
| `computation` | The work being introduced, audited, moved, or certified. |
| `canonical_plane` | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, OMP/Certification, or `NOT_APPLICABLE_WITH_REASON`. |
| `canonical_owner` | Existing owner responsible for the computation. |
| `runtime_placement_allowed` | `YES_ONLY_IF_LIVE_SAFETY_REQUIRED`, `NO`, or `NOT_APPLICABLE`. |
| `can_move_earlier` | `YES`, `NO_WITH_SAFETY_REASON`, or `ALREADY_PREPARED`. |
| `reaction_latency_impact` | Observation, Decision, Execution, Verification, Feedback/Learning, Reaction, `NONE`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |

Product Evolution Review Gate:

Every future OMP task must pass these reviews before implementation is considered complete:

| Review | Required output |
| --- | --- |
| Certification Review | Mandatory, supporting, optional, or not applicable evidence, according to the canonical certification owner. |
| Work Placement Review | Canonical plane and owner for each meaningful computation. |
| Runtime Latency Review | Reaction Latency component affected, or `NONE`. |
| Runtime Cost Review | CPU, memory, IO, blocking, lock contention, execution cost, rollback cost, and runtime cost impact. |
| Decision Freshness Review | Birth/fresh/stale/invalid/destroyed state and owner for runtime-relevant decision objects. |
| Safety Review | Live gates that remain live and exact `STOP_SAFE` triggers. |

If any review cannot map to an existing owner, OMP must stop and run owner mapping before implementation.

Every future change must answer:

1. Does this increase Runtime work?
2. Can this work be safely prepared earlier?
3. Which latency component is affected?
4. Which live safety gate must remain live?
5. Does the change move V7 toward lower safe Reaction Latency or away from it?

Mandatory Runtime Latency Engineering Review:

| Question | Required answer |
| --- | --- |
| Does this work increase the Runtime execution path? | `YES`, `NO`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| Can this work move into Observation, World Model, Planning, read model, or background computation? | `YES`, `NO_WITH_SAFETY_REASON`, or `NOT_APPLICABLE`. |
| If it must stay live, why? | Existing safety gate, live eligibility, irreversible apply, verification, rollback, authority, freshness, or `NOT_APPLICABLE`. |
| Which latency components change? | Observation, Decision, Execution, Verification, Feedback, Learning, Reaction, or `NONE`. |
| Does it reduce any latency? | Component name and reason, or `NO`. |
| Does it create a wait state or blocking dependency? | `YES_WITH_OWNER`, `NO`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| Does it change safety gates? | Freshness, restore barrier, rollback, verification, authority, anti-flap, blast radius, source/target eligibility, or `NONE`. |
| Does it preserve Thin Runtime Path? | `YES` required; `NO` blocks implementation. |
| Can computation be precomputed safely? | `YES`, `NO_WITH_SAFETY_REASON`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| If latency impact is unknown, how will it be measured later? | Existing field, existing owner extension, or explicit `NOT_APPLICABLE` reason. |

This checklist is mandatory for implementation, audit, verification, test, deployment, certification, owner extension, planner change, runtime change, feedback change, learning change, read-model change, policy change, and OMP change.

Phase 1 forbids:

- runtime automation;
- user movement;
- production apply;
- authority expansion;
- batch movement;
- parallel movement;
- execution queues;
- latency SLOs as gates;
- planner rewrite;
- runtime behavior change.

Phase 2 is deferred, not optional.
It may start only after bounded automation, runtime eligibility, verification, rollback, blast radius, metric reliability, reaction latency measurement, and explicit authority are certified or approved through existing owners.

### Pre-Phase-2 Readiness

Status: `CANONICAL_PROGRAM`
Owner: OMP.
Canonical foundation owner: `docs/reference/V7_RUNTIME_MODEL.md`.

Purpose:

Prepare V7 for Runtime Phase 2 Automation & Runtime Optimization without starting Phase 2, enabling runtime automation, expanding authority, moving users, creating a new owner, or creating a new backlog item.

Pre-Phase-2 Readiness is an implementation-readiness program inside OMP.
It does not replace RT Phase 1, RT6, RT8, A5, A6, B13, B16, or the Implementation Backlog.
It consumes them and decides whether Phase 2 may be opened later.

Foundation status:

| Foundation | Status | Canonical owner | Current integration |
| --- | --- | --- | --- |
| `DL1` Decision Lifetime Model | `EXISTS` | Runtime Model | Canonicalized in Decision Lifecycle And Runtime Foundation; consumed by OMP/report lifecycle. |
| `DL2` Decision Freshness Contract | `EXISTS` | Runtime Model | Canonical states `BORN`, `FRESH`, `STALE`, `INVALID`, `DESTROYED`; consumed by freshness, lease, material-change, and OMP review owners. |
| `DL3` World Model Ownership | `EXISTS` | Runtime Model + SYSTEM_MAP reference | Plane-based ownership exists; SYSTEM_MAP maps current owners. |
| `DL4` Desired Safe State Contract | `EXISTS_PARTIAL` | Runtime Model + Decision Model | Desired State exists; Desired Safe State artifact belongs to Phase 2 and must wait for A6/B13/authority. |
| `DL5` Runtime Cost Model | `EXISTS` | Runtime Model | Runtime cost review is mandatory in Product Evolution Review; measurement remains pre-Phase-2/Phase-2 work. |
| `DL6` Runtime Budget Allocation | `EXISTS_PARTIAL` | Runtime Model | Budget categories exist; numeric budgets are forbidden before measurement and Phase 2 entry. |
| `DL7` Product Evolution Review Gate | `EXISTS` | Runtime Model + OMP | Mandatory for future OMP tasks and Engineering Reports. |

Readiness stages:

| Stage | Goal | Dependencies | Existing owner | Completion criteria | Validation | Relationship to A5/A6/B13/B16/RT Phase 2 |
| --- | --- | --- | --- | --- | --- | --- |
| `DL1` Decision Lifetime Implementation | Make all runtime-relevant decision objects traceable from birth to terminal state. | Decision Lifecycle Foundation, packet/lease/outcome owners. | Runtime Model, packet/lease/governed transaction owners. | Objects have owner, valid-while rule, invalidation rule, and terminal state. | Tests/truth/convergence/report when implementation touches behavior. | Required before A6 can arbitrate live execute/stop reliably. |
| `DL2` Decision Freshness Implementation | Ensure every decision object has a freshness state and material-change semantics. | A2, material-state gate, freshness owners. | Freshness/lease/runtime eligibility owners. | Freshness changes and material invalidation are separated. | Freshness tests, material-change tests, truth/convergence. | Required for A6 and Phase 2 decision freshness lifetime. |
| `DL3` World Model Ownership | Ensure every state family has one plane owner and no silent owner replacement. | SYSTEM_MAP, Work Placement Law, read-model owners. | Runtime Model + SYSTEM_MAP + OMP. | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, and OMP ownership are explicit. | Work Placement review and duplicate-owner checks. | Required before continuous world model work in Phase 2. |
| `DL4` Desired Safe State | Define desired safe state without self-authorizing execution. | Business Objectives, policies, A6, B13, authority model. | Runtime Model, Decision Model, OMP, planner owners. | Desired Safe State is bounded by policy, blast radius, authority, rollback, verification, and runtime eligibility. | Product Evolution Review and safety review. | Cannot become runtime behavior before A6/B13/B16 and authority; Phase 2 consumes it later. |
| `DL5` Runtime Cost Model | Make runtime cost visible before optimization. | Work Placement, Runtime Latency Review, Product Scale. | Runtime Model + OMP. | CPU, memory, IO, blocking, lock contention, execution, rollback, and runtime cost are reviewed. | Engineering Report Runtime Cost Review. | Required before any Phase 2 runtime optimization. |
| `DL6` Runtime Budget Allocation | Keep budget categories ready without premature SLO gates. | Runtime Cost Model, Reaction Latency measurements. | Runtime Model + Production Maturity/OMP owners. | Observation, World Model, Planning, Execution, Verification, Learning, and OMP budgets are categorized; numeric gates remain deferred. | Reported as measurement category, not authority. | Numeric budgets wait for Phase 2 entry evidence. |
| `DL7` Product Evolution Review Gate | Ensure every future change passes certification, placement, time, cost, freshness, and safety review. | Engineering Report Lifecycle, OMP. | OMP + Runtime Model. | Every meaningful action records Product Evolution Review or explicit not-applicable reason. | Engineering Report completeness and truth/convergence. | Guards A5/A6/B13/B16 and all Phase 2 readiness work. |

Pre-Phase-2 Readiness is complete only when:

- RT Phase 1 is `FULLY_COMPLETE`;
- Work Placement Law is canonical;
- Decision Lifecycle And Runtime Foundation is canonical;
- Engineering Report Lifecycle requires Product Evolution Review, Work Placement, Latency Impact, Runtime Cost Review, and Decision Freshness Review;
- A5 is complete;
- A6 is complete;
- B13 is complete;
- B16 is complete;
- bounded automation is certified or explicitly approved through existing authority owners;
- Reaction Latency is measurable;
- Runtime Cost is measurable;
- World Model ownership is canonical and consumed by implementation owners;
- Desired Safe State is canonical and bounded by policy/authority/safety;
- OMP explicitly authorizes Phase 2 entry.

Phase 2 entry contract:

```text
Phase 2 may begin only when:
RT Phase 1 COMPLETE
AND Work Placement COMPLETE
AND Decision Lifecycle COMPLETE
AND Pre-Phase-2 Readiness COMPLETE
AND A5 COMPLETE
AND A6 COMPLETE
AND B13 COMPLETE
AND B16 COMPLETE
AND Reaction Latency measurable
AND Runtime Cost measurable
AND World Model canonical
AND Desired Safe State canonical
AND Engineering Review active
AND explicit authority permits Phase 2 work.
```

If any condition is missing, OMP must continue through the existing highest-priority backlog item and must not start Phase 2.

Before Phase 2 entry, OMP forbids:

- parallel movement;
- batch movement;
- continuous apply;
- execution queues;
- desired-state runtime;
- latency SLO gates;
- planner rewrite;
- authority expansion.

Phase 2 completion requires:

- end-to-end Reaction Latency measurement;
- per-plane latency visibility;
- Desired-State Delta implemented through existing planner owners;
- Execution Queue certification;
- Bounded Parallelism certification;
- fail-closed Runtime preserved;
- rollback and verification preserved unless separately certified;
- authority unchanged unless separately approved.

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

### Architectural Design Methodology Execution

OMP does not own a separate architectural law.
OMP executes the complete methodology preserved in `docs/reference/V7_CANONICAL_REFERENCE.md` under `ARCHITECTURAL_DESIGN_METHODOLOGY`.

For every meaningful future capability, OMP must prove:

| Review | Required OMP answer |
| --- | --- |
| Product intent | Which Business Objective and Product Scale Objective are affected. |
| Existing owner | Which owner in SYSTEM_MAP, Canonical Reference, OMP, policy, ADR, Runtime Model, Decision Model, or backlog already owns the capability. |
| Work placement | Which plane owns the computation and whether it can safely move earlier. |
| Decision lifecycle | Which objects are born, fresh, stale, invalid, destroyed, committed, or terminal. |
| Certification truth | Which canonical owner declares mandatory, supporting, optional, inventory, or optimization evidence. |
| Runtime time / cost | Which Reaction Latency component and Runtime Cost dimension are affected. |
| Product scale | Whether the design remains suitable for `10,000+` users, `100+` channels, millions of decisions, and long-lived evidence. |
| Safety | Which live gates remain live and what forces `STOP_SAFE`. |
| Automation / authority | Whether the work changes authority, autonomy, runtime apply, or production movement. |
| Execution queue | Which existing backlog item or OMP capability owns the implementation. |

If any answer requires a new owner, new backlog item, new runtime path, or new architecture, OMP must first run Architecture Closed by Default and the Root Cause Engine.

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
| Tier A | `6` | `6` | `COMPLETE` |
| Tier B | `21` | `21` | `COMPLETE` |
| Tier C | `4` | `7` | `IN_PROGRESS` |
| Tier D optional | `0` | `6` | `OPTIONAL` |
| Overall actionable | `31` | `34` | `ACTIVE` |

Implementation maturity:

```text
91.2%
```

Estimated remaining effort:

```text
Moderate
```

Next backlog item:

```text
C5
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
| Implementation | `91.2` | `100` | `20` |
| Testing | `74` | `100` | `10` |
| Production Deployments | `100` | `100` | `10` |
| Production Outcomes | `25` | `100` | `15` |
| Certification | `95` | `100` | `15` |
| Authority Evolution | `15` | `100` | `10` |
| Production Autonomy | `0` | `100` | `10` |
| Implementation Backlog Completion | `91.2` | `100` | `10` |

Production Maturity:

```text
Current: 64.3%
Target: 100%
Remaining: 35.7%
```

Backlog:

```text
Tier A: 6 / 6 complete
Tier B: 21 / 21 complete
Tier C: 4 / 7 complete
Tier D: 0 / 6 optional complete
Overall: 31 / 34 actionable complete
```

Current highest implementation task:

```text
C5: Preserve rollback as operational compensation rather than transaction rollback.
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
50%: Implementation Half Complete
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
91.2%

Certification
95%

Autonomy
0%

Production Maturity
64.3%

Overall Status
ENGINEERING_COMPLETE / PRODUCTION_IN_PROGRESS

Current Focus
IMPLEMENTATION

Backlog
Tier A
6 / 6
Tier B
21 / 21
Tier C
4 / 7
Tier D
0 / 6 optional
Overall
31 / 34 complete

Current Tier
TIER_1_GOVERNED

Highest Priority Task
C5: preserve rollback as operational compensation rather than transaction rollback.

Status
C4 DONE_READ_ONLY / C5 Ready

Authority
No expansion active

Required Action
Run C5 through existing Runtime Model, rollback policy, verification, and canonical update owners.

Engineering
READY

Runtime
READY_READ_ONLY

Packet
NONE_ACTIVE

Estimated Remaining Work
Moderate

Expected Next Milestone
50%: Implementation Half Complete
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
Movement Protection | 76.0% | 100% | 24.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | B16, B19, B21, C7 | Complete after movement stability, rollback, recovery, anti-flap, routing mode, slow-start, and pool-health criteria are satisfied.
Runtime Eligibility | 61.0% | 100% | 39.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | B17, B18, C1, C6 | Complete after Runtime can decide execute-or-stop from certified gates and related stale-read/lease semantics are certified.
Authority Evolution | 68.0% | 100% | 32.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | B12, B16, B21, C3, C4 | Complete after action classes and delegated policy can replace repeated packet approval.
Rollback | 47.0% | 100% | 53.0% | IN_PROGRESS | VERY_HIGH | HIGH | A3, B15, B16, C5 | Complete after rollback/no-rollback class evidence and authority are certified.
Recovery Admission | 78.0% | 100% | 22.0% | IN_PROGRESS | HIGH | HIGH | D2, D3 if optional recovery scope changes | Complete after recovered channels are reintroduced through certified readiness and slow-start and optional recovery scope remains resolved or explicitly not applicable.
Learning | 63.0% | 100% | 37.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A3 | Complete after real outcomes reliably improve future decisions.
Production Readiness | 64.3% | 100% | 35.7% | IN_PROGRESS | VERY_HIGH | HIGH | Remaining actionable backlog and certification | Complete at PRODUCTION_AUTONOMY_CERTIFIED.
Production Autonomy | 0.0% | 100% | 100.0% | IN_PROGRESS | VERY_HIGH | VERY_HIGH | A3, A4, A5, A6, B10, B12, B16, C4 | Complete when Runtime operates inside certified policy and operator supervises.
Knowledge System | 100.0% | 100% | 0.0% | LOCKED | HIGH | MEDIUM_HIGH | None | Complete and locked under canonical knowledge rules.
Observability | 63.0% | 100% | 37.0% | IN_PROGRESS | HIGH | MEDIUM_HIGH | B15, B17, C2 | Complete when operators and OMP can inspect all safety/runtime evidence without mutation.
Decision Explainability | 25.0% | 100% | 75.0% | IN_PROGRESS | HIGH | HIGH | B1, B4, B13, B15, B17, C2 | Complete when every approval request explains the decision in Russian before Approve / Reject, using existing evidence owners only.
Implementation Discipline | 100.0% | 100% | 0.0% | COMPLETE | VERY_HIGH | MEDIUM | None | Complete while Backlog remains the only live queue.
Engineering Knowledge Preservation | 100.0% | 100% | 0.0% | LOCKED | HIGH | MEDIUM | None | Complete and locked while reference/report/ADR roles remain normalized.

Current Capability
Action-Class Stage Certification / Authority Evolution / Production Readiness

Current Backlog Item
B12

Completion Prediction
B12 completes after the next action-class stage is implemented only from existing certification evidence, authority policy owners, and OMP without direct class promotion, Runtime apply, authority expansion, synthetic evidence, or user movement.

Blocking Items
B12 current; later authority, runtime apply, delegated policy, user-mode, and production autonomy work remains blocked by B16, B21, C3, C4, and remaining certification where applicable.
```

Initial capability registry:

| Capability | Purpose | Current % | Target % | Current Status | Canonical Owner | Production Value | Autonomy Impact | Blocking Backlog Items | Expected Completion Point | Re-open Triggers |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| Movement Protection | Prevent chaotic user movement while preserving fast reaction to real failures. | `76.0` | `100` | `IN_PROGRESS` | OMP, Movement Protection Model, Runtime Model, Canonical Policy Library | `VERY_HIGH` | `VERY_HIGH` | `B16`, `B19`, `B21`, `C7` | All Movement Protection DoD criteria complete or explicitly `NOT_APPLICABLE`. | Production evidence disproves behavior; planner/runtime architecture materially changes; explicit operator request. |
| Runtime Eligibility | Decide whether Runtime may execute or must stop using certified gates. | `61.0` | `100` | `IN_PROGRESS` | Runtime Model, OMP, delegated policy preview, action-class enablement owners | `VERY_HIGH` | `VERY_HIGH` | `B17`, `B18`, `C1`, `C6` | Action-class runtime eligibility arbitration is implemented; freshness/reporting semantics remain to be certified. | Runtime architecture changes; production eligibility failure; explicit operator request. |
| Authority Evolution | Move from packet approval to bounded class/policy authority without silent expansion. | `68.0` | `100` | `IN_PROGRESS` | OMP, Authority policy, Runtime Model, action-class ladder | `VERY_HIGH` | `VERY_HIGH` | `B12`, `B16`, `B21`, `C3`, `C4` | Certified class evidence supports authority recommendation and operator/certified policy approval. | Authority incident; operator policy change; explicit authority expansion/shrink request. |
| Rollback | Guarantee safe compensation or certified no-rollback behavior for production actions. | `42.9` | `100` | `IN_PROGRESS` | Restore barrier, rollback manifest, Runtime Model, execution feedback | `VERY_HIGH` | `HIGH` | `A3`, `B15`, `B16`, `C5` | Rollback/no-rollback class evidence and automatic rollback authority are certified. | Failed rollback; verification failure pattern; explicit operator request. |
| Recovery Admission | Admit recovered channels safely without oscillation or premature scale. | `78.0` | `100` | `IN_PROGRESS` | Recovery admission owner, service matrix, quality compact, blast-radius/action-class ladder | `HIGH` | `HIGH` | `D2`, `D3` if optional recovery scope changes | Repeated real readiness evidence, observation windows, and read-only slow-start progression are complete; runtime consumption remains future authority/implementation work. | Recovery incident; service evidence changes; explicit operator request. |
| Learning | Convert real outcomes into future decision quality without synthetic evidence. | `63.0` | `100` | `IN_PROGRESS` | Feedback/learning owner, OMP, Canonical Reference | `VERY_HIGH` | `VERY_HIGH` | `A3` | Representative real outcomes and metric reliability support promotion recommendations. | Learning regression; synthetic evidence risk; explicit operator request. |
| Production Readiness | Make V7 deployable, operable, verifiable, and certifiable as a production system. | `64.3` | `100` | `IN_PROGRESS` | OMP, Production Maturity Model, Implementation Backlog | `VERY_HIGH` | `HIGH` | `C7`, optional `D1`-`D6` only if scope changes | Production Maturity reaches `100%` and outputs `PRODUCTION_AUTONOMY_CERTIFIED`. | Production safety incident; deploy model change; explicit operator request. |
| Production Autonomy | Enable Runtime to operate inside certified authority while operator supervises. | `0.0` | `100` | `IN_PROGRESS` | OMP, Runtime Model, Authority Evolution, action-class promotion | `VERY_HIGH` | `VERY_HIGH` | `A3`, `A4`, `A5`, `A6`, `B10`, `B12`, `B16`, `C4` | Bounded autonomy and then production autonomy are certified by real outcomes and approved authority. | Autonomy incident; authority policy change; explicit operator request. |
| Knowledge System | Preserve verified project knowledge and prevent repeated rediscovery. | `100.0` | `100` | `LOCKED` | Canonical Reference, Context Resolver, Research Framework, Policy Library, Document Lifecycle | `HIGH` | `MEDIUM_HIGH` | None current. | Current knowledge owners remain canonical and read-only under document lifecycle rules. | Industry consensus changes; `FUNDAMENTAL_ARCHITECTURE_GAP`; explicit operator request. |
| Observability | Expose enough read-only truth for operators, OMP, Runtime, and certification. | `35.0` | `100` | `IN_PROGRESS` | Admin read models, trust/evidence inventory, truth/convergence | `HIGH` | `MEDIUM_HIGH` | `B1`, `B4`, `B9`, `B15`, `B17`, `C2` | Read-only evidence shows eligibility, rollback, stale reads, promotion quality, and runtime readiness. | Operator cannot diagnose; evidence disagreement; explicit operator request. |
| Decision Explainability | Explain existing Runtime / OMP decisions to the operator before any approval request. | `25.0` | `100` | `IN_PROGRESS` | OMP, Current Program State, Runtime Model, evidence read models | `HIGH` | `HIGH` | `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Every approval request explains reason, evidence, expected value, risks, alternatives, and capability impact in Russian before Approve / Reject. | Operator cannot understand approval reason; explanation contradicts evidence; explicit operator request. |
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
| Runtime Eligibility | Freshness windows exist; owner-issued freshness exists; authority, blast, rollback, anti-flap, verification, and learning gates are arbitrated; stale read reporting is preserved; bounded stale allowance is decided by action class. | Runtime Model; A2 freshness windows; A6 read-only execute-or-stop arbitration. | B17 stale-read reporting; B18 owner lease extension; C1 fail-open/fail-closed; C6 bounded stale allowance. |
| Authority Evolution | Operational and engineering authority are separated; packet approval is retired class-by-class; class approval and delegated policy approval require certified evidence; authority never expands silently. | Authority normalization; action-class ladder; packet approval classified as temporary governed fallback; A3-A5 evidence; A6 read-only eligibility; B13 blocking recommendation metric reliability. | B11 isolation; B12 staged promotion; B16 rollback authority; B21 user mode; C3/C4 authority constraints. |
| Rollback | Restore barrier works; rollback manifest exists; exact selected move identity is preserved; rollback/no-rollback evidence is certified; automatic rollback authority is certified only after reliable verification. | Restore barrier; rollback manifest; exact packet/lease identity path. | A3 class evidence; B15 containment/forward-fix classification; B16 automatic rollback authority; C5 compensation semantics. |
| Recovery Admission | Recovered channels require repeated real success/readiness evidence; post-admission observation exists; slow-start recovery is runtime-certified. | Recovery admission read model; limited recovery blast radius. | B8 certification; B9 observation windows; B10 slow-start progression. |
| Learning | Only real observed outcomes feed learning; outcome closure exists; representative evidence exists; metric reliability supports promotion recommendations. | Real-only learning rule; feedback owner; outcome closure path; B13 blocking recommendation metric reliability. | A3/A4 real outcomes; B5 attribution. |
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
- Product Evolution Review;
- Work Placement;
- Latency Impact;
- Canonical Knowledge;
- Evidence: tests, truth, convergence, deploy, production outcome where applicable;
- Next Step;
- Re-audit Rule.

Latency Impact must include:

| Field | Required value |
| --- | --- |
| Observation Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Decision Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Execution Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Verification Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Feedback / Learning Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Reaction Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Runtime path impact | `increased`, `decreased`, `unchanged`, or `not applicable`. |
| Precompute opportunity | `YES` or `NO`. |
| Live gate impact | `YES` or `NO`. |
| Wait-state impact | `YES_WITH_OWNER`, `NO`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| Measurement plan | Existing measurement field, existing owner extension, or `NOT_APPLICABLE_WITH_REASON`. |
| Notes | Short explanation. |

`UNKNOWN` is acceptable in RT Phase 1.
Omitting Latency Impact is not acceptable after RT Phase 1.

Engineering Reports must use the canonical Runtime Latency Engineering Review Checklist from `docs/reference/V7_RUNTIME_MODEL.md`.

Work Placement must include:

| Field | Required value |
| --- | --- |
| Computation | Meaningful computation touched by the action, or `NOT_APPLICABLE_WITH_REASON`. |
| Canonical Plane | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, OMP/Certification, or `NOT_APPLICABLE_WITH_REASON`. |
| Canonical Owner | Existing owner responsible for the computation. |
| Runtime Placement | `YES_ONLY_IF_LIVE_SAFETY_REQUIRED`, `NO`, or `NOT_APPLICABLE`. |
| Move Earlier? | `YES`, `NO_WITH_SAFETY_REASON`, or `ALREADY_PREPARED`. |
| Reaction Latency Impact | Observation, Decision, Execution, Verification, Feedback/Learning, Reaction, `NONE`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |

Product Evolution Review must include:

| Field | Required value |
| --- | --- |
| Certification Review | Mandatory, supporting, optional, or not applicable evidence with owner. |
| Work Placement Review | `PASS`, `FAIL`, or `NOT_APPLICABLE_WITH_REASON`. |
| Runtime Latency Review | Affected component or `NONE`. |
| Runtime Cost Review | CPU, memory, IO, blocking, lock contention, execution cost, rollback cost, runtime cost, or `NONE`. |
| Decision Freshness Review | Relevant lifecycle states and owner, or `NOT_APPLICABLE_WITH_REASON`. |
| Safety Review | Live gates and `STOP_SAFE` triggers, or `NOT_APPLICABLE_WITH_REASON`. |

Architectural Methodology Review must include:

| Field | Required value |
| --- | --- |
| Methodology status | `COMPLETE`, `REUSED`, or `BLOCKED_WITH_REASON`. |
| Existing laws used | Product intent, owner reuse, Work Placement, Decision Lifecycle, Certification Truth, Runtime Time, Product Scale, Safety, Authority, and OMP/backlog path, or `NOT_APPLICABLE_WITH_REASON`. |
| Missing law | `NONE` unless a complete Architecture Closed by Default audit proves otherwise. |
| New owner/backlog/architecture | `FALSE` unless explicitly proven. |

Pre-Phase-2 Readiness Review must include:

| Field | Required value |
| --- | --- |
| DL1-DL7 impact | Affected foundation or `NONE`. |
| Phase 2 readiness impact | `TOWARD`, `AWAY`, or `NEUTRAL_WITH_REASON`. |
| Entry contract impact | Which Phase 2 entry criterion changed, or `NONE`. |
| Runtime automation impact | `NO` unless explicit authority and certification exist. |

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
| Highest implementation leverage task | `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD` |
| Implementation class | `IMPLEMENT_VERIFICATION` |
| Exact owner | Action-class ladder, planner budgets, capacity/load gates, blast-radius evidence owner |
| Exact module | Canonical Policy Library Stage 4 implementation backlog and existing action-class/blast-radius owners |
| Exact files | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_execution_pipeline.py` |
| Implementation status | `A4_DONE_A5_READY` |
| Backlog source | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` item `A5` |
| Priority model | `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md` |
| Truth/convergence | Latest run after A4 closure read-model deploy: truth `PASS`; convergence `ALIGNED`. |
| New highest implementation leverage task | `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD` |
| Stop boundary | `NONE`: continue A5 certification analysis through existing owners; do not expand authority or runtime automation. |

Current A4 bounded authority envelope:

| Field | Current Value |
| --- | --- |
| Authority status | `ACTIVE` |
| Approved scope | Current A4 bounded evidence collection only |
| Max successful evidence outcomes requested | `63` remaining at start of latest bounded run |
| One-user limit | `YES` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Packet-by-packet approval | `NO` inside this bounded envelope |
| Stop rule | Stop on first failed gate, failed verification, rollback need, duplicate, non-missing candidate, scope expansion, or runtime automation attempt |
| Current stop | `REAL_WORLD_LIMIT_A4_NO_GAP_REDUCING_CANDIDATE`; evidence-gap guard stopped before lease, restore-barrier write, or apply |

Latest bounded A4 collection continuation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_170227_a4_bounded_collection_outcome.md` |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `duplicate_transaction_candidate` |
| Successful verified outcomes | `1` |
| Successful move | `10.7.0.25 vless -> awg3` |
| Verification | `PASS` |
| Rollback | `NOT_REQUIRED` |
| A4 evidence | `94 / 156 = 60.3%`; missing `62 / 156 = 39.7%` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Current next action | Continue A4 bounded collection under the existing approved envelope; do not ask for packet approval. |

Latest bounded A4 gap-guard stop:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_170634_a4_gap_guard_stop.md` |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `candidate_not_missing_a4_evidence` |
| Candidate | `10.7.0.5 awg0 -> vless` |
| Successful verified outcomes | `0` |
| Apply | `NO` |
| Restore barrier | `NO` |
| Users moved | `0` |
| A4 evidence | `94 / 156 = 60.3%`; missing `62 / 156 = 39.7%` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Current next action | Wait for a fresh gap-reducing candidate or read-model refresh through existing owners; do not request packet approval and do not synthesize evidence. |

Latest A4 gap-directed candidate existence audit:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_174442_a4_gap_directed_candidate_existence_audit.md` |
| Missing A4 candidate keys | `62` |
| Eligible candidate rows | `40` |
| Gap-reducing eligible candidate rows | `18` |
| Planner-selected candidate | `10.7.0.5 -> vless` |
| Planner-selected candidate missing? | `NO` |
| Users moved | `0` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Verdict | `GAP_REDUCING_CANDIDATES_EXIST_BUT_NOT_SELECTED` |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle`; `admin_core.autonomy_trust_acceleration`; `admin_core.intelligence_workers` |
| Next OMP action | Extend existing A4 governed selection to choose a safe gap-reducing candidate before attempting bounded transaction execution. |

Latest A4 goal-directed selection implementation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_180848_a4_goal_directed_selection_fix.md` |
| Code commit | `1db9267d862675d85742339532ed8180b10552ef` |
| Deploy id | `deploy-z8-14-Updatesystem-1db9267-20260627T180506` |
| Owner reused | `tools/v7-governed-canary-dry-run-cycle` |
| Missing keys loaded before selection | `YES` |
| Eligible universe scanned | `YES` |
| Non-missing candidate skipped | `YES` |
| Gap-reducing candidate selected when available | `YES` |
| Explicit stop when none available | `NO_SAFE_GAP_REDUCING_A4_CANDIDATE` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Users moved during implementation | `0` |
| Truth | `PASS` |
| Convergence | `PASS / ALIGNED` |
| Next OMP action | Resume A4 bounded representative evidence collection through the existing governed transaction owner. |

Latest A4 evidence requirement sanity audit:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_181934_a4_evidence_requirement_sanity_audit.md` |
| Final verdict | `A4_EVIDENCE_REQUIREMENT_OVERSCOPED` |
| `candidate_count` origin | Dynamic count of concrete `user -> candidate_channel` keys from `candidate-suitability-summary` |
| Current count | `94 / 156 = 60.3%`; missing inventory keys `62` |
| Canonical finding | The `156` keys are inventory coverage, not a canonical A4 completion threshold. |
| A4 intent | Representative action-class evidence for the first action class, not exhaustive full-matrix enumeration. |
| Product Scale alignment | Full user-channel enumeration must not become a permanent autonomy blocker unless explicitly justified. |
| Existing owners | `A4`; `B13`; `A5`; `A6`; `POLICY_005_ACTION_CLASS_PROMOTION`; Product Scale Model |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Runtime changed | `NO` |
| Next OMP action | Extend existing A4/B13 evidence owners to separate representative completion from candidate inventory coverage before continuing bounded collection as a completion strategy. |

Latest Master Action Class Certification Model audit:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_182735_master_action_class_certification_model_audit.md` |
| Final verdict | `ACTION_CLASS_CERTIFICATION_MODEL_COMPLETE` |
| Canonical A4 objective | Materialize representative real outcome evidence for the first action class. |
| First action class | `single-user governed candidate failover` |
| Full certification chain | `A4 -> A5 -> A6 -> B13 -> B12/authority` |
| `missing_candidate_outcomes` role | Inventory coverage / supporting evidence / learning input; not canonical hard gate |
| Current implementation mismatch | `readiness_impact.exact_outcome_deficit_blocks_canary = missing_candidate_outcomes` over-converts inventory deficit into a hard blocker |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Need New Architecture | `FALSE` |
| Next OMP action | `A4_CERTIFICATION_GATE_ALIGNMENT_IN_EXISTING_EVIDENCE_OWNER`; do not move users solely to exhaust all remaining inventory keys. |

Latest Master OMP Certification Alignment implementation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_215615_master_omp_certification_alignment_implementation.md` |
| Implementation owner | `admin_core.autonomy_trust_acceleration` |
| Existing owners reused | `YES` |
| New owner | `NO` |
| New backlog item | `NO` |
| New architecture | `NO` |
| Runtime behavior changed | `NO` |
| Canonical alignment | `missing_candidate_outcomes` remains visible as `INVENTORY_SIGNAL`; it is no longer exposed as mandatory `missing_evidence` for A4 certification/runtime enablement. |
| Downstream alignment | A5 consumes certified A4 outputs; A6 consumes certified gates and live runtime safety, not exhaustive inventory deficits; B13 consumes representative evidence/reliability. |
| Validation | `python3 -m unittest tests.unit.test_autonomy_trust_acceleration`; `python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_pipeline`; `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only --pretty` |
| Next OMP action | `A4_REPRESENTATIVE_CERTIFICATION_VALIDATION_AND_CONTINUE_OMP` |

Latest A4 representative certification validation access correction:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_222642_a4_representative_certification_validation.md` |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle`; `admin_core.autonomy_trust_acceleration` |
| Bounded collection command | `tools/v7-governed-canary-dry-run-cycle --execute-a4-bounded-evidence-collection --confirm-a4-bounded-evidence-collection EXECUTE_A4_BOUNDED_EVIDENCE_COLLECTION_APPROVED --max-users 1 --max-evidence-outcomes 68 --pretty` |
| Collection status | `LOCAL_RUN_INVALID_FOR_PRODUCTION_EVIDENCE` |
| Stop reason | `local_runtime_state_unavailable` |
| Current missing A4 candidate keys | `NOT_VERIFIED`; local `0` was caused by absent local `/opt/v7` state and must not be treated as production evidence |
| Transactions attempted | `0` |
| Users moved | `0` |
| Runtime automation enabled | `NO` |
| Authority expanded | `NO` |
| Truth | `PASS` |
| Convergence | `PASS` |
| Production access | Direct SSH read-only attempt to production was denied by authentication; existing production-side owner must be run where `/opt/v7` state is available. |
| OMP meaning | Do not infer A4 candidate absence from local missing runtime state; continue only through authenticated production-side validation. |
| Next OMP action | `A4_PRODUCTION_SIDE_CERTIFICATION_VALIDATION` |

Latest A4 collection input guard implementation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_224128_a4_collection_input_guard.md` |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle` |
| Implementation | A4 bounded collection now checks required runtime state, candidate snapshot, and evidence sources before calculating missing candidate keys. |
| Stop reason when inputs are unavailable | `runtime_state_unavailable` |
| False completion prevented | Local missing `/opt/v7` state can no longer be interpreted as `no_missing_a4_candidate_outcomes`. |
| Runtime automation enabled | `NO` |
| Users moved | `0` |
| Authority expanded | `NO` |
| Next OMP action | `A4_PRODUCTION_SIDE_CERTIFICATION_VALIDATION` through production-side existing owners. |

Previous bounded A4 collection result:

| Field | Current Value |
| --- | --- |
| Collection status | `STOP_SAFE` after bounded production execution |
| Successful outcomes | `2` |
| Users moved | `10.7.0.20 vless -> awg3`; `10.7.0.21 vless -> awg3` |
| Verification | `PASS` for both governed transactions |
| Rollback | `NOT_REQUIRED` for both governed transactions |
| A4 evidence | `90 / 156 = 57.7%`; missing `66 / 156 = 42.3%` |
| Stop reason | `duplicate_transaction_candidate`; duplicate guard stopped before another lease, restore-barrier write, or apply |
| Runtime automation | `NO`; still disabled |
| Authority expansion | `NO` |
| Current next action | Continue A4 only when a fresh non-duplicate candidate exists; do not synthesize evidence or repeat the duplicate candidate |

Previous single approved A4 transaction:

| Field | Current Value |
| --- | --- |
| Packet | `pkt_preview_a61462aaffb4510b6237fb95` |
| User moved | `10.7.0.5 awg3 -> awg0` |
| Apply | `PASS` |
| Verification | `PASS` |
| Rollback | `NOT_REQUIRED` |
| Outcome closure | `CLOSED`; feedback and learning records written from real observed outcome |
| Users moved | `1` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| A4 coverage after outcome | `90 / 156 = 57.7%`; missing `66 / 156 = 42.3%` |
| Progression note | Real outcome was recorded, but representative coverage did not increase; continue with the next fresh A4 candidate through existing OMP. |

Previous bounded A4 authority-envelope run:

| Field | Current Value |
| --- | --- |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `transaction_verification_failed` |
| Transactions attempted | `3` |
| Successful verified outcomes | `2` |
| Successful moves | `10.7.0.22 vless -> awg3`; `10.7.0.23 vless -> awg3` |
| Failed transaction | `10.7.0.24 vless -> awg3` |
| Verification | `FAIL` for `10.7.0.24` |
| Rollback | `ROLLBACK_COMPLETED`; user returned to `vless` |
| A4 evidence | `93 / 156 = 59.6%`; missing `63 / 156 = 40.4%` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Current next action | Do not ask for packet approval. Continue bounded A4 collection under the existing approved envelope. |

Latest rollback learning audit:

| Field | Current Value |
| --- | --- |
| Audit report | `docs/reports/engineering/2026-06-27_162929_master_rollback_learning_audit.md` |
| Rollback behavior | `EXPECTED_RUNTIME_PROTECTION`; verification failed and rollback completed to `vless` |
| Exact verification failure | Assignment expected `awg3`, but table route and route_get for `10.7.0.24` still used `tun0` after apply |
| Planner verdict | No planner defect proven; candidate was in A4 scope and passed pre-apply guards |
| Feedback defect | Fixed and deployed: `tools/v7-governed-canary-dry-run-cycle::materialize_governed_transaction_feedback` now materializes terminal outcome classification and `admin_core.operator_execution_feedback` consumes terminal state before feedback/learning |
| Incorrect learning result | Previous behavior produced `outcome_status=success`, `outcome_quality=SUCCESS`, positive trust/recommendation deltas |
| Correct learning result | `ROLLBACK_SUCCESS` / rollback learning; preserve rollback success evidence; do not count as successful move evidence or promotion success |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle`; `admin_core/operator_execution_feedback.py`; A4 evidence owners |
| Need New Owner | `FALSE` |
| Need New Backlog | `FALSE` |
| Current next action | Continue bounded A4 collection without packet-by-packet approval; preserve terminal classifications for every real outcome |

Non-blocking A4 optimization note:

| Field | Current Value |
| --- | --- |
| Optimization | `A4_MARGINAL_EVIDENCE_VALUE_RANKING` |
| Status | `RECORDED_NOT_BLOCKING` |
| Classification | `FUTURE_EFFICIENCY_WORK` |
| Blocks A4 | `NO` |
| Creates backlog item | `NO` |
| Current behavior | Bounded A4 collection asks: `Does this fresh candidate reduce the current A4 evidence gap?` |
| Future behavior | Rank currently eligible candidates by marginal evidence value and prefer the highest-value safe one. |
| Marginal Evidence Value | Expected reduction of the current A4 representative evidence gap + verified learning value + new cohort/user/channel coverage value - movement/risk/cost/anti-flap penalty. |
| Boundaries | No new authority; no runtime automation; no batch movement; one user per governed A4 transaction; stop on any failed live gate; no synthetic evidence; no threshold or formula change now. |
| Existing owners | A4 evidence matcher/read-model owners; governed dry-run owner; intelligence workers; outcome leverage model; OMP. |
| Current OMP action | Continue current bounded evidence collection; this note must not delay A4 evidence collection. |

Latest safe deployment result:

| Field | Current Value |
| --- | --- |
| Deployed commit | `19882a14d81cc8a6d05e8e46d40fc63ae7ed5446` |
| Deploy id | `deploy-z8-14-Updatesystem-19882a1-20260627T125619` |
| Deployed backlog items | `A1`, `A2`; A3 approval-to-execution lease binding fix; A3 approved plan lock snapshot-gate consumption fix; A3 real no-rollback outcome closure; A4 governed transaction feedback materialization; A4 bounded evidence collection mode; A4 bounded collection evidence/duplicate pre-apply guard |
| Safety | Bounded collection mode reuses the existing one-user governed transaction owner, requires explicit confirmation, stops before lease/restore/apply for non-missing or duplicate candidates, keeps runtime automation disabled, and does not expand authority. |
| Truth | Full `tools/v7-truth-check --all --json` with network access: `PASS`; local, GitHub, and production all at `19882a14d81cc8a6d05e8e46d40fc63ae7ed5446`. |
| Convergence | Runtime aligned; deploy delta empty; runtime action guard `READY_FOR_RUNTIME_ACTION`. |
| Current stop | `NONE_FOR_CLASSIFICATION_FIX`: terminal classification fix is implemented, tested, deployed, and verified; continue A4 bounded evidence collection |

Latest A4 completion:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_232150_a4_closure_read_model_filter.md` |
| Final A4 state | `DONE` |
| Real evidence | A4 bounded collection reduced missing candidate inventory to `0`; inventory signals are empty. |
| Outcome closure | `COMPLETE`; production replay showed `387` valid closure candidates, `0` missing closure records, and `8011` non-closure history records ignored. |
| Deploy | `deploy-z8-14-Updatesystem-f49f4fa-20260627T232657` |
| Commit | `f49f4fa8d4ffe0d582bd807f0b45e7e48d724b38` |
| Truth/convergence | Truth `PASS`; convergence `ALIGNED`. |
| Runtime automation | `NO` |
| Authority expanded | `NO` |
| Users moved by read-model fix | `0` |
| Next OMP action | `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD` |

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
| Runtime Latency Foundation | RT1-RT8 complete: Runtime Time Architecture, Reaction Latency, Thin Runtime Path Contract, live/precompute matrix, Engineering Report Latency Impact, Phase 2 Automation-Time Contract, Runtime Latency Engineering Review Checklist, and complete Phase 2 Automation Contract embedded through existing owners | `COMPLETED` | `docs/reference/V7_RUNTIME_MODEL.md`, `docs/reports/engineering/2026-06-28_003325_rt_phase1_runtime_latency_foundation.md`, `docs/reports/engineering/2026-06-28_004129_rt_phase1_extension_rt7_rt8.md` |

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
| Current bottleneck | C5 rollback-as-operational-compensation documentation is next; C4 is complete as read-only all-at-once promotion unavailable verification. |
| Current highest leverage action | Run C5 through existing Runtime Model, rollback policy, verification, and canonical update owners. |
| Current reuse ratio | `100%`. |
| Current duplicate ratio | `0% known introduced`. |
| Current automation ratio | `84.167%`. |
| Current blockers | None yet for C5 rollback semantics preservation; C5 must not execute rollback, grant authority, enable Runtime apply, enable automation, move users, replace planner ownership, create a new owner, or bypass existing Runtime Model/rollback policy owners. |
| Current maturity | Tier 0 `COMPLETE`; Tier 1 `ACTIVE`; Production Maturity `64.3%`; Tier A backlog `6 / 6`; Tier B backlog `21 / 21`; Tier C backlog `4 / 7`; overall backlog `31 / 34`. |
| Current runtime posture | No autonomous apply, no daemon enablement, no authority expansion; local validation moved `0` users and now stops explicitly with `runtime_state_unavailable` when local `/opt/v7` state is absent. |
| Current next best action | `C5_PRESERVE_ROLLBACK_AS_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK`; no runtime apply, no automation, no authority expansion, no rollback execution, no synthetic evidence, no user movement, no planner replacement, no new owner, no new backlog, no architecture change. |
| Last optimizer iteration | `2026-06-29`: RT2-S6 evidence-based continuous improvement implemented as read-only owner-mapped advisory recommendation; current result is `DONE_READ_ONLY_OWNER_MAPPED_RECOMMENDATION`; tests passed. |

## 24.1 Capability Transition Contract

Status: `ACTIVE_CANONICAL`.

Owner: OMP.

Purpose:

OMP must permanently explain not only what the next step is, but why that step is now available, which capability produced the unlocking evidence, which owner may consume it, and why later steps remain forbidden.

This contract is not a new lifecycle, roadmap, owner, planner, runtime, truth source, capability program, dashboard authority, automation mode, or implementation queue.

Transition audit:

| Item | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Execution order | `EXISTS_COMPLETE` | `A5 -> A6 -> B13 -> B16 -> Runtime Capability Maturation Program`. | None. |
| RT2 entry criteria | `EXISTS_COMPLETE` | Section 28.1 entry criteria. | None. |
| Workstream flow | `EXISTS_COMPLETE` | Section 28.3 workstream table and OMP engineering lifecycle. | None. |
| Transition explanation | `EXISTS_PARTIAL` | CPS and OMP state show the next step and produced evidence, but not a durable transition reason table. | Add this contract inside OMP. |
| Transition owner mapping | `EXISTS_PARTIAL` | SYSTEM_MAP maps owners but not transition ownership as a first-class lookup. | Add SYSTEM_MAP transition row. |
| Durable transition rule | `EXISTS_PARTIAL` | Canonical Reference preserves execution order and current state. | Add durable rule that reports must not be the only transition explanation. |

Transition rule:

1. A step becomes available only when the previous step produced real or read-only certified evidence accepted by its canonical owner.
2. A step may consume only the evidence named for that transition.
3. Unlocking a step never unlocks later steps by implication.
4. Runtime apply, automation, authority expansion, user movement, dashboard authority, synthetic evidence, and new ownership remain forbidden unless the specific transition explicitly produces certified authority for them.
5. If the next step cannot explain current capability, produced evidence, consumed evidence, unlocked capability, blocked capability, and safety reason, OMP must stop and extend this contract before continuing.

Major capability transitions:

| From step | Current capability | Produced evidence | Consumed evidence | Unlocked capability | Still blocked capability | Why next step is available | Why later steps remain forbidden |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A5` -> `A6` | Blast-radius certification. | Class-level blast-radius evidence beyond one-user guard; historical E29 one/two/four-user proofs consumed read-only. | A3 rollback/no-rollback evidence, A4 representative outcome evidence, action-class ladder, policy/blast-radius owners. | Runtime eligibility arbitration. | Runtime apply, authority expansion, automation, concurrency, class promotion. | A6 can safely arbitrate execute-or-stop only after blast-radius evidence is no longer unknown. | A5 proves evidence shape only; it does not approve execution, authority, positive promotion, or runtime mutation. |
| `A6` -> `B13` | Runtime eligibility arbitration. | Read-only execute-or-stop gate rows across freshness, authority, blast radius, rollback/no-rollback, anti-flap, verification, learning, routing readiness, and runtime_apply. | A1-A5 certification outputs, freshness owners, authority owners, runtime_apply boundary. | Metric reliability certification for promotion recommendations. | Positive promotion, automatic execution, authority expansion, runtime apply. | B13 may consume A6 because metric reliability needs one canonical gate answer before metrics can support promotion recommendations. | A6 result is `STOP_SAFE` at authority/runtime_apply; it cannot unlock execution or authority by itself. |
| `B13` -> `B16` | Metric reliability certification. | Reliable blocking recommendation certification; positive promotion remains blocked. | Trust/confidence, source confidence, rollback evidence, blast-radius evidence, closure, learning, A6 runtime eligibility. | Rollback authority readiness certification. | Positive promotion, automatic rollback authority, runtime apply, action-class authority, automation. | B16 may start because rollback authority review needs reliable metric and evidence classification before evaluating rollback readiness. | B13 certifies blocking recommendations only; it does not certify authority, rollback execution, or movement. |
| `B16` -> `RT2-S1` | Rollback authority readiness. | Rollback/verification/metric/runtime evidence certified for authority review only; authority/runtime_apply remain STOP gates. | Rollback evidence, verification closure, no-rollback learning, B13 metric reliability, A6 runtime eligibility. | RT2-S1 Measurement & Observability Foundation. | RT2-S2 through RT2-S6 execution, runtime apply, automation, dashboard authority, concurrency, authority expansion. | RT2-S1 may begin because measurement can safely consume certified rollback/verification evidence as read-only context without granting authority. | B16 does not grant automatic rollback authority; only read-only measurement becomes safe, and later RT2 workstreams still require S1 outputs and their own completion criteria. |
| `RT2-S1` -> `RT2-S2` | Measurement and observability. | Runtime cost, runtime time, reaction latency, stop reasons, lifecycle, wait states, dependency topology, Time-To-Safe-Recovery, and bottlenecks visible or owner-mapped as missing. | Execution contracts, events, read models, timestamps, duration fields, latency fields, CPS, truth/convergence. | World and readiness maturation. | Desired-state delta, governed execution coordination, concurrency, recommendations, runtime apply. | S2 may begin only after measurement blockers are owner-mapped so world/readiness can consume known observability gaps safely. | Measurement fields are read-only; dashboards/read models cannot decide, approve, rank execution, mutate, or certify later workstreams. |
| `RT2-S2` -> `RT2-S3` | World and readiness maturation. | Fresh prepared state and readiness summaries bounded for runtime consumption. | Observation outputs, snapshots, freshness, service matrix, quality compact, user/channel/policy state. | Desired-state delta preparedness. | Execution coordination, queue behavior, concurrency, authority expansion, runtime mutation. | S3 may begin when readiness is prepared and bounded, allowing deltas to reference current state without raw runtime scans. | Prepared world/readiness state cannot approve movement, become a planner, or bypass live gates. |
| `RT2-S3` -> `RT2-S4` | Desired-state delta preparedness. | Advisory desired-state delta or bounded prepared plan. | Business Objectives, policies, current state, action-class certification, movement protection. | Governed execution coordination. | Concurrency, automation, runtime queue, authority expansion. | S4 may begin only when a prepared plan can be consumed safely by existing packet/lease/verification owners. | Desired State and deltas remain advisory and non-authorizing; they cannot become Runtime behavior. |
| `RT2-S4` -> `RT2-S5` | Governed execution coordination. | Idempotent governed execution coordination and terminal classification. | Prepared plan, packet, lease, restore barrier, verification plan, rollback/no-rollback state. | Certified concurrency ladder. | Parallelism, blast-radius expansion, automatic execution without authority. | S5 may begin only after one bounded action can move from approval to terminal outcome without stale loops. | Coordination proof for one bounded path does not certify parallelism, wider blast radius, or authority. |
| `RT2-S5` -> `RT2-S6` | Certified concurrency ladder. | Certified concurrency level or explicit STOP_SAFE. | Blast-radius evidence, rollback capacity, verification capacity, policy scope, authority envelope, anti-flap state. | Evidence-based continuous improvement. | Runtime self-optimization, automatic recommendations, authority lowering, safety gate weakening. | S6 may begin after concurrency is certified or explicitly deferred, because recommendations need known safe execution limits. | Parallelism is safety certification only; recommendations cannot mutate runtime, expand authority, or convert metrics into authority. |
| `RT2-S6` -> graduate or return to OMP | Evidence-based continuous improvement. | Owner-mapped recommendation or explicit no-change verdict with safety, latency, cost, time, evidence, and canonical update. | Outcomes, reports, latency/cost/time/topology data, fit analysis, maturity gaps. | Graduation or return to highest unfinished OMP/backlog owner. | New roadmap, new owner, Runtime self-optimization, direct implementation without OMP. | Graduation is allowed only when S6 produces a no-change or owner-mapped recommendation that has been canonically preserved. | S6 output is advisory until OMP routes approved implementation to an existing owner or backlog item. |
| `B9` -> `B10` | Post-admission observation windows. | `post_admission_observation_windows = DONE_READ_ONLY_OWNER_MAPPED`; verified service observation and quality compact `5m`/`1h` windows. | B8 recovery admission certification, service matrix, quality compact. | Recovery slow-start progression. | Runtime apply, traffic admission, authority expansion, queue, synthetic evidence, user movement. | B10 could safely define slow-start only after observation windows were owner-mapped and tested. | B9 only verified observation windows; it could not grant runtime behavior or authority. |
| `B10` -> `B11` | Recovery slow-start progression. | `recovery_slow_start_progression = DONE_READ_ONLY_OWNER_MAPPED`; staged progression `OBSERVATION_CERTIFIED_READ_ONLY` -> `ONE_USER_GOVERNED_RECOVERY_REVIEW` -> `BEYOND_ONE_USER_ACTION_CLASS_REVIEW`. | B8 recovery certification, B9 observation windows, class-level blast-radius certification, action-class ladder. | Org/cohort isolation and identity policy integration. | Runtime apply, traffic admission, automation, authority expansion, concurrency, queue, synthetic evidence, user movement. | B11 may start because B10 defines the recovery progression boundary and keeps identity/cohort scope as the next policy integration gap. | B10 is read-only progression only; it cannot approve recovery traffic, expand authority, or bypass identity/cohort policy gates. |
| `B11` -> `B12` | Org/cohort identity policy integration. | `org_cohort_identity_policy_integration = DONE_READ_ONLY_OWNER_MAPPED`; existing identity -> group/cohort -> allowed/preferred/excluded egress -> exclusive_group/egress ACL/default isolation gates are integrated read-only. | B10 recovery slow-start progression, existing planner gates, identity policy, org policy, channel policy, action-class ladder, authority policy owners. | Next action-class stage certification. | Runtime apply, traffic admission, automation, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion. | B12 may start because B11 proves identity/cohort policy boundaries are visible through existing owners before action-class certification can consume them. | B11 is read-only policy integration only; it cannot grant action-class authority, promote a class, admit traffic, move users, or bypass certification evidence. |
| `B12` -> `B14` | Next action-class stage certification. | `next_action_class_stage_certification = DONE_READ_ONLY_STAGE_GATE_IMPLEMENTED`; A5/A6/B13/B11 evidence is consumed into a stage-review gate that cannot grant authority or runtime apply. | A5 blast-radius evidence, A6 runtime eligibility arbitration, B13 blocking metric reliability, B11 identity/policy boundaries, action-class ladder. | Service/pool/cohort blast-radius scope. | Runtime apply, traffic admission, automation, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion, blast-radius expansion. | B14 may start because B12 proves next-stage work is bounded by certification evidence and explicit authority/runtime STOP gates. | B12 is a read-only stage gate only; it cannot approve class authority, expand blast radius, mutate Runtime, or bypass service/pool/cohort blast-radius review. |
| `B17` -> `B18` | Stale-read reporting with mutation blocking. | `stale_read_mutation_blocking = DONE_READ_ONLY_STALE_READ_MUTATION_BLOCKING`; stale/unknown freshness remains reportable as read-only evidence while mutation stays blocked. | Freshness actionability, runtime eligibility arbitration, routing recommendation readiness, truth/convergence, read-only inventory, OMP. | Owner-issued version/lease pattern extension. | Runtime apply, automation, mutation from stale read, authority expansion, concurrency, queue, planner replacement, synthetic evidence, threshold/formula mutation, user movement. | B18 may start because B17 proves stale reads remain visible but cannot authorize mutation, so lease/version extension can consume freshness and snapshot identity safely. | B17 is observability and gating only; it cannot grant runtime apply, change lease semantics, create a new owner, mutate thresholds/formulas, or move users. |
| `B18` -> `B19` | Owner-issued version/lease pattern. | `owner_issued_version_lease_pattern = DONE_READ_ONLY_OWNER_ISSUED_VERSION_LEASE_PATTERN`; owner-issued version/lease/generation/TTL/source-hash coverage is visible without lease behavior change. | Execution lease, Runtime Model freshness gates, `SNAPSHOT_FAMILIES`, freshness actionability, action-class freshness windows, B17 stale-read mutation blocking, OMP. | Hysteresis and state-change-cost mapping. | Runtime apply, automation, authority expansion, threshold/formula mutation, lease behavior change, new owner, concurrency, queue, planner replacement, synthetic evidence, user movement. | B19 may start because B18 makes freshness/lease identity coverage explicit, allowing state-change-cost and hysteresis mapping to consume currentness boundaries safely. | B18 is read-only coverage only; it cannot change lease behavior, become a truth source, mutate thresholds/formulas, or authorize movement. |
| `B19` -> `B20` | Hysteresis and state-change-cost mapping. | `hysteresis_state_change_cost_mapping = DONE_READ_ONLY_HYSTERESIS_STATE_CHANGE_COST_MAPPING`; existing sticky/current bias, minimum improvement, cooldown, observation window, oscillation detection, user freeze, pair reversal, target block/quarantine, recovery thresholds, and freshness identity cost vocabulary are centralized. | Anti-flap, recovery admission, service threshold, movement-protection, autoswitch safety, OMP. | Hard-failure override anti-flap arbitration. | Runtime apply, automation, authority expansion, threshold/formula mutation, new owner, concurrency, queue, planner replacement, synthetic evidence, user movement. | B20 may start because B19 defines the anti-flap/state-change-cost vocabulary that hard-failure override must arbitrate against. | B19 is read-only vocabulary only; it cannot implement hard-failure override, mutate thresholds/formulas, or authorize movement. |
| `B20` -> `B21` | Hard-failure override anti-flap arbitration. | `hard_failure_override_anti_flap_arbitration = DONE_READ_ONLY_HARD_FAILURE_OVERRIDE_ANTI_FLAP_ARBITRATION`; confirmed hard failure is encoded as anti-flap override candidate for authority review only, while suspected/no hard failure cannot override anti-flap. | Hard-failure classification, hard-failure policy windows, anti-flap, B19 hysteresis/state-change-cost mapping, planner/runtime eligibility, OMP. | Per-user routing control mode. | Runtime apply, automation, authority expansion, hard-failure override execution, threshold/formula mutation, new owner, concurrency, queue, planner replacement, synthetic evidence, user movement. | B21 may start because B20 makes hard-failure/anti-flap arbitration explicit and non-authorizing, so per-user routing control can consume clear safety boundaries. | B20 is read-only arbitration only; it cannot execute override, mutate Runtime, change thresholds/formulas, expand authority, or move users. |
| `B21` -> `C1` | Per-user routing control mode. | `per_user_routing_control_mode = DONE_READ_ONLY_PER_USER_ROUTING_CONTROL_MODE`; explicit or inferred per-user `AUTO` / `PINNED` / `MANUAL` routing control semantics are visible through existing owners. | User registry, group/org policy, planner gates, admin operator surface, B11 identity/cohort policy, B20 hard-failure/anti-flap arbitration, OMP. | Fail-open/fail-closed action-class behavior. | Runtime apply, automation, authority expansion, registry write, planner replacement, new owner, concurrency, queue, synthetic evidence, user movement. | C1 may start because B21 makes user-control mode explicit and non-authorizing, so action-class fail behavior can be recorded against known movement/authority boundaries. | B21 is read-only routing control evidence only; it cannot write the registry, mutate Runtime, expand authority, replace Planner, synthesize evidence, or move users. |
| `C1` -> `C2` | Fail-open/fail-closed action-class behavior. | `fail_open_fail_closed_action_class_behavior = DONE_READ_ONLY_FAIL_OPEN_FAIL_CLOSED_ACTION_CLASS_BEHAVIOR`; every action class records fail-closed Runtime mutation/apply behavior and read-only fail-open allowances for diagnosis, evidence collection, operator explanation, engineering report, and canonical update. | Runtime Model, OMP, planner gates, action-class policy, B21 user mode, stale-read/lease owners, hard-failure arbitration, read-only inventory. | Probabilistic suspicion advisory evidence. | Runtime apply, automation, authority expansion, fail-open runtime mutation, planner replacement, new owner, concurrency, queue, synthetic evidence, user movement. | C2 may start because C1 makes stop/continue behavior explicit and non-authorizing, so weak probabilistic suspicion can be classified advisory-only against a known fail behavior contract. | C1 records behavior only; it cannot make suspicion actionable, grant authority, mutate Runtime, replace Planner, synthesize evidence, or move users. |
| `C2` -> `C3` | Probabilistic suspicion advisory evidence. | `probabilistic_suspicion_advisory_evidence = DONE_READ_ONLY_PROBABILISTIC_SUSPICION_ADVISORY_EVIDENCE`; shadow autonomy, source-confidence, and soft-degradation suspicion have direct blocking power `NONE` and direct execution power `NONE`. | Trust/confidence model, shadow autonomy, soft-degradation policy, OMP, read-only inventory, C1 fail-closed behavior. | Break-glass authority audited exceptional operator policy. | Runtime apply, automation, direct suspicion blocking, authority expansion, planner replacement, threshold/formula mutation, synthetic evidence, user movement. | C3 may start because C2 proves weak/probabilistic suspicion cannot become action authority, so exceptional authority can be documented against a non-silent advisory boundary. | C2 is advisory read-only evidence only; it cannot grant emergency authority, mutate Runtime, lower gates, replace Planner, synthesize evidence, or move users. |
| `C3` -> `C4` | Break-glass authority audited exceptional operator policy. | `break_glass_authority_policy_contract = DONE_READ_ONLY_AUDITED_EXCEPTIONAL_OPERATOR_POLICY`; break-glass is disabled by default, exceptional, audited, operator-policy controlled, and non-authorizing by itself. | OMP, operator authority, governed execution pipeline, observability/audit, feedback/closure, packet/rollback evidence, C2 advisory-only boundary. | All-at-once promotion unavailable verification. | Runtime apply, automation, silent authority expansion, all-at-once promotion, blast-radius expansion, direct class promotion, planner replacement, synthetic evidence, rollback/apply execution, user movement. | C4 may start because C3 proves exceptional authority cannot silently become runtime/class authority, so all-at-once promotion can be verified as unavailable against an explicit non-silent authority boundary. | C3 defines policy only; it cannot invoke break-glass, write restore barrier, execute apply/rollback, expand authority, synthesize evidence, or move users. |
| `C4` -> `C5` | All-at-once promotion unavailable verification. | `all_at_once_promotion_unavailable_verification = DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE`; current action classes have no all-at-once/direct promotion path and remain class-by-class/authority-review bounded. | Action-class runtime enablement, A5 blast-radius certification, B12 stage certification, B14 service/pool/cohort scope, C3 break-glass policy boundary, OMP. | Rollback as operational compensation preservation. | Runtime apply, automation, silent authority expansion, all-at-once promotion, direct class promotion, blast-radius expansion, rollback/apply execution, planner replacement, synthetic evidence, user movement. | C5 may start because C4 proves promotion cannot silently widen authority, so rollback semantics can be preserved as compensation rather than transaction rollback against a stable non-promoting action-class boundary. | C4 is read-only verification only; it cannot promote classes, widen blast radius, mutate Runtime, grant authority, execute rollback/apply, synthesize evidence, or move users. |

Current transition state:

| Field | Value |
| --- | --- |
| Last completed transition | `C4 -> C5` |
| Produced evidence | `all_at_once_promotion_unavailable_verification = DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE`; C4 verifies broad/direct promotion remains unavailable through existing owners. |
| Current unlocked step | `C5_PRESERVE_ROLLBACK_AS_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK` |
| Current forbidden later steps | Runtime self-optimization; automatic recommendations; direct implementation without OMP; authority lowering; safety-gate weakening; Runtime apply; automation; concurrency enablement; authority expansion; blast-radius expansion; all-at-once promotion; queue daemon; planner replacement; registry write; user movement |
| Safety reason | Only existing backlog continuation is unlocked; C4 output is read-only verification evidence and cannot promote classes, mutate Runtime, expand authority, synthesize evidence, start implementation outside OMP, create a new owner, replace Planner, execute rollback/apply, or move users. |

## 24.2 Capability Production Contract

Status: `ACTIVE_CANONICAL`.

Owner: OMP.

Purpose:

OMP must permanently explain not only what stage comes next and why it becomes available, but what capability each stage produces, who owns that capability, who consumes it, what future capability it unlocks, what remains blocked, and why.

This contract is not a new lifecycle, roadmap, owner, planner, runtime, truth source, capability program, dashboard authority, automation mode, or implementation queue.

Capability production audit:

| Item | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Stage execution order | `EXISTS_COMPLETE` | OMP order and transition contract already define `A5 -> A6 -> B13 -> B16 -> RT2-S1 -> RT2-S6`. | None. |
| Produced evidence | `EXISTS_COMPLETE` | Transition contract names evidence produced by each prior stage. | Reuse. |
| Capability owner | `EXISTS_PARTIAL` | Workstream tables and SYSTEM_MAP name owners, but not as a production graph. | Add production contract and graph. |
| Capability consumers | `EXISTS_PARTIAL` | Workstream tables name consumers, but not one producer / owner / consumer validation. | Add producer-consumer matrix. |
| Blocked capability rule | `EXISTS_PARTIAL` | Transition contract names blocked later stages. | Extend into capability-production terms. |
| Durable production rule | `MISSING` | Reports recorded production evidence, but OMP did not permanently state that production knowledge cannot remain report-only. | Add OMP rule and Canonical Reference durable conclusion. |

Capability production rule:

1. Every produced capability must have exactly one stage producer.
2. Every produced capability must have one canonical owner.
3. Every produced capability must have one or more named consumers.
4. A consumer may use only the evidence and capability named by the producing stage.
5. Producing a capability unlocks only the named next capability and never unlocks later capabilities by implication.
6. Blocked capabilities remain blocked until their own producing stage emits accepted evidence.
7. If a capability has no owner, no consumer, duplicate producers, or circular production, OMP must stop before continuing.
8. Engineering reports may record evidence, but the Capability Production Graph, producer/consumer relationships, and unlocked/blocked rules must live in OMP/SYSTEM_MAP/Canonical Reference/CPS.

Capability production graph:

```text
A5 Blast-Radius Certification
  -> A6 Runtime Eligibility Arbitration
  -> B13 Metric Reliability Certification
  -> B16 Rollback Authority Certification
  -> RT2-S1 Measurement & Observability Foundation
  -> RT2-S2 Prepared World & Readiness
  -> RT2-S3 Prepared Delta / Prepared Plan
  -> RT2-S4 Governed Execution Coordination
  -> RT2-S5 Certified Concurrency
  -> RT2-S6 Engineering Recommendation / Engineering Learning
  -> OMP continuation or existing-owner backlog implementation
  -> B1/B2/B3/B4/B5/B6/B7/B8/B9/B10/B11/B12/B14/B15/B17/B18/B19/B20/B21/C1 implementation queue continuation
```

Producer / consumer matrix:

| Stage | Produced Capability | Produced Evidence | Capability Owner | Capability Consumers | Unlocked Capability | Unlocked Stage | Blocked Capability | Blocked Stage | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A5` | Blast-Radius Certification. | `class_level_blast_radius_certification`; E29 one/two/four-user historical proof consumed read-only. | OMP + blast-radius/action-class owners. | `A6`, Runtime Model, Production Maturity, OMP. | Runtime Eligibility Arbitration. | `A6` | Runtime apply, automation, authority expansion, class promotion, concurrency. | `B13+`, RT2, runtime apply. | Blast-radius evidence shape is certified, but it does not grant execution or authority. |
| `A6` | Runtime Eligibility Arbitration. | `runtime_eligibility_arbitration`; execute-or-stop gate rows. | Runtime Model + OMP + delegated policy/action-class owners. | `B13`, Runtime Model, Production Maturity, OMP. | Metric Reliability Certification. | `B13` | Positive promotion, automatic execution, authority expansion, runtime apply. | `B16+`, RT2, runtime apply. | Metric reliability can consume one canonical STOP/execute answer; A6 itself stops at authority/runtime_apply. |
| `B13` | Metric Reliability Certification. | `metric_reliability_certification`; reliable blocking recommendation evidence. | OMP + metric/promotion evidence owners. | `B16`, Production Maturity, Engineering Intelligence, OMP. | Rollback Authority Certification. | `B16` | Positive promotion, automatic rollback authority, action-class authority, runtime apply. | RT2 and runtime apply. | Rollback authority review needs reliable metric classification; B13 certifies blocking recommendations only. |
| `B16` | Rollback Authority Certification. | `rollback_authority_certification`; rollback evidence certified for authority review only. | Rollback authority/certification owners + OMP. | `RT2-S1`, Runtime Model, Engineering Intelligence, OMP. | Measurement Foundation. | `RT2-S1` | Runtime apply, automation, authority expansion, user movement, RT2-S2+. | `RT2-S2+`, runtime apply. | Measurement may safely consume rollback evidence read-only; authority is not granted. |
| `RT2-S1` | Measurement Evidence, Time Domains, Runtime Observability. | `rt2_s1_measurement_observability_foundation`; cost/time/latency/stop/lifecycle/topology fields visible or owner-mapped. | OMP + Runtime Model + measurement/read-model owners. | `RT2-S2`, `RT2-S6`, Runtime Model, Engineering Intelligence, operator dashboards as read-only surfaces. | Prepared World & Readiness. | `RT2-S2` | Desired-state delta, governed execution coordination, concurrency, recommendations, runtime apply. | `RT2-S3+`, runtime apply. | S2 can consume known measurement/observability gaps; measurement cannot decide or mutate. |
| `RT2-S2` | Prepared World, Prepared Readiness. | `rt2_s2_world_readiness_maturation`; compact state, freshness/readiness, policy gate ownership, trust/learning context. | World Model Plane + Runtime Model placement rules + OMP. | `RT2-S3`, Runtime consumption contract, `RT2-S6`, Engineering Intelligence. | Prepared Delta / Prepared Plan. | `RT2-S3` | Execution coordination, queue behavior, concurrency, authority expansion, runtime mutation. | `RT2-S4+`, runtime apply. | S3 may reference bounded current/readiness state; prepared state cannot approve or bypass gates. |
| `RT2-S3` | Prepared Delta, Prepared Execution Plan. | `rt2_s3_desired_state_delta_preparedness`; advisory desired-state delta and preview-only prepared plan. | Decision Model + existing planner/autoswitch owners + OMP. | `RT2-S4`, Runtime live-gate validation, packet/preview owners. | Governed Execution Coordination. | `RT2-S4` | Concurrency, automation, runtime queue, authority expansion, user movement. | `RT2-S5+`, runtime apply. | S4 may consume a bounded prepared plan; desired state and deltas remain advisory and non-authorizing. |
| `RT2-S4` | Governed Execution Coordination. | `rt2_s4_governed_execution_coordination`; read-only owner-mapped bounded decision-to-terminal-outcome coordination and terminal classification. | Runtime Model + existing execution owners + OMP. | `RT2-S5`, feedback/learning owners, Production Maturity, OMP. | Certified Concurrency. | `RT2-S5` | Parallelism, blast-radius expansion, automatic execution without authority. | `RT2-S6` and runtime apply. | One bounded path is owner-mapped; concurrency still needs its own proof, authority, and capacity certification. |
| `RT2-S5` | Certified Concurrency. | `rt2_s5_certified_concurrency_ladder`; serial-only read-only boundary certified and wider levels explicitly STOP_SAFE. | OMP + action-class/blast-radius/rollback/verification owners + `admin_core.autonomy_trust_acceleration`. | `RT2-S6`, Runtime execution owners, authority model, CPS, Production Maturity. | Evidence-Based Continuous Improvement. | `RT2-S6` | Runtime self-optimization, automatic recommendations, authority lowering, safety gate weakening, runtime apply, concurrency enablement. | `RT2-S6` recommendation effects and runtime apply. | Recommendations now have known safe execution limits; concurrency certification remains safety boundary, not performance-only parallelism or authority. |
| `RT2-S6` | Engineering Recommendation, Engineering Learning, Recommendation Confidence. | `rt2_s6_evidence_based_continuous_improvement`; owner-mapped recommendation to return OMP to existing backlog item `B1`. | OMP + Backlog + Production Maturity + Research Framework/Process + canonical owners + `admin_core.autonomy_trust_acceleration`. | OMP, Engineering Intelligence, future capability evolution, `B1`, Current Program State, Production Maturity. | OMP backlog continuation. | `B1`. | New roadmap, new owner, Runtime self-optimization, direct implementation without OMP, authority lowering, safety-gate weakening. | Any parallel lifecycle. | S6 output is advisory and canonically preserved; OMP now routes continuation to existing backlog item B1. |
| `B9` | Post-Admission Observation Window Verification. | `post_admission_observation_windows`; existing service observation and quality compact `5m`/`1h` windows verified after B8. | Existing recovery admission, service matrix, quality compact owners + OMP + Backlog + Production Maturity. | OMP, `B10`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Observability, Recovery Admission, Runtime Eligibility. | Recovery Slow-Start Progression. | `B10` | Runtime apply, automation, traffic admission, authority expansion, queue, synthetic evidence, user movement. | `B11+`, runtime apply. | Observation windows are verified read-only; they only unlock slow-start progression design. |
| `B10` | Recovery Slow-Start Progression. | `recovery_slow_start_progression`; staged mapping to existing recovery admission and blast-radius/action-class ladder. | Existing recovery admission, blast-radius/action-class ladder owners + OMP + Backlog + Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B11`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Recovery Admission, Runtime Eligibility, Authority Evolution. | Org/Cohort Isolation and Identity Policy Integration. | `B11` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement. | `B12+`, runtime apply. | Slow-start is defined as a read-only progression only; identity/cohort policy boundaries are now the next integration gap. |
| `B11` | Org/Cohort Identity Policy Integration. | `org_cohort_identity_policy_integration`; existing identity, org/cohort, allowed/preferred/excluded egress, exclusive group, ACL, and default isolation gates integrated read-only. | Existing planner gates, identity/policy owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B12`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Production Autonomy. | Next Action-Class Stage Certification. | `B12` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion. | `B13+`, runtime apply. | Identity/cohort policy boundaries are now visible to action-class certification; B11 does not grant authority or promote a class. |
| `B12` | Next Action-Class Stage Certification. | `next_action_class_stage_certification`; A5/A6/B13/B11 evidence consumed into a read-only stage certification gate. | Existing action-class ladder, A5/A6/B13/B11 evidence owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B14`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Blast Radius, Production Autonomy. | Service/Pool/Cohort Blast-Radius Scope. | `B14` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion, blast-radius expansion. | `B15+`, runtime apply. | B12 guarantees next-stage work consumes certification evidence and stops at authority/runtime boundaries; B14 must still model service/pool/cohort scope before any wider blast radius can exist. |
| `B14` | Service/Pool/Cohort Blast-Radius Scope. | `service_pool_cohort_blast_radius_scope`; service/user/SLA fit, B11 identity/cohort policy, A5 blast-radius certification, B12 stage certification, and autoswitch capacity/load owners consumed read-only. | Existing planner capacity/load, service/user/SLA, B11 identity/cohort, A5 blast-radius, B12 stage-certification, autoswitch dynamic blast-radius owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B15`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Blast Radius, Production Autonomy. | Containment / Forward-Fix Classification. | `B15` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion, blast-radius expansion, threshold/formula mutation. | `B16+`, runtime apply. | B14 makes blast-radius scope visible across service, pool, and cohort dimensions, but does not widen scope or grant authority; B15 may now classify containment/forward-fix outcomes through existing rollback/execution owners. |
| `B15` | Containment / Forward-Fix Classification. | `containment_forward_fix_classification`; terminal containment vs forward-fix states exposed from packet, verification, rollback, and partial-failure policy evidence. | Existing Runtime Model, execution packet, verification, rollback, partial-failure policy, RT2-S4 owners, OMP, Backlog, Production Maturity + `admin_core.operator_execution` and `admin_core.operator_execution_pipeline`. | OMP, `B17`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Rollback, Decision Explainability, Production Autonomy. | Stale-Read Reporting With Mutation Blocking. | `B17` | Runtime apply, rollback execution, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, planner replacement, threshold/formula mutation. | `B18+`, runtime apply. | B15 makes terminal containment and forward-fix outcomes visible and explainable, but does not execute rollback or grant authority; B17 may now preserve stale-read reporting while keeping mutation blocked. |
| `B17` | Stale-Read Reporting With Mutation Blocking. | `stale_read_mutation_blocking`; stale/unknown freshness visibility is preserved as reportable read-only evidence while mutation remains blocked. | Existing freshness actionability, runtime eligibility, routing readiness, truth/convergence, read-only inventory owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B18`, Current Program State, Production Maturity, Canonical Reference, Freshness, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Owner-Issued Version / Lease Pattern. | `B18` | Runtime apply, automation, mutation from stale read, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, planner replacement, threshold/formula mutation, new owner. | `B19+`, runtime apply. | B17 proves stale reads can remain visible without becoming mutation authority; B18 may now extend existing lease/version semantics where owner-issued fields already exist. |
| `B18` | Owner-Issued Version / Lease Pattern. | `owner_issued_version_lease_pattern`; owner-issued version/lease/generation/TTL/source-hash coverage exposed without changing lease behavior. | Existing execution lease, Runtime Model freshness gates, `SNAPSHOT_FAMILIES`, freshness actionability, action-class freshness windows, B17 stale-read mutation blocking, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B19`, Current Program State, Production Maturity, Canonical Reference, Freshness, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Hysteresis and State-Change-Cost Mapping. | `B19` | Runtime apply, automation, authority expansion, threshold/formula mutation, lease behavior change, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `B20+`, runtime apply. | B18 makes owner-issued currentness and identity coverage visible; B19 may now centralize existing state-change-cost vocabulary without changing formulas or authority. |
| `B19` | Hysteresis and State-Change-Cost Mapping. | `hysteresis_state_change_cost_mapping`; sticky/current bias, minimum improvement, cooldown, observation window, oscillation detection, user freeze, pair reversal, target block/quarantine, recovery thresholds, and freshness identity cost vocabulary centralized read-only. | Existing anti-flap, recovery admission, service threshold, movement-protection, autoswitch safety, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B20`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Hard-Failure Override Anti-Flap Arbitration. | `B20` | Runtime apply, automation, authority expansion, hard-failure override execution, threshold/formula mutation, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `B21+`, runtime apply. | B19 proves the existing anti-flap/state-change-cost vocabulary is centralized; B20 may now encode hard-failure override arbitration without creating a new policy owner. |
| `B20` | Hard-Failure Override Anti-Flap Arbitration. | `hard_failure_override_anti_flap_arbitration`; confirmed hard failure becomes anti-flap override candidate for authority review only, while suspected/no hard failure cannot override anti-flap. | Existing hard-failure, hard-failure policy window, anti-flap, B19 hysteresis/state-change-cost, planner/runtime eligibility owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B21`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Per-User Routing Control Mode. | `B21` | Runtime apply, automation, authority expansion, hard-failure override execution, threshold/formula mutation, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C1+`, runtime apply. | B20 proves hard-failure/anti-flap arbitration is explicit and non-authorizing; B21 may now expose user-level routing control mode without creating a new planner or owner. |
| `B21` | Per-User Routing Control Mode. | `per_user_routing_control_mode`; explicit or inferred per-user `AUTO` / `PINNED` / `MANUAL` routing control semantics are exposed read-only. | Existing user registry, group/org policy, planner gate, admin operator surface, B11 identity/cohort policy, B20 hard-failure/anti-flap arbitration, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C1`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Decision Explainability, Production Autonomy. | Fail-Open / Fail-Closed Action-Class Behavior. | `C1` | Runtime apply, automation, authority expansion, registry write, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C2+`, runtime apply. | B21 proves user-control boundaries are explicit and non-authorizing; C1 may now record action-class fail behavior without creating a new planner, registry owner, or runtime behavior. |
| `C1` | Fail-Open / Fail-Closed Action-Class Behavior. | `fail_open_fail_closed_action_class_behavior`; per-action-class fail-closed Runtime mutation/apply behavior and read-only fail-open allowance are recorded. | Existing Runtime Model, OMP, planner gates, action-class policy, B21 user mode, stale-read/lease, hard-failure arbitration, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C2`, Current Program State, Production Maturity, Canonical Reference, Runtime Eligibility, Authority Evolution, Movement Protection, Decision Explainability, Production Autonomy. | Probabilistic Suspicion Advisory Evidence. | `C2` | Runtime apply, automation, authority expansion, fail-open runtime mutation, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C3+`, runtime apply. | C1 makes stop/continue semantics explicit without authorizing execution; C2 may now constrain probabilistic suspicion as advisory-only evidence. |
| `C2` | Probabilistic Suspicion Advisory Evidence. | `probabilistic_suspicion_advisory_evidence`; shadow autonomy, source-confidence, and soft-degradation suspicion are advisory-only with direct blocking power `NONE` and direct execution power `NONE`. | Existing trust/confidence model, shadow autonomy, soft-degradation policy, OMP, read-only inventory, C1 fail-closed behavior, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C3`, Current Program State, Production Maturity, Canonical Reference, Decision Explainability, Observability, Authority Evolution, Production Autonomy. | Break-Glass Authority Audited Exceptional Operator Policy. | `C3` | Runtime apply, automation, direct suspicion blocking, authority expansion, threshold/formula mutation, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C4+`, runtime apply. | C2 makes weak/probabilistic suspicion non-authorizing; C3 may now define exceptional authority boundaries without allowing suspicion to become action authority. |
| `C3` | Break-Glass Authority Audited Exceptional Operator Policy. | `break_glass_authority_policy_contract`; break-glass is disabled-by-default, audited, exceptional operator policy only, requiring explicit operator policy, incident context, audit, verification/closure, truth/convergence, OMP, and CPS updates. | Existing OMP, operator authority, governed execution pipeline, audit/observability, feedback/closure, packet/rollback owners, Backlog, Production Maturity + `admin_core.operator_execution_pipeline`. | OMP, `C4`, Current Program State, Production Maturity, Canonical Reference, Authority Evolution, Blast Radius, Decision Explainability, Observability, Production Autonomy. | All-at-Once Promotion Unavailable Verification. | `C4` | Runtime apply, automation, silent authority expansion, all-at-once promotion, blast-radius expansion, direct class promotion, rollback/apply execution, synthetic evidence, user movement, planner replacement. | `C5+`, runtime apply. | C3 makes exceptional authority explicit and non-authorizing; C4 may now verify broad promotion remains unavailable under a non-silent authority boundary. |
| `C4` | All-at-Once Promotion Unavailable Verification. | `all_at_once_promotion_unavailable_verification`; current action classes have all-at-once/direct promotion unavailable and class-by-class authority review remains required. | Existing OMP, blast-radius/action-class gates, A5/B12/B14 evidence owners, C3 break-glass policy boundary, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C5`, Current Program State, Production Maturity, Canonical Reference, Authority Evolution, Blast Radius, Decision Explainability, Observability, Production Autonomy. | Rollback As Operational Compensation. | `C5` | Runtime apply, automation, silent authority expansion, all-at-once promotion, direct class promotion, blast-radius expansion, rollback/apply execution, synthetic evidence, user movement, planner replacement. | `C6+`, runtime apply. | C4 proves broad promotion is unavailable without authorizing anything; C5 may now preserve rollback semantics against stable authority/promotion boundaries. |

Capability graph validation:

| Check | Result | Evidence |
| --- | --- | --- |
| One producer per capability | `PASS` | Each produced capability is tied to exactly one stage in the matrix. |
| One canonical owner per capability | `PASS` | Owners are existing OMP/Runtime/Decision/workstream owners; no new owner is introduced. |
| One or more consumers per capability | `PASS` | Every row names at least one consumer. |
| No orphan capability | `PASS` | Every produced capability unlocks one stage or returns to OMP/existing owner flow. |
| No duplicated producer | `PASS` | Related concepts may be consumed later, but production belongs to one stage only. |
| No circular production | `PASS` | The graph is linear through RT2-S6, then returns to OMP continuation; it does not loop back as a producer of earlier stages. |

Current produced capability state:

| Field | Value |
| --- | --- |
| Last produced capability | Probabilistic Suspicion Advisory Evidence |
| Producer stage | `C2` |
| Produced evidence | `probabilistic_suspicion_advisory_evidence = DONE_READ_ONLY_PROBABILISTIC_SUSPICION_ADVISORY_EVIDENCE`; next step is existing backlog item `C3`. |
| Capability owner | Existing trust/confidence model, shadow autonomy, soft-degradation policy, OMP, read-only inventory, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration` |
| Current consumers | OMP, `C3`, Current Program State, Production Maturity, Canonical Reference, Decision Explainability, Observability, Authority Evolution, Production Autonomy |
| Current unlocked capability | Break-Glass Authority Audited Exceptional Operator Policy |
| Current blocked capabilities | Runtime apply, automation, direct suspicion blocking, authority expansion, threshold/formula mutation, new owner, queue daemon, planner replacement, synthetic evidence, user movement |

## 24.3 OMP Progress Dashboard Model

Status: `ACTIVE_CANONICAL_READ_ONLY`.

Owner: OMP.

Purpose:

OMP must provide a permanent read-only dashboard model so an operator can understand current project state within one minute without reading historical reports.

This dashboard model is not a Runtime, Planner, owner, truth source, roadmap, master program, capability program, authority surface, automation mode, implementation queue, or scoring engine. It consumes canonical owners only.

Dashboard audit:

| Dashboard area | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Overall OMP Progress | `EXISTS_PARTIAL` | V7 Production Status, Production Maturity, backlog progress, and CPS metrics. | Define one read-only visual grouping. |
| Current OMP State | `EXISTS_PARTIAL` | CPS current state, transition state, produced capability state. | Define mandatory current-state dashboard fields. |
| Capability Progress | `EXISTS_PARTIAL` | Capability Dashboard and CPS capability progress. | Reuse existing capability registry and status terms. |
| Capability Production Graph | `EXISTS_COMPLETE` | OMP Capability Production Contract. | Reuse graph as dashboard source. |
| RT2 Progress | `EXISTS_PARTIAL` | RT2 workstreams and CPS RT2 statuses. | Define compact S1-S6 visual status. |
| Production Maturity | `EXISTS_PARTIAL` | Production Maturity Model and CPS metrics. | Define visual score, target, remaining, and trend fields. |
| Engineering Intelligence | `EXISTS_PARTIAL` | Runtime Model, OMP lifecycle, Production Maturity, SYSTEM_MAP, CPS. | Define compact maturity view. |
| Current Stop Gates | `EXISTS_PARTIAL` | CPS stop reason, OMP stop conditions, Runtime/authority boundaries. | Define operator-visible gate list. |
| Transition Explanation | `EXISTS_COMPLETE` | OMP Capability Transition Contract. | Reuse current transition explanation in dashboard. |
| Capability Quality Future View | `MISSING` | Quality/confidence/readiness/reliability may exist per owner but not as a dashboard read-model placeholder. | Add future-ready read-only placeholder; no scoring yet. |

Dashboard source map:

| Dashboard data | Permanent source | Dashboard use |
| --- | --- | --- |
| Scheduler rules, execution order, transition explanation, production graph | OMP | Explain why current and next steps exist. |
| Current step, previous step, next step, stop reason, current metrics | Current Program State | Display volatile current state only. |
| Owner lookup | SYSTEM_MAP | Show where evidence and capabilities belong. |
| Durable conclusions | Canonical Reference | Prevent report-only dashboard knowledge. |
| Production maturity score | Production Maturity Model | Display current score, target, remaining, and trend. |
| Capability state | OMP capability registry + CPS snapshot | Display capability status without creating a second backlog. |

Visual grammar:

| Visual element | Required meaning |
| --- | --- |
| Progress bar | Shows current value against target only; it is not authority and not certification by itself. |
| Status color | Green = complete/certified, blue = current, amber = waiting/partial, red = blocked/STOP, gray = not started. |
| Capability graph | Displays producer -> produced capability -> owner -> consumers -> unlocked stage -> blocked stage. |
| Compact card | Displays one dashboard area with source owner and current state. |
| Expandable details | May reveal evidence, owner, consumers, stop reason, and source document. |

Dual-view visualization audit:

| Item | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Operator-facing project view | `EXISTS_PARTIAL` | V7 Production Status, CPS snapshot, UI Operator Surface principle. | Add Operator View contract inside the existing dashboard model. |
| Engineering trace view | `EXISTS_PARTIAL` | Capability Production Contract, Transition Contract, SYSTEM_MAP ownership lookup, Engineering Surface principle. | Add Engineering View contract inside the existing dashboard model. |
| Shared canonical data | `EXISTS_COMPLETE` | OMP, SYSTEM_MAP, CPS, Production Maturity Model, Canonical Reference. | Reuse only; no duplicated read model. |
| View synchronization rule | `MISSING` | Current dashboard says sources, but not that both views use identical data. | Add explicit synchronization rule. |
| Future-ready quality/confidence placeholders | `EXISTS_PARTIAL` | Capability Quality future view exists; Recommendation Confidence exists through RT2-S6/confidence owners. | Expose placeholders in both views without scoring. |

Dual-view rule:

1. OMP Dashboard has exactly two presentation views: `OPERATOR_VIEW` and `ENGINEERING_VIEW`.
2. Both views consume the same canonical data from OMP, SYSTEM_MAP, Current Program State, Production Maturity Model, and Canonical Reference.
3. The views may differ only by presentation density, labels, grouping, and default expansion level.
4. Neither view may duplicate state, create a read model, create a truth source, change priority, approve work, certify evidence, mutate Runtime, expand authority, create a queue, or replace Planner.
5. If the two views disagree, the dashboard must treat the mismatch as a visualization defect and resolve back to canonical owners before display.

Synchronization model:

| Shared data | Operator View presentation | Engineering View presentation | Canonical owner |
| --- | --- | --- | --- |
| Overall OMP Progress | Progress bars and status cards. | Score components, backlog counts, maturity source. | OMP + CPS + Production Maturity Model. |
| Current Step / Previous Step / Next Step | Simple current-state card. | Transition contract row with evidence and blockers. | CPS + OMP. |
| Current Production Maturity | One score, target, trend. | Score inputs, target, remaining, next milestone. | Production Maturity Model + CPS. |
| RT2 stage | Compact S1-S6 progress. | RT2 workstream table, owners, inputs, outputs, consumers. | OMP + CPS. |
| Engineering Intelligence stage | Compact maturity strip. | EI ownership lookup, lifecycle, validation/adaptation status. | Runtime Model + OMP + SYSTEM_MAP + CPS. |
| Stop Gates | Red/amber gate cards with reason. | Gate owner, evidence, stop condition, blocked capability. | OMP + Runtime Model + CPS. |
| Produced / Unlocked / Blocked Capability | Simple capability graph. | Capability Production Graph and producer/consumer matrix. | OMP + SYSTEM_MAP + CPS. |
| Current Risks | Short risk cards. | Evidence gaps, blockers, owners, canonical references. | CPS + OMP + Canonical Reference. |
| Current Recommendation | Plain recommendation card. | Recommendation evidence, owner, confidence placeholder, consumers. | OMP + RT2-S6 + CPS. |
| Capability Quality future fields | Placeholder chips only. | Owner-mapped placeholder table. | Existing future read-model owners through SYSTEM_MAP. |

Operator View contract:

| Area | Required display | Default presentation |
| --- | --- | --- |
| Overall OMP Progress | Architecture, Tier A, Tier B, RT2, Engineering Intelligence, Overall Progress, Production Maturity. | Progress bars and compact cards. |
| Current Step | Current Step, Previous Step, Next Step, Reason. | One current-state card with expandable detail. |
| Current Production Maturity | Current score, target, remaining, trend. | Progress bar and milestone label. |
| Current RT2 stage | S1-S6 status. | Compact stage strip. |
| Current Engineering Intelligence stage | Observation, Process, Time, Recommendation, Validation, Adaptation. | Compact maturity strip. |
| Current Stop Gates | Runtime Apply, Automation, Authority, User Movement, Planner, Queue, Concurrency, Desired State. | Color-coded gate cards. |
| Capability state | Current Produced Capability, Current Unlocked Capability, Current Blocked Capability. | Simple capability graph. |
| Current Risks | Active stop risks and forbidden later steps. | Short risk cards. |
| Current Recommendation | Current OMP recommendation and required action. | Plain-language recommendation card. |
| Expandable details | Source owner, evidence pointer, blocker reason. | Hidden by default. |

Operator View principles:

1. Minimal.
2. Fast.
3. Visually understandable.
4. Uses progress bars, cards, color coding, and a simple capability graph.
5. No engineering noise by default.
6. Every card can expand to show its source owner.

Engineering View contract:

| Area | Required display | Default presentation |
| --- | --- | --- |
| Capability Graph | Current capability dependency graph. | Expanded graph. |
| Capability Production Graph | Stage -> Produced Capability -> Owner -> Consumers -> Unlocked Stage -> Blocked Stage. | Full production graph. |
| Producer / Consumer Matrix | Producer, produced evidence, owner, consumers, blockers. | Full matrix. |
| Transition Contracts | Why next step is available and why later steps remain blocked. | Full transition rows. |
| Capability Contracts | Capability status, DoD, remaining criteria, reopen triggers. | Traceable tables. |
| Capability Quality future-ready | Quality, Confidence, Readiness, Reliability, Recommendation Confidence. | Placeholder table; no scoring. |
| Owner Mapping | Canonical owner, existing read owners, forbidden ownership. | SYSTEM_MAP links. |
| Engineering Intelligence | Observation, Process, Time, Recommendation, Validation, Adaptation. | Owner and lifecycle trace. |
| RT2 Workstreams | Purpose, owners, inputs, outputs, consumers, criteria, evidence. | Full workstream rows. |
| Dependency Graph | Produced capability, consumed evidence, blocked future capabilities. | Expanded dependency view. |
| Current Evidence | Current produced evidence and consumers. | Evidence trace table. |
| Current Blockers | Stop gates, blocked capabilities, unsafe later steps. | Blocker matrix. |

Engineering View principles:

1. Complete.
2. Traceable.
3. Explainable.
4. Evidence based.
5. Every displayed field must point back to OMP, SYSTEM_MAP, CPS, Production Maturity Model, Canonical Reference, or an existing owner named by those documents.

Dashboard sections:

| Section | Required display | Canonical source |
| --- | --- | --- |
| Overall OMP Progress | Architecture, Tier A, Tier B, RT2, Engineering Intelligence, Overall Progress, Production Maturity. | OMP + CPS + Production Maturity Model. |
| Current OMP State | Current Step, Previous Step, Next Step, Reason, Current Stop, Current Capability Produced, Current Capability Consumed. | CPS + OMP transition/production contracts. |
| Capability Progress | Status for each major capability: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `BLOCKED`, `WAITING`, `CERTIFIED`, `CONSUMED`. | OMP capability registry + CPS. |
| Capability Production Graph | Stage -> Produced Capability -> Capability Owner -> Consumers -> Unlocked Stage -> Blocked Stage. | OMP Capability Production Contract + SYSTEM_MAP. |
| RT2 Progress | `RT2-S1` through `RT2-S6` and current maturity. | OMP RT2 workstreams + CPS. |
| Production Maturity | Current score, target score, remaining score, latest trend, next milestone. | Production Maturity Model + CPS. |
| Engineering Intelligence | Observation, Process, Time, Recommendation, Validation, Adaptation, current maturity. | Runtime Model + OMP + Production Maturity + CPS. |
| Current Stop Gates | Runtime Apply, Automation, Authority, User Movement, Planner, Queue, Concurrency, Desired State, and why each is blocked or open. | OMP stop rules + Runtime Model + CPS. |
| Transition Explanation | Current stage -> Produced capability -> Why next stage unlocked -> Why later stages remain blocked. | OMP Capability Transition Contract. |
| Capability Quality Future View | Capability Quality, Confidence, Readiness, Reliability as reserved read-model fields only. | Future existing-owner read models; no score until certified. |

Current dashboard snapshot:

| Area | Current display |
| --- | --- |
| Architecture | `[##########] 100% COMPLETE` |
| Tier A | `[##########] 6 / 6 COMPLETE` |
| Tier B | `[##########] 21 / 21 COMPLETE` |
| RT2 | `[##########] 6 / 6 COMPLETE_READ_ONLY` |
| Engineering Intelligence | `[########--] FINAL_CANONICAL_STATE / implementation evidence future` |
| Overall actionable backlog | `31 / 34 complete` |
| Production Maturity | `[######----] 64.3 / 100; target 100; remaining 35.7` |
| Current step | `C5_PRESERVE_ROLLBACK_AS_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK` |
| Previous step | `C4_ALL_AT_ONCE_PROMOTION_UNAVAILABLE_FOR_CURRENT_ACTION_CLASSES` |
| Reason current step is available | C4 produced all-at-once promotion unavailable evidence without granting runtime/class authority, enabling C5 to preserve rollback semantics against stable authority boundaries. |
| Current stop | `NONE_FOR_C5_ROLLBACK_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK` |

RT2 dashboard:

| Workstream | Status | Current maturity | Dashboard note |
| --- | --- | --- | --- |
| `RT2-S1` | `DONE_READ_ONLY` | Complete | Measurement/observability visible or owner-mapped. |
| `RT2-S2` | `DONE_READ_ONLY` | Complete | Prepared world/readiness is read-only and non-authorizing. |
| `RT2-S3` | `DONE_READ_ONLY` | Complete | Desired-state delta remains advisory. |
| `RT2-S4` | `DONE_READ_ONLY` | Complete | Governed coordination is owner-mapped without queue creation. |
| `RT2-S5` | `DONE_READ_ONLY` | Complete | Wider concurrency remains STOP_SAFE. |
| `RT2-S6` | `DONE_READ_ONLY` | Complete | Recommendation returns OMP to `B1`; advisory only. |

Engineering Intelligence dashboard:

| Capability | Current maturity | Source |
| --- | --- | --- |
| Observation | `MEASURED_PARTIAL` | `RT2-S1`, existing observation/read-model owners. |
| Process | `UNDERSTOOD_EXPRESSED` | Runtime Model + Work Placement + Decision Lifecycle + OMP. |
| Time | `CANONICALIZED_INSIDE_RT2` | Runtime Model + `RT2-S1` + `RT2-S6`. |
| Recommendation | `MATERIALIZED_ADVISORY` | `RT2-S6` + OMP + Backlog. |
| Validation | `UNDERSTOOD_PARTIAL_VALIDATION` | Engineering Intelligence Phase 2 owners. |
| Adaptation | `ADAPTIVE_ENGINEERING_READY_IMPLEMENTATION_FUTURE` | Engineering Intelligence Phase 3 owners. |

Current stop gates dashboard:

| Gate | Display status | Why |
| --- | --- | --- |
| Runtime Apply | `BLOCKED` | No runtime apply authority or certification is active. |
| Automation | `BLOCKED` | Production autonomy is not certified. |
| Authority | `BLOCKED` | No authority expansion is active. |
| User Movement | `BLOCKED` | No approved packet or movement authority is active. |
| Planner | `BLOCKED` | Existing planner/autoswitch owners remain; no replacement is allowed. |
| Queue | `BLOCKED` | No queue daemon or hidden retry engine is certified. |
| Concurrency | `BLOCKED` | Current certified boundary is serial-only/read-only. |
| Desired State | `ADVISORY_ONLY` | Desired state and deltas cannot authorize movement or mutate Runtime. |

Capability quality future view:

| Field | Current status | Rule |
| --- | --- | --- |
| Capability Quality | `RESERVED_READ_MODEL_ONLY` | No score until an existing owner produces certified quality evidence. |
| Capability Confidence | `RESERVED_READ_MODEL_ONLY` | May display existing confidence only; cannot become authority. |
| Capability Readiness | `RESERVED_READ_MODEL_ONLY` | May display readiness from canonical owners only. |
| Capability Reliability | `RESERVED_READ_MODEL_ONLY` | May display reliability after verification/certification evidence exists. |

Dashboard rules:

1. Dashboard is read-only.
2. Dashboard consumes canonical owners only.
3. Dashboard cannot decide, approve, rank implementation, mutate Runtime, certify evidence, expand authority, create a queue, create a planner, create a roadmap, or become a truth source.
4. Dashboard status must name its source owner.
5. Dashboard may show future-ready placeholders only as `RESERVED_READ_MODEL_ONLY`; placeholders cannot affect OMP priority or authority.
6. Engineering reports may record dashboard audit evidence, but the dashboard model must live in OMP and the current snapshot must live in Current Program State.
7. Deleting the engineering report must not remove any important dashboard structure, ownership rule, current state field, or durable conclusion.

### Dashboard UI Foundation Contract

Status: `ACTIVE_CANONICAL_UI_FOUNDATION`.

Owner: OMP.

Purpose:

The OMP Dashboard is the canonical V7 OMP section inside the admin panel. It lives behind the separate top-level admin navigation item `OMP` and route `/admin/omp`; it does not replace the existing admin home / overview screen. Inside the OMP tab, Executive View is the top layer, followed by synchronized Operator View and Engineering View, all from the same canonical data.

The UI foundation is not dashboard implementation code, a Runtime, Planner, owner, truth source, roadmap, scoring engine, authority surface, automation surface, queue, or implementation path.

UI discovery audit:

| Existing UI/read-model area | Classification | Reuse decision | Dashboard role |
| --- | --- | --- | --- |
| Existing admin Overview / dashboard schema | `EXISTS_PARTIAL` | Reuse read-only summary, health, route, service, and alert patterns from `admin_core.overview_views` and `v7.admin.dashboard.v1`. | Existing admin home / overview remains unchanged; OMP is a separate top-level tab. |
| Existing admin navigation | `EXISTS_UNDER_OTHER_NAME` | Reuse simple top-level sections and one-click section switching. | Add/reuse top-level `OMP` tab; do not create a second shell or replace the home screen. |
| Existing Operator surfaces | `EXISTS_PARTIAL` | Reuse recommendation, evidence, blocker, drawer, and progressive-disclosure patterns from operator view/decision/observability surfaces. | Operator View language and expandable details. |
| Existing Execution surfaces | `EXISTS_PARTIAL` | Reuse governed execution, packet, lease, rollback, evidence, and terminal-state trace as details. | Engineering View trace links only; no execution control. |
| Existing Health / Checks / Runtime read views | `EXISTS_PARTIAL` | Reuse read-only health, runtime-summary, service, route, and diagnostic contracts. | Drill-down evidence panels and stop-gate explanations. |
| Existing design HTML dashboards | `EXISTS_UNDER_OTHER_NAME` | Reuse layout vocabulary only: top navigation, compact metrics, status chips, cards, tables, alerts, topology, responsive grid. | Visual reference only; no state, owner, or implementation truth. |
| OMP Dashboard Model and Dual-View Model | `EXISTS_COMPLETE` | Reuse as canonical dashboard data contract and presentation split. | Permanent model for the OMP tab. |
| Canonical OMP navigation rule | `MISSING` | Add inside OMP. | `OMP_DASHBOARD` is a separate top-level admin section, not the global home page. |

OMP tab rule:

1. The existing V7 admin home / overview page remains unchanged.
2. `OMP_DASHBOARD` is reached through the top-level `OMP` admin tab and route `/admin/omp`.
3. Executive View is the first layer inside the OMP tab.
4. Operator View and Engineering View are synchronized modes on the same OMP page, not separate sources, read models, or dashboards.
5. Existing Overview, Health, Operator, Routing, Users, Channels, Checks, Execution, Logs, Settings, and Security surfaces keep their existing navigation meaning and may be drill-down destinations.
6. A secondary surface may display domain-specific state only from its existing owner; it must not override OMP Dashboard state.
7. If a secondary surface and OMP Dashboard disagree, the disagreement is a visualization/data wiring defect and must resolve back to canonical owners.

Dashboard hierarchy:

| Layer | UI responsibility | Required content | Source |
| --- | --- | --- | --- |
| App shell | Provide stable navigation. | Existing home / overview remains default; top-level `OMP` tab opens `/admin/omp`; drill-downs reuse existing admin sections. | OMP + SYSTEM_MAP. |
| Page header | Show current program identity inside OMP tab. | V7, Product Execution Mode, current step, Executive/Operator/Engineering view toggle, source timestamp, read-only badge. | CPS + OMP. |
| Operator summary band | One-minute status. | Overall progress, Production Maturity, RT2, Engineering Intelligence, current step, next step, stop gates. | CPS + OMP + Production Maturity. |
| Current work area | Explain why now. | Previous/current/next step, reason, produced capability, consumed capability, unlocked capability, blocked capability, recommendation, risk. | OMP transition/production contracts + CPS. |
| Capability visual area | Show system flow. | Simple capability graph in Operator View; full production/dependency graph in Engineering View. | OMP + SYSTEM_MAP. |
| Detail drawer / expandable rows | Preserve traceability without noise. | Owner, evidence, consumers, blockers, source document, related report, current verification state. | SYSTEM_MAP + CPS + Canonical Reference + existing owners. |

Operator View UI foundation:

| Region | Required widgets | Rule |
| --- | --- | --- |
| Status strip | Production Maturity indicator, current step badge, read-only badge, stop-gate summary. | Must fit one scan; no raw engineering tables by default. |
| Progress row | Overall OMP progress, Tier A/B/C, RT2, Engineering Intelligence, backlog completion. | Progress bars only; progress is not authority. |
| Current work card | Previous step, current step, next step, reason current step is available. | Plain operator language. |
| Capability card | Produced, consumed, unlocked, blocked capability. | Simple graph or stacked cards. |
| Stop gates | Runtime Apply, Automation, Authority, User Movement, Planner, Queue, Concurrency, Desired State. | Red/amber/blue/green/gray status colors with reason. |
| Recommendation / risk cards | Current recommendation, current risks, why later steps remain forbidden. | Short by default; expandable details. |
| Drill-down links | Operator, Execution, Health, Evidence, Canonical owner. | One click from the card; no duplicated state. |

Engineering View UI foundation:

| Region | Required widgets | Rule |
| --- | --- | --- |
| Capability graph | Capability dependency graph and current position. | Trace every node to owner. |
| Production graph | Stage -> produced capability -> owner -> consumers -> unlocked stage -> blocked stage. | Reuse OMP Capability Production Contract. |
| Producer / consumer matrix | Producer, evidence, consumers, blockers, owner. | Full trace table. |
| Transition contracts | Why next step is available; why later steps remain blocked. | Reuse OMP Capability Transition Contract. |
| RT2 / Engineering Intelligence | Workstream and EI maturity details. | Read-only/advisory boundaries visible. |
| Evidence and blocker panes | Produced evidence, consumed evidence, stop gates, missing proof. | Link to existing reports/owners; no synthetic evidence. |
| Owner mapping | Canonical owner and existing read owners. | SYSTEM_MAP owns lookup. |
| Future quality placeholders | Quality, confidence, readiness, reliability, recommendation confidence. | `RESERVED_READ_MODEL_ONLY`; no scoring. |

Navigation model:

| Navigation target | User meaning | Source rule |
| --- | --- | --- |
| `OMP` | See complete project state and current OMP step. | Top-level admin tab at `/admin/omp`; consumes canonical owners only and does not replace existing home. |
| `Current Step` | Jump to current backlog/work item context. | CPS current step + OMP. |
| `Current Report` | Open latest relevant Engineering Report as evidence. | Report is evidence only. |
| `Canonical Owner` | Open the document that owns the displayed rule. | SYSTEM_MAP + Canonical Reference. |
| `Evidence` | Open evidence, tests, or read-only payload behind a card. | Existing evidence/read-model owner. |
| `Operator` | Open operator-facing recommendation/workflow details. | Existing operator surfaces. |
| `Execution` | Open governed execution/packet trace when relevant. | Existing execution owners; no apply control from dashboard. |
| `Health / Read Models` | Open health, route, service, runtime, and diagnostic details. | Existing read-only owners. |

Visual foundation:

| Component | Required use | Forbidden use |
| --- | --- | --- |
| Progress bar | Show percent/count against canonical target. | Authority, certification, or hidden scoring. |
| Timeline | Show previous/current/next OMP stage. | New roadmap or alternate queue. |
| Stage card | Show one OMP capability/stage with owner and status. | Duplicated backlog item. |
| Badge/chip | Show status, owner, gate, or maturity. | Substitute for evidence. |
| Capability graph | Explain producer/consumer/unlock/block flow. | Planner or dependency executor. |
| Producer -> consumer graph | Show traceability. | Automation trigger. |
| Stop-gate indicator | Show why something is blocked/open. | Gate decision or authority change. |
| Expandable detail | Show source, evidence, owner, blockers. | Hide missing ownership. |
| Charts | Reserved for later implementation. | Do not implement or require charts in this task. |

UX principles:

1. Modern engineering platform: calm, fast, readable, sparse, and high signal.
2. Operator View is minimal and beautiful enough to understand in one minute.
3. Engineering View is complete, traceable, and evidence based.
4. Both views use identical canonical data.
5. No duplicated widgets when a single shared widget can change presentation density.
6. No duplicated read model, state, truth, score, priority, or authority.
7. Default view hides engineering noise but keeps one-click traceability.
8. Dashboard is read-only and must visibly say so.
9. Charts are not part of this foundation; only the UI model is canonicalized.
10. Existing admin surfaces remain useful, and the OMP Dashboard is a separate top-level admin section rather than the home screen.

### Dashboard Design System

Status: `ACTIVE_CANONICAL_DESIGN_SYSTEM`.

Owner: OMP.

Purpose:

The Dashboard Design System defines the permanent visual language for future OMP Dashboard implementation. It does not implement UI, React, HTML, Runtime behavior, OMP logic, new read models, new data models, new authority, or new architecture.

Dashboard philosophy:

The dashboard must answer immediately:

1. Where are we?
2. Why are we here?
3. What is blocked?
4. What was produced?
5. What comes next?
6. Why?
7. What changed today?
8. What is the current maturity?

Reference-product research:

| Reference | Reuse for V7 | Avoid for V7 |
| --- | --- | --- |
| Linear | Focused workspace, restrained density, keyboard-fast feel, low visual noise, elegant status language. | Ambiguous beauty without explicit evidence trace. |
| GitHub Projects | Multiple synchronized views over the same underlying items: table, board, roadmap, filters, fields. | Turning view configuration into a second planning system. |
| Stripe Dashboard | Clear home surface, sidebar navigation, search/command access, strong hierarchy, operational polish. | Business-metric cards that imply authority without evidence. |
| Datadog | Dashboard purpose, widgets, grouping, drill-down, operational status visualization. | Metric overload, duplicated dashboards, noisy wallboards. |
| Grafana | Time-series/dashboard discipline, panels, variables, reusable views, drill-down by data source. | Chart-first UI before V7 has certified chart read models. |
| Apple HIG / modern macOS / modern iOS | Clarity, hierarchy, spacing, legibility, calm color, accessible targets, dark/light mode quality. | Decorative motion, low contrast, tiny hit targets, excessive translucency. |

V7 visual language:

| Dimension | Canonical rule |
| --- | --- |
| Tone | Calm, precise, production-grade, minimal, not decorative. |
| Density | Operator View is sparse; Engineering View is dense but structured. |
| Typography | Large readable headings, compact labels, numeric emphasis only for canonical metrics. |
| Spacing | Consistent 8px rhythm; card interiors breathe; engineering tables remain scan-friendly. |
| Radius | Small radius, preferably `6-8px`; no large bubbly cards. |
| Color | Soft semantic palette: green complete, blue current/info, amber waiting/risk, red blocked/STOP, gray inactive. |
| Dark mode | First-class, low-glare, high-contrast text, restrained borders, no heavy gradients. |
| Light mode | First-class, quiet background, clear cards, same semantic colors. |
| Icons | Use simple recognizable icons for status/navigation when implemented; text labels remain required for safety-critical status. |
| Motion | Minimal and functional only: expansion, focus, selection, graph highlight. |
| Visual noise | No decorative blobs, no chart clutter, no duplicated widgets, no irrelevant metrics. |

Dashboard layout system:

| Surface | Layout |
| --- | --- |
| Operator Home Screen | Header + status strip + progress row + current stage card + stop-gate/risk row + simple capability graph + expandable details. |
| Engineering View | Header + graph/matrix split + transition/production contracts + RT2/EI panels + evidence/blocker/owner tables + expandable technical detail. |
| Capability Graph | Left-to-right flow: stage -> produced capability -> owner -> consumers -> unlocked stage -> blocked stage. |
| Production Maturity | One large maturity indicator with target, remaining, next milestone, and source owner. |
| RT2 Progress | Six-stage horizontal strip with complete/current/blocked markers and workstream detail expansion. |
| Engineering Intelligence | Six-part maturity strip: Observation, Process, Time, Recommendation, Validation, Adaptation. |
| Current Stage | Timeline card: previous -> current -> next, plus why current is available. |
| Current Stop Gates | Grid of gate cards with status, reason, owner, and blocked capability. |

Operator Home Screen conceptual mockup:

```text
V7 / OMP Dashboard                                      READ ONLY
Product Execution Mode             Operator View | Engineering View

[Production Maturity 64.3/100] [Current: C5] [RT2 Complete] [EI Canonical]

Overall Progress
Architecture [##########]  Tier A [##########]  Tier B [######----]
RT2          [##########]  Backlog [######----] Production [#####-----]

Current Stage
C4 completed -> C5 current -> Continue OMP after evidence/report/canonical update
Why now: C4 produced owner-mapped all-at-once promotion unavailable verification evidence.

Capability
Produced: Probabilistic Suspicion Advisory Evidence
Consumed by: C3 break-glass authority audited exceptional operator policy
Unlocked: Break-Glass Authority Audited Exceptional Operator Policy
Blocked: Runtime apply, automation, authority, queue, concurrency, registry write, user movement, new owner

Stop Gates
[BLOCKED Runtime Apply] [BLOCKED Automation] [BLOCKED Authority] [BLOCKED User Movement]
[BLOCKED Planner] [BLOCKED Queue] [BLOCKED Concurrency] [ADVISORY Desired State]

Recommendation
Execute C3 through existing OMP, operator authority, documentation, and canonical update owners.
```

Engineering View conceptual mockup:

```text
V7 / OMP Dashboard                                      READ ONLY
Engineering View

Capability Production Graph
B12 -> Next Action-Class Stage Certification -> existing action-class ladder/A5/A6/B13/B11 evidence owners
   -> consumers: OMP, B14, CPS, Production Maturity, Canonical Reference
   -> unlocks: B14
   -> blocks: runtime apply, automation, authority expansion, queue, user movement, direct class promotion, blast-radius expansion

Producer / Consumer Matrix
| Producer | Evidence | Owner | Consumers | Unlocked | Blocked |

Transition Contract
Why C3 is available: C2 evidence is read-only, owner-mapped, tested, and safe to consume.
Why later steps remain forbidden: no runtime apply, authority, registry write, concurrency, planner replacement, user movement, or new-owner proof.

Panels
[RT2 S1-S6] [Engineering Intelligence] [Production Maturity] [Stop Gates]
[Evidence] [Canonical Owners] [Risks] [Expandable Technical Detail]
```

Component design:

| Component | Visual rule | Interaction |
| --- | --- | --- |
| Progress bar | Thin, labeled, source-owned, no hidden formula. | Hover/focus shows source and last update. |
| Timeline | Previous/current/next only by default. | Click current opens transition detail. |
| Capability card | Status, owner, produced/consumed/unlocked/blocked. | Expand for evidence and consumers. |
| Capability graph | Simple in Operator View; full in Engineering View. | Select node to show owner/evidence/details. |
| Stage graph | Horizontal OMP/RT2 stage flow. | Click stage opens workstream/contract detail. |
| Dependency graph | Engineering-only by default. | Filter by owner, blocker, consumer. |
| Status badge | Semantic color plus text. | Never color-only. |
| Maturity indicator | Score, target, remaining, next milestone. | Expand to category breakdown. |
| Risk indicator | Amber/red card with reason and owner. | Expand to mitigation/blocked capability. |
| Stop Gate card | Gate status, reason, owner, blocked capability. | Expand to rule/evidence. |
| Engineering card | Dense trace card with owner and source. | Expand/collapse technical details. |
| Recommendation card | Plain-language recommendation plus safety boundary. | Expand for evidence/confidence placeholder. |
| Expandable section | Progressive disclosure. | Default closed unless current blocker. |

Interaction model:

1. Default view is `OPERATOR_VIEW`.
2. `ENGINEERING_VIEW` is a mode switch, not a new page or data source.
3. Every card supports one-click drill-down to owner/evidence when implemented.
4. Search is global across current step, capability, owner, evidence, gate, report, and canonical reference.
5. Filters exist only in Engineering View by default: owner, status, stage, blocker, consumer, evidence type.
6. Timeline interaction shows previous/current/next; deeper history is an expansion.
7. Capability graph interaction highlights producer, produced capability, owner, consumers, unlocked stage, and blocked stages.
8. Mobile adaptation stacks status strip, current stage, stop gates, and recommendation first; graph becomes scrollable/summary-first.
9. Keyboard access and visible focus are required in future implementation.
10. Dashboard interactions cannot mutate Runtime, approve work, rank implementation, or change authority.

Design Do / Do Not:

| Do | Do not |
| --- | --- |
| Use clear hierarchy, calm contrast, compact status language. | Create decorative hero/marketing UI. |
| Show source owner for every important field. | Present unsourced numbers. |
| Prefer progress bars, timelines, cards, badges, and simple graphs. | Require charts before chart read models exist. |
| Use progressive disclosure. | Dump full engineering tables into Operator View. |
| Preserve identical data across both views. | Duplicate state, truth, read models, or widgets. |
| Make blocked state explicit. | Hide STOP gates behind green progress. |
| Keep dark and light modes equally polished. | Treat dark mode as an afterthought. |

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

## 28. Runtime Capability Maturation Program / RT Phase 2

Status: `DISCOVERED_VALIDATED_REFINED_NOT_IMPLEMENTED`.

Canonical name:

```text
Runtime Capability Maturation Program
```

Alias:

```text
RT Phase 2
```

Purpose:
Mature existing runtime capabilities through OMP without creating a new Runtime, Planner, World Model, Truth Source, Owner, Backlog, roadmap, dashboard authority, queue daemon, or automation path.

Current execution order remains:

```text
A5 -> A6 -> B13 -> B16 -> Runtime Capability Maturation Program
```

RT2 execution must not begin until OMP proves all entry criteria below.
The entry chain is complete or explicitly scoped through A5/A6/B13/B16. RT2-S1 through RT2-S6 are complete as read-only/advisory owner-mapped surfaces. RT2 produced an owner-mapped recommendation to return OMP to existing backlog item `B1_AGGREGATE_LIVENESS_EVIDENCE_BY_SOURCE_FAMILY_AND_CONFIDENCE`.

### 28.1 Entry Criteria

| Criterion | Required state |
| --- | --- |
| A5 | Class-level blast-radius evidence beyond one-user guard complete. |
| A6 | Runtime eligibility arbitration complete. |
| B13 | Metric reliability for promotion recommendations certified. |
| B16 | Automatic rollback authority after reliable verification evidence certified or explicitly scoped. |
| Runtime automation | Still disabled until explicit authority/certification exists. |
| Authority | No silent expansion; required class/policy/blast authority explicitly approved. |
| Measurement readiness | Runtime cost and reaction-latency measurement owners available through existing read models. |
| Safety readiness | Freshness, authority, verification, rollback, blast radius, anti-flap, and STOP_SAFE gates preserved. |
| Owner reuse | Existing owners cover the work; Need New Owner remains `FALSE`. |

### 28.2 Stop Conditions

RT2 must stop at the existing OMP stop conditions:

1. `OPERATIONAL_AUTHORITY`
2. `ENGINEERING_AUTHORITY`
3. `REAL_WORLD_LIMIT`
4. `UNSAFE_IMPLEMENTATION`
5. `FUNDAMENTAL_ARCHITECTURE_GAP`

Additional RT2-specific stop rules:

- stop if a workstream requires a new runtime/planner/truth-source/owner before reuse is proven impossible;
- stop if a queue, dashboard, desired-state artifact, latency metric, or improvement recommendation starts granting authority;
- stop if automation, concurrency, blast-radius expansion, or runtime behavior change is requested without certification and explicit authority;
- stop if evidence is synthetic or not tied to observed outcomes.

### 28.3 Workstreams

| Workstream | Purpose | Existing owners | Inputs | Outputs | Consumers | Completion criteria | Safety gates | Evidence requirements | Report requirements | Canonical promotion rule | Next OMP step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RT2-S1` Measurement & Observability Foundation | Make runtime cost, runtime time, reaction latency, stop reasons, lifecycle, wait states, dependency topology, Time-To-Safe-Recovery, and bottlenecks visible without hot-path cost. | OMP, Runtime Model, `admin_core/runtime_read_views.py`, `admin_core/operator_execution_pipeline.py`, `admin/v7-admin-api`, `admin_core/autonomy_trust_acceleration.py`. | Execution contracts, events, planner durations, read models, CPS, truth/convergence, existing timestamps, duration fields, latency fields, and blocker/wait reasons. | Read-only measurement, topology explanation, and dashboard payloads. Current implementation surface: `rt2_s1_measurement_observability_foundation`. | OMP, Engineering Reports, Runtime Model, Production Maturity, operator dashboards as read-only surfaces. | `DONE_READ_ONLY`; required latency/cost/time/topology fields are visible or explicitly marked missing with owner. | Dashboard/read model cannot decide, approve, rank execution, certify, or mutate. | Existing event/contract/read-model fields; no synthetic metrics. | Engineering report with Latency Impact, Work Placement, Runtime Cost Review, and Time Topology owner mapping when applicable. | Durable measurement semantics go to Runtime Model/OMP; UI field meaning goes to SYSTEM_MAP only if ownership changes. | `RT2-S2` is unlocked; S3+ remain blocked until S2 evidence exists. |
| `RT2-S2` World & Readiness Maturation | Mature prepared world/readiness state for runtime consumption. | World Model Plane, `admin_core/intelligence_snapshots.py`, `admin_core/intelligence_workers.py`, `admin_core/runtime_read_views.py`, `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py`. | Observation, snapshots, freshness, service matrix, quality compact, user/channel/policy state. | Fresh/bounded prepared state and readiness summaries. Current implementation surface: `rt2_s2_world_readiness_maturation`. | Runtime consumption contract, planner/autoswitch owners, decision surface, OMP readiness review. | `DONE_READ_ONLY`; Runtime can consume compact state as READY/STOP; live gates remain live. | Prepared state cannot approve movement or authority. | Freshness and source hashes from existing owners. | Report freshness/readiness owners and stale behavior. | Durable state semantics to Runtime Model; ownership lookup to SYSTEM_MAP. | `RT2-S3` is unlocked; S4+ remain blocked until S3 evidence exists. |
| `RT2-S3` Desired-State Delta Preparedness | Prepare bounded deltas from current state toward Desired Safe State through existing planner owners. | Product Specification, policies, Decision Model, Runtime Model, `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py`, OMP. | Business Objectives, policies, current state, action-class certification, movement protection. | Advisory desired-state delta / prepared plan. Current implementation surface: `rt2_s3_desired_state_delta_preparedness`. | Existing planner/autoswitch, packet/preview owners, Runtime live-gate validation, OMP. | `DONE_READ_ONLY`; delta is bounded, explainable, owner-mapped, and non-authorizing. | Desired State cannot become authority, planner, or runtime mutation. | Decision freshness, policy basis, gate status, real outcome requirements. | Report decision semantics and owner reuse. | Decision semantics to Decision Model; execution rules remain Runtime/OMP. | `RT2-S4` is unlocked; S5+ remain blocked until S4 evidence exists. |
| `RT2-S4` Governed Execution Coordination | Mature the bounded decision-to-terminal-outcome path. | `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py`, `tools/v7-governed-canary-dry-run-cycle`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_feedback.py`. | Prepared plan, packet, lease, restore barrier, verification plan, rollback/no-rollback state. | Idempotent governed execution coordination and terminal classification. Current implementation surface: `rt2_s4_governed_execution_coordination`. | Feedback/learning owners, OMP, CPS, Runtime Model execution contract. | `DONE_READ_ONLY`; one bounded action path is owner-mapped from packet/recheck/restore/apply/verify/rollback/feedback/closure without stale loops or new execution path. | Queue is not created; every live action would still revalidate gates and require explicit authority. | Lease, packet identity, verification, rollback/no-rollback, feedback, terminal classification. | Report terminal state, STOP_SAFE, rollback and learning paths. | Durable execution contract to Runtime Model/OMP; no new execution path. | `RT2-S5` is unlocked; S6+ remain blocked until S5 evidence exists. |
| `RT2-S5` Certified Concurrency Ladder | Certify safe levels beyond one action only when evidence supports it. | OMP, action-class ladder, Policy 006, A5/A6/B13/B16 owners, `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`. | Blast-radius evidence, rollback capacity, verification capacity, policy scope, authority envelope, anti-flap state. | Certified concurrency level or STOP_SAFE. Current implementation surface: `build_rt2_s5_certified_concurrency_ladder`. | Runtime execution owners, authority model, CPS, Production Maturity, operator approval surface. | `DONE_READ_ONLY`; current certified level is `SERIAL_ONLY_READ_ONLY`, wider levels are explicit `STOP_SAFE`, and no silent blast expansion exists. | Parallelism is safety certification, not performance optimization; concurrency enablement remains forbidden without explicit authority. | Real outcomes, capacity/load, rollback, verification, metric reliability, authority. | Report class, level, proof, limits, and stop condition. | Certification results go through OMP/Current Program State; no backlog fork. | `RT2-S6` is unlocked; runtime apply/concurrency enablement remain blocked. |
| `RT2-S6` Evidence-Based Continuous Improvement | Convert measured evidence into OMP-owned recommendations, including Runtime Time Intelligence recommendations that reduce safe recovery time. | OMP, Backlog, Production Maturity Model, Engineering Reports, Research Framework/Process, Canonical Reference, `admin_core/autonomy_trust_acceleration.py`. | Outcomes, reports, latency/cost/time/topology data, fit analysis, maturity gaps, RT2-S5 safe execution limits. | Owner-mapped recommendations or explicit no-change verdict. Current implementation surface: `build_rt2_s6_evidence_based_continuous_improvement`. | OMP optimizer, Backlog, Canonical Reference, Research Framework, Current Program State. | `DONE_READ_ONLY`; recommendation is owner-mapped to existing backlog item `B1` and remains advisory. | Recommendations cannot mutate runtime, expand authority, lower gates, create synthetic evidence, convert latency metrics into authority, or start direct implementation. | Real evidence, fit analysis, Product Evolution Review, Work Placement Review, Safety/Authority/Verification/Rollback/STOP_SAFE review. | Report recommendation, owner, safety, latency/cost/time impact, and canonical update. | Durable conclusions promoted to canonical owner; reports remain historical evidence only. | Return to existing backlog item `B1`. |

Every RT2 workstream executes the same OMP engineering lifecycle:

```text
Resolve current workstream
  -> consume canonical knowledge and research inventory
  -> verify existing implementation and owner coverage
  -> reuse existing owner if sufficient
  -> extend existing owner only when evidence proves a gap
  -> implement only the minimal safe change allowed by current authority
  -> verify tests, truth, convergence, safety, latency, cost, freshness, rollback, and STOP_SAFE
  -> create Engineering Report
  -> promote durable conclusions through canonical owner update
  -> update Current Program State when state changes
  -> continue next RT2 workstream or graduate
```

### 28.4 Old RT2 Mapping

The old RT2.1-RT2.12 proposal is superseded as an active roadmap.
Its content is preserved only as absorbed responsibilities:

| Old item | Canonical workstream |
| --- | --- |
| RT2.1 Continuous World Model | `RT2-S2` |
| RT2.2 Continuous Readiness | `RT2-S2` |
| RT2.3 Desired State Engine | `RT2-S3` |
| RT2.4 Continuous Planning | `RT2-S3` |
| RT2.5 Execution Orchestration | `RT2-S4` |
| RT2.6 Safe Execution Queue | `RT2-S4` as queue feasibility only |
| RT2.7 Bounded Parallelism | `RT2-S5` |
| RT2.8 Runtime Cost Intelligence | `RT2-S1` |
| RT2.9 Runtime Intelligence / Latency Intelligence | `RT2-S1` |
| RT2.10 Runtime Evolution Engine | `RT2-S6` |
| RT2.11 Runtime Performance Dashboard | `RT2-S1` as read-only consumer |
| RT2.12 Continuous Runtime Evolution Framework | `RT2-S6` |

### 28.4.1 Runtime Time Intelligence Placement

Runtime Time Intelligence fits existing RT2 architecture.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, or automation mode.

Placement:

| Capability | Canonical placement | Rule |
| --- | --- | --- |
| Runtime Time Model | Runtime Model + `RT2-S1` | Defines time domains as read-only measurement categories. |
| Time Topology | Runtime Model + `RT2-S1` | Explains why time is spent by mapping waits/dependencies to existing owners. |
| Time Domains | Runtime Model | Observation, World Update, Readiness, Planning, Decision, Execution Wait, Execution, Verification, Rollback, Learning, Engineering Report, Canonical Update, and OMP Progress Time. |
| Recommendation Model | `RT2-S6` | Recommends move-earlier, remove-duplicate, reduce-blocking, reduce-waiting, reduce-cost, or reduce-latency changes only through existing owners. |
| Time/Latency/Cost read models | Existing read-model/admin/runtime owners under `RT2-S1` | Read-only evidence; no decision authority or truth-source promotion. |

All Runtime Time Intelligence work must preserve Safety, Authority, Verification, Rollback, and `STOP_SAFE`.
If a proposed time optimization requires new authority, runtime behavior, queue behavior, or user movement, OMP stops and maps the gap before implementation.

### 28.4.2 Runtime Time Intelligence Capability Maturation

Status: `CANONICALIZED_INSIDE_RT2`.

Runtime Time Intelligence matures only inside `RT2-S1` and `RT2-S6`.
It is not a new phase, roadmap, owner, planner, runtime, truth source, dashboard authority, or implementation queue.

| Level | Maturity capability | RT2 owner | OMP rule |
| --- | --- | --- | --- |
| 1 | Time Measurement | `RT2-S1` | Measure or mark missing with owner. |
| 2 | Time Domains | `RT2-S1` + Runtime Model | Map each field to one canonical domain. |
| 3 | Time Topology | `RT2-S1` + Runtime Model | Explain dependency/wait cause without ranking or approval. |
| 4 | Critical Path | `RT2-S1` | Identify longest safe-recovery path or missing evidence. |
| 5 | Time Budget | Runtime Model + OMP/Production Maturity | Categorize budgets without unsafe numeric gates. |
| 6 | Dependency Weight | `RT2-S1` evidence + `RT2-S6` use | Estimate bottleneck contribution with uncertainty. |
| 7 | Impact Prediction | `RT2-S6` | Predict effect only as advisory engineering evidence. |
| 8 | Engineering Recommendation | `RT2-S6` | Produce owner-mapped recommendation/no-change verdict. |
| 9 | Certification | OMP + Production Maturity + relevant owner | Certify implemented change only after separate implementation approval. |
| 10 | Continuous Runtime Optimization Recommendation Loop | `RT2-S6` + Learning owners | Feed certified measurements back into future recommendations; Runtime never self-optimizes. |

Required lifecycle:

```text
Measurement
  -> domains
  -> topology
  -> critical path
  -> budget category
  -> dependency weight
  -> impact prediction
  -> engineering recommendation
  -> OMP/backlog/canonical owner
  -> implementation only after separate approval
  -> certification
  -> measured learning
  -> future recommendation or no-change
```

Every level must produce an Engineering Report when it changes durable knowledge, owner mapping, certification state, or future implementation placement.
No level may change Runtime behavior, authority, safety gates, verification, rollback, `STOP_SAFE`, users, or automation.

### 28.5 RT2 Continue OMP Loop

When OMP reaches RT2, it must execute:

```text
Resolve current RT2 workstream
  -> consume Research Framework / canonical owners
  -> verify existing implementation
  -> reuse or extend existing owner
  -> implement minimal safe change
  -> verify tests / truth / convergence / safety
  -> create Engineering Report
  -> promote durable knowledge to canonical owner when needed
  -> update Current Program State
  -> continue next workstream or graduate
```

Unfinished RT2 work must be resumed, closed, or explicitly deferred by OMP before unrelated new work is selected.

### 28.6 External Model Loop

External runtime/control-plane practices enter V7 only through:

```text
Research Framework / Research Process
  -> research inventory inside existing research owner
  -> V7 Fit Analysis
  -> Work Placement Review
  -> Safety / Authority / Verification / Rollback / Freshness Review
  -> canonical owner or backlog mapping only if applicable
```

External models never override V7 architecture directly.
Vendor-specific mechanisms are examples, not authority.
Research may update OMP only when scheduler or optimizer meaning changes.

### 28.7 Graduation Criteria

RT2 graduates when all six workstreams are complete, explicitly deferred with safety reason, or marked not applicable by OMP, and Runtime can:

- consume prepared world/readiness/desired-state/planning knowledge;
- perform only live validation, bounded mutation, verification, rollback/STOP_SAFE, and outcome collection;
- expose runtime cost/reaction latency/stop reason visibility through read models;
- coordinate bounded certified execution through existing owners;
- feed real outcomes back into OMP without creating new architecture.

No `RT3` program is created by default.
Future runtime improvement after graduation proceeds through Product Evolution Review, Engineering Review, OMP, Backlog, production evidence, certification, and explicit authority where required.

### 28.8 Current Status

RT2 Program Integration: `CANONICALIZED_DOCS_ONLY`.

RT2 implementation: `FUTURE_NOT_ACTIVE`.

Current practical next OMP step: `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD`.

## 29. Master OMP Completeness Certification

Status: `MASTER_2_COMPLETE`.

Purpose:
Certify OMP as the only long-term execution program of V7.

This section does not create a new roadmap, master program, runtime, planner, owner, truth source, phase, automation path, authority path, or implementation queue.

OMP remains the operating system of V7 development:

```text
Future capability
  -> Engineering Context Resolver
  -> Knowledge Plane
  -> OMP placement
  -> existing owner / backlog / canonical owner
  -> implementation or audit only when required
  -> verification / certification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> next OMP step
```

### 29.1 Future Capability Coverage

Every future capability class must enter through the existing OMP path below.

| Future activity | OMP entry | Existing owner destination | Canonical destination | Completion evidence |
| --- | --- | --- | --- | --- |
| Runtime evolution | RT2 / Runtime Eligibility / Authority Evolution | Runtime Model, existing runtime owners, Backlog | Runtime Model, OMP, CPS | Tests, truth/convergence, safety, authority, Engineering Report |
| Routing evolution | Movement Protection / Routing capability backlog | Autoswitch/planner, policies, service matrix owners | OMP, SYSTEM_MAP, policies | Real outcomes, rollback/verification, production evidence |
| Research / world practices | Research integration gate | Research Framework / Research Process | Canonical owner or OMP only if durable | Fit Analysis, Work Placement, Safety Review, Engineering Report |
| Product evolution | Product Evolution Review | Product Specification, OMP, Backlog | Product Specification, Canonical Reference | Business Objective mapping and certification review |
| Runtime optimization | Continuous optimization / RT2 | Runtime Model, read models, existing runtime owners | Runtime Model or OMP | Runtime cost, latency, safety, no live gate bypass |
| Latency optimization | Runtime Latency Review | Runtime Model, Work Placement owners | Runtime Model / OMP | Latency Impact and measurement owner |
| Runtime cost optimization | Product Evolution Review / RT2-S1 | Runtime Model, Production Maturity, read models | Runtime Model / Production Maturity | Cost dimension evidence and report |
| Decision evolution | Decision Lifecycle / Decision Explainability | Decision Model, decision surface, planner owners | Decision Model / OMP | Freshness, lifecycle, authority separation |
| Policy evolution | Policy library to OMP gate | Canonical Policy Library, Backlog, Runtime gates | Policies, OMP, Canonical Reference | Policy fit, interaction audit, certification |
| UX evolution | Business Operator Experience / Decision Explainability | Product Specification, UI/read-model owners, OMP | Product Specification / SYSTEM_MAP if ownership changes | Operator evidence, no truth-source promotion |
| Dashboard evolution | Observability / read-model discipline | Admin read models, OMP, Runtime Model | SYSTEM_MAP only if owner meaning changes | Read-only evidence, no authority |
| Read-model evolution | Observability / Knowledge System | Existing read-model owners | SYSTEM_MAP / Canonical Reference if durable | Scale, freshness, truth consistency |
| Observability | Observability capability | Admin read models, truth/convergence, evidence inventory | OMP / SYSTEM_MAP | Read-only safety evidence coverage |
| Deployment | Production Readiness | Safe deploy, truth/convergence, production owners | CPS, Production Maturity | Deploy verification and no unapproved mutation |
| Certification | Certification workflow | OMP, policies, action-class owners | CPS, Production Maturity, Canonical Reference | Mandatory/supporting evidence closed |
| Production maturity | Production Maturity ladder | Production Maturity Model, Backlog, CPS | CPS / Production Maturity Model | Score recalculation from real state |
| Operator workflow | Decision Explainability / Operator Responsibility | Product Specification, UI/read-model owners, OMP | Product Specification / Canonical Reference | Russian explanation, risk/value/evidence |
| AI-assisted engineering | ECR / Knowledge Plane / Continue OMP | Kernel, Context Resolver, OMP, reports | OMP / Canonical Reference if durable | Existing-owner mapping and report |
| Future protocols | Architecture Closed by Default / Movement Protection | Policies, Runtime Model, routing owners, Backlog | Policies / Runtime Model / SYSTEM_MAP | Reuse proof, certification, production evidence |
| Future routing methods | Movement Protection / Routing evolution | Autoswitch/planner, policy, service matrix owners | OMP / SYSTEM_MAP / policies | Safety gates, rollback, verification, outcomes |
| Capability change / merge / split / deprecation / retirement | Product Evolution Review / Capability state | Owning capability, Backlog, CPS | OMP / CPS / Canonical Reference | Consumer inventory, ownership review, safety and rollback review |

If a future activity cannot be mapped to this table, OMP must run Architecture Closed by Default before proposing any new owner or roadmap.

Capability lifecycle state changes use this same table.
Changing, merging, splitting, deprecating, or retiring a capability is normal Product Execution work when the existing owner, consumer inventory, evidence, report, canonical update, CPS update, and next OMP step are clear.
If any of those are unclear, OMP stops at owner/evidence discovery before architecture is reopened.

### 29.2 Growth Readiness

OMP may grow for years only by extending existing owner sections.

Forbidden growth patterns:

- duplicate roadmap;
- duplicate OMP;
- duplicate capability program;
- nested master program;
- repeated stage sequence with a new name;
- dead stage without owner, evidence, report, and canonical destination;
- parallel implementation queue;
- report-only truth;
- dashboard authority;
- research-driven runtime change without OMP placement.

Allowed growth patterns:

- add a row to an existing capability table;
- extend an existing owner contract;
- add backlog mapping through OMP;
- promote durable report findings to canonical owners;
- update CPS for volatile state;
- retire or deprecate capability wording when no live consumer remains.

### 29.3 OMP Engineering Language

Canonical OMP vocabulary for future work:

| Term | Meaning |
| --- | --- |
| Discovery | Find current reality and existing owners. |
| Research | Collect mature outside practice through Research Framework. |
| Fit Analysis | Compare research to V7 constraints, owners, product intent, and safety. |
| Reuse | Use existing owner without new architecture. |
| Extension | Add capability to an existing owner when reuse is insufficient. |
| Implementation | Change existing code/doc owner only after OMP placement. |
| Verification | Prove behavior, truth, convergence, safety, and no unintended mutation. |
| Certification | Close required evidence for capability, policy, action class, or maturity. |
| Production | Real deployed/runtime state and observed outcomes. |
| Learning | Feed real outcomes into existing evidence and OMP owners. |
| Engineering Report | Historical evidence saved after meaningful action. |
| Canonical Update | Durable knowledge promoted from reports to existing canonical owner. |
| Current Program State | Volatile current bottleneck, task, authority, metrics, and stop reason. |
| Product Evolution | Product Review -> OMP -> Backlog/canonical owner update. |
| Retirement | Mark a capability path complete, superseded, or no longer active. |
| Deprecation | Remove active recommendation status while preserving history. |

### 29.4 Self-Evolution Rule

OMP improves only through:

```text
Engineering Report
  -> durable conclusion extracted
  -> Canonical Update
  -> Current Program State when state changes
  -> next OMP step
  -> future Engineering Report
```

Reports may trigger OMP improvement, but reports never become OMP, backlog, roadmap, truth source, or owner.

OMP update is required only when scheduler, optimizer, capability, command, stop condition, maturity, or canonical placement semantics change.

### 29.5 Completeness Verdict

OMP completeness score: `100 / 100`.

Architecture completeness score inside OMP: `100 / 100`.

Growth readiness: `READY`.

Future evolution readiness: `READY_THROUGH_EXISTING_OMP`.

No second roadmap is justified.
No parallel capability program is justified.
No MASTER 3 was started by this certification at that time.

Historical practical implementation next step at that time:

```text
A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD
```

## 30. OMP Resilience Certification / Master 3

Status: `MASTER_3_COMPLETE`.

Purpose:
Record the destructive stress test of OMP.

MASTER 3 does not create a new canonicalization layer, integration layer, roadmap, master program, runtime, planner, owner, truth source, automation path, authority path, or capability program.

### 30.1 Stress Test Results

| Test | Break attempt | Result | Required invariant |
| --- | --- | --- | --- |
| Duplicate Test | Split OMP into another roadmap/program or duplicate capability flow. | `FAILED_TO_BREAK`; duplicate would create conflicting scheduler/queue/authority. | OMP remains the only execution program; Backlog remains the only queue. |
| Dependency Test | Remove ECR, Knowledge Plane, Backlog, Runtime Model, Decision Model, SYSTEM_MAP, Canonical Reference, CPS, reports, or truth/convergence. | `FAILED_TO_BREAK`; each removal loses placement, owner, state, evidence, or verification. | Dependencies are mandatory by task class and loaded through ECR. |
| Completion Criteria Test | Mark stages complete without criteria. | `FAILED_TO_BREAK`; stage remains incomplete without owner, evidence, report, and canonical destination. | Every stage needs objective completion criteria. |
| Evidence Test | Execute stages without evidence. | `FAILED_TO_BREAK`; OMP stops at safety, authority, certification, or real-world limit. | No evidence means no certification or authority promotion. |
| Owner Test | Remove owners from stages. | `FAILED_TO_BREAK`; responsibility becomes ambiguous. | Every stage maps to existing owner, existing backlog, or canonical owner. |
| Engineering Report Test | Remove reports. | `FAILED_TO_BREAK`; history, why, safety, and verification context are lost. | Every meaningful action creates a report. |
| Canonical Update Test | Remove canonical updates. | `FAILED_TO_BREAK`; durable knowledge stays trapped in history. | Durable findings must be promoted to existing canonical owners. |
| Capability Injection Test | Inject future capabilities. | `PASSED`; all tested capabilities enter OMP through existing placement. | New capability starts with ECR -> OMP placement -> existing owner. |
| Evolution Pressure Test | Run V7 for 1/3/5/10 years. | `PASSED_WITH_INVARIANT`; pressure to create OMP2/Roadmap2 is blocked. | Extend existing OMP sections; never create parallel program. |
| Growth Test | Simplify, merge, remove, shorten. | `NO_SAFE_SIMPLIFICATION_FOUND`; removal loses owner/evidence/report/canonical/state function. | Growth by rows and owner extensions only. |
| Failure Test | Remove one master, capability, lifecycle, owner, criterion, or flow. | `FAILED_TO_BREAK`; each removal loses a required invariant. | No required invariant may be optionalized. |
| Architecture Pressure Test | Invent future architecture. | `PASSED`; proposed architecture must map to existing OMP or stop at Architecture Closed by Default. | New architecture is last resort after impossible reuse proof. |
| Self-Evolution Test | Remove Engineering Report -> Canonical Update -> CPS -> next OMP step -> future report loop. | `FAILED_TO_BREAK`; OMP stops learning and future work rediscovers history. | OMP self-evolves only through report, canonical promotion, CPS update, and next OMP step. |
| Knowledge Preservation Test | Leave durable knowledge only in reports, audits, research, or implementation notes. | `FAILED_TO_BREAK`; future agents lose durable truth or treat history as current truth. | Durable conclusions must have a canonical destination before closure. |

### 30.2 Required Resilience Invariants

OMP is resilient only while all invariants remain true:

1. OMP is the only long-term execution program.
2. Implementation Backlog is the only engineering queue.
3. Current Program State owns volatile current state.
4. Canonical Reference and SYSTEM_MAP own durable truth and owner lookup.
5. Engineering Reports are historical evidence only and mandatory after meaningful work.
6. Durable findings never remain only in reports.
7. Every stage has owner, completion criteria, evidence, engineering report, and canonical destination.
8. Runtime remains thin; OMP never authorizes runtime behavior without certification and explicit authority.
9. Research cannot bypass Fit Analysis, Work Placement, owner mapping, and OMP.
10. Dashboard, UX, read model, telemetry, and AI assistance never become truth source or authority.
11. Retirement and deprecation preserve history and require no live consumer plus safety review.
12. Any unmappable future capability stops at Architecture Closed by Default.

### 30.3 Capability Injection Matrix

| Injected future capability | OMP entry | Existing owner | Production path | Canonical path |
| --- | --- | --- | --- | --- |
| New routing protocol | Future protocols / Movement Protection | Policies, Runtime Model, autoswitch/planner, Backlog | Certification, rollback, verification, real outcomes | Policies / Runtime Model / SYSTEM_MAP |
| New VPN protocol | Future protocols / Product Evolution Review | Product Specification, policies, service matrix, routing owners | Backlog, safe deploy, truth/convergence, production evidence | Product Specification / policies / SYSTEM_MAP |
| New transport | Future protocols / Product Evolution Review | Product Specification, policies, Runtime Model, routing owners | Backlog, compatibility tests, verification, production evidence | Product Specification / Runtime Model / SYSTEM_MAP |
| New telemetry | Observability / read-model discipline | Admin read models, evidence inventory, Runtime Model | Read-only rollout, truth consistency, no authority | SYSTEM_MAP / Runtime Model if semantics change |
| New runtime optimization | Continuous optimization / RT2 | Runtime Model, existing runtime/read-model owners | Tests, latency/cost review, no live gate bypass | Runtime Model / OMP |
| New latency optimization | Runtime Latency Review / Work Placement | Runtime Model, Work Placement owners, OMP | Measurement plan, tests, no live safety bypass | Runtime Model / OMP |
| New Runtime Cost optimization | Runtime Cost Review / Product Evolution Review | Runtime Model, Production Maturity, read-model owners | Cost evidence, safety review, no authority expansion | Runtime Model / Production Maturity |
| New dashboard | Observability / Dashboard evolution | Admin API/read-model owners, OMP | Read-only UI/API, no decision authority | SYSTEM_MAP only if owner meaning changes |
| New UX | Business Operator Experience / Decision Explainability | Product Specification, UI/read-model owners | Operator validation, evidence-linked explanation | Product Specification / Canonical Reference |
| New AI subsystem | AI-assisted engineering / ECR | Kernel, Context Resolver, OMP, Research Framework | Advisory use only, report, no authority | OMP / Canonical Reference if durable |
| New policy | Policy evolution | Canonical Policy Library, Research Framework, OMP | Fit Analysis, interaction audit, backlog/certification | Policies / OMP / Canonical Reference |
| New routing algorithm | Routing evolution | Autoswitch/planner, policies, service matrix | Backlog, tests, rollback/verification, outcomes | OMP / SYSTEM_MAP / policies |
| New verification | Certification workflow | Verification owners, truth/convergence, Runtime Model | Evidence validation before certification | Runtime Model / OMP / SYSTEM_MAP |
| New rollback strategy | Rollback / Movement Protection | Restore barrier, rollback owners, Runtime Model | Governed proof, rollback/no-rollback evidence | Runtime Model / policies / SYSTEM_MAP |
| New deployment model | Production Readiness | Safe deploy, truth/convergence, Production Maturity | Deploy verification, no unapproved mutation | CPS / Production Maturity / Canonical Reference |
| New observability source | Observability / Knowledge System | Read-model/evidence owners, SYSTEM_MAP | Read-only evidence, freshness and source validation | SYSTEM_MAP / Canonical Reference |
| New Research result | Research integration gate | Research Framework, Research Process, OMP | Fit Analysis, owner mapping, implementation only through Backlog if required | Canonical owner / OMP only when durable |
| New Client capability | Product Evolution Review / Business Operator Experience | Product Specification, policies, UI/read-model/routing owners | Backlog, tests, operator validation, production evidence | Product Specification / SYSTEM_MAP / Canonical Reference |
| New Server capability | Product Evolution Review / Production Readiness | Product Specification, Runtime Model, deploy/runtime owners | Backlog, tests, safe deploy, truth/convergence | Runtime Model / SYSTEM_MAP / Production Maturity |

### 30.4 Growth Pressure Verdict

For 1 year, 3 years, 5 years, and 10 years, OMP must resist creation of `OMP2`, `Roadmap2`, a new master program, or a new capability program.

The correct growth action is:

```text
Extend existing OMP section
  -> map to existing owner
  -> update Backlog only through OMP when implementation is required
  -> report
  -> canonical update
  -> Current Program State
```

If this path cannot hold a future capability, OMP must stop at `FUNDAMENTAL_ARCHITECTURE_GAP`; it must not silently create parallel structure.

### 30.4.1 Failure Injection Results

| Removed item | What breaks |
| --- | --- |
| One MASTER conclusion | Closure chain loses proof that prior architecture/canonicalization/resilience work is complete. |
| One capability | Backlog-to-maturity mapping loses production purpose and progress visibility. |
| One lifecycle | Work can skip owner mapping, verification, report, canonical update, or CPS. |
| One owner | Responsibility becomes ambiguous and duplicate owners become tempting. |
| One completion criterion | Two engineers can close the same stage differently. |
| One engineering report | Historical reason, safety, evidence, and alternative analysis disappear. |
| One canonical update | Durable knowledge remains trapped in report/audit/research history. |
| One dependency | Context, placement, owner lookup, runtime semantics, decision semantics, state, or verification becomes unbounded. |

### 30.4.2 Architecture Pressure Results

Invented future architectures tested:

| Future architecture pressure | OMP result |
| --- | --- |
| Event-driven autonomous runtime expansion | Maps to Runtime Model, RT2, Authority Evolution, and explicit authority; no new runtime by default. |
| Multi-protocol routing substrate | Maps to Product Evolution, policies, Movement Protection, Runtime Model, and Backlog. |
| AI engineering assistant subsystem | Maps to ECR, Knowledge Plane, Research Framework, OMP, and reports as advisory-only. |
| New observability/control dashboard plane | Maps to Observability/read-model owners; dashboard cannot become truth or authority. |
| Distributed deployment model | Maps to Production Readiness, safe deploy, truth/convergence, CPS, and Production Maturity. |

No tested future architecture requires a new architecture proposal.

### 30.4.3 Knowledge Preservation Results

Durable knowledge must never remain only inside:

- Engineering Reports;
- audits;
- research;
- implementation notes;
- chat handoffs.

Required preservation path:

```text
Historical evidence
  -> durable conclusion extraction
  -> canonical owner update
  -> SYSTEM_MAP only if ownership/topology changes
  -> Current Program State only if volatile state changes
  -> OMP only if scheduler/optimizer/capability semantics change
```

### 30.5 Resilience Verdict

OMP resilience score: `100 / 100`.

OMP simplicity score: `100 / 100`.

OMP long-term evolution score: `100 / 100`.

Weaknesses found: `1`; stress-test invariants and injected-capability examples were implicit rather than explicit.

Improvements made: `1`; this section records destructive test results, required invariants, injection matrix, and growth pressure verdict.

Simplifications performed: `0`; no safe merge/removal preserved owner, evidence, report, canonical, and state invariants.

Merges performed: `0`; existing flows are layered responsibilities, not duplicates.

MASTER 4 later completed; this historical Master 3 section did not itself start it.

## 31. Architecture Graduation & Product Transition / Master 4

Status: `MASTER_4_COMPLETE`.

Purpose:
Certify that V7 architecture is complete and graduate V7 from Architecture Mode to Product Execution Mode.

MASTER 4 does not create a new roadmap, master program, runtime, planner, owner, truth source, capability program, implementation queue, automation path, authority path, or runtime behavior.

### 31.1 Architecture Graduation Certification

Architecture Graduation Score: `100 / 100`.

Graduation checks:

| Area | Verdict | Owner |
| --- | --- | --- |
| Runtime architecture | `COMPLETE` | Runtime Model |
| Decision architecture | `COMPLETE` | Decision Model |
| OMP | `COMPLETE` | OMP |
| Work Placement | `COMPLETE` | Runtime Model + OMP |
| RT2 integration | `COMPLETE_DOCS_ONLY` | OMP + Runtime Model |
| Capability ownership | `COMPLETE` | SYSTEM_MAP + OMP |
| Canonical ownership | `COMPLETE` | Canonical Reference + SYSTEM_MAP |
| Research flow | `COMPLETE` | Research Framework / Research Process |
| Knowledge preservation | `COMPLETE` | Canonical Reference + Document Lifecycle + OMP |

No architecture gap remains inside MASTER 4 scope.

### 31.2 Architecture Constitution

Architecture exists to preserve:

- Reality;
- Safety;
- Authority;
- Certification;
- Verification;
- Knowledge;
- Evolution.

Architecture does not own:

- backlog execution;
- runtime mutations;
- deployments;
- user movement;
- engineering tasks;
- implementation selection;
- production operations;
- engineering history.

Architecture is now closed by default.
It changes only when existing architecture cannot express a capability after complete owner, OMP, canonical, policy, runtime, decision, research, and backlog reuse review.

### 31.3 Architecture Change Protocol

Normal change path:

```text
Idea
  -> Existing Owner Check
  -> Reuse / Extend Existing Owner
  -> OMP
  -> Implementation only if approved and backlog-owned
  -> Verification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> Continue OMP
```

Architecture proposal path:

```text
Existing architecture cannot express capability
  -> Architecture Proposal
  -> Discovery
  -> Validation
  -> OMP Integration
  -> Implementation only through existing or newly certified owner
```

Architecture changes must never bypass OMP, Engineering Report, Canonical Update, or Current Program State.

### 31.4 Capability Admission Rule

Every future capability must answer:

```text
Why can the existing owner not express this capability?
```

If the answer is missing, incomplete, speculative, implementation-convenience-only, or based on preference, new capability ownership is forbidden.

Default result:

```text
Need New Owner = FALSE
Need New Roadmap = FALSE
Need New Architecture = FALSE
```

Only a proven `FUNDAMENTAL_ARCHITECTURE_GAP` may change the default.

Engineering Review capability injection:

| Future capability | Existing entry | Existing owner destination |
| --- | --- | --- |
| Runtime Time Intelligence | `RT2-S1` / `RT2-S6` | Runtime Model, OMP, read-model owners, Production Maturity |
| Client Intelligence | Product Evolution Review / Client capability | Product Specification, UI/client/read-model owners, OMP |
| Future Routing | Movement Protection / routing evolution | Autoswitch/planner, policies, service matrix, Runtime Model |
| AI Engineering | ECR / Knowledge Plane / Research Framework | Kernel, Context Resolver, OMP, Research Framework, Canonical Reference if durable |
| Future Telemetry | Observability / read-model discipline | Admin read models, evidence inventory, Runtime Model, SYSTEM_MAP if ownership changes |
| Advanced Recovery | Recovery Admission / Rollback / Movement Protection | Restore barrier, rollback owners, Runtime Model, policies, OMP |
| New Dashboard | Observability / dashboard evolution | Admin API/read-model owners, OMP, SYSTEM_MAP if owner meaning changes |
| New Verification | Certification workflow | Verification owners, truth/convergence, Runtime Model, OMP |
| New Research | Research integration gate | Research Framework, Research Process, OMP, canonical owner if durable |

All injected examples enter existing architecture.
None justifies reopening architecture.

### 31.5 Knowledge Preservation Contract

Durable knowledge must never remain only inside:

- reports;
- audits;
- research;
- chats;
- implementation notes;
- handoff notes.

Every durable conclusion must have exactly one canonical owner.

Required preservation path:

```text
Historical evidence
  -> durable conclusion extraction
  -> exactly one canonical owner
  -> SYSTEM_MAP only if ownership/topology changes
  -> Current Program State only if volatile state changes
  -> OMP only if scheduler/optimizer/capability semantics change
```

Reports remain historical evidence.
Canonical owners preserve durable truth.

### 31.6 Product Execution Contract

Product Execution Mode is active after MASTER 4.

The only normal engineering workflow is:

```text
OMP
  -> Implementation Backlog or existing owner
  -> Verification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> Continue OMP
```

No parallel workflow is allowed.
Future architecture work is exceptional and must pass Architecture Closed by Default first.

Capability lifecycle certification:

```text
Idea
  -> Existing Owner Check
  -> Architecture Fit
  -> OMP Admission
  -> Capability Classification
  -> Owner Mapping
  -> Canonical Integration
  -> Implementation Backlog or existing owner
  -> Implementation only after approval
  -> Verification / Certification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> Continue OMP
```

Capability evolution, including measurement, topology, critical path, budget, recommendation, certification, optimization, change, merge, split, deprecation, and retirement, must reuse this same Product Execution workflow.

Governance mapping:

| Question | Existing answer |
| --- | --- |
| Who approves? | OMP / operator approval where authority is required. |
| Who owns? | Existing canonical owner identified by SYSTEM_MAP and OMP owner check. |
| Who implements? | Existing owner or Implementation Backlog item selected by OMP. |
| Who certifies? | OMP, Production Maturity, policy/action-class owner, or affected canonical owner. |
| Who preserves knowledge? | Exactly one canonical owner; reports remain evidence. |
| Who updates Current Program State? | OMP through `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Who continues work? | `Continue OMP`. |

No separate capability lifecycle, roadmap, owner, or master program is allowed.

### 31.7 Program Navigation

Separate `ARCHITECTURAL_INVARIANTS.md` and `PROGRAM_MAP.md` files are not created.

Existing navigation is sufficient:

| Navigation need | Existing owner |
| --- | --- |
| Architectural invariants | OMP, Canonical Reference, Runtime Model, Decision Model, Kernel |
| Program map | OMP, SYSTEM_MAP, Current Program State, Document Lifecycle |
| Document roles | SYSTEM_MAP + Document Lifecycle |
| Current execution state | Current Program State |
| Future capability routing | OMP + SYSTEM_MAP |

Future engineer navigation:

| Question | Destination |
| --- | --- |
| Where to implement? | OMP selects Implementation Backlog item or existing owner. |
| Where to document? | Engineering Report for evidence; canonical owner for durable conclusion. |
| Where to certify? | OMP, Production Maturity, policy/action-class owner, or affected canonical owner. |
| Where to report? | `docs/reports/engineering/` after meaningful work. |
| Where to preserve knowledge? | Exactly one canonical owner; SYSTEM_MAP only for ownership/topology; CPS only for volatile state. |
| Where to continue? | `Continue OMP`. |

Creating additional navigation files would duplicate existing owners.

### 31.8 Boundary Review

Architecture owns:

- laws;
- contracts;
- ownership;
- structure;
- evolution rules.

Architecture does not own:

- implementation;
- runtime mutation;
- deployment;
- production operations;
- user movement;
- engineering history;
- backlog ranking;
- certification evidence execution.

### 31.9 Graduation Review

Attempt to reopen architecture: `FAILED`.

Future work can continue without modifying architecture because:

- OMP is complete and self-evolving;
- SYSTEM_MAP owns future capability placement;
- Canonical Reference owns durable conclusions;
- Current Program State owns volatile state;
- Engineering Reports preserve historical evidence;
- Architecture Closed by Default blocks speculative redesign;
- Product Execution Mode routes work through OMP and existing owners.

Graduation verdict:

```text
MASTER_4_COMPLETE
```

Product Execution Mode is active.
Do not begin A5 from MASTER 4.

## 32. Engineering Intelligence Materialization / Phase 1

Status: `PHASE_1_COMPLETE`.

Engineering Intelligence Materialization turns existing architecture into explicit engineering capability.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability program, automation mode, or implementation queue.

Gate 0 classification:

| Target | Classification | Existing owner reused |
| --- | --- | --- |
| Observation Intelligence | `EXISTS_UNDER_OTHER_NAME` | Observation Plane owners + `RT2-S1` |
| Process Intelligence | `EXISTS_UNDER_OTHER_NAME` | Runtime Model + Work Placement + Decision Lifecycle + `RT2-S1` |
| Runtime Time Intelligence | `EXISTS_COMPLETE` | Runtime Model + `RT2-S1` + `RT2-S6` |
| Recommendation Intelligence | `EXISTS_PARTIAL` | `RT2-S6` + OMP + Backlog + Engineering Reports |
| Execution Intelligence | `EXISTS_UNDER_OTHER_NAME` | Runtime Model + execution/lease/packet/verification/rollback owners |
| Prediction Intelligence | `EXISTS_COMPLETE` | Prediction Evidence / Confidence owners |
| Confidence Intelligence | `EXISTS_COMPLETE` | Autonomy Root Confidence / Trust owners |
| Adaptive Engineering Intelligence | `EXISTS_PARTIAL` | Decision To Outcome To Learning + feedback/learning owners + `RT2-S6` |

### Engineering Intelligence Lifecycle

Engineering Intelligence lifecycle:

```text
Observation
  -> Process Understanding
  -> Runtime Time Understanding
  -> Recommendation
  -> Implementation through OMP if approved
  -> Outcome
  -> Prediction vs Reality
  -> Confidence Update
  -> Recommendation Evolution
```

Materialization rule:

Only `EXISTS_PARTIAL` read-model or lifecycle surfaces may be extended, and only under the existing owner.
`EXISTS_COMPLETE` and `EXISTS_UNDER_OTHER_NAME` surfaces must be reused.
Recommendation evolution remains advisory until OMP selects an implementation owner and later certification proves the outcome.

### RT2-S1 Engineering Measurement Contract

`RT2-S1` owns Engineering Measurement for Engineering Intelligence.
It materializes only read-only evidence:

- observation evidence;
- time fields;
- process/topology/critical-path fields;
- wait and blocker evidence;
- missing-field owner mapping;
- measurement reliability status.

`RT2-S1` must not decide, approve, rank execution, certify, mutate Runtime, create synthetic evidence, or become a truth source.

### RT2-S6 Engineering Recommendation Contract

`RT2-S6` owns Engineering Recommendation for Engineering Intelligence.
It materializes:

- owner-mapped recommendation;
- explicit no-change verdict;
- missing-evidence verdict;
- expected measurement plan;
- Product Evolution Review;
- Work Placement Review;
- Safety/Authority/Verification/Rollback/STOP_SAFE review.

`RT2-S6` recommendations are advisory until OMP routes approved implementation to an existing owner or Backlog.
`RT2-S6` must not mutate Runtime, expand authority, bypass verification, create a parallel roadmap, or replace OMP prioritization.

Engineering Intelligence maturity states:

```text
Measured
  -> Understood
  -> Recommended
  -> Validated
  -> Predictive
  -> Adaptive
```

The current Phase 1 materialization state is `UNDERSTOOD_PARTIAL_RECOMMENDED`: observation/process/time/prediction/confidence owners exist; recommendation and adaptive loops exist but need future measured implementation outcomes before `VALIDATED`, `PREDICTIVE`, or `ADAPTIVE` can be claimed for Engineering Intelligence as an operating capability.

## 33. Engineering Intelligence Materialization / Phase 2

Status: `PHASE_2_COMPLETE`.

Phase 2 materializes the Engineering Validation Loop.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability program, automation mode, or implementation queue.

Gate 0 classification:

| Target | Classification | Existing owner reused |
| --- | --- | --- |
| Prediction History | `EXISTS_COMPLETE` | Prediction Evidence / Confidence owners |
| Prediction vs Reality | `EXISTS_COMPLETE` | Prediction Evidence / Confidence + feedback/outcome owners |
| Recommendation History | `EXISTS_PARTIAL` | OMP + Engineering Reports + Backlog |
| Outcome History | `EXISTS_COMPLETE` | Feedback/outcome/learning owners |
| Confidence History | `EXISTS_COMPLETE` | Autonomy Root Confidence / Trust owners |
| Engineering Validation | `EXISTS_PARTIAL` | OMP + Runtime Model + Engineering Reports |
| Recommendation Accuracy | `EXISTS_PARTIAL` | `RT2-S6` + Prediction Evidence / Confidence |
| Recommendation Success | `EXISTS_PARTIAL` | `RT2-S6` + outcome owners |
| Recommendation Failure | `EXISTS_PARTIAL` | `RT2-S6` + outcome owners |
| Recommendation Drift | `MISSING` -> materialized | `RT2-S6` + OMP + confidence owners |
| Recommendation Confidence | `EXISTS_PARTIAL` | `RT2-S6` + Autonomy Root Confidence / Trust |
| Prediction Confidence | `EXISTS_COMPLETE` | Prediction Evidence / Confidence owners |
| Engineering Validation Loop | `EXISTS_PARTIAL` | OMP |

### Engineering Validation Lifecycle

Engineering Validation uses the existing OMP lifecycle.
No second engineering lifecycle is allowed.

```text
Recommendation
  -> Implementation through OMP if approved
  -> Outcome
  -> Prediction vs Reality
  -> Difference
  -> Confidence Update
  -> Recommendation Evolution
```

### Recommendation Validation Lifecycle

Every implemented recommendation must eventually be classified:

| Validation class | Meaning | Required evidence |
| --- | --- | --- |
| `RECOMMENDATION_SUCCESS` | Observed outcome supports the recommendation. | Verification/outcome evidence and expected-result match. |
| `RECOMMENDATION_FAILURE` | Observed outcome contradicts the recommendation or harms safety/product objective. | Verification/outcome evidence and contradiction. |
| `RECOMMENDATION_PARTIAL` | Outcome is mixed or incomplete. | Known pass/fail/unknown evidence split. |
| `RECOMMENDATION_DRIFT` | Recommendation assumptions changed before or after implementation. | Material state, owner, freshness, or evidence-version difference. |
| `RECOMMENDATION_UNVALIDATED` | Implementation/outcome evidence is missing. | Explicit missing owner/evidence reason. |

Recommendation validation must report expected result, observed result, difference, confidence delta, evidence source, owner, and canonical update need.
Validation cannot approve runtime action, expand authority, certify automation, or replace verification.

### Phase 2 Knowledge Preservation Rule

Validation-loop knowledge must survive report deletion through existing owners:

- Runtime Model owns Prediction, Validation, and Confidence contracts.
- OMP owns Engineering Validation Lifecycle and Recommendation Validation Lifecycle.
- Production Maturity owns Engineering Intelligence Validation Maturity.
- SYSTEM_MAP owns validation ownership lookup.
- Canonical Reference owns durable conclusions only.
- CPS owns current Engineering Intelligence validation maturity.

## 34. Engineering Intelligence Materialization / Phase 3

Status: `PHASE_3_COMPLETE`.

Phase 3 materializes Adaptive Engineering and closes the Engineering Intelligence materialization roadmap.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability family, automation mode, or implementation queue.
Runtime never self-improves.
Only Engineering Intelligence evolves through OMP and existing owners.

Gate 0 classification:

| Target | Classification | Existing owner reused |
| --- | --- | --- |
| Engineering Adaptation | `EXISTS_PARTIAL` | OMP + `RT2-S6` + Production Maturity |
| Recommendation Evolution | `EXISTS_PARTIAL` | `RT2-S6` + OMP |
| Recommendation Confidence Evolution | `EXISTS_PARTIAL` | `RT2-S6` + confidence owners |
| Engineering Learning | `EXISTS_PARTIAL` | Decision To Outcome To Learning + OMP |
| Recommendation Drift | `EXISTS_COMPLETE` | OMP + `RT2-S6` + affected owner |
| Recommendation Improvement | `EXISTS_PARTIAL` | `RT2-S6` + validation/outcome owners |
| Prediction Improvement | `EXISTS_UNDER_OTHER_NAME` | Prediction Evidence / Confidence owners |
| Adaptive Engineering | `EXISTS_PARTIAL` | Runtime Model + OMP + Production Maturity |
| Engineering Feedback Loop | `EXISTS_UNDER_OTHER_NAME` | Engineering Report -> Canonical Update -> CPS -> Continue OMP |
| Engineering Recommendation Quality | `EXISTS_PARTIAL` | `RT2-S6` + validation/outcome owners |
| Engineering Recommendation Confidence | `EXISTS_PARTIAL` | `RT2-S6` + confidence owners |

### Adaptive Engineering Lifecycle

Adaptive Engineering uses the existing OMP lifecycle.
No second engineering loop is allowed.

```text
Recommendation
  -> Implementation through OMP if approved
  -> Outcome
  -> Prediction vs Reality
  -> Confidence Update
  -> Recommendation Improvement
  -> Future Recommendation
  -> Engineering Learning
  -> Future Engineering
```

### Recommendation Evolution Lifecycle

Recommendation Evolution belongs to `RT2-S6` and OMP.

| Stage | Owner | Output |
| --- | --- | --- |
| Recommendation Version | `RT2-S6` + Engineering Report | Versioned recommendation basis. |
| Recommendation Confidence | `RT2-S6` + confidence owners | Advisory confidence. |
| Recommendation History | OMP + Engineering Reports + Backlog | Historical evidence and implementation state. |
| Recommendation Quality | `RT2-S6` + validation/outcome owners | Quality classification from real outcomes. |
| Recommendation Evolution | `RT2-S6` + OMP | Improved, degraded, drifted, retired, unchanged, or blocked. |
| Future Recommendation | `RT2-S6` + OMP | Owner-mapped future recommendation/no-change/missing-evidence verdict. |

### Engineering Learning Lifecycle

Engineering Learning is a documentation/control-plane learning loop.
It reuses existing learning owners but does not modify Runtime Learning.

```text
Outcome
  -> Engineering Learning
  -> Recommendation Confidence
  -> Recommendation Evolution
  -> Future Recommendation
```

Engineering Learning must name the outcome, prediction difference, confidence delta, recommendation quality, affected owner, canonical update need, and future recommendation state.
It cannot mutate Runtime, expand authority, approve implementation, create synthetic evidence, or replace OMP.

### Adaptive Read Models

Adaptive read models remain future read-only surfaces under existing owners.

| Possible read model | Existing owner | Phase 3 status |
| --- | --- | --- |
| Recommendation Confidence Trend | `RT2-S6` + confidence owners | `EXISTS_PARTIAL` |
| Recommendation Quality Trend | `RT2-S6` + outcome/validation owners | `EXISTS_PARTIAL` |
| Prediction Accuracy Trend | Prediction Evidence / Confidence owners | `EXISTS_COMPLETE` |
| Engineering Learning History | OMP + Engineering Reports + learning owners | `EXISTS_PARTIAL` |
| Recommendation Evolution History | OMP + Engineering Reports + Backlog | `EXISTS_PARTIAL` |
| Engineering Confidence History | Autonomy Root Confidence / Trust owners | `EXISTS_COMPLETE` |
| Engineering Improvement History | OMP + Engineering Reports + Production Maturity | `EXISTS_PARTIAL` |

Adaptive read models must not decide, approve, rank execution, mutate Runtime, certify themselves, or become a truth source.

### Engineering Intelligence Final State

Engineering Intelligence materialization is complete at the architecture/canonical level.
Remaining work is future implementation and evidence collection only.
Final canonical state: `MEASURED_UNDERSTOOD_RECOMMENDED_VALIDATION_MATERIALIZED_ADAPTIVE_ENGINEERING_READY`.
