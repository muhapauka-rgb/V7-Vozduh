# Program A.C Discovery / Duplication Audit

Date: 2026-06-02

Scope: service-aware best available pool and capacity-aware policy implementation for `tools/v7-users-autoswitch`.

## Existing Ownership Reused

The implementation reuses the existing autoswitch planner and does not create a second planner, second orchestrator, duplicate scheduler, duplicate state writer, duplicate execution path, or duplicate truth source.

Existing reused surfaces:

- `AutoswitchPlanner._decision_for_user`: primary candidate evaluation and action recommendation owner.
- `AutoswitchPlanner._candidate`: central candidate gate and score owner.
- `AutoswitchPlanner._pick_projected_moves`: selected move projection owner.
- `AutoswitchPlanner._projected_target_for_move`: projected target selection owner.
- Existing safety gates: user safety, reservation/manual-only gates, restore barrier, cooldown/sticky, relative improvement, quality/load gates.
- Existing state readers: egress inventory, service matrix, quality summary, load summary, restore barrier, user state.
- Existing audit/selected move outputs: dry-run operation payload and selected move records.

## Classification

| Component | Classification | Reason |
| --- | --- | --- |
| `tools/v7-users-autoswitch` planner | EXTEND | Existing execution planning owner; safest place to add pool/capacity policy without duplicate authority. |
| Existing service-aware policy from Program A.B | EXTEND | A.C builds directly on service suitability and contextual quality decisions. |
| Existing projected move picker | EXTEND | Already distributes moves by projected load; A.C constrains it to best available pool when present. |
| Existing hard gates | REUSE | Safety, reservation, route class, quality, service, load, sticky, anti-flap remain in the existing chain. |
| Existing truth/release sync tools | REUSE | Used for read-only convergence checks and dry-run release planning. |
| Production runtime binary | DO_NOT_TOUCH | A.C did not deploy or mutate production. |
| Systemd services/timers | DO_NOT_TOUCH | No restart, enable/disable, or timer changes were performed. |

## Duplication Gate Result

- duplicate planner: none created
- duplicate execution path: none created
- duplicate state writer: none created
- duplicate scheduler: none created
- duplicate selected move writer: none created
- duplicate restore barrier path: none created
- runtime mutation: none
- autoswitch apply: none

## Local Dirty State Blocking Live Sync

Final truth/release checks report dirty runtime-critical local work:

- `tools/v7-users-autoswitch`: modified, runtime-critical
- `tests/unit/test_best_available_pool_policy.py`: untracked, runtime-relevant
- `tests/unit/test_service_aware_policy.py`: untracked, runtime-relevant
- evidence/report files: documentation-only

This is expected for the implementation phase and blocks production convergence until commit/push/safe release sync are explicitly approved.
