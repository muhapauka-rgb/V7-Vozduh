# V7 Autonomous Evolution Program Refactoring Plan

Date: 2026-07-08

Subject:

```text
docs/programs/V7_AUTONOMOUS_EVOLUTION_PROGRAM.md
```

Mode: `ARCHITECTURE_REFACTORING_PLANNING_ONLY`

Program changes performed: `NO`

Architecture changes performed: `NO`

OMP changes performed: `NO`

AOS changes performed: `NO`

`LOCKED_ARCHITECTURE` changes performed: `NO`

`LOCKED_KNOWLEDGE` changes performed: `NO`

## 1. Refactoring Summary

The current Autonomous Evolution Program is structurally sound as a post-Stage-2 route:

```text
LOCKED_ARCHITECTURE
  -> LOCKED_KNOWLEDGE
  -> Ideal Model
  -> Current Reality
  -> Certified Gaps
  -> OMP Missions
  -> Structural Integration
  -> Production Certification
  -> Continuous Evolution
```

It already correctly preserves:

- OMP as the only execution operating system;
- locked architecture and locked knowledge as immutable foundations;
- Source Resolution by Knowledge Category;
- Foundation consumption and verification;
- producer/consumer chain closure;
- consumer confirmation;
- no duplicate OMP, Runtime, Authority, Function Graph, Knowledge Graph, or truth source.

The main refactoring need is philosophical and architectural in emphasis:

```text
From component/function/document evolution
to situation-aware autonomous behaviour.
```

The program must explicitly treat current situations, their interpretation, applicable existing laws, reasoning, decision, execution, verification, learning, and improvement as the primary autonomous behaviour chain.

Existing V7 laws remain central, but law execution alone is too late in the chain. The system must first understand what is happening and why a law applies.

## 2. Canonical Project Goal

Canonical goal for the refactor:

```text
V7 gradually becomes a system that automatically executes its already-existing
architecture laws, engineering knowledge, policies, runtime rules, routing rules,
channel rules, OMP rules, decision logic, verification rules, rollback rules,
learning rules, and canonical synchronization rules.
```

The objective is not primarily to create new capabilities.

The objective is to make existing system knowledge applicable and executable:

```text
Observe
  -> Understand
  -> Analyze
  -> Select applicable laws
  -> Decide
  -> Execute
  -> Verify
  -> Learn
  -> Improve
```

without constant human participation.

## 3. What Already Fully Matches The Goal

| Program Area | Current Fit | Reason |
|---|---|---|
| Non-goals | `FULL_MATCH` | Correctly forbids new architecture, OMP replacement, Runtime replacement, Authority replacement, new truth source, production mutation, and synthetic evidence. |
| Source Resolution | `FULL_MATCH` | Knowledge Category based resolution is already compatible with situation-aware, law-bound autonomous behaviour. |
| Foundation Knowledge Set | `FULL_MATCH` | Locked architecture, locked knowledge, knowledge maps, and implementation maps are required before action. |
| Foundation Lifecycle | `FULL_MATCH` | Synchronization and verification prevent stale foundations. |
| OMP relationship | `FULL_MATCH` | OMP remains the single execution operating system. |
| Function Graph relationship | `FULL_MATCH` | Function Graph remains evidence/index, not truth. |
| CPS relationship | `FULL_MATCH` | CPS remains volatile current reality, not authority or truth. |
| Production Maturity relationship | `FULL_MATCH` | Maturity remains an evidence consumer, not a capability creator. |
| Knowledge Evolution relationship | `FULL_MATCH` | Locked knowledge can evolve only through governed Knowledge Evolution. |
| Chain Closure | `FULL_MATCH` | Results require producer, consumer, consumption, confirmation, next action, and closure. |
| Consumer Confirmation | `FULL_MATCH` | Consumer assignment alone is not enough. |
| Forbidden Actions | `FULL_MATCH` | Current forbidden actions match the law-execution safety boundary. |

These sections should be preserved and reused.

## 4. What Requires Only New Interpretation

