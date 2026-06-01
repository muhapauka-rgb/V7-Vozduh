# PROGRAM Z6.1 - Runtime Execution Ownership Audit Report

Project: V7 Vozduh
Branch target in prompt: `v7-next`
Local audit date: 2026-06-01
Mode: read-only repository audit

## Safety Statement

No implementation, fixes, refactoring, deploy, autoswitch apply, user movement, routing mutation, runtime mutation, service restart, systemd modification, timer modification, cleanup, deletion, merge, or force push was performed.

This report is based on local repository discovery. Live VPS validation was not completed because the read-only SSH probe did not authenticate without a password, and no password was passed through shell/tool input.

Evidence folder: `z6_1-evidence`

## Primary Answer

V7 does not contain a full Runtime Orchestrator.

V7 does contain a partial Runtime Orchestrator ownership model.

The closest existing orchestrator candidate is:

`systemd/v7-users-autoswitch.timer` -> `systemd/v7-users-autoswitch.service` -> `tools/v7-users-autoswitch`

This chain owns the recurring autoswitch runtime cycle, planner generation, selected move calculation, restore-barrier enforcement, bounded apply, verification, immediate rollback-on-verify-fail, and safety/reconnect state writes.

It is not full orchestration because approval authority, execution contracts, restore-barrier generation/closure, global mutation locking, full rollback manifest ownership, and audit completion are split across other components or are read-only/advisory.

## Ownership Map

| Area | Current Owner(s) | Status |
|---|---|---|
| Runtime cycle start | `systemd/v7-users-autoswitch.timer` | Owned for autoswitch only |
| Runtime cycle end | `tools/v7-users-autoswitch` command exit | Partial, no global closure |
| Planner execution | `tools/v7-users-autoswitch` | Strong for autoswitch |
| Selected moves | `tools/v7-users-autoswitch.plan()` generates; Admin/operator read adapters inspect multiple files | Partial/fragmented truth source |
| Restore barrier enforcement | `tools/v7-users-autoswitch` | Strong enforcement |
| Restore barrier generation/closure | No singular active owner found | Gap |
| Runtime recheck | `admin_core/operator_execution.py` for zero-move packets; Admin read adapters for previews | Partial/read-only |
| Runtime execution | Autoswitch timer/tool, Admin autoswitch apply, Admin user switch, rollback tool | Split |
| Rollback | Autoswitch verify rollback, Admin manual rollback, generic latest-change rollback | Split |
| Audit completion | Admin audit, `v7-audit-log`, operator execution audit, event writers | Split |

## Authority Map

| Component | Authority Level | Authority |
|---|---|---|
| `tools/v7-users-autoswitch` | HIGH | Can apply bounded user movement through `v7-user-switch` when `--apply` is used. |
| `systemd/v7-users-autoswitch.timer/service` | HIGH | Schedules and launches movement-capable autoswitch cycles. |
| `admin/v7-admin-api` action endpoints | HIGH | Can launch manual user switch, autoswitch apply, rollback apply, and many other mutations subject to roles/CSRF/confirm tokens. |
| `tools/runtime-support/v7-rollback-last-change` | HIGH | Can restore latest backup across broad runtime/config roots when `--apply` is used. |
| `tools/v7-telegram-sentinel` | MEDIUM, latent HIGH | Production unit is signal-only; binary can launch autoswitch if invoked without `--no-autoswitch`. |
| `admin_core/operator_execution.py` | MEDIUM governance, NONE movement | Validates zero-move packet and writes append-only governance/audit records. |
| Admin execution APIs | LOW/NONE | Read-only contract/event foundation; explicitly cannot execute. |
| Observability/readiness tools | LOW | Read-only advisory and gate checks. |

## State Ownership Map

| State | Writer(s) | Reader(s) | Assessment |
|---|---|---|---|
| `users.registry` | User lifecycle/Admin/runtime tools/`v7-user-switch` | Autoswitch, Admin, recheck/readiness tools | Core runtime truth, split mutation authority. |
| `egress.registry` | Egress lifecycle/Admin/runtime tools | Autoswitch, Admin, readiness tools | Core runtime truth, split mutation authority. |
| `policy.json` / `org-egress-policy.json` | Admin/operator policy actions | Autoswitch/Admin/observability | Hard policy authority. |
| `service-matrix.json` | Service matrix refresh/test and Telegram sentinel | Autoswitch/Admin/observability | Supporting signal with multiple writers. |
| `telegram-sentinel.json` | Telegram sentinel | Autoswitch/Admin/observability | Fast service signal. |
| `egress-quality-summary.json` | Quality compact timer/tool | Autoswitch/Admin/observability | Historical quality support. |
| `autoswitch-safety.json` | Autoswitch | Autoswitch/Admin/observability | Anti-flap authority. |
| `client-reconnect-state.json` | Autoswitch/client observers | Autoswitch/Admin/observability | Supporting client signal. |
| `autoswitch-restore-barrier.json` | No singular active writer identified | Autoswitch/Admin/observability/gates | Enforcement exists, lifecycle owner gap. |
| `selected-moves.json` variants | No singular active writer identified | Admin/operator/observability | Fragmented selected-move truth source. |
| `execution-contracts.json` / `execution-events.jsonl` | P2/Admin foundation | Admin execution APIs | Read-only execution model, not active executor. |
| `audit.jsonl` and governance audit stores | Admin, `v7-audit-log`, operator execution, event writers | Admin/ops/readers | Distributed audit, no unified completion owner. |

