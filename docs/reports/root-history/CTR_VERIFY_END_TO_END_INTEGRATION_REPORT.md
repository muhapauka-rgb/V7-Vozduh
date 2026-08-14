# PROGRAM CTR.VERIFY - End-To-End CTR Integration Verification

Дата: 2026-06-11  
Проект: V7 Vozduh  
Ветка: Updatesystem  
Режим: READ ONLY / TEST ONLY  
Финальный вердикт: **CTR_INTEGRATED_WORKING**

## 1. Executive Summary

CTR реально встроен в код и работает в сертифицированной роли:

```text
CTR = advisory + explainability + governance evidence + shadow comparison
```

CTR не является:

- planner authority;
- runtime authority;
- hard gate;
- selected move writer;
- packet approver;
- restore barrier writer;
- routing mutator.

Проверено:

- CTR truth source читается из существующей intelligence snapshot семьи `trust-evolution-summaries.channel_trust_recovery`.
- Planner прикрепляет `ctr_advisory` к candidate rows.
- Review semantics работают для `TRUSTED`, `WATCH`, `NEW`, `RECOVERING`, `DEGRADED`, `QUARANTINED`.
- Governance/packet evidence содержит CTR review поля.
- Dry-run score simulation существует.
- `ctr_shadow_comparison` существует.
- CTR не меняет production score, score_parts, selected moves, runtime, routing, governance authority или packet authority.
- Production read-only dry-run подтвердил наличие CTR fields в живом `/api/autoswitch-plan`.

## 2. Code Reality Map

Evidence file:

- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/code_reality_map.txt`

Main code locations:

| Purpose | File / function |
|---|---|
| CTR truth source | `admin_core/intelligence_workers.py`, `channel_trust_recovery` model |
| CTR snapshot family | `trust-evolution-summaries.channel_trust_recovery` |
| CTR planner reader | `tools/v7-users-autoswitch`, `_ctr_advisory_for_egress()` |
| CTR candidate attachment | `tools/v7-users-autoswitch`, `_candidate()` sets `c.ctr_advisory` |
| CTR candidate JSON output | `tools/v7-users-autoswitch`, `_candidate_json()` emits `ctr_advisory` and `ctr_score_simulation` |
| CTR review matrix | `admin_core/operator_decision_surface.py`, `ctr_review_semantics()` |
| Russian operator text | `admin_core/operator_decision_surface.py`, `CHANNEL_STATE_COPY` |
| Governance evidence | `admin_core/operator_decision_surface.py`, `ctr_governance_evidence` rows |
| Packet evidence | `admin_core/operator_execution_feedback.py`, `recommendation_approval_packet()` |
| Execution pipeline contract | `admin_core/operator_execution_pipeline.py` |
| Score simulation | `tools/v7-users-autoswitch`, `_attach_ctr_score_simulation()` |
| Shadow comparison | `tools/v7-users-autoswitch`, `_ctr_shadow_comparison()` |
| No-bypass flags | `tools/v7-users-autoswitch`, CTR simulation and shadow comparison flags |
| Admin surface | `admin/v7-admin-api`, channel drawer / CTR review fields |

## 3. Unit Test Results

Evidence files:

- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/tests_found.txt`
- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/targeted_unit_tests.txt`

Targeted tests run:

```text
tests.unit.test_ctr_i1_no_bypass
tests.unit.test_ctr_i2_review_required
tests.unit.test_ctr_i5_observation_window
tests.unit.test_channel_trust_recovery
tests.unit.test_operator_decision_surface
tests.unit.test_operator_execution_feedback
tests.unit.test_operator_execution_pipeline
tests.unit.test_v7_users_autoswitch_policy
```

Result:

- tests run: `133`
- failed: `0`
- errors: `0`
- verdict: `PASS`

## 4. End-To-End Fixture Test

Evidence files:

- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/fixture_verification.json`
- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/fixture_summary.json`

Fixture model:

- Reused existing `tests/unit/test_v7_users_autoswitch_policy.py` helper.
- Built temporary state dir.
- Built intelligence snapshots.
- Ran real `AutoswitchPlanner.plan()`.

Verified required candidate fields:

- `ctr_advisory.state`
- `ctr_advisory.reason`
- `ctr_advisory.recovery_state`
- `ctr_advisory.recovery_path`
- `ctr_advisory.confidence`
- `ctr_advisory.blocked_actions`
- `ctr_advisory.recommended_action`
- `ctr_advisory.soft_adjustment`
- `ctr_advisory.advisory_score`

Result:

- all candidate CTR fields present: true
- all score simulation fields present: true
- selected moves count: `0`
- apply requested: false

## 5. Review Semantics Test

Expected and verified:

| State | review_required | emergency_only |
|---|---:|---:|
| `TRUSTED` | false | false |
| `WATCH` | true | false |
| `NEW` | true | false |
| `RECOVERING` | true | false |
| `DEGRADED` | true | false |
| `QUARANTINED` | true | true |

Russian operator text:

- present: true
- tested in `test_ctr_visibility_copy_is_short_russian_and_complete_for_all_states`

Verdict: PASS

## 6. Governance Evidence Test

Verified CTR appears in:

- recommendation rows;
- batch preview;
- packet evidence preview;
- approval intent payload.

Verified fields:

- `review_required`
- `review_reason`
- `review_category`
- `review_severity`
- `emergency_only`
- `recommended_action`
- `blocked_actions`
- `recovery_path`

Packet/evidence result:

- packet schema: `v7.operator-recommendation-approval-intent.v1`
- `execution_allowed_now=false`
- CTR approval authority: `none`
- CTR denial authority: `none`
- packet authority changed: false
- execution authority changed: false

Verdict: PASS

## 7. Shadow Scoring Test

Verified score simulation fields:

- `existing_score`
- `ctr_soft_adjustment`
- `simulated_score`
- `ranking_delta`

Verified no production score mutation:

- production candidate score unchanged: true
- production `score_parts` unchanged: true
- no `ctr` entry in production `score_parts`: true
- selected moves unchanged: true
- selected move hash unchanged in existing tests: true
- `planner_score_applied=false`
- `selected_moves_changed=false`
- `runtime_behavior_changed=false`

Verdict: PASS

## 8. Shadow Comparison Test

Verified `ctr_shadow_comparison` exists in dry-run output.

Verified fields:

- `current_ranking`
- `ctr_simulated_ranking`
- `winner_without_ctr`
- `winner_with_ctr`
- `same_winner`
- `different_top3`
- `different_pool_order`
- `quality_delta`
- `service_aware_validation`
- `no_bypass`

Fixture and production dry-run both expose CTR shadow comparison.

Verdict: PASS

## 9. No-Bypass Certification

CTR cannot:

- create selected moves;
- change selected moves;
- approve packets;
- deny packets;
- write restore barrier;
- mutate runtime;
- change routing;
- change real planner score;
- change governance authority.

Evidence:

- unit tests: PASS
- fixture: all no-bypass flags PASS
- production dry-run no-bypass flags all false

Production no-bypass flags:

```text
selected_moves_changed=false
planner_ranking_changed=false
runtime_behavior_changed=false
routing_changed=false
governance_authority_changed=false
packet_authority_changed=false
```

Verdict: PASS

## 10. Production Dry-Run Check

Evidence files:

- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/production_autoswitch_plan_wrapper.json`
- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/production_autoswitch_plan.json`
- `docs/reports/evidence/CTR_VERIFY_EVIDENCE/production_dry_run_ctr_summary.json`

Access path:

- existing admin read-only endpoint: `GET /api/autoswitch-plan`
- underlying command: `v7-users-autoswitch --pretty`
- forbidden `--apply`: not used

Observed production dry-run:

- HTTP: `200`
- terminal state: `DRY_RUN`
- terminal reason: `dry_run_intelligence_snapshot_stop_required`
- users total: `26`
- candidate moves total: `8`
- selected moves: `0`
- apply requested: false
- apply result: `applied=false`, `reason=dry_run`
- `ctr_shadow_comparison` present: true
- sample candidate has `ctr_advisory`: true
- sample candidate has `ctr_score_simulation`: true

Note:

- Production admin login writes a normal auth audit event. No routing/runtime mutation was performed.

Verdict: PASS

## 11. Gaps Found

No CTR integration gap was found.

Known non-CTR operational blocker remains:

- production planner still reports snapshot stop for intelligence snapshot mismatch in live dry-run.

This does not invalidate CTR integration. It only means production selected moves remain suppressed until snapshot mismatch is closed.

CTR-specific gaps:

- none for advisory/explainability/governance/shadow role.

CTR is intentionally not a planner influence layer after PDR.1.

## 12. Final Verdict

Final verdict: **CTR_INTEGRATED_WORKING**

Final flags:

- ctr_truth_source_exists: true
- ctr_read_by_planner: true
- ctr_advisory_attached_to_candidates: true
- ctr_review_semantics_exist: true
- ctr_russian_operator_text_exists: true
- ctr_governance_evidence_exists: true
- ctr_packet_preview_evidence_exists: true
- ctr_dry_run_score_simulation_exists: true
- ctr_shadow_comparison_exists: true
- ctr_does_not_alter_selected_moves: true
- ctr_does_not_mutate_runtime: true
- ctr_does_not_change_routing: true
- ctr_does_not_change_governance_authority: true
- production_dry_run_checked: true
- tests_passed: true
- users_moved: 0
- autoswitch_apply_run: false
- deploy_run: false
- final_role: advisory + explainability + governance evidence + shadow comparison
- SAFE_NEXT_STEP: close non-CTR production snapshot mismatch, then continue planner/snapshot reliability work

