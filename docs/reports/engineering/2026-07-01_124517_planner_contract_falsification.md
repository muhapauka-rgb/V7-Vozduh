# Planner Contract Falsification

Date: 2026-07-01 12:45:17

Task: attempt to falsify H1: `Planner -> Runtime Contract is incomplete`.

Final result: H1 is refuted as the primary/root explanation.

Final verdict: `PLANNER_CONTRACT_REFUTED`

## Hypotheses

H1: Planner -> Runtime Contract is incomplete.

H0: Planner Contract is already complete; the observed failure is caused by implementation, configuration, execution mode, selected-move handoff, stale state, or another subsystem.

## Semantic Duplicate Audit

Searched by responsibility and runtime effect across planner, runtime, wake, incident, service matrix, observation, authority, execution, verification, rollback, learning, capability state, selected move, move evidence, service evidence, current channel failure, and required service failure.

Equivalent existing semantics found:

| Concept | Existing implementation | Status |
| --- | --- | --- |
| Planner selected move consumed by Runtime | `tools/v7-users-autoswitch::_emergency_failover_authority_gate()` consumes `selected` moves and produces `move_evidence` | `EXISTS_COMPLETE` |
| Required service failure derived from selected move | `tools/v7-users-autoswitch::_emergency_failover_move_evidence()` reads move candidates, important services, current service suitability, and target suitability | `EXISTS_COMPLETE` |
| L3 wake derived from move evidence | `tools/v7-users-autoswitch::_l3_wake_decision()` infers `confirmed_service_failure` and `confirmed_current_channel_failure` from `move_evidence` | `EXISTS_COMPLETE` |
| External L3 wake event path | `_l3_external_wake_events()` plus tests using `events/l3-wake-events.jsonl` | `EXISTS_PARTIAL/ALTERNATE` |
| Planner consumption proof | `tests/unit/test_v7_users_autoswitch_policy.py` verifies incident consumes planner output without Runtime replacing planner | `EXISTS_COMPLETE` |

No new semantic owner is required.

## Evidence That Refutes H1

### Counterexample 1: Runtime Already Derives Wake From Planner Move Evidence

`tools/v7-users-autoswitch:971-1005`:

- iterates selected Planner moves;
- calls `_emergency_failover_move_evidence(move)`;
- passes resulting `per_move` evidence into `_l3_wake_decision(policy, per_move)`.

`tools/v7-users-autoswitch:1171-1244`:

- verifies move type is `failover`;
- verifies reason includes `current_egress_not_eligible`;
- reads the current candidate and target candidate from the selected move;
- checks current required-service failures;
- checks target service readiness;
- returns `current_failures`.

`tools/v7-users-autoswitch:1263-1327`:

- reads failed sources and failed services from `move_evidence`;
- if both exist, infers `confirmed_service_failure` and `confirmed_current_channel_failure`;
- accepts wake when inferred source is allowed.

If Planner -> Runtime Contract were intrinsically incomplete, this path could not exist.

### Counterexample 2: Unit Test Passes Without Independent Wake Producer

`tests/unit/test_v7_users_autoswitch_policy.py:1281-1309` proves:

- service failure exists;
- emergency failover autonomy is enabled;
- no explicit wake file is created;
- Runtime selects one move;
- execution is not blocked;
- execution mode becomes `emergency_failover`.

This is a minimal execution where Planner contract remains unchanged and Runtime succeeds.

### Counterexample 3: Incident Consumes Planner Output

`tests/unit/test_v7_users_autoswitch_policy.py:1311-1349` proves:

- wake is `ACCEPT_WAKE`;
- accepted wake sources include `confirmed_service_failure` and `confirmed_current_channel_failure`;
- incident is `READY_FOR_EXECUTION`;
- affected user, failed source, target channel, and selected move hash come from Planner output;
- `runtime_replaced_planner=false`.

This proves the existing contract already carries enough information when the selected move is preserved.

## Observed Production Failure Reinterpreted

Latest production evidence from Current Program State and recent reports shows:

- `selected_moves_before_restore_barrier = 1`
- `selected_moves_after_gate = 0`
- `approved_plan_lock_selected_moves_missing`
- `approved_plan_lock_snapshot_gate_stop_required`
- `execution_blocker = emergency_failover_autonomy`
- `move_evidence = []`
- `failed_sources = []`
- `failed_services = []`
- wake decision = `REJECT_WAKE`

