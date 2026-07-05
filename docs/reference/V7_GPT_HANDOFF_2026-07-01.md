# V7 Vozduh GPT Handoff

Status: transfer package for a new GPT/Codex chat
Created: 2026-07-01
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

This file is a handoff, not a new truth source.

If this file conflicts with canonical owners, use this priority:

1. `docs/product/V7_PRODUCT_SPECIFICATION.md`
2. `docs/reference/V7_CANONICAL_REFERENCE.md`
3. `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
4. `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
5. `docs/reference/SYSTEM_MAP.md`
6. `docs/reference/V7_RUNTIME_MODEL.md`
7. `docs/reference/V7_DECISION_MODEL.md`
8. `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md`
9. `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
10. `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
11. Latest engineering reports under `docs/reports/engineering/`

Engineering reports are evidence. Canonical documents are durable truth. Chat is not durable truth.

## Paste This Into The New GPT Chat

You are taking over work on V7 Vozduh in `/Users/ponch/Documents/New project`, branch `Updatesystem`.

Do not restart architecture research. The current work is implementation/debugging inside existing owners. Architecture is closed by default.

Read this handoff first, then read the current canonical owners and latest reports listed in the "Immediate Read List" section.

The current exact technical problem:

```text
L3 Production Validation cannot reach user movement because Planner emits an L3-shaped failover candidate from broad `current_egress_not_eligible`, but Runtime correctly requires same-subject required-service failure evidence for the selected current source.

Latest production candidate:
  user: 10.7.0.5
  source: awg0
  target: vless
  reason: current_egress_not_eligible
  move_type: failover
  current_failures: []
  blockers:
    - required_service_failure_required
    - confirmed_l3_wake_required

Latest differential proof:
  FIRST_DIVERGENCE_FOUND
  divergent field: selected_move.candidates[current_source].service_suitability.per_service[required_service]
  divergent function: tools/v7-users-autoswitch::_emergency_failover_move_evidence
  root executable reason: good path has telegram DOWN/PERSISTENT_FAIL/FRESH on current source; production awg0 has no Runtime-verifiable required-service failure.
```

Do not propose new architecture, new Runtime, new Planner, new owner, new event bus, new wake source, new authority model, or new OMP.

The likely next implementation direction, if the user asks to patch:

```text
Inside existing Planner/Autoswitch owner only, prevent `move_type=failover` from being L3-executable when the selected user/source/target lacks same-subject current-channel required-service failure evidence.

If current egress is merely not eligible but required-service failure is absent, Planner should not emit L3-executable failover. It should emit a non-L3 outcome such as PROBE_ONLY / WAIT / ASK_OPERATOR / NO_ACTION / non-L3 MOVE, depending on existing vocabulary and code paths.

Runtime must continue STOP_SAFE when current_failures is empty.
```

## Project Identity

V7 Vozduh is a production connectivity and autonomous routing control-plane project.

Its purpose is to keep users online by:

- observing real production state;
- understanding users, channels, services, cohorts, and risk;
- selecting safe routing actions through existing owners;
- executing only under valid authority;
- preserving blast-radius limits;
- verifying outcomes;
- rolling back or containing failures;
- learning from real evidence;
- advancing maturity through OMP.

The project is not "automation for automation's sake." The product philosophy is governed autonomy: build toward autonomous execution, but only after proof, certification, authority, and runtime safety are all present.

## Moral / Operating Philosophy

V7 is built around a few moral engineering commitments:

1. Reality first.
   Production facts, truth checks, convergence, real outcomes, and executable traces beat opinions, labels, dashboards, or reports.

2. Safety is not theater.
   If the system cannot prove freshness, authority, rollback, verification, blast radius, service failure, or target safety, it must `STOP_SAFE`.

3. No synthetic maturity.
   Reports, simulations, dry-run previews, advisory scores, and read models are useful only if consumed by a real executable owner. They do not become production evidence by themselves.

