# PROGRAM FULL EGRESS POOL REALITY AUDIT AND LARGE BATCH CAPACITY FOUNDATION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence: `full_egress_pool_large_capacity_evidence/`

## Executive Verdict

The full production egress pool is not ready for LARGE_BATCH execution.

The limiting factor is not raw slot capacity. The limiting factor is eligible
pool health:

- production registry contains 7 egress channels
- only 2 are currently eligible for planner movement: `vless`, `awg0`
- 5 are excluded by health, stability, reservation, or governance policy
- no egress is overloaded
- no egress is quarantined
- `awg3` is service-healthy but rejected by quality stability

No users were moved. No apply was executed. No authority was promoted.

## Production Truth

Evidence:

- `production_truth.json`
- `production_truth_summary.json`
- `convergence_status.json`
- `convergence_status_summary.json`

Result:

- `truth_check_final_verdict=PASS`
- `convergence_status=FULLY_ALIGNED`
- `convergence_final_verdict=PASS`
- `runtime_action_status=READY_FOR_RUNTIME_ACTION`
- `runtime_action_safe=true`
- `local_commit=8dda6fa35a7657f28c7a4164bdfd2a3ab6729989`
- `github_commit=8dda6fa35a7657f28c7a4164bdfd2a3ab6729989`
- `production_commit=8dda6fa35a7657f28c7a4164bdfd2a3ab6729989`
- `runtime_root=/opt/v7`
- `runtime_truth_status=KNOWN`

Workspace note:

The workspace has documentation/evidence-only untracked files. Truth check
classified them as non-blocking:

- `runtime_critical=0`
- `runtime_relevant=0`
- `unknown=0`
- `blocking_dirty=false`

## Phase 1 - Full Egress Inventory

Evidence:

- `production_state/egress.registry`
- `production_state/users.registry`
- `egress_inventory.json`

Current registry egress:

| Egress | Type | Interface | Enabled | Reserved | Users | Role |
| --- | --- | --- | --- | --- | ---: | --- |
| `vless` | proxy | `tun0` | true | false | 13 | |
| `awg0` | interface | `awg0` | true | false | 1 | `GLOBAL_STABLE` |
| `awg3` | interface | `awg3` | true | false | 0 | `GLOBAL_STABLE` |
| `1` | interface | `v7e356a192b79` | true | false | 0 | `GLOBAL_FAST` |
| `openvpn-1779388847-d2ad7c` | interface | `v7edb0c189291` | true | false | 0 | `GLOBAL_FAST` |
| `wireguard-1779454504-c43409` | interface | `v7e06a394c478` | true | true | 0 | `GLOBAL_FAST` |
| `amneziawg-exec-20260528-10-8-1-14` | interface | `v7execwg0` | true | true | 4 | `EXECUTION_ONLY` |

Additional quality-history-only entries not in current registry:

- `amneziawg-1779227510-8c08e7`
- `awg2`

These are not counted as active production registry egress.

## Phase 2 - Health Audit

Evidence:

- `egress_health_audit.json`
- `planner_candidate_summary.json`
- `production_state/service-matrix.json`
- `production_state/egress-quality-summary.json`

Current health classification:

| Egress | Health | Avg Mbps | Min Mbps | Stability | Service Score | Telegram | Planner Blocks |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `vless` | healthy | 54.22 | 51.56 | 0.951 | 100.0 | OK | none |
| `awg0` | healthy | 47.08 | 27.82 | 0.591 | 100.0 | OK | none |
| `awg3` | degraded_stability | 48.59 | 10.21 | 0.210 | 100.0 | OK | `stability_below_floor` |
| `1` | unhealthy | 0.0 | 0.0 | 0.0 | 2.854 | `TELEGRAM_DOWN_14S` | health/speed/telegram |
| `openvpn-1779388847-d2ad7c` | unhealthy | 0.0 | 0.0 | 0.0 | 2.856 | `TELEGRAM_DOWN_14S` | health/speed/telegram |
| `wireguard-1779454504-c43409` | healthy_reserved | 55.67 | 48.66 | 0.874 | 100.0 | OK | canary reserved |
| `amneziawg-exec-20260528-10-8-1-14` | healthy_reserved | 37.52 | 9.52 | 0.254 | 100.0 | OK | manual/reserve/canary |

Conclusion:

The pool is mixed. There are enough healthy-looking channels by service truth,
but only two are eligible for production planner movement.

## Phase 3 - Eligibility Audit

Evidence:

- `egress_eligibility_audit.json`
- `planner_dry_run.json`
- `planner_candidate_summary.json`

Eligibility:

| Egress | Eligible | Exact Exclusion Reason |
| --- | --- | --- |
| `vless` | true | none |
| `awg0` | true | none |
| `awg3` | false | `stability_below_floor` |
| `1` | false | `health_code_000`, `severity_FAIL`, `avg_mbps_below_floor`, `min_mbps_below_floor`, `telegram_required_telegram_down_14s` |
| `openvpn-1779388847-d2ad7c` | false | `health_code_000`, `severity_FAIL`, `avg_mbps_below_floor`, `min_mbps_below_floor`, `telegram_required_telegram_down_14s` |
| `wireguard-1779454504-c43409` | false | `canary_reserved_production_assignment_blocked` |
| `amneziawg-exec-20260528-10-8-1-14` | false | `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked` |

Conclusion:

Eligibility rules are working as designed. They are excluding:

- unhealthy legacy channels
- a stability-degraded channel
- intentionally reserved channels

No duplicate planner or bypass path was introduced.

## Phase 4 - Service Audit

Evidence:

- `egress_service_audit.json`
- `production_state/service-matrix.json`
- `production_state/intelligence/channel-service-scores.json`

