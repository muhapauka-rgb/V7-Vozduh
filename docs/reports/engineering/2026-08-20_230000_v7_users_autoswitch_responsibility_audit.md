# V7 Users Autoswitch Responsibility Audit Report

**Mission:** `V7_USERS_AUTOSWITCH_RESPONSIBILITY_AUDIT_V1`
**Date:** 2026-08-20
**Type:** bounded read-only code and consumer audit
**Runtime / Production / Authority / CPS effects:** `NONE / NONE / NONE / NONE`

## SUMMARY

**Verdict:** `MIXED_RESPONSIBILITY_COMPONENT; NOT_A_CLEAN_SINGLE_ORCHESTRATION_OWNER`.

`tools/v7-users-autoswitch` is a real deployed, safety-relevant component. It
is not tests-only, dead code, or a historical artifact. It is also not a thin
user-migration coordinator: the one executable combines planning, policy and
authority gates, Matrix/quality/stability reading, capacity and target ranking,
L3/passive reconciliation, controlled certification/Polygon diagnostics,
Packet/rollback support, routing apply, verification, terminal/audit
materialisation and CLI-only engineering surfaces.

No source code, Runtime, Matrix, Planner decision law, CPS, route, Packet,
lease, barrier, user or Authority was changed. Model selection is explicitly
outside this audit. Current V5.3 evidence selects B+C under existing Matrix
ownership, while automatic FAST consumer remains held; this Mission neither
changes nor anticipates that decision.

## CURRENT V5.3 / CPS CONTEXT

| Field | Current owner-backed fact |
| --- | --- |
| Active Program | `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` |
| Current stage | `V5_3_MATRIX_HEALTH_OPTIMIZATION` |
| Current CPS next action | `EXECUTE_V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS` |
| Current frontier | `ADMITTED_READY_READ_ONLY:V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS_V1` |
| Latest V5.3 terminal | `READ_ONLY_V5_3_MISSION_COMPLETE_CONSUMED` |
| Matrix full path | Existing fallback preserved |
| Automatic FAST role consumer | `HOLD_PENDING_SYSTEM_LEVEL_REVALIDATION` |
| VLESS ordinary scope | `NO_OPEN_CURRENT_VLESS_INCIDENT`; affected=0 |

## CURRENT ROLE OF V7-USERS-AUTOSWITCH

**CURRENT_RESPONSIBILITY**

`GOVERNED_USER_SWITCHING_ORCHESTRATION_AND_LEGACY_COMPATIBILITY_SURFACE`.

It consumes existing assignment, Matrix, policy, capacity, quality/stability,
L3 incident, execution-control and safety facts; produces plan/advisory
projections, governed apply attempts/verification, lifecycle records and
controlled diagnostic output. It can invoke the existing `v7-user-switch`
writer only after its gates and the external action control pass.

**DESIRED_RESPONSIBILITY**

`THIN_GOVERNED_USER_MIGRATION_COORDINATOR`:
consume canonical health/current scope and existing eligibility/Authority
facts; use the permitted Candidate/Packet/lease/barrier boundary; invoke the
single legal writer; verify; publish a minimal terminal.

**RESPONSIBILITY_GAP**

The source embeds health interpretation, quality/stability/capacity ranking,
L3/history reconciliation, controlled source/campaign diagnostics and
programme-like audit materialisation beside apply/verify. This is a future
bounded-separation hypothesis, not a deletion verdict.

## RESPONSIBILITY MAP

| Family | Inputs | Output / consumer | State / effect | Plane | Disposition |
| --- | --- | --- | --- | --- | --- |
| User decision / bounded selection | registry, assignment, policy, Matrix, quality, capacity, safety | decision rows / selected moves | reads current state; plan projection | Control | Keep; narrow only later |
| Governed execution | committed lock, execution control, Packet/lease/barrier facts | existing `v7-user-switch` | safety/execution records | Data/Control boundary | Keep safety boundary |
| Route/service verification | kernel rules/routes, Matrix path/service evidence | verification / rollback trigger | reads kernel/Matrix; outcome safety writes | Data/Control | Keep |
| Passive/L3 reconciliation | event JSONL, runtime/closure state | re-entry/outcome/closure projections | L3 and history writes | Control + Engineering tail | Separate from synchronous path, not delete |
| Health/quality/capacity interpretation | Matrix, quality, stability, load | gates/scores/ranking | reads broad state; limited load/reconnect writes | Control | Mixed owner boundary |
| Controlled certification/Polygon | drafts, reservations, campaign/Authority evidence | diagnostics / authority request output | command-specific read/write | Engineering | Not ordinary hot path |
| CLI/report helpers | explicit CLI flags | JSON diagnostic/projection | mostly read-only | Engineering/test | Keep pending consumer proof |

## RUNTIME PATH MAP