## Execution Lifecycle Map

### Active Autoswitch Lifecycle

1. Timer starts `v7-users-autoswitch.service`.
2. Service runs `v7-users-autoswitch --apply`.
3. Tool reads runtime state, policies, service signals, safety state, reconnect state, load summary, and restore barrier.
4. Planner computes generation id, decisions, selected moves, selected move hash, and restore-barrier guard result.
5. Apply path exits if dry-run, disabled, observe mode, or no selected moves.
6. If selected moves remain, tool calls `v7-user-switch` for each move.
7. Tool verifies routes.
8. On verification failure, tool calls `v7-user-switch` back to previous egress when rollback-on-verify-fail is enabled.
9. Tool writes safety/reconnect state.
10. Tool prints JSON. No global execution contract completion is written.

### Admin Action Lifecycles

Admin can start runtime-changing paths through authenticated HTTP actions:

- `autoswitch-apply-guarded` -> `v7-users-autoswitch --mode guarded --apply`.
- `user-switch` -> direct `v7-user-switch`.
- `rollback-apply` -> `v7-rollback-last-change --apply`.

These are governed by role/CSRF/confirm-token checks, but they are not bound to the read-only P2 execution contract model.

### Execution Contract Lifecycle

Admin execution contracts model statuses, events, rollback summaries, and explanations. The code explicitly marks this foundation read-only, non-authoritative, and `execution_allowed_now=false`.

## Rollback Ownership Map

| Rollback Path | Owner | Scope | Gap |
|---|---|---|---|
| Autoswitch verify rollback | `tools/v7-users-autoswitch` | User moved during current autoswitch run | Not tied to execution contract closure. |
| Admin manual switch rollback | `admin/v7-admin-api` | User moved through Admin manual path if proxy runtime switch fails | Endpoint-local rollback only. |
| Generic latest-change rollback | `v7-rollback-last-change` | Broad latest backup under runtime/config roots | Not contract-scoped; can affect broad targets. |
| Execution contract rollback summary | Admin execution APIs | Read-only contract/event data | No apply authority. |

## Restore Barrier Ownership Map

| Step | Owner | Status |
|---|---|---|
| Path and schema consumption | `tools/v7-users-autoswitch` | Exists |
| Enforcement | `tools/v7-users-autoswitch` | Exists and strong |
| Read adapters/previews | Admin/observability/readiness tools | Exists |
| Generation/write | No singular active owner found | Gap |
| Completion/closure | No singular active owner found | Gap |

## Existing Orchestrator Candidates

| Candidate | Location | Purpose | Inputs | Outputs | Authority Level | Reuse Score | Risk Score |
|---|---|---|---|---|---|---:|---:|
| Autoswitch Mini-Orchestrator | `tools/v7-users-autoswitch`, `systemd/v7-users-autoswitch.*` | Runtime autoswitch planner/apply | Runtime registries, policies, service signals, quality, safety, reconnect, load, restore barrier | Plan JSON, selected moves, state writes, `v7-user-switch` calls, verify/rollback results | HIGH | 9 | 8 |
| Admin Action Runner | `admin/v7-admin-api` | Operator/admin mutation entrypoint | HTTP actions, auth, state, policies | Runtime command calls, audit, overview | HIGH | 8 | 9 |
| Admin Execution Contract Foundation | `admin/v7-admin-api` | Read-only future execution model | Contract/event stores | Read-only APIs | LOW/NONE | 7 | 2 |
| Zero-Move Operator Execution | `admin_core/operator_execution.py` | Validate/recheck/audit zero-move approvals | Packet, runtime hashes, selected moves | Audit/governance records | MEDIUM governance, NONE movement | 8 | 3 |
| Operator Observability | `admin_core/operator_observability.py` | Read-only workflow/rehearsal/governance preview | Runtime state/evidence | Preview models | LOW | 8 | 2 |
| Telegram Sentinel | `tools/v7-telegram-sentinel`, systemd unit/timer | Fast Telegram signal | Egress registry, TCP checks, prior state | Sentinel/matrix/event state; latent autoswitch launch | MEDIUM, latent HIGH | 7 | 6 |
| Generic Rollback Owner | `tools/runtime-support/v7-rollback-last-change` | Latest-backup restore | Backup roots | File restore, optional systemctl/audit | HIGH | 5 | 8 |
| Signal Scheduler Set | Service matrix and quality timers/tools | Refresh decision inputs | Timers/probes/state | Health/quality state | MEDIUM | 7 | 4 |

