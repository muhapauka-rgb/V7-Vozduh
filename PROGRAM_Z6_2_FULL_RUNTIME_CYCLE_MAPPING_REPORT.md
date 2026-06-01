# PROGRAM Z6.2 - Full Runtime Cycle Mapping Report

Project: V7 Vozduh
Branch target: `v7-next`
Audit mode: READ ONLY
Date: 2026-06-02

## Executive Verdict

V7 already contains a partial Runtime Orchestrator, not a full one.

Closest existing orchestrator candidate:

`tools/v7-users-autoswitch` plus `systemd/v7-users-autoswitch.timer/service`.

It owns autonomous runtime-cycle start, planner execution, selected-move generation, restore-barrier enforcement, movement execution through `v7-user-switch`, path-local verification, local rollback after failed verification, and safety/reconnect/load state writes.

It does not own full lifecycle governance, approval packet authority, unified runtime recheck across all execution paths, contract-scoped rollback, persistent selected-move truth, restore-barrier creation/closure, or final audit completion.

## Evidence Folder

`z6_2-evidence`

- `00_discovery_index.md`
- `01_signal_flow.md`
- `02_planner_selected_restore_flow.md`
- `03_execution_rollback_audit_bypass_flow.md`
- `04_end_to_end_timeline_and_gaps.md`
- `05_final_verdicts.md`

## 1. Ownership Map

| Runtime Area | Current Owner(s) | Classification |
|---|---|---|
| Autonomous runtime scheduling | `systemd/v7-users-autoswitch.timer/service` | REUSE |
| Planner execution | `tools/v7-users-autoswitch` | REUSE / EXTEND |
| Selected move generation | `tools/v7-users-autoswitch.plan()` | REUSE / EXTEND |
| Selected move persistence | No canonical live writer; multiple read/evidence conventions | REFACTOR LATER |
| Restore barrier enforcement | `tools/v7-users-autoswitch` | REUSE |
| Restore barrier generation/clearance/closure | Historical/manual/governance flows; no single active owner found | REFACTOR LATER |
| Runtime signals | Service matrix, Telegram sentinel, quality compact, health/speed/client tools | REUSE |
| Runtime recheck | Autoswitch path-local checks; `admin_core/operator_execution.py` zero-move recheck; Admin preview gates | REUSE / EXTEND |
| Movement execution | `v7-users-autoswitch`, Admin user-switch endpoint, low-level `v7-user-switch` | REUSE / EXTEND |
| Rollback | Autoswitch local rollback, Admin rollback, `v7-rollback-last-change`, proxy guard rollback | REUSE / REFACTOR LATER |
| Audit | Admin audit, `v7-audit-log`, operator execution audit, service event JSONL, stdout/journal | REUSE / REFACTOR LATER |
| Execution contracts | Admin/P2 APIs | REUSE / EXTEND |
| Draft planner timer | `systemd/drafts/v7-autoswitch-planner.*` | DO NOT TOUCH |

## 2. Authority Map

| Authority | Current Reality |
|---|---|
| Scheduler authority | Autoswitch systemd timer is primary autonomous scheduler. Telegram, service matrix, and quality compact timers own supporting signals. |
| Planner authority | `v7-users-autoswitch` owns planner decisions. |
| Policy authority | `policy.json` and `org-egress-policy.json` are hard/tenant policy inputs. |
| Selected-move authority | In-process autoswitch plan JSON, not persistent selected-move files. |
| Restore-barrier authority | Autoswitch enforces barrier semantics; lifecycle write/closure authority is fragmented. |
| Execution authority | Autoswitch and Admin mutating endpoints can execute; execution contract APIs cannot. |
| Runtime recheck authority | Path-local and fragmented; no global runtime admission owner. |
| Rollback authority | Fragmented by path and tool. |
| Audit authority | Fragmented; no single audit-completion owner. |
| Governance authority | Admin and operator execution surfaces provide governance/read models, but autonomous autoswitch bypasses approval packets. |

## 3. State Ownership Map

| State | Writer(s) | Reader(s) | Notes |
|---|---|---|---|
| `v7-state.json` | Runtime/health state tools | Autoswitch, quality compact, Admin | Current routing/state snapshot. |
| `policy.json` | Operator/Admin | Autoswitch, Admin | Hard policy authority. |
| `org-egress-policy.json` | Operator/Admin | Autoswitch, Admin | Tenant policy authority. |
| `service-matrix.json` | Service matrix tooling and Telegram sentinel | Autoswitch, Admin, observability | Live service health signal. |
| `telegram-sentinel.json` | Telegram sentinel | Autoswitch, Admin | Fast Telegram signal. |
| `egress-quality-summary.json` | Quality compact timer/tool | Autoswitch, Admin | Historical quality signal. |
| `autoswitch-safety.json` | Autoswitch | Autoswitch, Admin | Anti-flap/safety state. |
| `client-reconnect-state.json` | Autoswitch/client observers | Autoswitch, Admin | Client experience/reconnect state. |
| `egress-load-summary.json` | Autoswitch dynamic load writer | Autoswitch, Admin | Capacity signal. |
| `autoswitch-restore-barrier.json` | Fragmented historical/manual/governance flows | Autoswitch, Admin | Enforcement owner exists; lifecycle owner fragmented. |
| selected-move files | Evidence/manual/historical copies; no active autoswitch queue writer found | Admin gates, operator execution/observability, restore-settle samples | Not canonical autonomous runtime truth. |

