# PROGRAM CTR.0 — Channel Trust & Recovery Reality Audit

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Mode: DISCOVERY ONLY

Safety result:

- implementation_changes=false
- runtime_mutation=false
- deploy_run=false
- commits_created=false
- new_storage_created=false
- new_snapshots_created=false
- new_api_created=false

## 1. Executive Summary

V7 already has a strong Channel Trust & Recovery foundation. It is not an empty area and must not be rebuilt as a second trust system.

Existing foundation:

- channel/service quality history exists in `ServiceHistoryStore`;
- execution trust exists in `ExecutionTrustModel`;
- risk, trust, blast-radius, prediction, candidate suitability and trust-evolution snapshots exist;
- `trust-evolution-summaries` already contains `channel_trust_recovery`;
- channel lifecycle states already exist: `NEW`, `TRUSTED`, `WATCH`, `DEGRADED`, `RECOVERING`, `QUARANTINED`;
- admin/operator UI already reads channel trust state from `trust-evolution-summaries.channel_trust_recovery`;
- runtime planner already reads required intelligence snapshot families, including `risk-summaries`, `trust-summaries`, and `blast-radius-summaries`.

The missing part is not "trust model from zero". The missing part is a stricter canonical decision about how advisory channel recovery becomes governed runtime policy, without creating duplicate truth sources or giving intelligence modules direct execution authority.

Final discovery verdict: `STRONG_FOUNDATION`.

## 2. Existing Trust Systems

| System | Location | Structure | Owner | Truth source | Runtime usage | Snapshot usage | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Execution trust model | `admin_core/routing_intelligence.py:743` | `ExecutionTrustModel.from_records()` scores successful executions, rollbacks, failures, governance violations, blast-radius expansions | `admin_core.routing_intelligence` | audit records, switch records, rollback records | advisory only, `runtime_decision_authority=none_shadow_only` | feeds `trust-summaries` and trust evolution | REUSE |
| Routing brain execution trust advice | `admin_core/routing_brain.py:40` | advisory contract may output `execution_trust_score` but may not move users or write selected moves | `RoutingBrain` | runtime truth + audit records | bounded planner score part only after hard gates | indirect via RI/advisory snapshots | EXTEND |
| Trust snapshot family | `admin_core/intelligence_snapshots.py:109` | `trust-summaries.json`, required for intelligence apply, stale behavior `STOP` | PERF.3 audit trust aggregation worker | audit history, switch history | runtime planner trust guard | canonical trust snapshot | REUSE |
| Trust evolution snapshot family | `admin_core/intelligence_snapshots.py:181` | `trust-evolution-summaries.json`, advisory only | RI6 trust evolution worker | trust, prediction, service, candidate, blast-radius, outcomes | advisory reader only | canonical trust evolution snapshot | EXTEND |
| Governed-to-autonomy trust bridge | `admin_core/intelligence_platform.py` | confidence and evidence bridge from governed outcomes to autonomy readiness | intelligence platform | outcomes, trust, prediction, recommendation, rollback | no runtime authority | trust-evolution summary content | REUSE_AS_EVIDENCE |
| Operator trust surface | `admin_core/operator_decision_surface.py:232` | `_trust_evolution_advice()` exposes confidence, trust, evidence counts, blockers | operator decision surface | `trust-evolution-summaries` | read-only operator view | consumes trust-evolution snapshot | REUSE |

Key evidence:

- `admin_core/routing_brain.py:56` explicitly forbids `move_users`, `bypass_planner`, `bypass_governance`, `write_selected_moves_directly`, `approve_execution`, `mutate_runtime_state`.
- `admin_core/routing_intelligence.py:743` defines the existing execution trust scorer.
- `admin_core/intelligence_snapshots.py:109` defines `trust-summaries` as required for intelligence apply with stale behavior `STOP`.
- `admin_core/intelligence_workers.py:200` defines trust worker inputs as audit, switch, and rollback history.

## 3. Existing Risk Systems

