# CHANNEL.TRUTH.1 Full Decision Pipeline And Score Alignment Audit

Date: 2026-06-15

Program: CHANNEL.TRUTH.1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT

Final Verdict: SCORE_UNSAFE

## 1. Current Saved State

| Check | Result |
| --- | --- |
| Workspace | `/Users/ponch/Documents/New project` |
| Branch | `Updatesystem` |
| HEAD before audit | `56f80750 Add channel polish validation report` |
| Git status before audit | Only `V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md` untracked |
| Uncommitted approved UX/channel work | None |
| Runtime mutation | None |
| UI change | None |
| Score formula change | None |

The untracked handoff document was not part of this task and was not committed.

## 2. Truth/Convergence Gate

Initial gate:

| Gate | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS |
| `tools/v7-convergence-status --json` | PASS after single re-run |

One parallel convergence run hit a transient nested GitHub read failure. A single follow-up run returned `PASS`, `status=ALIGNED`, GitHub/local at `56f8075096954472f1777b831de55a4e2ff9db5b`, production runtime at `566ee5122c70f731e536bec84e75d4db90f994c4`, and the mismatch was classified as docs-only.

## 3. Existing Tool/Code Owner Map

| Area | Existing Owner | File/Function | Reuse? | Gap |
| --- | --- | --- | --- | --- |
| Channel UI score | Admin UI | `admin/v7-admin-api`, `channelSuitability` | Reuse for display only | Does not include planner hard gates |
| Channel verdict | Admin UI | `channelSuitabilityStatus` | Reuse label language | Verdict can contradict assignment eligibility |
| Channel table rendering | Admin UI | `channelSuitabilityCell`, `channelCommercialStatusCell`, `channelMainIssueCell` | Reuse | Needs future assignment column |
| Channel drawer analysis | Admin UI | `channelAnalysisCard`, `channelSuitabilityBreakdownHtml` | Reuse | Needs hard-gate-first model later |
| Planner decision | Runtime planner | `tools/v7-users-autoswitch` | Reuse as authority | Dry-run may write reconnect observation unless redirected |
| Candidate selection | Runtime planner | `tools/v7-users-autoswitch` candidates / selected moves | Reuse | Planner score is not normalized 0-100 UI score |
| Routing intelligence | Advisory only | `admin_core/routing_brain.py` | Reuse as advice | Import unavailable in copied local preview |
| Operator decision surface | Read model | `admin_core/operator_decision_surface.py` | Reuse | CTR snapshots missing/UNKNOWN in planner preview |
| Governance checks | Existing governance | `tools/v7-control-plane-governance-check` | Reuse | Global gate, not per-channel assignment answer |
| Restore barrier | Existing gate | `tools/v7-restore-settle-gate` | Reuse | Execution gate, not UI score input today |
| Autoswitch safety | Read-only review | `tools/v7-autoswitch-safety-review` | Partial | On copied registry, reported `enabled_egress=0`; parser gap |
| Service matrix | Runtime truth file/tool | `service-matrix.json`, `tools/v7-service-matrix-test` | Reuse | UI uses generic count; planner uses required/profile semantics |
| Capacity/load | Runtime planner | `capacity_decision` in candidates | Reuse | UI overload wording does not mean planner hard block |
| Trust/recovery | CTR/intelligence | `trust-evolution-summaries`, CTR advisory | Reuse later | Current preview reports CTR `UNKNOWN` |
| Runtime readiness | Admin/runtime | `egress_runtime_readiness`, planner health/severity | Reuse | UI readiness and planner health are not unified |
| Route safety | Runtime policy/service-aware routing | route class fitness and policy tools | Reuse | UI route score is generic; planner route class is profile-specific |

## 4. Full Decision Pipeline Map

Observed decision chain:

1. Raw channel identity from `egress.registry`.
2. Enabled/disabled state from `egress.registry`.
3. Runtime health/severity inside `tools/v7-users-autoswitch`.
4. Service truth from `service-matrix.json`.
5. Required/profile service compatibility from candidate `service_suitability`.
6. Speed and stability floor gates from planner quality decision.
7. Capacity/load from candidate `capacity_decision`.
8. Manual/reserve/canary reservation gates from registry.
9. Route class compatibility from route-class fitness and service-aware routing.
10. Trust/recovery advisory from CTR snapshots where available.
11. Planner eligibility and ranking in `tools/v7-users-autoswitch`.
12. Selected moves in planner dry-run.
13. Governance/approval chain outside direct planner selection.
14. Restore barrier before execution.
15. Execution readiness remains governed and was not executed.

Important separation:

| Layer | Meaning | Current Source |
| --- | --- | --- |
| Channel Quality | Technical health/readability score | Admin `channelSuitability` |
| Assignment Eligibility | Can V7 assign users now | `tools/v7-users-autoswitch` candidates |
| Retention Eligibility | Can current users safely stay | Planner selected moves / blockers |
| Evacuation Need | Should users move away | Planner selected moves |
| Execution Readiness | Can an approved action run | Governance + restore barrier + execution packet |

## 5. Hard Gates Matrix

| Gate | Source | Hard/Soft | Blocks Assignment | Blocks Retention | Blocks Execution |
| --- | --- | --- | --- | --- | --- |
| disabled | `egress.registry`, runtime readiness | Hard | Yes | Conditional | Yes |
| manual_only | `egress.registry` | Hard | Yes | No | Yes |
| reserve_only | `egress.registry` | Hard | Yes | Conditional | Yes |
| canary_reserved_production_assignment_blocked | Planner candidate gate | Hard | Yes | Conditional | Yes |
| production_assignment_allowed=false | `egress.registry` | Hard | Yes | Conditional | Yes |
| health_code_000 | Planner health gate | Hard | Yes | No | Yes |
| severity_FAIL | Planner severity gate | Hard | Yes | No | Yes |
| telegram_required_telegram_down_14s | Service suitability / Telegram truth | Hard | Yes | No | Yes |
| avg_mbps_below_floor | Planner quality gate | Hard | Yes | Conditional | Yes |
| min_mbps_below_floor | Planner quality gate | Hard | Yes | Conditional | Yes |
| stability_below_floor | Planner quality gate | Hard | Yes | Conditional | Yes |
| route_class_*_failed_nonpersistent_service_truth | Service-aware route class | Soft/Hard by profile | Yes | Conditional | Yes |
| restore_barrier_active | Restore barrier | Hard for execution | No | No | Yes |
| governance_bypass | Operator/governance model | Hard for direct execution | No | No | Yes |

## 6. Channel By Channel Audit

| Channel | UI Score | UI Verdict | Real Eligibility | Receive Users | Keep Users | Move Away | Hard Gate | Planner Reason | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `vless` | 72 | Требует проверки | NOT_ELIGIBLE | No | No | Yes, 10 moves | `min_mbps_below_floor` | `min_mbps_below_floor`, `stability_below_floor` | DO_NOT_ASSIGN_EVACUATE |
| `awg0` | 92 | Отличный | NOT_ELIGIBLE | No | N/A | Yes | `min_mbps_below_floor` | `min_mbps_below_floor`, `stability_below_floor` | DO_NOT_ASSIGN_UI_MISMATCH |
| `awg3` | 72 | Требует проверки | NOT_ELIGIBLE | No | No | Yes, 8 moves | `stability_below_floor` | `stability_below_floor` | DO_NOT_ASSIGN_EVACUATE |
| `1` | 79 | Рабочий | NOT_ELIGIBLE | No | N/A | Yes | `health_code_000` | `severity_FAIL`, Telegram down, speed floor | DO_NOT_ASSIGN |
| `openvpn-1779388847-d2ad7c` | 37 | Непригоден | NOT_ELIGIBLE | No | N/A | Yes | `health_code_000` | `severity_FAIL`, Telegram down, speed floor | DO_NOT_ASSIGN |
| `wireguard-1779454504-c43409` | 72 | Требует проверки | ELIGIBLE | Yes | Yes | N/A | None | Best available pool rank 1 | USE |
| `amneziawg-exec-20260528-10-8-1-14` | 92 | Отличный | NOT_ELIGIBLE | No | N/A | Conditional | `manual_only` | `manual_only`, `reserve_only`, canary reserved | EMERGENCY_ONLY |

Planner dry-run selected 18 moves:

| From | To | Count | Reason |
| --- | --- | --- | --- |
| `vless` | `wireguard-1779454504-c43409` | 10 | `current_egress_not_eligible` |
| `awg3` | `wireguard-1779454504-c43409` | 8 | `current_egress_not_eligible` |

## 7. UI Score vs Real Pipeline Comparison

| Channel | UI Says | Pipeline Says | Mismatch Type | Risk |
| --- | --- | --- | --- | --- |
| `awg0` | 92 / Excellent | Do not assign | UI excellent but planner blocks | CRITICAL |
| `amneziawg-exec-20260528-10-8-1-14` | 92 / Excellent | Emergency/reserve only | UI excellent but assignment forbidden | CRITICAL |
| `1` | 79 / Working | Do not assign | UI working but planner blocks | CRITICAL |
| `wireguard-1779454504-c43409` | 72 / Requires check | Only eligible production target | UI under-rates actual usable target | MEDIUM |
| `vless` | 72 / Requires check | Do not assign and evacuate | UI soft warning, planner hard retention issue | HIGH |
| `awg3` | 72 / Requires check | Do not assign and evacuate | UI soft warning, planner hard retention issue | HIGH |
| `openvpn-1779388847-d2ad7c` | 37 / Unusable | Do not assign | Aligned directionally | MEDIUM |