4. Authority is bounded.
   Authority must be explicit, scoped, and consumed by Runtime. It does not expand itself. Operator approval is not a general autonomy grant.

5. Runtime must stay thin.
   Runtime consumes prepared knowledge and applies live gates. Runtime must not become the planner, classifier, research engine, certification owner, or dashboard brain.

6. Existing owners win.
   Every task follows:

```text
Discover
  -> Semantic Reuse
  -> Canonical Reuse
  -> Owner Reuse
  -> Extend Existing Owner
  -> Implement only if required
```

7. The user does not want long reports in chat.
   Put long audits/reports into files. In chat, return only the verdict, path, and the most important conclusion.

## Current Human Context

The operator is frustrated by repeated manual approvals and wants real autonomous user movement. That frustration is valid: earlier exact-packet approval workflows created loops and were replaced by bounded governed transactions.

However, the current L3 issue is not solved by "just approve it." Runtime is correctly stopping because the selected production candidate does not prove L3 emergency conditions on the selected source.

The correct tone with the user:

- be direct;
- do not hide behind architecture;
- do not flood chat;
- write full reports to files;
- name the exact executable blocker;
- when implementation is requested, patch the narrow existing owner only;
- do not reopen foundational architecture unless the implementation contradicts it.

## Architecture In One Page

V7 is organized by planes:

```text
Observation Plane
  -> World Model Plane
  -> Planning Plane
  -> Execution Plane
  -> Verification Plane
  -> Feedback / Learning Plane
  -> OMP / Certification Plane
```

Core owners:

| Area | Owner / source |
| --- | --- |
| Product intent | `docs/product/V7_PRODUCT_SPECIFICATION.md` |
| Canonical truth | `docs/reference/V7_CANONICAL_REFERENCE.md` |
| Owner lookup | `docs/reference/SYSTEM_MAP.md` |
| Runtime behavior | `docs/reference/V7_RUNTIME_MODEL.md` |
| Decision vocabulary | `docs/reference/V7_DECISION_MODEL.md` |
| Maturity program | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Current volatile state | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Autonomous execution | `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` |
| Runtime Operating System | `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` |
| L3 capability contract | `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` |
| Planner/autoswitch | `tools/v7-users-autoswitch` |
| Governed execution CLI | `tools/v7-governed-canary-dry-run-cycle` |
| Packet/lock/restore barrier | `admin_core/operator_execution.py` |
| Execution pipeline | `admin_core/operator_execution_pipeline.py` |
| Feedback/outcome | `admin_core/operator_execution_feedback.py` |
| Maturity/read models | `admin_core/autonomy_trust_acceleration.py` |

## Runtime Model

Runtime is a thin execution path:

```text
Wake
  -> Observe
  -> Incident
  -> Planner
  -> Authority
  -> Eligibility
  -> Execute or STOP_SAFE
  -> Verify
  -> Rollback / Contain
  -> Learn
  -> Report
  -> Sleep
```

Runtime must:

- consume prepared knowledge;
- revalidate live safety gates;
- preserve selected identity;
- fail closed on missing or contradictory evidence;
- never invent decisions;
- never promote action classes;
- never expand authority.

## Decision Model

Decision vocabulary includes things like:

```text
KEEP
MOVE
FAILOVER
DRAIN
QUARANTINE
RECOVER
PROBE_ONLY
ASK_OPERATOR
NO_ACTION
WAIT
```

Important distinction:

```text
FAILOVER as decision vocabulary
  !=
L3 executable emergency failover truth
```

For L3 execution, Runtime needs composite truth:

```text
same assigned user
+ same failed current channel
+ required services failed on that current channel
+ safe target
+ fresh evidence
+ valid L3 authority
+ selected move identity matches
+ restore barrier valid
+ rollback ready
+ verification ready
+ blast/budget/movement gates pass
= EXECUTION_READY
```

If this is not true, Runtime must `STOP_SAFE`.

## OMP

OMP is the single execution program. It owns maturity order, certification, capability progression, and engineering discipline.

