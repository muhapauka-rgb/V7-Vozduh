# Execution, Rollback, Audit, and Bypass Flow Evidence

## Execution Paths

| Path | Start Owner | Execution Owner | Inputs | Outputs | Governance Level |
|---|---|---|---|---|---|
| Autonomous autoswitch | `systemd/v7-users-autoswitch.timer/service` | `tools/v7-users-autoswitch` + `v7-user-switch` | State, policy, signals, restore barrier, planner selected moves | Route movement, safety/reconnect/load state, stdout JSON | Partial: planner/safety/barrier governance, no Admin approval packet. |
| Admin autoswitch dry run | Admin API | `v7-users-autoswitch` without apply | Same planner inputs | Plan JSON/audit | Read-only planning. |
| Admin autoswitch apply | Admin API | `v7-users-autoswitch --mode guarded --apply` | Confirm string, planner inputs | Route movement, audit, command result | Manual Admin action; bypasses execution-contract lifecycle. |
| Admin user switch | Admin API | `v7-user-switch` | Session/CSRF, user IP, target egress | Direct movement, Admin audit, possible proxy-runtime rollback on failure | Manual operator path; bypasses planner and restore-barrier selected-move flow. |
| Operator execution packet | `admin_core/operator_execution.py` | Append-only zero-move governance writer | Approval packet, runtime recheck, selected-move hash | Governance audit record only | Explicitly no user movement/routing/autoswitch apply. |
| P2 execution contract APIs | Admin API | None | Proposal/draft contract | Preview, validation gates, simulation/verification preview | Non-authoritative read model; `execution_allowed_now=false`. |
| Telegram sentinel latent autoswitch | `v7-telegram-sentinel` | `v7-users-autoswitch --mode guarded --apply` if not disabled | Telegram signal and service args | Possible autoswitch apply | Production unit uses `--no-autoswitch`; latent bypass in tool. |

## Runtime Recheck Ownership

Runtime recheck is not globally owned.

- `admin_core/operator_execution.py` owns runtime recheck for zero-move governance packets only.
- Admin execution contract validation has read-only gate adapters and preview checks.
- `v7-users-autoswitch` performs its own runtime planning, restore-barrier checks, safety checks, and verification before/after apply.
- No single component rechecks every mutating execution path immediately before movement.

## Rollback Paths

| Path | Owner | Scope | Authority |
|---|---|---|---|
| Autoswitch verification rollback | `v7-users-autoswitch.apply()` | Users moved in current apply run | Local, automatic after verify failure. |
| Admin user-switch proxy failure rollback | Admin API user-switch endpoint | One direct manual switch | Manual endpoint rollback to previous egress on runtime/proxy failure. |
| Generic latest-change rollback | `tools/runtime-support/v7-rollback-last-change --apply` | Latest backup under configured roots | Broad runtime rollback; not proposal/contract scoped. |
| Admin rollback endpoint | Admin API | Calls `v7-rollback-last-change --apply` after confirm | Manual Admin rollback authority. |
| Proxy runtime guard rollback | `v7-proxy-runtime-guard-rollback` via Admin API | Proxy runtime guard domain | Domain-specific runtime rollback. |
| Approval-packet rollback preview | P2/Admin contract surfaces | Manifest/read-only preview | Not executable in current contract engine. |
| Historical raw fallback rollback | E25 movement packets | Explicit raw fallback command | Prepared in evidence, not connected to zero-move packet executor. |

Rollback ownership is fragmented. The broadest active rollback authority is `v7-rollback-last-change --apply`; the closest runtime-local rollback owner is `v7-users-autoswitch` for moves it just made.

## Audit Paths

| Audit / Event | Writer | Scope |
|---|---|---|
| Admin audit | `admin/v7-admin-api` audit helpers | Admin autoswitch, user switch, rollback, execution preview/action surfaces. |
| Generic runtime audit | `tools/runtime-support/v7-audit-log` | Runtime-support tool events and rollback actions. |
| Operator execution audit | `admin_core/operator_execution.py` | Chained append-only zero-move governance action records. |
| Service matrix refresh events | `v7-service-matrix-refresh-all` | Service-matrix refresh event JSONL. |
| Telegram sentinel events | `v7-telegram-sentinel` | Telegram sentinel state and event JSONL. |
| Autoswitch stdout/systemd journal | `v7-users-autoswitch` and systemd | Command result; not a unified audit completion owner by itself. |

There is no single audit-completion owner for the entire runtime cycle.

## Bypass Paths

| Bypass Candidate | Bypasses | Risk |
|---|---|---:|
| `systemd/v7-users-autoswitch.service` running `--apply` every 20s | Admin approval packet, Admin execution contract, operator zero-move recheck | HIGH |
| Admin `autoswitch_apply_guarded` | P2 execution contract and preview-only validation lifecycle | MEDIUM/HIGH |
| Admin direct user-switch endpoint | Planner, selected-move lifecycle, restore barrier lifecycle, execution contract | HIGH |
| Manual CLI `v7-user-switch` | All Admin governance unless externally wrapped | HIGH |
| `v7-telegram-sentinel` without `--no-autoswitch` | Timer-controlled sentinel can invoke autoswitch apply | MEDIUM/HIGH latent; production unit lowers active risk. |
| `v7-rollback-last-change --apply` | Contract-scoped rollback manifest and selected operation context | MEDIUM/HIGH |
| Signal/state file writers | Direct approval, but intentionally feed planner | MEDIUM |
| Draft planner systemd unit | Active scheduler truth if enabled outside known unit set | MEDIUM latent |

## Execution and Bypass Verdict

- Execution lifecycle is understood, but not centrally governed.
- Rollback lifecycle is understood, but fragmented.
- Audit lifecycle is understood, but no single final audit/closure authority exists.
- Manual bypass risk remains HIGH.

