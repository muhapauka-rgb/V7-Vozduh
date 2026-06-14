# CHANNEL.TRUTH.3A Visual Truth Validation Report

Project: V7 VOZDUH  
Program: CHANNEL.TRUTH.3A_VISUAL_TRUTH_VALIDATION  
Date: 2026-06-15  
Mode: validation only, no code changes, no deploy, no commits

## 1. Screenshot Gallery

Evidence folder:

`docs/channel_truth_3a/screenshots/`

| Evidence | File |
|---|---|
| Desktop table | `desktop_table.png` |
| Mobile table | `mobile_table.png` |
| Mobile drawer | `mobile_awg0_drawer.png` |
| vless table row | `row_vless_evacuate.png` |
| awg0 table row | `row_awg0_use.png` |
| awg3 table row | `row_awg3_keep_only.png` |
| channel 1 table row | `row_channel_1_emergency_mismatch.png` |
| vless drawer screen 1 | `drawer_vless_screen1.png` |
| vless drawer details | `drawer_vless_details.png` |
| awg0 drawer screen 1 | `drawer_awg0_screen1.png` |
| awg0 drawer details | `drawer_awg0_details.png` |
| awg3 drawer screen 1 | `drawer_awg3_screen1.png` |
| awg3 drawer details | `drawer_awg3_details.png` |
| channel 1 drawer screen 1 | `drawer_channel_1_screen1.png` |
| channel 1 drawer details | `drawer_channel_1_details.png` |
| Validation JSON | `validation_summary.json` |

Truth gate before capture:

| Gate | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS |
| `tools/v7-convergence-status --json` | PASS |

## 2. Table Validation

Question: can operator answer immediately how good the channel is, whether V7 can use it, and why?

| Channel | Quality Visible | Assignment Visible | Blocker Visible | PASS |
|---|---:|---:|---:|---:|
| vless | Yes, `68/100` | Yes, `Evacuate` | Yes, `Recommended movement` | PASS |
| awg0 | Yes, `92/100` | Yes, `Use` | Yes, `None` | PASS |
| awg3 | Yes, `72/100` | Yes, `Keep Only` | Yes, `None` | PASS with concern |
| 1 | Yes, `79/100` | Yes, `Emergency Only` | Yes, `Manual only` | PASS |
| OpenVPN-Kolosov | Yes, `37/100` | Yes, `Emergency Only` | Yes, `Manual only` | PASS |

Important observation:

On a fresh load, table initially showed `Blocked / Assignment truth unavailable` for several rows. After the assignment surface stabilized, real statuses appeared. This means truth is visible, but initial loading can temporarily look like a hard planner verdict.

## 3. Drawer Validation

Question: can operator answer in 5 seconds: how good, can receive users, can keep users, should users leave, why?

| Channel | Quality | Assignment | Blocker | PASS |
|---|---|---|---|---:|
| vless | `68/100`, requires check | `Evacuate` | `Recommended movement` | PASS |
| awg0 | `92/100`, excellent | `Use` | `None` | PASS |
| awg3 | `72/100`, requires check | `Keep Only` | `None` | PARTIAL |
| 1 | `79/100`, working | `Emergency Only` | `Manual only` | PASS |

The drawer does expose the story order:

`Quality -> Assignment -> Blocker -> Problem -> Action`

But details still contain technical terms deeper down.

## 4. Quality vs Assignment Audit

| Channel | Mismatch Visible? | PASS |
|---|---:|---:|
| 1 | Yes: `Emergency Only`, `Manual only`, `Качество не равно назначению` | PASS |
| OpenVPN-Kolosov | No mismatch expected because quality is low | PASS |
| awg0 | No mismatch expected because quality and assignment agree | PASS |

Mismatch is obvious in the drawer for channel `1`:

`Оценка 79 / 100`  
`Назначение Emergency Only`  
`Блокер Manual only`  
`Расхождение Качество не равно назначению`

Concern:

The explanation line still includes English technical phrasing: `Quality score good, planner assignment blocked.`

## 5. Blocker Audit

| Blocker / Text | Human Readable? |
|---|---:|
| `Manual only` | Mostly readable, but English |
| `Recommended movement` | Partial; operator can infer movement, but not why |
| `None` | Yes |
| `planner truth` | No, technical |
| `quality score conflicts with planner truth` | No, technical |
| `curl_failed_and_handshake_stale` in details | No, raw technical value |

