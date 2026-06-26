# PROGRAM POOL.2
# POST-STABILITY POOL OBSERVATION AND EQUILIBRIUM RECHECK REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence: `POOL2_EVIDENCE/`

Date: 2026-06-19

## 1. Executive Summary

POOL.2 был выполнен в режиме read-only.

Запрещенные действия не выполнялись:

- apply не запускался
- пользователи не перемещались
- маршруты не менялись
- policy не менялась
- autonomy не расширялась
- deploy не выполнялся
- packet generation не выполнялся
- restore barrier generation не выполнялся

Итог:

POOL.1 равновесие не сохранилось полностью.

Физическое распределение пользователей осталось тем же:

- `awg3` = 8
- `wireguard-1779454504-c43409` = 8
- `vless` = 10

Но свежий planner теперь видит:

- `candidate_moves_total = 8`
- `healthy_egress_total = 2`
- все 8 кандидатов идут с `awg3` на `wireguard-1779454504-c43409`

Причина:

`awg3` перестал быть planner-eligible из-за:

- `min_mbps_below_floor`
- `stability_below_floor`

Финальный вердикт:

`POOL_NEEDS_RECOVERY`

## 2. Runtime Truth Gate

Truth gate:

- `final_verdict = PASS`
- `convergence_status = FULLY_ALIGNED`
- local commit = `3fcae4417a94d2cfdf740e92160a0e7cb842fb10`
- GitHub commit = `3fcae4417a94d2cfdf740e92160a0e7cb842fb10`

Convergence status:

- `final_verdict = PASS`
- `runtime_action_status = READY_FOR_RUNTIME_ACTION`
- `runtime_action_safe = true`
- production commit = `3fcae4417a94d2cfdf740e92160a0e7cb842fb10`
- `deploy_delta_mismatches = []`

Evidence:

- `POOL2_EVIDENCE/truth_check.json`
- `POOL2_EVIDENCE/convergence_status.json`

## 3. Current Pool Snapshot

Production API snapshot:

- users total = 26
- egress total = 7
- route OK = 26
- route leak risk = false
- killswitch OK = true

Planner snapshot:

- users total = 26
- egress total = 7
- planner healthy egress total = 2
- candidate moves total = 8
- selected moves = 0
- authority class = `POOL`
- current allowed user budget = 25
- planned limit = 10
- failover limit = 25

Snapshot gate:

- `stop_required = false`
- `source_mismatch_families = []`

Atomic envelope:

- `condition = ENVELOPE_VALID`
- `mismatches = []`

Operation state:

- `terminal_state = DRY_RUN`
- `terminal_reason = dry_run_restore_barrier_clearance_generation_expired`

This terminal reason is expected for this read-only observation stage because POOL.2 explicitly forbids packet generation and restore barrier generation.

Evidence:

- `POOL2_EVIDENCE/api_overview.json`
- `POOL2_EVIDENCE/api_autoswitch_plan.json`
- `POOL2_EVIDENCE/planner_summary.json`

## 4. Current Distribution

Current active user distribution:

| Channel | Users |
|---|---:|
| `awg3` | 8 |
| `wireguard-1779454504-c43409` | 8 |
| `vless` | 10 |

`awg3` users:

- `10.0.0.2`
- `10.7.0.3`
- `10.7.0.4`
- `10.7.0.8`
- `10.7.0.10`
- `10.7.0.12`
- `10.7.0.14`
- `10.7.0.16`

`wireguard-1779454504-c43409` users:

- `10.0.0.3`
- `10.0.0.6`
- `10.7.0.2`
- `10.7.0.6`
- `10.7.0.9`
- `10.7.0.11`
- `10.7.0.13`
- `10.7.0.15`

`vless` users:

- `10.7.0.5`
- `10.7.0.17`
- `10.7.0.18`
- `10.7.0.19`
- `10.7.0.20`
- `10.7.0.21`
- `10.7.0.22`
- `10.7.0.23`
- `10.7.0.24`
- `10.7.0.25`

Evidence:

- `POOL2_EVIDENCE/current_distribution.json`
- `POOL2_EVIDENCE/api_users.json`

## 5. POOL.1 vs POOL.2 Comparison

POOL.1:

- verdict = `POOL_STABLE`
- users total = 26
- healthy egress total = 3
- candidate moves total = 0
- selected moves = 0
- distribution = `awg3:8`, `wireguard:8`, `vless:10`

POOL.2:

- users total = 26
- healthy egress total = 2
- candidate moves total = 8
- selected moves = 0
- distribution = `awg3:8`, `wireguard:8`, `vless:10`

Interpretation:

The assignment distribution remained unchanged, but planner pressure returned. POOL.1 equilibrium was real at that time, but it is no longer fully stable because one previously participating production channel, `awg3`, is now excluded by quality/stability floors.

Evidence:

- `POOL1_POST_AUTONOMY_STABILITY_AND_EQUILIBRIUM_REPORT.md`
- `POOL2_EVIDENCE/pool1_vs_pool2_summary.json`

## 6. Planner Recheck

Fresh planner answer:

Planner would move users now.

It found 8 failover candidates:

