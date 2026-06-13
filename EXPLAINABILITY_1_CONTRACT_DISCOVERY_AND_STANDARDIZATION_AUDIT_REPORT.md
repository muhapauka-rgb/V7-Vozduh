# EXPLAINABILITY.1 CONTRACT DISCOVERY AND STANDARDIZATION AUDIT REPORT

Project: V7 Vozduh
Date: 2026-06-14
Branch inspected: `Updatesystem`
Mode: read-only contract discovery

This report does not implement Why-Cards, UI, API changes, or a new explanation engine. It audits whether an explainability contract already exists, where it lives, how much can be reused, and what must be standardized before Why-Cards are implemented.

Runtime mutation status: none. No apply, no deploy, no user movement, no runtime write path.

## Truth Gate

| Gate | Result | Notes |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | PASS | Sandbox read initially failed on GitHub remote; network-enabled retry passed. |
| `tools/v7-convergence-status --json` | PASS | Local, GitHub, and production were aligned for runtime-action safety. |

Gate facts:

- Local commit: `ae7f35a9817f2238becfd70168ac989d626bede9`.
- GitHub `Updatesystem`: `ae7f35a9817f2238becfd70168ac989d626bede9`.
- Production/runtime commit model: `bdb1bc5b9ec9ec7578ec36f8fcfb83d54588239c`.
- Dirty worktree paths were documentation-only and ignored by the gate.

## 1. Contract Inventory

| Surface | Status | Reuse | Gap |
| --- | --- | --- | --- |
| `admin_core/intelligence_platform.py` `explainability_framework()` | CONTRACT EXISTS | REUSE | Defines `subject`, `score`, `components`, `confidence`, `source`, `authority`, but not `status`, `threshold`, `updated_at`, `next_action`, or UI visibility rules. |
| `admin_core/intelligence_platform.py` `explain_score()` | CONTRACT EXISTS | REUSE | Generic normalized payload exists with schema `v7.intelligence.explainability-payload.v1`; it is not the universal shape used by admin UI payloads. |
| `admin_core/intelligence_platform.py` `recommendation_engine_contract()` | CONTRACT EXISTS | REUSE | Strong shadow recommendation contract with weights and confidence floors; scoped to shadow recommendations, not all explainability objects. |
| `admin_core/intelligence_platform.py` `shadow_recommendation_for_user()` | CONTRACT EXISTS | REUSE/EXTEND | Has `why`, `why_now`, `why_this_channel`, `why_not_current`, `why_confidence`, `why_risk`, `reason_breakdown`, blockers, and candidates. Not fully surfaced as a common admin contract. |
| `admin_core/operator_decision_surface.py` user rows | CONTRACT EXISTS | REUSE | Has recommendation, confidence, improvement, risk, trust, prediction, reasons, blockers, source hash, action chain. Lacks normalized `value/threshold/source/updated_at` per field. |
| `admin_core/operator_decision_surface.py` channel rows | PARTIAL CONTRACT | EXTEND | Has state, state reason, users, capacity, stability, risk, trust, prediction, services. Lacks explicit eligibility/exclusion contract with values and required thresholds. |
| `admin_core/operator_observability.py` selected moves | PARTIAL CONTRACT | REUSE | Has `candidate_moves_total`, selected moves, source, freshness. No standardized no-move reason taxonomy in admin API payload. |
| `admin_core/operator_observability.py` target pool | PARTIAL CONTRACT | REUSE | Has users, soft/hard limits, readiness, warnings, registry. No computed headroom field and no common capacity reason field. |
| `admin_core/routing_intelligence.py` service scoring | PARTIAL CONTRACT | REUSE | Has service score, confidence, explainability strings, criteria components. Thresholds exist more as scoring logic than a stable admin-facing contract. |
| `admin_core/routing_intelligence.py` prediction | PARTIAL CONTRACT | REUSE | Has forecast probabilities, confidence, authority `none_prediction_only`. No universal `prediction_score/source/updated_at` payload. |
| `admin_core/runtime_read_views.py` schema contracts | CONTRACT EXISTS | REUSE | Runtime read contracts define required/optional fields, read-only boundary, reasons. Scope is runtime summaries, not business explainability. |
| `admin_core/route_reality_views.py` schema contracts | CONTRACT EXISTS | REUSE | Route reality and trusted-RU contracts exist with required fields. Scope is route truth, not recommendation contract. |
| `admin_core/diagnostic_views.py` capacity state | PARTIAL CONTRACT | REUSE | Strong capacity numbers exist: active, registered, capacity, free capacity, pools, warnings. Not merged into recommendation/channel eligibility contract. |
| `admin_core/performance_summaries.py` path maps | BOUNDARY CONTRACT | DO_NOT_TOUCH | Documents read-only builders, forbidden request path items, ownership. Not an explainability payload owner. |
| `admin_core/admin_registry_views.py` registry views | FACT CONTRACT | REUSE | Registry truth can be reused as source. It is not an explanation contract by itself. |
| Evidence payloads | CONTRACT EXISTS | REUSE | Evidence bundle has status, severity, summary, evidence items, recommendation, source, updated_at, freshness metadata. Missing `value/threshold/confidence` as common fields. |
| Proposal payloads | CONTRACT EXISTS | REUSE | Proposal has status, confidence, severity, reason, affected users, targets, services, evidence link, benefit, rollback hint, source, freshness. Missing normalized score/value/threshold structure. |
| Execution explanation payloads | CONTRACT EXISTS | REUSE | Execution explain/readiness/candidate explain payloads include why blocked/ready, owners, evidence, risk, next step, read-only flags. Scope is execution readiness, not user/channel planner contract. |
| User drawer payloads | PARTIAL CONTRACT | EXTEND | User data, evidence, proposal, route, recommendation links exist. Needs canonical why contract as default object summary. |
| Channel drawer payloads | PARTIAL CONTRACT | EXTEND | Channel health/service/speed/problem detail exists. Needs canonical eligibility/exclusion fields. |
| Planner payloads | PARTIAL CONTRACT | EXTEND | Planner dry-run and evidence show no-move reasons. Needs standard no-move summary in admin contract. |

