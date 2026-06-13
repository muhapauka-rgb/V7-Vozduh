# EXPLAINABILITY.0 DISCOVERY AND GAP AUDIT REPORT

Project: V7 Vozduh
Date: 2026-06-14
Branch inspected: `Updatesystem`
Mode: read-only discovery and gap audit

This report is intentionally not an implementation plan for a new engine. It audits what already exists, what is visible to the operator, what can be reused, and where the commercial/user-facing explainability gaps are.

Runtime mutation status: none. No deploy, no user movement, no apply action, no runtime write path.

## Truth Gate

The required gate was run before discovery.

| Gate | Result | Notes |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | PASS | First sandbox run could not resolve GitHub remote. Network-enabled retry passed with local, GitHub, and runtime truth aligned. |
| `tools/v7-convergence-status --json` | PASS | Convergence status aligned. Runtime action status was `READY_FOR_RUNTIME_ACTION`, but this audit did not perform runtime actions. |

Relevant truth facts:

- Local commit: `ae7f35a9817f2238becfd70168ac989d626bede9`.
- Runtime convergence was aligned.
- Dirty worktree content was documentation-only and ignored by the truth gate.
- Production commit reported by convergence: `bdb1bc5b9ec9ec7578ec36f8fcfb83d54588239c`.

## Discovery Scope

Inspected targets:

- `admin/v7-admin-api`
- `admin_core/operator_decision_surface.py`
- `admin_core/operator_observability.py`
- `admin_core/routing_intelligence.py`
- `admin_core/intelligence_platform.py`
- `admin_core/runtime_read_views.py`
- `admin_core/route_reality_views.py`
- `admin_core/diagnostic_views.py`
- `admin_core/performance_summaries.py`
- `admin_core/admin_registry_views.py`
- Admin-v2 UI surfaces: users, channels, routing, operator, checks, security, settings, logs
- User Drawer, Channel Drawer, Planner, Recommendation, Evidence, Proposal, and Execution surfaces

## 1. Existing Explainability Inventory

| Surface | Exists | What It Explains Today | Reuse Decision | Gap |
| --- | --- | --- | --- | --- |
| `admin/v7-admin-api` | Yes | Provides admin-v2 UI, evidence, proposals, execution, operator, runtime, release, route, diagnostic, and action endpoints. | Reuse and extend. | Monolithic surface, many entrypoints, mixed Russian/English labels, explanations fragmented across drawers. |
| `admin_core/operator_decision_surface.py` | Yes | User/channel recommendation state, confidence, risk, trust, prediction, blockers, reason breakdown, action chain, batch preview. | Reuse as primary explainability source. | Excellent data exists, but not all numeric thresholds and reason parts are visible in the operator UI. |
| `admin_core/operator_observability.py` | Yes | Operator overview, evidence detail, timeline, lineage, audit search, evidence archive, governance previews. | Reuse. | Strong for engineers/operators, but wording and navigation are still too technical for commercial simplicity. |
| `admin_core/routing_intelligence.py` | Yes | Service scores, suitability, risk, forecast trust, failure probability, future stability, dynamic blast-radius advisory. | Reuse. | Advisory explanations exist but are not consistently rendered as plain-language "why" cards. |
| `admin_core/intelligence_platform.py` | Yes | Trust evolution, prediction accuracy, suitability, candidate pool logic, explainability contract metadata. | Reuse and standardize. | The code itself flags `missing_explainability_contract`; this is the central technical gap. |
| `admin_core/runtime_read_views.py` | Yes | Runtime payload classification, source status, reason, known/unknown state. | Reuse. | Useful as low-level truth view, not sufficient as operator-facing explanation. |
| `admin_core/route_reality_views.py` | Yes | Route reality, trusted RU status, validation, checks, blockers, warnings. | Reuse. | Route terms are technical and need commercial wording. |
| `admin_core/diagnostic_views.py` | Yes | Capacity, pool state, readiness, user/channel diagnostic facts. | Reuse. | Numeric data is strong but separated from user/channel "why" explanations. |
| `admin_core/performance_summaries.py` | Yes | Component summaries, cache/candidate status, execution ownership boundaries. | Limited reuse. | Performance layer is not a user-facing explanation layer. |
| `admin_core/admin_registry_views.py` | Yes | Registry truth and read-only admin registry facts. | Reuse. | Registry facts need translation into "what this means" language. |
| Admin-v2 UI | Yes | Main operator navigation: overview, users, channels, routes, operator, checks, security, settings, logs. | Extend. | Good coverage, but too many places to look for one answer. |
| User Drawer | Yes | User facts, live state, evidence/proposal links, problem/action details. | Extend. | Does not yet default to one clear "why this channel / why not moved" explanation. |
| Channel Drawer | Yes | Channel facts, live state, service matrix, speed panels, problem detail. | Extend. | Needs exact eligibility/exclusion reasons with values and thresholds. |
| Planner surfaces | Yes | Autoswitch/dry-run/proposal/evidence surfaces explain candidate moves and governance. | Extend. | `candidate_moves_total=0` is explainable in data, but not first-class in commercial UI. |
| Recommendation surface | Yes | User move/keep recommendation, reason breakdown, confidence, risk, action chain. | Reuse and polish. | Strong core, but labels like `HIGH/MEDIUM/LOW` need visible thresholds. |
| Evidence surface | Yes | Evidence bundles, timelines, closure, verification, linked objects. | Reuse. | Rich but expert-oriented; should be context-linked from user/channel cards. |
| Proposal surface | Yes | Read-only proposals with confidence, severity, reason, benefit, rollback hint, governance path. | Reuse. | Commercial copy should explain "proposal" as "suggested next step". |
| Execution surface | Yes | Contracts, candidates, readiness, gates, timeline, verification, rollback, explain endpoint. | Reuse carefully. | Advanced and safety-rich, but too much governance vocabulary leaks to ordinary operators. |

