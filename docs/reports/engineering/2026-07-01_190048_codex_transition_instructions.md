# V7 Codex Transition Instructions

Status: `CODEX_TRANSITION_HANDOFF`
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Created: `2026-07-01`

This file is a handoff instruction for another Codex/GPT chat.
It is not a new canonical owner, not a roadmap, not an OMP replacement, and not a second truth source.

Use it to enter the project without losing the thread.

## 1. One-Screen Start Prompt For New Codex

Paste this first:

```text
You are continuing V7 Vozduh in workspace:
/Users/ponch/Documents/New project
branch:
Updatesystem

Read first:
- docs/reports/engineering/2026-07-01_190048_codex_transition_instructions.md
- docs/reports/engineering/2026-07-01_172201_gpt_handoff_package.md
- docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md
- docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
- docs/programs/V7_CURRENT_PROGRAM_STATE.md
- docs/reference/V7_CANONICAL_REFERENCE.md
- docs/reference/SYSTEM_MAP.md
- docs/reference/V7_RUNTIME_MODEL.md
- docs/reference/V7_DECISION_MODEL.md
- docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md

Rules:
- Do not redesign.
- Do not create new owners.
- Do not create new Runtime, Planner, Authority, OMP, Event bus, Wake system, Truth source, or roadmap.
- Discover -> Reuse -> Extend -> Implement.
- Reports go to docs/reports/engineering/.
- Chat output must be short; long analysis goes into files.

Current known focus:
L3 one-user Production Validation is blocked because Planner emits L3-executable failover from broad current_egress_not_eligible without same-subject required-service failure evidence for awg0.

Latest root report:
docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md
```

## 2. Project Essence

V7 Vozduh is a governed autonomous routing and control-plane project for production connectivity.

It is not simply a VPN manager or autoswitch script.
The product is a safety-governed system that:

1. observes production reality;
2. builds a world model;
3. plans safe routing actions;
4. executes only under valid authority;
5. verifies results;
6. rolls back or contains failed execution;
7. learns from real outcomes;
8. advances autonomy through OMP certification.

The long arc is:

```text
Reality
  -> Evidence
  -> Knowledge
  -> Decision
  -> Authority
  -> Runtime Execution or STOP_SAFE
  -> Verification
  -> Rollback / Success / No Execution
  -> Learning
  -> Production Maturity
  -> OMP
  -> Next Capability
```

The moral center:

```text
Keep users online, but never fake certainty.
```

If V7 cannot prove safety, authority, freshness, source/target eligibility, rollback, verification, and blast-radius bounds, it must stop safely.

## 3. Current State In Plain Language

Architecture work is considered complete by the current project history.
Future work should proceed through OMP and existing owners.

The active capability is:

```text
L3 Emergency Autonomous Failover
```

Current goal:

```text
Complete the first legal one-user L3 Production Validation.
```

This means one real user may be moved only if all existing gates pass.
No broad automation.
No timer-based movement.
No batch movement.
No authority expansion.
No new runtime path.

Latest known production validation target:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
```

Latest known STOP result:

```text
apply_executed: false
users_moved: 0
current_failures: []
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
```

Latest root conclusion:

```text
Planner overclassified broad current candidate ineligibility as L3 failover.
```

Exact report:

```text
docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md
```

## 4. Source Hierarchy

When files disagree, use this order.

| Rank | Source | Role |
| --- | --- | --- |
| 1 | Product Specification | Highest product intent. |
| 2 | `docs/reference/V7_CANONICAL_REFERENCE.md` | Current durable truth. |
| 3 | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Execution program and maturity scheduler. |
| 4 | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Volatile current state, may lag latest report if not updated. |
| 5 | `docs/reference/SYSTEM_MAP.md` | Owner and topology lookup. |
| 6 | `docs/reference/V7_RUNTIME_MODEL.md` | Runtime laws, work placement, execution lifecycle. |
| 7 | `docs/reference/V7_DECISION_MODEL.md` | Decision semantics and action vocabulary. |
| 8 | `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | Stable autonomous Runtime Operating System contract. |
| 9 | `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` | Autonomy ladder and execution philosophy. |
| 10 | `docs/reference/capabilities/` | Capability contracts such as L3. |
| 11 | `docs/policies/` | Operational policies. |
| 12 | `docs/decisions/` | ADR decisions. |
| 13 | Source code and tests | Executable truth for implementation reality. |
| 14 | `docs/reports/engineering/` | Historical evidence, not canonical truth by itself. |