## 4. Execution Lifecycle Map

Autonomous path:

1. `v7-users-autoswitch.timer` fires.
2. `v7-users-autoswitch.service` runs `/usr/local/bin/v7-users-autoswitch --apply`.
3. Autoswitch loads policy, state, health, service, quality, safety, capacity, reconnect, and restore-barrier inputs.
4. Autoswitch computes candidates and selected moves.
5. Restore barrier and generation guards suppress or allow selected moves.
6. `apply(plan)` exits on disabled/observe/dry-run/no selected moves.
7. If allowed, autoswitch calls `v7-user-switch` for each selected move.
8. Autoswitch verifies route result.
9. Autoswitch locally rolls back failed verification cases.
10. Autoswitch writes safety/reconnect/load state and emits JSON result.

Manual/Admin paths:

- Admin autoswitch apply calls `v7-users-autoswitch --mode guarded --apply`.
- Admin user-switch calls `v7-user-switch` directly.
- Admin rollback calls `v7-rollback-last-change --apply`.
- Execution contract APIs remain preview/read-only and explicitly non-executable.
- Operator execution packet engine records only zero-move governance actions.

## 5. Rollback Ownership Map

| Rollback Scope | Owner | Status |
|---|---|---|
| Current autoswitch move verification failure | `v7-users-autoswitch` | Active path-local rollback. |
| Direct Admin user switch proxy failure | Admin API | Active manual endpoint rollback. |
| Latest backup/config rollback | `v7-rollback-last-change --apply` | Active generic rollback when invoked. |
| Proxy runtime guard rollback | Admin API plus proxy runtime guard tool | Active domain-specific rollback. |
| Contract rollback manifest | Admin/P2 preview surfaces | Read-only/non-executable. |
| Historical raw fallback rollback | E25 packets | Prepared evidence, not connected to zero-move executor. |

## 6. Restore Barrier Ownership Map

| Restore Barrier Phase | Owner |
|---|---|
| Root-cause evidence | E11.14/E11.16/E11.17/E12 historical reports. |
| Runtime enforcement | `v7-users-autoswitch`. |
| Runtime read/gate visibility | Admin restore-settle adapter and observability. |
| Evidence classification | `v7-restore-settle-gate`. |
| Generation token/hash/count/budget validation | `v7-users-autoswitch`. |
| Creation/write | Fragmented; no singular active owner found. |
| Clearance/closure | Fragmented; consumed by autoswitch but not centrally owned. |

Root-cause answer:

The restore-barrier exists because restore-settle GO proved only a quiet sample window. After the apply timer resumed, a fresh autoswitch generation recomputed Telegram-down failover moves and executed them. The issue was fresh timer-driven apply after restore, not stale selected-move replay.

## 7. Existing Orchestrator Candidates

| Candidate | Location | Purpose | Inputs | Outputs | Authority Level | Reuse Score | Risk Score |
|---|---|---|---|---|---|---:|---:|
| Autoswitch runtime engine | `tools/v7-users-autoswitch` | Plan/apply/verify/rollback autonomous user movement | Policy, state, service, quality, safety, barrier, load, reconnect | Plan JSON, selected moves, movement calls, safety/reconnect/load state | HIGH for autonomous runtime | 10/10 | 8/10 |
| Autoswitch systemd scheduler | `systemd/v7-users-autoswitch.timer/service` | Start autonomous cycle | Timer | `v7-users-autoswitch --apply` process | HIGH scheduler | 10/10 | 7/10 |
| Admin API mutating endpoints | `admin/v7-admin-api` | Manual autoswitch/user-switch/rollback | Operator request, confirm strings, runtime inputs | Mutations, audits, command results | HIGH manual execution | 8/10 | 9/10 |
| Admin execution contracts | `admin/v7-admin-api` | Preview validation/read model | Proposals, gates, runtime adapters | Drafts, validation, simulation, verification preview | LOW execution; HIGH read model | 8/10 | 4/10 |
| Operator execution engine | `admin_core/operator_execution.py` | Zero-move runtime recheck and audit record | Approval packet, selected-move hash, registries | Chained audit record | LOW movement; MEDIUM governance | 7/10 | 3/10 |
| Telegram sentinel | `tools/v7-telegram-sentinel` | Fast Telegram signal, optional autoswitch trigger | Telegram checks, egress list | Sentinel state, service-matrix updates, events, optional autoswitch | MEDIUM signal; latent HIGH execution | 7/10 | 7/10 |
| Restore-settle gate | `tools/v7-restore-settle-gate` | Read-only restore evidence classifier | Samples/evidence | GO/CONDITIONAL/NO-GO recommendations | LOW execution; MEDIUM governance evidence | 7/10 | 2/10 |
| Generic rollback tool | `tools/runtime-support/v7-rollback-last-change` | Restore latest backup | Backup roots, apply flag | File restore, optional service reload/restart, audit | HIGH rollback when invoked | 6/10 | 8/10 |