```text
Matrix health/event + registry/assignment + quality/capacity/stability + L3
  -> AutoswitchPlanner
  -> plan / advisory / governed eligibility
  -> Candidate / Packet / lease / restore barrier owners
  -> v7-user-switch only after allowed-forward-mutation
  -> route + required-service verification
  -> closure/outcome consumers

Engineering / controlled diagnostics
  -> explicit CLI branches
  -> JSON projections or existing authority-request owners
```

| Verified caller | Invocation | Consumer / effect | Classification |
| --- | --- | --- | --- |
| `v7-users-autoswitch.timer` | 20-second timer activates service | deployed lifecycle edge | Runtime, non-direct |
| `v7-users-autoswitch.service` | executes `v7-governed-canary-dry-run-cycle ... --max-users 0` | dry-run owner reaches autoswitch observe/plan path; service text contains no direct `v7-users-autoswitch --apply` | Runtime, non-mutating systemd entry |
| `v7-governed-canary-dry-run-cycle` | invokes autoswitch in `--mode observe` and guarded plan modes | controlled or dry-run planner output; wrapper records no mutation | Runtime/control consumer |
| `v7-service-matrix-refresh-all` | `--consume-service-failure-automation-only` | advisory + existing downstream OMP receipt | Runtime non-blocking tail |
| `v7-telegram-sentinel` | guarded CLI command, conditional apply mode | existing sentinel path; Matrix remains canonical health owner | conditional Runtime edge |
| Admin API | diagnostics and guarded commands | operator surface, never independent routing authority | Management |
| Tests/scenarios | imports/CLI modes | unit and controlled evidence | Test/Engineering |

No direct Python import of the extensionless executable can prove the full
dynamic graph. Static absence of a simple caller is **not** proof of dead code.

## DECISION AUTHORITY MAP

| Capability | Can autoswitch do it? | Owner/boundary | Evidence | Correct future rule |
| --- | --- | --- | --- | --- |
| Propose target | YES, bounded | Planner methods `_decision_for_user`, `_best_alternative`, `_select_moves` consume Matrix/policy/capacity facts | lines 13374-14370 | May consume, not create parallel eligibility truth |
| Change source assignment | YES, gated | `apply -> _run_switch -> v7-user-switch` | lines 14372-14922, 16958-16993 | Keep exact writer boundary |
| Create Candidate-level move | YES, projection | Planner plan output; governed packet owners remain external | lines 11345-11815 | No bypass of action contract |
| Create Packet | Indirect/bounded | existing operator-execution and approved-lock owners; rollback helper exists | lines 12783-12908 | Not independent Packet authority |
| Initiate lease | Consumes/gates only | existing execution-control/lease owner | lock and validation methods | Keep external owner |
| Mutate route / move user | YES, conditional | existing `v7-user-switch` after apply gates | `_run_switch` | Keep, never call from health code |
| Bypass Matrix | NO by contract | Matrix owns row/event; this file has no `update_matrix` definition/call | static source search | Must remain NO |
| Bypass freshness/capacity | NO by intended gates | Planner, freshness/capacity/safety and execution controls | gates 7044-14370 | Must remain NO |
| Bypass verification | NO on governed apply | route/service verify plus rollback path | lines 16995-17243 | Must remain NO |

## HEALTH RESPONSIBILITY MAP

The file does **not** write canonical Matrix health: it has no
`tools/v7-service-matrix-test.update_matrix` implementation and no
`update_matrix(...)` call. Existing Matrix test/refresh owners retain atomic
row, episode persistence and canonical service-failure observation.

It nevertheless embeds health-policy interpretation:

- `_service_truth_freshness`, `_service_truth_classification`,
  `_service_suitability*`, `_gate_service*`;
- `_quality_ok_for_load`, `_healthy_for_load`, `_severity_classification`;
- `_capacity_status`, `_load_limits_for_egress`,
  `_routing_intelligence_*`, `_best_alternative`;
- `_reuse_or_verify_emergency_required_services`, which reuses fresh Matrix
  evidence or calls the existing tester for a required subset.

**Answer:** no second canonical Health Truth owner was found. There is,
however, a second concentration of health-policy interpretation. It must not
choose Model A/B/C, maintain a second health row, or become a fast health caller
before the existing V5.3 system-level gate permits it.

## MATRIX / PLANNER / AUTOSWITCH BOUNDARIES

| Responsibility | One current owner | Autoswitch role |
| --- | --- | --- |
| Matrix row, health truth, failure episode | `v7-service-matrix-test.update_matrix` / Matrix owner | read/consume; can request existing bounded verifier only through action path |
| Passive suspicion | sentinel/passive + Matrix confirmation | cannot turn raw signal directly into movement |
| Target eligibility | Matrix + quality/capacity/policy owners | reads existing facts into planner gates |
| Target selection | existing Planner semantics currently embedded here | current implementation owner, not a reason for a new Planner |
| Movement Authority | existing action class, Packet, lease, barrier, execution control | consumes exact permitted contract |
| Route writer | `v7-user-switch` or Core writer for action class | invokes only the existing allowed writer |
| Verification / rollback | existing route, Matrix and restore owners | coordinates, does not redefine truth |

