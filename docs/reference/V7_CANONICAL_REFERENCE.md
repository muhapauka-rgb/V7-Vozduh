# V7 Canonical Reference

Status: canonical project reference
Last verified commit: `7b3f6bca`
Last verified date: 2026-06-23

This document describes the current meaning of V7 system concepts. It is not a history log and not an audit report. Reports remain evidence. ADRs explain why a decision was made. This reference is the current truth that future V7 work must read before re-auditing old concepts.

## Reference Update Rule

Any audit or implementation that changes system meaning must update this file. If the work makes or changes a decision, it must also add or update an ADR under `docs/decisions/`.

No important V7 knowledge may remain only in chat, temporary reports, Codex output, screenshots, or one-off validation notes.

Before commit and push after major logic work:

1. Update `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Update or create an ADR when a decision changed.
3. Run `tools/v7-truth-check --all --json`.
4. Run `tools/v7-convergence-status --json`.
5. Commit code and docs together.

## Knowledge Preservation Rules

1. No important knowledge may live only in chat.
2. No important knowledge may live only in reports.
3. Stable conclusions must move into `docs/reference/V7_CANONICAL_REFERENCE.md`.
4. Architectural decisions must move into ADRs under `docs/decisions/`.
5. Future audits must read this reference, relevant ADRs, and `docs/reference/SYSTEM_MAP.md` before auditing.
6. Full autonomy architecture, dependency, maturity, and roadmap questions must read `docs/reference/V7_AUTONOMY_BLUEPRINT.md` before launching a new autonomy-wide audit.

Before launching any new audit, use Reference First:

1. Read `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Read relevant ADRs.
3. Read `docs/reference/SYSTEM_MAP.md`.
4. Determine whether the answer already exists.

A new audit is allowed only when the reference has no answer, the reference explicitly marks the area `UNKNOWN`, system behavior changed after the last verified commit, or evidence contradicts this canonical reference. Otherwise, update the reference if needed and do not create a new audit.

## Certified Root Cause Rule

When a phase has already certified all of the following:

1. root cause found;
2. solution proven;
3. dry-run successful;
4. no runtime-apply risk;

the next phase must move to:

```text
IMPLEMENT
  -> TEST
  -> VERIFY
  -> DOCUMENT
```

It must not create another discovery/audit report for the same root cause.

Allowed exception: a new audit may run only if new evidence contradicts the certified root cause, the proven dry-run no longer reproduces, the implementation would introduce runtime apply risk, or the reference explicitly marks the area `UNKNOWN`.

This rule applies after Reference First. Reference First determines whether the answer already exists; Certified Root Cause Rule determines that a proven answer must be implemented and verified rather than re-discovered.

## Autonomy Blueprint Rule

`docs/reference/V7_AUTONOMY_BLUEPRINT.md` is the permanent autonomy engineering blueprint. It maps current subsystems, dependency graphs, hidden/dormant systems, maturity percentages, industry comparison, and the 12-month roadmap from governed operator actions to event-driven autonomy.

Current blueprint verdict: `AUTONOMY_BLUEPRINT_CREATED_EVENT_DRIVEN_AUTONOMY_PARTIAL`.

Stable conclusions:

1. V7 already has the main owners for planner, governed execution, restore barrier, rollback, feedback, learning, trust, prediction, shadow comparison, and truth/convergence.
2. The safe path is to reuse and connect existing owners, not create a new planner, governance model, execution path, truth source, or confidence model.
3. Production event-driven autonomy remains blocked by insufficient observed outcome confidence, low prediction confidence, uncertified live event consumption, and autonomy floors still below `70.0`. Operator comparison is secondary supervised confirmation, not the primary trust source.
4. Timer-only movement remains rejected. Event-driven autonomy means regression event -> planner -> packet -> restore barrier -> bounded apply -> verification -> rollback decision -> feedback -> learning.
5. The next roadmap position is `OBSERVED_OUTCOME_EVIDENCE_AND_EVENT_CONSUMER_CLOSURE`.
6. The post-production scale phase `AUTONOMY.EVIDENCE.INDEX_AND_FRESHNESS_MODEL` is documented but deferred. It must not start until Production Autonomy is certified.

## AUTONOMY_TRUST_SOURCE_HIERARCHY

1. Observed network outcome is the primary autonomy trust source for V7.
2. Primary sources are observed service outcome, observed channel quality, post-switch verification, rollback/no-rollback result, forecast-to-actual accuracy, and future client telemetry when implemented.
3. Operator comparison, operator override, and manual approval are secondary supervised evidence. They are useful only when the operator has enough operational context.
4. Manual operator actions are authoritative system actions, but they are not synthetic agreement with V7's autonomous recommendation.
5. After a manual action, V7 should respect the action and then observe service/channel outcome quality through existing evidence owners.
6. Operator comparison must not be used as blind bulk training data. Do not require an operator to manufacture comparison history for users whose real service quality they cannot directly observe.
7. Diagnostic sources such as raw technical health, route details, logs, and score components support explanation and troubleshooting; they are not primary autonomy trust sources by themselves.
8. Canary readiness must still block when primary observed-outcome confidence, trust, or prediction evidence is insufficient. Operator comparison may accelerate supervised confidence but does not replace observed outcome evidence.
9. Implementation owner for read-only classification: `admin_core/autonomy_trust_acceleration.py`; CLI surface: `tools/v7-autonomy-trust-evidence-inventory`.
10. Related ADR: `docs/decisions/ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.md`.

## AUTONOMY_EXPERIENCE_CONFIDENCE_MODEL

V7 experience is the accumulated observed evidence that connects a real operational state or action to a later real outcome. It is not a single score and not operator opinion alone.

Canonical flow:

```text
Reality
  -> Observation
  -> Evidence
  -> Outcome
  -> Suitability
  -> Confidence
  -> Trust
  -> Planner
  -> Action
```

Current production forensic truth from `AUTONOMY.CANDIDATE_OUTCOME.REALITY.COLLECTION`:

1. Prediction experience is complete for the current window: `21/21` matched rows. It is undervalued as raw accuracy evidence, but intentionally limited by low forecast source confidence.
2. Service/channel experience exists (`21` rows) and is fresh, but source row confidence remains low at about `0.39`, so it cannot certify autonomy by itself.
3. Candidate/suitability experience is consumed but incomplete: `84` real selected-candidate outcomes against `156` candidates, with `72` missing candidate outcomes.
4. Suitability is genuinely low, not merely hidden: current mean correctness is `62.132`, mean candidate confidence is `0.407`, and suitability confidence is `27.569`.
5. Blast and rollback experience are sufficient and contribute `100`; they are not current canary blockers.
6. Operator comparison evidence is secondary supervised confirmation and remains underfed (`0` comparisons in this forensic pass).
7. Read-only visibility and aggregation gaps were fixed in existing owners: the inventory now exposes `candidate_outcome_reality_collection`, trust refresh uses the full decision family for candidate outcomes, and snapshot refresh reads the extended JSONL evidence window. Final production classification reports `captured_but_not_consumed=0`, `visibility_issue=0`, and `aggregation_issue=0`.
8. The final verdict is `OUTCOME_EVIDENCE_INCOMPLETE`: the experience pipeline exists and consumes available reality, but canary remains blocked because `72` candidate user/channel outcomes have not happened yet and `43` consumed outcomes are still weakly weighted.

Related reports: `docs/reports/AUTONOMY_SUITABILITY_KNOWLEDGE_AND_CONFIDENCE_FORENSICS_REPORT.md`, `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`.
Implementation owner: `admin_core/autonomy_trust_acceleration.py`.

## POST_PRODUCTION_SCALE_PHASE

Phase name: `AUTONOMY.EVIDENCE.INDEX_AND_FRESHNESS_MODEL`.

Status: `DEFERRED_UNTIL_PRODUCTION_AUTONOMY_CERTIFIED`.

Purpose: prepare V7 for `100+` channels, `1000+` users, and years of evidence without planner slowdown, trust distortion, or irrational use of stale data.

This is not a current blocker. It is documentation of a future scalability phase. It does not authorize runtime changes, code changes, planner changes, trust changes, execution changes, new owners, new schemas, new storage, or new truth sources.

Evidence classification for the future phase:

| Class | Name | Examples | Future meaning |
| --- | --- | --- | --- |
| A | Fast Reality | Telegram, YouTube, latency, packet loss, Service Matrix, Route Readiness | Fresh operational probes that age quickly and should influence current state only while fresh. |
| B | Channel Behavior | Stability, speed, failure rate, recovery rate, quality trend | Medium-horizon behavior evidence that describes how a channel behaves over time. |
| C | Outcome Evidence | Candidate outcomes, governed outcomes, manual outcomes, post-switch verification | Direct proof that decisions or movements produced good or bad real outcomes. |
| D | System Safety Evidence | Blast, rollback, restore, packet validity, feedback closure, learning closure | Safety evidence proving V7 can act, verify, recover, and learn inside bounded governance. |

Future evidence index concept:

| Field | Meaning |
| --- | --- |
| `evidence_id` | Stable id for the future catalog row. |
| `timestamp` | Time the evidence was observed or closed. |
| `evidence_type` | Class/type of evidence, for example service probe, candidate outcome, rollback proof. |
| `channel_id` | Channel scope when applicable. |
| `service_id` | Service scope when applicable. |
| `owner` | Existing owner that produced the evidence. |
| `quality_score` | Current quality/correctness meaning, calculated by existing owners only. |
| `freshness_score` | Future freshness/age weighting, shadow-only until certified. |
| `confidence_score` | Existing confidence meaning from current models, not a new trust engine. |
| `weight` | Future derived weighting after shadow validation. |

Freshness principles:

1. Old evidence is not deleted.
2. Old evidence loses weight.
3. Freshness depends on evidence type.
4. Telegram/service probe evidence and blast/rollback safety evidence must not age identically.
5. Freshness must not change planner, trust, or execution behavior until it has passed shadow validation.

Future aggregated read models:

| Read model | Intended future role |
| --- | --- |
| `channel_current_summary` | Compact current channel state for planner/operator reads. |
| `channel_service_summary` | Service availability and freshness summary. |
| `channel_behavior_summary` | Stability, speed, failures, recovery, and quality trend summary. |
| `candidate_outcome_summary` | Candidate and assignment outcome summary. |
| `system_safety_summary` | Blast, rollback, restore, packet, feedback, and learning safety summary. |
| `trust_evolution_summary` | Existing trust evolution summarized for scalable reads. |

Cardinality control rules:

1. Allowed dimensions should stay bounded: evidence type, channel, service, owner, time bucket, and outcome class.
2. High-cardinality risk comes from per-user, per-request, per-packet, per-log-line, and unbounded raw event dimensions.
3. Future mitigation should use existing-owner aggregation, bounded time windows, summaries, and retention-aware indexes before planner consumption.
4. Raw detail may remain in evidence/history stores, but planner-facing reads should use aggregated summaries.

Shadow validation rule:

Any future freshness/index model must first run in shadow mode with no direct planner impact, no direct trust impact, no direct execution impact, and no direct governance impact. It must compare old behavior versus freshness-weighted behavior before promotion.

Integration rule:

Any future implementation must reuse existing owners, existing truth sources, existing planner, existing governance, and existing execution path. It must not create a new trust engine.

Activation criteria:

1. Production Autonomy is certified.
2. Event-driven autonomy is operating through the existing chain: regression -> planner -> packet -> restore barrier -> bounded apply -> feedback -> learning.
3. Evidence volume or query cost demonstrates a real scale need, such as `100+` channels, `1000+` users, or multi-year evidence history.
4. A shadow freshness/index validation proves no trust distortion and no planner regression.
5. Truth and convergence pass before and after any future implementation.

Related ADR: `docs/decisions/ADR-FUTURE-EVIDENCE-INDEX-AND-FRESHNESS-MODEL.md`.

## Channels Final UX Rules

