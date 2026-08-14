# Planner, Selected Move, and Restore Barrier Flow Evidence

## Planner Flow

`tools/v7-users-autoswitch` is the closest existing lifecycle owner for autonomous planning.

Observed planner inputs:

- `/opt/v7/egress/state/v7-state.json`
- `/etc/v7/policy.json`
- `/etc/v7/org-egress-policy.json`
- `/opt/v7/egress/state/egress-quality-summary.json`
- `/opt/v7/egress/state/autoswitch-safety.json`
- `/opt/v7/egress/state/egress-speed.json`
- `/opt/v7/egress/state/client-speed.json`
- `/opt/v7/egress/state/service-matrix.json`
- `/opt/v7/egress/state/telegram-sentinel.json`
- `/opt/v7/egress/state/client-reconnect-state.json`
- `/opt/v7/egress/state/vless-activity.json`
- `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- user registry, egress registry, route classes, service preferences, dynamic load.

Observed planner outputs:

- stdout JSON plan.
- `summary.selected_moves`.
- top-level `selected_moves`.
- dynamic load summary writes.
- reconnect state writes during observation/apply when state changes.
- safety state writes after apply.

The autonomous service invokes `v7-users-autoswitch --apply`, and the tool always builds a plan before attempting `apply(plan)`.

## Selected Move Lifecycle

| Phase | Owner | Evidence / Behavior |
|---|---|---|
| Create | `v7-users-autoswitch.plan()` | Candidate and selected moves are calculated in memory. |
| Serialize | `v7-users-autoswitch` stdout JSON | The selected moves appear in the plan JSON emitted by the command. |
| Persist | No active autoswitch queue writer found | Existing persistent selected-move files are read adapters, evidence snapshots, or historical copies, not the live autoswitch source of truth. |
| Read | Admin selected-move gate, operator observability, operator execution, restore-settle evidence parser | Multiple readers inspect possible selected-move files or plan samples. |
| Consume | `v7-users-autoswitch.apply(plan)` | Consumes selected moves from the same in-process plan when `--apply` is used. |
| Execute | `v7-users-autoswitch._run_switch()` | Calls `v7-user-switch <ip> <egress>` with autoswitch reason environment. |
| Verify | `v7-users-autoswitch._verify_routes()` | Verifies route result after movement. |
| Roll back | `v7-users-autoswitch.apply()` local rollback branch | On verification failure, attempts to switch users back to prior egress. |
| Expire | Process end, next planner generation, stale file detection in readers, restore-barrier generation/hash mismatch | No canonical persistent selected-move TTL owner exists. |

## Selected Move Readers

Known selected-move file conventions:

- `/opt/v7/egress/state/selected-moves.json`
- `/opt/v7/egress/state/autoswitch-selected-moves.json`
- `/opt/v7/egress/state/selected_moves.json`
- `/opt/v7/egress/state/current-selected-moves.json`
- historical evidence copies under `docs/track7/control-plane/...`

Observed read semantics differ:

- Admin selected-move gate: missing source becomes `REVIEW_REQUIRED`; nonzero moves become `FAIL`; zero moves become `PASS`.
- `admin_core/operator_execution.py`: missing selected-move files are treated as empty for zero-move packet recheck.
- Restore-settle parser: parses selected moves from evidence samples and text, not a live execution queue.

## Restore Barrier Lifecycle

Root cause from E11.14:

- Restore-settle GO only proved the sampled window was quiet.
- After the apply timer was restored, a fresh autoswitch timer generation recomputed a Telegram-down plan and selected three non-cohort failovers.
- Users moved because the fresh apply-timer plan was valid under the old logic.
- The cause was not stale selected-move replay; it was fresh timer-driven apply logic without a post-restore barrier.

Observed restore-barrier enforcement:

- `v7-users-autoswitch` reads `autoswitch-restore-barrier.json`.
- It computes active, expired, cleared, post-TTL blocking, failover quarantine, clearance generation, and clearance budget semantics.
- Active barrier suppresses failover selection.
- Expired but uncleared barrier fails closed.
- Post-TTL apply requires explicit clearance metadata.
- Nonzero post-TTL clearance requires generation token, selected-move hash, expected selected-move count, and budget.
- Mismatched, stale, missing, or over-budget clearance yields selected moves = 0.

Observed restore-barrier ownership:

| Lifecycle Segment | Owner Found | Status |
|---|---|---|
| Root-cause detection | Historical reports E11.14/E11.16/E11.17/E12 | Understood. |
| Enforcement | `v7-users-autoswitch` | Centralized enough for runtime suppression. |
| Admin read/gate view | `admin/v7-admin-api` restore-settle adapter | Read-only gate owner. |
| Evidence classification | `tools/v7-restore-settle-gate` | Read-only evaluator. |
| Creation/write | Historical/manual/governance flows; no singular active writer found | Fragmented. |
| Clearance/closure | Barrier metadata fields consumed by autoswitch; no singular active closer found | Fragmented. |
| Audit completion | Historical reports and Admin audit paths; no single lifecycle closer | Fragmented. |

## Planner and Restore Barrier Verdict

- Planner execution owner: `tools/v7-users-autoswitch`.
- Selected move source of truth in autonomous runtime: in-process plan JSON, not persistent selected-move files.
- Restore barrier enforcement owner: `tools/v7-users-autoswitch`.
- Restore barrier lifecycle owner: fragmented/manual/governance-history, not centrally owned.