Inventory verdict: the system already has a large explainability substrate. The problem is not absence of data; it is fragmentation, missing standardized contract, and insufficient plain-language/numeric visibility in the UI.

## 2. User Explainability

| Question | Current Answer | Visible To Operator? | Gap |
| --- | --- | --- | --- |
| Why is this user on this channel? | Partially available through current channel, evidence, route facts, and recommendation rows. | Partly. Requires opening multiple drawers or surfaces. | Needs one default user explanation card. |
| Why not move this user now? | Available through keep recommendation, `current_is_best`, sticky behavior, blockers, and planner evidence. | Weakly. Not a first-class top-level explanation. | Needs explicit "not moved because..." line. |
| Is the current channel best? | Available through recommendation result, improvement score, suitability, trust, and risk fields. | Partly. | Needs yes/no result plus score delta and threshold. |
| Is there a candidate move? | Available as `move_recommended` vs `keep`, batch preview, proposals, and candidate endpoints. | Yes, but scattered. | Needs visible candidate state in user card and drawer. |
| What is the expected benefit? | `expected_improvement`, `improvement_score`, service score deltas, confidence. | Partly. | `HIGH/MEDIUM/LOW` labels need numeric threshold and delta explanation. |
| What is the risk? | Risk value, risk label, blockers, review requirements. | Partly. | Risk should show value, threshold, and cause. |
| What services matter for this user? | Required service data and service matrix are available. | Partly. | Required services should be shown directly near the recommendation. |
| What is the evidence? | Evidence bundles link user/channel/route/audit facts. | Yes. | Evidence is still a separate expert-style surface. |
| What action can operator take? | Action chain, ignore/approve/governed move workflow, dry-run endpoints. | Yes. | Copy must make clear that approve is not direct runtime mutation. |

User explainability verdict: BASIC to GOOD. The raw ingredients are strong, but the operator does not yet get a single obvious answer to "why this exact user is here and why nothing moved".

## 3. Channel Explainability

| Question | Current Answer | Visible To Operator? | Gap |
| --- | --- | --- | --- |
| Why is this channel healthy/unhealthy? | Channel state, trust, risk, service score, code status, service matrix, speed panels. | Yes, partially. | State thresholds must be shown near labels. |
| Why eligible for routing? | Available from trust/service/capacity facts and route reality. | Partly. | Needs explicit eligibility line: eligible/excluded plus reason. |
| Why excluded? | Blockers, warnings, route mismatches, degraded state, service failures. | Partly. | Needs exact blocker table with value, threshold, source. |
| How stable is it? | Stability and prediction data exist. | Partly. | Stability should be shown as number plus last observed/freshness. |
| What services does it support? | Service matrix exists; channel service panel exists. | Yes. | Compact channel table hides services in some views. |
| Is capacity safe? | Capacity, load, used/free/headroom exist in diagnostics and channel data. | Partly. | Capacity should be visible next to every eligibility decision. |
| Is trust recovering or declining? | Trust evolution advice exists. | Partly. | Needs plain trend label with evidence. |
| What changed recently? | Timeline/audit/evidence archive exists. | Yes for advanced operator. | Needs a simple "last reason changed at..." field. |

