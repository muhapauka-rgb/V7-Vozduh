# Z6.1 Authority And State Ownership Map

## Authority Map

| Authority | Owner | Evidence | Risk |
|---|---|---|---|
| Recurring runtime cycle start | `systemd/v7-users-autoswitch.timer` | `OnUnitActiveSec=20s`, `Unit=v7-users-autoswitch.service` | High because it can initiate movement-capable runs without execution-contract closure semantics. |
| Autoswitch movement execution | `tools/v7-users-autoswitch` | `--apply` path calls `v7-user-switch`; service runs with `--apply` | High, but bounded by planner policy and restore-barrier checks. |
| Manual user movement | Admin `/api/actions/user-switch` | Calls `v7-user-switch` with `V7_SWITCH_REASON=admin_manual` | High manual bypass risk relative to P2 execution contracts. |
| Admin autoswitch execution | Admin `/api/actions/autoswitch-apply-guarded` | Calls `v7-users-autoswitch --mode guarded --apply` after confirm token | High, parallel entrypoint into same mini-orchestrator. |
| Generic rollback execution | Admin `/api/actions/rollback-apply` -> `v7-rollback-last-change --apply` | Owner role and `ROLLBACK` confirm; broad latest backup target selection | High because rollback scope is not contract-scoped. |
| Zero-move governance execution | `admin_core/operator_execution.py` | Allows append-only governance records; forbids user movement and routing mutation | Low runtime risk; useful governance model. |
| Signal authority | Telegram sentinel, service matrix refresh, quality compact | Writes service/quality/sentinel state consumed by autoswitch | Medium because signal quality affects movement decisions. |
| Audit authority | Admin audit functions, `v7-audit-log`, `operator_execution.py` append records, event writers | Multiple JSONL/event stores | Medium because completion is distributed. |

## State Ownership Map

| State / File | Writer(s) | Reader(s) | Ownership Assessment |
|---|---|---|---|
| `/opt/v7/egress/state/users.registry` | User lifecycle/Admin/runtime support tools, `v7-user-switch` | Autoswitch, Admin, operator recheck/readiness tools | Runtime truth source; mutation owner is not singular. |
| `/opt/v7/egress/state/egress.registry` | Egress lifecycle/Admin/runtime support tools | Autoswitch, Admin, readiness tools | Runtime truth source; mutation owner is not singular. |
| `/etc/v7/policy.json` | Admin/operator policy actions | Autoswitch, Admin, observability | Hard policy authority. |
| `/etc/v7/org-egress-policy.json` | Admin/operator org policy actions | Autoswitch, Admin, observability | Tenant policy authority. |
| `/opt/v7/egress/state/service-matrix.json` | `v7-service-matrix-test`, `v7-service-matrix-refresh-all`, `v7-telegram-sentinel` | Autoswitch, Admin, observability | Duplicate writer by design; must be coordinated as signal source. |
| `/opt/v7/egress/state/telegram-sentinel.json` | `v7-telegram-sentinel` | Autoswitch, Admin, observability | Fast Telegram signal source. |
| `/opt/v7/egress/state/egress-quality-summary.json` | `v7-egress-quality-compact` | Autoswitch, Admin, observability | Supporting historical quality source. |
| `/opt/v7/egress/state/autoswitch-safety.json` | `v7-users-autoswitch` | Autoswitch, Admin, observability | Anti-flap and quarantine authority. |
| `/opt/v7/egress/state/client-reconnect-state.json` | `v7-users-autoswitch` and client observers | Autoswitch, Admin, observability | Supporting client-experience signal. |
| `/opt/v7/egress/state/egress-load-summary.json` | `v7-users-autoswitch` dynamic summary / optional future writer | Autoswitch, Admin, observability | Supporting capacity signal, potential stale/optional owner. |
| `/opt/v7/egress/state/autoswitch-restore-barrier.json` | No singular active writer found in local scan; historical governance/report flows imply external/manual creation | Autoswitch, Admin read adapters, observability | Restore-barrier enforcement exists; lifecycle ownership is partial/orphan-prone. |
| `/opt/v7/egress/state/selected-moves.json` and variants | No singular active autoswitch writer identified in current scan; read adapters treat missing as empty or review-required | Admin, operator execution, observability | Selected move truth source is fragmented between live and historical files. |
| `/opt/v7/egress/state/execution-contracts.json` | P2/Admin execution foundation | Admin execution read APIs | Read-only execution truth model, not runtime execution authority. |
| `/opt/v7/egress/state/execution-events.jsonl` | P2/Admin execution foundation | Admin execution read APIs | Read-only event model, not runtime execution authority. |
| `/opt/v7/audit/audit.jsonl` | `v7-audit-log`, Admin action audit | Admin/ops readers | Shared audit sink, not single lifecycle closure owner. |