1. Channel Decision V7 is primary.
2. Channel table signals stay compact and are explained by the S/L/R/T header legend plus one V7-styled tooltip source.
3. Only one tooltip source is allowed for signal dots; native browser `title` tooltips must not duplicate custom tooltips.
4. Channel diagnostics use a balanced layout: summary first, then responsive reality-first diagnostic cards.
5. Diagnostics primary text is reality-first, not score-first; score math and point loss must not dominate the operator view.
6. Trust/recovery metadata must not compete with Channel Decision V7 in the first-level Channels table.
7. Every channel warning must be actionable. A visible warning must explain one of three outcomes: existing safe action and where it opens, automatic handling and what updates it, or why no safe action is available.
8. Channel drawer first screen must remain a compact operator inspection surface, not a form-like stack of nested cards. The first screen answers: channel, V7 decision, reason, next safe action, active problems, compact signals, and where engineer diagnostics live.
9. Ambiguous labels such as "check", "verify", "clarify", or "attention" are not enough on channel surfaces. If evidence is incomplete, the wording must say the reality and next step, for example "fresh data unavailable", "open service matrix", "open users", "open logs", "automatic refresh pending", or "safe action unavailable".
10. Operator Surface and Engineering Surface are separate. The Channel Drawer first screen must not show `score/100`, technical health/rating, confidence labels, raw status/state, evidence, history, logs, execution details, or service matrix details. Those belong behind the Engineer Diagnostics boundary.
11. The aggregate `Сигналы` table column is a compact visual container, not a sortable truth. Channel ordering may use individual first-level signals only: Services, Load, Runtime, or Stability.

## Channel Drawer Operator Rules

1. Channel identity is shown once, in the drawer header.
2. Decision is shown once.
3. Reason is shown once.
4. Operator view contains no score math, score badges, confidence labels, raw technical state, service matrix detail, evidence, execution, logs, settings, or debug content.
5. Every first-screen signal is actionable: clicking the signal opens an inline explanation and the existing safe destination when one exists.
6. Every first-screen problem is actionable: clicking the problem opens an inline explanation and the existing safe destination when one exists.
7. If no safe action exists, the UI explains why inside the same drawer.
8. Engineering diagnostics has one entry point and remains collapsed below the operator answer.
9. Settings and debug content must not appear in the operator view.
10. First-screen operator wording must avoid vague labels such as `Уточнить`, `Требует проверки`, and `Уверенность неполная`; use concrete reality-first wording such as `Нет свежих данных`, `Нет свежего подтверждения`, `Открыть матрицу сервисов`, `Открыть пользователей`, `Открыть логи`, or `Действие недоступно`.

## CHANNEL_OPERATOR_LANGUAGE_RULES

1. Decision first: Channel Decision V7 is the final operator answer.
2. Reason second: the first reason explains why V7 wants that decision.
3. Signals third: signals explain confidence and evidence behind the decision; they are not a second decision model.
4. Engineering hidden: scores, formulas, raw readiness, trust math, capacity math, planner internals, evidence, and logs stay behind Engineering Diagnostics.
5. Yellow never overrides decision: yellow signals mean attention or freshness limits, not "do not use" by themselves.
6. Red may influence decision: red signals can participate in `Evacuate`, `Blocked`, or other assignment restrictions and must explain the impact in operator language.
7. Signal details must answer `What happened`, `Why`, and `What to do`, without using a competing `Decision` field.
8. Problem details must answer `What happened`, `Why it matters`, and `What can be done now`.
9. Operator copy must avoid developer-only terms on the first screen, including raw `runtime`, `confidence`, `evidence`, `snapshot`, `eligibility`, `trust score`, and planner/gate internals.
10. If a warning does not change the decision, the UI must say that plainly, for example: "does not prohibit use" or "follow V7 decision".

## OPERATOR_ACTION_FLOW_RULES

1. Every operator-visible channel issue must explain itself.
2. Every issue detail must show a consistent structure: status, reason, decision impact, and action.
3. Every issue must explicitly explain whether it affects Channel Decision V7.
4. Every issue must explain whether operator action is required, optional, automatic, or unavailable.
5. Action categories are `Observe`, `Review`, and `Execute`; `Execute` may only prepare or open an existing governed flow.
6. Action rows must state where the action leads and what result the operator should expect.
7. A visible issue must not end at explanation only. If no safe action exists, the UI must say why in the same expanded item.
8. Problem details and signal details use the same action-flow structure.
9. Existing destinations are reused: Service Matrix, channel users, channel logs, engineering diagnostics, and governed user/action flows.
10. This rule does not create new planner logic, routing logic, signal calculations, governance, storage, or execution paths.

## CHANNEL_ATTENTION_RULES

1. Channels attention is a derived operator view, not a new truth source.
2. Channels attention must reuse existing Channel Decision V7, Overview Attention, first-level channel signals, service matrix, capacity/load, runtime readiness, stability, and channel status.
3. Attention priority is strict: Critical, Action Required, Review, Information, Healthy.
4. Critical means the operator should look first because users may need to leave or users are on a channel V7 should not use.
5. Action Required means an existing safe destination/action exists now.
6. Review means the channel needs fresh evidence or inspection but does not override Channel Decision V7 by itself.
7. Information means the role/state matters but can wait when no users or active problems are affected.
8. Healthy means Use or Keep with first-level operator signals OK; these channels can be ignored during triage.
9. Attention First sorting may reorder the Channels table by derived attention priority, assigned users, first-level signal severity, existing default operator order, and channel name.
10. Default table mode must preserve existing channel table behavior and manual sort settings.
11. The aggregate `Сигналы` column must not become a sortable truth. Attention ordering may use individual first-level signal severities only.
12. Attention visual styling must stay calm: urgent rows may have a narrow marker, while healthy rows remain visually quiet.
13. Attention entries must open existing destinations only: Channel Drawer, Service Matrix, channel users, logs/diagnostics, or existing governed user/action flows.
14. This rule does not change planner logic, assignment logic, execution, governance, signal calculations, decision logic, capacity formulas, routing formulas, storage, or database state.

## POOL_AUTONOMY_RUNTIME_RULES

1. V7 autonomy has been certified through governed execution up to 10 users, but that certification is not the same as a continuously enabled production daemon.
2. WireGuard `wireguard-1779454504-c43409` is promoted into the production pool and is a valid production channel, subject to the same planner/capacity/load gates as every other channel.
3. POOL.2 evidence on 2026-06-19 showed `POOL_NEEDS_RECOVERY`: active distribution `awg3=8`, `wireguard=8`, `vless=10`, with 8 failover candidates from `awg3` to `wireguard-1779454504-c43409`.
4. POOL.3 evidence on 2026-06-21 showed active distribution still `awg3=8`, `wireguard=8`, `vless=10`; `awg0` remained below stability floor; `awg3` was barely above stability floor but below min-speed floor and hard-full; WireGuard remained technically strong but hard-full. Fresh available API evidence did not reproduce the old 8-user awg3-to-WireGuard failover as an actionable current apply.
5. Current truth says `autoswitch_scheduler_active=false` and `autoswitch_service_active=false`, with inactive scheduler approved as manual mode.
6. Production autonomy direction is event-driven autonomy: channel/service regression -> planner -> packet -> restore barrier -> bounded apply -> verification -> rollback decision -> feedback -> learning.
7. Timer-only movement is rejected as a product model. Periodic probes and previews may run; periodic blind user movement must not run.
8. Any future production autonomy daemon must reuse existing planner, packet, restore barrier, execution, rollback, feedback, learning, truth, and convergence owners.

## EVENT_TRIGGER_READ_ONLY_CERTIFICATION

1. EVENT.1 evidence on 2026-06-21 certified the current event-driven autonomy trigger chain as read-only and blocked for live production apply.
2. Existing regression/evidence sources include `tools/v7-telegram-sentinel`, service matrix refresh, egress quality compaction, route/runtime/capacity read models, and planner blocker transitions.
3. The existing chain can preview planner output, execution packet draft, restore barrier ownership, rollback model, feedback model, and learning/confidence evidence without moving users.
4. EVENT.1 current truth: `preview_only=true`, `read_only=true`, `execution_allowed_now=false`, `apply_executed=false`, `users_moved=0`, `rollback_executed=false`, and `autonomy_enabled=false`.
5. EVENT.1 blockers were `confidence_too_low`, `trust_too_low`, `prediction_confidence_too_low`, operator comparison evidence below floor, restore barrier readiness blocked, and no certified live event consumer binding from regression evidence to governed planner trigger.
6. `v7-telegram-sentinel` is an event/regression source, but current service mode uses `--no-autoswitch`; it is not a certified production apply trigger.
7. EVENT.1 final verdict is `EVENT_TRIGGER_BLOCKED`.
8. EVENT.CONSUMER.READONLY.2 certified the missing read-only event consumer link without enabling apply. Existing production events now flow through `admin_core/events.py` into `admin_core/operator_execution_pipeline.py::event_consumer_readonly_certification_model`, which previews planner, packet, restore barrier, rollback, feedback, and learning surfaces without mutation.
9. EVENT.CONSUMER.READONLY.2 evidence used 10 real production event rows from Telegram Sentinel and Service Matrix. The read-only certification produced `event_count=10`, `primary_event_count=10`, `packet_preview_count=1`, `restore_preview_count=1`, `rollback_preview_count=1`, `feedback_preview_count=1`, `learning_preview_count=1`, `apply_executed=false`, `users_moved=0`, and `autonomy_enabled=false`.
10. The event consumer is now certified only as read-only. It is not a daemon, not an apply authority, not a new truth source, and not permission to move users. The next safe phase is readiness recheck plus evidence collection until confidence, trust, prediction, restore barrier, rollback, feedback, and learning gates pass together.

## AUTONOMY_CANARY_READINESS