| System | Location | Structure | Owner | Truth source | Runtime usage | Snapshot usage | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Risk summary snapshot | `admin_core/intelligence_snapshots.py:97` | `risk-summaries.json`, required for intelligence apply, stale behavior `STOP` | PERF.3 risk worker | service scores, channel scores, quality summary | runtime planner risk guard | canonical risk snapshot | REUSE |
| Blast-radius snapshot | `admin_core/intelligence_snapshots.py:121` | `blast-radius-summaries.json`, required for intelligence apply, stale behavior `STOP` | risk/trust worker | risk + trust + runtime counts | runtime blast-radius guard | canonical blast-radius snapshot | REUSE |
| Dynamic blast radius model | `admin_core/routing_intelligence.py:819` | recommends bounded budget from trust, risk, platform health | RI.1 foundation | execution trust + service risk + platform health | advisory only | feeds risk/trust reasoning | EXTEND_AS_ADVICE |
| Runtime authority budgets | `tools/v7-users-autoswitch:144` | `CANARY=1`, `SMALL_BATCH=2`, `MEDIUM_BATCH=5`, `LARGE_BATCH=10`, `POOL=25` | runtime planner/governance | policy + authority evidence | hard runtime budget | not snapshot-owned | DO_NOT_TOUCH |
| Runtime safety policy | `tools/v7-users-autoswitch:107` | anti-flap, target block, egress quarantine policy | runtime planner | autoswitch safety state | hard runtime gate | not intelligence snapshot | DO_NOT_TOUCH |

Risk foundation is already split correctly: intelligence computes compact risk evidence, while runtime remains the owner of hard movement authority.

## 4. Existing History Systems

| System | Location | Structure | Owner | Truth source | Runtime usage | Snapshot usage | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Service history read model | `admin_core/routing_intelligence.py:430` | `ServiceHistoryStore` over `1h`, `24h`, `7d`, `30d` windows | RI.1 | `service-matrix.json`, `egress-quality-summary.json` | advisory service scoring | service/channel snapshots | REUSE |
| JSONL bounded history reader | `admin_core/intelligence_workers.py:76` | bounded tail reader, max records/bytes | intelligence workers | switch/rollback/history JSONL | worker input only | trust and trust-evolution snapshots | REUSE |
| Switch history | `tools/runtime-support/v7-switch-log` | append-only switch history | runtime support | movement events | feedback and audit input | trust evolution input | REUSE |
| Rollback history | `tools/v7-intelligence-snapshot-refresh:54` | CLI accepts rollback history file | runtime/event history | rollback events | feedback and safety input | trust/risk/rollback evidence | REUSE |
| Egress quality history compaction | `tools/v7-egress-quality-compact` | bounded quality history compaction | runtime support | quality samples | service stability evidence | service-score snapshots | REUSE |
| Client/path sample history | `tools/v7-path-sample-ingest` and `tools/v7-client-speed-api` | bounded path/user speed history | runtime support | client/path samples | observability and speed evidence | possible future CTR input | EXTEND_LATER |

History already exists in several forms. CTR should not create a new independent history store unless it is only an index/view over existing canonical histories.

## 5. Existing Channel Lifecycle Systems

| System | Location | Structure | Owner | Truth source | Runtime usage | Snapshot usage | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Channel trust recovery model | `admin_core/intelligence_workers.py:900` | `build_channel_trust_recovery_model()` computes lifecycle, trust score, recovery state, decay, routing impact | `admin_core.intelligence_workers.trust-evolution-summaries` | channel service scores, candidate suitability, best pool, decision records | advisory only | embedded inside `trust-evolution-summaries` | REUSE_AND_EXTEND |
| Channel lifecycle policy | `admin_core/intelligence_workers.py:1016` | lifecycle policy in model output | intelligence workers | current score, confidence, verdict, required services, feedback | no runtime authority | trust evolution | REUSE |
| Recovery state | `admin_core/intelligence_workers.py:994` | `NOT_NEEDED`, `IN_PROGRESS`, `RECOVERED`, `BLOCKED`, `REVIEW` logic | intelligence workers | feedback and lifecycle | advisory only | trust evolution | REUSE |
| Channel state UI mapping | `admin_core/operator_decision_surface.py:297` | labels/copy for `NEW`, `TRUSTED`, `WATCH`, `DEGRADED`, `RECOVERING`, `QUARANTINED` | operator decision surface | trust-evolution snapshot | read-only UI | consumes trust evolution | REUSE |
| Legacy channel fallback | `admin_core/operator_decision_surface.py:394` | fallback maps existing health to coarse state | operator surface | runtime/egress row | read-only UI fallback | none | EXTEND_CAREFULLY |
| Egress draft quarantine lifecycle | `admin/v7-admin-api:6460` | preflight/runtime/quarantine/add-disabled/provision/enable steps | admin API | egress draft metadata + runtime helper results | egress onboarding, not general CTR | draft metadata and service matrix evidence | REUSE_FOR_ONBOARDING_ONLY |

