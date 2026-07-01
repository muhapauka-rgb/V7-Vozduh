# Planner -> Runtime Data Lineage Proof

Date: 2026-07-01 12:55:41

Task: identify the exact production data object that loses the information required for Runtime to execute the first L3 Production Validation.

No code was changed.

Final verdict: `DATA_OBJECT_MUTATED`

## Answer

The first broken production data object is:

`approved_plan_lock.selected_moves`

More precisely:

`packet.approved_plan_lock.selected_moves` -> `restore_barrier.approved_plan_lock.selected_moves`

This object is born from Planner-selected move data, but it is serialized as an identity-only move. It loses the semantic evidence required by Runtime L3 execution:

- `reason`
- `important_services`
- `candidates`
- current channel `service_suitability`
- target channel `service_suitability`
- service failure evidence needed to derive `current_failures`

The downstream `move_evidence`, `failed_sources`, `failed_services`, `l3_wake`, and `incident` objects are not the first broken objects. They are downstream consequences of the semantic loss in `approved_plan_lock.selected_moves`.

## Object Inventory

| Object | Plane | Producer | Consumer | Status |
| --- | --- | --- | --- | --- |
| Planner decision row | Planning | `tools/v7-users-autoswitch` | selected move builder | COMPLETE |
| Planner selected move | Planning -> Execution | `tools/v7-users-autoswitch::plan()` | packet materialization | COMPLETE before serialization |
| Packet selected abstraction | Execution | `admin_core/operator_execution.selected_moves_from_plan()` | `packet_from_plan()` | MUTATED / evidence stripped |
| `packet.approved_plan_lock.selected_moves` | Execution | `admin_core/operator_execution.approved_plan_lock_from_selected()` | restore barrier clearance | BROKEN OBJECT |
| `restore_barrier.approved_plan_lock.selected_moves` | Runtime guard | `build_restore_barrier_clearance()` | `tools/v7-users-autoswitch._approved_plan_lock_validation()` | BROKEN COPY |
| Runtime selected move | Runtime | `_approved_plan_lock_validation()` + `_merge_locked_moves_with_live_decisions()` | `_emergency_failover_authority_gate()` | PARTIAL / depends on rehydration |
| Move evidence | Runtime | `_emergency_failover_move_evidence()` | `_l3_wake_decision()` | DOWNSTREAM EMPTY/INSUFFICIENT |
| L3 wake | Runtime | `_l3_wake_decision()` | incident/authority gate | DOWNSTREAM REJECT |
| Incident | Runtime | `_l3_incident` path | execution eligibility | NOT FIRST BROKEN |
| Apply result | Runtime | `apply()` | lease/feedback | DOWNSTREAM STOP_SAFE |

## Lineage Graph

```text
Planner decision
  -> Planner selected move
     contains user/source/target/type/reason/important_services/candidates/service_suitability
  -> selected_moves_from_plan(plan)
     keeps only user/source/target/type/hash/count
  -> packet.approved_plan_lock.selected_moves
     identity-only selected move
  -> restore_barrier.approved_plan_lock.selected_moves
     identity-only selected move copy
  -> _approved_plan_lock_validation()
     validates identity and returns selected move without semantic evidence
  -> _merge_locked_moves_with_live_decisions()
     tries to rehydrate evidence from fresh live decisions
  -> _emergency_failover_move_evidence()
     requires reason/important_services/candidates/service_suitability
  -> _l3_wake_decision()
     cannot infer failed_sources/failed_services if evidence is absent
  -> selected moves cleared
  -> apply() returns approved_plan_lock_selected_moves_missing
```

## Mutation Proof

### Producer Object

Planner selected moves include semantic execution evidence. `tools/v7-users-autoswitch` selected moves are built from decisions that include:

- `reason`
- `important_services`
- `candidates`
- per-candidate `service_suitability`

Runtime evidence extraction explicitly depends on these fields.

`tools/v7-users-autoswitch:1171-1209`:

- reads `reason`;
- reads `important_services`;
- reads `candidates`;
- finds current and target candidates;
- reads current `service_suitability.per_service`;
- produces `current_failures`.

### First Mutation

`admin_core/operator_execution.py:301-389` converts Planner output into the selected object used by packet materialization.

At `admin_core/operator_execution.py:327-332`, each move is reduced to:

- `user_ip`
- `current_egress`
- `recommended_egress`
- `move_type`

It does not carry:

- `reason`
- `important_services`
- `candidates`
- `service_suitability`
- service failure evidence

### Broken Serialized Object

`admin_core/operator_execution.py:392-430` builds `approved_plan_lock.selected_moves`.

At `admin_core/operator_execution.py:403-410`, the lock stores only:

- `user_ip`
- `current_egress`
- `recommended_egress`
- `move_type`

This is the first persisted/cross-plane object whose semantic content differs from its Planner producer.

### Runtime Copy

`admin_core/operator_execution.py:1475-1517` embeds the lock into restore barrier clearance.

The restore barrier faithfully preserves the already-mutated lock. It does not create the loss; it carries the loss.

### Runtime Consumption

`tools/v7-users-autoswitch:5155-5167` consumes the approved plan lock and turns it back into selected moves.

Because the lock is identity-only, Runtime then calls:

`tools/v7-users-autoswitch:5498-5525`

`_merge_locked_moves_with_live_decisions()` tries to recover missing semantic fields from fresh live decisions:

- `reason`
- `important_services`
- `candidates`
- `scores`
- `service_failover`

