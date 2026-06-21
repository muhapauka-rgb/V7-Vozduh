# POOL.3 Runtime Discover

Status: runtime/discover audit
Timestamp: 2026-06-21T15:41:45+0700
Runtime snapshot: 2026-06-21T08:15:44.315146+00:00
Branch: `Updatesystem`
Audit base commit: `6c5f8eeabdf36c5360825d8cbb7388b7fdde8659`
Report commit: `f875eeee50091382c1332aaa85449010875357b1`
Runtime deployed code commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Scope

POOL.3 was read-only.

No apply was executed. No users were moved. No routes, planner, governance, execution path, timers, policy, database, snapshots, or truth sources were changed.

## Commands Run

Discovery:

- `pwd`
- `git status --short`
- `git branch --show-current`
- `find tools -maxdepth 2 -type f | sort`
- `find docs -maxdepth 3 -type f | sort`
- `rg -n "POOL|pool|autoswitch|autonomy|candidate_moves|restore|rollback|timer|cron|systemd|event|watch|daemon|planner|authority|blast|batch" tools docs . --glob '!node_modules' --glob '!venv' --glob '!dist'`
- `rg -n "candidate_moves_total|selected_moves|failover|restore|rollback|stability_floor|production pool|wireguard|POOL\\.2|POOL2|POOL_NEEDS_RECOVERY" tools docs POOL2_EVIDENCE POOL2_STABILITY_WINDOW_RECHECK_REPORT.md --glob '!node_modules' --glob '!venv' --glob '!dist'`

Canonical gates:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

Production API read-only evidence:

- `POST /login`
- `GET /api/session`
- `GET /api/overview?force=1`
- `GET /api/users`
- `GET /api/egress`
- `POST /api/actions/autoswitch-dry-run` with `{}`
- `POST /api/actions/autoswitch-dry-run` with `{"egress":"wireguard-1779454504-c43409"}`
- `POST /api/actions/users-rebalance-dry-run` with `{}`
- `POST /api/actions/planner-refresh-dry-run` with `{}`
- `GET /api/operator/autonomous-dry-run`

Evidence paths:

- `docs/reports/POOL3_EVIDENCE/truth_check.json`
- `docs/reports/POOL3_EVIDENCE/convergence_status.json`
- `docs/reports/POOL3_EVIDENCE/api_overview.json`
- `docs/reports/POOL3_EVIDENCE/api_users.json`
- `docs/reports/POOL3_EVIDENCE/api_egress.json`
- `docs/reports/POOL3_EVIDENCE/api_autoswitch_dry_run.json`
- `docs/reports/POOL3_EVIDENCE/api_autoswitch_dry_run_wireguard.json`
- `docs/reports/POOL3_EVIDENCE/api_users_rebalance_dry_run.json`
- `docs/reports/POOL3_EVIDENCE/api_planner_refresh_dry_run.json`
- `docs/reports/POOL3_EVIDENCE/api_operator_autonomous_dry_run.json`
- `docs/reports/POOL3_EVIDENCE/pool3_summary.json`

## Runtime Truth

Truth:

- `final_verdict = PASS`
- `convergence_status = FULLY_ALIGNED`
- `runtime_access_status = READY`
- `runtime_truth_status = KNOWN`
- `state_truth_status = KNOWN`
- `runtime_action_safe = true` via convergence status

Runtime derived facts:

- `admin_service_active = true`
- `operation_wiring_present = true`
- `execution_store_available = true`
- `restore_barrier_known = true`
- `snapshot_refresh_cli_available = true`
- `snapshot_refresh_mechanism_known = true`
- `autoswitch_scheduler_active = false`
- `autoswitch_service_active = false`
- `scheduler_inactive_approved_manual_mode = true`
- `service_inactive_explained = true`

Convergence:

- `final_verdict = PASS`
- `status = ALIGNED`
- Runtime deployed code is still `67fbd8506321802222c6f8ed3d34cfe406a45d8a`.
- Local/GitHub are at report commit `f875eeee50091382c1332aaa85449010875357b1` after documentation commit.
- The mismatch is classified as docs-only; deployment is not required for this audit.

## Current Pool Verdict

POOL.2 exact state does not hold as a current runtime verdict.

The POOL.2 claim was:

- `POOL_NEEDS_RECOVERY`
- active distribution `awg3=8`, `wireguard=8`, `vless=10`
- `candidate_moves_total=8`
- 8 failover candidates from `awg3` to `wireguard-1779454504-c43409`
- `awg3` failed `min_mbps_below_floor` and `stability_below_floor`

POOL.3 current evidence:

- active distribution remains `awg3=8`, `wireguard-1779454504-c43409=8`, `vless=10`
- registry has 27 users, but `10.7.0.7` is disabled on `vless`
- autoswitch dry-run action returned `rc=0`, `apply_requested=false`, `terminal_state=DRY_RUN`, `selected_move_count=0`
- the admin API stdout tail shows `selected_moves=[]` and `apply_result.applied=false`
- the previous exact `8 awg3 -> wireguard` failover pressure is not visible in the fresh API evidence
- exact full `candidate_moves_total` from raw CLI JSON could not be recovered through the admin action because `plan=null` and the API only returns the last 12000 bytes of stdout
- direct SSH CLI capture was attempted read-only, but interactive SSH did not complete reliably in this environment; no runtime mutation occurred

Practical verdict:

`POOL_RECOVERY_NOT_APPLIED_AND_NO_8_USER_FAILOVER_PROVEN_NOW`

This is not a green light for autonomous apply. It means the POOL.2 emergency failover evidence is stale or no longer reproduced through the current available read-only surfaces.

## User Distribution

Active users:

| Channel | Active Users |
| --- | ---: |
| `awg3` | 8 |
| `wireguard-1779454504-c43409` | 8 |
| `vless` | 10 |

Registry users:

| Channel | Registry Users |
| --- | ---: |
| `awg3` | 8 |
| `wireguard-1779454504-c43409` | 8 |
| `vless` | 11 |

Disabled user:

| User | Channel | Table |
| --- | --- | --- |
| `10.7.0.7` | `vless` | `1005` |

## Channel Runtime Snapshot

| Channel | Users | Avg Mbps | Min Mbps | Stability | Load | Runtime |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `awg0` | 0 | 28.3783 | 6.38 | 0.22482 | OK | READY |
| `awg3` | 8 | 14.41 | 6.50 | 0.451076 | HARD_FULL | READY |
| `wireguard-1779454504-c43409` | 8 | 61.851 | 60.77 | 0.982523 | HARD_FULL | READY |
| `vless` | 10 active / 11 registry | 48.837 | 44.94 | 0.920204 | HARD_FULL | READY |

Quality floor:

- `min_avg_mbps = 15.0`
- `min_floor_mbps = 10.0`
- `min_stability = 0.45`

## POOL.2 Questions

| Question | POOL.3 Answer | Evidence |
| --- | --- | --- |
| A. Does POOL.2 still hold? | Partially no. Distribution still matches active counts, but the exact 8-user awg3 failover pressure is not reproduced by fresh available evidence. | `api_users.json`, `api_autoswitch_dry_run.json` |
| B. Are there still 8 failover candidates on awg3? | Not proven now. Active awg3 users are still 8, but fresh autoswitch tail shows `selected_move_count=0`; exact `candidate_moves_total` is unavailable because API `plan=null`. | `api_autoswitch_dry_run.json` |
| C. Did awg0 recover above stability floor 0.45? | No. `awg0 stability=0.22482`, below 0.45. | `api_overview.json` |
| D. Did awg3 recover above stability floor 0.45? | Barely yes by stability only: `0.451076`; but min speed remains below floor and load is hard-full. | `api_overview.json` |
| E. Is real failover of 8 users still needed? | Not from current evidence. No apply should run without a fresh full CLI plan and governed packet. | API dry-run evidence |
| F. Is WireGuard still the correct target? | WireGuard remains technically strong and production-ready, but current evidence does not produce an 8-user failover recommendation to it. It is also `HARD_FULL` under current load posture. | `api_overview.json`, `api_egress.json` |
| G. What checks are periodic? | Health/state loop, quality compaction, service matrix refresh, Telegram sentinel, and historical autoswitch timer definitions exist. Current truth says autoswitch scheduler is inactive. | `systemd/*`, `truth_check.json` |
| H. What exactly is their periodicity? | `v7-health` loop sleeps 30s; `v7-egress-quality-compact.timer` every 5m; `v7-service-matrix-refresh.timer` every 15m plus random 60s; `v7-telegram-sentinel.timer` every 4s; `v7-users-autoswitch.timer` definition every 20s but currently inactive. | `systemd/`, `truth_check.json` |
| I. Are they probes/planners/previews/apply? | Health/quality/service/sentinel are probes/read-model refreshes. `v7-telegram-sentinel.service` is explicitly `--no-autoswitch`. `v7-autoswitch-planner` draft is planner-only. `v7-users-autoswitch.service` would apply, but current truth says inactive. | `systemd/*`, `truth_check.json` |
| J. Why is full automation not continuously enabled? | The apply timer/service is inactive and approved as manual mode; autonomous dry-run hard-stops on confidence/trust/prediction floors and restore barrier readiness. | `truth_check.json`, `api_operator_autonomous_dry_run.json` |
| K. What is missing for event-driven autonomy? | A production event gate that converts channel/service regression into a bounded governed packet with fresh restore barrier, confidence/trust/prediction floors passing, and audit/feedback closure. | `api_operator_autonomous_dry_run.json` |
| L. What is safest next phase? | Implement no movement now. First build/certify event-driven trigger path as read-only then one bounded governed apply packet when fresh full CLI plan says READY. | This report |

