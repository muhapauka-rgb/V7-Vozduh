# PROGRAM RI.3 Advisory Decision Integration And Routing Intelligence Certification Report

Project: V7 Vozduh

Branch: `Updatesystem`

Workspace: `/Users/ponch/Documents/New project`

Mode: implementation

Runtime mutation: not performed

User movement: not performed

Deploy: not performed

## 1. Human Explanation Of Routing Brain

Routing Brain is an advisory intelligence layer.

It reads existing truth inputs:

- service matrix;
- egress quality history;
- service preferences;
- user service weights;
- switch/audit history;
- execution trust signals.

It produces bounded advice:

- service history score;
- weighted service score;
- execution trust score;
- service confidence score;
- degradation risk score;
- dynamic blast radius recommendation;
- candidate explanation.

It does not:

- create candidates;
- move users;
- approve execution;
- write selected moves;
- bypass planner gates;
- bypass governance;
- bypass canary reservation;
- bypass best available pool;
- mutate runtime state.

Authority chain remains:

```text
Routing Brain advises.
Planner decides.
Governance authorizes.
Runtime executes.
Audit records.
Closure records.
```

## 2. Discovery

Evidence:

```text
ri3_evidence/discovery_and_duplication_audit.md
```

Existing components found:

| Component | Location | RI.3 decision |
| --- | --- | --- |
| Runtime planner | `tools/v7-users-autoswitch` | Reuse and extend ranking only |
| Candidate scoring | `tools/v7-users-autoswitch::_score_parts` | Add bounded `routing_intelligence` score part |
| Candidate ranking | `tools/v7-users-autoswitch::_decision_for_user` | Reuse |
| Best available pool | `tools/v7-users-autoswitch::_mark_best_available_pool` | Preserve |
| Capacity routing | `tools/v7-users-autoswitch::_capacity_decision` | Preserve |
| Service-aware routing | `tools/v7-users-autoswitch::_service_suitability` | Preserve |
| Service History | `admin_core/routing_intelligence.py::ServiceHistoryStore` | Reuse |
| User Service Weights | `admin_core/routing_intelligence.py::UserServiceWeights` | Reuse |
| Execution Trust | `admin_core/routing_intelligence.py::ExecutionTrustModel` | Reuse |
| Dynamic Blast Radius | `admin_core/routing_intelligence.py::DynamicBlastRadiusModel` | Reuse as advice |
| Routing Brain | `admin_core/routing_brain.py::RoutingBrain` | Extend with RI.3 candidate advisory contract |
| Shadow replay | `tools/v7-routing-intelligence-shadow` | Reuse |

## 3. Duplication Audit

No second planner was created.

No second governance system was created.

No second routing authority was created.

No duplicate service history model was created.

No duplicate user weighting model was created.

No duplicate execution trust model was created.

No duplicate blast-radius model was created.

The existing planner path is reused.

## 4. Advisory Score Contract

Implemented in:

```text
admin_core/routing_brain.py
```

New schema:

```text
ri3.candidate-advisory-scores.v1
ri3.candidate-advisory-score.v1
ri3.intelligence-advisory-contract.v1
```

Brain may contribute:

- `service_history_score`
- `weighted_service_score`
- `execution_trust_score`
- `service_confidence_score`
- `degradation_risk_score`
- bounded `score_part`

Contract constraints:

```text
may_create_candidates=false
may_change_hard_gates=false
may_change_reservation=false
may_change_governance=false
may_change_runtime_execution=false
```

## 5. Service History Integration

Implemented in:

```text
admin_core/routing_brain.py::RoutingBrain.candidate_advisory_scores
```

The score uses existing RI.1 service history across:

```text
1h
24h
7d
30d
```

Window weights:

```text
1h=0.40
24h=0.30
7d=0.20
30d=0.10
```

Effect:

```text
Two channels with the same current service snapshot can rank differently
when one has better historical service stability.
```

## 6. User Weight Integration

Implemented in:

```text
admin_core/routing_intelligence.py::UserServiceWeights
admin_core/routing_brain.py::RoutingBrain.candidate_advisory_scores
tools/v7-users-autoswitch
```

Effect:

```text
Telegram-heavy user -> Telegram quality has higher advisory influence.
ChatGPT-heavy user -> ChatGPT quality has higher advisory influence.
```

Certified by:

```text
tests.unit.test_routing_brain.RoutingBrainPlannerIntegrationTest.test_ri3_influences_planner_ranking_among_eligible_candidates
```

The replay fixture uses two equal base-score eligible candidates:

- `a_telegram`
- `z_chatgpt`

The ChatGPT-heavy user's weights give `z_chatgpt` a stronger RI score part, so planner ranks it first. Planner still owns the decision.

## 7. Execution Trust Integration

Implemented in:

```text
admin_core/routing_intelligence.py::ExecutionTrustModel
admin_core/routing_brain.py::RoutingBrain.candidate_advisory_scores
```

Execution trust contributes to:

- candidate confidence;
- blast-radius recommendation;
- advisory score.

It does not contribute to:

- governance approval;
- runtime execution authority;
- selected moves writing.

## 8. Degradation Risk Model

Implemented in:

```text
admin_core/routing_brain.py::RoutingBrain.candidate_advisory_scores
```

Risk is advisory and based on:

- weighted service score;
- current 1h score vs 24h/7d/30d baseline;
- service confidence.

Output:

```text
degradation_risk_score
```

This does not hard-block a candidate by itself. Planner hard gates remain separate.

## 9. Planner Influence

Implemented in:

```text
tools/v7-users-autoswitch
```

Changes:

- `Candidate` now carries `routing_intelligence`;
- planner calculates RI advice per user/service/route-class set;
- eligible candidate score parts include `routing_intelligence`;
- candidate JSON exposes RI explanation and authority;
- top-level `routing_brain` summary shows candidate ranking influence.

Bounded influence:

```text
score_part = clamp((advisory_score - 50) * 2, -100, 100)
```

RI score is added only after hard gates and only for eligible candidates.

## 10. Hard Gate Preservation

Certified by:

```text
tests.unit.test_routing_brain.RoutingBrainPlannerIntegrationTest.test_ri3_does_not_bypass_canary_reservation_or_create_candidates
```

Result:

- `z_chatgpt` receives strong RI advice;
- when marked `canary_reserved=true`, it remains blocked;
- planner selects another eligible candidate;
- no new candidate appears.

## 11. Explainability

For every candidate planner output now exposes:

```text
routing_intelligence.score_part
routing_intelligence.advisory_score
routing_intelligence.service_history_score
routing_intelligence.weighted_service_score
routing_intelligence.execution_trust_score
routing_intelligence.service_confidence_score
routing_intelligence.degradation_risk_score
routing_intelligence.explainability
routing_intelligence.authority
```

Human-readable planner explanation includes:

```text
routing intelligence <recommendation> score_part <n> risk <n>
```

Rejected candidates still show either:

- hard block reason;
- lower score reason.

## 12. Shadow Replay

Evidence:

```text
ri3_evidence/shadow_replay_summary.md
ri3_evidence/ri3_shadow_replay.json
```

Shadow command reused:

```text
tools/v7-routing-intelligence-shadow
```

Observed:

- execution trust score: `70.0`
- dynamic blast radius recommendation: `3`
- service risk input: `24.783`
- platform health input: `75.217`
- mode remains `shadow_read_only`
- runtime decision authority remains none

Planner behavior replay:

- RI.3 changes ranking among already eligible candidates;
- RI.3 does not create candidates;
- RI.3 does not bypass reservation.

## 13. Performance Impact

Evidence:

```text
ri3_evidence/performance_certification.md
```

Measured tests:

```text
python3 -m unittest tests.unit.test_routing_brain
Ran 14 tests in 0.127s
OK

python3 -m unittest discover tests/unit
Ran 195 tests in 13.942s
OK

python3 -m unittest discover tests/contracts
Ran 5 tests in 0.265s
OK
```

Planner caches RI candidate scores per user/service/route-class set during one planner run.

No network lookup was added.

No runtime write was added.

No governance mutation was added.

Recommended future optimization before large pools:

- pre-aggregate service history;
- cache user service weights;
- keep execution trust compact;
- use background computation for admin-only views.

## 14. Tests

Evidence:

```text
ri3_evidence/test_results.md
```

Commands run:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin_core/routing_brain.py admin_core/routing_intelligence.py tools/v7-users-autoswitch
python3 -m unittest tests.unit.test_routing_brain
python3 -m unittest tests.unit.test_routing_intelligence tests.unit.test_v7_users_autoswitch_policy tests.unit.test_best_available_pool_policy
python3 -m unittest discover tests/unit
python3 -m unittest discover tests/contracts
```

All passed.

## 15. Files Changed

Code:

```text
admin_core/routing_brain.py
admin_core/routing_intelligence.py
tools/v7-users-autoswitch
tests/unit/test_routing_brain.py
```

Evidence:

```text
ri3_evidence/discovery_and_duplication_audit.md
ri3_evidence/performance_certification.md
ri3_evidence/ri3_shadow_replay.json
ri3_evidence/shadow_replay_summary.md
ri3_evidence/test_results.md
```

Final report:

```text
PROGRAM_RI3_ADVISORY_DECISION_INTEGRATION_AND_ROUTING_INTELLIGENCE_CERTIFICATION_REPORT.md
```

## 16. Final Verdicts

```text
service_history_integrated=true
user_weights_integrated=true
execution_trust_integrated=true
risk_model_integrated=true
planner_influence_active=true
planner_ownership_preserved=true
governance_preserved=true
performance_certified=true
tests_pass=true
routing_intelligence_advisory_certified=true
```

## 17. Safety

```text
routing_brain_moved_users=false
routing_brain_approved_execution=false
routing_brain_bypassed_planner=false
routing_brain_bypassed_governance=false
runtime_mutation_performed=false
users_moved=false
autoswitch_apply_run=false
routing_changed=false
deploy_performed=false
systemd_changed=false
```

## 18. Certification

PASS.

Routing Brain now influences planner ranking.

Planner remains the decision owner.

Governance remains the authorization owner.

Runtime remains the execution owner.

Performance remains acceptable for current test scale.

Routing Intelligence is operational as advisory planner influence, not authority.