## COMPLETE FUNCTION INVENTORY

Static AST inventory contains **327 functions/methods**, **74 top-level
functions**, **4 classes/dataclasses**, and **24,651 LOC**. In the manifest:
`R` = static read helper call, `W` = existing write helper, `P` = subprocess,
`M` = mutation-capable. Group contracts above supply common inputs/outputs/state
and side-effect context. A blank flag means no such call was statically found;
it does not prove runtime purity.

| Function | Lines | Responsibility cluster | Path class | Static flags |
| --- | --- | --- | --- | --- |
| `now_iso` | 377-378 | FOUNDATION_ADMISSION | SUPPORT | - |
| `read_json` | 381-390 | FOUNDATION_ADMISSION | SUPPORT | R |
| `normalize_authority_class` | 393-395 | FOUNDATION_ADMISSION | SUPPORT | - |
| `authority_class_budget` | 398-402 | FOUNDATION_ADMISSION | SUPPORT | - |
| `normalize_authority_lifecycle_state` | 405-407 | FOUNDATION_ADMISSION | SUPPORT | - |
| `min_authority_class` | 410-414 | FOUNDATION_ADMISSION | SUPPORT | - |
| `canonical_authority_class_for_promotion` | 417-421 | FOUNDATION_ADMISSION | SUPPORT | - |
| `sha256_file` | 424-432 | FOUNDATION_ADMISSION | SUPPORT | R |
| `sha256_json` | 435-437 | FOUNDATION_ADMISSION | SUPPORT | - |
| `build_prepared_class_decision_projection` | 440-522 | FOUNDATION_ADMISSION | SUPPORT | - |
| `validate_prepared_class_decision_projection` | 525-556 | FOUNDATION_ADMISSION | SUPPORT | - |
| `matrix_comparative_probe_selection` | 559-620 | FOUNDATION_ADMISSION | SUPPORT | - |
| `_matrix_observation_refresh` | 623-645 | FOUNDATION_ADMISSION | SUPPORT | P |
| `_required_service_verdicts` | 648-672 | FOUNDATION_ADMISSION | SUPPORT | - |
| `run_matrix_comparative_preflight` | 675-751 | FOUNDATION_ADMISSION | SUPPORT | - |
| `build_service_failure_adaptive_cohort_contract` | 754-959 | FOUNDATION_ADMISSION | SUPPORT | - |
| `planner_movable_rows_with_selected_capacity` | 962-989 | FOUNDATION_ADMISSION | SUPPORT | - |
| `passive_event_provenance_classification` | 1016-1030 | FOUNDATION_ADMISSION | SUPPORT | - |
| `parse_kv_line` | 1033-1040 | FOUNDATION_ADMISSION | SUPPORT | - |
| `parse_registry` | 1043-1056 | FOUNDATION_ADMISSION | SUPPORT | R |
| `declared_target_egress_ip` | 1059-1126 | FOUNDATION_ADMISSION | SUPPORT | R |
| `read_flat_state` | 1132-1146 | FOUNDATION_ADMISSION | SUPPORT | R |
| `controlled_certification_source_health_status` | 1149-1302 | FOUNDATION_ADMISSION | SUPPORT | R |
| `controlled_certification_pool_status` | 1305-1532 | FOUNDATION_ADMISSION | SUPPORT | - |
| `to_float` | 1535-1541 | FOUNDATION_ADMISSION | SUPPORT | - |
| `to_int` | 1544-1550 | FOUNDATION_ADMISSION | SUPPORT | - |
| `bool_value` | 1553-1554 | FOUNDATION_ADMISSION | SUPPORT | - |
| `route_writer_failure_code` | 1557-1573 | FOUNDATION_ADMISSION | SUPPORT | - |
| `split_csv` | 1576-1579 | FOUNDATION_ADMISSION | SUPPORT | - |
| `normalize_service_ids` | 1582-1588 | FOUNDATION_ADMISSION | SUPPORT | - |
| `user_priority_services_from_pref` | 1591-1597 | FOUNDATION_ADMISSION | SUPPORT | - |
| `telegram_status_is_hard` | 1600-1602 | FOUNDATION_ADMISSION | SUPPORT | - |
| `merge_defaults` | 1605-1612 | FOUNDATION_ADMISSION | SUPPORT | - |
| `glob_contains` | 1615-1616 | FOUNDATION_ADMISSION | SUPPORT | - |
| `parse_ts` | 1619-1623 | FOUNDATION_ADMISSION | SUPPORT | W |
| `runtime_authority_contract_status` | 1626-1853 | FOUNDATION_ADMISSION | SUPPORT | - |
| `action_class_contract_source_generation` | 1856-1900 | FOUNDATION_ADMISSION | SUPPORT | - |
| `availability_first_action_class_context` | 1903-1954 | FOUNDATION_ADMISSION | SUPPORT | - |
| `action_class_contract_reconciliation_request` | 1957-2257 | FOUNDATION_ADMISSION | SUPPORT | - |
| `write_json_atomic` | 2260-2264 | FOUNDATION_ADMISSION | SUPPORT | W |
| `read_jsonl` | 2267-2300 | FOUNDATION_ADMISSION | SUPPORT | R |
| `read_jsonl_exact_schema` | 2303-2328 | FOUNDATION_ADMISSION | SUPPORT | R |
| `append_jsonl` | 2331-2337 | FOUNDATION_ADMISSION | SUPPORT | R |
| `acquire_service_matrix_lock` | 2340-2392 | FOUNDATION_ADMISSION | SUPPORT | R |
| `service_failure_causal_integrity_status` | 2395-2573 | FOUNDATION_ADMISSION | SUPPORT | R |
| `ct_m0f_active_service_failure_binding_projection` | 2576-2928 | FOUNDATION_ADMISSION | SUPPORT | WR |
| `ct_m0f_active_service_failure_binding_projection.current_accounted_scope` | 2632-2637 | FOUNDATION_ADMISSION | SUPPORT | - |
| `ct_m0f_active_service_failure_binding_projection.current_actionable_scope` | 2639-2670 | FOUNDATION_ADMISSION | SUPPORT | - |
| `ct_m0f_active_service_failure_binding_projection.matches_live_source_scope` | 2672-2679 | FOUNDATION_ADMISSION | SUPPORT | - |
| `ct_m0f_active_service_failure_binding_projection.semantic_key` | 2746-2751 | FOUNDATION_ADMISSION | SUPPORT | - |
| `effective_pre_planner_refresh_mode` | 2991-2999 | FOUNDATION_ADMISSION | SUPPORT | - |
| `controlled_campaign_execution_target_admission` | 3002-3101 | FOUNDATION_ADMISSION | SUPPORT | - |
| `__init__` | 3105-3220 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_record_performance_span` | 3222-3248 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `performance_timeline` | 3250-3256 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_exact_controlled_verifier_scope` | 3258-3334 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_exact_availability_first_controlled_scope` | 3336-3645 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_exact_ct_m0f_standing_reset_scope` | 3647-3742 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_activate_controlled_verifier_contention` | 3744-3854 | L3_AUTHORITY_RECONCILIATION | SUPPORT | WPR |
| `_execution_action_class` | 3856-3866 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `bind_routing_core_certification` | 3868-4007 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_execution_control_decision` | 4009-4033 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_switch_policy` | 4035-4040 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_authority_budget_policy` | 4042-4143 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_emergency_failover_policy` | 4145-4181 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_load_l3_runtime_state` | 4183-4195 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_write_l3_runtime_state` | 4197-4203 | L3_AUTHORITY_RECONCILIATION | SUPPORT | W |
| `_bounded_cohort_checkpoint` | 4205-4303 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `reconcile_bounded_cohort_closure_obligations` | 4305-4381 | L3_AUTHORITY_RECONCILIATION | SUPPORT | WR |
| `_passive_incident_projection_key` | 4383-4393 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_materialize_passive_incident_projection` | 4395-4719 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `reconcile_passive_causal_projections` | 4721-4786 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_effective_service_failure_causal_binding` | 4788-4827 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_reconcile_incident_scope_accounting` | 4829-5286 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_reconcile_incident_cumulative_scope` | 5288-5418 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_reconcile_recovered_service_failure_intents` | 5420-5655 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `reconcile_service_failure_execution_outcomes` | 5657-5984 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `reconcile_service_failure_execution_outcomes.record_passive_reconciliation_span` | 5667-5669 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_incident_attempt_count` | 5986-5993 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_attempt_consumed_retry_budget` | 5996-6011 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_semantic_attempt_signature` | 6014-6030 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_consumed_retry_attempts` | 6032-6048 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_retry_budget_exhausted_for_move` | 6050-6085 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_enabled_users_on_source` | 6087-6093 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_required_service_failures_for_source` | 6095-6130 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_failed_source_scope` | 6132-6169 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_active_incident_source_context` | 6171-6273 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_failed_source_cooldown_override_context` | 6275-6341 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_external_wake_events` | 6343-6385 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_authority_promotion_truth_check` | 6387-6428 | L3_AUTHORITY_RECONCILIATION | SUPPORT | P |
| `_authority_promotion_runtime_fingerprint_check` | 6430-6459 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_emergency_failover_authority_gate` | 6461-6849 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_approved_l3_production_validation_envelope` | 6851-6954 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_emergency_failover_move_evidence` | 6956-7042 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_state_file_freshness` | 7044-7065 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_file_freshness` | 7067-7087 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_controlled_certification_failure_context` | 7089-7136 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_current_channel_failure_evidence` | 7138-7175 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_normalized_wake_source` | 7177-7192 | L3_AUTHORITY_RECONCILIATION | SUPPORT | W |
| `_l3_wake_decision` | 7194-7320 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_incident_key` | 7322-7334 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_behavior_contracts` | 7336-7527 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_behavior_contracts.row` | 7356-7379 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_operator_surface` | 7529-7549 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_production_validation_ladder` | 7551-7584 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_certification_pipeline` | 7586-7614 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_runtime_incident_record` | 7616-7692 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_l3_incident_context` | 7694-7834 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_authority_promotion_feedback_paths` | 7836-7846 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_authority_feedback_records_for_operation` | 7848-7871 | L3_AUTHORITY_RECONCILIATION | SUPPORT | R |
| `_authority_promotion_stability_window_seconds` | 7873-7900 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_pool_equivalence_distribution_review` | 7902-7930 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_pool_equivalence_planner_review` | 7932-7955 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_pool_authority_equivalence_review` | 7957-8030 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `_authority_promotion_evidence_review` | 8032-8136 | L3_AUTHORITY_RECONCILIATION | SUPPORT | - |
| `promote_authority` | 8138-8321 | L3_AUTHORITY_RECONCILIATION | SUPPORT | WR |
| `_quality_policy` | 8323-8326 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_policy` | 8328-8331 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_reconnect_policy` | 8333-8336 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_safety_policy` | 8338-8341 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_signal_policy` | 8343-8346 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_quality_policy` | 8348-8351 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_best_available_pool_policy` | 8353-8356 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_restore_barrier_status` | 8358-8455 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_generation_status` | 8457-8480 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_intelligence_snapshots` | 8482-8558 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_run_pre_planner_refresh` | 8560-8795 | POLICY_HEALTH_CAPACITY | SUPPORT | P |
| `_reload_intelligence_sources_after_pre_planner_refresh` | 8797-8832 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_retry_pre_planner_refresh_after_source_reload` | 8834-8905 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_intelligence_snapshot_source_mismatches` | 8907-8925 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_intelligence_snapshot_gate` | 8927-8949 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_apply_source_bundle_lease_to_intelligence_gate` | 8951-9073 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_apply_source_bundle_lease_to_intelligence_gate.allow_non_material_source_mismatch` | 8959-8974 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_apply_source_bundle_lease_to_intelligence_gate.can_allow_non_material_source_mismatch` | 8976-8982 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_approved_plan_lock_snapshot_gate_materiality` | 9075-9139 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_safety` | 9141-9148 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_compact_safety` | 9150-9189 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_active_users` | 9191-9192 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_quality_ok_for_load` | 9194-9215 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_healthy_for_load` | 9217-9232 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_dynamic_load_summary` | 9234-9294 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_capacity_status` | 9296-9307 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_persist_dynamic_load_summary` | 9309-9330 | POLICY_HEALTH_CAPACITY | SUPPORT | W |
| `_load_limits_for_egress` | 9332-9405 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_users` | 9407-9436 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_runtime_registry_users` | 9438-9462 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_operational_egress_states` | 9464-9483 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_org_user_map` | 9485-9493 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_egress` | 9495-9537 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_sync_egress_user_counts` | 9539-9545 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_load_reconnect_state` | 9547-9554 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_activity_epoch_for_user` | 9556-9560 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_observe_reconnect_events` | 9562-9631 | POLICY_HEALTH_CAPACITY | SUPPORT | W |
| `_client_mbps_for_egress` | 9633-9640 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_last_switches` | 9642-9663 | POLICY_HEALTH_CAPACITY | SUPPORT | WR |
| `_group_usage` | 9665-9670 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_group_policy` | 9672-9673 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_required_services` | 9675-9686 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_important_services` | 9688-9695 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_matrix_services` | 9697-9698 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_route_class_fitness` | 9700-9701 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_severity_classification` | 9703-9740 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_quality_history` | 9742-9743 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_quality_window` | 9745-9746 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_explicit_required_services` | 9748-9758 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_metric_latency` | 9760-9761 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_row_ts` | 9763-9768 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_truth_freshness` | 9770-9798 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_probe_methodology_issue` | 9800-9812 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_truth_classification` | 9814-9934 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_suitability_for_row` | 9936-9996 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_service_suitability` | 9998-10045 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_attach_service_revalidation_command` | 10047-10073 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_user_safety` | 10075-10076 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_egress_safety` | 10078-10079 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_user_frozen` | 10081-10090 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_blocked_target_for_user` | 10092-10094 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_pair_reversal_blocked_for_user` | 10096-10107 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_safety_summary` | 10109-10119 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_lifecycle_model` | 10121-10133 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_bridge_model` | 10135-10166 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_certification_rules` | 10168-10209 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_governance_policy` | 10211-10262 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_full_action_matrix` | 10264-10346 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_action_matrix` | 10348-10359 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_action_class_execution_boundary` | 10361-10419 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_authority_budget_gate` | 10421-10561 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_recent_audit_records` | 10563-10580 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_snapshot_items` | 10582-10596 | POLICY_HEALTH_CAPACITY | SUPPORT | R |
| `_snapshot_channel_score_map` | 10598-10604 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_snapshot_channel_trust_recovery_map` | 10606-10616 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_soft_adjustment_for_state` | 10618-10626 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_recommended_action_for_state` | 10628-10636 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_blocked_actions_for_state` | 10638-10650 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_advisory_for_egress` | 10652-10722 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_snapshot_user_candidate_suitability_map` | 10724-10736 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_first_snapshot_item` | 10738-10740 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_snapshot_candidate_advisory_scores` | 10742-10846 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_routing_intelligence_scores_for_user` | 10848-10886 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_routing_intelligence_candidate_advice` | 10888-10913 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_snapshot_routing_brain_advisory` | 10915-11065 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_routing_brain_advisory` | 11067-11131 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_candidate_shadow_row` | 11133-11151 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_quality_delta` | 11153-11189 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_service_aware_delta` | 11191-11207 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `_ctr_shadow_comparison` | 11209-11343 | POLICY_HEALTH_CAPACITY | SUPPORT | - |
| `plan` | 11345-11815 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | R |
| `_operation_context` | 11817-11829 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_merge_locked_moves_with_live_decisions` | 11831-11868 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_runtime_snapshot_hash` | 11870-11875 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_committed_apply_identity_validation` | 11877-11959 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_approved_plan_lock_validation` | 11961-12115 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_committed_selected_moves_from_approved_plan_lock` | 12117-12176 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_runtime_source_hashes` | 12178-12188 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | R |
| `_operation_scoped_source_binding` | 12190-12251 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_snapshot_source_bundle` | 12253-12265 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_atomicity_state` | 12267-12336 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_atomic_execution_envelope` | 12338-12395 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_validate_atomic_execution_envelope` | 12397-12486 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_source_bundle_stability_lease_validation` | 12488-12609 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_l3_execution_eligibility` | 12611-12769 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_selected_moves_hash` | 12771-12781 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `generate_rollback_packet_from_result` | 12783-12859 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `write_rollback_packet_from_result` | 12861-12867 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | WR |
| `_validate_rollback_packet` | 12869-12908 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `execute_rollback_packet` | 12910-13025 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | RM |
| `_restore_clearance_generation_check` | 13027-13246 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_restore_barrier_source_bundle_lease` | 13248-13290 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_source_bundle_lease_scope` | 13292-13362 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_org_isolation_summary` | 13364-13372 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_decision_for_user` | 13374-13493 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_ctr_simulated_score` | 13495-13497 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_attach_ctr_score_simulation` | 13499-13553 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_best_alternative` | 13555-13568 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_stable_pair_rank` | 13570-13572 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_score_without_sticky` | 13574-13579 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_capacity_decision` | 13581-13610 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_mark_best_available_pool` | 13612-13643 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_rebalance_needed` | 13645-13657 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_route_class_for_services` | 13659-13666 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_candidate` | 13668-13686 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_block` | 13688-13690 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_basic` | 13692-13720 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_reservation` | 13722-13738 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_load` | 13740-13748 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_safety` | 13750-13762 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_org` | 13764-13784 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_quality` | 13786-13842 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_telegram_sentinel_row` | 13844-13845 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_telegram_candidate_state` | 13847-13874 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_service` | 13876-13937 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_service_failure_count` | 13939-13946 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_service_failure_persistent` | 13948-13952 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_gate_service_failures` | 13954-13981 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_service_signal_only_block` | 13983-13992 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_score_parts` | 13994-14050 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_service_scores` | 14052-14084 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_cooldown_ok` | 14086-14094 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_beats_current` | 14096-14099 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_explanation` | 14101-14175 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_candidate_json` | 14177-14216 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_select_moves` | 14218-14268 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_pick_projected_moves` | 14270-14331 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `_projected_target_for_move` | 14333-14370 | PLAN_APPLY_CLOSURE_VERIFY | SUPPORT | - |
| `apply` | 14372-14877 | PLAN_APPLY_CLOSURE_VERIFY | A_HOT_GOVERNED_EXECUTION | M |
| `finalize_operation` | 14879-14922 | PLAN_APPLY_CLOSURE_VERIFY | A_HOT_GOVERNED_EXECUTION | - |
| `finalize_operation.record_finalization_span` | 14885-14893 | PLAN_APPLY_CLOSURE_VERIFY | A_HOT_GOVERNED_EXECUTION | - |
| `_consume_passive_production_events` | 14924-15368 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | WR |
| `_consume_passive_production_events.record_passive_substep` | 14936-14938 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_consume_passive_production_events.consumed_event_requires_scope_repair` | 15008-15041 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_consume_passive_production_events.event_order` | 15101-15108 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_service_failure_automation_obligation_id` | 15371-15378 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_service_failure_stop_safe_classification` | 15381-15417 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_standing_delegated_policy_status` | 15419-15456 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `reconcile_service_failure_shadow_outcomes` | 15458-15508 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | WR |
| `materialize_service_failure_automation_advisory` | 15510-16197 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | WR |
| `materialize_service_failure_automation_advisory.record_advisory_span` | 15525-15533 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `materialize_service_failure_automation_advisory.obligation_semantic_projection` | 16014-16048 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_l3_materialize_learning_closure` | 16199-16360 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | W |
| `_l3_execution_closure_verification` | 16362-16574 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_l3_execution_closure_verification.status` | 16381-16382 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_l3_execution_closure_verification.row` | 16384-16415 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_l3_close_incident_and_update_capability` | 16576-16702 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | WR |
| `_terminal_verdict` | 16704-16727 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_dry_run_terminal_reason` | 16729-16751 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_rollback_verdict` | 16753-16766 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_restore_barrier_status_label` | 16768-16778 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_terminal_audit_reference` | 16780-16807 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_rollback_audit_reference` | 16809-16840 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_emit_terminal_audit` | 16842-16866 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | P |
| `_closure_target` | 16868-16876 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_future_iso` | 16878-16879 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_update_safety_after_apply` | 16881-16956 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | W |
| `_run_switch` | 16958-16993 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | PM |
| `_verify_routes` | 16995-17005 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | P |
| `_verify_routes_for_apply` | 17007-17013 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | - |
| `_verify_user_route` | 17015-17118 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | PR |
| `_verify_emergency_required_services` | 17120-17154 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | P |
| `_reuse_or_verify_emergency_required_services` | 17156-17243 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | PR |
| `_ct_m0f_kernel_cutover_evidence` | 17245-17550 | PLAN_APPLY_CLOSURE_VERIFY | B_NONBLOCKING_OR_TERMINAL | P |
| `build_arg_parser` | 17553-17832 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `consume_passive_events_only` | 17835-17933 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `consume_passive_events_only.record_passive_span` | 17895-17902 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `consume_service_failure_automation_only` | 17936-18029 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `reconcile_passive_causal_projections_only` | 18032-18074 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `classify_shared_target_availability` | 18077-18173 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `shared_target_stage_allocations` | 18176-18300 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `availability_first_target_growth_trial_projection` | 18303-18430 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `shared_target_semantic_fingerprint` | 18433-18452 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `availability_first_standing_policy_semantic_coverage_gate` | 18455-18615 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `controlled_campaign_target_selection_diagnostic` | 18618-19732 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `_controlled_source_reservation_owner_capability` | 19735-19776 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `_controlled_source_draft_candidates` | 19779-19870 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `_controlled_source_key_value_output` | 19873-19882 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `consume_approved_controlled_source_topology` | 19885-20154 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | PR |
| `reconcile_released_controlled_source_topology` | 20157-20193 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `controlled_source_topology_diagnostic` | 20196-22482 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `controlled_source_topology_authority_request_only` | 22485-22681 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `standing_delegated_policy_status_only` | 22684-23060 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `controlled_certification_substrate_authority_request_only` | 23063-23283 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `ct_m0f_controlled_validation_authority_request_only` | 23286-23410 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `action_class_contract_reconciliation_only` | 23413-23557 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `routing_core_certification_authority_request_only` | 23560-23653 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | - |
| `_routing_core_scoped_route_verify` | 23656-23685 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | P |
| `routing_core_certification_execute_only` | 23688-23846 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | WPR |
| `ct_m0f_standing_source_selection_only` | 23849-24433 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | R |
| `main` | 24436-24647 | CLI_CONTROLLED_ENGINEERING | C_ENGINEERING_OR_D | M |