1. AUTONOMY.CANARY.1_READINESS_RECHECK on 2026-06-23 returned `AUTONOMY_CANARY_NO_GO`.
2. The canary blocker is not missing architecture. Existing owners for event consumer, planner preview, packet preview, restore barrier preview, rollback preview, feedback preview, and learning preview are present and read-only certified.
3. Current production floors remain below the `70.0` canary requirement: confidence `39.606`, trust `54.705`, prediction confidence `36.859`, and secondary operator earned confidence `45.807`.
4. Current production comparison evidence remains underfed: comparison count `0`, agreement rate `0.0`, reviewable decisions `27`.
5. Current prediction lifecycle is durable but under-confident: `21/21` forecasts matched actuals, `0` pending rows, forecast accuracy `97.189`, and prediction confidence `36.859`.
6. Blast and rollback are not current blockers: blast radius confidence is `100.0` and rollback confidence is `100.0`.
7. The current planner observe run selected `0` moves and stopped with `dry_run_intelligence_snapshot_stop_required`; snapshot stop families were `service-scores` and `channel-service-scores`.
8. Snapshot refresh dry-run is stable and non-mutating: `source_stable=true`, `snapshot_count=11`, `runtime_behavior_changed=false`, `governance_behavior_changed=false`, and `users_moved=false`.
9. Production autonomy remains disabled. No apply, no user movement, no daemon enablement, no autoswitch enablement, no threshold/floor/formula change, no synthetic evidence, and no new truth source occurred.
10. Shortest safe path before another canary decision: snapshot gate / candidate recheck through existing owners, real observed service/channel outcome collection, prediction source-confidence collection, contextual supervised operator comparison if useful, then another canary readiness recheck.
11. AUTONOMY.CANARY.1A on 2026-06-23 returned `CANDIDATE_VISIBILITY_BLOCKED`.
12. Current production planner evidence shows `candidate_moves_total=18` with distribution `awg3=8`, `wireguard-1779454504-c43409=8`, and `vless=10`, but normal `v7-users-autoswitch --mode observe` still returns `selected_move_count=0` because snapshot gate stops on `service-scores` and `channel-service-scores` source mismatch against `service_matrix`.
13. Standalone `v7-intelligence-snapshot-refresh --pretty` is snapshot-only and safe (`source_stable=true`, `snapshot_count=11`, `runtime_behavior_changed=false`, `governance_behavior_changed=false`, `users_moved=false`), but by itself does not make the normal planner observe path persistently pass the snapshot gate.
14. Planner-owned refresh through existing `v7-users-autoswitch --mode observe --max-selected-moves 1 --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh` clears snapshot gate inside that observe run (`stop_required=false`, `stop_families=[]`) without apply or user movement, but the run then stops at `dry_run_restore_barrier_clearance_generation_expired`.
15. AUTONOMY.CANARY.1B on 2026-06-23 implemented the smallest existing-owner durability fix in `tools/v7-users-autoswitch`: normal read-only `--mode observe` now auto-enables the existing pre-planner snapshot refresh owner when no explicit pre-refresh mode is supplied; explicit modes still win and `--apply` does not auto-enable refresh.
16. After deploy, production normal observe reports `snapshot_gate.stop_required=false`, `stop_families=[]`, `pre_planner_refresh.auto_enabled=true`, `pre_planner_refresh.state=REFRESH_SUCCESS`, and then stops at `dry_run_restore_barrier_clearance_generation_expired`.
17. Candidate visibility is now real on the normal observe path: production reports `candidate_moves_total=8`; canary-limited observe exposes the fresh candidate `10.0.0.2` from `awg3` to `wireguard-1779454504-c43409` before the restore guard.
18. A fresh execution packet preview for that one canary candidate validates as `PACKET_VALID` with `runtime_action=CREATE_RESTORE_BARRIER_CLEARANCE`, but no packet execution, restore-barrier write, apply, user movement, daemon, synthetic evidence, floor change, or new truth source occurred.
19. Canary is still blocked by restore: the current production restore barrier clearance expired on `2026-06-13T19:29:19.851623+00:00`, references planner generation `1fd508b2fc82598d134f3defb598dd6593f0decd3da8437d953e788c3d3c098b`, and contains an old approved plan lock for 10 `vless` moves. The fresh generation is `d4098562a46e2cb32db70bab1943d638637198b896423da9b633f79d8e250080`, so reusing the old lock is correctly rejected with `approved_plan_lock_expired` and `approved_plan_lock_user_source_mismatch`.
20. AUTONOMY.CANARY.1B final verdict is `CANARY_BLOCKED_BY_RESTORE`. The next safe phase is explicit governed restore-barrier clearance generation through the existing `tools/v7-operator-execution-packet` / `admin_core/operator_execution.py` owner, followed by another readiness recheck. This must not move users unless a later phase separately authorizes apply.
21. AUTONOMY.CANARY.1C on 2026-06-23 implemented the smallest existing-owner restore-barrier lifecycle fix: `admin_core/operator_execution.py` can now run a read-only `runtime_action_preview` for `CREATE_RESTORE_BARRIER_CLEARANCE` via `tools/v7-operator-execution-packet --preview-runtime-action`.
22. The new preview does not write the restore barrier, does not append audit/lifecycle state, does not apply autoswitch, and does not move users. It preserves duplicate active owner denial and returns explicit non-mutation flags.
23. Production 1C evidence shows `candidate_moves_total=8`; a fresh packet `pkt_09e0c1125bc0a6016abbb5a6` selects one canary move: `10.0.0.2 awg3 -> wireguard-1779454504-c43409`.
24. Restore-barrier preview now passes for that fresh packet with `ALLOW_RESTORE_BARRIER_CLEARANCE` and `RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID`; the clearance preview uses generation `d4098562a46e2cb32db70bab1943d638637198b896423da9b633f79d8e250080` and selected move count `1`.
25. The valid clearance preview survives reread and an explicit snapshot refresh. Normal production observe still stops at `dry_run_restore_barrier_clearance_generation_expired` because 1C intentionally did not write clearance state.
26. After restore preview is clear, the next canary blocker is evidence confidence: confidence `39.558`, trust `54.668`, prediction confidence `36.511`, and secondary operator earned confidence `45.837`, all below the `70.0` floor.
27. AUTONOMY.CANARY.1C final verdict is `CANARY_BLOCKED_BY_CONFIDENCE`; the next safe phase is real existing-owner confidence/trust/prediction evidence closure, not runtime apply.
28. AUTONOMY.TIER1.GOVERNED_CANARY.READINESS on 2026-06-24 prepared and validated a fresh governed one-user canary packet without apply, movement, daemon enablement, runtime write, floor/formula change, synthetic evidence, or new truth source.
29. Fresh production reality changed from the older 1C candidate: `v7-users-autoswitch --mode observe --max-selected-moves 1` now exposes one planner-selected pre-guard canary candidate `10.7.0.5 vless -> awg0`. The older WireGuard target remains a strong candidate but is not the selected current target; target-constrained WireGuard observe produced no selected pre-guard move.
30. The fresh packet `pkt_7c64f53a8fd169a07445c438` validates as `PACKET_VALID` for operation `govexec_ebf49d9c3f11a0cdd04cd738`; its rollback manifest maps `10.7.0.5 awg0 -> vless`.
31. Production registry-backed restore preview for that packet passes with `ALLOW_RESTORE_BARRIER_CLEARANCE` and `RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID`; it writes no record, performs no runtime mutation, performs no user movement, and does not apply autoswitch.
32. Current trust inventory reports `TIER_1 MARGINAL_OPERATOR_REVIEW`: confidence `38.82`, trust `54.115`, prediction confidence `35.514`, operator earned confidence `45.815`, rollback confidence `100.0`, and `72` missing candidate outcomes. Autonomous one-user canary remains `NO_GO`.
33. Final verdict for the phase is `TIER1_GOVERNED_CANARY_MARGINAL`: V7 can prepare a complete governed one-user canary packet, but execution still requires a separate explicit operator approval for the exact packet and target. Because the target is now `awg0`, operator review is mandatory before any apply.

## AUTONOMY_RISK_TIERED_FLOOR_MODEL

1. V7 uses tiered floor semantics for autonomy readiness as of AUTONOMY.FLOOR.SEMANTICS_AND_RISK_TIER_REVIEW.
2. The implementation is read-only semantics in `admin_core/operator_execution_pipeline.py::autonomy_risk_tier_floor_model`, `admin_core/operator_execution_pipeline.py::autonomy_risk_tier_review`, and `admin_core/autonomy_trust_acceleration.py::build_canary_proximity`.
3. Existing hard autonomous canary floors were not lowered: confidence `70.0`, trust `70.0`, and prediction confidence `70.0` still block bounded autonomous one-user canary readiness.
4. The accepted tiers are:
   - `TIER_0`: read-only preview, no apply, no movement.
   - `TIER_1`: first one-user governed canary review. If absolute safety gates are clean but confidence floors are low, status may be `MARGINAL_OPERATOR_REVIEW`; this is not `AUTONOMY_CANARY_GO`.
   - `TIER_2`: governed canary requiring hard `70/70/70`.
   - `TIER_3`: bounded autonomous one-user canary requiring hard `70/70/70` and a future explicit autonomy authority.
   - `TIER_4`: bounded autonomous small batch requiring `85/85/85`.
   - `TIER_5`: batch autonomy requiring `90/90/90`.
   - `TIER_6`: production autonomy requiring `95/95/95`; not granted by the current program.
5. Non-negotiable gates stay absolute for every movement tier: candidate exists, packet valid, rollback target known, restore barrier available before apply, snapshot gate clean, no hard service/capacity blocker, and existing runtime owner only.
6. Current certified values simulate as `TIER_1 MARGINAL_OPERATOR_REVIEW` and `TIER_3 NO_GO`: confidence `38.872`, trust `54.154`, prediction confidence `35.385`, rollback confidence `100`.
7. This model changes wording and readiness classification only. It does not change formulas, thresholds, runtime apply, planner, governance, execution, daemon status, autoswitch status, or truth source.
8. Related report / ADR: `docs/reports/AUTONOMY_FLOOR_SEMANTICS_AND_RISK_TIER_REVIEW_REPORT.md`, `docs/decisions/ADR-AUTONOMY-RISK-TIERED-FLOORS.md`.
9. AUTONOMY.TIER1.GOVERNED_CANARY.READINESS confirms the same tier semantics on fresh production evidence: `TIER_1 MARGINAL_OPERATOR_REVIEW`, `TIER_2+ NO_GO`, and no autonomous apply authority. Current planner-selected TIER_1 packet is `10.7.0.5 vless -> awg0`; the packet and restore preview are valid, but execution is still a separate governed apply decision.

## AUTONOMY_TRUST_SUFFICIENCY_MODEL

1. Trust sufficiency means "enough trust for this tier", not "enough trust for every autonomy tier".
2. Current stable verdict is `TRUST_MODEL_MIXED`.
3. The model is correct and safe for blocking autonomous canary and production autonomy: current production remains `TIER_2+ NO_GO` and autonomous one-user canary remains `NO_GO`.
4. The model is also correct for `TIER_1`: a first one-user governed canary may be `MARGINAL_OPERATOR_REVIEW` when non-negotiable gates are clean, but this is not an autonomous GO.
5. The mixed part is semantic/operational clarity: `70/70/70` must be described as the hard governed/autonomous progression boundary for TIER_2 and TIER_3+, not as a requirement to merely prepare a TIER_1 operator-reviewed packet.
6. Current production facts remain: prediction `21/21`, candidate outcomes `84/156`, missing outcomes `72`, blast `100`, rollback `100`, capture/visibility/aggregation loss `0`, confidence about `38.8`, trust about `54.1`, prediction confidence about `35.5`, operator earned confidence about `45.8`.
7. Full candidate coverage alone is not sufficient. Current projection for converting all `72` missing candidate outcomes reaches only about confidence `51.832`, trust `62.794`, suitability `52.769`, and still fails primary canary floors.
8. Prediction is undervalued as raw accuracy but fairly discounted as autonomy source confidence because the formula is `mean(matched_forecast_accuracy) * mean(forecast_confidence)`.
9. Blast and rollback confidence make a bounded governed canary safer, but they do not substitute for prediction, service, or suitability evidence.
10. No floor, formula, planner, governance, execution, truth source, daemon, autoswitch, runtime apply, synthetic evidence, or user movement changed in AUTONOMY.TRUST.SUFFICIENCY.MODEL.
11. The exact next phase is `AUTONOMY.TIER1.GOVERNED_CANARY.APPLY_DECISION`: approve or reject packet `pkt_7c64f53a8fd169a07445c438` (`10.7.0.5 vless -> awg0`) through existing owners only.
12. Related report / ADR: `docs/reports/AUTONOMY_TRUST_SUFFICIENCY_MODEL_REPORT.md`, ADR-AUTONOMY-TRUST-SUFFICIENCY-TIER-AWARE.
13. Last verified commit: `d4ee291be875b825fb883d835621c8530c8eda8c`.

## AUTONOMY_ROOT_CONFIDENCE_TRUST_MODEL

1. V7 has two related but separate confidence layers: governed execution evidence and operator-free autonomy evidence.
2. Governed execution evidence comes from certified BA runs, execution outcomes, feedback, rollback readiness, and intelligence snapshots. It can raise inherited execution trust.
3. Operator-free autonomy evidence is stricter: it must prove safe autonomous trigger, self-stop, rollback decision, observed outcome quality, confidence floors, and operator-free apply boundary. Operator comparison is secondary supervised confirmation, not the primary proof.
4. BA1/BA3/BA4 evidence is consumed by `trust-evolution-summaries`; EVENT.1 reports `evidence_produced=true`, `evidence_stored=true`, `evidence_visible=true`, `evidence_consumed=true`, and `evidence_weighted=true`.
5. BA evidence does not automatically certify production autonomy. It currently raises inherited execution trust to `87.048`, while autonomy-specific trust remains `0.0` and autonomy-specific gap remains `100.0`.
6. Current candidate floor gates are owned by `admin_core/operator_execution_pipeline.py`. Floors are `confidence >= 70`, `trust >= 70`, and `prediction_confidence >= 70`.
7. Current EVENT.1 values are `confidence=45.8`, `trust=39.584`, and `prediction_confidence=39.6`; all are below floor, so apply must stop.
8. Outcome evidence is active and consumed from `trust-evolution-summaries`, but current component quality is insufficient: decision `50.0`, service `39.225`, suitability `29.528`, blast-radius `0.0`, prediction `37.355`, rollback `100.0`.
9. Shadow comparison evidence is owned by `admin_core/shadow_autonomy.py` and the existing `/api/actions/shadow-autonomy-compare` endpoint. Current production comparison count is `0`, so earned confidence remains about `45.802`, but this is a secondary supervised signal and must not force blind operator review.
10. Missing primary evidence must be collected through existing owners only: observed service/channel outcomes, matched prediction actuals, matched service/candidate outcomes, post-action verification, rollback/no-rollback evidence, and explicit blast-radius evidence. Read-only event consumer certification is complete, but evidence floors still block apply.
11. Lowering floors, adding a new planner, adding a new execution path, or enabling a timer/daemon to move users would violate the current autonomy model.
12. Last verified commit: `68b4153e95712b1ac432ccfac785561025ea4aed`.