| Program Area | Current Meaning | Required New Interpretation |
|---|---|---|
| Knowledge Model | Categories request knowledge sources. | Categories must also resolve situation types, interpretation inputs, applicable law families, reasoning inputs, and execution obligations. |
| Phase Model | Route from ideal to inventory to gaps. | Route from ideal autonomous behaviour target to current situation/reasoning/execution reality to certified Autonomous Behaviour Gaps. |
| Artifact Lifecycle | Tracks documents and phase artifacts. | Track law-execution artifacts as first-class outputs, not only documents. |
| Definition of Done | Ensures artifact completeness. | Add law coverage, execution-state coverage, automation-state coverage, and feedback coverage. |
| Canonical Sync | Updates owners when phase output changes durable knowledge. | Include synchronization of durable law-execution findings through existing owners. |
| Continuous Evolution | Detect gap or improvement opportunity. | Detect where situation interpretation, decision, law execution, verification, learning, or improvement regressed, became stale, needs automation, or produced learning. |

These areas do not require new architecture, but their text should be refocused around situation-aware application of existing laws and knowledge.

## 5. What Requires Refactoring

| Program Area | Refactoring Need | Reason |
|---|---|---|
| Purpose | Add situation-aware autonomous behaviour target explicitly. | Current purpose says autonomous operation but does not make situation understanding and application of existing laws explicit. |
| Knowledge Category Model | Add situation / interpretation / law / rule overlay or clarify existing categories as carriers of applicable knowledge. | Current categories include Policy, Authority, Decision Model, Engineering Truth, but situation interpretation and law discovery are implicit. |
| Phase 2 | Rename/expand from Current Autonomous System Inventory to Current Autonomous Reality Model. | Current inventory is too narrow for law execution, automation state, and manual dependency mapping. |
| Phase 3 | Redefine Gap as certified failure or incompleteness in execution of existing laws. | Current gap rules are strong, but still read partly like missing capability/function checks. |
| Gap Priority | Add law criticality and human-dependency reduction. | Current priority covers production/autonomy/debt, but not explicit law-execution criticality. |
| Phase 5 | Reframe structural integration as execution-path integration of certified laws through existing owners. | Current text says implement certified missions, which can sound capability-first. |
| Phase 7 | Reframe loop as continuous law execution monitoring and learning. | Current loop is good but too generic around gaps/improvements. |
| Acceptance Model | Add law-execution acceptance criteria. | Acceptance currently verifies artifact DoD and boundaries, not law coverage directly. |

## 6. What May Be Combined Or Simplified

| Candidate | Recommendation | Reason |
|---|---|---|
| Source Resolution Model + Knowledge Source Contract | Keep separate but add Law Source Resolution subsection. | Existing split is useful; only missing law lens. |
| Foundation Lifecycle + Foundation Synchronization Law + Foundation Verification | Keep separate; add short "Foundation As Law Baseline" rule. | These are already clean and should not be collapsed. |
| Phase Closure Matrix + Phase Readiness Contract + Program State Machine | Consider adding one consolidated route table after them, not replacing them. | Current repetition is useful for audit, but an autonomous-behaviour summary table would reduce ambiguity. |
| Chain Closure Law + Consumer Confirmation Law | Keep separate; add law-output consumption examples. | They solve different lifecycle problems. |
| Gap Certification Rules + Gap Priority Model | Keep separate; add "Law Execution Gap" definition before both. | Certification and priority should remain distinct. |
| Canonical Synchronization Matrix + Foundation Update Matrix | Cross-reference more tightly. | Both govern updates; the refactor should reduce duplicate wording while preserving both views. |

No section should be removed entirely.

## 7. What Is No Longer Sufficient As Written