Channel explainability verdict: GOOD technically, BASIC commercially. The channel drawer already has strong facts, but eligibility/exclusion logic should be presented as a concise decision, not inferred from many metrics.

## 4. Planner Explainability

| Question | Current Answer | Visible To Operator? | Gap |
| --- | --- | --- | --- |
| Why did planner propose a move? | Recommendation reasons, reason breakdown, expected improvement, confidence, risk, action chain. | Yes, inside decision/recommendation surfaces. | Needs standardized "why score" contract. |
| Why did planner not propose moves? | Existing evidence can represent sticky/current-is-best/no-candidate reasons. Recent state shows `candidate_moves_total=0`. | Weakly in commercial UI. | Needs top-level "0 moves because..." summary. |
| Why is current channel kept? | `keep`, `current_is_best`, sticky reasons, suitability/risk comparison. | Partly. | Needs explicit per-user keep reason. |
| What blocks execution? | Execution readiness, governance gates, restore barrier, rollback preview, blockers. | Yes. | Wording is too technical for non-engineer operator. |
| What is safe to do now? | Runtime action safe/convergence status, readiness gates, dry-run previews. | Yes. | Needs clearer separation between "recommended", "safe to preview", and "runtime execution". |
| What data source was used? | Evidence bundle/source/timeline/freshness exists. | Yes. | Source should be shown inline in recommendation drawer. |
| Does planner mutate runtime? | Operator decision surface marks read-only, preview-only, execution not allowed in many paths. | Partly. | UI labels like "Apply" can imply direct mutation and should be renamed. |

Planner explainability verdict: GOOD internally, BASIC in the operator mental model. The planner can explain itself, but the UI does not yet make "no move" and "safe/not safe" explanations effortless.

## 5. Operator UX

| Screen | Current State | Commercial Grade | Main Gap |
| --- | --- | --- | --- |
| Overview | Shows trust, runtime, release, execution, active users, channels, operator summary. | Partial. | Needs one 30-second "what matters now" explanation. |
| Users | Has columns for channel, recommended channel, decision, priorities, status, problem, traffic, device/action. | Partial. | Too much depends on opening drawers; hidden columns reduce explainability. |
| User Drawer | Contains detailed user/live/evidence/problem information. | Partial. | Needs default why-card before details. |
| Channels | Shows channel trust state, status, users, traffic, services, speed, role, load. | Partial. | Services/load can be hidden; eligibility thresholds not obvious. |
| Channel Drawer | Has live state, service/speed panels, problem drawer, metric detail. | Partial to good. | Needs direct "eligible/excluded because..." block. |
| Routes | Strong route reality and RU readiness surfaces. | Expert-grade. | Too technical for non-engineer commercial operator. |
| Operator | Strong decision, batch, approval, rollback, lineage, audit surfaces. | Expert-grade. | Workflow vocabulary is advanced and fragmented. |
| Evidence | Rich bundle/timeline/source/verification model. | Expert-grade. | Needs contextual summaries from user/channel views. |
| Proposals | Read-only proposals with governance path and expected benefit. | Partial. | "Proposal" concept should be simplified as suggested next step. |
| Execution | Very strong safety/readiness/rollback coverage. | Expert-grade, not commercial-simple. | Terms like gate, contract, barrier, rollback packet need friendly labels. |
| Diagnostics | Numeric facts and capacity details exist. | Good for operators. | Not merged into recommendation explanations. |

Operator UX verdict: the system is safe and powerful, but not yet "any operator understands in 30 seconds". It is closer to an expert cockpit than a commercial control panel.

## 6. Numeric Evidence Audit

