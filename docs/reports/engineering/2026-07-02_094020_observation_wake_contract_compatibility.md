# Observation Wake Contract Compatibility

Generated: 2026-07-02_094020

Mode: IMPLEMENTATION AUDIT

Implementation audited:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Deployment performed: NO

Production modified: NO

Runtime modified during this audit: NO

Planner modified during this audit: NO

Authority modified during this audit: NO

Restore Barrier modified during this audit: NO

## Mission

Prove whether the Observation -> L3 Wake bridge changed only the Wake source or accidentally changed downstream execution contracts.

## Verdict

`CONTRACT_COMPATIBLE_WITH_MINOR_EXTENSION`

The implementation did not create a new execution path.

The first changed contract is the Wake evidence input contract:

`tools/v7-users-autoswitch._emergency_failover_move_evidence()` may now emit optional `current_channel_failure` evidence, and `tools/v7-users-autoswitch._l3_wake_decision()` may consume it as `confirmed_current_channel_failure`.

Downstream execution contracts remain compatible and owned by the existing governed L3 execution chain.

## Allowed Difference

Old wake source:

`confirmed_service_failure`

New wake source:

`confirmed_current_channel_failure`

No downstream owner consumes the wake source as execution authority. Wake acceptance remains evidence only; execution still requires the existing Authority, Restore Barrier, Runtime eligibility, apply, verification, rollback/no-rollback, and learning contracts.

## Reference Paths Compared

Old path:

`confirmed_service_failure -> Incident -> Planner -> Authority -> Approved Plan Lock -> Restore Barrier -> Runtime -> Apply -> Verification -> Learning`

New path:

`confirmed_current_channel_failure -> Incident -> Planner -> Authority -> Approved Plan Lock -> Restore Barrier -> Runtime -> Apply -> Verification -> Learning`

## Contract Matrix

| Owner | Input contract | Output contract | Old path | New path | Classification |
| --- | --- | --- | --- | --- | --- |
| Observation | `v7-state.json`, `users.registry`, service matrix | Candidate current state | Service failure could be derived from service matrix rows | Channel failure can be derived from `diagnose_severity=FAIL`, `diagnose_reason=interface_down_or_missing`, affected users, fresh `v7-state.json` | COMPATIBLE |
| Wake | `move_evidence[]`, allowed/rejected wake source policy | `v7.l3-wake-decision.v1` | Accepts `confirmed_service_failure`; also inferred `confirmed_current_channel_failure` when service failure exists | Accepts `confirmed_current_channel_failure` from current-channel failure evidence | CHANGED |
| Incident | Emergency failover gate, selected moves, selected hash, operation | `v7.l3-incident-context.v1` | `failure_family=CURRENT_CHANNEL_FAILED`, `service_family=[required service]` | Same incident schema and failure family; `service_family=["current_channel_failure"]` when no service-specific failure exists | COMPATIBLE |
| Planner | Decisions and selected moves | Selected move set | `user_ip`, `current_egress`, `recommended_egress`, `move_type=failover` | Same selected move contract | IDENTICAL |
| Authority | Selected moves, restore barrier, approved plan lock validation | `v7.emergency-failover-autonomy-gate.v1` | Requires one-user bounds, failover move, accepted wake, incident key, safety gates | Same gate and same one-user bounds | IDENTICAL |
| Approved Plan Lock | `v7.approved-plan-lock.v1` | lock validation | Validates schema, selected moves, selected hash, users, targets, expiry, no replacement/reselection | Same lock contract; no wake-source field added | IDENTICAL |
| Restore Barrier | Restore barrier state, selected move hash/count, generation, approved lock | clearance/execution gate | Budget/generation/source-bundle checks | Same barrier object and checks | IDENTICAL |
| Runtime eligibility | Plan, selected moves, wake, incident, live users/egress | `v7.l3-execution-eligibility.v1` | Requires gate ok, wake accepted, incident ready, exactly one move, operation id/hash, live source/target | Same requirements | IDENTICAL |
| Apply | Selected moves, operation id/hash, atomic envelope, l3 eligibility | apply result rows | Calls `v7-user-switch` for selected move; verifies and rolls back if needed | Same apply loop; no branch for wake source | IDENTICAL |
| Verification | Apply result and emergency mode | verify route/service results | Route verify and required service verify in emergency mode | Same verification behavior | IDENTICAL |
| Learning | Operation, incident, apply results | outcome/trust/prediction/recommendation/closure records | Uses operation id, incident key, selected move hash, source/target/user/outcome | Same learning contract | IDENTICAL |

## Object Schema Comparison