Inventory verdict: a common explainability framework already exists, but it is not consistently used as the canonical payload across user, channel, planner, evidence, proposal, and execution surfaces.

## 2. Trust Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `trust_score` | Yes | `trust-summaries`, `trust-evolution-summaries`, operator user/channel rows, `score_shadow_candidate()` components. | Partly | Field name alternates between `trust`, `trust_score`, `overall_confidence`, and trust component. |
| `trust_state` | Partial | Channel trust recovery payload, runtime/release trust gates, confidence bands. | Partly | No universal state enum for user/channel/planner trust. |
| `trust_reason` | Partial | Channel state reason, runtime/release trust gate reasons, trust evolution advice. | Partly | Reason exists but is not normalized as `trust_reason`. |
| `trust_source` | Partial | Snapshot family names, `source_hash`, runtime/release trust source fields. | Partly | Source is often implicit by snapshot family or endpoint. |
| `trust_updated_at` | Partial | Snapshot freshness metadata and evidence freshness. | Weak | Updated timestamp is not attached to every trust-bearing value. |

Trust owner recommendation: `admin_core/intelligence_platform.py` owns the abstract contract; `admin_core/operator_decision_surface.py` should remain the operator-facing assembler.

## 3. Risk Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `risk_score` | Yes | `risk-summaries`, `_risk_penalty()`, user/channel decision rows, execution candidate risk summaries. | Partly | Sometimes rendered as `risk`, sometimes `risk_penalty`, sometimes categorical `risk_state`. |
| `risk_label` | Yes | Execution candidate `risk_state`, proposal severity, operator states. | Yes | Labels are not always tied to numeric thresholds. |
| `risk_reason` | Partial | Candidate blocked reasons, severity classification, execution risk items, channel state reasons. | Partly | No single `risk_reason` field across payloads. |
| `risk_source` | Partial | Snapshot family, validation source, blast-radius/service/rollback sources. | Partly | Source exists but differs by surface. |
| `risk_updated_at` | Partial | Evidence/proposal freshness and snapshot freshness. | Weak | Risk values rarely carry their own timestamp. |

Risk owner recommendation: scoring belongs to existing routing/intelligence/execution owners; normalized display should be assembled by operator decision surface, not a new risk engine.

## 4. Prediction Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `prediction_score` | Partial | `score_shadow_candidate()` component, predictive foundation summaries, user row `prediction` summary. | Partly | No universal `prediction_score`; often represented as confidence/probability/summary. |
| `confidence` | Yes | Prediction summaries, recommendation rows, evidence/proposal/execution surfaces. | Yes | Scale differs: some confidence is 0-1, some 0-100, some string bands. |
| `prediction_reason` | Partial | Prediction summary text, forecast factors, execution readiness forecast assumptions. | Partly | Reason not standardized under one key. |
| `prediction_source` | Partial | `prediction-summaries`, predictive foundation, source hash. | Partly | Source is mostly family/endpoint-derived. |

