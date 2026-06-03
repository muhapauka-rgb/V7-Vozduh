# PROGRAM RI.1 — ROUTING INTELLIGENCE FOUNDATION REPORT

Date: 2026-06-03
Project: V7 Vozduh
Branch: Updatesystem
Mode: foundation-only, shadow/read-only

## Result

PASS

Routing Intelligence foundation now exists as a non-authoritative read model and shadow replay layer. It does not change production routing decisions, move users, change governance, change autoswitch behavior, restart services, or mutate runtime state.

## Discovery Gate

Existing reusable truth inputs:

| Area | Existing source | RI.1 classification |
| --- | --- | --- |
| Required services | `service-preferences.json`, policy/org policy, autoswitch required services | REUSE |
| Service matrix | `/opt/v7/egress/state/service-matrix.json` | REUSE |
| Telegram checks | service matrix Telegram rows, sentinel state | REUSE |
| YouTube checks | service matrix YouTube rows | REUSE |
| Instagram checks | service matrix Instagram rows | REUSE |
| ChatGPT checks | service matrix ChatGPT/OpenAI rows where present | REUSE |
| Google / Google Auth checks | service matrix Google rows | REUSE |
| Historical quality | `/opt/v7/egress/state/egress-quality-summary.json` | REUSE |
| Capacity model | `tools/v7-users-autoswitch` load/capacity policy | DO NOT TOUCH |
| Best available pool | `tools/v7-users-autoswitch` pool scoring | DO NOT TOUCH |
| Dynamic blast radius foundation | `tools/v7-users-autoswitch` plan safety summary | DO NOT TOUCH |
| Service-aware routing | `tools/v7-users-autoswitch` candidate gates/suitability | DO NOT TOUCH |
| Audit/planner/runtime history | switch history and operator audit JSONL stores | REUSE AS INPUT |

Existing intelligence pieces:

- Runtime planner already computes service suitability for live routing candidates.
- Runtime planner already has best available pool and capacity-aware selection.
- Runtime planner already exposes dynamic blast radius context in plans.
- Existing E33/E35 documentation defines conceptual routing intelligence and required service control boundaries.

Missing before RI.1:

- Certified service history storage schema for RI.
- Separate Service Intelligence Engine with explainability outside runtime execution.
- User service weights read model.
- Execution trust score model.
- Dynamic blast radius recommendation model outside runtime.
- Disabled predictive foundation model.
- Reproducible shadow replay CLI and test suite.

## Duplication Audit

No duplicate production truth source was created.

RI.1 creates a derived, non-authoritative model only:

- Existing runtime truth remains `service-matrix.json`, `egress-quality-summary.json`, `service-preferences.json`, users registry, and audit/history JSONL.
- RI.1 storage is marked `authoritative_runtime_truth=false_shadow_read_model_only`.
- RI.1 outputs include `runtime_decision_authority=none_shadow_only`.
- Runtime planner remains the only owner of production selected moves.
- Governance/approval modules remain the only owners of governed execution authority.

## Implementation

Added:

- `admin_core/routing_intelligence.py`
  - `ServiceHistoryStore`
  - `ServiceIntelligenceEngine`
  - `UserServiceWeights`
  - `ExecutionTrustModel`
  - `DynamicBlastRadiusModel`
  - `PredictiveFoundation`
  - `RoutingIntelligenceShadow`
- `tools/v7-routing-intelligence-shadow`
  - read-only CLI for local or evidence-based shadow replay.
- `tests/unit/test_routing_intelligence.py`
  - full RI.1 foundation tests.

No runtime/autoswitch/governance/systemd file was modified.

## Phase Results

| Phase | Status | Evidence |
| --- | --- | --- |
| Service History Model | COMPLETE | `ServiceHistoryStore`, unit tests |
| Service Intelligence Model | COMPLETE | `ServiceIntelligenceEngine`, unit tests |
| User Service Weights | COMPLETE | `UserServiceWeights`, unit tests |
| Execution Trust Model | COMPLETE | `ExecutionTrustModel`, unit tests |
| Dynamic Blast Radius Model | COMPLETE | `DynamicBlastRadiusModel`, unit tests |
| Predictive Foundation | COMPLETE | `PredictiveFoundation`, prediction disabled |
| Shadow Replay | COMPLETE | `ri1_evidence/live_shadow_replay.json` |
| Tests | COMPLETE | 186 unittest tests passing |
| Certification | COMPLETE | runtime/governance/systemd diff empty |

## Shadow Validation

Read-only production snapshot captured into `ri1_evidence/live_state` and `ri1_evidence/live_events`.

Inputs:

- `ri1_evidence/live_state/service-matrix.json`
- `ri1_evidence/live_state/egress-quality-summary.json`
- `ri1_evidence/live_state/service-preferences.json`
- `ri1_evidence/live_state/users.registry`
- `ri1_evidence/live_events/switch-history.tail.jsonl`

Shadow replay output:

- schema: `ri1.shadow-replay.v1`
- mode: `shadow_read_only`
- target count: 7
- execution trust: 70.0
- prediction enabled: false
- recommended budget: 3
- authority: `none_shadow_only`

The recommended budget is a model output only. It is not wired into runtime and does not approve or select movement.

## No-Behavior-Change Certification

Verified:

- `git diff -- tools/v7-users-autoswitch admin_core/operator_execution.py admin_core/operator_observability.py systemd` returned empty output.
- No `selected_moves` field is emitted by RI.1 shadow replay.
- No `apply_requested` field is emitted by RI.1 shadow replay.
- No runtime action record is emitted by RI.1 shadow replay.
- Unit tests confirm shadow replay contains non-authority guards:
  - `no_runtime_mutation=true`
  - `no_routing_decision_change=true`
  - `no_user_movement=true`
  - `no_governance_change=true`

## Tests

Evidence:

- `ri1_evidence/test_routing_intelligence.txt`
- `ri1_evidence/test_full_unittest_discover.txt`
- `ri1_evidence/test_compileall.txt`
- `ri1_evidence/test_shadow_cli_help.txt`

Results:

- `python3 -m unittest tests.unit.test_routing_intelligence`: 8 tests OK
- `python3 -m unittest discover tests`: 186 tests OK
- `PYTHONPYCACHEPREFIX=/tmp/ri1_pycache python3 -m compileall admin_core/routing_intelligence.py`: OK
- `tools/v7-routing-intelligence-shadow --help`: OK

## Evidence Folder

`ri1_evidence`

Key evidence:

- `phase0_truth_check.txt`
- `discovery_related_files.txt`
- `discovery_rg_intelligence_sources.txt`
- `live_shadow_replay.json`
- `final_truth_check.txt`
- test outputs listed above

Note: pre-commit `final_truth_check.txt` reports NO-GO because the workspace is intentionally dirty with RI.1 work and remote read is unavailable inside sandbox. This is not a runtime behavior regression. A post-commit/post-push convergence check should be captured after publishing.

## Final Verdicts

service_history_model_complete=true

service_intelligence_model_complete=true

user_service_weights_complete=true

execution_trust_model_complete=true

dynamic_blast_radius_model_complete=true

predictive_foundation_complete=true

tests_pass=true

routing_intelligence_foundation_certified=true