## AUTONOMY_EVIDENCE_COLLECTION_RULES

1. Operator comparison evidence is collected only through the existing shadow autonomy comparison path: `/api/actions/shadow-autonomy-compare`.
2. A comparison record is valid only when a real operator judges a current shadow `decision_id` as `agree`, `disagree`, or `override`. Synthetic agreement records must not be generated to raise confidence.
3. The comparison endpoint writes `operator_comparison` records to the existing shadow autonomy JSONL store and admin audit, while reporting `runtime_mutation_performed=false`, `users_moved=0`, `apply_executed=false`, and `autonomy_enabled=false`.
4. Operator comparisons raise shadow `comparisons_total`, agreement rate, and earned confidence. They do not directly raise candidate trust or prediction confidence, and they are secondary supervised evidence rather than the primary autonomy trust path.
5. Prediction confidence improves only through existing matched prediction actuals from service/channel evidence, existing governed prediction feedback, and intelligence snapshot refresh. Current EVENT.1 evidence has `prediction_actuals_count=21`, `prediction_confidence=37.355` from outcome evidence, and final candidate prediction confidence `39.6`.
6. Service confidence improves through existing service matrix / channel-service score / quality evidence consumed by `service_intelligence_trust_model`. Current EVENT.1 service confidence is `39.225`.
7. Candidate confidence improves through existing candidate suitability and governed outcome evidence. Current EVENT.1 has `candidate_outcomes_count=83`, `suitability_confidence=29.528`, and final candidate confidence `45.8`.
8. Blast-radius confidence is owned by the existing `blast_radius_confidence_model` and `build_blast_radius_evidence_rows`; current EVENT.1 value is `0.0`, meaning consumed records did not classify into explicit usable blast-radius evidence.
9. Evidence collection may update evidence stores and snapshots only through existing owners. It must not create a new evidence store, planner, governance path, execution path, confidence model, trust model, prediction model, or truth source.
10. OPERATOR.COMPARISON.COLLECTION.1 implemented the durable existing-owner comparison collection path. `admin_core/shadow_autonomy.py` now exposes an operator review packet, per-decision comparison eligibility, and growth projection using the existing earned-confidence formula. `admin/v7-admin-api` reads active and rotated shadow-autonomy JSONL family records and preserves comparison rows separately from decision rows so old real comparisons are not displaced by newer shadow decisions.
11. Production inventory on 2026-06-23 found 27 users, 27 reviewable current shadow decisions, 0 comparison records, agreement rate `0.0`, earned confidence `45.802`, and user distribution `awg3=8`, `wireguard-1779454504-c43409=8`, `vless=11`.
12. Real operator comparison evidence must still be collected through the existing UI/API. The path is ready; the evidence volume is not.
13. Implementation commit: `f86148dc70a3a4d039dc41b555060ae0d2d4f13e`; deploy id `deploy-z8-14-Updatesystem-f86148d-20260623T094821`.
14. AUTONOMY.TRUST.ACCELERATION.1 added a read-only evidence inventory owner: `admin_core/autonomy_trust_acceleration.py` and `tools/v7-autonomy-trust-evidence-inventory`.
15. The trust acceleration inventory is a derived read model only. It may expose prediction collection plans, operator review batches, growth projections, and canary proximity, but it must not create synthetic comparisons, synthetic actuals, runtime apply, user movement, daemon enablement, new storage, new planner, new governance, new execution, new confidence model, or new truth source.
16. Production trust acceleration inventory after final deploy and snapshot refresh found 27 reviewable decisions, 0 reviewed decisions, 0 comparisons, agreement rate `0.0`, and earned confidence `45.802`.
17. The inventory exposes review batches for 5, 10, and 15 current decisions. A 5-comparison batch is insufficient for the `70.0` earned-confidence floor even at 100% agreement (`59.352`). A 10-comparison batch reaches the floor only at 100% agreement (`72.901`). A 15-comparison batch reaches the floor at 90% (`78.951`) or 80% (`71.451`) agreement, but not at 75% (`67.701`).
18. If operator comparison evidence is collected, it should use only recommendations where the operator has enough context. It must not be blind bulk training data. All comparison evidence must still pass through `/api/actions/shadow-autonomy-compare`.
19. AUTONOMY.TRUST.ACCELERATION.1 final verdict is `AUTONOMY_TRUST_ACCELERATION_PARTIAL`.
20. Implementation commits: `fd868640185461abb42f0e010e3beada9e6d9fc2`, `43effb2a7a58a545fd90d48db53bbe1c0968a75b`; final deploy id `deploy-z8-14-Updatesystem-43effb2-20260623T101511`.
21. AUTONOMY.TRUST.SOURCE.REALITY.1 reclassified operator comparison as secondary supervised confirmation and observed network outcome as the primary trust source. The read-only inventory now exposes `trust_source_classification`, `operator_authority_model`, `primary_real_evidence_path`, `secondary_supervised_confirmation_path`, and `blind_operator_training_required=false`.

## AUTONOMY_PREDICTION_EVIDENCE_RULES

1. Prediction confidence is calculated by `admin_core/intelligence_platform.py::prediction_accuracy_model`.
2. Forecasts are generated by `admin_core/intelligence_workers.py::build_prediction_snapshot` from existing service matrix, quality summary, risk, trust, and blast-radius evidence.
3. Forecast rows are extracted from existing `channel_forecasts` and `service_forecasts` by `admin_core/intelligence_workers.py::_prediction_forecast_rows`.
4. Prediction actuals are built by `admin_core/intelligence_workers.py::build_prediction_actual_rows` from existing service/channel score rows, bounded decision records, and existing governed prediction feedback fields (`prediction_expected`, `prediction_actual`) when present.
5. Forecasts match actuals by existing row keys: `id`, `channel`, `service`, `target`, `user`, or positional index.
6. The current formula is `prediction_confidence = mean(matched_forecast_accuracy) * mean(forecast_confidence)`, where matched accuracy is `100 - abs(predicted_quality - observed_quality)`.
7. The autonomy gate merges prediction values with `max(candidate_prediction_confidence, outcome_prediction_confidence)` and requires `prediction_confidence >= 70.0`.
8. AUTONOMY.PREDICTION.EVIDENCE.1 production forensics on 2026-06-22 found `forecasts_seen=21`, `prediction_actuals_built=21`, `matched_count=21`, `unmatched_forecasts=0`, `ignored_service_actuals=0`, mean accuracy `98.488`, mean forecast confidence `0.3792`, and outcome prediction confidence `37.351`.
9. The current prediction blocker is not missing matches. The blocker is low forecast/source confidence: accurate predictions are multiplied by low forecast confidence, keeping the result around `37.351` while the gate floor is `70.0`.
10. Current candidate prediction confidence remains `39.6`, so the final autonomy gate remains blocked by `prediction_confidence_too_low`.
11. Raising prediction confidence must use existing evidence owners only: repeated real forecast-to-later-actual comparisons, existing governed prediction feedback, fresher service/quality/trust/blast inputs, existing snapshot refresh, and existing shadow/operator comparison evidence.
12. Synthetic prediction actuals, changed confidence floors, changed prediction formula, new prediction owner, new planner, new governance path, new execution path, or new truth source are forbidden.
13. AUTONOMY.PREDICTION.EVIDENCE.2 implemented the existing-owner lifecycle fix in `admin_core/intelligence_workers.py`: direct governed prediction feedback now becomes prediction actual evidence through the existing `build_prediction_actual_rows` path.
14. Direct prediction feedback is consumed from the full existing decision stream so older feedback can survive refresh/rebuild/reread even when newer non-prediction records fill the bounded tail. Service/channel actuals remain bounded through the existing bounded decision set.
15. Local lifecycle proof in `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_2_EVIDENCE/local_prediction_feedback_lifecycle.json` shows an old existing feedback record outside the 1000-row bounded tail still produces `prediction_actuals_count=1`, `matched_count=1`, `prediction_confidence=88.2`, and survives snapshot write/reread.
16. Production baseline before the fix was still `forecast_rows=21`, `matched_count=21`, `prediction_actuals_count=21`, and `prediction_confidence=36.992`; after safe deploy and snapshot refresh it remained `forecast_rows=21`, `matched_count=21`, `prediction_actuals_count=21`, and `prediction_confidence=36.651`. Current production confidence did not rise because no additional matching direct prediction feedback was present in the refreshed production evidence set.
17. The improvement is evidence durability/consumption, not a formula or floor change. Next safe phase: continue real outcome/source confidence and operator comparison evidence collection; do not enable operator-free autonomy until confidence/trust/prediction/comparison/event-consumer gates pass.
18. Implementation commit: `87ce1986a5b71751ed20fb82dd4b799f505f3928`.
19. AUTONOMY.TRUST.ACCELERATION.1 production inventory after final deploy and snapshot refresh found `forecasts_seen=21`, `forecast_actuals_seen=21`, `service_actuals_seen=21`, `matched_rows=21`, `pending_rows=0`, forecast accuracy `97.194`, and prediction confidence `36.861`.
20. Current prediction acceleration truth: there are no pending forecast rows to match, so adding "missing actuals" cannot raise the current snapshot. The blocker is source/forecast confidence and future real forecast cycles, not missing current matches.
21. The read-only acceleration inventory reports `best_possible_gain_if_5_pending_match=0.0` and `best_possible_gain_if_all_pending_match=0.0` because pending rows are currently zero.
22. Next prediction evidence phase must use existing owners only: fresh service/quality/trust inputs, future forecast-to-later-actual cycles, governed prediction feedback, and snapshot refresh. Formula/floor changes and synthetic actuals remain forbidden.

## AUTONOMY_BLAST_RADIUS_MATERIALIZATION_RULES