### Wake Object

Schema: `v7.l3-wake-decision.v1`

Same fields preserved:

- `decision`
- `accepted`
- `requested_wake_source`
- `accepted_wake_sources`
- `rejected_wake_sources`
- `allowed_wake_sources`
- `failed_sources`
- `failed_services`
- `observed_events`
- `consumed_event_ids`
- `late_event_ids`
- `blockers`
- `wake_may_grant_execution`
- `runtime_apply_allowed_now`
- `authority_expanded`

Changed compatible field values:

- `accepted_wake_sources` may include `confirmed_current_channel_failure` without `confirmed_service_failure`.
- `observed_events[].path` may be `inferred:v7-state-current-channel-failure`.
- `observed_events[].service` may be empty for channel-level failure.

Classification: CHANGED, compatible.

### Incident Object

Schema: `v7.l3-incident-context.v1`

Same fields preserved:

- `incident_state`
- `incident_key`
- `incident_key_components`
- `incident_generation`
- `authority_object`
- `allowed_move`
- `allowed_reason`
- `affected_users`
- `failed_sources`
- `failed_required_services`
- `target_channels`
- `selected_move_hash`
- `operation_id`
- `event_collapse`
- `incident_merge`
- `incident_split`
- `planner_consumption`
- behavior contracts
- operator surface
- production validation ladder
- certification pipeline

Changed compatible fields:

- `incident_key_components.service_family` may be `["current_channel_failure"]` when channel failure is proven and no required-service row is failed.
- Optional `confirmed_current_channel_failures[]` is added for evidence provenance.
- `failed_required_services=[]` remains truthful when no service-specific failure is proven.

Classification: COMPATIBLE.

## Identity Proof

Downstream owners receive the same object type:

- Selected move object remains `{user_ip, current_egress, recommended_egress, move_type}` plus existing semantic fields.
- Operation object remains `runtime_autoswitch`.
- Atomic execution envelope remains `v7.atomic-execution-envelope.v1`.
- Approved plan lock remains `v7.approved-plan-lock.v1`.
- L3 execution eligibility remains `v7.l3-execution-eligibility.v1`.
- Apply result rows remain per selected move.
- Learning records remain outcome/trust/prediction/recommendation/closure rows.

Downstream identity fields are preserved:

- `operation_id`
- `planner_generation_id`
- `selected_move_hash`
- `selected_move_count`
- `selected_move_index`
- `atomic_execution_envelope_id`
- `atomic_execution_envelope_hash`
- `incident_key`
- `user_ip`
- `current_egress`
- `recommended_egress`
- `move_type`

The only semantic identity difference is inside the incident key components:

- old service-family dimension: service ids from failed required services
- new service-family dimension: `current_channel_failure`

This does not create a new incident schema. It preserves the existing incident key split rule: different source/service-family/authority/generation splits incidents.

## Incident Semantics Investigation

Function: `tools/v7-users-autoswitch._l3_incident_context()`

Result:

`OWNER_REUSE`

The implementation did not create a new Incident type.

The same `v7.l3-incident-context.v1` object is created with:

- `authority_object=EMERGENCY_FAILOVER_AUTONOMY`
- `allowed_move=FAILOVER`
- `allowed_reason=CURRENT_CHANNEL_FAILED`
- same `event_collapse`
- same `incident_merge`
- same `incident_split`
- same `planner_consumption`
- same operator surface / validation ladder / certification pipeline

The compatible extension is that `service_family` can be `["current_channel_failure"]` for channel-level failure evidence, and optional provenance is exposed as `confirmed_current_channel_failures[]`.

Classification: OWNER_REUSE.

## Authority Proof

Functions:

- `tools/v7-users-autoswitch._emergency_failover_authority_gate()`
- `tools/v7-users-autoswitch._approved_l3_production_validation_envelope()`

Authority receives the same execution contract:

- selected moves
- restore barrier
- approved plan lock validation
- one-user bound
- failover-only move
- verification required
- rollback required
- no batch movement
- user/target scope match

No new authority envelope was introduced.

No new packet was introduced.

No new approval path was introduced.

No new authority writer was introduced.

Wake remains non-authorizing because the wake decision explicitly preserves:

- `wake_may_grant_execution=False`
- `authority_expanded=False`

Classification: IDENTICAL downstream authority contract.

## Restore Barrier Proof

Functions:

- `tools/v7-users-autoswitch._approved_plan_lock_validation()`
- restore barrier generation / clearance checks in `tools/v7-users-autoswitch.plan()`

Restore Barrier receives the same object:

- same restore barrier file
- same selected move hash
- same selected move count
- same generation clearance fields
- same approved plan lock fields
- same allowed users
- same allowed targets
- same source bundle lease checks

No new restore barrier generation was added.

No bypass was added.

No synthetic clearance was added.

No synthetic packet was added.

Classification: IDENTICAL.

## Runtime Proof

Functions:

- `tools/v7-users-autoswitch._l3_execution_eligibility()`
- `tools/v7-users-autoswitch.apply()`

Runtime receives the same execution object:

- plan
- selected move
- operation id
- selected move hash
- atomic execution envelope
- L3 incident
- L3 wake decision
- live users
- live egress

Runtime eligibility still requires:

- authority gate ok
- wake accepted
- incident ready
- exactly one selected move
- selected move hash present
- operation id present
- move execution mode emergency failover
- move type failover
- selected move identity matches operation identity
- user/source/target still live
- source not recovered before apply
- target services ready

No Runtime branch was added.

No Runtime shortcut was added.

No Runtime special-case for `confirmed_current_channel_failure` was added.

Classification: IDENTICAL runtime contract with compatible upstream evidence.

## End-To-End Ownership Proof

| Transition | Producer | Consumer | Contract | Changed? | Reason |
| --- | --- | --- | --- | --- | --- |
| Observation -> Wake evidence | `_candidate()`, `_gate_basic()`, `_emergency_failover_move_evidence()` | `_l3_wake_decision()` | `move_evidence[]` | YES | Optional `current_channel_failure` evidence added |
| Wake -> Incident | `_l3_wake_decision()` | `_l3_incident_context()` | `v7.l3-wake-decision.v1` + gate evidence | YES | wake source may be `confirmed_current_channel_failure` |
| Incident -> Planner | `_l3_incident_context()` | selected move / operation plan | `v7.l3-incident-context.v1` | COMPATIBLE | same schema, optional provenance, service family extension |
| Planner -> Authority | `plan()` selected moves | `_emergency_failover_authority_gate()` | selected move list | NO | selected move contract unchanged |
| Authority -> Approved Plan Lock | `_emergency_failover_authority_gate()` | `_approved_plan_lock_validation()` | selected move hash/user/target scope | NO | no wake-source dependency |
| Approved Plan Lock -> Restore Barrier | `_approved_plan_lock_validation()` | restore barrier clearance gates | approved lock + selected hash/count | NO | no new fields required |
| Restore Barrier -> Runtime | restore barrier gates | `_l3_execution_eligibility()` | selected move + operation identity | NO | no bypass, no synthetic clearance |
| Runtime -> Apply | `_l3_execution_eligibility()` | `apply()` | `EXECUTE` or `STOP_SAFE` | NO | same eligibility object |
| Apply -> Verification | `apply()` | route/service verification calls | apply result row | NO | same verification behavior |
| Verification -> Learning | `apply()` / `finalize_operation()` | `_l3_materialize_learning_closure()` | operation + incident + apply result | NO | same learning records |

## Test Evidence

Command:

```bash
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 127 tests in 9.936s
OK
```

Covered compatibility cases:

- `confirmed_service_failure` path still accepts wake and reaches incident.
- `confirmed_current_channel_failure` path accepts wake from `FAIL/interface_down_or_missing` and affected users.
- timer path still rejects wake even when channel failure evidence exists.
- selected move remains one affected user from failed source.
- selected move remains `move_type=failover`.
- `selected_moves_after_gate == 1`.
- broad automation remains disabled.
- governed canary CLI tests still pass.

## Changed Contracts

Only these contracts changed:

1. `move_evidence[]`
   - Added optional `current_channel_failure` evidence object.

2. `v7.l3-wake-decision.v1`
   - `accepted_wake_sources` may now contain `confirmed_current_channel_failure` produced from Observation.
   - `observed_events[]` may include a deterministic inferred current-channel failure event.

3. `v7.l3-incident-context.v1`
   - Optional `confirmed_current_channel_failures[]` provenance field.
   - `incident_key_components.service_family` may be `["current_channel_failure"]` for channel-only failure evidence.

No Authority, Approved Plan Lock, Restore Barrier, Runtime, Apply, Verification, or Learning contract changed.

## Deployment Recommendation

`SAFE_TO_DEPLOY`

Deploy only through the existing safe deployment and bounded governed L3 production validation ladder.

Do not enable broad automation.

Do not move more than one user in the first validation.

Do not bypass Authority, Approved Plan Lock, Restore Barrier, Runtime eligibility, Verification, Rollback/no-rollback closure, or Learning.
