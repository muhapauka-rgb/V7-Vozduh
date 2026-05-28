# E11.16 Generation Governance Design

## Selected Bounded Fix

fix_path_selected=RESTORE_BARRIER_POST_TTL_FAIL_CLOSED_CLEARANCE

The safest bounded fix is to make restore barriers fail closed after TTL until
an explicit governed clearance is present. TTL expiry no longer means apply is
authorized to perform failover.

## Runtime Semantics

`v7-users-autoswitch` now reports restore barrier fields:

- `active`: barrier TTL is currently active.
- `expired`: barrier TTL is in the past.
- `cleared`: barrier has explicit `cleared=true`, `allow_post_ttl_apply=true`,
  or `generation_clearance=true`.
- `post_ttl_blocking`: barrier expired and not cleared.
- `failover_quarantine`: barrier is active or expired without clearance.

Failover selection is suppressed when `failover_quarantine=true`.

Reasons:

- active barrier: `restore_barrier_failover_suppressed`
- expired uncleared barrier:
  `restore_barrier_post_ttl_generation_clearance_required`

## Clearance Model

Future governed clearance must be explicit and auditable. A later block may set
one of:

- `cleared=true`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`

Only after such clearance may post-TTL apply failover resume. That clearance
must include fresh target readiness, restore-settle, selected_moves, runtime
checks, hidden mover scan, and rollback/containment decision.

## Why This Is Bounded

- No routing logic was rewritten.
- No production user was moved.
- No `v7-user-switch` path was called.
- No manual autoswitch apply was called.
- The change only affects failover selection while a restore barrier exists and
  is not explicitly cleared.

## Follow-Up Generation Token

A stronger future model may add immutable generation IDs:

- `restore_generation_id`
- `planner_generation_id`
- `apply_generation_id`
- `clearance_generation_id`

The E11.16 fix is intentionally smaller: it prevents unsafe post-TTL failover
now and creates a clearance hook for the later full generation-token model.