Reports can prove what happened.
Reports do not define permanent truth unless durable knowledge is promoted to the correct canonical owner.

## 5. Main Directory Map

| Path | Meaning |
| --- | --- |
| `docs/product/` | Product-level specification and product intent. |
| `docs/reference/` | Canonical references, architecture, Runtime, Decision, maps, models. |
| `docs/reference/capabilities/` | Capability contracts. Current key file: `L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`. |
| `docs/programs/` | OMP, Current Program State, Implementation Program, Backlog. |
| `docs/policies/` | Canonical policy library: hard failure, authority, rollback, freshness, anti-flap, blast radius, etc. |
| `docs/decisions/` | ADRs. Use when a durable decision changes. |
| `docs/reports/engineering/` | Standard engineering reports for audits, implementation, validation, deployment, production traces. |
| `docs/reports/` | Older or broad evidence sets and certification artifacts. |
| `docs/research/` | Research evidence; not implementation truth. |
| `admin_core/` | Core Python owners for admin surfaces, execution pipeline, feedback, read models, intelligence. |
| `admin/` | Admin API/UI surface. |
| `tools/` | Operational CLIs and runtime tools. Important: `v7-users-autoswitch`, safe deploy, truth/convergence, governed cycle. |
| `tests/` | Unit/integration tests. |

## 6. What Each Core File Is For

### Program / Truth Files

| File | Purpose | How to use |
| --- | --- | --- |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Permanent production operating program. | Read before "continue OMP" or production/certification work. |
| `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Volatile state and current bottleneck. | Update only if volatile operational state changes. Check freshness. |
| `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` | Implementation queue when OMP selects backlog work. | Do not create new backlog unless impossible to reuse. |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Durable project truth. | Update only when durable meaning changes. |
| `docs/reference/SYSTEM_MAP.md` | Owner lookup and topology. | Use to find existing owners and avoid duplicates. |
| `docs/reference/V7_RUNTIME_MODEL.md` | Runtime laws and Work Placement. | Use for runtime/execution/freshness/STOP_SAFE reasoning. |
| `docs/reference/V7_DECISION_MODEL.md` | Decision semantics and action vocabulary. | Use when classifying actions: KEEP/MOVE/FAILOVER/DRAIN/PROBE/etc. |
| `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | Autonomous runtime operating contract. | Use for L3-L7 runtime orchestration; do not replace Runtime Model. |
| `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` | Autonomy execution ladder. | Use for certification and autonomy stage meaning. |
| `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` | L3 capability contract. | Use for exact L3 entry, wake, authority, execution, verification, rollback rules. |

### Policy Files

| File | Purpose |
| --- | --- |
| `docs/policies/POLICY_001_HARD_FAILURE.md` | Hard failure semantics and failover inspiration. |
| `docs/policies/POLICY_004_AUTHORITY.md` | Authority, emergency/break-glass, least privilege. |
| `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md` | Action-class promotion rules. |
| `docs/policies/POLICY_006_BLAST_RADIUS.md` | Blast-radius bounds. |
| `docs/policies/POLICY_007_ROLLBACK.md` | Rollback/no-rollback behavior. |
| `docs/policies/POLICY_008_FRESHNESS.md` | Freshness windows and stale evidence handling. |
| `docs/policies/POLICY_009_ANTI_FLAP.md` | Anti-flap and movement protection. |

### Code Owners

| File / module | Owns |
| --- | --- |
| `tools/v7-users-autoswitch` | Planner/autoswitch, candidate generation, selected moves, apply path, L3 gates, verification/rollback handling. |
| `admin_core/operator_execution_pipeline.py` | Canonical governed/operator execution pipeline. |
| `admin_core/operator_execution.py` | Packet/selected-move materialization, approved plan lock, restore barrier clearance, execution artifacts. |
| `admin_core/operator_execution_feedback.py` | Terminal outcome feedback/classification. |
| `admin_core/operator_decision_surface.py` | Operator decision/read surface. |
| `admin_core/autonomy_trust_acceleration.py` | Evidence/trust/read-only capability and maturity surfaces. |
| `admin_core/intelligence_workers.py` | Intelligence/evidence materialization. |
| `admin_core/intelligence_snapshots.py` | World/read-model snapshots. |