Recent OMP state is complicated:

- architecture is complete;
- many A/B/C/RT2 items are marked read-only complete;
- L3 implementation and production candidate work occurred;
- L3 safe deploy passed;
- runtime validation/truth/convergence passed at several stages;
- first L3 production validation remains blocked by executable evidence semantics.

Do not treat "implementation complete" as "production certified." Production certification requires real production validation and evidence closure.

## L3 Capability

L3 Emergency Autonomous Failover exists to restore user connectivity after confirmed current-channel failure.

Allowed:

- detect failed current channel;
- detect affected users;
- identify required services affected by the failed current channel;
- find safe target;
- execute bounded failover only inside certified/approved scope;
- verify;
- rollback/contain;
- learn;
- update evidence and OMP.

Forbidden:

- rebalance;
- preference movement;
- capacity optimization;
- cleanup;
- target optimization;
- movement without fresh failure evidence;
- timer/cron/broad loop movement;
- authority expansion;
- Runtime class promotion.

L3 entry conditions include:

```text
current channel failed
users affected
required services failed on current channel
safe target exists
fresh evidence
authority allows L3
restore ready
rollback ready
verification ready
```

Any false/unknown condition -> `STOP_SAFE`.

## What Was Already Fixed

Major recent resolved issues:

1. Exact packet approval loop.
   Fixed conceptually and materially via Decision Commit / Governed Execution Transaction work. Authority can bind to a bounded transaction/decision rather than stale exact packet in the governed workflow.

2. Terminal outcome classification.
   Runtime classification now uses final terminal transaction state, not intermediate `apply_result`. Rollback success is not counted as success.

3. OMP Execution Closure / Verified Consumption.
   OMP now requires output produced, consumed, consumption verified, behavior changed, next output produced, and terminal consumer verified before a capability is complete.

4. L3 implementation and closure.
   L3 phases created real code paths for authority, wake, incident, planner integration, eligibility, execution, verification, rollback, behavior contracts, UI surface, tests, and production validation ladder.

5. Production promotion and safe deploy.
   L3 production candidate was sealed and safely deployed; truth and convergence passed.

6. Authority envelope gate.
   A prior blocker where one-user production validation was rejected for lacking certified autonomy was narrowed/fixed. One-user production validation can consume current approved emergency envelope without broad autonomy.

7. Serialization defect.
   `approved_plan_lock.selected_moves` used to strip semantic Planner fields. Fixed in `admin_core/operator_execution.py`, `tools/v7-governed-canary-dry-run-cycle`, and tests. Semantic fields such as `reason`, `important_services`, `candidates`, `scores`, and `service_failover` now survive.

## Current Exact Blocker

After those fixes, the latest L3 production validation still stops safely:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
approved_plan_lock_validation.ok: true
semantic fields preserved: true
current_failures: []
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
apply_executed: false
users_moved: 0
```

The current root cause is not packet, restore barrier, authority envelope, or serialization.

The current root cause is:

```text
Planner emits an L3-shaped `failover` selected move from broad `current_egress_not_eligible`,
but the selected source `awg0` does not carry Runtime-verifiable required-service failure evidence.
```

Good L3 path:

```text
current source: 1
required service: telegram
telegram.available: false
telegram.status: DOWN
telegram.truth_class: PERSISTENT_FAIL
telegram.freshness: FRESH
current_failures:
  - telegram
wake: ACCEPT_WAKE
authority_gate.ok: true
selected_moves_after_gate: 1
```

Production path:

```text
current source: awg0
required service failure rows: none
current_failures: []
wake: REJECT_WAKE
authority_gate.ok: false
selected_moves_after_gate: 0
```

Latest verdict:

```text
FIRST_DIVERGENCE_FOUND
```

First divergent field:

```text
selected_move.candidates[current_source].service_suitability.per_service[required_service]
```

First divergent function:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence
```

Root executable reason:

```text
Production selected source `awg0` has no Runtime-verifiable required-service failure row,
while the good path has telegram DOWN/PERSISTENT_FAIL/FRESH.
```