## Critical Questions

Q1. What currently starts the runtime cycle?

`systemd/v7-users-autoswitch.timer` starts the autoswitch movement-capable cycle. Signal cycles are started by Telegram sentinel, service matrix, and quality compact timers.

Q2. What currently ends the runtime cycle?

No unified owner. Autoswitch ends when the command exits after plan/apply and safety/reconnect writes. There is no global lifecycle closure record.

Q3. Who owns planner execution?

`tools/v7-users-autoswitch` owns autoswitch planner execution.

Q4. Who owns selected moves?

`tools/v7-users-autoswitch.plan()` generates selected moves for autoswitch. Persistent selected-move truth is fragmented across expected/read adapter paths, with no singular active writer identified.

Q5. Who owns restore barrier generation?

No singular active generation owner was found. Autoswitch owns enforcement; Admin/observability own read/preview.

Q6. Who owns runtime recheck?

`admin_core/operator_execution.runtime_recheck()` owns zero-move packet recheck. Admin/readiness adapters provide read-only preview checks. No general movement-capable contract-bound recheck executor exists.

Q7. Who owns execution?

Execution is split between autoswitch, Admin action wrappers, direct `v7-user-switch`, and rollback tooling. Execution contracts are read-only.

Q8. Who owns rollback?

Rollback is split between autoswitch verify rollback, Admin manual rollback, generic latest-change rollback, and read-only execution rollback summaries.

Q9. Who owns audit completion?

No single audit completion owner exists. Audit is distributed across Admin audit, `v7-audit-log`, operator execution audit, and event writers.

Q10. Can any component bypass the intended governance path?

Yes. Admin manual user switch, Admin autoswitch apply, the active autoswitch timer, generic rollback, and latent sentinel autoswitch invocation can all bypass the read-only P2 execution contract path.

## Truth Source Audit

Duplicate authority: HIGH

Duplicate execution paths: HIGH

Duplicate state writers: MEDIUM/HIGH

Duplicate schedulers: MEDIUM

Duplicate orchestration logic: MEDIUM

Legacy/stale ownership: MEDIUM

Orphan ownership: MEDIUM/HIGH for restore-barrier generation/closure and selected-move persistence.

## Gate 0 Classifications

REUSE:

- `tools/v7-users-autoswitch`
- `systemd/v7-users-autoswitch.*`
- `admin/v7-admin-api` action and read surfaces
- `admin_core/operator_observability.py`
- `tools/v7-telegram-sentinel`
- Service matrix and quality signal tools/timers
- `tools/runtime-support/v7-audit-log`
- Read-only readiness/gate tools

EXTEND:

- `tools/v7-users-autoswitch` as the existing autoswitch mini-orchestrator
- Admin execution contract/read APIs
- `admin_core/operator_execution.py`
- Admin action runner, with future orchestration gates/locks rather than duplicate action paths

REFACTOR:

- `tools/runtime-support/v7-rollback-last-change`, later only, into a bounded contract-scoped rollback path or wrapper.

REPLACE:

- None identified for Z6.1. Replacement would risk duplicate runtime truth or duplicate execution paths.

DO NOT TOUCH:

- `systemd/drafts/*` planner/health units during this phase.
- Live timers/services/runtime files during this phase.
- Any movement-capable or rollback-capable runtime command during this phase.

## Final Verdicts

existing_full_orchestrator=false

existing_partial_orchestrator=true

closest_orchestrator_candidate=tools/v7-users-autoswitch plus systemd/v7-users-autoswitch.timer/service

duplicate_authority_risk=HIGH

manual_bypass_risk=HIGH

safe_to_continue_to_Z6_2=true

Condition for Z6.2: continue only by reusing and coordinating existing owners. Do not create a parallel executor, duplicate scheduler, duplicate selected-move truth source, duplicate restore-barrier lifecycle owner, or duplicate rollback path.