Bad raw planner reasons like `avg_mbps_below_floor`, `stability_below_floor`, or `candidate_blocked` were not visible in first-screen rows. However, deeper details still expose technical health/action text.

## 6. Evacuation Audit

| Channel | Evacuation Obvious? |
|---|---:|
| vless | PASS, table and drawer show `Evacuate` |
| awg3 | FAIL for requested expectation: current production shows `Keep Only`, not `Evacuate` |

This does not prove the adapter is fake, but it means the operator cannot assume all overloaded/problem channels are evacuation channels. `awg3` still requires interpretation.

## 7. Assignable Audit

| Channel | Assignment Obvious? |
|---|---:|
| awg0 | PASS, table and drawer show `Use` |

Concern:

The reason says `10 selected moves target this channel`. This does expose planner-derived truth, not only a label. It is still English and could be made more operator-native later.

## 8. Emergency Audit

| Channel | Emergency Visible | Why Visible | PASS |
|---|---:|---:|---:|
| 1 | Yes, `Emergency Only` | Yes, `Manual only` | PASS |
| OpenVPN-Kolosov | Yes, `Emergency Only` | Yes, `Manual only` | PASS |
| wg wireguard channel | Yes, `Emergency Only` | Yes, `Manual only` | PASS |

Emergency-only state is clearly visible. The reason is understandable enough, but still English.

## 9. Mobile Audit

Viewport: 390 x 844.

| Check | Result |
|---|---:|
| Quality visible | PASS |
| Assignment visible | PASS |
| Blocker visible | PASS |
| No horizontal overflow | PASS |
| No clipping in awg0 drawer | PASS |

Mobile table compresses text with truncation, but does not overflow. Drawer first screen is readable and keeps quality, assignment, blocker, and action visible.

## 10. Story Audit

| Channel | Quality -> Assignment -> Blocker -> Action | PASS |
|---|---|---:|
| vless | `68/100 -> Evacuate -> Recommended movement -> Check users` | PASS |
| awg0 | `92/100 -> Use -> None -> No action required` | PASS |
| awg3 | `72/100 -> Keep Only -> None -> Check users` | PARTIAL |
| 1 | `79/100 -> Emergency Only -> Manual only -> Open channel/check services` | PASS |

If a channel has a clean `Use`, `Evacuate`, or `Emergency Only`, the operator can understand the main truth quickly. `Keep Only` plus `None` blocker on a channel with overload/problem language is less obvious.

## 11. Before/After

| Question | Before | After |
|---|---|---|
| Can use? | Inferred from trust/status/quality | Visible as `Use` |
| Must evacuate? | Not first-class | Visible as `Evacuate` when selected moves exist |
| Blocked? | Mixed with quality/trust | Visible, but current sample had no stable blocked row |
| Emergency only? | Hidden in registry/governance detail | Visible as `Emergency Only` |
| Why? | Scattered metrics/reasons | Visible as `Blocker`, but some language is still technical |

## 12. Remaining Problems

| Problem | Severity | Evidence |
|---|---|---|
| Initial loading can show `Assignment truth unavailable` as `Blocked` | P1 | Fresh page showed unavailable state before stabilizing. |
| `awg3` expected evacuation audit target shows `Keep Only` | P1 | Table and drawer show `Keep Only / None`, not `Evacuate`. |
| Some blocker/reason text remains English/technical | P2 | `Recommended movement`, `planner truth`, `quality score conflicts with planner truth`, `curl_failed_and_handshake_stale`. |
| Details capture is dense | P3 | Details are available, but not as clean as screen 1. |

## 13. Final Verdict

`PARTIALLY_VISIBLE`

Answer to the most important question:

We did expose real planner/assignment truth in the UI, not only another static label. Evidence: `Evacuate` appears for vless with selected users leaving, `Use` appears for awg0 with selected moves targeting it, and `Emergency Only` appears with registry/governance blocker `Manual only`.

But the result is not clean enough for `TRUTH_VISIBLE` because initial loading can temporarily present assignment truth as unavailable/blocked, `awg3` does not satisfy the requested evacuation expectation, and several blocker/reason phrases still require V7 internal knowledge.