Prediction owner recommendation: keep `routing_intelligence.PredictiveFoundation` and `intelligence_platform` as owners; standardize scale and display in the canonical contract.

## 5. Suitability Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `suitability_score` | Yes | `candidate-suitability-summary`, `_candidate_component_scores()`, `score_shadow_candidate()`, recommendation rows through score/improvement. | Partly | UI often shows recommendation label rather than suitability score. |
| `suitability_reason` | Yes | Candidate `reasons`, `reason_breakdown`, `why_this_channel`, `why_not_current`. | Partly | Reasons are split between lists, strings, and component maps. |
| `suitability_source` | Partial | Candidate snapshot family, source hash, planner dry-run payload. | Partly | Source is not consistently attached per reason. |

Suitability owner recommendation: candidate suitability and best-available-pool snapshots are the canonical source; operator decision surface should assemble the operator-facing contract.

## 6. Service Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `service_score` | Yes | `routing_intelligence.py`, channel service scores, service matrix, channel decision rows. | Partly | It is not always visible beside channel/recommendation labels. |
| `threshold` | Partial | `intelligence_platform.py` SLO thresholds and recommendation confidence floors; service scoring logic. | Weak | Threshold is not consistently emitted beside each service result. |
| `service_reason` | Yes | Service matrix rows, `service_*_ok` reasons, Telegram sentinel reason, execution service impact summary. | Partly | Reason key varies. |
| `service_source` | Yes | Service matrix, sentinel, quality history, execution service impact `evidence_source`. | Partly | Source exists but not normalized across user/channel/planner payloads. |

Service owner recommendation: service matrix and routing intelligence remain source owners; canonical contract should reuse their score/reason/source without changing service logic.

## 7. Capacity Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `users` | Yes | Target pool, channel rows, egress registry derived counts, execution blast radius. | Yes | User count appears in several shapes. |
| `soft_limit` | Yes | `operator_observability.target_pool()`, execution capacity preview, planner candidate `load`. | Partly | Not always present in channel decision rows. |
| `hard_limit` | Yes | Registry, target pool, proposals, execution blast radius. | Partly | Good source exists; UI often hides exact threshold. |
| `headroom` | Partial | Computable from users/hard limit/free capacity; diagnostics has `free_capacity`. | Weak | Not consistently named as `headroom`. |
| `capacity_reason` | Partial | Target pool warnings, proposal reason, execution `capacity_exceeded`, planner `load status`. | Partly | No universal `capacity_reason`. |

Capacity owner recommendation: registry/diagnostic/execution capacity should be reused; standardization should add naming and presentation only.

## 8. Eligibility Contract

| Field | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `eligible` | Yes | Planner candidates, `score_shadow_candidate()`, best available pool evidence. | Partly | Channel drawer does not present this as a first-class decision. |
| `exclusion_reason` | Partial | Candidate `blocked`, `reasons`, execution risk items, route blockers. | Partly | Existing fields are strong but not normalized as `exclusion_reason`. |
| `current_value` | Partial | Score parts, load users, service status, route values. | Weak | Values are nested in source-specific payloads. |
| `required_value` | Partial | Confidence floors, hard limits, service pass requirements, gate requirements. | Weak | Threshold/requirement is often implicit in code or gate model. |
| `source_snapshot` | Partial | `source_hash`, snapshot family names, evidence source. | Partly | Needs stable per-field source metadata. |

Eligibility owner recommendation: planner candidate payload and operator decision surface should be canonical for eligibility assembly; no new planner needed.

## 9. No-Move Contract

This is the most important section for `candidate_moves_total=0`.

