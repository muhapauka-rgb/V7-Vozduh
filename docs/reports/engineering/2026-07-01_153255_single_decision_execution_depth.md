# Single Decision Execution Depth Proof

Status: `COMPLETE`
Mode: `READ_ONLY_SINGLE_DECISION_PROOF`
Code modified: `NO`
Runtime modified: `NO`
Architecture modified: `NO`
Candidate regenerated: `NO`

## Target Decision

Latest failed L3 Production Validation candidate, from the deployed post-serialization-fix production run:

```text
logical_decision_id: L3PV-2026-07-01-latest-10.7.0.5-awg0-vless
user: 10.7.0.5
source: awg0
target: vless
planner_action: switch
planner_move_type: failover
planner_reason: current_egress_not_eligible
terminal_result: STOP_SAFE
apply_executed: false
users_moved: 0
runtime_blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
move_evidence.current_failures: []
```

Evidence source:

- `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md`
- `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md`
- Source code read-only inspection of `tools/v7-users-autoswitch` and `admin_core/operator_execution.py`

## Decision Lifecycle

| Stage | Same decision survived? | Meaning at stage | Evidence status | Owner |
| --- | --- | --- | --- | --- |
| Observation | `PARTIAL` | Production has channel/service problems, but latest failed-channel evidence was not bound to selected source `awg0`. | Some world failure evidence exists; same-subject `awg0` required-service failure not proven. | Observation / service evidence owners |
| World Model | `PARTIAL` | User `10.7.0.5` is on `awg0`; target `vless` is available enough to be considered. | User/source/target identity exists. Required-service failure for `awg0` not established. | World model / planner inputs |
| Planner | `NO` for L3 semantics; `YES` for movement identity | Planner emits `switch`, `move_type=failover`, reason `current_egress_not_eligible`. | Decision carries broad current-not-eligible reason, not L3 same-subject required-service failure proof. | `tools/v7-users-autoswitch::_decision_for_user` |
| Packet | `YES` for identity; `NO` for L3 semantics | Packet carries selected user/source/target/move_type and preserved semantic fields. | Serialization no longer strips fields, but the preserved evidence still lacks current failures. | `admin_core/operator_execution.py` |
| Approved Plan Lock | `YES` for identity; `NO` for L3 semantics | Lock preserves selected move identity and semantic payload. | Lock is valid. Missing proof is inherited, not introduced here. | `admin_core/operator_execution.py` |
| Restore Barrier | `YES` for identity; `NO` for L3 semantics | Restore barrier binds approved lock to runtime action. | Restore barrier valid; cannot invent L3 failure evidence. | `admin_core/operator_execution.py` |
| Runtime | `YES` for identity; `NO` for executable L3 meaning | Runtime consumes the same selected move and evaluates it as emergency failover. | `_emergency_failover_move_evidence()` produces no `current_failures`. | `tools/v7-users-autoswitch` |
| Eligibility | `NO` | Eligibility rejects the move for L3 execution. | `required_service_failure_required` is present. | `_emergency_failover_move_evidence` |
| Authority | `PARTIAL` | Approved one-user production validation envelope passes identity/authority shape, but cannot override L3 entry truth. | Authority exists, readiness truth does not. | `_emergency_failover_authority_gate` |
| Wake | `NO` | Runtime cannot accept L3 wake because no failed source/services are inferred. | `confirmed_l3_wake_required`. | `_l3_wake_decision` |
| Apply | `NO / NOT_REACHED` | No executable selected moves survive gate. | `selected_moves_after_gate = 0`. | `tools/v7-users-autoswitch.apply` |
| Verification | `NOT_REACHED` | No apply, no verification. | Not run. | Verification owner |
| Rollback | `NOT_REACHED` | No mutation, rollback not required. | Not required. | Rollback owner |
| Learning | `NOT_REACHED` | No production outcome. | No A4/L3 evidence increment. | Learning / evidence owners |
| OMP | `STOP_SAFE` | Production validation rung remains incomplete. | No production-proven transition. | OMP |

## Decision Semantics Graph

```text
World / observation
  -> "some production channel/service failure exists"
  -> selected user/source/target: 10.7.0.5 awg0 -> vless
  -> Planner meaning: "current egress not eligible, switch as failover"
  -> Packet/lock/barrier: same identity preserved
  -> Runtime meaning: "L3 emergency failover requires current_failures on awg0"
  -> current_failures = []
  -> STOP_SAFE
```

The decision identity does not become a different object. The user, source, target, move type, lock, and restore-barrier identity survive.

The decision stops being the same decision semantically at Planner classification:

```text
current_egress_not_eligible
  -> move_type = failover
```

That meaning is broader than the L3 execution meaning:

```text
current channel failed
+ required services failed for this user on this current channel
+ safe target
  -> L3 failover candidate
```

## Evidence Lineage

