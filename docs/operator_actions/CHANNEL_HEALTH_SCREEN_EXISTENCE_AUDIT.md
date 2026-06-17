# CHANNEL.HEALTH.1_EXISTENCE_AUDIT

## 1. Saved State

| Check | Value |
| --- | --- |
| Branch | Updatesystem |
| Local HEAD | acafe030f36c9a5a898441502a391bccc53f405b |
| Last commit | acafe030 Separate channel outcomes from causes |
| Git status before audit | Untracked `V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` only |
| Scope | Audit/report only |
| UI changes | None |
| Runtime changes | None |
| Deploy | None |

The untracked handoff document was left untouched.

## 2. Truth Gate

| Gate | Status | Evidence |
| --- | --- | --- |
| `tools/v7-truth-check --all --json` | PASS | `FULLY_ALIGNED`; local, GitHub, and runtime all at `acafe030f36c9a5a898441502a391bccc53f405b` |
| `tools/v7-convergence-status --json` | PASS | `ALIGNED`; no deployment required |
| Non-blocking warning | PASS | `documentation_dirty_ignored` for the existing untracked handoff document |

## 3. Channel Drawer Inventory

Evidence:

- `admin/v7-admin-api:27646` defines `channelAnalysisCard(source)`.
- `admin/v7-admin-api:28260` defines `renderChannelDrawerLive(d)`.

Current Channel Drawer already contains the operator-facing channel model:

| Block | Purpose | Operator Value | Keep |
| --- | --- | --- | --- |
| Channel Model / Decision V7 | Shows assignment decision, reason, and action | High | Yes |
| Technical Health | Shows health score and links to breakdown | Medium | Yes, as secondary |
| Problems | Shows compressed operator problems | High | Yes |
| Working Checks | Shows what is OK | Medium | Yes |
| Details | Contains deeper operational/technical data | Medium | Yes |
| Channel State | Health/service/speed/events snapshot | Medium | Yes, inside details |
| Why Card | Explains channel recommendation | High | Yes |
| Operator Checklist | Health, services, speed, users, profile, logs | Medium | Yes, details only |
| Actions | Existing safe channel actions | High | Yes |
| Lifecycle / Speed / Users / Services / Config / Events | Technical and support data | Low to Medium | Yes, technical depth |

Primary operator questions are already answerable in the drawer:

| Question | Answered In Drawer |
| --- | --- |
| What did V7 decide? | Decision V7 |
| Can this channel be used? | Decision V7 / assignment status |
| What is broken? | Problems |
| Why? | Decision reason / Why Card |
| What should I do? | Decision action / action controls |
| What is the technical health? | Technical Health |

## 4. Health Screen Inventory

Evidence:

- `admin/v7-admin-api:27716` defines `openChannelSuitabilityBreakdown(id)`.
- `admin/v7-admin-api:27629` defines shared `channelSuitabilityBreakdownHtml(source)`.

The Health screen is a compact diagnostic drawer titled `Health score / 100`. It contains:

| Block | Purpose | Operator Value | Technical Value |
| --- | --- | --- | --- |
| Why health X/100? | Channel, status, primary cause, action | Medium | Medium |
| Breakdown | Score/max for Services, Stability, Capacity, Route, Runtime, History | Medium | High |
| Action | Primary diagnostic/action button plus Open Channel | Medium | Medium |

It derives from `channelSuitability(row)`, the same model used by the Channel Drawer. It does not introduce a separate truth source.

## 5. Overlap Analysis

| Health Screen Item | Already Exists In Channel Drawer | Duplication Level |
| --- | --- | --- |
| Health score | Technical Health row | High |
| Human health status | Technical Health row | High |
| Primary cause | Problems / Decision reason / Why | Medium |
| Action | Decision action / action controls | Medium |
| Services check | Details / Services / Operator Checklist | High |
| Stability check | Health breakdown only in compact scored form | Medium |
| Capacity check | Problems / users / assignment context | Medium |
| Route check | Problems / readiness / route details | Medium |
| Runtime check | Details / profile readiness / logs | High |
| History check | Events / logs | High |

The Health screen duplicates the decision surface, but it is still the cleanest single view of the mechanical score decomposition.

## 6. Operator Value Audit

| Operator Goal | Channel Drawer Answers It | Health Screen Adds Value | Health Screen Required |
| --- | --- | --- | --- |
| Understand if channel is usable | Yes | Minor | No |
| Understand assignment decision | Yes | No | No |
| Understand what is broken | Yes | Sometimes, as technical detail | No |
| Choose next action | Yes | Minor | No |
| Explain exact score | Partly | Yes | Diagnostics only |
| Debug why score is low | Partly | Yes | Diagnostics only |
| Support/engineering investigation | Partly | Yes | Diagnostics only |