| Reason Type | Exists | Location | Visible | Gap |
| --- | --- | --- | --- | --- |
| `current_is_best` | Yes | `POOL1_EVIDENCE/phase2/zero_candidate_user_reasons.json`, BA6 root-cause evidence, planner payloads. | Weak in commercial UI | Exists as evidence, not normalized into admin top-level contract. |
| `sticky_keep_current` | Yes | `POOL1_EVIDENCE/phase2/zero_candidate_user_reasons.json`, BA6 root-cause evidence, planner payloads. | Weak in commercial UI | Exists as evidence, not surfaced as "no move because sticky/current route kept". |
| `blocked_by_capacity` | Partial | Planner candidate load, execution blast radius `capacity_exceeded`, proposals above hard limit. | Partly | Not part of one no-move taxonomy. |
| `blocked_by_service` | Partial | Service matrix proposals, candidate blocked reasons, execution service impact. | Partly | Reasons exist but are source-specific. |
| `blocked_by_stability` | Partial | Planner candidate blocked reasons such as `stability_below_floor`, quality history, service scoring. | Partly | No universal field. |
| `blocked_by_governance` | Yes | Execution readiness gates, restore barrier, selected moves, authority gates. | Yes for execution | Needs simpler no-move summary for planner/admin. |
| `blocked_by_reserve` | Partial | Planner candidate reserved/canary fields, `_risk_penalty()` canary reserved handling, target pool reserved warning. | Partly | No unified reserve blocker field. |

Current factual no-move evidence:

- `candidate_moves_total=0`.
- `POOL1_EVIDENCE/phase2/zero_candidate_user_reasons.json` records `sticky_keep_current=18` and `current_is_best=8`.
- BA6 root-cause evidence states that every planner-visible user had `action=keep`, so no real planner-selected users existed for a 25-user packet.

No-move verdict: the explanation exists, but the no-move contract is fragmented. The canonical no-move payload should be standardized from existing planner/evidence fields.

## 10. Duplication Audit

| Meaning | Locations Found | Canonical Owner | Duplicate? |
| --- | --- | --- | --- |
| Trust | `trust-summaries`, trust evolution, runtime/release trust gates, operator rows. | `intelligence_platform` for model, `operator_decision_surface` for admin assembly. | Yes, but acceptable if normalized. |
| Risk | `risk-summaries`, `_risk_penalty()`, execution risk summaries, proposal severity. | Routing/intelligence for score; execution for execution risk; operator surface for display. | Yes. |
| Prediction | `routing_intelligence.PredictiveFoundation`, prediction summaries, user row prediction. | `routing_intelligence` and `intelligence_platform`. | Partial duplication by representation. |
| Suitability | Candidate suitability, best available pool, shadow candidate score, operator user rows. | Candidate suitability/best pool snapshots; operator surface as assembler. | Yes, but same domain. |
| Service Score | Service matrix, routing intelligence service score, execution service impact. | Service matrix/routing intelligence. | Yes, with different scopes. |
| Capacity | Registry limits, diagnostics capacity, target pool, execution blast radius, proposals. | Registry/diagnostics for facts; execution for execution preview. | Yes. |
| Eligibility | Planner candidate `eligible`, shadow score `eligible`, route/trusted checks. | Planner candidate payload. | Partial duplication. |
| Recommendation | Planner dry-run, shadow recommendation, operator decision surface, proposals. | Operator decision surface for operator-facing recommendation; planner remains source. | Yes. |
| Evidence | Evidence bundles, proposal evidence links, execution evidence refs. | Evidence bundle model in admin API. | No harmful duplication; it is a linking layer. |

Duplication verdict: there is duplication of representation, not necessarily duplication of authority. Do not refactor owners blindly. Standardize a read-only adapter/contract around existing owners.

## 11. Commercial Readiness

| Object | Can Explain Itself Today? | Score | Main Missing Piece |
| --- | --- | ---: | --- |
| User | Partly | 6/10 | Needs one canonical why payload with current channel, recommendation/keep reason, score delta, blockers, source, and freshness. |
| Channel | Partly | 6/10 | Needs eligibility/exclusion contract with values, thresholds, and source snapshot. |
| Recommendation | Mostly | 7/10 | Strong `why_*`, confidence, reason breakdown, blockers, and action chain exist; needs uniform field names and UI visibility. |
| Planner | Partly | 5/10 | Can explain no-move via evidence, but `candidate_moves_total=0` is not a first-class commercial contract. |

Commercial readiness verdict: technically explainable, commercially inconsistent. A non-engineer operator still needs a normalized "why" object per user/channel/planner state.

## 12. Recommended Canonical Contract

This is a recommendation only. It is not implemented by this audit.

