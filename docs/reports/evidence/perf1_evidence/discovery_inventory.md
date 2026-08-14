# PERF.1 Discovery Inventory

Program: PERF.1 - Runtime and Intelligence Performance Architecture

Mode: read-only static audit plus synthetic pure-model measurement. No runtime commands, deploy, service restart, user movement, autoswitch apply, or state mutation were performed.

## Runtime Platform Owners

| Area | Current owner | Notes |
|---|---|---|
| Planner | `tools/v7-users-autoswitch` / `AutoswitchPlanner.plan()` | Loads runtime truth, computes decisions, selected moves, operation ids, restore-barrier guard, RI advisory context. |
| Execution | `tools/v7-users-autoswitch` / `AutoswitchPlanner.apply()` plus runtime switch tools | Execution happens only when `--apply` is passed. Dry-run is read-only. |
| Governance | Operator/governance packet flow and admin previews | Governance remains outside RI and pure read views. |
| Rollback | `AutoswitchPlanner` rollback-on-verify-fail and runtime rollback tools | Rollback is execution-owned, not intelligence-owned. |
| Audit | `v7-audit-log`, event/audit stores, `AutoswitchPlanner._emit_terminal_audit()` | Terminal audit is emitted only on apply. |
| Closure | `admin/v7-admin-api` and `admin_core/operator_observability.py` | Closure target is generated after terminal state/audit. |
| Restore barrier | `autoswitch-restore-barrier.json` consumed by planner | Barrier gates selected moves and generation clearance. |
| Admin API | `admin/v7-admin-api` | Request owner; still owns auth, actions, command reads, dispatch. |

## Intelligence Owners

| Area | Current owner | Notes |
|---|---|---|
| Routing Intelligence read models | `admin_core/routing_intelligence.py` | Read-only service history, user weights, service intelligence, execution trust, dynamic blast radius, predictive foundation. |
| Routing Brain | `admin_core/routing_brain.py` | Advisory-only integration; cannot move users, approve, write selected moves, or mutate runtime. |
| RI shadow CLI | `tools/v7-routing-intelligence-shadow` | Reads service matrix, quality summary, preferences, audit logs and emits shadow models. |
| Service matrix | `tools/v7-service-matrix-test` | Performs network/service probes and writes `service-matrix.json`; diagnostic only. |
| Quality compaction | `tools/v7-egress-quality-compact` | Bounded EMA/ring compaction; avoids unbounded append-only scans. |
| Admin read views | `admin_core/*views.py` | Pure payload builders after API.2-API.5. |

## Current Runtime Path

`AutoswitchPlanner.__init__` reads current state and compact inputs:

- `v7-state.json`
- policy files
- org policy file
- `egress-quality-summary.json`
- autoswitch safety file
- `egress-speed.json`
- `client-speed.json`
- `service-matrix.json`
- telegram sentinel state
- vless activity state
- restore barrier file
- service preferences
- `users.registry`
- `egress.registry`
- switch history JSONL tail through bounded helper

`AutoswitchPlanner.plan()` computes:

- active user decisions
- candidate moves
- selected moves
- dynamic blast radius metadata
- restore barrier checks
- operation context and selected move hash
- RI advisory context

`AutoswitchPlanner.apply()` executes only when `--apply` is true.

## Current Intelligence Path

`service-matrix.json` + `egress-quality-summary.json` + `service-preferences.json` + bounded audit records

-> `RoutingBrain.candidate_advisory_scores`

-> bounded `score_part`

-> existing planner ranking after planner hard gates

The current contract is advisory-only.
