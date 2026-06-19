# V7 Canonical Reference

Status: canonical project reference
Last verified commit: `2fb9d205`
Last verified date: 2026-06-19

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

Before launching any new audit, use Reference First:

1. Read `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Read relevant ADRs.
3. Read `docs/reference/SYSTEM_MAP.md`.
4. Determine whether the answer already exists.

A new audit is allowed only when the reference has no answer, the reference explicitly marks the area `UNKNOWN`, system behavior changed after the last verified commit, or evidence contradicts this canonical reference. Otherwise, update the reference if needed and do not create a new audit.

## 1. Channels

- What it means: A channel is an egress path that can carry users, be inspected by operators, and be considered by the planner.
- Source of truth: Channel registry/runtime channel state, operator decision surface, service matrix, route/runtime readiness, planner assignment truth.
- Where it is calculated: `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch`, and channel helper functions in `admin/v7-admin-api`.
- Where it is displayed: Admin Channels table, Channel Drawer, Attention/Overview derived surfaces, technical diagnostics.
- What affects it: Registry flags, manual/reserve/canary role, service checks, stability, capacity/load, route readiness, runtime readiness, history, assigned users, planner gates.
- What does NOT affect it: Cosmetic UI labels, screenshots, operator-facing health score alone, or raw trust labels alone.
- Operator meaning: "Can this channel be used, should users stay, what is wrong, and what action is safe?"
- Engineer meaning: Aggregated runtime/planner/read-model state for one egress object.
- Known caveats: Some roles such as Keep Only or Blocked may not appear in production screenshots if live data currently has no channel in that state.
- Related reports / ADRs: `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `CHANNEL_TRUTH_4_CHANNEL_ROLE_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, ADR-004.
- Last verified commit: `8ba2178f`.

## 2. Channel Decision V7

- What it means: The operator-facing decision for a channel: Use, Evacuate, Keep Current Users, Emergency Only, or Blocked.
- Source of truth: Existing planner/assignment truth and channel role flags, not a separate UI score.
- Where it is calculated: `tools/v7-users-autoswitch` candidate/blocker/selected-move logic and adapter code in `admin_core/operator_decision_surface.py` plus channel decision helpers in `admin/v7-admin-api`.
- Where it is displayed: Primary Channel table column and Channel Drawer first screen. The Channel Drawer first screen is Decision-first: Decision → Reason → Signals → Problems → Works → Diagnostics, with nothing above the Decision block.
- What affects it: Selected moves, eligible candidates, blockers, current users, `manual_only`, `reserve_only`, canary reservation, disabled/quarantine/maintenance, service/route/speed/stability/load/policy gates.
- What does NOT affect it: Channel Score by itself, old TRUSTED/WATCH/QUARANTINED labels, or raw engineering health labels.
- Operator meaning: "What does V7 want me to do with this channel?" `Use` means V7 can use the channel under current planner/assignment evidence; it does not mean fastest, best, warning-free, or unlimited capacity. `Emergency Only` means the channel is role/policy restricted for manual, reserve, canary, or execution-only use; it does not mean technically broken.
- Engineer meaning: A read-only projection of planner assignment/retention/evacuation truth into operator language.
- Known caveats: If the planner cannot produce a role because data is absent, UI must show the safest truthful state rather than inventing eligibility. A channel can be `Use` while capacity/load is at warning or hard-full for new assignments; the decision must be read together with blocker/load details.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, ADR-009.
- Last verified commit: `2fb9d205`.

## 3. Channel Score

- What it means: A technical/mixed health score from 0 to 100 that explains channel condition; it is not assignment truth.
- Source of truth: Existing `channelSuitability(source)` model and its component breakdown.
- Where it is calculated: `admin/v7-admin-api` functions `channelSuitabilityServices`, `channelSuitabilityStability`, `channelSuitabilityCapacity`, `channelSuitabilityRoute`, `channelSuitabilityRuntime`, `channelSuitabilityHistory`, and `channelSuitability`.
- Where it is displayed: Secondary Health/Technical Health column, Channel Drawer diagnostics, score explanation.
- What affects it: Services, stability, capacity, route/topology, runtime/readiness, and history components.
- What does NOT affect it: Planner assignment eligibility directly, emergency/manual role policy directly, or whether V7 should move current users.
- Operator meaning: "How healthy does the channel look technically?"
- Engineer meaning: A mixed diagnostic score useful for explanation and troubleshooting, separate from planner hard gates.
- Known caveats: A high score can coexist with Do Not Assign/Emergency Only/Evacuate if planner gates or role flags block assignment. A capacity penalty inside the score means user-assignment pressure against limits, not bandwidth saturation or speed failure. This is intentional after CHANNEL.TRUTH alignment.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_SUITABILITY_1_PLANNER_DERIVED_SUITABILITY_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, ADR-002, ADR-009.
- Last verified commit: `2fb9d205`.

## 4. Technical Health

- What it means: A diagnostics-only explanation of why the Channel Score is what it is.
- Source of truth: Existing channel suitability breakdown and evidence/read models.
- Where it is calculated: `admin/v7-admin-api` channel suitability and score explanation functions.
- Where it is displayed: Nested technical diagnostics inside the Channel Drawer, not as a primary workflow.
- What affects it: Score components, fresh service/route/runtime evidence, stability/capacity/history inputs.
- What does NOT affect it: Operator action flow directly, assignment decision directly, or governance approval.
- Operator meaning: "Why did V7 give this channel this health score?" Technical health can be good while assignment is Emergency Only, Keep Only, or load-limited.
- Engineer meaning: Component-level diagnostic view for the score model.
- Known caveats: Health must not reintroduce action/resolution language as first-line operator truth. Diagnostics may point to missing evidence but should not become a separate execution path. Table-level "Healthy" is narrower than technical health: it requires a usable/keep assignment posture and no red first-level operator signal.
- Related reports / ADRs: `docs/operator_actions/CHANNEL_HEALTH_SCREEN_EXISTENCE_AUDIT.md`, `docs/operator_actions/CHANNEL_HEALTH_2_DIAGNOSTICS_ONLY_IMPLEMENTATION_REPORT.md`, `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, ADR-003, ADR-009.
- Last verified commit: `2fb9d205`.