## 7. Where To Store Reports

All meaningful engineering work must create a report here:

```text
docs/reports/engineering/
```

Recommended filename:

```text
YYYY-MM-DD_HHMMSS_short_slug.md
```

Examples:

```text
docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md
docs/reports/engineering/2026-07-01_190048_codex_transition_instructions.md
```

Reports must include only what is needed for that task.
The user asked not to paste long reports into chat.
Chat should contain only the most important result and the path.

Every report should normally include:

```text
Summary
Inputs read
Source files/state inspected
Evidence
Owner
Exact file/function if code-related
Result / blocker
Need New Owner?
Need New Backlog?
Need New Architecture?
Canonical updates or NONE
Next OMP step
Final verdict
```

Implementation reports should also include:

```text
Files changed
Tests run
Truth result
Convergence result
Production impact
Rollback plan
```

## 8. How To Work In This Project

Default method:

```text
Discover
  -> Semantic Reuse
  -> Canonical Reuse
  -> Owner Reuse
  -> Extend Existing Owner
  -> Implement only if required
  -> Verify
  -> Engineering Report
  -> Canonical update only if durable knowledge changed
  -> Current Program State update only if volatile state changed
  -> Continue OMP
```

Before implementation:

1. Search for existing equivalent semantics.
2. Search owner map.
3. Search code for existing function/module/path.
4. Search tests.
5. Prove no duplicate owner/path is being created.

Do not create:

- new Runtime;
- new Planner;
- new Authority model;
- new OMP;
- new roadmap;
- new event bus;
- new wake source;
- new truth source;
- new owner;
- new backlog item;
- new architecture document;
- parallel execution path.

Default answers unless proven impossible:

```text
Need New Owner = FALSE
Need New Backlog = FALSE
Need New Architecture = FALSE
Need New Runtime = FALSE
Need New Planner = FALSE
Need New Authority = FALSE
```

## 9. Ideal Relationship Between Documents

The ideal chain is:

```text
Product Specification
  -> Canonical Reference
  -> OMP
  -> Current Program State
  -> SYSTEM_MAP
  -> Runtime Model
  -> Decision Model
  -> Capability Contract
  -> Policies / ADRs
  -> Existing Code Owner
  -> Tests
  -> Runtime / Production Validation
  -> Engineering Report
  -> Durable Knowledge Promotion
  -> Current Program State / OMP Next Step
```

Each layer has a job:

| Layer | Must do | Must not do |
| --- | --- | --- |
| Product | Define why V7 exists. | Implement. |
| Canonical Reference | Preserve durable truth. | Become a report log. |
| OMP | Decide what work happens next. | Become a code owner or second runtime. |
| Current Program State | Store current volatile state. | Redefine architecture. |
| SYSTEM_MAP | Map owners and topology. | Become the canonical content for every owner. |
| Runtime Model | Define execution laws. | Create daemon/timer/apply code by itself. |
| Decision Model | Define decision semantics. | Execute movement. |
| Capability Contract | Define bounded capability behavior. | Expand authority. |
| Policies | Define operational constraints. | Select candidates by themselves. |
| Code owner | Implement existing owner responsibility. | Invent new architecture silently. |
| Tests | Prove behavior. | Replace production proof. |
| Reports | Preserve evidence. | Become permanent truth alone. |

## 10. Ideal Relationship Between Runtime Planes

The Work Placement Law says every computation must have one canonical plane.

```text
Observation Plane
  -> World Model Plane
  -> Planning Plane
  -> Execution Plane
  -> Verification Plane
  -> Feedback / Learning Plane
  -> OMP / Certification Plane
```