## Execution Lifecycle Map

### Autoswitch Timer Lifecycle

1. `systemd/v7-users-autoswitch.timer` schedules the cycle.
2. `systemd/v7-users-autoswitch.service` runs `/usr/local/bin/v7-users-autoswitch --apply`.
3. `tools/v7-users-autoswitch` loads policy, state, service signals, quality, safety, reconnect state, load summary, and restore barrier.
4. `plan()` computes decisions, selected moves, selected move hash, generation id, restore-barrier clearance status, and dynamic load summary.
5. `apply()` exits as dry-run/disabled/observe/no-selected-moves, or applies selected moves.
6. Applied moves call `v7-user-switch`.
7. Optional route verification runs.
8. If verification fails and rollback is enabled, the same tool calls `v7-user-switch` back to the previous egress.
9. Safety and reconnect state are written.
10. JSON output is printed; no unified execution contract completion record is produced.

### Admin Manual Movement Lifecycle

1. Operator/admin authenticates and passes CSRF.
2. `/api/actions/user-switch` validates user IP and target egress.
3. Admin audit records request.
4. Endpoint calls `v7-user-switch` with manual reason.
5. Optional proxy runtime route switch runs.
6. If proxy runtime route switch fails, endpoint calls `v7-user-switch` back to previous egress.
7. Endpoint returns overview; no P2 execution contract is required.

### Execution Contract Lifecycle

1. Admin code defines execution statuses and read APIs.
2. Admin explains execution foundation as read-only and non-authoritative.
3. It explicitly cannot move users, change routing, apply autoswitch, create authority, or execute a proposal.
4. Therefore execution contract lifecycle is modeled but not runtime-owned.

## Rollback Ownership Map

| Rollback Type | Owner | Scope | Governance |
|---|---|---|---|
| Autoswitch verify rollback | `tools/v7-users-autoswitch` | Current user moved during current autoswitch run | Automatic after failed route verify if enabled. |
| Admin manual switch rollback | `admin/v7-admin-api` | Current user switched through `/api/actions/user-switch` | Automatic only when proxy runtime switch fails. |
| Generic latest-change rollback | `v7-rollback-last-change`, exposed by Admin owner endpoint | Broad file targets under `/usr/local/bin`, `/etc/wireguard`, `/etc/v7`, `/etc/logrotate.d`, `/etc/systemd/journald.conf.d`, `/opt/v7/egress/state` | Owner role plus `ROLLBACK` confirmation; not tied to execution contract manifest. |
| Contract rollback model | Admin execution APIs | Read-only summaries from execution contracts/events | Advisory only; no apply authority. |

## Restore Barrier Ownership Map

| Lifecycle Step | Current Owner | Assessment |
|---|---|---|
| Barrier file path | `tools/v7-users-autoswitch` default and Admin read adapter | Known path: `/opt/v7/egress/state/autoswitch-restore-barrier.json`. |
| Barrier generation/write | No singular active owner identified in local code scan | Partial/orphan ownership. Must be resolved before implementation. |
| Barrier enforcement | `tools/v7-users-autoswitch` | Strong. It blocks or clears selected moves based on active/expired/cleared/generation/hash/budget fields. |
| Barrier read/preview | Admin read adapters, observability, restore-settle gate | Strong read-only support. |
| Barrier completion/closure | No unified closure owner identified | Lifecycle gap. |