## 5. Route

- What it means: Route reality/readiness for user/channel traffic, including route status, direct/RU route checks, mismatch/leak risk, and topology signals.
- Source of truth: Runtime route read models and route reality helpers.
- Where it is calculated: `admin_core/route_reality_views.py`, `admin_core/route_views.py`, `admin/v7-admin-api` route status/readiness functions, and planner route gates in `tools/v7-users-autoswitch`.
- Where it is displayed: Routes surface, User Drawer, Channel Drawer diagnostics, Attention items when route risk exists.
- What affects it: Runtime route tables, policy routing, direct/RU route state, route evidence freshness, channel topology, planner route gates.
- What does NOT affect it: Channel Score alone, UI ordering, or manual labels.
- Operator meaning: "Is traffic going where it should, and is there a safety/leak problem?"
- Engineer meaning: Read-only runtime route evidence and planner gate input.
- Known caveats: Route validation is primarily diagnostic/status until a safe existing handler exists; it must not imply unsafe execution.
- Related reports / ADRs: `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 6. Capacity

- What it means: Assignment/load posture for a channel or pool: current and projected users compared with configured soft, hard, and failover-hard limits. Capacity answers whether V7 may add users, should pause additions, or must treat a channel as full for planned/failover movement.
- Source of truth: Egress registry capacity fields (`capacity_users`, `soft_limit`, `hard_limit`), live assigned user counts, policy load settings, dynamic load summary, planner capacity/load gates, and capacity readiness tools.
- Where it is calculated: `tools/v7-users-autoswitch` `_load_policy`, `_healthy_for_load`, `_dynamic_load_summary`, `_load_limits_for_egress`, `_capacity_status`, `_capacity_decision`, `_gate_load`; `admin/v7-admin-api` `channelSuitabilityCapacity`, `channelLoad`, `loadPosture`, capacity read/preview helpers; runtime support tools `v7-capacity-check` and `v7-capacity-readiness`.
- Where it is displayed: Channel table Load/Capacity signal, Channel Drawer diagnostics, score explanation, execution preview/gates, overview Load card, global capacity/readiness summaries.
- What affects it: Current users assigned to an egress, projected users after movement, explicit per-egress limits, dynamic load policy, healthy working pool size, reserve ratio, soft/hard/failover multipliers, failover capacity multiplier, min/max limits, role flags that remove channels from normal working pool, and planner purpose (`current`, `planned`, `failover`).
- What does NOT affect it: CPU usage, bandwidth saturation, traffic volume, raw speed complaint alone, raw service success alone, cosmetic UI ordering, screenshots, or the mixed Channel Score by itself.
- Operator meaning: `Load OK` means the channel is within assignment limits. `Soft Full` / warning means the channel is near or at the soft limit and new additions require caution/checking. `Hard Full` / "on limit" means new planned assignments are restricted; current users are not automatically failing. `Overloaded` means failover-hard capacity was reached and is a stronger emergency load state.
- Engineer meaning: Planner/gate input that bounds movement, affects ranking, can block planned/failover candidates, and prevents broad unsafe switching.
- Known caveats: Capacity/load is not speed quality and not traffic saturation. A channel can have good speed/stability and still be hard-full because too many users are assigned relative to policy. Production evidence on 2026-06-18 showed `vless` and `awg3` as technically usable/currently retained while load was hard-full for assignment. Global IP capacity readiness (`capacity_plan`) is a separate pool/readiness check and can fail independently from per-channel assignment load.
- Related reports / ADRs: `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `docs/track7/productization/e35_0_1-audit/capacity-policy-audit.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, ADR-009.
- Last verified commit: `2fb9d205`.

## 7. Service Matrix

- What it means: Per-service reachability/health diagnostics for channels/services.
- Source of truth: Existing service matrix refresh/test outputs and admin service matrix read models.
- Where it is calculated: Runtime tools `v7-service-matrix-refresh-all` and `v7-service-matrix-test`; admin rendering helpers in `admin/v7-admin-api`.
- Where it is displayed: Checks, Channel Drawer service details, diagnostics, Attention item source when service failure affects users.
- What affects it: Service test results, freshness, channel availability, runtime check outputs.
- What does NOT affect it: It does not by itself execute user movement, bypass governance, or replace planner eligibility.
- Operator meaning: "Which services work on this channel and what needs re-checking?"
- Engineer meaning: Measurement/diagnostic input consumed by UI and planner gates.
- Known caveats: Service Matrix is diagnostic/background automation, not a standalone business action. Manual refresh is allowed only through existing safe handlers. First-level channel Services should track primary user-facing services; hidden endpoint checks such as auth/API companion endpoints remain supporting diagnostics unless they become explicit planner blockers.
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
- Known caveats: Planner read-only outputs are not the same as applying execution. Apply remains governed.
- Related reports / ADRs: `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 12. Assignment

