# World Model Provenance Trace

Timestamp: 2026-07-01 18:58:31 Asia/Bangkok

Verdict: FIRST_DIVERGENCE_FOUND

## Summary

The failed L3 Production Validation candidate was:

```text
user: 10.7.0.5
source: awg0
target: vless
reason: current_egress_not_eligible
move_type: failover
```

Runtime later found:

```text
current_failures: []
blockers:
  - required_service_failure_required
  - confirmed_l3_wake_required
```

The first proven divergence is not Observation, serialization, restore barrier, or authority materialization.

The first proven divergence is Planner classification:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

Planner converts broad current candidate ineligibility:

```text
not current or not current.eligible
```

into:

```text
action = switch
move_type = failover
reason += current_egress_not_eligible
```

That broad condition is not equivalent to the L3 entry condition:

```text
current channel failed
AND required services failed on the current channel
AND affected user is assigned to that failed current channel
```

Runtime correctly requires the narrower L3 fact and stops because no required-service failure is present for `10.7.0.5 / awg0`.

## Target Candidate

| Field | Value |
| --- | --- |
| User | `10.7.0.5` |
| Current source | `awg0` |
| Target | `vless` |
| Planner reason | `current_egress_not_eligible` |
| Planner move type | `failover` |
| Runtime evidence | `current_failures: []` |
| Runtime blockers | `required_service_failure_required`, `confirmed_l3_wake_required` |

## Source Files / State Inspected

### Required Engineering Reports

- `docs/reports/engineering/2026-07-01_172201_gpt_handoff_package.md`
- `docs/reports/engineering/2026-07-01_171437_l3_differential_execution_trace.md`
- `docs/reports/engineering/2026-07-01_153255_single_decision_execution_depth.md`
- `docs/reports/engineering/2026-07-01_151234_formal_model_verification.md`
- `docs/reports/engineering/2026-07-01_144247_final_implementation_decision.md`
- `docs/reports/engineering/2026-07-01_150144_system_invariant_proof.md`

### Canonical / Policy Sources

- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/policies/POLICY_001_HARD_FAILURE.md`
- `docs/policies/POLICY_004_AUTHORITY.md`
- `docs/policies/POLICY_008_FRESHNESS.md`

### Code Owners

- `tools/v7-users-autoswitch`
- `admin_core/operator_execution.py`

### Read-Only Live Production Snapshot

Authenticated production API was queried read-only.

Endpoints inspected:

- `/api/session`
- `/api/overview`
- `/api/operator/decision-surface`
- `/api/operator/autonomous-dry-run`

No apply endpoint was called.
No users were moved.

Current live state no longer reproduces the historical failed candidate:

| Live fact | Current value |
| --- | --- |
| User | `10.7.0.5` |
| Current channel | `awg0` |
| Current decision-surface recommendation | `keep` |
| Current decision-surface suggested channel | `awg3` |
| Current decision-surface blockers | `[]` |
| Live service-user fit | `BLOCKED` because `no candidate satisfies current service/user/SLA fit` |
| Live service-user fit candidate reason | `service_freshness_not_actionable` |
| Current channel service status in decision surface | `unknown`, not confirmed failure |

Therefore current live state is useful as control evidence only. The exact historical `awg0 -> vless` candidate must be reconstructed from persisted reports and source code.

## Canonical L3 Requirement

`docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` defines L3 as emergency failover only:

- restore connectivity after confirmed current-channel failure;
- identify required services affected by the failed current channel;
- movement without fresh failure evidence is forbidden;
- required services must fail on the current channel;
- any unknown or false entry condition produces `STOP_SAFE`.

Relevant canonical lines:

- Purpose and boundary: lines 26-47.
- Forbidden movement without fresh failure evidence: lines 53-67.
- Entry conditions: lines 71-84.
- Allowed reason: `CURRENT_CHANNEL_FAILED`, lines 190-202.
- Source eligibility gate: lines 218-233.
- Incident must expose failed required services: lines 305-312.

## Planner Input Provenance Table

| Trace point | Producer / source | Raw / normalized value | Consumer | Result |
| --- | --- | --- | --- | --- |
| User registry assignment | World/user registry via planner input | `10.7.0.5` assigned to `awg0` | `_decision_for_user()` | Preserved |
| Required services | `_important_services(user)` | Required service set for the user is computed before candidate scoring | `_candidate()` and `_service_suitability()` | Preserved into selected move after serialization fix |
| Route class | `_route_class_for_services(important)` | Derived from required services | `_candidate()` | Preserved as planner context |
| Current candidate | `_candidate(user, awg0, important, route_class, purpose="current")` | Candidate object with `eligible` boolean, `blocked`, `reasons`, `service_suitability` | `_decision_for_user()` | Determines current ineligibility |
| Current candidate service suitability | `_service_suitability()` and `_gate_service()` | Required-service rows if available | `_candidate_json()` and selected move semantics | Preserved if present |
| Planner action branch | `_decision_for_user()` | `elif not current or not current.eligible` | selected move creation | Emits `move_type=failover` |
| Selected move | `_decision_for_user()` | `action=switch`, `move_type=failover`, reason `current_egress_not_eligible` | `selected_moves_from_plan()` | Preserved |

## Runtime Input Provenance Table

| Trace point | Producer / source | Runtime value | Consumer | Result |
| --- | --- | --- | --- | --- |
| Selected move after Planner | `tools/v7-users-autoswitch` | `10.7.0.5 awg0 -> vless`, `move_type=failover` | `admin_core/operator_execution.py::selected_moves_from_plan()` | Preserved |
| Approved plan lock | `approved_plan_lock_from_selected()` | selected move identity and semantic fields preserved | restore barrier materialization | Preserved |
| Restore barrier lock | `build_restore_barrier_clearance()` | approved plan lock embedded | `tools/v7-users-autoswitch --apply --verify` | Preserved |
| Runtime evidence extraction | `_emergency_failover_move_evidence()` | required services read from selected move, current candidate read from selected move | `_l3_wake_decision()` and authority gate | No current failures found |
| Current failures | `_emergency_failover_move_evidence()` | `[]` | `_l3_wake_decision()` | Wake rejected |
| Wake decision | `_l3_wake_decision()` | no failed sources/services | `_emergency_failover_authority_gate()` | `confirmed_l3_wake_required` |
| Authority gate | `_emergency_failover_authority_gate()` | move evidence not L3-ready | selected move filter | selected moves after gate = `0` |

## Planner vs Runtime Fact Comparison

| Fact | Planner side | Runtime side | Same? | Meaning |
| --- | --- | --- | --- | --- |
| User identity | `10.7.0.5` | `10.7.0.5` | YES | Identity preserved |
| Source identity | `awg0` | `awg0` | YES | Identity preserved |
| Target identity | `vless` | `vless` | YES | Identity preserved |
| Move type | `failover` | `failover` | YES | Runtime evaluates as emergency failover |
| Reason | `current_egress_not_eligible` | `current_egress_not_eligible` | YES | Reason preserved |
| Candidate semantics | Preserved after final serialization fix | Available to Runtime | YES | No serialization regression |
| Required-service failure for `awg0` | Not proven in persisted candidate evidence | `current_failures: []` | YES, absent on both sides as proven evidence | L3 entry not proven |
| L3 wake | Implied by Planner label only | Not accepted by Runtime | NO | Planner label carries less information than Runtime L3 gate requires |

## Exact Chain

### Planner branch

File/function:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

Code owner lines:

```text
6607 def _decision_for_user(...)
6614 current = self._candidate(... purpose="current") ...
6631 elif not current or not current.eligible:
6641   failover_candidates = [...]
6644   best_failover = ...
6645   if best_failover and best_failover.egress.id != user.current and cooldown_ok:
6646     action = "switch"
6647     move_type = "failover"
6650     reason.append("current_egress_not_eligible")
```

This branch does not require same-subject required-service failure before emitting `move_type=failover`.

### Candidate construction

File/function:

```text
tools/v7-users-autoswitch::_candidate()
```

Code owner lines:

```text
6897 def _candidate(...)
6900 c.service_suitability = self._service_suitability(...)
6903 self._gate_basic(...)
6906 self._gate_quality(...)
6907 self._gate_service(...)
6908 self._gate_load(...)
6909 self._gate_safety(...)
6911 if not c.eligible: return c
```

`current.eligible == False` can come from many gates, not only required-service failure.

### Runtime evidence extraction

File/function:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence()
```