Current score is commercially readable but not truthful as an assignment verdict.

## 8. Assignment / Retention / Evacuation Model

Future model must not collapse these into one number:

| Dimension | Meaning | Source |
| --- | --- | --- |
| Technical Quality | How good the channel looks technically | Service matrix, health, route, capacity, runtime |
| Assignment Eligibility | Whether V7 may assign new users now | Planner hard gates and policy restrictions |
| Retention Eligibility | Whether current users can safely stay | Planner selected moves and hard blockers |
| Evacuation Need | Whether users should leave channel | Planner selected failover moves |
| Execution Readiness | Whether an approved action can run | Governance, restore barrier, execution packet |

For this production snapshot:

| Category | Channels |
| --- | --- |
| Assignable | `wireguard-1779454504-c43409` |
| Keep allowed | `wireguard-1779454504-c43409` |
| Evacuate | `vless`, `awg3` |
| Do not assign | `1`, `openvpn-1779388847-d2ad7c`, `awg0` |
| Emergency/reserve only | `amneziawg-exec-20260528-10-8-1-14` |

## 9. Mismatch Detection

Detected mismatches:

1. `awg0`: UI `Отличный 92/100`; planner blocks on speed/stability floors.
2. `amneziawg-exec-20260528-10-8-1-14`: UI `Отличный 92/100`; planner blocks production assignment because it is manual/reserve/canary/execution-only.
3. `1`: UI `Рабочий 79/100`; planner blocks with `health_code_000`, `severity_FAIL`, Telegram hard gate, speed floors.
4. `wireguard-1779454504-c43409`: UI `Требует проверки 72/100`; planner selects it as the only target for 18 moves.
5. `vless`: UI `Требует проверки`; planner says existing users should move away.
6. `awg3`: UI `Требует проверки`; planner says existing users should move away.

Critical pattern: UI score currently answers "how good does the channel look in the drawer/table?" but the operator needs "can V7 actually use this channel now?"

## 10. Safety Risk Classification

| Risk | Channels | Reason |
| --- | --- | --- |
| CRITICAL | `awg0`, `1`, `amneziawg-exec-20260528-10-8-1-14` | UI can imply assignment safety while planner blocks assignment |
| HIGH | `vless`, `awg3` | UI soft-warning language underplays evacuation need |
| MEDIUM | `wireguard-1779454504-c43409`, `openvpn-1779388847-d2ad7c` | One under-rated eligible channel; one directionally aligned unusable channel |
| LOW | None | No fully aligned healthy/eligible channel presentation |

## 11. Automated Commands Run

| Command | Purpose | Mutation |
| --- | --- | --- |
| `git status --short` | Saved state | None |
| `git branch --show-current` | Saved state | None |
| `git log -1 --oneline` | Saved state | None |
| `tools/v7-truth-check --all --json` | Truth gate | None |
| `tools/v7-convergence-status --json` | Convergence gate | None |
| `tools/v7-runtime-tool-enumerate --pretty` | Tool inventory | None |
| `tools/v7-admin-endpoint-inventory --out ...` | Admin endpoint inventory | Writes evidence file only |
| `tools/v7-observability-summary --state-dir /private/tmp/... --pretty` | Copied-state observability | Writes evidence file only |
| `tools/v7-autoswitch-safety-review --state-dir /private/tmp/... --pretty` | Read-only safety review | Writes evidence file only |
| `tools/v7-users-autoswitch --state-dir /private/tmp/... --reconnect-state-file /private/tmp/... --pre-planner-refresh off --pretty` | Planner preview on copied state | Writes temp reconnect state only, not runtime |
| `tools/v7-control-plane-governance-check --pretty` | Governance evidence | Writes evidence file only |
| `tools/v7-restore-settle-gate --json --state-dir /private/tmp/...` | Restore barrier evidence | Writes evidence file only |

Authenticated admin API was not used because `/login` writes an admin audit event. Visual UI score evidence came from the already captured production screenshot `docs/uxc1_polish/screenshots/production_table_desktop.png`.

## 12. Evidence Files

| Evidence | File |
| --- | --- |
| Reduced channel pipeline audit | `docs/channel_truth_1/evidence/channel_pipeline_audit_summary.json` |
| Planner preview | `docs/channel_truth_1/evidence/autoswitch_planner_preview.json` |
| Observability summary | `docs/channel_truth_1/evidence/observability_summary.json` |
| Autoswitch safety review | `docs/channel_truth_1/evidence/autoswitch_safety_review.json` |
| Control-plane governance check | `docs/channel_truth_1/evidence/control_plane_governance_check.txt` |
| Restore settle gate | `docs/channel_truth_1/evidence/restore_settle_gate.json` |
| Runtime tool inventory | `docs/channel_truth_1/evidence/runtime_tool_enumerate.txt` |
| Admin endpoint inventory | `docs/channel_truth_1/evidence/admin_endpoint_inventory.json` |