| Area | Insufficiency |
|---|---|
| Phase 2 title and output | "Current Autonomous System Inventory" does not fully express reality model, law execution, automation state, manual dependency, and structural friction. |
| Phase 3 purpose | "Only source of new autonomous evolution missions" is correct, but gap definition should not imply only missing functions. |
| Gap certification first checks | Existing knowledge/implementation checks are correct, but must be expanded to law-execution checks. |
| Continuous Evolution loop | It should explicitly monitor situation interpretation, decision quality, execution of laws, verification, and learning, not only gaps or improvement opportunities. |
| Knowledge categories | They need a situation / interpretation / law-rule overlay so the program thinks in autonomous behaviour chains first and source surfaces second. |
| Law Execution Unit | Useful but too late as the primary unit. It must be nested inside a broader situation interpretation and autonomous behaviour model. |

## 8. How The Philosophy Must Change

Current implicit philosophy:

```text
Ideal system
  -> current inventory
  -> gap
  -> mission
  -> implementation
  -> certification
```

Required philosophy:

```text
Situation
  -> interpretation
  -> applicable existing laws
  -> reasoning
  -> decision
  -> execution
  -> verification
  -> learning
  -> improvement
```

The law-execution lens remains necessary, but it is a middle segment:

```text
Situation interpretation
  -> applicable law selection
  -> law-bound decision
  -> law execution
  -> outcome verification
  -> feedback
```

Autonomous evolution therefore should certify failures in autonomous behaviour, not only failures in law execution.

Current implementation route remains:

```text
Autonomous behaviour gap
  -> OMP mission
  -> existing-owner integration
  -> verification
  -> learning
  -> canonical synchronization
```

This is not a new route.

It is a refactoring of what each route step is looking at.

## 9. How The Program Must Think In Laws

The refactored program should still introduce:

```text
Law Execution Unit
```

as a required sub-unit inside a broader autonomous behaviour analysis. It is not a new owner and not a new artifact class that replaces Knowledge Object or Function Graph.

Answer to the refinement question:

```text
LAW_EXECUTION_MODEL_ALONE_IS_NOT_SUFFICIENT
```

Reason:

Law execution begins after the system has already understood the situation and selected the applicable laws. V7 autonomy requires the system to determine what happened, why it happened, which laws and policies apply, what constraints are active, what authority exists, and which action is admissible.

### 9.1 Situation Interpretation Chain

The refactored program should make this chain explicit:

```text
Situation
  -> Interpretation
  -> Applicable Laws
  -> Reasoning
  -> Decision
  -> Execution
  -> Verification
  -> Learning
  -> Improvement
```

This is not a new architecture.

It is the more precise description of the same autonomous evolution route.

### 9.2 Autonomous Behaviour Unit

The broader analytical unit should be:

```text
Autonomous Behaviour Unit
```

This is not a new owner, new program, new Runtime, or new Planner.

It is a schema for Phase 2 and Phase 3 analysis.

Minimum fields:

| Field | Meaning |
|---|---|
| Situation | What is happening in current reality. |
| Situation Source | Production signal, report, CPS state, runtime evidence, test, tool, admin read model, operator input, or engineering evidence. |
| Interpretation | What the situation means and why. |
| Applicable Knowledge | Existing knowledge, laws, policies, models, rules, owners, and evidence relevant to the situation. |
| Applicable Constraints | Authority, policy, blast radius, routing mode, channel/service requirements, freshness, rollback, certification, and production maturity constraints. |
| Reasoning | How the system determines possible actions or no-action. |
| Decision | Chosen decision or terminal no-action/hold/manual-review result. |
| Law Execution Unit | The law-bound execution segment when execution is allowed. |
| Verification | How the result is proven. |
| Rollback / No-Rollback | Recovery, containment, compensation, or no-rollback closure. |
| Learning | What outcome feedback is produced. |
| Canonical Sync | Whether durable knowledge, maps, CPS, OMP, or Production Maturity need synchronization. |
| Human Dependency | What still requires human or Codex participation. |
| Automation State | Current automation state of the whole behaviour chain. |

### 9.3 Law Execution Unit

Inside the Autonomous Behaviour Unit, Law Execution Unit records the execution segment.

Minimum fields:

| Field | Meaning |
|---|---|
| Law / Rule | Existing law, policy, rule, model rule, OMP rule, runtime rule, verification rule, rollback rule, learning rule, or sync rule. |
| Source | Canonical, locked, policy, ADR, runtime, OMP, CPS, report, code, or evidence source. |
| Owner | Existing owner responsible for the law. |
| Intended Execution | What the law requires the system to do. |
| Current Executor | Human, Codex, OMP, Runtime, tool, service, pipeline, test, script, owner, or none. |
| Current Trigger | Manual command, operator action, timer, service event, OMP continuation, production event, test, or report. |
| Current Consumer | Existing consumer of the law output. |
| Verification | How execution is verified. |
| Evidence | Current evidence that execution occurs or does not occur. |
| Automation State | Documented only, manual, semi-automatic, shadow, operator-approved, bounded, production-certified, not applicable, or superseded. |
| Human Dependency | What still requires human participation. |
| Learning Path | Whether outcomes feed learning. |
| Canonical Sync Path | Where durable results go. |

This unit should be embedded into Phase 2 and Phase 3, not introduced as a new owner.

### 9.4 Real V7 Examples

| V7 Area | Situation Interpretation Required Before Law Execution |
|---|---|
| Channel degradation | The system must determine what happened, why it happened, affected service/channel/user scope, required services working or failing, evidence freshness, blast radius, authority, routing mode, applicable hard/soft degradation policy, recovery or no-action path, and allowed decision before any routing law can execute. |
| Engineering Reports | The system must understand whether a report is historical evidence, current execution evidence, durable knowledge candidate, Production Maturity input, CPS update input, or no-sync evidence before report lifecycle laws execute. |
| Knowledge Evolution | The system must understand whether new evidence changes locked knowledge, only refreshes a map, or is report-only before Knowledge Evolution laws apply. |
| OMP | The system must interpret whether a situation is an OMP continuation, certified gap candidate, operator command, production evidence, or terminal no-action before OMP mission rules apply. |
| Runtime | Runtime must know the situation class, freshness, authority envelope, action class, scope, and stop condition before runtime execution laws apply. |
| Verification | The system must understand what claim or mutation is being verified and which owner owns verification before verification laws execute. |
| Rollback | The system must interpret whether rollback, containment, forward-fix, or no-rollback closure applies before rollback laws execute. |
| Learning | The system must understand terminal outcome quality, source reliability, prediction mismatch, and feedback consumer before learning laws execute. |
| Canonical Sync | The system must interpret whether the outcome changes durable truth, current state, implementation map, knowledge map, maturity, or nothing before canonical synchronization laws execute. |

## 10. Phase 2 Refactoring Plan

Current Phase 2:

```text
Current Autonomous System Inventory
```

Recommended Phase 2:

```text
Current Autonomous Reality Model
```

Answer to the main Phase 2 question:

```text
Current Inventory is insufficient by itself.
Phase 2 must build Current Autonomous Reality Model.
```

Required Phase 2 changes:

| Change | Required? | Reason |
|---|---|---|
| Rename output from `CURRENT_AUTONOMOUS_SYSTEM_INVENTORY.md` to a reality-model artifact | YES | The output must include law execution, automation state, manual dependency, structural friction, and evidence map. |
| Add situation discovery | YES | Phase 2 must inventory the situations V7 currently observes or handles, such as degradation, authority stops, verification outcomes, reports, learning signals, and sync needs. |
| Add interpretation discovery | YES | Phase 2 must determine whether the system can interpret what a situation means, not only whether a component exists. |
| Add reasoning discovery | YES | Phase 2 must find how the system selects applicable knowledge, constraints, policies, and possible decisions. |
| Add decision discovery | YES | Phase 2 must show how decisions are made, blocked, escalated, or deferred. |
| Add law/rule discovery | YES | The current Phase 2 categories discover implementation reality but not all laws. |
| Add execution reality matrix | YES | The program must know how each law is actually executed. |
| Add automation state matrix | YES | Canonical goal depends on automation state, not just existence. |
| Add manual dependency inventory | YES | Human participation is the central thing to reduce. |
| Add structural friction inventory | YES | Phase 3 needs evidence of friction without Phase 2 creating gaps. |
| Add unknown/manual review registry | YES | Unresolved reality must not silently become a gap. |
| Preserve "no gap creation" | YES | Phase 2 must stop before certification. |