| Field | Reuse Source | Owner | Gap |
| --- | --- | --- | --- |
| `status` | Evidence/proposal/execution/operator state labels. | Operator decision surface for display. | Need consistent enum mapping. |
| `reason` | `why`, `reasons`, `state_reason`, evidence summary, proposal reason. | Operator decision surface as assembler. | Reason currently split across many keys. |
| `value` | Score, trust, risk, service, users, current metric. | Existing domain owner. | Needs per-field normalized emission. |
| `threshold` | Confidence floors, service thresholds, hard limits, gate requirements. | Existing domain owner. | Often implicit or nested. |
| `source` | Snapshot family, evidence source, source hash, gate adapter source. | Existing source owner. | Needs one visible source field. |
| `updated_at` | Evidence/proposal freshness, snapshot freshness, quality history timestamps. | Existing source owner. | Missing on many operator decision fields. |
| `confidence` | Recommendation, prediction, service, proposal confidence. | Existing domain owner. | Scale must be normalized or labeled. |
| `next_action` | Proposal next step, execution recommended action, channel/user next step. | Operator surface. | Not present in every explainable object. |
| `read_only` | Evidence/proposal/execution/runtime contracts. | Every adapter. | Already common in many surfaces, should be preserved. |
| `authority` | `authority_boundary()`, execution/readiness non-authoritative flags. | Existing governance/authority model. | Needs consistent propagation. |

Recommended canonical shape:

```json
{
  "status": "OK|WARNING|BLOCKED|REVIEW_REQUIRED|UNKNOWN",
  "reason": "plain operator-facing explanation",
  "value": 0,
  "threshold": 0,
  "source": "snapshot-or-evidence-owner",
  "updated_at": "ISO-8601 or empty if unknown",
  "confidence": 0,
  "next_action": "plain safe next step",
  "read_only": true,
  "authority": "existing authority boundary"
}
```

The correct implementation direction is to map existing payloads into this shape where useful. It must not become a new truth source or a new explanation engine.

## 13. Top 10 Reuse Opportunities

| Rank | Opportunity | Value | Risk | Complexity |
| ---: | --- | --- | --- | --- |
| 1 | Reuse `explainability_framework()` as the formal anchor for normalized Why-Card contract. | Very high | Low | Low |
| 2 | Reuse `shadow_recommendation_for_user()` `why_*` fields for user Why-Cards. | Very high | Low | Medium |
| 3 | Reuse `operator_decision_surface.py` user rows as the admin-facing assembler. | Very high | Low | Medium |
| 4 | Reuse channel decision rows and trust recovery payload for channel Why-Cards. | High | Low | Medium |
| 5 | Reuse evidence bundle `source/updated_at/freshness` fields for source visibility. | High | Low | Low |
| 6 | Reuse proposal fields for `next_action`, expected benefit, and rollback hint. | High | Low | Low |
| 7 | Reuse execution readiness/candidate explain fields for governance blockers. | Medium-high | Low | Medium |
| 8 | Reuse diagnostics/target pool for capacity `users/soft/hard/headroom`. | High | Low | Low |
| 9 | Reuse service matrix and routing intelligence for service score/reason/source. | High | Low | Medium |
| 10 | Reuse POOL1/BA6 no-move reason taxonomy as the seed for planner no-move contract. | Very high | Low | Medium |

## 14. Final Verdict

Final verdict: CONTRACT_PARTIALLY_EXISTS.

Evidence:

- `admin_core/intelligence_platform.py` already defines `v7.intelligence.explainability-framework.v1`.
- `admin_core/intelligence_platform.py` already defines generic `v7.intelligence.explainability-payload.v1`.
- Shadow recommendation already answers the required operator questions: `why`, `why_now`, `why_this_channel`, `why_not_current`, `why_confidence`, and `why_risk`.
- Operator decision surface already assembles user and channel recommendation rows with confidence, improvement, risk, trust, prediction, reasons, blockers, source hash, and read-only action chain.
- Evidence, proposal, execution, route, runtime, and diagnostics surfaces all have partial read-only contracts with status, reason, source, freshness, and safety boundaries.

Why not CONTRACT_ALREADY_EXISTS:

- No single payload shape is currently used across trust, risk, prediction, suitability, service, capacity, eligibility, no-move, evidence, proposal, and execution.
- `value`, `threshold`, `source`, `updated_at`, `confidence`, and `next_action` are present in different places but not standardized.
- No-move explanations exist in planner/evidence artifacts, but not as a first-class commercial admin contract.

Why not CONTRACT_MISSING:

- The framework, generic explainability payload, shadow recommendation contract, evidence/proposal contracts, execution explanations, and operator decision rows already exist.
- Implementation can proceed via REUSE + EXTEND, not by creating a new explanation engine.

Recommended next step: standardize a thin read-only canonical adapter around the existing contracts, with `intelligence_platform.explainability_framework()` as the conceptual owner and `operator_decision_surface.py` as the operator-facing assembler.
