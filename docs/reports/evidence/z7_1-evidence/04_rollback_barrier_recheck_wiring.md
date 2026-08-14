# Z7.1 Evidence 04 - Rollback, Restore Barrier, and Runtime Recheck Wiring

## Rollback Wiring

### Runtime rollback

`tools/v7-users-autoswitch` performs normal movement rollback when:

- a move command succeeds,
- route verification is enabled,
- route verification fails,
- `--rollback-on-verify-fail` is active.

The rollback result is recorded inside `apply_result.results[]` with:

- `rollback_rc`
- `rollback_output`

Status: CONNECTED runtime rollback mechanics, MISSING operation lineage.

### Generic rollback

`tools/runtime-support/v7-rollback-last-change`:

- finds newest backup candidate,
- supports dry-run by default,
- applies with `--apply`,
- writes `v7-audit-log "rollback_last_change" "rollback" ...` if available.

Status: CONNECTED generic primitive, MISSING operation lineage.

### Admin rollback

`admin/v7-admin-api`:

- `/api/actions/rollback-preview` calls `v7-rollback-last-change`.
- `/api/actions/rollback-apply` requires `confirm=ROLLBACK`, audits the Admin action, then calls `v7-rollback-last-change --apply`.

Status: CONNECTED Admin rollback surface, DUPLICATED rollback path unless constrained as break-glass.

## Restore Barrier Wiring

### Connected

`tools/v7-users-autoswitch` reads `autoswitch-restore-barrier.json` and propagates barrier status into plan safety.

It recognizes:

- `enabled`
- `expires_at` / `suppress_until` / `active_until`
- `created_at` / `activated_at`
- `cleared`
- `allow_post_ttl_apply`
- `generation_clearance`
- `clearance_max_selected_moves`
- `clearance_generation_id`
- `approved_generation_id`
- `planner_generation_id`
- `selected_moves_generation`
- `approved_selected_moves_hash`
- `clearance_expected_selected_moves`
- `approved_selected_moves_count`
- `generation_token`

It checks:

- generation token presence,
- clearance expiry,
- current vs approved generation,
- selected move hash,
- selected move count.

### Partial

Admin/operator read adapters also read `autoswitch-restore-barrier.json`, but they are preview/read-only.

### Missing

The restore barrier lifecycle is not bound to `operation_id`.

## Runtime Recheck Wiring

### Autoswitch runtime recheck

Autoswitch performs runtime guard checks as part of plan/apply:

- current state inputs are hashed into `planner_generation_id`,
- restore barrier and generation clearance are checked,
- selected moves are recomputed at runtime before apply.

Status: CONNECTED mechanics, MISSING named `operation_id` lineage.

### Operator packet recheck

`admin_core/operator_execution.py` has a separate `runtime_recheck(packet, state_dir, now)` path:

- validates approval packet,
- reads `users.registry`,
- reads `egress.registry`,
- reads selected move state,
- computes `runtime_snapshot_hash`,
- compares expected hashes,
- requires selected moves to remain zero,
- returns `ALLOW_RECORD_ONLY` and explicitly marks `real_runtime_action_after_recheck=False`.

Status: CONNECTED governance recheck, not runtime execution recheck.

## Verdict

Rollback, restore barrier, and recheck mechanics exist. Their operation lineage is partial or missing. Operator recheck is a duplicate-looking governance chain but not a duplicate runtime execution chain because it is intentionally zero-move/read-only.

