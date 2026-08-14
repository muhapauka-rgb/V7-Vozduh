# EXPLAINABILITY.2 CANONICAL ADAPTER AND WHY CARD FOUNDATION REPORT

Date: 2026-06-14

Mode: Phase 1 explainability foundation. Read-only. No apply. No user movement. No route mutation. No policy mutation. No deployment.

## 1. Discovery

Truth gate was executed before implementation.

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS / FULLY_ALIGNED |
| `tools/v7-convergence-status --json` | PASS / ALIGNED |

Existing contracts and surfaces reused:

| Existing source | Reused for | Extension |
| --- | --- | --- |
| `admin_core.intelligence_platform.explainability_framework()` | Existing explainability boundary and authority vocabulary | Adapter emits the required canonical metric fields without changing this contract |
| `admin_core.intelligence_platform.authority_boundary()` | Read-only authority and source semantics | Copied into every card as authority metadata |
| `admin_core.operator_decision_surface` | Existing operator-facing truth aggregation | Added `why_cards` to the existing decision-surface response |
| Existing candidate/user recommendation rows | User status, reasons, confidence, risk, trust, blockers | Normalized into compact user why cards |
| Existing channel decision rows | Channel state, reason, users, limits, service score, stability | Normalized into compact channel why cards |
| Existing batch preview | Planner candidate move count | Normalized into planner why card and no-move reason counts |

No new engine, planner, governance layer, route policy, storage, snapshot, runtime state, or truth source was created.

## 2. Adapter

Implemented `admin_core/explainability_adapter.py` as a thin read-only adapter over existing rows and snapshot status metadata.

Canonical metric shape:

| Field | Source |
| --- | --- |
| `status` | Existing recommendation/channel/planner state |
| `reason` | Existing reasons, blockers, state reasons, or no-move classifier |
| `value` | Existing numeric value; `null` when unavailable |
| `threshold` | Existing policy/contract threshold where known; `null` when unavailable |
| `source` | Existing snapshot or decision-surface family |
| `updated_at` | Existing freshness timestamp when present; otherwise `null` |
| `confidence` | Existing row or snapshot confidence |
| `next_action` | Existing operational next step or `none` |
| `read_only` | Always `true` |
| `authority` | Existing authority boundary |

Thresholds were not invented as runtime truth. They are adapter constants mapped from existing contracts/policies:

| Adapter threshold | Existing meaning |
| --- | --- |
| `80.0` service score | Existing service suitability threshold used by service scoring |
| `0.45` stability | Existing stability lower bound used by policy/autoswitch logic |
| `0.60` recommendation confidence | Existing recommendation confidence floor |
| `1.0` improvement score | Existing move-benefit floor used by decision surface logic |

Unavailable values remain `null`.

## 3. User Why Card

Added user why cards to the existing decision surface payload.

Example shape:

```json
{
  "schema": "v7.explainability.why-card.user.v1",
  "object_type": "user",
  "current_channel": "awg3",
  "recommended_channel": "awg3",
  "recommended_state": "KEEP",
  "reason": "sticky/current route kept",
  "metrics": [
    {
      "status": "ok",
      "reason": "recommendation confidence",
      "value": 0.94,
      "threshold": 0.6,
      "source": "candidate-suitability-summary",
      "updated_at": null,
      "confidence": 0.94,
      "next_action": "none",
      "read_only": true,
      "authority": {}
    }
  ],
  "required_to_move": [],
  "read_only": true
}
```

The card shows why the user is kept or recommended to move, which metrics support that decision, and what is still required for movement.

## 4. Channel Why Card

Added channel why cards to the existing decision surface payload.

Example shape:

```json
{
  "schema": "v7.explainability.why-card.channel.v1",
  "object_type": "channel",
  "channel": "awg3",
  "state": "Good",
  "reason": "service score and trust evidence are strong",
  "users": 8,
  "soft_limit": 19,
  "hard_limit": 24,
  "headroom": 16,
  "metrics": [],
  "read_only": true
}
```

The card exposes channel capacity, service score, stability, source family, and recommended next action without changing any channel state.

## 5. Planner Why Card

Added planner why card to the existing operator execution dashboard.

Example shape:

```json
{
  "schema": "v7.explainability.why-card.planner.v1",
  "candidate_moves_total": 0,
  "reason_counts": {
    "sticky_keep_current": 1
  },
  "summary": "No user movement candidates. Main reason: sticky_keep_current.",
  "read_only": true
}
```

The planner card summarizes whether there are movement candidates and why users are not moving.

## 6. No Move Explanation

No-move explanations are derived from existing operator decision rows and existing batch preview data.

Classifier buckets:

| Bucket | Meaning |
| --- | --- |
| `current_is_best` | Existing recommendation keeps the user on the current channel |
| `sticky_keep_current` | Existing reasons mention sticky/current-route preservation |
| `blocked_by_capacity` | Existing blockers mention capacity/limit constraints |
| `blocked_by_service` | Existing blockers mention service/suitability constraints |
| `blocked_by_stability` | Existing blockers mention stability constraints |
| `blocked_by_governance` | Existing blockers mention policy/governance constraints |
| `blocked_by_reserve` | Existing blockers mention reserve constraints |

This is not a planner and does not make movement decisions. It only labels already-produced decision rows for operator readability.

## 7. Duplication Audit

| Meaning | Canonical owner reused | Duplicate created |
| --- | --- | --- |
| User recommendation | Existing decision-surface user rows | No |
| Channel state | Existing decision-surface channel rows | No |
| Batch movement preview | Existing batch preview | No |
| Confidence | Existing row/snapshot confidence | No |
| Trust/risk/improvement | Existing user row values | No |
| Service score/stability | Existing channel service/state fields | No |
| Authority | Existing `authority_boundary()` | No |
| Runtime apply/move | Existing runtime systems only | No |

## 8. Tests

| Test | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS |
| `tools/v7-convergence-status --json` | PASS |
| Adapter smoke test with sample user/channel/planner data | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin_core/explainability_adapter.py admin_core/operator_decision_surface.py admin/v7-admin-api` | PASS |

No deployment was performed. No runtime state was changed. No user movement was executed.

## 9. Screens Modified

| Screen/surface | Modification |
| --- | --- |
| Existing `/api/operator/decision-surface` payload | Added `why_cards` |
| User drawer | Added compact user why card |
| User recommendation drawer | Added compact user why card; raw reasons remain available |
| Channel drawer | Added compact channel why card |
| Channel state drawer | Added compact channel why card |
| Planner/operator execution dashboard | Added compact planner why card and no-move reason counts |

No new screen was created.

## 10. Final Verdict: PASS

Phase 1 explainability foundation is implemented as a read-only adapter and compact UI cards over existing contracts. The operator can now answer why a user is kept/moved, why a channel has its current state, and why no moves are proposed from the existing decision surface without opening logs or hunting through multiple evidence screens.
