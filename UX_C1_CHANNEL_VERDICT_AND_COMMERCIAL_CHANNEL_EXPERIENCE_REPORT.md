# UX.C1 Channel Verdict And Commercial Channel Experience Report

Date: 2026-06-14

Verdict: CONDITIONAL_PASS

Reason: implementation is complete and local smoke validation passes, but production screenshots will be attached after deploy validation in the next report update.

## 1. Reuse Audit

| Source | Reused | Notes |
|---|---:|---|
| Overview Alerts | Yes | Existing attention/summary signals remain unchanged. |
| User Status | Yes | No user workflow or drawer changes. |
| Channel Status | Yes | Existing health, lifecycle, topology, and pool state are reused. |
| Checks | Yes | Existing service matrix, runtime readiness, load, and diagnosis checks are reused. |
| Why Cards | Yes | Existing `channelWhyCard` remains available in drawer details. |
| Recommendations | Yes | Existing `operatorDecisionSurface.channels_by_id` feeds history/trust. |
| Execution Readiness | Yes | Existing runtime readiness is scored; no execution path was added. |
| Route Problems | Yes | Existing topology grouping feeds route score. |
| Leak Problems | Indirect | No new leak model; existing checks stay in technical/attention surfaces. |
| Capacity Problems | Yes | Existing user count and load limits feed capacity score. |

No new storage, snapshots, APIs, pages, drawers, planners, governance, or execution owners were introduced.

## 2. Verdict Model

Channel verdict is now operator-facing:

| Score | Human Status |
|---:|---|
| 90-100 | Excellent |
| 75-89 | Working |
| 50-74 | Needs Check |
| 0-49 | Unusable |

Raw states such as `TRUSTED`, `WATCH`, and `QUARANTINED` remain reachable only through existing technical details.

## 3. Suitability Formula

| Area | Weight | Existing Signal |
|---|---:|---|
| Services | 30 | `overview.service_matrix`, draft service evidence |
| Stability | 20 | channel health, lifecycle, diagnosis |
| Capacity | 15 | assigned users, soft/hard load limits |
| Route | 15 | existing channel topology state |
| Runtime | 10 | `overview.egress_runtime_readiness` |
| History | 10 | channel decision row and Why Card trust state |
| Total | 100 | Explainable sum |

Each row produces `Check / Score / Max / Why`, exposed by clicking the score.

## 4. Human Status Mapping

The operator table now defaults to:

| Channel | Score | Status | Main Issue | Users | Action |
|---|---:|---|---|---:|---|

Engineering columns remain configurable but are no longer first-screen defaults.

## 5. Channel Table Before/After

| Area | Before | After |
|---|---|---|
| Channel quality | Trust/status split across columns | Single 0-100 score |
| Operator status | `TRUSTED/WATCH/QUARANTINED` plus lifecycle text | `Excellent/Working/Needs Check/Unusable` |
| Main issue | Inferred from services/status/load | Explicit `Main Issue` |
| Action model | Multiple icon actions including admin/destructive commands | One primary operator action |
| Raw metrics | Traffic, service counts, speed visible by default | Hidden behind details/configurable columns |

## 6. Channel Drawer Before/After

| Area | Before | After |
|---|---|---|
| First visible block | Engineering channel snapshot | `CHANNEL ANALYSIS` |
| First answer | Status/service/speed cards | Status, suitability, problems, working checks, next action |
| Why | Full Why Card immediately after snapshot | One-line reason in analysis; full Why Card remains deeper |
| Dangerous actions | Header export/delete visible | Header shows `Details`; admin actions stay deeper |

Drawer screens remain the same existing drawer path:

1. Verdict, score, problem, action, why.
2. Analysis, checks, users, services.
3. Evidence, history, technical data.

## 7. Screenshots

Production screenshot capture is pending deploy validation.

Planned files:

| Scenario | Desktop | Mobile |
|---|---|---|
| Healthy channel | `docs/uxc1/screenshots/production_healthy_desktop.png` | `docs/uxc1/screenshots/production_healthy_mobile.png` |
| Working channel | `docs/uxc1/screenshots/production_working_desktop.png` | `docs/uxc1/screenshots/production_working_mobile.png` |
| Needs check | `docs/uxc1/screenshots/production_needs_check_desktop.png` | `docs/uxc1/screenshots/production_needs_check_mobile.png` |
| Unusable channel | `docs/uxc1/screenshots/production_unusable_desktop.png` | `docs/uxc1/screenshots/production_unusable_mobile.png` |

## 8. Mobile Validation

Local smoke at 390px:

| Check | Result |
|---|---|
| Channel table renders | PASS |
| Required C1 columns render | PASS |
| Horizontal overflow | PASS, none |
| Console errors | PASS, none |

Production mobile validation remains pending deploy screenshots.

## 9. Tests

| Test | Result |
|---|---|
| `python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| Local admin-v2 login | PASS |
| Local channel table renders | PASS |
| Local suitability columns render | PASS |
| Local mobile no overflow | PASS |
| Drawer opens | Pending production data |
| Breakdown renders | Pending production data |
| Production screenshots | Pending deploy |
| Truth | Pending final post-commit check |
| Convergence | Pending final post-commit check |

## 10. Remaining Issues

| Issue | Status |
|---|---|
| Local state has no channels, so local cannot validate real channel categories | Accepted; production validation required |
| Production screenshots not yet attached | Pending |

## 11. Verdict

CONDITIONAL_PASS

Implementation is complete and local smoke validation passes. Final commercial certification requires production deploy and visual evidence for real channels.