| User | Current | Recommended | Type | Reason |
|---|---|---|---|---|
| `10.0.0.2` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible` |
| `10.7.0.3` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible` |
| `10.7.0.4` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible` |
| `10.7.0.8` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible`, `projected_load_target_adjusted` |
| `10.7.0.10` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible` |
| `10.7.0.12` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible`, `projected_load_target_adjusted` |
| `10.7.0.14` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible` |
| `10.7.0.16` | `awg3` | `wireguard-1779454504-c43409` | failover | `current_egress_not_eligible`, `projected_load_target_adjusted` |

Decision summary:

- keep = 18
- switch = 8
- `current_is_best` = 8
- `sticky_keep_current` = 10
- `current_egress_not_eligible` = 8

No movement was executed because this program is read-only.

Evidence:

- `POOL2_EVIDENCE/planner_switch_candidates.json`
- `POOL2_EVIDENCE/planner_decision_reason_summary.json`

## 7. Channel Health Review

| Channel | Eligible | Users | Service | Avg Mbps | Min Mbps | Stability | Telegram | Blockers |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `wireguard-1779454504-c43409` | true | 8 | 100.000 | 58.59 | 53.99 | 0.922 | OK | none |
| `vless` | true | 10 | 99.846 | 47.84 | 44.26 | 0.925 | OK | none |
| `awg3` | false | 8 | 100.000 | 36.47 | 6.03 | 0.165 | OK | `min_mbps_below_floor`, `stability_below_floor` |
| `awg0` | false | 0 | 100.000 | 43.36 | 18.71 | 0.432 | OK | `stability_below_floor` |
| `amneziawg-exec-20260528-10-8-1-14` | false | 0 | 100.000 | 63.70 | 50.07 | 0.786 | OK | `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked` |
| `1` | false | 0 | 2.724 | 0.00 | 0.00 | 0.000 | TELEGRAM_DOWN_14S | health/floor/Telegram blockers |
| `openvpn-1779388847-d2ad7c` | false | 0 | 2.710 | 0.00 | 0.00 | 0.000 | TELEGRAM_DOWN_14S | health/floor/Telegram blockers |

Important distinction:

`awg3` is not failing service suitability. Telegram, Google, Google Auth, Instagram and YouTube are OK. It is failing transport quality floors: minimum speed and stability.

Evidence:

- `POOL2_EVIDENCE/channel_health_compact.json`

## 8. AWG0 Recovery Check

AWG0 improved but did not fully recover.

Current AWG0:

- service score = 100.000
- Telegram = OK
- avg Mbps = 43.36
- min Mbps = 18.71
- stability = 0.432
- eligibility = false
- blocker = `stability_below_floor`

Current floor:

- stability floor = 0.45

Interpretation:

AWG0 is near the floor and looks like a recovering channel, but planner correctly keeps it out of the production candidate pool because it has not crossed the stability threshold.

POOL.2 answer:

AWG0 did not recover enough to become eligible.

## 9. Equilibrium Validation

Current state classification:

`POOL_NEEDS_RECOVERY`

Reason:

The user distribution remained balanced numerically, but the planner no longer agrees with keeping all users where they are. Eight users remain on `awg3`, while `awg3` is currently ineligible. That creates planner pressure for failover from `awg3` to WireGuard.

This is not a snapshot bug:

- snapshot gate PASS
- source mismatch families empty
- atomic envelope valid

This is not a capacity overload:

- `awg3` load = 8/30 soft limit
- `vless` load = 10/30 soft limit
- `wireguard` load = 8/30 soft limit

This is channel recovery/transport stability pressure.

## 10. Counterfactual Analysis

If planner reruns now:

- candidate moves = 8
- all from `awg3`
- recommended target = `wireguard-1779454504-c43409`

If AWG0 becomes healthy:

- healthy pool would likely increase from 2 to 3
- planner would gain another eligible target
- failover pressure from `awg3` may be distributed across more targets

If WireGuard disappears:

- healthy pool would likely drop from 2 to 1
- all eight `awg3` users would be pushed toward `vless` if capacity and suitability allow
- routing resilience would degrade materially

If `awg3` recovers:

- candidate pressure may return to zero
- the POOL.1 equilibrium may be restored without user movement

## 11. Pool Health Score

Assessment:

- distribution = fair numerically
- diversity = acceptable but reduced
- healthy planner pool = degraded from 3 to 2
- service quality = strong on eligible channels
- transport quality = weak on `awg3`, recovering but not sufficient on `awg0`
- candidate pressure = active, 8 users
- autonomy effectiveness = previously successful, but no new execution should be started until channel recovery or failover decision is made

Pool health score:

`PARTIAL / NEEDS_RECOVERY`

## 12. Next Stage Review

Pool observation is complete enough to make a decision.

The project should not proceed as if POOL is still fully stable.

Safe next stage:

`CHANNEL_RECOVERY_AWG3_AWG0_STABILITY_REVIEW`

Purpose:

- observe whether `awg3` naturally recovers
- observe whether `awg0` crosses the 0.45 stability floor
- decide whether the 8 `awg3` failover candidates require a governed failover packet

No automatic movement is recommended from POOL.2 alone because this program was explicitly read-only.

## 13. Final Verdict

Final verdict:

`POOL_NEEDS_RECOVERY`

Final flags:

- truth_healthy = true
- convergence_healthy = true
- runtime_action_safe = true
- distribution_unchanged = true
- planner_agrees_with_current_distribution = false
- candidate_moves_total = 8
- selected_moves = 0
- users_moved = 0
- apply_executed = false
- routing_changed = false
- policy_changed = false
- autonomy_changed = false
- deploy_executed = false
- awg0_recovered = false
- awg3_recovered = false
- pool_observation_complete = true
- SAFE_NEXT_STEP = `CHANNEL_RECOVERY_AWG3_AWG0_STABILITY_REVIEW`