## CLASSIFICATION, DUPLICATES, LEGACY

| Class | Paths | Result |
| --- | --- | --- |
| A: real Runtime hot path | `plan`, `apply`, lock validation, execution control, `_run_switch`, route/service verification | Safety-critical; direct systemd service is dry-run with max-users 0, while direct apply remains explicitly gated. |
| B: Runtime but non-blocking | passive consumption, L3 reconciliation, outcome/closure/advisory materialisation, performance spans | Must stay outside automatic ordinary switching critical path. |
| C: Engineering/reporting/controlled | source topology, campaign diagnostics, authority-request-only, Polygon/CT-M0F helpers | Not ordinary Runtime hot path. |
| D: test only | test/fixture imports and scenarios | A consumer exists, but not production invocation proof. |
| E: legacy compatibility | broad policy/load/scoring and per-member guarded writer flow | Keep until migration/residue proof. |
| F: unused/dead | none asserted | Every candidate remains `UNKNOWN_REQUIRES_OWNER_EVIDENCE`. |

Findings:

1. **Health interpretation overlap:** Matrix is the canonical writer, but
   autoswitch repeats freshness, suitability, quality, stability, capacity and
   target interpretation. This is the primary future boundary question.
2. **L3/history and movement coexist:** passive event, closure, learning and
   advisory materialisation sit alongside apply/verify. V5.3 requires these not
   to become synchronous FAST prerequisites.