## Immediate Read List

Read these before changing code:

1. `docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md`
2. `docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md`
3. `docs/reports/engineering/2026-07-01_152327_action_class_ownership_proof.md`
4. `docs/reports/engineering/2026-07-01_151234_formal_model_verification.md`
5. `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md`
6. `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md`
7. `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
8. `tools/v7-users-autoswitch`
9. `admin_core/operator_execution.py`
10. `tests/unit/test_v7_users_autoswitch_policy.py`
11. `tests/unit/test_operator_execution_packet.py`

## Code Hotspots

### Planner emits failover

File:

```text
tools/v7-users-autoswitch
```

Function / area:

```text
_decision_for_user()
```

Known behavior:

```text
elif not current or not current.eligible:
  failover_candidates = ...
  best_failover = ...
  if best_failover:
    action = "switch"
    move_type = "failover"
    reason.append("current_egress_not_eligible")
```

Risk:

`current_egress_not_eligible` is broader than L3 emergency failure. It can mean "not eligible" for reasons other than same-subject required-service failure.

### Runtime extracts L3 move evidence

File:

```text
tools/v7-users-autoswitch
```

Function:

```text
_emergency_failover_move_evidence()
```

Key rule:

```text
for service in required_services:
  row = current.service_suitability.per_service[service]
  if row.available is False
     or row.truth_class == PERSISTENT_FAIL
     or row.status in DOWN/FAIL/ERROR/NOT_STARTED:
       current_failures.append(row)

if not current_failures:
  blockers.append("required_service_failure_required")