1. Blast-radius confidence is calculated by `admin_core/intelligence_platform.py::blast_radius_confidence_model`.
2. Blast-radius evidence rows are built by `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows` and consumed by the `trust-evolution-summaries` snapshot family.
3. A usable blast-radius evidence row requires a known governed outcome and a movement radius derived from existing fields such as `blast_radius`, `affected_users`, `movement_count`, `users_moved`, `selected_move_count`, `target_users`, `users`, `moved_users`, `selected_moves`, or `moves`.
4. Historical governed feedback from BA/small-batch runs contains reusable movement-radius, success, verification, closure, and no-rollback evidence. A prior local rebuild using existing owners classified that evidence into `blast_radius_confidence=100.0` with `blast_radius_evidence_count=2`.
5. Current production autonomy evidence on 2026-06-21 still consumes `blast_radius_confidence=0.0`, so historical blast-radius evidence exists but is not currently materialized into the production consumed autonomy snapshot.
6. This is a materialization/refresh gap, not a reason to create a new blast-radius model, new confidence model, new trust model, new snapshot family, or new truth source.
7. The safe next action is to run the existing production snapshot refresh/materialization path against the correct production feedback stores, then re-read `trust-evolution-summaries` and `/api/operator/autonomous-dry-run`.
8. If production feedback stores lack the historical governed records, new governed evidence may be required; that must still be collected through existing execution, feedback, closure, and snapshot owners only.
9. `GET /api/operator/shadow-autonomy` currently records missing shadow decision rows through `record=true`; strict read-only audits should use `/api/operator/decision-surface` plus the pure `admin_core.shadow_autonomy` decision builder, or explicitly allow that product write.
10. AUTONOMY.REMATERIALIZATION.1 on 2026-06-21 re-ran the current existing builder against saved production governed feedback and again produced 2 usable blast-radius rows: radius `1` and radius `2`, both successful and rollback-free. The resulting existing model output was `blast_radius_confidence=100.0`, `successful_small_operations=2`, and `unsafe_large_operations=0`.
11. Fresh production API capture in AUTONOMY.REMATERIALIZATION.1 still reported `blast_radius_confidence=0.0`, `confidence=39.597`, `trust=39.597`, `prediction_confidence=39.6`, `apply_executed=false`, and `users_moved=0`.
12. If only blast-radius confidence becomes visible as `100.0`, estimated trust rises to about `54.698`, but the `70` trust floor still does not pass and autonomy remains `NOT_READY`.
13. Existing `tools/v7-intelligence-snapshot-refresh` supports the required feedback inputs and has a `--dry-run` mode; refresh writes intelligence snapshots only and must not move users or enable autonomy.
14. AUTONOMY.REMATERIALIZATION.2 on 2026-06-21 executed the existing production-supported path `/api/actions/planner-refresh-dry-run`, which runs `v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh`.
15. The refresh was safe: `apply_executed=false`, `user_movement_performed=false`, `routing_mutation_performed=false`, `users_moved=0`, and `runtime_mutation_scope=intelligence_snapshot_refresh_only`.
16. The refresh regenerated `trust-evolution-summaries` (`generated_at` changed from `2026-06-21T17:48:03.651484+00:00` to `2026-06-21T17:48:12.525206+00:00`) but had no metric effect: `blast_radius_confidence` stayed `0.0`, trust stayed `39.602`, confidence stayed `39.602`, and prediction stayed `39.6`.
17. The `blast_radius_records` source hash after refresh equals `sha256_json([])`, so the production consumed snapshot still contains no blast-radius rows. The standard production refresh path alone did not recover historical BA evidence.
18. AUTONOMY.REMATERIALIZATION.3 on 2026-06-22 certified the root cause as `BLAST_RECORDS_IN_DIFFERENT_STORE`.
19. The active production default refresh paths `/opt/v7/egress/state/execution-events.jsonl`, `/opt/v7/egress/state/runtime-trust.jsonl`, `/opt/v7/egress/state/proposal-records.jsonl`, `/opt/v7/egress/state/proposals.jsonl`, and `/opt/v7/egress/state/closure-records.jsonl` exist but currently contain 0 records, so standard refresh gives the builder no governed movement/outcome rows.
20. Historical governed blast-radius evidence still exists in production rotated stores such as `/opt/v7/egress/state/execution-events.jsonl.1`, `/opt/v7/egress/state/runtime-trust.jsonl.1`, `/opt/v7/egress/state/closure-records.jsonl.1`, and `/opt/v7/egress/state/proposal-records.jsonl.1`.
21. The current existing builder classifies those rotated production records without code changes: combined rotated `.jsonl.1` inputs produce 11 valid blast-radius rows. Therefore this is not a schema mismatch, not a builder/model failure, and not a reason to create a new model.
22. The safe recovery path is an approved use of existing archive restore/materialization or snapshot rebuild/refresh capability against real rotated feedback inputs. Manual trust snapshot editing, synthetic evidence, and runtime apply remain forbidden.
23. AUTONOMY.REMATERIALIZATION.4 on 2026-06-22 previewed recovery without writes. A strict refresh-equivalent run with rotated feedback inputs still produced `blast_radius_confidence=0.0` because the useful rotated rows did not become visible in the final bounded trust-evolution decision set.
24. The same phase previewed the existing trust model with the 11 builder-classified rotated blast rows supplied as visible `blast_radius_records`. That moved `blast_radius_confidence` from `0.0` to `100.0`, `overall_confidence` from `42.678` to `59.345`, and operator trust from `39.602` to `54.684`.
25. Blast recovery has moderate readiness impact but does not certify autonomy: confidence remains `45.8`, trust remains below the `70.0` floor at `54.684`, and prediction confidence remains `39.6`.
26. After visible blast recovery, the dominant remaining blocker is `prediction_confidence_too_low`; confidence remains a second blocker. The next evidence phase is `AUTONOMY.PREDICTION.EVIDENCE.1`.
27. AUTONOMY.FINAL.BRANCH_1 on 2026-06-22 closed the blast planning branch with immediate production recovery `NO-GO`.
28. Immediate recovery is blocked because the current as-is refresh/materialization paths can still leave `blast_radius_confidence=0.0`: `build_trust_evolution_snapshot` constructs `decision_records = audit_records + switch_records + rollback_records`, then uses `decision_records[-1000:]`. Current large `switch-history` can push restored feedback rows out of the consumed tail.
29. Existing refresh only is rejected as ineffective because active stores are empty. Existing execution-feedback materialization is rejected as an immediate path because active feedback rows can still be ordered before switch history and filtered out. Existing archive restore is useful as a real evidence source but is not sufficient alone.
30. Recommended recovery owner remains the existing snapshot rebuild/refresh owner, but it needs one visibility step: feed existing builder-classified blast rows into `trust_evolution_summary` as visible `blast_radius_records`, or equivalently fix existing-owner ordering/bounding so real feedback rows survive into the consumed trust-evolution snapshot.
31. This visibility step must not create a new planner, governance path, execution path, trust source, confidence model, or synthetic evidence. It is an existing-owner correction before any snapshot-only recovery write.
32. Exact next phase: `AUTONOMY.FINAL.BRANCH_1A_BLAST_VISIBILITY_OWNER_FIX_AND_DRY_RUN`.
33. Last verified commit: `5011d253e2bb0a11753d25a7487902ee528f84c1`.
34. AUTONOMY.FINAL.BRANCH_1A implemented the existing-owner visibility fix in `admin_core.intelligence_workers.build_trust_evolution_snapshot`.
35. The fix keeps general outcome mappers bounded by `bounded_decisions = decision_records[-MAX_HISTORY_RECORDS:]`, but builds `blast_radius_records` from the full existing `decision_records` stream before shared tail bounding can hide older governed feedback.
36. Production-data dry-run with the patched existing owner and real rotated `.jsonl.1` inputs produced `blast_radius_evidence_count=11`, `blast_radius_confidence=100.0`, `trust_evolution_overall_confidence=59.358`, `prediction_confidence=37.37`, `users_moved=0`, and `snapshot_written=false`.
37. Blast Branch acceptance passed: blast evidence count is nonzero, blast confidence is nonzero, evidence originates from real production governed records, no synthetic evidence was created, and existing owners only were used.
38. Blast Branch status is now `CLOSED`. Production autonomy is not enabled and still remains blocked by confidence, trust, prediction confidence, and operator comparison evidence.
39. AUTONOMY.FINAL.BRANCH_1B on 2026-06-22 deployed Branch 1A through the existing approved `tools/v7-safe-deploy` flow. Local, GitHub, and runtime are aligned at `c4adc537b39e0335ad9cc0cf7ff9589d85860d60`; final truth is `PASS` and final convergence is `ALIGNED`.
40. The approved production recovery write used the existing `/usr/local/bin/v7-intelligence-snapshot-refresh` owner with real rotated production stores: `execution-events.jsonl.1`, `runtime-trust.jsonl.1`, `proposal-records.jsonl.1`, `proposals.jsonl.1`, and `closure-records.jsonl.1`.
41. The recovery write was snapshot-only: `runtime_behavior_changed=false`, `governance_behavior_changed=false`, `users_moved=false`, `apply_executed=false`, and no daemon/autoswitch was enabled.
42. Production consumed autonomy metrics after recovery: `blast_radius_evidence_count=11`, `blast_radius_source_record_count=3372`, `blast_radius_confidence=100.0`, `trust_score=54.684`, `confidence_score=39.578`, `prediction_confidence=37.312`, `rollback_confidence=100.0`, `execution_allowed_now=false`, and `users_moved=0`.
43. Blast Branch status is now `OPERATIONALLY_CLOSED`. Blast recovery is no longer the dominant blocker.
44. Production autonomy remains blocked by `confidence_too_low`, `trust_too_low`, and `prediction_confidence_too_low`. The next safe phase is `AUTONOMY.PREDICTION.EVIDENCE.2_REAL_OUTCOME_CONFIDENCE_COLLECTION`; operator comparison evidence remains a parallel P1 track.
45. Last verified commit: `c4adc537b39e0335ad9cc0cf7ff9589d85860d60`.

## AUTONOMY_TRUST_BUILDOUT_RULES

1. AUTONOMY.TRUST.BUILDOUT.1 on 2026-06-22 re-read production using `/api/operator/autonomous-dry-run`, `/api/operator/decision-surface`, and a read-only local shadow model built from the decision surface.
2. No runtime apply, user movement, daemon enablement, autoswitch enablement, threshold change, floor change, synthetic evidence, manual snapshot edit, new planner, new governance path, new execution path, or new truth source occurred.
3. Fresh current consumed dry-run values were `candidate_count=1`, `execution_allowed_now=false`, `users_moved=0`, final confidence `45.8`, trust `39.582`, final prediction confidence `39.6`, outcome prediction confidence `37.343`, rollback confidence `100.0`, and blast-radius confidence `0.0`.
4. The fresh consumed values differ from the Branch 1B post-recovery evidence where production consumed blast-radius confidence was `100.0` and trust was `54.684`.
5. Canonical interpretation: Branch 1B blast recovery was proven and remains closed, but the currently consumed default autonomy dry-run does not durably preserve recovered blast evidence. This is a trust durability gap, not a reason to reopen blast model discovery.
6. The next trust phase must make existing recovered blast evidence durable under the normal existing snapshot/refresh owner before canary readiness can be considered.
7. Current operator comparison reality from read-only shadow build: 27 decisions, 0 comparisons, agreement rate `0.0`, average decision confidence `45.828`, and earned confidence `45.828`.
8. With the current shadow formula, the practical operator-comparison target is about 9 all-agree comparisons, 11 comparisons at 90% agreement, 15 at 80%, or 17 at 75% to reach earned confidence near or above `70.0`. The formal minimum comparison count remains 5, but that alone is unlikely to reach the earned-confidence floor.
9. Current prediction path remains healthy but under-confident: matching works, forecast accuracy was previously about `98.5`, and the blocker is low forecast/source confidence. Estimated future evidence need is about 23 perfect matched actuals or about 35 high-quality 90% matched actuals to approach the `70.0` floor.
10. Trust buildout order is: `AUTONOMY.TRUST.DURABILITY.1` -> `OPERATOR.COMPARISON.COLLECTION.1` -> `AUTONOMY.PREDICTION.EVIDENCE.2` -> `EVENT.CONSUMER.READONLY.2` -> `AUTONOMY.CANARY.1_READINESS_RECHECK`. EVENT.CONSUMER.READONLY.2 is complete as a read-only consumer certification.
11. AUTONOMY.TRUST.BUILDOUT.1 final verdict is `AUTONOMY_TRUST_PATH_PARTIAL`.
12. Last verified commit: `6b0c72f4157d5e4cb57db864d0bcd73b593f4fe0`.

## AUTONOMY_TRUST_DURABILITY_RULES