Recommended Phase 2 output:

```text
docs/reports/research/V7_CURRENT_AUTONOMOUS_REALITY_MODEL.md
```

This aligns with the separate Phase 2 program layer already organized for future execution:

```text
docs/programs/V7_AUTONOMOUS_REALITY_MODEL_PROGRAM.md
```

The parent AEP should not duplicate that entire layer, but it should incorporate the same principles into its Phase 2 definition.

Phase 2 should therefore be organized around:

```text
Situation Discovery
  -> Interpretation Discovery
  -> Reasoning Discovery
  -> Decision Discovery
  -> Law Discovery
  -> Execution Discovery
  -> Automation Discovery
```

not law discovery alone.

## 11. Phase 3 Refactoring Plan

Current Phase 3:

```text
Certified Autonomy Gap Register
```

The phase should remain.

The gap definition must change from any possible reading of "missing function/capability" or even only "law-execution gap" to:

```text
A certified Autonomous Behaviour Gap where V7 cannot yet independently
understand a situation, select applicable existing knowledge and laws,
reason about constraints, decide an allowed action or no-action, execute
through existing owners, verify the result, learn from the outcome, and
synchronize durable consequences.
```

Gap may include:

- situation is observed but not interpreted;
- interpretation exists only in human/Codex reasoning;
- applicable policies or laws are not selected automatically;
- constraints are not resolved automatically;
- decision requires human synthesis;
- law exists only in documents;
- law requires human execution;
- law requires Codex orchestration;
- law has partial implementation but no automatic trigger;
- law has trigger but no verifier;
- law has producer but no consumer;
- law has consumer but no consumption confirmation;
- law has execution but no evidence;
- law has evidence but no learning path;
- law has learning but no canonical sync path;
- law has runtime path but lacks authority;
- law has authority but lacks production certification;
- law has implementation but stale owner mapping.

Gap must not mean:

- simply a missing function;
- a preferred feature;
- a new roadmap item;
- an implementation idea;
- a duplicate of an existing owner responsibility;
- an uncertified operator desire.

Phase 3 should certify Autonomous Behaviour Gaps only after Phase 2 reality evidence.

Law Execution Gap remains a subtype of Autonomous Behaviour Gap.

## 12. OMP Usage Plan

OMP must remain:

```text
the only execution operating system
```

Refactored AEP should state:

- AEP understands and certifies the autonomous evolution path.
- AEP does not execute implementation.
- AEP does not own a mission queue.
- AEP does not prioritize work except as certified input to OMP.
- Phase 3 produces certified Autonomous Behaviour Gap candidates.
- Phase 4 hands those candidates to OMP.
- OMP decides mission creation, sequencing, routing, continuation, and closure.

This preserves the current correct relationship while making the program situation-aware and law-bound.

## 13. Section-by-Section Refactoring Matrix