| UI/Surface | Label Seen | Number Exists? | Threshold Visible? | Severity |
| --- | --- | --- | --- | --- |
| User recommendation | `Recommendation`, `Warning`, `OK` | Yes: confidence, trust, risk, improvement score. | Not consistently. | High |
| User expected improvement | `HIGH`, `MEDIUM`, `LOW` | Yes: `improvement_score`. | No. | High |
| User keep/move decision | `keep`, `move_recommended` | Yes: reasons, blockers, score delta. | Partly. | High |
| Channel state | `Excellent`, `Good`, `Warning`, `Degraded` | Yes: service score, trust, risk, capacity, stability. | No. | High |
| Channel trust state | Trust/status pill | Yes: trust score and trust model data. | Partly. | High |
| Channel health | `OK`, `WARN`, `DOWN`, `UNKNOWN` | Yes: code status, service matrix count, route reality. | Partly. | Medium |
| Channel load | Load/users | Yes: users, soft/hard capacity, headroom in diagnostics. | Partly and sometimes hidden. | Medium |
| Route reality | OK/WARN route state | Yes: OK/total, mismatch/leak counts. | Partly. | Medium |
| Evidence freshness | Fresh/stale/expired style state | Yes: age seconds, TTL-like freshness facts. | Partly. | Medium |
| Execution readiness | PASS/FAIL/UNKNOWN gates | Yes: gate reasons and readiness payload. | Partly. | Medium |
| Proposal confidence | Confidence label/value | Yes: confidence and severity. | Partly. | Medium |
| Diagnostics capacity | Capacity/pool readiness | Yes: used/free/pct/capacity/target users. | Mostly. | Low |

Numeric evidence verdict: numbers exist in the backend and supporting models, but commercial UI labels often do not carry the value and threshold next to the word. This is the biggest explainability gap after fragmentation.

## 7. Commercial Readiness

| Area | Score | Evidence | Main Problem |
| --- | ---: | --- | --- |
| User state explanation | 5/10 | User rows, recommendation rows, evidence, proposals, drawers exist. | No default one-sentence "why this user is here". |
| Channel explanation | 6/10 | Channel state, service matrix, speed, trust, risk, capacity exist. | Eligibility/exclusion not summarized as a decision. |
| Planner explanation | 5/10 | Reasons, blockers, batch preview, candidate/readiness endpoints exist. | `candidate_moves_total=0` not surfaced commercially. |
| Evidence traceability | 8/10 | Evidence bundles, timelines, lineage, archive, sources. | Too expert-oriented. |
| Operator simplicity | 4/10 | Navigation is broad and powerful. | Too many places to find one answer. |
| Numeric threshold visibility | 4/10 | Numeric substrate exists. | Thresholds hidden or not rendered near labels. |
| Russian localization | 6/10 | Most UI is Russian and i18n map exists. | Some English labels remain visible. |
| Safety/governance explainability | 7/10 | Read-only previews, gates, rollback, approvals, contracts. | Vocabulary too technical. |
| 30-second operational summary | 5/10 | Overview/operator panels exist. | Needs direct "what matters now / why / next safe action". |

Commercial readiness verdict: not commercial-ready yet. The control plane is explainable to engineers and advanced operators, but not yet to a non-technical commercial operator.

## 8. Top 20 Highest Value Improvements

Ranked by value, risk, and complexity. All recommendations reuse existing sources and avoid creating a new planner, governance layer, routing brain, truth source, observability stack, or explanation engine.

| Rank | Improvement | Value | Risk | Complexity | Reuse Source |
| ---: | --- | --- | --- | --- | --- |
| 1 | Add user "why-card": current channel, recommended/kept state, main reason, score delta, blocker. | Very high | Low | Medium | `operator_decision_surface.py`, evidence bundles |
| 2 | Add channel "eligibility-card": eligible/excluded, exact blocker, value, threshold, source. | Very high | Low | Medium | Channel decision rows, diagnostics, route reality |
| 3 | Add top-level "0 moves because..." planner summary. | Very high | Low | Low | Planner/evidence counters and recommendation reasons |
| 4 | Rename `Apply Best Recommendations` to a Russian safe-preview label. | High | Low | Low | Existing UI copy |
| 5 | Show numeric threshold under every `HIGH/MEDIUM/LOW`, `GOOD/WARNING/DEGRADED`, `PASS/FAIL` label. | High | Low | Medium | Existing scores and threshold code |
| 6 | Put `reason_breakdown` into plain Russian bullet lines. | High | Low | Medium | Decision surface reason breakdown |
| 7 | In User Drawer, show required services and whether current/recommended channel satisfies each. | High | Low | Medium | Service matrix and user priorities |
| 8 | In User Drawer, show trust/risk/prediction/suitability together. | High | Low | Low | Existing row fields |
| 9 | In Channel Drawer, show capacity as users/soft/hard/headroom. | High | Low | Low | Diagnostics capacity data |
| 10 | Add per-user "not moved because current is best/sticky/no safe candidate" reason. | High | Low | Medium | Planner and decision reasons |
| 11 | Add channel exclusion table: blocker, current value, required value, source snapshot. | High | Low | Medium | Channel decision, route reality, diagnostics |
| 12 | Add evidence freshness inline: age, source, last update. | Medium-high | Low | Low | Evidence bundles |
| 13 | Clean remaining English labels in admin-v2. | Medium-high | Low | Low | `STATIC_I18N` and UI strings |
| 14 | Add 30-second operator summary: what is OK, what is blocked, what safe action exists. | Medium-high | Low | Medium | Operator overview and execution summary |
| 15 | Replace expert workflow terms with friendly labels, keeping advanced detail expandable. | Medium | Low | Medium | Existing execution/governance surfaces |
| 16 | Context-link Evidence/Proposal/Execution from the object currently viewed. | Medium | Low | Medium | Existing drawers and endpoints |
| 17 | Add "same truth source" badges so users trust consistency across screens. | Medium | Low | Medium | Evidence source metadata |
| 18 | Reduce duplicate entrypoints by adding context-sensitive "why" buttons. | Medium | Low | Medium-high | Existing UI navigation |
| 19 | Standardize explainability payload contract across service, suitability, pool, prediction, risk, trust. | Very high | Medium | Medium-high | `intelligence_platform.py` existing contract notes |
| 20 | Add source freshness warning inside recommendation drawer before any approve/ignore action. | Medium | Low | Low | Evidence and runtime freshness fields |