1. AUTONOMY.TRUST.DURABILITY.1 on 2026-06-22 implemented the certified root-cause fix for recovered blast evidence durability.
2. Root cause: normal `tools/v7-intelligence-snapshot-refresh` consumed active JSONL paths only, while real governed recovery evidence could live in rotated numeric store-family files such as `execution-events.jsonl.1`.
3. Current rule: normal snapshot refresh must consume the existing JSONL family, not only the active file. The family order is oldest numeric rotation to newest active file, for example `execution-events.jsonl.2` -> `execution-events.jsonl.1` -> `execution-events.jsonl`.
4. This is not a new truth source. Numeric rotations are part of the same existing evidence store family.
5. The implemented owner is `tools/v7-intelligence-snapshot-refresh`; it now expands JSONL family reads for audit inputs, feedback inputs, switch history, and rollback history.
6. Automated durability tests prove that recovered blast evidence survives refresh, rebuild, snapshot write, and reread while bounded decision processing remains at `MAX_HISTORY_RECORDS`.
7. Local verification evidence: `docs/reports/AUTONOMY_TRUST_DURABILITY_1_EVIDENCE/local_rotated_family_durability.json`.
8. Verified local lifecycle metrics: after refresh/rebuild/reread, `blast_radius_confidence=100.0`, `blast_radius_evidence_count=1`, `blast_radius_source_record_count=1001`, and `bounded_decision_count=1000`.
9. Production deploy and snapshot refresh also verified the fix: deploy id `deploy-z8-14-Updatesystem-29b980c-20260623T000551`, `blast_radius_confidence=100.0`, `blast_radius_evidence_count=11`, `blast_radius_source_record_count=4407`, `bounded_decision_count=1000`, `successful_small_operations=9`, and `unsafe_large_operations=0`.
10. No runtime apply, user movement, daemon enablement, planner change, governance change, execution change, threshold change, floor change, formula change, synthetic evidence, or new truth source occurred.
11. Branch 1B remains the production proof point for 11 real recovered rows and trust `54.684`; AUTONOMY.TRUST.DURABILITY.1 makes that class of recovered evidence durable under normal refresh code behavior.
12. Remaining autonomy blockers still stand: trust floor, prediction confidence, operator comparison evidence, readiness recheck, and disabled daemon/autoswitch runtime. Live event consumer certification is complete in read-only mode only.
13. AUTONOMY.TRUST.DURABILITY.1 final verdict is `TRUST_DURABILITY_FIXED`.
14. Last verified commit: `29b980c00a11097332eaad53a2c1fe2f77d2389d`.
15. AUTONOMY.TRUST.ACCELERATION.1 final production canary proximity after refresh: confidence `39.606`, trust `54.704`, prediction confidence `36.861`, operator earned confidence `45.802`; all remain below the `70.0` floor.
16. `AUTONOMY.CANARY.1` is not ready. Missing floor set is `confidence`, `trust`, `prediction_confidence`, and `operator_earned_confidence`.
17. AUTONOMY.CANARY.1D added read-only floor forensics and materialization audit to the existing `admin_core/autonomy_trust_acceleration.py` / `tools/v7-autonomy-trust-evidence-inventory` owner.
18. Production after deploy `2915a4b8107d1fbd416661e562511a6ca2a864fe` reports floor values: confidence `37.402`, trust `53.051`, prediction confidence `33.753`, and secondary operator earned confidence `45.908`; all remain below the `70.0` floor.
19. The confidence floor is low because it is currently derived from decision `50.0`, service `36.079`, and suitability `26.126`. Blast and rollback are both `100.0`, but they do not close the current confidence floor.
20. The trust floor is low because it is currently derived from decision `50.0`, service `36.079`, suitability `26.126`, and blast `100.0`; the result remains `53.051`, below floor.
21. The prediction floor is low even though actual matching is complete: production has `21` forecasts, `21` actuals, `21` matched rows, `0` pending rows, forecast accuracy `94.786`, and mean forecast confidence `0.3561`. Root cause is `low_forecast_source_confidence`, not missing current actuals.
22. The service floor is low because service rows are matched but low-confidence: `21` rows, mean correctness `100.0`, mean row confidence `0.361`, and service confidence `36.079`.
23. The suitability floor is low because candidate outcome evidence is present but incomplete and low-confidence: `156` candidates, `83` outcomes, sampled rows include `8` without outcome, mean candidate confidence `0.372`, mean correctness `64.395`, and suitability confidence `26.126`.
24. Current safe materialization audit says prediction actuals, service actuals, and candidate outcomes are consumed by existing owners; there is no safe immediate fix that can raise floors without new real evidence. Synthetic prediction actuals, synthetic candidate outcomes, synthetic operator comparisons, threshold/formula changes, runtime apply, and user movement remain forbidden.
25. Next safe evidence phase: collect real higher-confidence service/channel probe cycles and real governed/manual outcome closure through existing owners, then refresh snapshots and re-read the canary floors. `AUTONOMY.CANARY.1` remains blocked.

## 1. Channels

- What it means: A channel is an egress path that can carry users, be inspected by operators, and be considered by the planner.
- Source of truth: Channel registry/runtime channel state, operator decision surface, service matrix, route/runtime readiness, planner assignment truth.
- Where it is calculated: `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch`, and channel helper functions in `admin/v7-admin-api`.
- Where it is displayed: Admin Channels table, Channel Drawer, Attention/Overview derived surfaces, technical diagnostics.
- What affects it: Registry flags, manual/reserve/canary role, service checks, stability, capacity/load, route readiness, runtime readiness, history, assigned users, planner gates.
- What does NOT affect it: Cosmetic UI labels, screenshots, operator-facing health score alone, or raw trust labels alone.
- Operator meaning: "Can this channel be used, should users stay, what is wrong, and what action is safe?" Operator wording must avoid vague "needs check" language. When evidence is incomplete, use reality-first wording that states the current reality and next step, such as "fresh data unavailable", "open service matrix", "open users", "open logs", "automatic refresh pending", or "safe action unavailable".
- Engineer meaning: Aggregated runtime/planner/read-model state for one egress object.
- Known caveats: Some roles such as Keep Only or Blocked may not appear in production screenshots if live data currently has no channel in that state.
- Related reports / ADRs: `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `CHANNEL_TRUTH_4_CHANNEL_ROLE_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, ADR-004.
- Last verified commit: `8ba2178f`.

## 2. Channel Decision V7

- What it means: The operator-facing decision for a channel: Use, Evacuate, Keep Current Users, Emergency Only, or Blocked.
- Source of truth: Existing planner/assignment truth and channel role flags, not a separate UI score.
- Where it is calculated: `tools/v7-users-autoswitch` candidate/blocker/selected-move logic and adapter code in `admin_core/operator_decision_surface.py` plus channel decision helpers in `admin/v7-admin-api`.
- Where it is displayed: Primary Channel table column and Channel Drawer first screen. The Channel Drawer first screen is Decision-first: drawer header channel identity → Decision → Reason → Signals → Problems → one collapsed Engineer Diagnostics entry, with no duplicate channel label and no score or technical health above the decision.
- What affects it: Selected moves, eligible candidates, blockers, current users, `manual_only`, `reserve_only`, canary reservation, disabled/quarantine/maintenance, service/route/speed/stability/load/policy gates.
- What does NOT affect it: Channel Score by itself, old TRUSTED/WATCH/QUARANTINED labels, or raw engineering health labels.
- Operator meaning: "What does V7 want me to do with this channel?" `Use` means V7 can use the channel under current planner/assignment evidence; it does not mean fastest, best, warning-free, or unlimited capacity. `Emergency Only` means the channel is role/policy restricted for manual, reserve, canary, or execution-only use; it does not mean technically broken.
- Engineer meaning: A read-only projection of planner assignment/retention/evacuation truth into operator language.
- Known caveats: If the planner cannot produce a role because data is absent, UI must show the safest truthful state rather than inventing eligibility. A channel can be `Use` while capacity/load is at warning or hard-full for new assignments; the decision must be read together with blocker/load details. Operator labels are locked as understandable terms: `Use`, `Keep Current Users`, `Evacuate`, `Emergency Only`, and `Blocked` / `Запрещён`; compact table labels may use Russian equivalents such as `Использовать`, `Оставить текущих`, `Перевести`, `Только аварийно`, `Запрещён`. `Загрузка решения` is an allowed transient loading state before assignment truth arrives; it is not a sixth planner decision and must not be counted as `Blocked`.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, ADR-009.
- Last verified commit: `2fb9d205`.

## 3. Channel Score

- What it means: A technical/mixed health score from 0 to 100 that explains channel condition; it is not assignment truth.
- Source of truth: Existing `channelSuitability(source)` model and its component breakdown.
- Where it is calculated: `admin/v7-admin-api` functions `channelSuitabilityServices`, `channelSuitabilityStability`, `channelSuitabilityCapacity`, `channelSuitabilityRoute`, `channelSuitabilityRuntime`, `channelSuitabilityHistory`, and `channelSuitability`.
- Where it is displayed: Diagnostics metadata and optional technical surfaces. Channel Drawer first screen must not display `score/100`; diagnostics must present reality-first explanations rather than score-first point math.
- What affects it: Services, stability, capacity, route/topology, runtime/readiness, and history components.
- What does NOT affect it: Planner assignment eligibility directly, emergency/manual role policy directly, or whether V7 should move current users.
- Operator meaning: "What real technical signals explain the channel condition?"
- Engineer meaning: A mixed diagnostic score useful for explanation and troubleshooting, separate from planner hard gates.
- Known caveats: A high score can coexist with Do Not Assign/Emergency Only/Evacuate if planner gates or role flags block assignment. A capacity reduction inside the score means user-assignment pressure against limits, not bandwidth saturation or speed failure. Operator diagnostics must not lead with point loss, component contribution, score penalty language, or vague "requires verification" wording.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_SUITABILITY_1_PLANNER_DERIVED_SUITABILITY_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`, ADR-002, ADR-009, ADR-010.
- Last verified commit: `2fb9d205`.

## 4. Technical Health

- What it means: A diagnostics-only reality explanation of what contributes to technical channel condition.
- Source of truth: Existing channel suitability breakdown and evidence/read models.
- Where it is calculated: `admin/v7-admin-api` channel suitability functions and reality-first diagnostics rendering.
- Where it is displayed: Nested technical diagnostics inside the Channel Drawer, not as a primary workflow.
- What affects it: Score components, fresh service/route/runtime evidence, stability/capacity/history inputs.
- What does NOT affect it: Operator action flow directly, assignment decision directly, or governance approval.
- Operator meaning: "What is really happening with services, stability, load, route readiness, runtime, and history?" Technical health can be good while assignment is Emergency Only, Keep Only, or load-limited. Diagnostics may use component status language such as `OK`, `Нет свежих данных`, and `Проблема`, then explain observed reality; first-screen operator wording must stay concrete and action-oriented.
- Engineer meaning: Component-level diagnostic view over the existing score inputs, rendered as observed reality instead of point math.
- Known caveats: Health must not reintroduce action/resolution language as first-line operator truth. Diagnostics may point to missing evidence but should not become a separate execution path. Diagnostics must not explain via lost points, penalties, score contribution, or generic "needs check" wording. Table-level "Healthy" is narrower than technical health: it requires a usable/keep assignment posture and no red first-level operator signal.
- Related reports / ADRs: `docs/operator_actions/CHANNEL_HEALTH_SCREEN_EXISTENCE_AUDIT.md`, `docs/operator_actions/CHANNEL_HEALTH_2_DIAGNOSTICS_ONLY_IMPLEMENTATION_REPORT.md`, `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`, ADR-003, ADR-009, ADR-010.
- Last verified commit: `2fb9d205`.

## 5. Route

- What it means: Route reality/readiness for user/channel traffic, including route status, direct/RU route checks, mismatch/leak risk, and topology signals.
- Source of truth: Runtime route read models and route reality helpers.
- Where it is calculated: `admin_core/route_reality_views.py`, `admin_core/route_views.py`, `admin/v7-admin-api` route status/readiness functions, and planner route gates in `tools/v7-users-autoswitch`.
- Where it is displayed: Routes surface, User Drawer, Channel Drawer diagnostics, Attention items when route risk exists.
- What affects it: Runtime route tables, policy routing, direct/RU route state, route evidence freshness, channel topology, planner route gates.
- What does NOT affect it: Channel Score alone, UI ordering, or manual labels.
- Operator meaning: "Is traffic going where it should, and is there a safety/leak problem?" In Channel diagnostics, route wording means readiness/topology confidence. It must not imply speed, bandwidth, latency, packet loss, or traffic quality unless route evidence explicitly shows a real route problem.
- Engineer meaning: Read-only runtime route evidence and planner gate input.
- Known caveats: Route validation is primarily diagnostic/status until a safe existing action exists; it must not imply unsafe execution. Channel UI should say "route readiness/confidence incomplete" rather than "route broken" unless runtime route evidence actually shows mismatch or leak risk.
- Related reports / ADRs: `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 6. Capacity