## 8. Truth Source Audit

Duplicate authority:

- Autonomous autoswitch and Admin manual endpoints can both execute movement.
- Admin direct user-switch and low-level CLI can bypass planner-selected moves.
- Generic rollback and path-local rollback have different scopes.

Duplicate execution paths:

- `v7-users-autoswitch --apply`.
- Admin `autoswitch_apply_guarded`.
- Admin direct user-switch.
- Manual CLI `v7-user-switch`.
- Latent Telegram sentinel autoswitch apply if not run with `--no-autoswitch`.

Duplicate state writers:

- Service matrix can be updated by service matrix tools and Telegram sentinel.
- Reconnect/client experience state has autoswitch and client observer ownership.
- Audit/event records are written by Admin, runtime-support, operator execution, signal tools, and reports.

Duplicate schedulers:

- Active autoswitch timer.
- Supporting signal timers.
- Draft planner timer path exists and must remain untouched unless explicitly governed later.

Duplicate orchestration logic:

- Autoswitch owns live plan/apply.
- Admin/P2 owns read-only execution workflow preview.
- Operator execution owns zero-move packet runtime recheck.
- Historical approval packets own manual fallback instructions.

Legacy/stale/orphan ownership:

- Persistent selected-move files are not the active autonomous selected-move truth.
- Draft planner systemd units are not active production owners in this evidence set.
- Restore-barrier lifecycle write/closure ownership remains orphaned/fragmented.

## 9. Critical Answers

Q1. What currently starts the runtime cycle?

`systemd/v7-users-autoswitch.timer/service`.

Q2. What currently ends the runtime cycle?

No unified component. Command exit, state writes, Admin audit/runtime audit, stdout/journal, and reports each close part of the cycle.

Q3. Who owns planner execution?

`tools/v7-users-autoswitch`.

Q4. Who owns selected moves?

`tools/v7-users-autoswitch.plan()` owns live ephemeral selected moves. Persistent selected-move files are reader/evidence artifacts, not the live queue.

Q5. Who owns restore barrier generation?

No singular active owner found. Autoswitch owns enforcement only.

Q6. Who owns runtime recheck?

Fragmented: autoswitch path-local checks, zero-move operator execution recheck, and Admin preview gates.

Q7. Who owns execution?

Autoswitch owns autonomous execution; Admin endpoints own manual execution; `v7-user-switch` is the low-level movement executor.

Q8. Who owns rollback?

Fragmented between autoswitch local rollback, Admin endpoint rollback, `v7-rollback-last-change`, and proxy guard rollback.

Q9. Who owns audit completion?

No unified owner.

Q10. Can any component bypass the intended governance path?

Yes. Autonomous autoswitch, Admin direct switch, manual CLI, generic rollback, and latent sentinel autoswitch path can bypass the preview-only execution-contract governance path.

## 10. Final Verdicts

existing_full_orchestrator=false

existing_partial_orchestrator=true

closest_orchestrator_candidate=tools/v7-users-autoswitch_plus_systemd/v7-users-autoswitch.timer_service

duplicate_authority_risk=HIGH

manual_bypass_risk=HIGH

runtime_cycle_fully_understood=true

runtime_cycle_start_owner=systemd/v7-users-autoswitch.timer/service

runtime_cycle_end_owner=NONE_UNIFIED_FRAGMENTED_COMMAND_EXIT_STATE_WRITES_ADMIN_AUDIT_RUNTIME_AUDIT_JOURNAL

selected_move_lifecycle_understood=true

restore_barrier_lifecycle_understood=true

execution_lifecycle_understood=true

rollback_lifecycle_understood=true

audit_lifecycle_understood=true

orchestrator_gap_understood=true

safe_to_continue_to_Z6_3=true

## 11. Z6.3 Boundary

It is safe to continue to Z6.3 only if Z6.3 reuses the existing autoswitch partial orchestrator and does not create:

- a parallel scheduler;
- a duplicate planner;
- a second selected-move truth source;
- a duplicate restore-barrier truth source;
- a duplicate execution path;
- a duplicate rollback truth source;
- a duplicate audit-completion source.

The required next-step boundary is ownership consolidation around existing components, not greenfield orchestration.