- What it means: Whether V7 can assign new users to a channel, keep current users, evacuate users, or restrict the channel to emergency/manual use.
- Source of truth: Planner assignment eligibility, selected moves, blockers, channel role flags, and current user counts.
- Where it is calculated: `tools/v7-users-autoswitch` `_candidate`, `_block`, `_gate_*`, `_select_moves`, `_candidate_json`; adapter projection in `admin_core/operator_decision_surface.py` and channel decision helpers.
- Where it is displayed: Channel table decision column, Channel Drawer first screen/details, Attention Layer when action is needed.
- What affects it: Eligibility candidates, blockers, selected moves away, current users, manual/reserve/canary flags, disabled/quarantine states, policy and runtime gates.
- What does NOT affect it: Technical Health/Score alone or old trust labels.
- Operator meaning: "Can V7 use this channel, must users leave, or is it restricted?"
- Engineer meaning: Planner-derived role projection over existing channel/user truth.
- Known caveats: Quality and assignment can intentionally disagree. The UI must make the decision primary and health secondary.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, ADR-002.
- Last verified commit: `8ba2178f`.

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

- What it means: Read-only intelligence/shadow/automation support that may recommend, simulate, or monitor but must not create an independent execution path.
- Source of truth: Existing shadow autonomy, intelligence platform, operator execution pipeline, governed execution path.
- Where it is calculated: `admin_core/shadow_autonomy.py`, `admin_core/intelligence_platform.py`, `admin_core/operator_execution_pipeline.py`, planner tools.
- Where it is displayed: Operator Center, execution readiness, attention/overview summaries, evidence/details.
- What affects it: Planner signals, safety gates, governance state, intelligence snapshots, execution readiness.
- What does NOT affect it: It does not bypass approval, restore barriers, governance, or existing execution handlers.
- Operator meaning: "V7 can surface what needs attention, but dangerous changes remain guarded."
- Engineer meaning: Derived intelligence layer over existing truth and governed execution.
- Known caveats: UNKNOWN - requires future audit to produce a complete autonomy contract across all shadow/intelligence modules.
- Related reports / ADRs: `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`.
- Last verified commit: `8ba2178f`.

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
- Operator meaning: "Show me what needs attention first; otherwise let me browse users/channels calmly." In the Channel Drawer this means the first screen answers what V7 wants before any health score, route detail, evidence, history, logs, execution context, or service matrix details.
- Engineer meaning: Derived UX projection over existing objects and truth sources.
- Known caveats: The Attention Layer must stay deduplicated and calm; otherwise it becomes a noisy ticket system. Channel Drawer diagnostics must remain last and collapsed for normal operator work.
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
- Known caveats: First-level channel table and Channel Drawer signals are `Services`, `Load`, `Runtime`, and `Stability` only when stability is not OK. The operator-facing table renders them as compact dot indicators with meaning exposed through hover/focus/tap tooltips; the Channel Drawer renders the same signal set as compact rows under the decision reason. No more than four first-level signals should be visible in one row. Route is supporting/diagnostics-only because the current route component is topology/readiness confidence and may be reduced by capacity or service state; it must not appear as a red first-level route failure unless planner/route evidence exposes a real route blocker. Services at first level track primary user-facing services; optional/hidden endpoint checks such as Anthropic API must not downgrade first-level Services by themselves. Technical Health remains diagnostics-only. Raw score components must not become an alternative planner or action owner. First-level signal color is decision-aligned: red means the current planner/assignment decision requires removal, block, or immediate action. If the decision is `Use`, `Keep Current Users`, or `Emergency Only`, a raw diagnostic failure may remain visible as warning/diagnostic text, but it must not appear as a red first-level contradiction to the planner decision. Load/capacity warning means assignment pressure, not internet quality or channel speed failure.
- Related reports / ADRs: `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2_TABLE_IMPLEMENTATION_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_SIGNALS_2B_ALIGNMENT_REPORT.md`, `CHANNEL_SIGNALS_2C_OPERATOR_SURFACE_REPORT.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, ADR-002, ADR-003, ADR-004, ADR-006, ADR-007, ADR-008, ADR-009.
- Last verified commit: `2fb9d205`.