- What it means: Assignment/load posture for a channel or pool: current and projected users compared with configured soft, hard, and failover-hard limits. Capacity answers whether V7 may add users, should pause additions, or must treat a channel as full for planned/failover movement.
- Source of truth: Egress registry capacity fields (`capacity_users`, `soft_limit`, `hard_limit`), live assigned user counts, policy load settings, dynamic load summary, planner capacity/load gates, and capacity readiness tools.
- Where it is calculated: `tools/v7-users-autoswitch` `_load_policy`, `_healthy_for_load`, `_dynamic_load_summary`, `_load_limits_for_egress`, `_capacity_status`, `_capacity_decision`, `_gate_load`; `admin/v7-admin-api` `channelSuitabilityCapacity`, `channelLoad`, `loadPosture`, capacity read/preview helpers; runtime support tools `v7-capacity-check` and `v7-capacity-readiness`.
- Where it is displayed: Channel table Load/Capacity signal, Channel Drawer diagnostics, score explanation, execution preview/gates, overview Load card, global capacity/readiness summaries.
- What affects it: Current users assigned to an egress, projected users after movement, explicit per-egress limits, dynamic load policy, healthy working pool size, reserve ratio, soft/hard/failover multipliers, failover capacity multiplier, min/max limits, role flags that remove channels from normal working pool, and planner purpose (`current`, `planned`, `failover`).
- What does NOT affect it: CPU usage, bandwidth saturation, traffic volume, raw speed complaint alone, raw service success alone, cosmetic UI ordering, screenshots, or the mixed Channel Score by itself.
- Operator meaning: `Load OK` means the channel is within assignment limits. `Soft Full` / warning means the channel is near or at the soft limit and new additions require capacity/headroom evaluation. `Hard Full` / "on limit" means new planned assignments are restricted; current users are not automatically failing. `Overloaded` means failover-hard capacity was reached and is a stronger emergency load state. Operator copy should explain preferred assignment level, hard assignment limit, assignment restriction, and why current users may still work.
- Engineer meaning: Planner/gate input that bounds movement, affects ranking, can block planned/failover candidates, and prevents broad unsafe switching.
- Known caveats: Capacity/load is not speed quality and not traffic saturation. A channel can have good speed/stability and still be hard-full because too many users are assigned relative to policy. Production evidence on 2026-06-18 showed `vless` and `awg3` as technically usable/currently retained while load was hard-full for assignment. Global IP capacity readiness (`capacity_plan`) is a separate pool/readiness check and can fail independently from per-channel assignment load. Prefer "assignment limit reached" over "channel overloaded" when the operator might confuse load with internet quality.
- Related reports / ADRs: `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `docs/capacity_2/CAPACITY_2_OBSERVED_CAPACITY_MODEL_REPORT.md`, `docs/track7/productization/e35_0_1-audit/capacity-policy-audit.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, ADR-009, ADR-011.
- Last verified commit: `2fb9d205`.

## 6A. Observed Capacity Shadow

- What it means: A future shadow/advisory model that learns practical channel capacity from observed quality at different assigned-user levels. It asks: "At what user count does this channel begin to degrade in measured reality?"
- Source of truth: Derived evidence only from existing assigned-user counts, service matrix, quality summary windows, runtime readiness, route readiness, and history. It is not an active runtime truth source.
- Where it is calculated: Not implemented as runtime behavior in CAPACITY.2. Future implementation should reuse read-only patterns from `tools/v7-egress-quality-compact`, `admin_core/intelligence_workers.py`, and `admin_core/shadow_autonomy.py`.
- Where it is displayed: Not currently displayed as an active operator/planner decision. Future display should be advisory only until separately approved.
- What affects it: Assigned-user count, service failures, fail rate, p95 latency, avg/min Mbps, stability, runtime readiness, route readiness, historical trend, sample freshness, and confidence.
- What does NOT affect it: It must not directly affect planner eligibility, selected moves, autoswitch, governance, runtime execution, or existing `soft_limit`, `hard_limit`, and `capacity_users` values.
- Operator meaning: "V7 is learning whether this channel remains stable as users increase." It is not permission to move users and not proof of physical bandwidth.
- Engineer meaning: A snapshot-only learning/advisory layer for practical capacity under third-party or partially owned tunnel constraints.
- Known caveats: Current production evidence proves V7 can observe users and quality together, but does not yet prove causal capacity curves. Observed Capacity Shadow must remain observe/learn/recommend until a future governed program certifies planner integration.
- Related reports / ADRs: `docs/capacity_2/CAPACITY_2_OBSERVED_CAPACITY_MODEL_REPORT.md`, `docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md`, `docs/capacity_2/DATA_GAP_ANALYSIS.md`, ADR-011.
- Last verified commit: `67fbd850`.

## 7. Service Matrix

- What it means: Per-service reachability/health diagnostics for channels/services.
- Source of truth: Existing service matrix refresh/test outputs and admin service matrix read models.
- Where it is calculated: Runtime tools `v7-service-matrix-refresh-all` and `v7-service-matrix-test`; admin rendering helpers in `admin/v7-admin-api`.
- Where it is displayed: Checks, Channel Drawer service details, diagnostics, Attention item source when service failure affects users.
- What affects it: Service test results, freshness, channel availability, runtime check outputs.
- What does NOT affect it: It does not by itself execute user movement, bypass governance, or replace planner eligibility.
- Operator meaning: "Which services work on this channel and what needs re-checking?"
- Engineer meaning: Measurement/diagnostic input consumed by UI and planner gates.
- Known caveats: Service Matrix is diagnostic/background automation, not a standalone business action. Manual refresh is allowed only through existing safe actions. First-level channel Services should track primary user-facing services; hidden endpoint checks such as auth/API companion endpoints remain supporting diagnostics unless they become explicit planner blockers.
- Related reports / ADRs: `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_2_OPERATOR_SURFACE_SIMPLIFICATION_REPORT.md`, `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 8. Stability

- What it means: Whether channel behavior is steady enough for assignment/retention, including interface/runtime availability and speed stability floors.
- Source of truth: Planner gates, runtime/channel evidence, suitability stability component.
- Where it is calculated: `tools/v7-users-autoswitch` quality/stability gates and `admin/v7-admin-api` channel stability/suitability helpers.
- Where it is displayed: Channel diagnostics, assignment blocker language, score explanation, Attention/Channel Drawer when it becomes a problem.
- What affects it: Interface up/down, missing interface, stability floor, speed samples, quality history.
- What does NOT affect it: Human-readable labels alone or decorative UI state.
- Operator meaning: "Is this channel stable enough to trust for users?"
- Engineer meaning: Hard/soft quality gate and score component.
- Known caveats: Raw labels such as `interface_down_or_missing` must be translated into operator language.
- Related reports / ADRs: `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_SUITABILITY_3_FINAL_CHANNEL_UI_POLISH_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 9. Runtime Readiness

- What it means: Whether runtime state and evidence are present/readable enough for V7 to trust or act on a decision.
- Source of truth: Runtime read adapters, execution readiness/gates, runtime convergence checks, planner stop conditions.
- Where it is calculated: `admin_core/runtime_read_views.py`, `admin/v7-admin-api` `egress_runtime_readiness`, `admin_core/operator_execution_pipeline.py`, and `tools/v7-users-autoswitch`.
- Where it is displayed: Operator Center, Channel/User detail surfaces, execution preview, diagnostics, truth/convergence status.
- What affects it: Runtime file availability, registry readability, restore barrier, execution packet validity, governance gates, runtime/repo convergence.
- What does NOT affect it: Static documentation, UI score alone, or local code state without runtime verification.
- Operator meaning: "Is V7 ready and safe enough to trust this action/status?"
- Engineer meaning: Runtime safety/readability contract for planner and execution surfaces.
- Known caveats: Runtime readiness can block or downgrade action even when UI health looks good.
- Related reports / ADRs: `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`, `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 10. History

- What it means: Past channel/user/runtime evidence used to explain trust, recovery, failures, and score/history components.
- Source of truth: Existing logs/evidence, intelligence snapshots, planner history/failure inputs.
- Where it is calculated: `admin_core/intelligence_platform.py`, `admin_core/intelligence_snapshots.py`, `tools/v7-users-autoswitch`, admin evidence/history views.
- Where it is displayed: Evidence/history/technical sections, not first-screen operator answers.
- What affects it: Failure history, recovery state, past measurements, audit events, intelligence snapshots.
- What does NOT affect it: It does not create a new truth source or new operator workflow by itself.
- Operator meaning: "What happened before, and does it explain this state?"
- Engineer meaning: Evidence trail and historical signal for diagnostics/planner decisions.
- Known caveats: History is useful after problem selection; it should not become top-level attention noise without another current problem source.
- Related reports / ADRs: `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/CHANNEL_UX_3_PROBLEM_CAUSE_SEPARATION_REPORT.md`, `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 11. Planner

- What it means: The existing autoswitch/planning authority that evaluates candidates, blockers, selected moves, retention, evacuation, ranking, and execution readiness inputs.
- Source of truth: `tools/v7-users-autoswitch` and its read-only surfaces/adapters.
- Where it is calculated: Candidate/blocker/gate functions in `tools/v7-users-autoswitch`, with operator projections in `admin_core/operator_decision_surface.py`.
- Where it is displayed: Operator decision surface, Channel Decision V7, recommendations, execution previews, Attention items.
- What affects it: Channel registry, user state, service/route/speed/stability/capacity/policy gates, cooldown/freeze, restore barrier, governance, current users.
- What does NOT affect it: Channel Score alone, UI rearrangement, screenshots, or standalone labels.
- Operator meaning: "What does V7 recommend or block, and why?"
- Engineer meaning: Existing decision pipeline and safety gate authority.
- Known caveats: Planner read-only outputs are not the same as applying execution. Apply remains governed. Admin action wrappers may expose a successful dry-run `rc=0` while returning only a truncated stdout tail; when exact `candidate_moves_total` matters, prefer a full CLI JSON capture or a normalized endpoint that preserves the parsed plan.
- Related reports / ADRs: `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md`, ADR-EVENT-DRIVEN-AUTONOMY.
- Last verified commit: `f875eeee`.

## 12. Assignment

- What it means: Whether V7 can assign new users to a channel, keep current users, evacuate users, or restrict the channel to emergency/manual use.
- Source of truth: Planner assignment eligibility, selected moves, blockers, channel role flags, and current user counts.
- Where it is calculated: `tools/v7-users-autoswitch` `_candidate`, `_block`, `_gate_*`, `_select_moves`, `_candidate_json`; adapter projection in `admin_core/operator_decision_surface.py` and channel decision helpers.
- Where it is displayed: Channel table decision column, Channel Drawer first screen/details, Attention Layer when action is needed.
- What affects it: Eligibility candidates, blockers, selected moves away, current users, manual/reserve/canary flags, disabled/quarantine states, policy and runtime gates.
- What does NOT affect it: Technical Health/Score alone or old trust labels.
- Operator meaning: "Can V7 use this channel, must users leave, or is it restricted?"
- Engineer meaning: Planner-derived role projection over existing channel/user truth.
- Known caveats: Quality and assignment can intentionally disagree. The UI must make the decision primary and health secondary. A channel can be technically READY and still hard-full for assignment; hard-full alone does not mean current users are broken or must move immediately.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md`, ADR-002, ADR-EVENT-DRIVEN-AUTONOMY.
- Last verified commit: `f875eeee`.

## 13. Users

- What it means: V7 customer/user objects with identity, profile, connection, route, channel, status, and operator actions.
- Source of truth: Existing user registry/identity data, runtime/user status, recommendations, why cards, route and profile state.
- Where it is calculated: Admin user surfaces in `admin/v7-admin-api`, user decision rows in `admin_core/operator_decision_surface.py`, explainability adapter, existing profile/identity handlers.
- Where it is displayed: Users table, User Drawer, Overview/Attention, Operator Center/recommendation details.
- What affects it: Profile issuance, connection status, assigned channel, route status, speed complaint/checks, phone confirmation, policy/group access, recommendations.
- What does NOT affect it: Channel score alone, unrelated channel diagnostics, or hidden technical evidence without a user-facing problem.
- Operator meaning: "Who is this, is there a problem, why, and what should I do?"
- Engineer meaning: User-centered projection of registry/runtime/profile/route/planner evidence.
- Known caveats: The current canonical reference focuses heavily on channel work because recent audits concentrated there. Deeper user lifecycle details may require a future dedicated audit.
- Related reports / ADRs: `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md`, `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 14. Groups / Policies