## Restore Barrier And Rollback

Restore barrier:

- Known by truth/convergence.
- Autonomous dry-run says `restore_barrier_required=true`.
- `restore_barrier_written_now=false`.
- `restore_barrier_readiness=BLOCKED`.

Rollback:

- Rollback model exists and is owned by `admin_core/operator_execution.py`.
- Simulated rollback is `STOP_BEFORE_APPLY`.
- Rollback was not executed.
- The dry-run rollback item blocks include `rollback packet missing`, `rollback target unknown`, `audit path unavailable`, and `restore barrier mismatch`.

## Autonomy Runtime Reality

Existing owner reuse is correct:

- planner: `tools/v7-users-autoswitch`
- packet tool: `tools/v7-operator-execution-packet`
- restore barrier owner: `admin_core/operator_execution.py`
- rollback owner: `admin_core/operator_execution.py`
- feedback model: `admin_core/operator_execution_feedback.py`

No duplicate planner, governance, execution path, or truth source was found in the autonomous dry-run model.

Current autonomous dry-run candidate:

| User | From | To | Why | Allowed? |
| --- | --- | --- | --- | --- |
| `10.7.0.5` | `vless` | `awg3` | best available channel has higher advisory suitability | No |

Hard stop blockers:

- `confidence_too_low`
- `trust_too_low`
- `prediction_confidence_too_low`

Scores:

- confidence = 45.8, floor = 70
- trust = 39.57, floor = 70
- prediction confidence = 39.6, floor = 70
- rollback confidence = 100, observed

## Periodic Runtime Model

| Unit / Loop | Periodicity | Current Meaning | Can Apply? |
| --- | --- | --- | --- |
| `v7-health.service` draft loop | every 30s | health/state summary loop | No direct autoswitch apply |
| `v7-egress-quality-compact.timer` | boot + 3m, then every 5m | quality summary compaction | No user movement |
| `v7-service-matrix-refresh.timer` | boot + 2m, then every 15m plus random 60s | service matrix refresh | No user movement |
| `v7-telegram-sentinel.timer` | boot + 30s, then every 4s | fast Telegram sentinel | No, service uses `--no-autoswitch` |
| `systemd/drafts/v7-autoswitch-planner.timer` | boot + 2m, then every 30s | planner refresh draft | Planner only |
| `v7-users-autoswitch.timer` | boot + 2m, then every 20s | guarded autoswitch apply service definition | Definition can apply, but current truth says inactive |

Fixed timer-only movement is rejected as the product model. Periodic probes may refresh evidence. Periodic planners may preview. They must not blindly move users every N minutes.

## Risk Assessment

| Risk | Status |
| --- | --- |
| Accidentally moving users | Avoided; no apply endpoint or CLI apply was run. |
| Stale POOL.2 conclusion | Present; POOL.2 evidence is no longer enough for current action. |
| Full CLI candidate total unavailable | Present; admin API truncates stdout tail and direct SSH CLI did not complete in this environment. |
| Autoswitch daemon silently active | Not observed; truth says service/timer inactive and approved manual mode. |
| Event-driven autonomy missing | Present; autonomous dry-run is simulation-only and hard-stopped. |

## Apply Decision

No apply.

Reasons:

- This task is discover-only.
- Fresh evidence does not prove the 8-user awg3 failover is still required.
- Restore barrier readiness is blocked for autonomy.
- Confidence/trust/prediction floors do not pass.
- The current product target is event-driven autonomy, not timer-based user movement.

## Next Step

Safest next phase:

1. Keep production movement manual/governed.
2. Add or certify an event-driven autonomy trigger in read-only mode first:
   channel/service regression -> planner -> packet preview -> restore barrier readiness -> bounded apply eligibility -> feedback preview.
3. Require fresh full CLI plan evidence before any apply packet.
4. Only then run one bounded governed apply if the plan says READY and restore barrier/rollback/audit are valid.

## Verdict

`POOL3_DISCOVER_COMPLETE_NO_APPLY`
