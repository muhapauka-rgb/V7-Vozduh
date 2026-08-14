# JSON Contract Audit

## Current Autoswitch Root Output

`tools/v7-users-autoswitch` currently prints one JSON object from `main()`:

```text
plan = planner.plan()
plan["apply_result"] = planner.apply(plan)
print(json.dumps(plan, ...))
return 0
```

Current root fields from `plan()` and `main()`:

| Field | Producer | Consumer Sensitivity |
|---|---|---|
| `schema_version` | `plan()` | Must remain numeric root field |
| `updated` | `plan()` | Keep |
| `enabled` | `plan()` | Admin/UI reads |
| `mode` | `plan()` | Admin/UI reads |
| `apply_requested` | `plan()` | Historical reports, operator reasoning |
| `target_egress` | `plan()` | Admin target-scoped workflows |
| `safety` | `plan()` | Admin/UI reads `anti_flap`, `generation`, `restore_barrier` |
| `summary` | `plan()` | Admin/UI and reports read counts |
| `dynamic_load` | `plan()` | Admin/UI reads load/capacity |
| `reconnect_events` | `plan()` | Reports/observability |
| `quality_history` | `plan()` | Admin/UI |
| `org_isolation` | `plan()` | Reports/Admin |
| `decisions` | `plan()` | Admin/UI, tests |
| `selected_moves` | `plan()` | Admin/UI, tests, historical evidence |
| `apply_result` | `main()` | Admin guarded apply and historical evidence |

## Current Nested Contract

`safety.generation` already contains:

- `schema_version`
- `planner_generation_id`
- `inputs`

`safety.restore_barrier` already carries barrier lifecycle and clearance fields:

- `enabled`
- `active`
- `expired`
- `cleared`
- `post_ttl_blocking`
- `clearance_max_selected_moves`
- `clearance_selected_moves_hash`
- `current_selected_moves_hash`
- `approved_selected_moves_hash`
- generation clearance ids/reasons

`summary` currently carries:

- `users_total`
- `egress_total`
- `healthy_egress_total`
- `candidate_moves`
- `candidate_moves_total`
- `selected_moves`
- `reconnect_rotation_candidates`
- `rebalance_candidates`
- `org_groups`

`apply_result` currently returns:

- no-apply variants: `{ "applied": false, "reason": "..." }`
- apply variant: `{ "applied": true, "results": [...], "safety_file": "..." }`

Result rows currently include:

- `user_ip`
- `from`
- `to`
- `move_type`
- `rc`
- `output`
- optional `verify_rc`
- optional `verify_output`
- optional `rollback_rc`
- optional `rollback_output`

## Safe Additive Fields

Safe if additive and not used as independent truth stores:

- root `operation`
- root `operation_id`
- root `runtime_snapshot_hash`
- root `selected_move_hash`
- root `terminal_state`
- root `terminal_reason`
- root `audit`
- root `closure`
- selected move row `operation_id`
- apply result row `operation_id`

Safer envelope location:

```text
root.operation = {
  operation_id,
  operation_owner,
  operation_type,
  planner_generation_id,
  selected_move_hash,
  runtime_snapshot_hash,
  terminal_state,
  terminal_reason,
  audit_ref,
  closure_target
}
```

Root aliases may be added for convenience, but `operation` should be canonical to reduce root-level clutter.

## Fields That Must Not Change

- `selected_moves` must remain a list.
- `summary.selected_moves` must remain a count.
- `decisions` must remain a list of decision objects.
- `apply_result.applied` must remain boolean.
- `apply_result.reason` must remain a string for no-op/deny paths.
- `apply_result.results` must remain a list for apply path.
- `schema_version=1` should not be bumped unless a migration is planned.
- stdout must remain one parseable JSON object.
- process exit code should remain `0` for normal dry-run/no-op/guard-denied planning.

## Strictness Verdict

New fields can be safely added if they are additive. Contract risk becomes HIGH if implementation:

- wraps the whole current output under a new envelope,
- replaces `selected_moves` list with an object,
- moves `apply_result`,
- changes no-op result reasons,
- changes stdout from pure JSON,
- changes exit code semantics.