```

This is correct for L3. Do not weaken it unless explicitly proven by executable evidence.

### Wake derives from failures

File:

```text
tools/v7-users-autoswitch
```

Function:

```text
_l3_wake_decision()
```

If `current_failures` is empty:

```text
failed_sources = []
failed_services = []
accepted_wake_sources = []
blocker = confirmed_l3_wake_required
```

This is correct for L3.

### Approved plan lock / serialization

File:

```text
admin_core/operator_execution.py
```

Functions:

```text
selected_moves_from_plan()
approved_plan_lock_from_selected()
build_restore_barrier_clearance()
```

This was already fixed to preserve semantic fields. Do not assume serialization is still the first blocker.

## Existing Regression Tests

Useful tests:

```text
tests/unit/test_v7_users_autoswitch_policy.py::test_l3_production_validation_envelope_reaches_switch_without_certifying_autonomy
tests/unit/test_v7_users_autoswitch_policy.py::test_l3_production_validation_blocks_two_users_and_source_recovered
tests/unit/test_operator_execution_packet.py::test_nonzero_packet_generation_and_clearance_lifecycle
```

Missing explicit test that should be added if patching:

```text
Planner must not emit L3-executable failover when current_egress_not_eligible exists
but same-subject required-service failure is absent.
```

Also keep tests proving:

- good L3 path still reaches fake `_run_switch()`;
- Runtime still STOP_SAFE when `current_failures` is empty;
- serialization preserves `reason`, `important_services`, `candidates`, `scores`, `service_failover`;
- non-L3 movement remains possible only through its proper governed/non-L3 path if one exists.

## Likely Next Patch Shape

Only if the user asks to implement:

1. Discover existing helpers in `tools/v7-users-autoswitch` for service failure / service suitability / required service checking.
2. Reuse existing `_emergency_failover_move_evidence()` logic or extract the smallest shared helper if necessary.
3. In `_decision_for_user()`, before setting `move_type = "failover"` for the `not current or not current.eligible` branch, require same-subject current-source required-service failure evidence.
4. If that evidence is absent, do not emit L3-executable failover.
5. Prefer existing vocabulary and behavior for non-L3 situation:

```text
PROBE_ONLY / WAIT / ASK_OPERATOR / NO_ACTION / planned MOVE
```

Use whichever existing code semantics already support. Do not invent a new action class.

6. Add tests.
7. Run targeted unit tests and compile checks.
8. Create engineering report in `docs/reports/engineering/`.
9. Do not deploy unless the user explicitly asks for production promotion/deploy.

## Forbidden Next Moves

Do not:

- add a new Runtime;
- add a new Planner;
- add a new owner;
- add a new event bus;
- add `service-failure-events.jsonl` as a new truth source;
- weaken `_emergency_failover_move_evidence()`;
- treat `current_egress_not_eligible` as sufficient for L3;
- bypass wake;
- bypass required-service failure;
- bypass restore barrier;
- bypass approved plan lock;
- bypass verification;
- bypass rollback;
- enable timers;
- enable broad autoswitch;
- move users without explicit production execution authority;
- rerun broad architecture audits.

## Important Reports Timeline

Latest high-signal reports:

| Report | Key result |
| --- | --- |
| `2026-07-01_171437_l3_differential_execution_trace.md` | First executable divergence found in current-source required-service failure evidence. |
| `2026-07-01_153255_single_decision_execution_depth.md` | Decision identity survives; decision semantics change. |
| `2026-07-01_152327_action_class_ownership_proof.md` | OMP Action-Class Authority owns durable Action Class; Planner owns candidates only. |
| `2026-07-01_151234_formal_model_verification.md` | Model deterministic; implementation divergence is Planner emitting failover from broad current-not-eligible. |
| `2026-07-01_150727_canonical_truth_proof.md` | Legal L3 execution truth is composite `EXECUTION_READY`, not Planner selected move or wake alone. |
| `2026-07-01_150144_system_invariant_proof.md` | Violated invariant: `FAILOVER_SEMANTIC_BINDING`. |
| `2026-07-01_144247_final_implementation_decision.md` | Serialization defect fixed and deployed; next blocker is required-service failure/wake. |
| `2026-07-01_125541_planner_runtime_data_lineage.md` | Earlier proved semantic loss in approved plan lock; now superseded by fix. |
| `2026-07-01_041410_final_root_cause_experiment.md` | Approved emergency envelope patch fixed authority rejection; next gate was wake. |

## Production UI / Channel Context

Earlier production incident involved `openvpn-1779388847-d2ad7c` showing users and bad/zero services. That investigation helped expose autonomous movement gaps.

But latest failed L3 Production Validation candidate is:

```text
10.7.0.5 awg0 -> vless
```

Do not mix failed-channel evidence from `openvpn-1779388847-d2ad7c` into the selected `awg0` decision. Runtime correctly requires same-subject evidence. Failure evidence from one source cannot authorize L3 movement from another source.

## How To Work With The User

The user has repeatedly asked:

- do not dump long reports into chat;
- save reports into files;
- only send the important result in chat;
- do not ask for dozens of approvals when a safe bounded authority exists;
- do not keep re-auditing architecture after the root executable issue is known.

Respond style:

```text
VERDICT

first blocker / owner / exact reason / report path
```

If implementing:

```text
changed files / tests / verdict / next exact blocker
```

Do not end with vague "if you want" language. Give the next concrete step.

## Current Best Next Step

If the next prompt asks for implementation:

```text
Implement the minimal Planner/Autoswitch correction so L3-executable `failover`
is emitted only when same-subject required-service failure evidence exists for
the selected current source.
```

Target owner:

```text
tools/v7-users-autoswitch
```

Likely test owner:

```text
tests/unit/test_v7_users_autoswitch_policy.py
```

Expected final state after patch:

```text
Production-shaped `current_egress_not_eligible` without required-service failure
does not become L3-executable failover.

Good L3 fixture with telegram DOWN/PERSISTENT_FAIL/FRESH still passes.

Runtime STOP_SAFE remains intact when current_failures is empty.
```

## Final Handoff Verdict

```text
HANDOFF_READY_FOR_IMPLEMENTATION_DEBUGGING
```

No further architecture investigation is expected before the next implementation/debugging step unless new executable evidence contradicts the current trace.