3. **Controlled engineering surface is embedded:** topology diagnostics
   (2,287 LOC), campaign diagnostic (1,115 LOC) and authority-request CLI
   surfaces are not ordinary switch core. They are future separation candidates,
   not deletion candidates.
4. **Per-member apply is safety-critical:** `apply` is 506 LOC and couples
   writer, verification, rollback and circuit breaker. No mechanical cleanup.
5. **No dead-code conclusion:** systemd/subprocess/Admin/dynamic CLI references
   make static non-reference insufficient evidence.

## COMPLEXITY FINDINGS

| Metric | Finding | Consequence |
| --- | --- | --- |
| LOC | 24,651 | One file exceeds a clean single responsibility. |
| Functions | 327 | Requires semantic clusters, never size-based deletion. |
| Largest functions | topology diagnostic 2,287 LOC; campaign diagnostic 1,115; advisory 688; apply 506; plan 471 | High mixed-responsibility risk. |
| Branches | apply 54; diagnostics 46/32; plan 31 | Bounded change only. |
| Static I/O | 19 W-flag functions; 13 P-flag functions; multiple M paths | File cannot be classified engineering-only. |
| Dependencies | Matrix/tester, user-switch, ip route, execution control, operator execution, registry/policy/JSONL | Consumer migration and lifecycle proof mandatory. |

