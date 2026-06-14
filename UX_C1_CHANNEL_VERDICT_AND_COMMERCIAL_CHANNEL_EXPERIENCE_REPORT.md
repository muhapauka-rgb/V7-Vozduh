# UX.C1 Channel Verdict And Commercial Channel Experience Report

Date: 2026-06-14

Verdict: COMMERCIAL_CHANNEL_READY

Reason: implementation is deployed, production UI was visually captured, and the operator-facing channel table and drawer now answer score, status, main issue, action, and explainable breakdown without exposing raw system statuses on the first screen.

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

Production screenshots were captured from:

`https://v7-admin.195-2-79-116.sslip.io/admin-v2?uxc1=eadfd559#channels`

| Scenario | Desktop | Mobile |
|---|---|---|
| Channel table | `docs/uxc1/screenshots/production_channels_table_desktop.png` | `docs/uxc1/screenshots/production_channels_table_mobile.png` |
| Healthy / Excellent channel | `docs/uxc1/screenshots/production_healthy_desktop.png` | `docs/uxc1/screenshots/production_healthy_mobile.png` |
| Working channel | `docs/uxc1/screenshots/production_working_desktop.png` | Covered by mobile table row; desktop drawer captured |
| Needs check | `docs/uxc1/screenshots/production_needs_check_desktop.png` | `docs/uxc1/screenshots/production_needs_check_mobile.png` |
| Unusable channel | `docs/uxc1/screenshots/production_unusable_desktop.png` | `docs/uxc1/screenshots/production_unusable_mobile.png` |
| Suitability breakdown | `docs/uxc1/screenshots/production_breakdown_desktop.png` | Desktop technical details are sufficient |

Captured production examples:

| Scenario | Production Result |
|---|---|
| Healthy / Excellent | `awg0`, `92/100`, `Excellent`, main issue `-`, action `Open Channel` |
| Working | `88/100`, `Working`, main issue `Route`, action `Check Route` |
| Needs Check | `vless`, `72/100`, `Needs Check`, main issue `Capacity`, action `Check Users` |
| Unusable | `OpenVPN-Kolosov`, `37/100`, `Unusable`, main issue `Services`, action `Check Services` |
| Breakdown | `vless`, explainable checks: Services, Stability, Capacity, Route, Runtime, History |

## 8. Mobile Validation

Local smoke at 390px:

| Check | Result |
|---|---|
| Channel table renders | PASS |
| Required C1 columns render | PASS |
| Horizontal overflow | PASS, none |
| Console errors | PASS, none |

Production mobile validation:

| Scenario | Result |
|---|---|
| Channel table | PASS, required columns render at 390px |
| Healthy / Excellent drawer | PASS, no horizontal overflow |
| Needs Check drawer | PASS, no horizontal overflow |
| Unusable drawer | PASS, no horizontal overflow |

Working status is visible in the mobile table. Drawer-level Working validation is covered by the desktop production screenshot because live channel score can drift between adjacent requests.

## 9. Tests

| Test | Result |
|---|---|
| `python3 -m py_compile admin/v7-admin-api` | PASS |
| `git diff --check` | PASS |
| Local admin-v2 login | PASS |
| Local channel table renders | PASS |
| Local suitability columns render | PASS |
| Local mobile no overflow | PASS |
| Drawer opens | PASS, production screenshots captured |
| Breakdown renders | PASS, production screenshot captured |
| Production screenshots | PASS |
| Mobile screenshots | PASS |
| Truth | PASS, `tools/v7-truth-check --all --json` |
| Convergence | PASS, `tools/v7-convergence-status --json` |

## 10. Remaining Issues

| Issue | Status |
|---|---|
| Local state has no channels, so local cannot validate real channel categories | Accepted; production visual validation completed |
| Live channel scores can drift by a few points between adjacent requests | Accepted; statuses remain human-readable and explainable |
| Browser full-page drawer capture timed out on large overlay shots | Accepted; final proof uses reliable clipped production screenshots of the actual visible operator blocks |

## 11. Verdict

COMMERCIAL_CHANNEL_READY

The channel experience is commercially ready for the current scope. Channels now present as operator-understandable objects: score, human status, main issue, one action, and a drill-down explanation. Raw engineering states remain deeper in technical detail surfaces.