This does not prove Planner Contract incompleteness. It proves Runtime wake derivation received no selected move evidence.

The observed behavior is fully explained by selected move loss or selected move non-consumption before the emergency failover gate.

## Alternative Explanation Matrix

| Alternative | Can fully explain observed behavior? | Evidence |
| --- | --- | --- |
| Selected move handoff/lock consumption defect | YES | Production state shows one selected move before restore barrier and zero after gate; apply reason is `approved_plan_lock_selected_moves_missing`. |
| Planner Contract incomplete | NO | Code and tests prove Runtime can derive wake from selected move evidence. |
| Missing independent wake producer | PARTIAL | External wake files are absent, but independent wake is not required when move evidence is preserved. |
| Runtime wake implementation bug | PARTIAL | Wake rejects empty evidence correctly; wake accepts non-empty move evidence in tests. |
| Authority bug | PARTIAL | Authority gate blocks because evidence is empty; not because the authority model cannot authorize. |
| Restore barrier bug | PARTIAL | Restore barrier/approved-plan-lock path participates in dropping or failing to preserve moves, but wake contract itself is not missing. |
| Packet bug | PARTIAL | Packet/apply fails downstream because selected move identity is missing; packet is not primary truth failure. |
| Execution mode confusion | PARTIAL | Production validation may route through a snapshot/apply path that loses selected moves, but the L3 mode itself has valid semantics. |
| Stale state | PARTIAL | Expired/invalid locks appear in history, but empty selected move evidence alone explains the current failure. |
| Planner bug | NO/PARTIAL | Planner produced at least one selected move before restore barrier; failure occurs after that boundary. |
| Test artifact | NO | Tests are valid counterexamples to the universal claim that contract is incomplete. They do not erase production failure, but they refute H1 as root cause. |
| CPS/state reporting bug | NO | CPS records the symptom; it is not the executable cause. |
| Verification/rollback/learning defect | NO | Execution never reaches these stages. |

## Planner Contract Test

Assume Planner Contract is already complete.

Would the observed production failure still occur?

YES.

Why: the production path can still fail if the selected move produced by Planner is lost, blocked, or not consumed before `_emergency_failover_authority_gate()`. In that case the complete contract has no runtime input, so `_l3_wake_decision()` receives `move_evidence=[]` and correctly returns `confirmed_l3_wake_required`.

## Counterexamples

| Counterexample | Result |
| --- | --- |
| Emergency failover autonomy unit path with service failure and no external wake file | Runtime authorizes bounded failover and selects one move. |
| L3 wake unit path with planner output | Wake accepts, incident consumes planner output, Runtime does not replace Planner. |
| External event unit path | Runtime can also consume explicit L3 wake events and reach fake `_run_switch()`. |

The first two counterexamples are sufficient to falsify H1 as stated.

## Generalization Test

If Planner Contract were incomplete, the same defect should necessarily appear in L4/L5/L6/L7 or any future capability that relies on Planner facts crossing into Runtime.

The current evidence does not support that. The existing L3 implementation already demonstrates the generic pattern:

Planner selected move -> move evidence -> Runtime gate -> wake/incident/authority.

The failure is path-specific: production validation loses or blocks the selected move before Runtime can consume the contract.

## SAT / UNSAT

H1 as a theorem is `UNSAT` against the discovered counterexamples.

A weaker hypothesis survives:

"The current L3 Production Validation execution path fails to preserve/consume selected move evidence before the emergency failover gate."

That weaker hypothesis is implementation-path specific, not Planner Contract incompleteness.

## Real Root Cause

The real executable root cause is:

The production execution path loses or invalidates the approved Planner selected move before `_emergency_failover_authority_gate()` can derive `move_evidence`, causing Runtime to see `selected=[]`, `move_evidence=[]`, and `confirmed_l3_wake_required`.

## Minimal Semantic Correction

No Planner Contract redesign is justified.

The next implementation, if requested later, should target only the selected-move preservation/approved-plan-lock consumption boundary in the existing execution path.

## Confidence

High.

Reason: there are direct code-level counterexamples and unit-level counterexamples where Planner evidence is sufficient. The production symptom matches missing selected move input, not missing Planner semantics.

## Final Verdict

`PLANNER_CONTRACT_REFUTED`