## ARCHITECTURE COMPATIBILITY

| Candidate | What remains | Autoswitch must not do | Compatibility |
| --- | --- | --- | --- |
| MODEL_A full Matrix | Consume full Matrix/event and fallback | own second health truth | Compatible, but slow economics remain |
| MODEL_B FAST+DEEP under Matrix owner | consume exact source/target facts and unchanged Matrix schema | become FAST detector/scheduler/writer | Compatible only as thin Matrix consumer |
| MODEL_C passive escalation | receive Matrix-confirmed event/scope | treat raw passive signal as movement authority | Compatible only merged into B+C |
| ROLE_AWARE_POLICY | apply existing role facts in decision | persist second role registry or select architecture | Evaluation dimension only |

## RECOMMENDED FUTURE ROLE

After existing V5.3 completion and a separately admitted Mission, the intended
role is a thin governed migration coordinator:

```text
canonical Matrix/current scope + existing eligibility/Authority
  -> bounded Candidate/Packet/lease/barrier consumption
  -> one existing writer
  -> route/service verification
  -> minimal terminal
```

This is a design recommendation, not a change authorisation. The first change
must be one existing-owner semantic cluster with known consumers and rollback;
not a broad file split, replacement Planner or deletion campaign.

## SAFE CLEANUP OPPORTUNITIES / BLOCKERS