Tracked service families include:

- YouTube
- Telegram
- Instagram
- Google
- Google Auth
- ChatGPT/OpenAI Auth
- Claude/Anthropic
- Facebook
- WhatsApp
- Spotify
- SoundCloud
- Apple

Important findings:

- `vless`, `awg0`, `awg3`, `wireguard-1779454504-c43409`, and `amneziawg-exec-20260528-10-8-1-14` have healthy Telegram.
- `1` and `openvpn-1779388847-d2ad7c` have Telegram hard-block signals.
- `awg3` service quality is not the blocker: `service_aggregate_score=100.0`, Telegram OK, and required services are not missing.
- Anthropic 404 appears as a profile-irrelevant/application endpoint failure, not the reason `awg3` is blocked.

## Phase 5 - Pool Utilization Audit

Evidence:

- `pool_utilization_audit.json`
- `production_state/egress-load-summary.json`

Current utilization:

| Egress | Active Users | Soft Limit | Hard Limit | Load Status | Eligible |
| --- | ---: | ---: | ---: | --- | --- |
| `vless` | 13 | 21 | 27 | OK | true |
| `awg0` | 1 | 21 | 27 | OK | true |
| `awg3` | 0 | 21 | 27 | OK | false |
| `1` | 0 | 21 | 27 | OK | false |
| `openvpn-1779388847-d2ad7c` | 0 | 21 | 27 | OK | false |
| `wireguard-1779454504-c43409` | 0 | 21 | 27 | OK | false |
| `amneziawg-exec-20260528-10-8-1-14` | 4 | 21 | 27 | OK | false |

Pool utilization verdict:

- `overloaded_egress=0`
- `underused_egress=1`
- `unused_healthy_egress=0`
- eligible soft spare users: 28
- eligible hard spare users: 40

Conclusion:

The pool has slot capacity, but the usable healthy eligible pool is too narrow
for LARGE_BATCH.

## Phase 6 - AWG3 Root Cause

Evidence:

- `awg3_root_cause_raw.json`
- `awg3_root_cause_report.json`

AWG3 root cause:

- class: `QUALITY_STABILITY_BELOW_FLOOR`
- planner reason: `stability_below_floor`
- current stability: `0.210`
- 1h stability: `0.3104`
- required stability: `0.45`
- avg Mbps: `48.59`
- min Mbps: `10.21`
- service aggregate score: `100.0`
- Telegram: OK
- capacity cause: false
- service cause: false
- policy cause: false
- measurement/quality-history cause: true

Conclusion:

`awg3` is not failing because Telegram, YouTube, Instagram, Google, Google Auth,
or capacity are bad. It is failing because both current and 1h quality stability
are below the planner floor.

## Phase 7 - In-Scope Remediation

No remediation was applied.

Reason:

No safe local fix was proven. Lowering the stability floor or forcing `awg3`
eligible would be a policy bypass, not a fix. The correct safe action is
observation/retest after new quality samples, or a separate program that proves
the stability metric is wrong.

Safe retest action performed:

- planner dry-run with pre-planner refresh write
- no apply
- no user movement
- no authority promotion

## Phase 8 - Post-Fix Recheck

Evidence:

- `post_fix_pool_state.json`
- `planner_dry_run.json`
- `planner_candidate_summary.json`

Since no mutation/fix was applied, post-fix state equals post-audit state:

- `eligible_egress=2`
- `healthy_egress=4`
- `overloaded_egress=0`
- `quarantined_egress=0`
- `pool_ready_for_large_batch=false`

Planner dry-run remained safe:

- `apply_requested=false`
- `selected_moves=0`
- `terminal_state=DRY_RUN`
- `terminal_reason=dry_run_restore_barrier_clearance_generation_expired`
- `snapshot_stop_required=false`
- `source_mismatch_families=[]`
- `pre_planner_refresh_state=REFRESH_SUCCESS`

## Phase 9 - LARGE_BATCH Capacity Review

Evidence:

- `large_batch_capacity_review.json`

Capacity analysis:

- eligible channels: `vless`, `awg0`
- eligible channel count: 2
- eligible soft spare users: 28
- eligible hard spare users: 40
- candidate moves total: 17
- LARGE_BATCH budget target: 10
- slot capacity sufficient: true
- pool health sufficient: false

Interpretation:

The system can physically absorb more users on paper, but LARGE_BATCH should not
be certified with only two eligible production channels and one of the intended
pool members (`awg3`) below stability floor.

## Phase 10 - Decision To Action

Evidence:

- `pool_decision_report.json`
- `full_pool_audit_summary.json`

Decision:

`POOL_NOT_READY_FOR_LARGE_BATCH`

Single blocker:

`POOL_HEALTH_ELIGIBILITY_LIMITED: only 2 eligible production channels; awg3 excluded by stability_below_floor; two legacy channels have health/telegram hard blocks; two channels are intentionally reserved/manual/canary.`

Safe next step:

`observe_and_retest_awg3_stability_then_prepare_large_batch_authority_packet_if_eligible_pool_reaches_3`

## Final Verdicts

```text
total_egress=7
healthy_egress=4
eligible_egress=2
disabled_egress=0
quarantined_egress=0
unused_healthy_egress=0
overloaded_egress=0
underused_egress=1
awg3_root_cause_identified=true
awg3_fixed=false
pool_capacity_sufficient=false
large_batch_pool_ready=false
single_blocker=POOL_HEALTH_ELIGIBILITY_LIMITED
users_moved=0
apply_executed=false
authority_promoted=false
SAFE_NEXT_STEP=observe_and_retest_awg3_stability_then_prepare_large_batch_authority_packet_if_eligible_pool_reaches_3
```
