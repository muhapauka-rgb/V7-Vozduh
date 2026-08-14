# PROGRAM DATA LINEAGE REALITY AUDIT AND OUTCOME INTEGRATION MAP REPORT

Project: V7 Vozduh
Workspace: /Users/ponch/Documents/New project
Branch: Updatesystem
Date: 2026-06-04

## Executive Verdict

V7 does not have a total absence of outcome data. Production contains substantial runtime, switch, audit, service, and channel history. The current problem is a lineage and consumption break:

- direct outcome-like production data exists in `switch-history.jsonl`, `audit.jsonl`, `operator-execution-audit.jsonl`, and governance audit files;
- service and channel history exists in service matrix refresh events, Telegram sentinel events, quality summary/ring/history, and service matrix state;
- the RI6 trust evolution model can accept prediction actuals, service actuals, and candidate outcomes;
- the current snapshot worker passes empty lists for `prediction_actuals`, `service_actuals`, and `candidate_outcomes`;
- production currently stores only 6 intelligence snapshot files, while the refresh CLI dry-run can build 11 snapshot families;
- closure and execution event files exist but are empty, so they cannot currently serve as populated canonical outcome stores.

Conclusion: outcome data exists, but the intelligence platform does not yet consume enough of it correctly as calibrated live outcomes.

## Scope And Safety

This was a read-first reality audit. No autonomy was enabled. No users were moved. No autoswitch apply was run. No routing, planner, governance, execution, rollback, service, systemd, timer, or runtime state mutation was performed.

The only production command that executed platform code was:

`/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run`

It reported `runtime_behavior_changed=false`, `governance_behavior_changed=false`, `users_moved=false`, and `written={}`.

## GLOBAL_DATA_SOURCE_MAP

| Domain | Existing Source | Runtime Path | Current Use | Lineage Verdict |
| --- | --- | --- | --- | --- |
| Service matrix | service matrix state | `/opt/v7/egress/state/service-matrix.json` | read by intelligence workers and routing intelligence | EXISTS_CONSUMED |
| Service refresh history | service matrix refresh events | `/opt/v7/events/service-matrix-refresh-*.jsonl` | historical probe evidence | EXISTS_PARTIALLY_CONSUMED |
| Telegram/channel telemetry | sentinel state and events | `/opt/v7/egress/state/telegram-sentinel.json`, `/opt/v7/events/telegram-sentinel-*.jsonl` | service/channel reality input | EXISTS_PARTIALLY_CONSUMED |
| Egress quality | summary, ring, history | `/opt/v7/egress/state/egress-quality-summary.json`, `egress-quality-ring.json`, `egress-history.jsonl` | scoring input | EXISTS_CONSUMED |
| Runtime state | runtime state | `/opt/v7/egress/state/v7-state.json` | snapshot and planner input | EXISTS_CONSUMED |
| Users registry | user registry | `/opt/v7/egress/state/users.registry` | candidate/user scoring input | EXISTS_CONSUMED |
| Egress registry | channel registry | `/opt/v7/egress/state/egress.registry` | channel/candidate scoring input | EXISTS_CONSUMED |
| Switch outcomes | switch history | `/opt/v7/events/switch-history.jsonl` | read by snapshot refresh and trust workers | EXISTS_PARTIALLY_CONSUMED |
| Runtime audit | audit log | `/opt/v7/audit/audit.jsonl` | available and partly read when passed as audit log | EXISTS_PARTIALLY_CONSUMED |
| Operator execution audit | execution audit | `/opt/v7/audit/operator-execution-audit.jsonl` | outcome evidence, not default refresh input | EXISTS_NOT_DEFAULT_CONSUMED |
| Governance actions | governance actions audit | `/opt/v7/audit/operator-runtime-governance-actions.jsonl` | governance outcome evidence | EXISTS_NOT_DEFAULT_CONSUMED |
| Closure records | closure JSONL | `/opt/v7/egress/state/closure-records.jsonl` | intended closure store | FILE_EXISTS_EMPTY |
| Execution events | execution events JSONL | `/opt/v7/egress/state/execution-events.jsonl` | intended execution event store | FILE_EXISTS_EMPTY |
| Intelligence snapshots | snapshot root | `/opt/v7/egress/state/intelligence/` | runtime fast path and advisory reads | PARTIAL_ON_PRODUCTION |

## PHYSICAL_STORAGE_MAP

Production direct outcome/audit counts observed read-only:

| Path | Exists | Lines | Bytes |
| --- | --- | ---: | ---: |
| `/opt/v7/events/switch-history.jsonl` | true | 2792 | 517129 |
| `/opt/v7/audit/audit.jsonl` | true | 4140 | 1840159 |
| `/opt/v7/audit/operator-execution-audit.jsonl` | true | 16 | 12871 |
| `/opt/v7/audit/operator-runtime-governance-actions.jsonl` | true | 1 | 1392 |
| `/opt/v7/egress/state/closure-records.jsonl` | true | 0 | 0 |
| `/opt/v7/egress/state/execution-events.jsonl` | true | 0 | 0 |
| `/opt/v7/egress/state/egress-history.jsonl` | true | 120 | 54478 |

Additional history exists:

- service matrix refresh JSONL events from 2026-05-20 through 2026-06-04, 1363 total observed lines;
- Telegram sentinel JSONL events from 2026-05-20 through 2026-06-04, 121468 total observed lines;
- `egress-quality-ring.json` and `egress-quality-summary.json` are populated and current.

## WRITER_OWNERSHIP_MAP

| Artifact | Writer Owner | Classification |
| --- | --- | --- |
| `service-matrix.json` | service matrix refresh/probe tooling | REUSE |
| `service-matrix-refresh-*.jsonl` | `tools/v7-service-matrix-refresh-all` | REUSE |
| `telegram-sentinel.json` and daily sentinel JSONL | `tools/v7-telegram-sentinel` | REUSE |
| `egress-quality-summary.json`, `egress-quality-ring.json` | `tools/v7-egress-quality-compact` | REUSE |
| `switch-history.jsonl` | runtime switch log support and autoswitch flow | REUSE |
| `audit.jsonl` | runtime audit support | REUSE |
| `operator-execution-audit.jsonl` | `admin_core/operator_execution.py` | REUSE |
| governance action audit | operator/runtime governance modules | REUSE |
| `closure-records.jsonl` | intended closure flow | EXTEND, currently empty |
| `execution-events.jsonl` | intended execution event flow | EXTEND, currently empty |
| intelligence snapshots | `admin_core/intelligence_workers.py` through `tools/v7-intelligence-snapshot-refresh` | EXTEND |

No new writer ownership should be created. Existing writers should be reused and normalized into existing RI6 inputs.

## READER_OWNERSHIP_MAP

| Reader | Reads | Current State |
| --- | --- | --- |
| `tools/v7-intelligence-snapshot-refresh` | state, registry, switch history, optional audit logs, rollback history | read-only snapshot builder exists |
| `admin_core/intelligence_workers.py` | service, channel, trust, candidate, prediction, audit/switch/rollback inputs | builds 11 snapshots locally/dry-run |
| `admin_core/intelligence_platform.py` | model inputs passed by workers | RI6 model supports live outcomes |
| `tools/v7-users-autoswitch` | runtime fast-path snapshot families | reads required families and stops on stale/invalid |
| routing intelligence modules | service matrix, quality summary, service preferences, audit records | advisory-only consumption |

Reader gap: default production refresh reads `switch-history.jsonl` as audit input but does not default-read `/opt/v7/audit/audit.jsonl` or `operator-execution-audit.jsonl`.

## SERVICE_LINEAGE_MAP

Service lineage exists and is broadly usable:

`service probes -> service-matrix.json -> egress-quality-summary/ring/history -> intelligence_workers -> service-scores/channel-service-scores/user-service-scores/prediction-summaries`

Breaks:

- production snapshot root currently lacks `user-service-scores.json` and `prediction-summaries.json`;
- `service_actuals` are passed as an empty list into RI6 trust evolution, so forecast-vs-live calibration is not yet connected.

## CHANNEL_LINEAGE_MAP

Channel lineage exists:

`egress.registry + service-matrix.json + egress-quality-summary.json + telegram-sentinel.json -> channel-service-scores -> candidate suitability/best available pool`

Breaks:

- production snapshot root currently lacks `candidate-suitability-summary.json` and `best-available-pool.json`;
- candidate outcomes are not derived from switch/audit history and are passed empty to RI6 trust evolution.

## EXECUTION_LINEAGE_MAP

Execution evidence exists, but not in one clean populated outcome stream:

- `switch-history.jsonl`: 2792 records, 40 rollback term hits;
- `audit.jsonl`: 4140 records, 38 selected_move hits, 17 terminal_state hits, 15 applied hits;
- `operator-execution-audit.jsonl`: 16 records, 5 selected_move hits;
- governance actions: 1 record;
- `execution-events.jsonl`: exists but 0 records.

The closest existing execution outcome chain is:

`planner/autoswitch/operator execution -> audit/switch history/governance audit -> snapshot refresh read_jsonl_tail -> trust summary and trust evolution`

Break: intended normalized `execution-events.jsonl` is empty and RI6 actual outcome inputs are not populated from the available logs.

## OUTCOME_REALITY_REPORT

Outcome data exists. Direct outcome/audit record count observed:

`2792 + 4140 + 16 + 1 + 0 + 0 = 6949`

This count excludes service refresh history, Telegram sentinel history, and egress history. Including `egress-history.jsonl` adds 120 operational history rows.

Important term counts:

| Source | rollback | apply | applied | selected_move | terminal_state | failed/error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| switch-history | 40 | 0 | 0 | 0 | 0 | 0 |
| audit.jsonl | 127 | 3057 | 15 | 38 | 17 | 31 failed, 50 error |
| operator-execution-audit | 3 | 12 | 0 | 5 | 0 | 8 error |
| governance actions | 1 | 1 | 0 | 3 | 0 | 0 |

Therefore, the correct answer is not "no outcome data". The correct answer is "outcome data exists but is not yet normalized and consumed enough by RI6 live calibration."

## OUTCOME_CONSUMPTION_MAP

`admin_core/intelligence_platform.py` exposes RI6 outcome-aware models:

- `decision_outcome_framework(records)`
- `prediction_accuracy_model(forecasts, actuals)`
- `suitability_trust_model(candidate_rows, outcomes)`
- `rollback_intelligence_model(records)`
- `trust_evolution_summary(...)`

`admin_core/intelligence_workers.py` currently calls:

- `decision_records=bounded_decisions`
- `prediction_forecasts=_prediction_forecast_rows(prediction_summary_snapshot)`
- `prediction_actuals=[]`
- `service_rows=service_rows`
- `service_actuals=[]`
- `candidate_rows=candidate_suitability_snapshot.get("items") or []`
- `candidate_outcomes=[]`
- `rollback_records=rollback_records or []`

This is the central consumption break.

## OUTCOME_GAP_REPORT

| Gap | Evidence | Risk | Safe Closure |
| --- | --- | --- | --- |
| RI6 prediction actuals empty | worker passes `prediction_actuals=[]` | predictions remain uncalibrated | map existing service/channel outcomes into model actuals |
| RI6 service actuals empty | worker passes `service_actuals=[]` | service trust lacks observed actual feedback | derive actual rows from quality/service history without new stores |
| RI6 candidate outcomes empty | worker passes `candidate_outcomes=[]` | suitability sees zero live outcomes | derive candidate outcome rows from switch/audit selected_move data |
| production full advisory snapshots absent | only 6 of 11 files present | RI4/RI5/RI6 advisory views absent at runtime | run approved snapshot refresh write after mapper design |
| `closure-records.jsonl` empty | file exists, 0 lines | closure truth unavailable in intended store | wire existing closure writer or document that audit is canonical |
| `execution-events.jsonl` empty | file exists, 0 lines | execution truth unavailable in intended store | wire existing execution event writer or document that audit is canonical |
| default refresh ignores audit logs | default `audit_paths` only includes switch history | audit outcomes under-consumed | pass approved audit log paths or extend default reader list |

## SNAPSHOT_LINEAGE_MAP

Expected intelligence snapshot families from code:

- `service-scores`
- `channel-service-scores`
- `user-service-scores`
- `risk-summaries`
- `trust-summaries`
- `blast-radius-summaries`
- `candidate-suitability-summary`
- `best-available-pool`
- `prediction-summaries`
- `trust-evolution-summaries`
- `overview-summary`

Production currently stores 6:

- `service-scores.json`
- `channel-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `overview-summary.json`

Production currently misses 5:

- `user-service-scores.json`
- `candidate-suitability-summary.json`
- `best-available-pool.json`
- `prediction-summaries.json`
- `trust-evolution-summaries.json`

Dry-run refresh result:

- `snapshot_count=11`
- `total_snapshot_bytes=546263`
- `runtime_behavior_changed=false`
- `governance_behavior_changed=false`
- `users_moved=false`
- `written={}`
- `warnings=[]`

So the builder can generate the complete set. The production root is partial because the complete write/refresh lifecycle is not currently reflected in stored files.

## RI6_OUTCOME_ROOT_CAUSE_REPORT

Root cause:

`RI6 outcomes_seen_zero` is caused by a combination of partial production snapshot materialization and missing actual-outcome mappers inside the existing worker flow.

More specifically:

1. Outcome evidence exists in production logs.
2. RI6 model functions support live outcomes.
3. The worker combines audit/switch/rollback records into `decision_records`, so decision and rollback foundation is partially connected.
4. The worker passes empty lists for `prediction_actuals`, `service_actuals`, and `candidate_outcomes`.
5. Production does not currently store `trust-evolution-summaries.json`, so RI6 output is not materialized in the production snapshot root.
6. Intended clean outcome stores `closure-records.jsonl` and `execution-events.jsonl` are present but empty.

Therefore the root cause is not missing data in general. It is missing normalization from existing audit/switch/service/channel histories into the existing RI6 actual-outcome inputs, plus incomplete production snapshot refresh materialization.

## INTELLIGENCE_LINEAGE_MAP

Current intended chain:

`service/channel/runtime/audit data -> intelligence_workers -> snapshot root -> runtime fast path/advisory readers -> operator-visible recommendations`

Actual current chain:

`service/channel/runtime/audit data -> intelligence_workers can build full set in dry-run -> production root contains only required fast-path subset -> RI6 actuals empty -> runtime stops on stale/mismatch when snapshots are expired or source hashes differ`

Required next chain:

`existing audit/switch/service/channel data -> read-only outcome mapper helpers -> RI6 actual inputs -> full snapshot refresh -> production snapshot root has all 11 families -> runtime truth check verifies freshness/hash -> advisory recommendations can use calibrated history`

## DATA_DUPLICATION_AUDIT

| Risk | Verdict | Notes |
| --- | --- | --- |
| Duplicate truth sources | NOT_CREATED | no new truth source was created |
| Duplicate outcome store | NOT_CREATED | existing stores were mapped only |
| Duplicate planner | NOT_CREATED | no planner change |
| Duplicate execution path | NOT_CREATED | no execution path change |
| Duplicate governance | NOT_CREATED | no governance change |
| Stale ownership | FOUND | production snapshot root is partial relative to current worker capability |
| Orphan ownership | FOUND | `closure-records.jsonl` and `execution-events.jsonl` exist but are empty |
| Under-consumed history | FOUND | audit/operator audit records are not default refresh inputs |

## DATA_LINEAGE_TEST_REPORT

Code-level tests were run after report creation:

`python3 -m unittest discover tests`

Result: PASS.

The production dry-run refresh also served as a read-only runtime lineage test:

`/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run`

Result: PASS, 11 snapshots buildable, no writes.

## Repair Decision

No code repair was performed in this audit. The lineage break is real, but the safe repair must be explicit:

- do not create a new truth source;
- do not create a duplicate outcome store;
- do not invent live outcome semantics without tests;
- implement pure mapper helpers inside the existing `admin_core/intelligence_workers.py` / `admin_core/intelligence_platform.py` boundary;
- keep runtime behavior read-only and advisory until calibrated outcomes are proven.

## Safe Next Step

Recommended next program:

`PROGRAM_OUTCOME_MAPPER_INTEGRATION_AND_FULL_SNAPSHOT_REFRESH_GATE`

Scope:

1. Add pure read-only mappers from existing audit/switch/operator audit/service history into RI6 actual input rows.
2. Add unit tests proving `prediction_actuals`, `service_actuals`, and `candidate_outcomes` become non-empty when existing logs contain matchable evidence.
3. Keep all authority advisory/read-only.
4. Run full tests.
5. Run production `v7-intelligence-snapshot-refresh --dry-run`.
6. Only after approval, run the existing approved snapshot refresh write path.
7. Verify production stores all 11 snapshot families.
8. Verify runtime snapshot gate freshness/source hashes.

## FINAL_VERDICTS

outcome_data_exists=true

outcome_data_record_count=6949

service_history_exists=true

channel_history_exists=true

execution_history_exists=true

rollback_history_exists=true

audit_history_exists=true

closure_history_exists=false

trust_inputs_exist=true

prediction_inputs_exist=true

recommendation_inputs_exist=true

ri6_outcomes_seen_zero_root_cause=EXISTING_OUTCOME_DATA_PARTIALLY_CONSUMED_WITH_MISSING_ACTUAL_OUTCOME_MAPPERS_AND_PARTIAL_PRODUCTION_SNAPSHOT_MATERIALIZATION

data_lineage_complete=false

lineage_breaks_found=true

lineage_breaks_repaired=false

new_truth_sources_created=false

duplicate_systems_created=false

runtime_mutation_performed=false

SAFE_NEXT_STEP=PROGRAM_OUTCOME_MAPPER_INTEGRATION_AND_FULL_SNAPSHOT_REFRESH_GATE