Highest-value near-term cluster: improvements 1, 2, 3, 5, 6, 9, and 13. They are mostly UI/contract presentation work and do not require changing routing behavior.

## 9. Recommended Explainability Roadmap

### Phase 1: Read-Only Operator Clarity

Goal: make existing data understandable without changing runtime behavior.

- Add user why-card and channel eligibility-card using existing fields.
- Surface numeric values and thresholds beside labels.
- Add "0 moves because..." summary to operator overview.
- Clean mixed-language labels.
- Add inline evidence freshness/source indicators.
- Keep all behavior read-only and preview-only.

Phase 1 should not introduce new APIs unless an existing endpoint cannot provide the already-computed field.

### Phase 2: Standardized Explanation Contract

Goal: normalize how existing explainability facts are shaped.

- Merge existing `reason_breakdown`, service scores, candidate suitability, prediction, risk, trust, capacity, and route facts into a stable contract.
- Do this as a contract around existing models, not a new explanation engine.
- Use `intelligence_platform.py`'s own `missing_explainability_contract` finding as the anchor.
- Preserve existing planner, governance, routing, and truth ownership boundaries.

Phase 2 should be reviewed carefully because it touches cross-surface contracts.

### Phase 3: Commercial Operator Experience

Goal: make the product understandable to a non-engineer operator.

- Consolidate user/channel/planner explanations into one contextual "why and next safe action" flow.
- Keep advanced evidence, execution, rollback, and audit details expandable.
- Replace expert terms with friendly labels while preserving exact raw detail for audit.
- Add a 30-second dashboard summary that answers: what is healthy, what is risky, why no users moved, and what can be safely previewed.

Phase 3 is UX consolidation, not a new control plane.

## 10. Final Verdict

Final verdict: GOOD.

Evidence for GOOD:

- The system already has a strong explainability substrate: operator decision surface, evidence bundles, proposals, execution readiness, route reality, diagnostics, runtime reads, service scoring, trust, risk, prediction, and lineage.
- User/channel/planner decisions can be explained from existing data.
- Runtime safety is strongly represented through read-only previews, readiness gates, rollback views, and non-authoritative proposals.
- The inspected code already recognizes the need for a standardized explainability contract.

Why not ADVANCED:

- Explanations are fragmented across many screens and drawers.
- Numeric values often exist but thresholds are not shown next to labels.
- `candidate_moves_total=0` and "why no move" are not first-class commercial explanations.
- Some UI labels remain English or too technical.

Why not COMMERCIAL_READY:

- A non-technical operator still needs to know where to look and how to interpret planner/governance vocabulary.
- The UI does not yet consistently answer in one place: "why this user", "why this channel", "why no move", "what number crossed what threshold", and "what is the next safe action".

The recommended direction is not to build a new explanation system. The correct path is to reuse the existing decision, evidence, proposal, diagnostic, route, runtime, and intelligence surfaces, standardize the explanation payload, and present it as concise operator-facing why-cards with visible numbers, thresholds, and sources.