Evidence caveats:

| Caveat | Impact |
| --- | --- |
| `v7-autoswitch-safety-review` reported `enabled_egress=0` on copied registry | Parser/read-model gap; not used for per-channel eligibility |
| Routing brain import unavailable in local copied-state planner preview | Planner still produced authoritative candidates; RI advisory is absent |
| CTR state was `UNKNOWN` in planner preview | Future formula must not pretend trust/recovery is present |
| Admin API login avoided | Prevented audit-log mutation; UI score taken from production screenshot evidence |

## 13. Future Score Model Recommendation

Do not make the visible `Оценка` the assignment truth. Use hard gates first, then score.

Recommended model:

| Component | Weight | Source | Why | Operator Meaning |
| --- | --- | --- | --- | --- |
| hard_gate_status | Gate, no weight | Planner blockers, registry restrictions, restore/governance gates | Hard gates override score | Can this channel be used at all? |
| assignment_status | Gate, no weight | `tools/v7-users-autoswitch` eligibility | Assignment is not the same as quality | Can V7 assign new users now? |
| technical_quality_score | 25 | Service matrix, health, speed, stability | Keep quality visible | How technically good is it? |
| service_suitability_score | 20 | Candidate `service_suitability` | Required/profile services decide usability | Does it serve the needed traffic? |
| capacity_score | 10 | Candidate `capacity_decision` | Avoid overload | Is there headroom? |
| trust_recovery_score | 10 | CTR/trust/recovery snapshots | Prevent premature reuse | Is recovery cleared? |
| route_runtime_score | 15 | Runtime readiness, route class fitness | Route safety is a hard dependency | Is route/runtime safe? |
| history_score | 5 | Quality history, recent failures | Smooth noisy checks | Has it behaved recently? |
| planner_alignment_score | 10 | Planner eligible/rank/selected moves | Align UI with real decision owner | Does planner agree? |
| governance_alignment_score | 5 | Governance/restore/execution readiness | Prevent direct execution bypass | Can action proceed safely? |

Display rule:

If any hard gate fails:

`assignment_status = BLOCKED / DO_NOT_ASSIGN / KEEP_ONLY / EMERGENCY_ONLY`

and the quality score remains visible only as `technical_quality_score`, not as the operator verdict.

## 14. Future Admin Presentation Recommendation

Future table should become:

| Channel | Quality | Assignment | Main Blocker | Users | Action |
| --- | --- | --- | --- | --- | --- |
| `wireguard-1779454504-c43409` | 72 | Eligible | None | 8 | Open |
| `awg0` | 92 | Do Not Assign | Stability floor | 0 | Details |
| `1` | 79 | Blocked | Health/Telegram | 0 | Check services |
| `vless` | 72 | Evacuate | Speed/stability floor | 10 | Review moves |
| `awg3` | 72 | Evacuate | Stability floor | 8 | Review moves |
| `amneziawg-exec-...` | 92 | Emergency Only | Reserved execution channel | 0 | Details |

Screen 1 must answer assignment truth first:

1. Assignment status
2. Main blocker
3. Existing users safe?
4. Planner action
5. Technical quality score

## 15. Implementation Plan For Next Step

No implementation in this task.

Recommended next implementation phases:

| Phase | Change | Risk | Complexity |
| --- | --- | --- | --- |
| 1 | Add read-only channel assignment adapter from existing planner/candidate evidence | Medium | Medium |
| 2 | Extend admin channel table with `Assignment` and `Main Blocker`; keep current quality score | Medium | Medium |
| 3 | Update channel drawer Screen 1: hard gate first, score second | Medium | Medium |
| 4 | Add automated regression fixture from `channel_pipeline_audit_summary.json` | Low | Low |
| 5 | Add safety copy for CTR UNKNOWN and routing brain unavailable states | Low | Low |

Non-goals:

- No new planner.
- No new governance.
- No new execution path.
- No runtime mutation.
- No score formula change until approved next prompt.

## 16. Final Verdict

SCORE_UNSAFE

Reason:

Current channel score is not aligned with the real V7 decision pipeline. It can mark channels as `Отличный` or `Рабочий` while the planner blocks assignment, and it can mark the only currently eligible target as `Требует проверки`.

The future model must split:

1. Technical quality score.
2. Assignment eligibility.
3. Retention eligibility.
4. Evacuation need.
5. Execution/governance readiness.

Final alignment before report commit:

| Check | Status |
| --- | --- |
| Local | PASS |
| GitHub | PASS |
| Runtime | PASS |
| Truth | PASS |
| Convergence | PASS |