| Section | Classification | Refactoring Direction |
|---|---|---|
| Purpose | `REQUIRES_REFACTORING` | Add canonical situation-aware autonomous behaviour goal and automation of existing knowledge application. |
| Non-Goals | `FULLY_MATCHES` | Preserve. |
| Existing Owner Discovery | `REQUIRES_NEW_INTERPRETATION` | Add that no owner covers law-execution route as a whole. |
| Knowledge Model | `REQUIRES_REFACTORING` | Add situation, interpretation, applicable-knowledge, law/rule, and execution overlay. |
| Source Resolution | `FULLY_MATCHES` | Preserve; add Law Source Resolution examples. |
| Foundation | `REQUIRES_NEW_INTERPRETATION` | Define Foundation as baseline of executable laws, not only knowledge inputs. |
| Phase Model | `REQUIRES_REFACTORING` | Reframe phase outputs around autonomous behaviour and law-bound execution. |
| Phase 2 | `REQUIRES_ARCHITECTURAL_REFACTORING` | Expand to Current Autonomous Reality Model built around situation, interpretation, reasoning, decision, law, execution, and automation discovery. |
| Phase 3 | `REQUIRES_ARCHITECTURAL_REFACTORING` | Redefine Gap as Autonomous Behaviour Gap, with Law Execution Gap as a subtype. |
| Phase 4 | `REQUIRES_NEW_INTERPRETATION` | OMP mission generation consumes certified Autonomous Behaviour Gaps. |
| Phase 5 | `REQUIRES_NEW_INTERPRETATION` | Structural integration integrates autonomous behaviour through existing owners, including law execution where applicable. |
| Phase 6 | `REQUIRES_NEW_INTERPRETATION` | Production certification certifies autonomous execution of law-bound action classes. |
| Phase 7 | `REQUIRES_REFACTORING` | Continuous loop should monitor situations, interpretation, decisions, execution, learning, and improvement. |
| Producer / Consumer | `FULLY_MATCHES` | Preserve; add law-output examples. |
| Chain Closure | `FULLY_MATCHES` | Preserve. |
| Consumer Confirmation | `FULLY_MATCHES` | Preserve. |
| Gap Model | `REQUIRES_REFACTORING` | Add Autonomous Behaviour Gap definition and retain Law Execution Gap as subtype. |
| Gap Priority | `REQUIRES_REFACTORING` | Add law criticality, human dependency, execution frequency, learning impact. |
| Artifact Lifecycle | `REQUIRES_REFACTORING` | Add current reality model and law-execution matrices. |
| Definition Of Done | `REQUIRES_REFACTORING` | Add law coverage and automation-state completeness. |
| Canonical Sync | `REQUIRES_NEW_INTERPRETATION` | Sync durable law-execution findings through existing owners. |
| Reality Model | `REQUIRES_ARCHITECTURAL_REFACTORING` | Make explicit as Phase 2 core. |
| Continuous Evolution | `REQUIRES_REFACTORING` | Loop should start from situation observation and interpretation quality, not only execution observation. |
| Relationship with OMP | `FULLY_MATCHES` | Preserve; clarify autonomous-behaviour-gap handoff. |
| Relationship with Runtime | `REQUIRES_NEW_INTERPRETATION` | Runtime executes only authorized law-bound actions. |
| Relationship with CPS | `REQUIRES_NEW_INTERPRETATION` | CPS records current law execution reality and blockers. |
| Relationship with Production Maturity | `REQUIRES_NEW_INTERPRETATION` | Maturity consumes law-execution evidence and automation state. |
| Relationship with Knowledge Evolution | `FULLY_MATCHES` | Preserve; law changes use Knowledge Evolution. |

## 14. New Principles To Add

The refactored program should add these principles:

| Principle | Meaning |
|---|---|
| Law-First Evolution Principle | The primary object of analysis is an existing V7 law or rule, not a file, function, document, or desired feature. |
| Situation-First Autonomy Principle | A law cannot be applied autonomously until the system understands the situation in which the law applies. |
| Interpretation Before Execution Principle | Observation must become interpreted situation before decision or execution. |
| Applicable Knowledge Selection Principle | The system must select applicable laws, policies, rules, owners, constraints, and evidence before deciding. |
| Autonomous Behaviour Gap Principle | A certified gap may exist at situation understanding, interpretation, reasoning, decision, execution, verification, learning, or improvement. |
| Execution Reality Principle | A law is not operationally real until its current executor, trigger, consumer, verification, and evidence are known. |
| Automation State Principle | Every law must have an automation state. |
| Human Dependency Principle | Manual participation must be recorded explicitly and may later become a certified gap only in Phase 3. |
| Existing Knowledge Execution Principle | The program should automate execution of existing knowledge before proposing new capabilities. |
| Law Gap Principle | A certified gap is a missing, partial, manual, unverified, unconsumed, unauthorised, or uncertified execution path for an existing law. |
| Feedback Closure Principle | Autonomous evolution is incomplete unless outcomes feed learning and canonical synchronization where applicable. |
| Discover Reuse Extend Implement Principle | The program must discover existing law, reuse existing owner, extend only when necessary, and implement only through OMP/existing owners. |