- What it means: Organizational/group policy and access settings that constrain what users/channels/actions are allowed.
- Source of truth: Existing policy settings, identity/group data, org policy gates, execution policy adapters.
- Where it is calculated: Policy settings and group/organization UI in `admin/v7-admin-api`, policy gates in `tools/v7-users-autoswitch`, execution policy adapters in `admin_core/operator_execution_pipeline.py`.
- Where it is displayed: Users/Organizations, Settings/Policy, Execution drawer, policy/domain panels.
- What affects it: Organization, group, access policy, autoswitch mode, quality thresholds, load limits, cooldowns, route/service rules.
- What does NOT affect it: Operator UI preference, raw health score alone, or report text without live policy/config.
- Operator meaning: "Is this user/action allowed under current policy?"
- Engineer meaning: Constraint layer that planner and execution must honor.
- Known caveats: UNKNOWN - requires future audit for a full canonical group/policy contract beyond the current channel/operator work.
- Related reports / ADRs: `docs/phase5/POLICY_BASED_ACCESS.md`, `docs/phase5/MULTITENANT_MODEL.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 15. Autonomy

- What it means: Read-only intelligence/shadow/automation support plus governed execution certification that may recommend, simulate, monitor, or prepare bounded action, but must not create an independent execution path.
- Source of truth: Existing shadow autonomy, intelligence platform, operator execution pipeline, governed execution path.
- Where it is calculated: `admin_core/shadow_autonomy.py`, `admin_core/intelligence_platform.py`, `admin_core/operator_execution_pipeline.py`, `admin_core/operator_execution.py`, `admin_core/operator_execution_feedback.py`, planner tools.
- Where it is displayed: Operator Center, execution readiness, attention/overview summaries, evidence/details.
- What affects it: Planner signals, channel/service regression, safety gates, governance state, intelligence snapshots, execution readiness, restore barrier state, rollback readiness, feedback/learning evidence.
- What does NOT affect it: It does not bypass approval, restore barriers, governance, rollback, feedback, truth/convergence, or existing execution handlers. It must not move users merely because a timer fired.
- Operator meaning: "V7 can surface what needs attention, and can prepare governed action, but dangerous changes remain guarded until an event-driven chain is ready."
- Engineer meaning: Derived intelligence and governed automation layer over existing truth and execution owners.
- Known caveats: Continuous production autonomy daemon is not active as of POOL.3/EVENT.1/AUTONOMY.ROOT. Truth says `autoswitch_scheduler_active=false` and `autoswitch_service_active=false`. EVENT.1 proved the current read-only chain can preview planner/packet/restore/rollback/feedback/learning surfaces but must stop because confidence/trust/prediction floors fail, operator comparison evidence is below floor, restore barrier readiness is blocked, and no live event consumer is certified. AUTONOMY.ROOT clarified that BA evidence is consumed and raises governed inherited execution trust, but does not close operator-free autonomy trust. AUTONOMY.SOURCE_CONFIDENCE.REALITY.AUDIT deployed `confidence_reality_audit` in the existing read-only trust inventory. AUTONOMY.REAL_OUTCOME_COLLECTION_AND_CONFIDENCE_GROWTH then deployed read-only `real_outcome_source_inventory` and `real_outcome_growth_projection`. AUTONOMY.CANDIDATE_OUTCOME.REALITY.COLLECTION then deployed read-only candidate outcome collection and fixed existing-owner aggregation/window gaps. Current production verdict is `OUTCOME_EVIDENCE_INCOMPLETE`: available real candidate outcomes are consumed (`84/156`), there is no remaining visibility/capture/aggregation loss, but `72` real candidate outcomes have not happened yet and canary floors still fail. Current after-refresh floors are confidence `38.872`, trust `54.154`, prediction confidence `35.385`, operator earned confidence `45.815`. AUTONOMY.FLOOR.SEMANTICS_AND_RISK_TIER_REVIEW then clarified that this state is `TIER_1 MARGINAL_OPERATOR_REVIEW` for a first governed one-user review only, while autonomous one-user canary remains `NO_GO`.
- Related reports / ADRs: `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md`, `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`, `docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`, `docs/reports/AUTONOMY_CANARY_1D_CONFIDENCE_TRUST_PREDICTION_FLOOR_CLOSURE_REPORT.md`, `docs/reports/AUTONOMY_EVIDENCE_REAL_SOURCE_CONFIDENCE_COLLECTION_REPORT.md`, `docs/reports/AUTONOMY_SOURCE_CONFIDENCE_REALITY_AUDIT_REPORT.md`, `docs/reports/AUTONOMY_REAL_OUTCOME_COLLECTION_AND_CONFIDENCE_GROWTH_REPORT.md`, `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`, `docs/reports/AUTONOMY_FLOOR_SEMANTICS_AND_RISK_TIER_REVIEW_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-AUTONOMY-RISK-TIERED-FLOORS.
- Last verified commit: `3753df1a`.

## 16. Truth / Convergence

- What it means: The project's guardrail that repo, runtime, approved files, deployment lineage, and system truth are aligned enough to proceed.
- Source of truth: `tools/v7-truth-check`, `tools/v7-convergence-status`, `tools/v7_sync_lib.py`, runtime fingerprints/linkage.
- Where it is calculated: Truth/convergence tools and their runtime/repo checks.
- Where it is displayed: CLI output, reports, admin status/convergence surfaces where present.
- What affects it: Repo commit, runtime deployed files, approved deploy file list, runtime hash/fingerprint, convergence status, lineage metadata.
- What does NOT affect it: Local documentation claims without tool verification, chat memory, or screenshots alone.
- Operator meaning: "Is this V7 instance aligned and safe to trust?"
- Engineer meaning: Mandatory pre/post gate for major audits, implementation, deploy, and canonical reference updates.
- Known caveats: Documentation-only commits may differ from runtime code commit while truth/convergence still pass; reports must state this honestly.
- Related reports / ADRs: `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`, `PROGRAM_Z8_8_TRUTH_MANIFEST_AND_V7_TRUTH_CHECK_IMPLEMENTATION_REPORT.md`, ADR-001.
- Last verified commit: `8ba2178f`.

## 17. Admin UI Operator Model

- What it means: The admin UI should present daily work as a hybrid model: attention/problem-first when action is required, object-first when the system is healthy or the operator knows the object.
- Source of truth: Existing Users/Channels/Routes/Checks/Operator surfaces, Attention Layer derived projection, User and Channel drawers.
- Where it is calculated: UI rendering in `admin/v7-admin-api`, operator decision surface in `admin_core/operator_decision_surface.py`, existing alerts/checks/recommendations/why cards.
- Where it is displayed: Overview/Attention, Users, Channels, User Drawer, Channel Drawer, Operator Center.
- What affects it: Active problems, severity, operator decision surface, user/channel status, warnings, why cards, recommendations, execution readiness.
- What does NOT affect it: It must not create a new page, drawer, workflow, planner, governance model, truth source, storage, or execution path.
- Operator meaning: "Show me what needs attention first; otherwise let me browse users/channels calmly." In the Channel Drawer this means the first screen answers what V7 wants before any health score, technical rating, confidence label, route detail, evidence, history, logs, execution context, or service matrix details.
- Engineer meaning: Derived UX projection over existing objects and truth sources.
- Known caveats: The Attention Layer must stay deduplicated and calm; otherwise it becomes a noisy ticket system. Channel Drawer diagnostics must remain behind an explicit engineer boundary for normal operator work.
- Related reports / ADRs: `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md`, `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`, `CHANNEL_DECISION_FIRST_1_OPERATOR_SURFACE_REPORT.md`, `CHANNEL_DECISION_FIRST_2_DRAWER_REPORT.md`, ADR-004.
- Last verified commit: `8ba2178f`.

## 18. Channel Operator Signal Model

- What it means: Channels must be presented through multiple operator signals, not through one mixed score that appears to explain everything.
- Source of truth: Existing Channel Decision V7 / assignment truth, channel suitability breakdown, service matrix, capacity/load state, route/topology readiness, runtime readiness, history, and current user counts.
- Where it is calculated: `admin/v7-admin-api` channel suitability, assignment, topology, and drawer helpers; planner assignment truth in `tools/v7-users-autoswitch`; operator projection in `admin_core/operator_decision_surface.py`.
- Where it is displayed: Channel table, Channel Drawer first-screen Signals block, technical diagnostics, and compact signal/tooltip presentation.
- What affects it: Planner decision/assignment role, selected moves, blockers, service availability, load/capacity posture, route readiness confidence, runtime readiness, stability, history, users on channel, and evidence freshness.
- What does NOT affect it: A single mixed score alone, raw trust/recovery labels alone, cosmetic table ordering, or UI-only labels without underlying existing truth.
- Operator meaning: "What did V7 decide, what compact signal explains it, how many users are affected, and what should I inspect next?" In the Channel Drawer, first-screen signals are compact support for the decision, not a score breakdown.
- Engineer meaning: A read-only classification layer over existing signals: operator signals, supporting signals, and diagnostics-only signals.
- Known caveats: First-level channel table signals are `Services`, `Load`, `Runtime`, and `Stability` in a stable S/L/R/T order so operators can understand dot position without widening the column. The operator-facing table renders them as compact dot indicators with meaning exposed through a minimal legend plus hover/focus/tap tooltips; the Channel Drawer renders the same signal set as compact clickable rows under the decision reason. The aggregate `Сигналы` table column must not be sorted as one mixed value; sorting is allowed only by an individual signal: Services, Load, Runtime, or Stability. No more than four first-level signals should be visible in one row. Route is supporting/diagnostics-only because the current route component is topology/readiness confidence and may be reduced by capacity or service state; it must not appear as a red first-level route failure unless planner/route evidence exposes a real route blocker. Services at first level track primary user-facing services; optional/hidden endpoint checks such as Anthropic API must not downgrade first-level Services by themselves. Technical Health remains diagnostics-only. Raw score components must not become an alternative planner or action owner, and diagnostics must explain observed reality instead of point deductions. First-level signal color is decision-aligned: red means the current planner/assignment decision requires removal, block, or immediate action. If the decision is `Use`, `Keep Current Users`, or `Emergency Only`, a raw diagnostic failure may remain visible as warning/diagnostic text, but it must not appear as a red first-level contradiction to the planner decision. Load/capacity warning means assignment pressure, not internet quality or channel speed failure. Operator Surface and Engineering Surface must stay separate: compact first-screen language tells the operator what to do; diagnostics may explain score inputs, confidence, evidence, and raw technical state. First-screen operator wording avoids generic "requires verification" phrasing and avoids `Уточнить`, `Требует проверки`, and `Уверенность неполная`; use `Нет свежих данных`, `Нет свежего подтверждения`, `Открыть матрицу сервисов`, `Открыть пользователей`, `Открыть логи`, or a concrete problem such as `Лимит назначений достигнут`.
- Related reports / ADRs: `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2_TABLE_IMPLEMENTATION_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_SIGNALS_2B_ALIGNMENT_REPORT.md`, `CHANNEL_SIGNALS_2C_OPERATOR_SURFACE_REPORT.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`, `CHANNELS_OPERATOR_ENGINEER_SEPARATION_REPORT.md`, ADR-002, ADR-003, ADR-004, ADR-006, ADR-007, ADR-008, ADR-009, ADR-010.
- Last verified commit: `2fb9d205`.

## 19. UI Density Rules

- What it means: V7 admin screens use one compact visual rhythm so operators can scan more useful information per viewport without losing hierarchy.
- Source of truth: Existing admin CSS/layout primitives in `admin/v7-admin-api`: `.metric`, `.stat-card`, `.cards-grid`, `.check-card`, `.filterbar`, `.filter-chip`, channel table, and Channel Drawer section classes.
- Where it is calculated: UI rendering and CSS only. Density rules do not calculate planner truth, channel score, assignment, capacity, route, service, runtime, or history semantics.
- Where it is displayed: Overview, Users, Channels, Routes, Operator, Checks, Channel table, Channel Drawer, and shared dashboard cards.
- What affects it: Card padding/height, section spacing, table row padding, filter chrome, drawer section spacing, and placement of explanatory legends.
- What does NOT affect it: Planner decisions, assignment eligibility, score formulas, signal severity, execution readiness, storage, snapshots, APIs, or runtime state.
- Operator meaning: "The screen should show the answer and next action without wasting vertical space." Cards are compact status summaries, filters behave like lightweight navigation, tables prefer useful density, and drawers keep readable but tight sections.
- Engineer meaning: A shared UI standard over existing components. Channels, Users, Routes, Operator, and Checks should reuse the same dashboard card sizing instead of each tab inventing its own visual scale.
- Known caveats: Density must not hide required operator answers. Mobile 390px views must keep filters horizontally usable without clipping. Channel signal explanation must not consume a standalone row; the S/L/R/T legend belongs inside the Signals column header, with detailed meaning in the existing tooltip source.
- Related reports / ADRs: `CHANNELS_FINAL_DENSITY_AND_CONSISTENCY_REPORT.md`, `CHANNELS_OPERATOR_ENGINEER_SEPARATION_REPORT.md`, `CHANNELS_DRAWER_NO_DUPLICATES_ACTIONABLE_PROBLEMS_REPORT.md`, ADR-006, ADR-007, ADR-010.
- Last verified commit: `CHANNELS.TABLE_AND_LAYOUT_FINAL_POLISH implementation commit`.
