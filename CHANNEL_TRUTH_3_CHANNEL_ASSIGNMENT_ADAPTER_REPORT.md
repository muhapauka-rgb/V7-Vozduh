# CHANNEL.TRUTH.3 Channel Assignment Adapter Report

Project: V7 VOZDUH  
Program: CHANNEL.TRUTH.3_CHANNEL_ASSIGNMENT_ADAPTER  
Date: 2026-06-15  
Branch: Updatesystem  
Runtime commit verified: 01c415a644bbfde3facbf241786e5ebaed61e6f8

## 1. Reuse Map

| Required Source | Reused | Notes |
|---|---:|---|
| Existing planner truth | Yes | Read-only selected moves are exposed through the operator decision surface. |
| Existing governance truth | Yes | Manual-only, reserve-only, canary-reserved, production-assignment flags are reused from channel registry/runtime data. |
| Existing restore/runtime truth | Yes | Existing runtime/registry data remains the only source for channel role and readiness. |
| Existing quality/suitability | Yes | Quality score remains visible and separate from assignment truth. |
| Existing channel table | Yes | Table model extended in place; no new page. |
| Existing channel drawer | Yes | Assignment status added under score; no new drawer. |
| Existing actions | Yes | Existing open/check actions reused. |

No new storage, database, snapshot, planner, governance, workflow, or execution path was created.

## 2. Existing Truth Sources

| Source | Role In Adapter |
|---|---|
| `selected_moves_read_adapter()` | Reads already selected movement truth without applying movement. |
| `operator_decision_surface.batch_preview` | Reuses existing operator preview moves when present. |
| Channel registry flags | Detects manual-only, reserve-only, canary-reserved, and production-assignment disabled channels. |
| Channel user counts | Distinguishes `Keep Only`, `Evacuate`, and empty usable channels. |
| Existing quality model | Still computes `Quality`; not used as a replacement for assignment truth. |

Runtime safety fields exposed by the adapter:

| Field | Value |
|---|---|
| `runtime_mutation_performed` | `false` |
| `new_truth_source_created` | `false` |
| `planner_executed` | `false` |
| `snapshot_written` | `false` |

## 3. Assignment Adapter

Operator-facing statuses:

| Status | Meaning |
|---|---|
| `Use` | No assignment blocker is present, or planner movement targets this channel. |
| `Keep Only` | Current users may stay, but the channel is not presented as a preferred new target. |
| `Evacuate` | Existing selected moves indicate users should leave this channel. |
| `Blocked` | Assignment truth is unavailable or a hard blocker exists. |
| `Emergency Only` | Registry/governance flags indicate manual/reserve/canary/emergency-only use. |

Important visual validation finding:

Initial production screenshot after deploy showed a false `Blocked / Planner truth unavailable` fallback on healthy empty channels. That was corrected in commit `01c415a6`: absence of a selected move for a channel no longer means blocked when the global assignment truth surface is loaded.

## 4. Table Before/After

Before:

| Channel | Trust/Status | Users | Services |
|---|---|---:|---|
| awg0 | Quality/trust wording only | 0 | Service data |

After:

| Channel | Quality | Assignment | Main Blocker | Users | Action |
|---|---:|---|---|---:|---|
| vless | 72/100 | Evacuate | Recommended movement | 11 | Check users |
| awg0 | 92/100 | Use | None | 0 | Open channel |
| awg3 | 72/100 | Evacuate | Recommended movement | 8 | Check users |
| 1 | 79/100 | Emergency Only | Manual only | 0 | Open channel |

The table now separates:

| Concept | Visible As |
|---|---|
| Channel quality | `Quality` score |
| Assignment decision | `Assignment` status |
| Assignment reason | `Main Blocker` |
| Mismatch | Explicit `Quality != Assignment` marker when quality is good but assignment is blocked/evacuate/emergency. |

## 5. Drawer Before/After

Before:

| Drawer Area | Issue |
|---|---|
| Quality score | Visible, but could be mistaken for assignment safety. |
| Trust/recovery fragments | Operator had to infer whether users can be assigned. |
| Raw channel details | Assignment truth was not first-class. |

After:

| Drawer Area | Result |
|---|---|
| Verdict | Quality verdict remains visible. |
| Score | Quality score remains visible. |
| Assignment | New row directly under score. |
| Blocker | New row directly under assignment. |
| Mismatch | Explicit when quality and assignment disagree. |
| Details | Existing technical content remains deeper. |

## 6. Production Screenshots

Evidence folder:

`docs/channel_truth_3/screenshots/`

| Screenshot | File |
|---|---|
| Desktop table | `production_channels_table_desktop.png` |
| Desktop drawer | `production_channel_drawer_desktop.png` |
| Mobile table | `production_channels_table_mobile.png` |
| Mobile drawer | `production_channel_drawer_mobile.png` |
| Validation data | `production_validation.json` |

Production URL used for capture:

`https://v7-admin.195-2-79-116.sslip.io/admin-v2?cb=01c415a6#overview`

## 7. Mobile Validation

| Check | Result |
|---|---|
| Viewport | 390 x 844 |
| Table visible | PASS |
| Drawer visible | PASS |
| Horizontal overflow | PASS, `false` |
| Drawer horizontal overflow | PASS, `false` |
| Assignment visible in drawer | PASS |
| Buttons clipped | PASS |

The mobile table uses compact truncated columns instead of horizontal page overflow. The drawer keeps assignment directly below score and remains usable at phone width.

## 8. Consistency Audit

| Requirement | Status |
|---|---|
| Quality remains visible | PASS |
| Assignment truth added, not replacing quality | PASS |
| `Quality != Assignment` surfaced | PASS |
| Channel table uses target model | PASS |
| Channel drawer places assignment under score | PASS |
| Existing drawer reused | PASS |
| Existing actions reused | PASS |
| No new endpoint owner | PASS |
| No planner execution | PASS |
| No runtime mutation | PASS |
| No new snapshot write | PASS |

## 9. Duplication Audit

| Possible Duplication | Result |
|---|---|
| New quality model | None created. |
| New assignment source | None created. |
| New planner | None created. |
| New table workflow | None created. |
| New drawer | None created. |
| New execution action | None created. |
| New storage/snapshot | None created. |

## 10. Remaining Issues

| Issue | Severity | Notes |
|---|---|---|
| Some assignment reason labels remain English | P3 | Status vocabulary was specified in English; blocker labels are operator-safe but can later be localized if desired. |
| Dense mobile table truncates long labels | P3 | No horizontal overflow; drawer provides full detail. |
| `candidate.blocked` is not recalculated by the page | P2 | Intentional. The page does not run planner or write snapshots. It displays existing read-only selected moves and registry/governance blockers. |

## 11. Final Verdict

`CHANNEL_TRUTH_ALIGNED`

Reason:

The admin now exposes channel assignment truth as a separate operator-facing layer next to quality score, using existing read-only V7 truth. The implementation avoids new truth sources, avoids planner execution, avoids storage/snapshot writes, and production screenshots confirm the table and drawer behavior on desktop and mobile.