| Plane | Owns | Must produce | Consumed by |
| --- | --- | --- | --- |
| Observation | Raw production reality, probes, service matrix, channel/user state. | Fresh evidence. | World Model, Planner, Runtime gates. |
| World Model | Compact reality/read models. | Consumable facts. | Planner and OMP. |
| Planning | Candidate universe, chosen action, reasons, blockers. | Decision/selected move. | Packet/lock/runtime. |
| Execution | Authority-bound apply-or-stop path. | Apply, STOP_SAFE, terminal execution state. | Verification/rollback/learning. |
| Verification | Post-action proof. | Pass/fail/timeout. | Rollback or terminal classification. |
| Feedback/Learning | Terminal outcome learning. | Evidence/trust/prediction changes. | OMP, maturity, future planning. |
| OMP/Certification | Maturity, certification, next action. | Continue/stop/certify/blocked state. | Current Program State, next capability. |

No plane may silently replace another.
Planner cannot become Runtime.
Runtime cannot become Planner.
Reports cannot become OMP.
Dashboard cannot become Authority.

## 11. Current L3 Root Cause Context

Latest root report:

```text
docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md
```

Finding:

```text
FIRST_DIVERGENCE_FOUND
```

First divergent fact:

```text
move_type=failover was emitted from broad current_egress_not_eligible
without same-subject required-service failure on awg0.
```

Producer:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