This means the production runtime consumer is not consuming a self-sufficient execution object. It is consuming an identity lock that must be rehydrated.

If exact live-decision rehydration is absent, stale, filtered, or mismatched, Runtime has an identity-valid move but lacks evidence required for L3 wake and eligibility.

## Downstream Failure Proof

`tools/v7-users-autoswitch:1171-1209` cannot produce `current_failures` without:

- `reason=current_egress_not_eligible`;
- `important_services`;
- current candidate with `service_suitability.per_service`.

`tools/v7-users-autoswitch:1263-1327` cannot infer:

- `confirmed_service_failure`;
- `confirmed_current_channel_failure`;
- `failed_sources`;
- `failed_services`;

unless `move_evidence.current_failures` exists.

`tools/v7-users-autoswitch:7508-7541` then converts empty selected moves into:

`approved_plan_lock_selected_moves_missing`

This is a terminal symptom, not the first broken object.

## Live Production Replay

Observed latest production validation state:

- candidate existed;
- user: `10.0.0.2`;
- source: `openvpn-1779388847-d2ad7c`;
- target: `vless`;
- restore barrier was written;
- approved plan lock was valid;
- selected moves before restore barrier: `1`;
- selected moves after gate: `0`;
- terminal reason: `approved_plan_lock_selected_moves_missing`;
- L3 wake blocker: `confirmed_l3_wake_required`;
- no user moved.

This is consistent with:

1. identity object surviving;
2. semantic evidence not surviving;
3. Runtime failing to derive service-failure wake;
4. emergency gate clearing selected moves;
5. apply seeing zero executable moves.

## Object State Matrix

| Object | Exists | Alive | Mutated | Lost | Empty | Rebuilt | Discarded | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Planner selected move | YES | transient | NO at birth | NO | NO | NO | copied | Contains full evidence. |
| Packet selected abstraction | YES | transient | YES | PARTIAL | NO | YES | source fields discarded | First reduction to identity. |
| `packet.approved_plan_lock.selected_moves` | YES | persisted in packet | YES | YES semantic evidence | NO identity | NO | NO | First broken object. |
| `restore_barrier.approved_plan_lock.selected_moves` | YES | persisted in barrier | inherits mutation | YES semantic evidence | NO identity | NO | NO | Broken copy. |
| Runtime selected move | YES | transient | PARTIAL | evidence absent unless rehydrated | can become empty after gate | PARTIAL | YES if gate blocks | Depends on live decision merge. |
| `move_evidence` | YES/NO | transient | downstream | YES if no evidence | often empty/insufficient | NO | YES after gate | Consequence. |
| `l3_wake` | YES | transient | NO | no accepted source | REJECT | NO | NO | Consequence. |
| `plan.selected_moves` after emergency gate | YES | transient | YES | YES | YES | NO | YES | Symptom before apply. |

## Ownership Graph

| Object | Owner | Producer | Consumer | Allowed mutations |
| --- | --- | --- | --- | --- |
| Planner selected move | `tools/v7-users-autoswitch` | Planner | packet materialization | Planner only before commit |
| Packet selected abstraction | `admin_core/operator_execution.py` | `selected_moves_from_plan()` | `packet_from_plan()` | Identity extraction only |
| Approved plan lock | `admin_core/operator_execution.py` | `approved_plan_lock_from_selected()` | restore barrier / Runtime apply | Must not reselect/replace users/targets |
| Restore barrier lock copy | `admin_core/operator_execution.py` | `build_restore_barrier_clearance()` | `tools/v7-users-autoswitch` | append-only clearance metadata |
| Runtime selected move | `tools/v7-users-autoswitch` | approved lock + live decision merge | emergency gate / apply | filtering only by gates |

## First Broken Object

`approved_plan_lock.selected_moves`

Reason:

It is the first persisted cross-plane object that should preserve the information Runtime needs to execute L3 Production Validation, but it preserves only identity fields and drops the Planner evidence needed to prove current-channel failure and required-service failure.

## Information-Loss Proof

Who created it:

`admin_core/operator_execution.py::approved_plan_lock_from_selected()`

Who modified/degraded it:

`admin_core/operator_execution.py::selected_moves_from_plan()` first reduces the rich Planner move; `approved_plan_lock_from_selected()` persists that reduced shape.

Who deleted or filtered it:

No one deletes the identity. The semantic evidence is omitted during serialization.

Who reconstructs it:

`tools/v7-users-autoswitch::_merge_locked_moves_with_live_decisions()` attempts to rehydrate the identity-only lock from live decisions.

Who should consume it:

`tools/v7-users-autoswitch::_emergency_failover_authority_gate()` and `_emergency_failover_move_evidence()`.

Why consumption fails:

The consumer needs semantic evidence, but the persisted object only guarantees identity.

## Minimal Correction

Preserve the existing object. Do not create a new object.

Minimal correction:

Extend the existing `approved_plan_lock.selected_moves` payload, produced by the existing `admin_core/operator_execution.py` owner, so the selected move preserves the L3 evidence already produced by Planner and already consumed by Runtime:

- `reason`
- `important_services`
- `candidates` or a bounded canonical evidence subset sufficient for `_emergency_failover_move_evidence()`
- current required-service failure evidence
- target service suitability evidence

Keep the existing identity fields, lock hash, allowed users, allowed targets, packet, restore barrier, and runtime consumer.

No new packet, event, wake, runtime state, planner output, owner, or architecture is required.

## Final Verdict

`DATA_OBJECT_MUTATED`
