# PROGRAM RI.2 - ROUTING BRAIN INTEGRATION REPORT

Date: 2026-06-03
Project: V7 Vozduh
Branch: Updatesystem
Mode: safe advisory integration

## Result

PASS

RI.2 connects RI.1 into a single Routing Brain advisory chain. Routing Intelligence is now visible to the runtime planner as planner advisory context only. It cannot move users, cannot approve governance, cannot write selected moves, and cannot mutate runtime state.

## 1. What the Routing Brain is

The Routing Brain is the connected control-system view of V7 routing:

Raw Runtime Data -> Service History -> Service Intelligence -> User Weights -> Service Suitability -> Execution Trust -> Dynamic Blast Radius Advice -> Planner Advisory Context -> Runtime Planner -> Governance Packet -> Execution -> Audit -> Closure -> History Feedback.

It is not a duplicate planner. It is an advisory layer that lets intelligence explain risk and suitability while preserving the existing owners:

| Domain | Owner |
| --- | --- |
| Runtime truth | existing runtime state files |
| Routing decision | `tools/v7-users-autoswitch` |
| Governance authorization | existing governance/operator modules |
| Runtime execution | runtime execution tools |
| Audit/closure | audit and closure stores |
| Intelligence advice | `admin_core.routing_brain.RoutingBrain` |

## 2. How modules connect

Implemented:

- `admin_core/routing_brain.py`
  - `routing_brain_map()`
  - `RoutingBrain.advisory_context()`
  - `RoutingBrain.feedback_envelope()`
- `tools/v7-users-autoswitch`
  - reads recent switch history as audit input;
  - builds RI.2 advisory context after normal decisions and selected moves are already computed;
  - exposes `routing_brain` in plan JSON.

The planner hook is deliberately placed after candidate decisions and selected move selection. Advisory output is not used for sorting, eligibility, target choice, governance approval, or execution.

## 3. What RI can influence

RI may influence explanations and future operator review surfaces:

- service suitability advice;
- user service weight advice;
- degradation trend advice;
- execution trust advice;
- dynamic blast radius advice;
- candidate explanation advice.

Planner output now exposes:

- `intelligence_present`
- `intelligence_confidence`
- `service_history_score`
- `weighted_service_score`
- `execution_trust_score`
- `recommended_blast_radius`
- `intelligence_used_for_explanation`

## 4. What RI cannot control

The RI.2 advisory contract forbids:

- user movement;
- planner bypass;
- governance bypass;
- direct selected-move writes;
- execution approval;
- runtime state mutation.

The plan exposes:

- `planner_decision_owner=tools/v7-users-autoswitch`
- `execution_authority=none`
- `selected_moves_write_authority=none`

## 5. How service history affects advice

`RoutingBrain` reuses RI.1 `ServiceHistoryStore` and `ServiceIntelligenceEngine`.

Bad service history lowers `service_history_score` and target service scores. Strong service history improves them. This changes advisory values only; existing planner candidate scoring remains the runtime decision owner.

## 6. How user weights affect advice

`RoutingBrain` reuses RI.1 `UserServiceWeights`.

Service weights change `weighted_service_score`. Tests prove Telegram-heavy weights score higher when Telegram is healthy and ChatGPT is degraded. This remains advice only and does not rewrite planner selected moves.

## 7. How execution trust affects blast radius

`RoutingBrain` reuses RI.1 `ExecutionTrustModel` and `DynamicBlastRadiusModel`.

Successful execution/audit history can raise advisory blast budget. Failed executions or governance violations lower it. The result is exposed as `recommended_blast_radius`, but the runtime planner's existing policy and governance still own actual selected move limits and authorization.

## 8. How feedback returns into intelligence

RI.2 defines `RoutingBrain.feedback_envelope()`:

- execution result;
- rollback result;
- audit result;
- closure result;
- service health after movement.

The envelope is storage/model definition only:

- `autonomous_learning_enabled=false`
- `runtime_state_mutation=false`

No autonomous learning is enabled in RI.2.

## 9. Why this is one organism, not separate modules

RI.1 models are now connected to the runtime planner through one advisory contract. Runtime Planner remains the decision organ. Governance remains the authorization organ. Execution remains the hands. Audit/closure remain the memory. RI provides context and feedback, not a parallel path.

## Discovery and Duplication Audit

| Component | Classification | RI.2 action |
| --- | --- | --- |
| Runtime planner | DO NOT TOUCH decision logic | EXTEND output with advisory context |
| Service-aware routing | REUSE | no scoring replacement |
| Best available pool | REUSE | no pool/ranking change |
| Capacity-aware routing | REUSE | no capacity change |
| RI.1 Service History | EXTEND | input to advisory context |
| RI.1 Service Intelligence | EXTEND | input to advisory context |
| RI.1 User Weights | EXTEND | input to weighted advice |
| RI.1 Execution Trust | EXTEND | input to blast advice |
| RI.1 Dynamic Blast Radius | EXTEND | advice only |
| Audit history | REUSE AS INPUT | recent switch-history tail |
| Closure history | DEFINE FEEDBACK | no write path |
| Governance packets | DO NOT TOUCH | no approval path |
| Admin surfaces | FUTURE EXTEND | no UI/API mutation in RI.2 |

No duplicate truth source was created. RI.2 reads existing state and emits derived advisory context only.

## Shadow Decision Replay

Evidence: `ri2_evidence/shadow_decision_replay_comparison.json`

Result:

- semantic selected moves same: true
- candidate ranking same: true
- planner decision owner: `tools/v7-users-autoswitch`
- execution authority: `none`
- selected moves write authority: `none`

Operation IDs and selected move indexes differ between replay runs because they are generated per plan run; they are excluded from semantic routing comparison.

## Tests

Evidence:

- `ri2_evidence/test_routing_brain.txt`
- `ri2_evidence/test_full_unittest_discover.txt`
- `ri2_evidence/test_compileall.txt`

Results:

- `python3 -m unittest tests.unit.test_routing_brain`: 10 tests OK
- `python3 -m unittest discover tests`: 196 tests OK
- compile check: OK

## Certification

routing_brain_map_complete=true

intelligence_advisory_contract_complete=true

planner_integration_safe=true

feedback_loop_defined=true

shadow_replay_complete=true

no_runtime_behavior_change=true

Certification note: RI.2 changes planner JSON output by adding `routing_brain` advisory context. It does not change routing selection, candidate ranking, governance authorization, execution, or runtime state.

## Evidence Folder

`ri2_evidence`

Pre-commit truth check reports NO-GO because the workspace is dirty during RI.2 development and production runtime remains on the previous deployed commit. No production deploy was performed in this block.

## Final Verdicts

routing_brain_architecture_complete=true

intelligence_advisory_contract_complete=true

planner_integration_complete=true

feedback_loop_complete=true

tests_pass=true

shadow_replay_complete=true

no_runtime_behavior_change=true

safe_to_continue_to_RI3=true