Consumer:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence()
tools/v7-users-autoswitch::_l3_wake_decision()
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
```

Owner:

```text
existing Planner/autoswitch owner
```

Minimal correction direction:

```text
Planner must not emit L3-executable failover from broad current_egress_not_eligible
unless the selected current source carries same-subject required-service failure evidence.
Otherwise emit a non-L3 advisory/recheck/wait/blocked outcome through existing semantics.
```

Do not solve this by weakening Runtime.
Runtime is correct to require `required_service_failure_required` and `confirmed_l3_wake_required`.

## 12. Important Historical Reports For Current Thread

Read in this order for the L3 issue:

| File | Why it matters |
| --- | --- |
| `docs/reports/engineering/2026-07-01_172201_gpt_handoff_package.md` | Broad project and current-state handoff. |
| `docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md` | Good path vs production path comparison. |
| `docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md` | Proves semantic break at decision depth. |
| `docs/reports/engineering/2026-07-01_151234_formal_model_verification.md` | Formal model: Planner partially conforms; Runtime stop is correct. |
| `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md` | Serialization defect was fixed; current blocker is not restore/serialization. |
| `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md` | First violated invariant: failover semantic binding. |
| `docs/reports/engineering/2026-07-01_185831_world_model_provenance_trace.md` | Latest root trace and current best actionable conclusion. |

## 13. Practical Code Navigation For L3

Start here:

```text
tools/v7-users-autoswitch
```

Important functions:

| Function | Purpose |
| --- | --- |
| `_decision_for_user()` | Produces keep/switch and `move_type`; current root owner. |
| `_candidate()` | Builds candidate with service, quality, load, safety gates. |
| `_service_suitability()` | Builds service suitability evidence. |
| `_gate_service()` | Applies service evidence/failure gates. |
| `_gate_service_failures()` | Blocks persistent failures and handles transient failures. |
| `_candidate_json()` | Serializes candidate semantics into decision output. |
| `_select_moves()` | Selects movements from decisions. |
| `_emergency_failover_move_evidence()` | Runtime extracts L3 evidence from selected move. |
| `_l3_wake_decision()` | Accepts/rejects L3 wake from failures. |
| `_emergency_failover_authority_gate()` | Final L3 authority/eligibility gate before selected move survives. |
| `_run_switch()` | Actual user movement path. Do not bypass gates to reach it. |

Packet/lock/restore path:

```text
admin_core/operator_execution.py
```

Important functions:

| Function | Purpose |
| --- | --- |
| `selected_moves_from_plan()` | Preserves selected move semantic payload. |
| `approved_plan_lock_from_selected()` | Writes approved plan lock. |
| `build_restore_barrier_clearance()` | Builds restore barrier clearance with approved plan lock. |

Canonical operator pipeline:

```text
admin_core/operator_execution_pipeline.py
```

Use it when the task says Production Validation or governed/operator execution should route through canonical owner.

## 14. Runtime Safety Rules That Must Not Be Weakened

Do not bypass:

- freshness;
- authority generation;
- source eligibility;
- target eligibility;
- required-service failure for L3;
- confirmed L3 wake;
- restore barrier;
- approved plan lock;
- selected move hash;
- user/source/target identity;
- rollback/no-rollback readiness;
- verification readiness;
- anti-flap;
- movement protection;
- blast radius;
- capacity/load gates;
- policy gates;
- fail-closed behavior.

For L3 specifically:

```text
current_egress_not_eligible alone is not enough.
```

L3 needs:

```text
current channel failed
AND affected user on that channel
AND required service failure on that same current channel
AND safe target
AND authority
AND all live gates
```

## 15. How To Update Canonical Knowledge

Only update canonical docs if durable system meaning changed.

Examples requiring canonical update:

- a new permanent rule;
- changed owner responsibility;
- changed OMP semantics;
- changed Runtime law;
- changed capability contract;
- changed policy meaning;
- changed action-class semantics.

Examples not requiring canonical update:

- one production trace;
- one failed validation;
- one implementation bug report;
- one test result;
- one transient live state snapshot;
- a report that only confirms existing rules.

If durable knowledge changed:

1. Update the specific canonical owner.
2. Update `docs/reference/V7_CANONICAL_REFERENCE.md` only if it needs durable cross-reference.
3. Update `docs/reference/SYSTEM_MAP.md` only if owner/topology lookup changed.
4. Add/update ADR only if a decision changed.
5. Create engineering report explaining the update.

## 16. How To Respond In Chat

The user prefers short chat output.

Do:

```text
Сделано. Отчет: <path>
Главный вывод: ...
Следующий шаг: ...
```

Do not paste long reports into chat.
Put long reasoning in files.

When the task has a strict final-output format, follow it exactly.

## 17. Production / Network Caution

Do not move users unless the user explicitly authorizes the exact production action and the task requires execution.

Read-only production/API checks are allowed only when needed and should be explicitly treated as read-only.

Never call apply/mutation endpoints during audits.

Do not enable:

- runtime automation;
- timers;
- daemon movement;
- broad autoswitch;
- batch movement;
- authority expansion.

## 18. Verification Commands

Use as required by task class:

```text
tools/v7-truth-check --all --json
tools/v7-convergence-status --json
```

Relevant tests depend on touched owner.
For L3/autoswitch work, search tests first:

```text
rg -n "L3|emergency|current_failures|current_egress_not_eligible|failover" tests tools admin_core
```

Do not run broad production actions when the task is read-only.

## 19. Current Recommended Next Work

If the next user asks to implement the current L3 fix, the likely narrow implementation target is:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

The implementation should enforce:

```text
Only emit L3-executable move_type=failover when same-subject required-service failure evidence exists on the current source.
```

If current is ineligible for another reason, use existing non-L3 semantics rather than L3 failover.

Tests needed:

1. Good L3 path still emits failover and reaches Runtime evidence.
2. Production-shaped `current_egress_not_eligible` without required-service failure does not emit L3 failover.
3. Runtime still STOP_SAFE when `current_failures` is empty.
4. Serialization still preserves semantic fields.
5. No duplicate planner/runtime/authority path is created.

## 20. Stop Conditions For New Codex

Stop and report only the blocker if:

- task requires production movement but no explicit authority exists;
- production candidate fails a live safety gate;
- command would create a new owner/architecture;
- code change would weaken Runtime safety;
- implementation would duplicate an existing owner;
- exact current state cannot be reproduced and no persisted evidence exists;
- task asks for architecture research after the current implementation/debugging path is already proven.

## 21. Final Mental Model

V7 is not trying to "move users as fast as possible."

V7 is trying to become a trustworthy autonomous production control plane.

Trustworthy means:

```text
one truth per concept
one owner per responsibility
one plane per computation
one authority envelope per execution
one terminal outcome per transaction
one learning path from reality
```

The right instinct in this codebase is not to invent.
The right instinct is to trace:

```text
Who produced this?
Who consumed it?
Did behavior change?
Did the next output appear?
Did a legal terminal consumer receive it?
```

If the chain breaks, fix the existing broken link.
Do not build a parallel chain beside it.

## Final Handoff Verdict

CODEX_TRANSITION_HANDOFF_COMPLETE