| Evidence fragment | Birth | Transformation | Consumption | Result |
| --- | --- | --- | --- | --- |
| `user=10.7.0.5` | World/user registry | Preserved in planner, packet, lock, barrier | Runtime identity checks | Survives |
| `source=awg0` | World/user registry | Preserved in selected move | Runtime source binding | Survives |
| `target=vless` | Planner target selection | Preserved in packet/lock/barrier | Runtime target binding | Survives |
| `move_type=failover` | Planner `_decision_for_user()` | Preserved downstream | Runtime treats as L3 failover input | Survives as label |
| `reason=current_egress_not_eligible` | Planner `_decision_for_user()` | Preserved downstream | `_emergency_failover_move_evidence()` checks it | Survives but is insufficient |
| Required services | Planner/user context | Preserved if present | `_emergency_failover_move_evidence()` iterates services | Present enough to check, not enough to prove failure |
| Current channel service failure | Service suitability for selected current source | Not present as failing rows for `awg0` | `_emergency_failover_move_evidence()` needs rows with unavailable/down/fail | Missing |
| `current_failures` | Runtime derived evidence | Cannot be derived | `_l3_wake_decision()` depends on it | Empty |
| L3 wake | Runtime derived/observed wake | Rejected | Authority gate consumes it | `confirmed_l3_wake_required` |

## Ownership Graph

| Stage | Owns decision now | May modify | May reject | May only consume |
| --- | --- | --- | --- | --- |
| Observation | Observation/service evidence owners | Observation owners may update facts | Runtime/Planner may reject stale or missing facts | Planner, Runtime |
| Planner | `tools/v7-users-autoswitch` | Planner may select candidate and reason | Planner may produce no candidate | Packet owner consumes |
| Action Class semantics | OMP Autonomy Promotion Engine / Action-Class Authority | OMP/policy owners only | Runtime/authority may reject unproven class applicability | Planner/Runtime consume |
| Packet / lock / barrier | `admin_core/operator_execution.py` | Packet owner may materialize identity and lock | Packet owner may fail closed on invalidity | Runtime consumes |
| Runtime gate | `tools/v7-users-autoswitch` | Runtime may filter selected moves | Runtime may STOP_SAFE | Apply consumes only surviving moves |
| Apply | `tools/v7-users-autoswitch` | Apply may mutate only surviving moves | Apply fails closed if no moves | Verification consumes result |

## Decision Continuity

| Continuity type | Result | Proof |
| --- | --- | --- |
| Semantically identical | `NO` | Planner meaning is broad `current_egress_not_eligible`; Runtime L3 meaning requires same-subject required-service failure. |
| Operationally identical | `PARTIAL` | User/source/target operation identity survives, but no executable move survives authority/wake gate. |
| Legally identical | `NO` | The decision is legal as a candidate, not legal as L3 execution authority. |
| Execution-identical | `NO` | Runtime converts the candidate to zero executable selected moves. |

## Execution Depth

Deepest reached stage:

```text
Runtime eligibility / authority / wake gate
```

Reached:

```text
Observation
World Model
Planner
Packet
Approved Plan Lock
Restore Barrier
Runtime
Eligibility
Authority envelope shape
Wake decision
STOP_SAFE
```

Not reached:

```text
_run_switch()
Apply mutation
Verification
Rollback
Learning
Production Proven
OMP capability transition
```

## First Identity Break

Strict identity does not break.

First semantic break:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

Executable moment:

```text
if current is absent or not eligible:
  action = switch
  move_type = failover
  reason += current_egress_not_eligible
```

Why this is the first break:

1. The selected move identity later survives packet, approved plan lock, and restore barrier.
2. Serialization now preserves semantic fields.
3. Runtime consumes the same selected move.
4. Runtime rejects it because the selected move does not prove required-service failure on the selected current source.

Therefore the first divergence is not packet, lock, restore barrier, authority envelope, or Runtime. It is semantic overclassification of the selected move before materialization.

## Execution Proof

Question:

```text
Did Planner create one decision and Runtime execute another?
```

Answer:

```text
NO
```

Runtime did not execute any decision.

More precise answer:

```text
Planner created one movement candidate whose identity survived.
Runtime interpreted that same candidate under the stricter L3 emergency-failover execution contract and stopped it.
```

So the failure is not replacement. It is semantic mismatch:

```text
candidate-failover label != executable L3 failover truth
```

## Formal Proof

Let:

```text
D = (user=10.7.0.5, source=awg0, target=vless, move_type=failover)
P(D) = Planner reason current_egress_not_eligible
L3(D) = current channel failed + required services failed on source for same user
```

Observed:

```text
P(D) = true
L3(D) = false / not proven
approved_plan_lock(D).ok = true
restore_barrier(D).ok = true
Runtime current_failures(D) = []
```

Canonical runtime rule:

```text
EXECUTE(D) only if L3(D) and authority/identity/restore/rollback/verification gates pass.
```

Therefore:

```text
P(D) does not imply L3(D)
not L3(D) -> STOP_SAFE
```

The decision remains the same identity `D`, but it does not remain the same meaning across Planner and Runtime.

## Final Reduction

One statement:

```text
Decision semantics changed.
```

The selected movement identity survived. The L3 executable meaning did not.

## Minimal Correction Direction

Inside existing owners only:

```text
Planner/Autoswitch must stop emitting or treating `move_type=failover` as L3-executable unless the selected user/source/target decision carries same-subject current-channel failure and required-service failure evidence.
```

If those facts are not present, the decision must remain a non-L3 candidate, no-action/wait/probe/operator-review candidate, or STOP_SAFE input. Runtime should continue rejecting it.

## Final Verdict

```text
DECISION_SEMANTICS_CHANGED
```