Important: general channel lifecycle already exists in `trust-evolution-summaries.channel_trust_recovery`; egress draft quarantine is a separate onboarding lifecycle and should not become the main CTR truth source.

## 6. Runtime Reality

Runtime currently knows the following about channels:

| Runtime item | Exists? | Evidence | Current owner |
| --- | --- | --- | --- |
| current health | EXISTS | `tools/v7-users-autoswitch:527` `Egress` has health fields; quality summary loaded at `tools/v7-users-autoswitch:593` | runtime planner |
| recent health | EXISTS | quality policy freshness at `tools/v7-users-autoswitch:77`; service truth freshness at `tools/v7-users-autoswitch:117` | runtime planner |
| historical health | PARTIAL | `ServiceHistoryStore` windows exist in RI; runtime itself reads compact snapshots rather than raw history | RI snapshots + runtime planner |
| failures | EXISTS | safety policy has failed verification quarantine fields at `tools/v7-users-autoswitch:107`; execution trust scans failures at `admin_core/routing_intelligence.py:769` | runtime + trust worker |
| recoveries | PARTIAL | prediction has recovery probability at `admin_core/routing_intelligence.py:926`; channel recovery state exists at `admin_core/intelligence_workers.py:994` | intelligence workers |
| stability | EXISTS | `Egress.stability` field at `tools/v7-users-autoswitch:547`; quality policy min stability at `tools/v7-users-autoswitch:80` | runtime planner |
| degradation | EXISTS | routing brain emits `degradation_risk_score` at `admin_core/routing_brain.py:212`; predictive model includes degradation domains at `admin_core/routing_intelligence.py:876` | RI/advisory snapshots |
| quarantine | EXISTS | autoswitch safety policy has egress quarantine fields at `tools/v7-users-autoswitch:114`; egress draft quarantine exists in admin API | runtime planner/admin onboarding |
| trust | EXISTS | runtime loads `trust-summaries` as required snapshot family at `tools/v7-users-autoswitch:58`; trust evolution is advisory at `tools/v7-users-autoswitch:3370` | snapshot + runtime planner |

Runtime does not currently grant channel trust recovery direct execution authority. That is good and should remain true until a future governed design explicitly promotes selected advisory fields into runtime policy gates.

## 7. Snapshot Reality

Canonical snapshot root:

- `admin_core/intelligence_snapshots.py:17`: `/opt/v7/egress/state/intelligence`

Snapshot ownership:

- `admin_core/intelligence_snapshots.py:237`: "Heavy Brain producers write; Runtime and Admin read"

Trust-related snapshot families:

| Raw data | Worker | Snapshot | Runtime/admin consumer | Runtime behavior |
| --- | --- | --- | --- | --- |
| service matrix, quality summary, service preferences | service score worker | `service-scores.json` | runtime planner advisory reader | WARN when stale |
| service matrix, quality summary, service preferences | service score worker | `channel-service-scores.json` | runtime planner channel ranking reader | WARN when stale |
| audit history, switch history, rollback history | trust worker | `trust-summaries.json` | runtime planner trust guard | STOP when stale/invalid |
| service/channel scores and quality summary | risk worker | `risk-summaries.json` | runtime planner risk guard | STOP when stale/invalid |
| risk + trust + runtime counts | blast-radius worker | `blast-radius-summaries.json` | runtime planner blast-radius guard | STOP when stale/invalid |
| users, egress, service matrix, quality, risk, trust, blast | candidate suitability worker | `candidate-suitability-summary.json` | runtime planner advisory reader | IGNORE when stale |
| trust, prediction, service, channel, suitability, best pool, blast, outcomes | trust evolution worker | `trust-evolution-summaries.json` | runtime/admin advisory reader | IGNORE when stale |

Existing trust signal path:

`audit/switch/rollback history` -> `admin_core.intelligence_workers` -> `trust-summaries.json` -> `tools/v7-users-autoswitch` trust guard.

Existing channel recovery signal path:

`channel-service-scores + candidate-suitability + best-available-pool + decision records` -> `build_channel_trust_recovery_model()` -> `trust-evolution-summaries.channel_trust_recovery` -> `operator_decision_surface` channel state rows.

Important snapshot rule:

- `trust-summaries`, `risk-summaries`, and `blast-radius-summaries` are runtime-required.
- `trust-evolution-summaries` is advisory-only today.

## 8. Routing Intelligence Reality

RI.1:

- `ServiceHistoryStore` exists and converts runtime truth into bounded service history.
- `ExecutionTrustModel` exists and scores execution trust from historical records.
- `DynamicBlastRadiusModel` exists as recommendation-only.

RI.2:

- `RoutingBrain` connects RI models to planner-facing advice.
- `routing_brain_map()` defines ownership and explicitly keeps planner/governance/runtime authority outside RI.

RI.3:

- advisory contract exists.
- It may output service suitability, degradation trend, execution trust, dynamic blast-radius advice, score parts, confidence, and explanations.
- It may not move users, override hard gates, write selected moves, approve execution, or mutate runtime state.

RI.4 / service scoring:

- service-specific quality models exist for Telegram, YouTube, Instagram, ChatGPT and generic services.
- channel-service scoring already feeds later trust/recovery logic.

RI.5 / prediction:

- prediction domains include channel quality, service quality, risk, trust, recovery, degradation, capacity, and blast radius.
- channel forecasts include degradation and recovery probability.

RI.6 / trust evolution:

- trust evolution aggregates decision records, prediction actuals, service actuals, candidate outcomes, rollback records, blast-radius records.
- `channel_trust_recovery` is already embedded in trust evolution.

Missing in RI:

- no single canonical CTR runtime policy contract yet;
- no clear rule for when `TRUSTED/WATCH/RECOVERING/QUARANTINED` becomes a hard runtime gate;
- no dedicated "channel recovery clearance" lifecycle equivalent to movement restore barrier;
- no final ownership document that says CTR policy lives in trust evolution while runtime enforcement remains in autoswitch/governance.

## 9. Admin Surface Reality

Admin/operator channel lifecycle already exists visually in part.

Evidence:

- `admin_core/operator_decision_surface.py:297` defines channel state labels.
- `admin_core/operator_decision_surface.py:306` defines human-readable state explanations and next steps.
- `admin_core/operator_decision_surface.py:346` reads channel trust rows from `trust-evolution-summaries.channel_trust_recovery`.
- `admin_core/operator_decision_surface.py:367` exposes `channel_state`, `channel_state_label`, explanation, next step, safe-now text, policy, evidence summary and raw reason.
- `tests/unit/test_operator_decision_surface.py:200` verifies the admin page has the existing column `Состояние доверия`, `channelStateCell`, `openChannelStateDrawer`, explanation and next-step data.

Admin quarantine/onboarding also exists:

- `admin/v7-admin-api:6460` tracks preflight/runtime/quarantine/add-disabled/provision/enable lifecycle.
- `admin/v7-admin-api:6679` reads quarantine evidence and service matrix evidence for draft pool readiness.

Classification:

- Reuse: existing channel state column/drawer and operator decision surface.
- Extend: make text shorter and more Russian/operator-friendly in a later UI program.
- Replace: none discovered.
- Do Not Touch: auth, RBAC, CSRF, execution handlers, rollback handlers, `run_action`, governance mutation paths.

## 10. Duplication Risks

If CTR is implemented today as a new independent subsystem, it would duplicate:

| Duplicate risk | Existing source that would be duplicated | Severity |
| --- | --- | --- |
| duplicate trust score | `ExecutionTrustModel`, `trust-summaries`, `trust-evolution-summaries` | HIGH |
| duplicate channel lifecycle | `trust-evolution-summaries.channel_trust_recovery` | HIGH |
| duplicate recovery state | `channel_trust_recovery.recovery` | HIGH |
| duplicate history model | `ServiceHistoryStore`, switch/rollback JSONL, quality history | HIGH |
| duplicate risk score | `risk-summaries`, `blast-radius-summaries` | MEDIUM_HIGH |
| duplicate quarantine logic | autoswitch safety quarantine and egress draft quarantine | MEDIUM_HIGH |
| duplicate admin channel state | operator decision surface channel state column/drawer | MEDIUM |
| duplicate runtime gates | `tools/v7-users-autoswitch` snapshot/authority/safety gates | HIGH |
| duplicate snapshot families | existing snapshot store already has trust/risk/recovery-adjacent families | HIGH |

Conclusion: CTR must be an extension of the current intelligence snapshot and runtime governance chain. A new parallel CTR store or CTR planner would be harmful.

## 11. Reuse Candidates

Reuse directly:

- `admin_core.intelligence_snapshots.SNAPSHOT_FAMILIES`
- `trust-summaries`
- `risk-summaries`
- `blast-radius-summaries`
- `trust-evolution-summaries`
- `ServiceHistoryStore`
- `ExecutionTrustModel`
- `PredictiveFoundation`
- `DynamicBlastRadiusModel`
- `build_channel_trust_recovery_model`
- `operator_decision_surface` channel state mapping
- `tools/v7-users-autoswitch` as runtime planner and enforcement owner
- existing switch/rollback/audit/closure history
- existing admin channel state drawer/column

## 12. Extend Candidates

Extend carefully:

- `trust-evolution-summaries.channel_trust_recovery`: should become the canonical advisory source for channel trust/recovery.
- `operator_decision_surface`: should expose simpler Russian copy, short reason, exact fix action, and one focused modal per issue.
- `tools/v7-users-autoswitch`: may later read CTR states as governed policy input, but only through existing snapshot gates and authority rules.
- `operator_execution_pipeline`: may later include CTR recovery clearance as a review item, not a new execution path.
- `intelligence_workers`: may later add richer recovery evidence fields inside the existing `trust-evolution-summaries`, not as a new snapshot family unless explicitly justified.

## 13. Do Not Touch Areas

Do not modify during CTR design unless a later program explicitly scopes it:

- user movement/apply path;
- `tools/v7-users-autoswitch --apply --verify`;
- rollback executor;
- restore barrier owner;
- selected moves writer;
- governance approval packet owner;
- auth/RBAC/CSRF;
- admin `run_action`;
- direct runtime state mutation;
- systemd/timers/deploy;
- authority ladder and budget promotion rules;
- raw production state files outside approved tooling.

## 14. Missing Pieces

Missing or incomplete:

- canonical CTR ownership statement;
- explicit rule separating advisory lifecycle from hard runtime policy;
- canonical mapping from `TRUSTED/WATCH/DEGRADED/RECOVERING/QUARANTINED` to planner/governance actions;
- recovery clearance process for moving a channel from blocked/recovering back to normal eligibility;
- operator action model that fixes only the specific channel issue from one focused modal;
- production evidence table showing current channel states and recent transitions;
- final duplication guard that forbids a second CTR state store;
- tests proving future CTR enforcement does not bypass existing planner/governance/runtime owners.

## 15. Recommended Architecture Direction

Do not create a new Channel Trust & Recovery system.

Recommended direction for the next stage:

1. Reuse `trust-evolution-summaries.channel_trust_recovery` as the canonical advisory CTR model.
2. Keep runtime enforcement owned by `tools/v7-users-autoswitch`.
3. Keep governance owned by existing approval packet, restore barrier, and execution pipeline modules.
4. Extend existing snapshots only when needed; prefer adding fields to `trust-evolution-summaries` over creating new families.
5. Use existing admin channel state UI as the operator surface.
6. In UI, show short Russian labels and one action per issue.
7. If a channel can be fixed from admin, open a focused modal for exactly that fix.
8. Never let CTR write selected moves, approve execution, or mutate runtime state directly.

The right next program is not "build CTR from scratch". It is:

`CTR.1 — Canonical Channel Trust & Recovery Ownership And Policy Mapping`

Expected CTR.1 scope:

- define canonical ownership;
- map lifecycle states to existing planner/governance behavior;
- decide which fields remain advisory and which may become hard gates later;
- design focused admin actions without touching execution paths;
- add tests for no duplicate truth source and no authority bypass.

## 16. Final Verdict

Final verdict: `STRONG_FOUNDATION`

Reason:

V7 already contains a substantial trust/recovery foundation:

- trust scoring exists;
- risk scoring exists;
- history inputs exist;
- channel lifecycle states exist;
- recovery states exist;
- trust evolution snapshots exist;
- admin channel state surface exists;
- runtime reads required trust/risk/blast-radius snapshots;
- authority boundaries are explicit and mostly healthy.

But it is not yet a complete governed CTR runtime policy layer. The current CTR-like logic is mostly advisory/read-only. The next work must consolidate ownership and policy mapping before any runtime enforcement or UI mutation work.

Final flags:

- existing_trust_systems=true
- existing_risk_systems=true
- existing_history_systems=true
- existing_channel_lifecycle_systems=true
- existing_recovery_tracking=true
- existing_admin_channel_surface=true
- existing_runtime_trust_guard=true
- duplicate_truth_source_risk=HIGH_if_new_CTR_created
- safe_to_design_CTR_1=true
- safe_to_implement_CTR_now=false
- required_next_step=CTR.1_canonical_ownership_and_policy_mapping