Operator-first value is mostly covered by the Channel Drawer. The unique Health value is diagnostic: exact score components and per-check mechanics.

## 7. Mechanics vs Outcomes

| Surface | Outcome-Oriented | Mechanics-Oriented | Notes |
| --- | ---: | ---: | --- |
| Channel Drawer Screen 1 | 75% | 25% | Decision, problem, reason, action are primary |
| Channel Drawer Details | 45% | 55% | Useful for investigation but contains technical depth |
| Health Screen | 20% | 80% | Explains score mechanics, not primary operator outcome |

Health explains why a technical score exists. It does not need to be the main operator screen because it starts from mechanics rather than from the operator decision.

## 8. Duplication Audit

| Capability | Duplicated By Channel Drawer | If Health Removed From Primary Flow |
| --- | --- | --- |
| See channel decision | Yes | No loss |
| See assignment action | Yes | No loss |
| See current problems | Yes | No loss |
| See health score | Yes | No loss |
| See services status | Yes | No loss |
| Open service check | Yes | No loss |
| Open users/actions/logs | Yes | No loss |
| See exact score/max breakdown | Partly | Loss of compact diagnostic view |
| See all scoring checks together | Partly | Loss of compact diagnostic view |

Health is redundant as a primary operator destination, but not redundant as a technical diagnostic view.

## 9. Survival Test

Question: if the Health screen disappears, what becomes impossible?

| Capability | Impossible? | Notes |
| --- | --- | --- |
| Understand whether channel is usable | No | Channel Drawer already answers |
| Know what V7 decided | No | Decision V7 already answers |
| Know what action to take | No | Drawer action model already answers |
| See services, users, logs, readiness | No | Existing details remain |
| Explain exact health score components | Partly | Would require browsing several drawer sections |
| Compare Services/Stability/Capacity/Route/Runtime/History in one compact list | Yes | This is the unique Health diagnostic value |

The Health screen does not pass the survival test as a primary operator surface. It does pass as an advanced diagnostic surface.

## 10. Alternative Classification

### Option A: Health Primary Operator Screen

| Criterion | Result |
| --- | --- |
| Operator starts from task/action | No |
| Avoids duplicate channel model | No |
| Reduces cognitive load | No |
| Uses existing truth | Yes |
| Verdict | Reject |

Health should not be a primary operator screen because it competes with the approved Channel Model and starts from a technical score.

### Option B: Health Advanced Diagnostics

| Criterion | Result |
| --- | --- |
| Preserves unique score explanation | Yes |
| Keeps Channel Drawer primary | Yes |
| Avoids new truth source | Yes |
| Supports investigation | Yes |
| Fits current implementation path | Yes |
| Verdict | Accept |

Health should exist as an advanced diagnostic layer reachable from Channel Drawer details / Technical Health / Technical Diagnostics.

### Option C: Remove Entirely

| Criterion | Result |
| --- | --- |
| Simplifies UI | Yes |
| Removes duplication | Yes |
| Loses compact score breakdown | Yes |
| Makes support/debug harder | Yes |
| Verdict | Reject for now |

Complete removal would be too aggressive because the score breakdown is useful when the operator or support needs to explain why a channel scored 18, 72, or 92.

## 11. Final Verdict

`HEALTH_SCREEN_DIAGNOSTICS_ONLY`

The Health screen should exist only as a technical diagnostic view. It should not be presented as a separate primary operator workflow, primary screen, or competing channel truth.

## 12. Recommendation

Keep the Channel Drawer as the primary operator experience:

1. Decision V7
2. Technical Health summary
3. Problems
4. Working checks
5. Details
6. Actions

Keep Health as a deeper diagnostic explanation:

1. Explain why the score is what it is.
2. Show Services / Stability / Capacity / Route / Runtime / History breakdown.
3. Preserve existing safe actions.
4. Do not create a new planner, workflow, storage, truth source, or automation.

Future UI direction:

| Surface | Classification |
| --- | --- |
| Channel Drawer | Primary operator surface |
| Channel Model / Decision V7 | Source of operator action |
| Health score | Secondary summary |
| Health breakdown | Technical diagnostics |
| Services / logs / runtime details | Technical diagnostics |

No UI changes were made in this audit.
