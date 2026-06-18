# V7 System Map

Status: compact current system map
Last verified commit: `8ba2178f`
Last verified date: 2026-06-18

| Module | Purpose | Main files | Truth source | Related reference section | Related reports | Last verified commit |
| --- | --- | --- | --- | --- | --- | --- |
| Channels UI | Operator channel inventory and drawer surfaces | `admin/v7-admin-api` | Derived from channel registry, planner assignment truth, service/route/runtime evidence | Channels; Channel Decision V7; Admin UI Operator Model | `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md` | `8ba2178f` |
| Channel Decision Adapter | Exposes planner-derived decision as Use/Evacuate/Keep/Emergency/Blocked | `admin_core/operator_decision_surface.py`, `admin/v7-admin-api` | `tools/v7-users-autoswitch` candidates, blockers, selected moves, channel role flags | Channel Decision V7; Assignment | `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md` | `8ba2178f` |
| Channel Score / Technical Health | Explains channel condition as score and breakdown | `admin/v7-admin-api` channel suitability helpers | Existing channel suitability components | Channel Score; Technical Health | `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md` | `8ba2178f` |
| Channel Operator Signal Model | Classifies channel signals as operator, supporting, or diagnostics-only | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch` | Existing assignment truth, score breakdown, service/capacity/route/runtime/history signals | Channel Operator Signal Model | `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2_TABLE_IMPLEMENTATION_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, ADR-006, ADR-007 | `021e7312` |
| Planner / Autoswitch | Candidate ranking, blockers, selected moves, assignment/retention/evacuation truth | `tools/v7-users-autoswitch` | Runtime/user/channel/policy/service/route/capacity gates | Planner; Assignment; Capacity | `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md` | `8ba2178f` |
| Operator Decision Surface | Read-only projection of planner/user/channel decisions for admin | `admin_core/operator_decision_surface.py`, `admin/v7-admin-api` | Planner outputs plus existing user/channel state | Planner; Admin UI Operator Model | `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md` | `8ba2178f` |
| Service Matrix | Per-service diagnostic checks and freshness | Runtime tools `v7-service-matrix-refresh-all`, `v7-service-matrix-test`; `admin/v7-admin-api` | Service matrix test output | Service Matrix | `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_2_OPERATOR_SURFACE_SIMPLIFICATION_REPORT.md` | `8ba2178f` |
| Route Reality | Route/readiness/leak/mismatch evidence | `admin_core/route_reality_views.py`, `admin_core/route_views.py`, `admin/v7-admin-api` | Runtime route tables and route read models | Route | `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md` | `8ba2178f` |
| Runtime Readiness | Runtime readability and safety readiness | `admin_core/runtime_read_views.py`, `admin_core/operator_execution_pipeline.py`, `admin/v7-admin-api` | Runtime files, registry, restore barrier, execution packet/gates | Runtime Readiness; Truth / Convergence | `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`, `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md` | `8ba2178f` |
| Capacity / Load | Bounds user movement and channel suitability under load | `tools/v7-users-autoswitch`, `admin_core/diagnostic_views.py`, `admin/v7-admin-api`, runtime support `v7-capacity-*` | Egress registry, current/projected users, policy load settings | Capacity | `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md` | `8ba2178f` |
| Users / Identity | User profile, connection, channel, route, company/phone/access state | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `admin_core/explainability_adapter.py` | User/identity registry, runtime status, profile and route state | Users; Groups / Policies | `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md`, `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md` | `8ba2178f` |
| Groups / Policies | Policy constraints for access, movement, quality and load | `admin/v7-admin-api`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_pipeline.py` | Policy settings, org/group identity, planner/execution gates | Groups / Policies | `docs/phase5/POLICY_BASED_ACCESS.md`, `docs/phase5/MULTITENANT_MODEL.md` | `8ba2178f` |
| Intelligence / History | Historical and derived diagnostic evidence | `admin_core/intelligence_platform.py`, `admin_core/intelligence_snapshots.py`, `admin_core/intelligence_workers.py` | Existing snapshots/logs/evidence | History; Autonomy | `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md` | `8ba2178f` |
| Shadow Autonomy | Read-only autonomy/intelligence comparison and recommendation support | `admin_core/shadow_autonomy.py`, `admin_core/operator_execution_pipeline.py` | Existing planner/execution truth and governance | Autonomy | `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md` | `8ba2178f` |
| Truth / Convergence | Repo/runtime/deploy alignment guard | `tools/v7-truth-check`, `tools/v7-convergence-status`, `tools/v7_sync_lib.py` | Runtime fingerprints, repo commit, approved deploy files | Truth / Convergence | `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`, `PROGRAM_Z8_8_TRUTH_MANIFEST_AND_V7_TRUTH_CHECK_IMPLEMENTATION_REPORT.md` | `8ba2178f` |
| Attention / Overview | Derived operator attention layer over existing objects | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py` | Existing alerts, checks, recommendations, user/channel/route state | Admin UI Operator Model | `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md` | `8ba2178f` |

## Workflow Integration Rule

Major logic, planner, UI meaning, governance, runtime, or truth-source work must update the canonical reference before commit. If the work changes a decision, add or update an ADR. Then run:

1. `tools/v7-truth-check --all --json`
2. `tools/v7-convergence-status --json`

Commit code and reference updates together so V7 knowledge does not split between code, reports, and chat.

## Reference First Workflow

Future questions and audits must follow this path:

```text
Question
  |
  v
V7_CANONICAL_REFERENCE.md
  |
  v
Relevant ADRs
  |
  v
SYSTEM_MAP.md
  |
  v
Audit only if still needed
```

Use this workflow for recurring concepts such as Route, Capacity, Channel Score, Technical Health, Planner, Assignment, Service Matrix, Trust, Recovery, and Autonomy. If the answer already exists, use the reference answer. If the answer is stable but incomplete, update the reference. Start a new audit only when the reference has no answer, marks the area `UNKNOWN`, system behavior changed after the last verified commit, or current evidence contradicts the reference.