No new owner is required for these principles.

## 15. Step-By-Step Full Refactoring Plan

1. Preserve all current non-goals and owner boundaries.
2. Update Purpose to state the canonical situation-aware autonomous behaviour goal explicitly.
3. Add a Situation-Aware Autonomous Behaviour Model after Knowledge-Driven Source Resolution.
4. Add Law / Rule Source Resolution rules without replacing Knowledge Categories.
5. Define Autonomous Behaviour Unit as the primary analytical schema, not a new owner.
6. Define Law Execution Unit as a subordinate execution schema inside Autonomous Behaviour Unit.
7. Reinterpret Foundation as the baseline of locked/canonical knowledge and laws available for situation interpretation and execution.
8. Update Phase Knowledge Requirements to include situation, interpretation, reasoning, decision, law/rule, and automation discovery where needed.
9. Refactor Phase 2 from Current Autonomous System Inventory to Current Autonomous Reality Model.
10. Add Phase 2 required outputs: Situation Inventory, Interpretation Matrix, Reasoning Matrix, Decision Matrix, Law Inventory, Execution Reality Matrix, Automation State Matrix, Manual Dependency Inventory, Structural Friction Inventory, Evidence Map.
11. Refactor Phase 3 Gap definition to Autonomous Behaviour Gap.
12. Keep Law Execution Gap as a subtype of Autonomous Behaviour Gap.
13. Update Gap Certification Rules to include situation interpretation, applicable knowledge selection, reasoning, decision, law execution, automation state, human dependency, feedback, and sync checks.
14. Update Gap Priority Model with situation criticality, law criticality, human-dependency reduction, production impact, learning impact, and decision safety.
15. Clarify Phase 4 as OMP mission generation from certified Autonomous Behaviour Gaps only.
16. Clarify Phase 5 as existing-owner integration of autonomous behaviour and law execution.
17. Clarify Phase 6 as certification of autonomous execution of law-bound action classes after situation interpretation and decision are proven.
18. Refactor Phase 7 loop to start with observation of current situations, interpretation quality, decision quality, execution quality, and learning.
19. Update Artifact Lifecycle to include Current Autonomous Reality Model, situation/interpretation/reasoning/decision matrices, and law-execution matrices.
20. Update Artifact DoD to include situation coverage, interpretation coverage, applicable-law coverage, decision coverage, execution coverage, automation-state coverage, and feedback closure.
21. Update Canonical Synchronization Matrix to include durable autonomous-behaviour findings.
22. Update Acceptance Model to require Autonomous Behaviour Review and Law Execution Review.
23. Re-run Architecture Review, Quality Review, OMP Review, Autonomous Behaviour Review, Law-Execution Review, Duplication Review, and Self Review.

## 16. Final Planning Verdict

```text
PROGRAM_REFACTORING_REQUIRED
```

The existing Autonomous Evolution Program is architecturally sufficient as the parent route, but it must be refactored to make Autonomous Behaviour the primary analytical and evolutionary unit.

Refinement verdict:

```text
LAW_EXECUTION_MODEL_ALONE_IS_NOT_SUFFICIENT
SITUATION_INTERPRETATION_REASONING_DECISION_MODEL_REQUIRED
```

The more accurate primary unit is Autonomous Behaviour:

```text
Situation
  -> Interpretation
  -> Applicable Laws
  -> Reasoning
  -> Decision
  -> Execution
  -> Verification
  -> Learning
  -> Improvement
```

The route should remain.

The owners should remain.

OMP should remain the only executor.

Phase 2 must become the Current Autonomous Reality Model, organized around Situation Discovery, Interpretation Discovery, Reasoning Discovery, Decision Discovery, Law Discovery, Execution Discovery, and Automation Discovery.

Phase 3 must certify Autonomous Behaviour Gaps, not missing functions. Law Execution Gap remains a subtype.

No new architecture, owner, roadmap, OMP, Runtime, Function Graph, Knowledge Graph, or truth source is required.

This is a more precise description of the same program, not a new architecture.