Code owner lines:

```text
1179 def _emergency_failover_move_evidence(...)
1183 if move_type != "failover": blocker
1185 if current_egress_not_eligible not in reasons: blocker
1191 current = selected source candidate
1201 required_services = move.important_services
1205 per_service = current.service_suitability.per_service
1206 for service in required_services:
1210   if unavailable / PERSISTENT_FAIL / DOWN / FAIL / ERROR / NOT_STARTED:
1215     current_failures.append(row)
1216 if not current_failures:
1217   blockers.append("required_service_failure_required")
```

Runtime consumes the selected move and derives L3 evidence only from current-source required-service failure rows.

### Wake decision

File/function:

```text
tools/v7-users-autoswitch::_l3_wake_decision()
```

Code owner lines:

```text
1271 def _l3_wake_decision(...)
1283 failed_sources = rows with current_failures
1288 failed_services = services inside current_failures
1294 if failed_sources and failed_services:
1295   infer confirmed_service_failure and confirmed_current_channel_failure
```

No current failures means no confirmed L3 wake.

## Questions Answered

### 1. What exact input made Planner set `current_egress_not_eligible`?

The exact executable Planner condition is:

```text
current is None OR current.eligible is False
```

For the target candidate, the persisted reports prove Planner emitted `current_egress_not_eligible`; therefore `_decision_for_user()` took that branch.

The exact historical sub-blocker inside `current.blocked[]` was not persisted in the available reports as a raw planner object. However, the downstream selected move and Runtime extraction prove the relevant L3 sub-fact was absent: no current-source required-service failure row existed for `awg0`.

### 2. Was that input required-service failure on `awg0`?

No, not as a proven L3 fact.

If the input had been a required-service failure on `awg0`, `_emergency_failover_move_evidence()` would have derived at least one `current_failures` row from:

- `available is false`, or
- `truth_class == PERSISTENT_FAIL`, or
- `status in DOWN / FAIL / ERROR / NOT_STARTED`.

It derived:

```text
current_failures: []
```

### 3. If not, what type of ineligibility was it?

The exact historical sub-type is not fully persisted.

The proven type is broader current candidate ineligibility:

```text
current.eligible == False
```

This could be produced by basic, quality, service freshness/evidence, load, safety, policy, or other candidate gates. Current live read-only state for the same user/channel shows service-user fit blocked by:

```text
service_freshness_not_actionable
```

and decision-surface candidate services are `unknown`, not confirmed failure. That current snapshot is not an exact replay, but it supports the same distinction: not every current ineligibility is L3 emergency failure.

### 4. Did Runtime receive the same input?

Runtime received the same selected move identity and semantic payload after the serialization fix:

- user;
- source;
- target;
- move type;
- reason;
- important services;
- candidates;
- service suitability payload if present.

Runtime did not receive a same-subject current required-service failure fact for `awg0`, because that fact was not present in the selected move payload.

### 5. Did selected move preserve the relevant input?

Yes for the selected move semantics that existed.

The final implementation decision fixed semantic preservation:

- `selected_moves_from_plan()` preserves semantic fields;
- `approved_plan_lock_from_selected()` preserves semantic fields;
- restore barrier embeds approved plan lock.

The relevant L3 fact was not lost in serialization. It was absent as required-service failure evidence for `awg0`.

### 6. Did Runtime extract from the same source and same services?

Yes.

Runtime extraction uses:

```text
move.current_egress
move.recommended_egress
move.important_services
move.candidates[source].service_suitability.per_service
```

That is the same selected move object preserved through approved plan lock and restore barrier.

### 7. Is the first divergence in Observation, World Model, Planner normalization, selected move serialization, restore barrier, or Runtime extraction?