| Item | Status | Required proof |
| --- | --- | --- |
| Separate controlled diagnostics from ordinary path | FUTURE_REVIEW | dynamic CLI caller map, Engineering owner, import/residue and rollback |
| Keep L3/history/advisory out of synchronous action | partially separated; FUTURE_REVIEW | fresh T0-T11 receipt proving no consumer loss |
| Reduce health interpretation overlap | NEEDS_OWNER_BOUNDARY_DECISION | Phase-E/V5.3 decision consumption and equivalence contract |
| Remove any function/flag | NOT_ADMITTED | exact CLI/systemd/Admin/test/dynamic consumer proof |
| Replace per-member writer | NOT_ADMITTED | Product Contract plus Packet/lease/barrier/rollback/verify migration proof |

## RISKS

- Broad refactor can orphan L3/closure/controlled Runtime consumers.
- Removing health-reading gates can weaken freshness/capacity/anti-flap although
  Matrix remains writer.
- Moving Packet/lease/barrier by LOC is a safety and Authority regression.
- Enabling FAST via autoswitch-local caller violates the current V5.3 hold.
- Static analysis cannot prove absence of dynamic consumers.

## NO CODE CHANGES PERFORMED

- Source files changed: 0
- Functions removed/moved/refactored: 0
- Runtime/Matrix/Planner/CPS changes: 0
- Routes/users/Packets/leases/barriers changed: 0
- Production/Authority effect: `NONE`

## EXACT NEXT STEP

Return to existing CPS/V5.3 action:
`EXECUTE_V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS`. This audit may be
reused only if an owner-backed bounded Mission selects one responsibility
cluster. It does not authorise autoswitch cleanup, FAST enablement, or any code
change.

