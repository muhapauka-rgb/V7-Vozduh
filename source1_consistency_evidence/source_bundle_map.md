# SOURCE_BUNDLE_MAP

Program: PROGRAM_SOURCE1_SNAPSHOT_SOURCE_CONSISTENCY_CLOSURE_AND_OPERATOR_VISIBLE_UNLOCK
Date: 2026-06-05

## service-scores

- Source Bundle: service_matrix, quality_summary, service_preferences
- Generation: tools/v7-intelligence-snapshot-refresh -> admin_core.intelligence_workers.build_service_scores_snapshot
- Hash: source_hashes.service_matrix, source_hashes.quality_summary, source_hashes.service_preferences
- Build Time: refresh build
- Validation Time: planner snapshot gate after source reload
- Acceptance Rules: FRESH/ALLOW, confidence above family floor, hash match for required sources

## channel-service-scores

- Source Bundle: service_matrix, quality_summary, service_preferences
- Generation: tools/v7-intelligence-snapshot-refresh -> admin_core.intelligence_workers.build_channel_service_scores_snapshot
- Hash: source_hashes.service_matrix, source_hashes.quality_summary, source_hashes.service_preferences
- Build Time: refresh build
- Validation Time: planner snapshot gate after source reload
- Acceptance Rules: FRESH/ALLOW, confidence above family floor, hash match for required sources

## candidate-suitability-summary

- Source Bundle: service_matrix, quality_summary, service_preferences, risk_summary, trust_summary, blast_radius, users_registry, egress_registry
- Generation: admin_core.intelligence_workers.build_candidate_suitability_snapshot
- Hash: source_hashes in snapshot envelope
- Build Time: refresh build
- Validation Time: snapshot reader validation; runtime-required source hash comparison is not assigned to this advisory family
- Acceptance Rules: advisory family may be ignored when stale; must not override planner hard gates

## prediction-summaries

- Source Bundle: service_matrix, quality_summary, risk_summary, trust_summary, blast_radius
- Generation: admin_core.intelligence_workers.build_prediction_summary_snapshot
- Hash: source_hashes in snapshot envelope
- Build Time: refresh build
- Validation Time: snapshot reader validation
- Acceptance Rules: advisory only; no runtime forecasting performed by planner

## trust-evolution-summaries

- Source Bundle: service scores, channel service scores, candidate suitability, prediction actuals, service actuals, decisions, rollback records, trust summary, blast radius
- Generation: admin_core.intelligence_workers.build_trust_evolution_snapshot
- Hash: source_hashes in snapshot envelope
- Build Time: refresh build
- Validation Time: snapshot reader validation
- Acceptance Rules: advisory only; no runtime trust training performed by planner

## Decision -> Action

Condition: required family source bundle matches current post-refresh source input.
Decision: snapshot may be trusted by planner gate.
Action: allow snapshot-backed advisory context.
Executor: tools/v7-users-autoswitch.
Trigger: snapshot gate validation.
Written Evidence: plan.safety.intelligence_snapshots.results.
Blocked Actions: none.
Next State: planner_advisory_context_available.