First proven divergence:

```text
Planner normalization / selected move birth
```

More specifically:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

Planner emits `move_type=failover` from broad `current_egress_not_eligible` without proving the narrower L3 required-service failure fact for the selected current source.

Not first divergence:

- serialization: semantic payload is preserved;
- restore barrier: approved plan lock is embedded and consumed;
- Runtime extraction: Runtime correctly derives empty `current_failures`;
- authority: authority correctly fails closed after evidence extraction.

### 8. Is Planner input wrong/incomplete, or did Planner overclassify correct input as L3 failover?

The proven answer is:

```text
Planner overclassified broad current_egress_not_eligible as L3 failover.
```

The world/planner input may have been useful for advisory movement, recheck, degraded-state handling, or non-L3 movement. It was not sufficient to prove L3 emergency failover.

## First Divergence

| Field | Value |
| --- | --- |
| First divergent fact | `move_type=failover` was emitted from broad `current_egress_not_eligible` without same-subject required-service failure on `awg0` |
| Producer | `tools/v7-users-autoswitch::_decision_for_user()` |
| Consumer | `tools/v7-users-autoswitch::_emergency_failover_move_evidence()` / `_l3_wake_decision()` / `_emergency_failover_authority_gate()` |
| Owner | Planner / autoswitch owner: `tools/v7-users-autoswitch` |
| Canonical owner | L3 capability contract: `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` |
| Exact file/function | `tools/v7-users-autoswitch::_decision_for_user()` |
| Minimal correction direction | Planner must not emit L3-executable `move_type=failover` from broad `current_egress_not_eligible` unless selected current source carries same-subject required-service failure evidence. Otherwise emit a non-L3 movement/advisory/recheck outcome. |

## Owner

Existing owner only:

```text
tools/v7-users-autoswitch
```

No new owner is needed.

No new Runtime, Planner, Authority, Wake system, Event bus, Truth source, OMP, or roadmap is needed.

## Exact File / Function

Primary correction owner:

```text
tools/v7-users-autoswitch::_decision_for_user()
```

Related evidence consumers that should remain strict:

```text
tools/v7-users-autoswitch::_emergency_failover_move_evidence()
tools/v7-users-autoswitch::_l3_wake_decision()
tools/v7-users-autoswitch::_emergency_failover_authority_gate()
```

Non-root preservation owners:

```text
admin_core/operator_execution.py::selected_moves_from_plan()
admin_core/operator_execution.py::approved_plan_lock_from_selected()
admin_core/operator_execution.py::build_restore_barrier_clearance()
```

These are not the current root cause.

## Minimal Correction Direction

Do not weaken Runtime.

Do not make `confirmed_l3_wake_required` optional.

Do not treat broad `current_egress_not_eligible` as L3 emergency evidence.

Minimal semantic correction:

```text
Before Planner emits L3-executable move_type=failover,
the current candidate must prove same-subject required-service failure
for the selected user's current source.
```

If the current source is ineligible for any other reason, Planner should not produce an L3 Production Validation selected move. It should produce the existing appropriate non-L3 outcome, such as advisory movement, recheck, wait, no-action, probe-only, or blocked state, depending on the existing owner semantics.

## Tests Needed If Implementation Follows

Required regression tests:

1. Good L3 path: current source has required-service failure row; Planner may emit L3 `failover`; Runtime derives non-empty `current_failures`.
2. Production-shaped path: current source is ineligible but has no required-service failure row; Planner must not emit L3-executable `failover`.
3. Service freshness / recheck / unknown service evidence must not become L3 `failover`.
4. Runtime must keep `STOP_SAFE` when `current_failures` is empty.
5. Serialization must continue preserving `important_services`, `candidates`, and `service_suitability`.
6. Restore barrier and approved plan lock identity semantics must remain unchanged.

## Canonical Knowledge Changes

None.

The canonical L3 rule already exists. The divergence is implementation semantics in the existing Planner/autoswitch owner.

## Final Verdict

FIRST_DIVERGENCE_FOUND
