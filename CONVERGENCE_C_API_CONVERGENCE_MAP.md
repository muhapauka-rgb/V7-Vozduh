# Convergence C API Convergence Map

Project: V7 Vozduh
Block: Convergence C / Wave 1 Runtime Read API Preservation
Date: 2026-05-31

## Map

| Runtime API | Runtime behavior | Branch status | Local dirty worktree status | Decision |
| --- | --- | --- | --- | --- |
| `/api/execution/summary` | Execution read summary and store consistency | Preserved | Present | Keep runtime-compatible |
| `/api/execution/contracts` | Contract summary list | Preserved | Present | Keep runtime-compatible |
| `/api/execution/contracts/` | Contract detail by id | Preserved | Present | Keep runtime-compatible |
| `/api/execution/timeline` | Execution event timeline | Preserved | Present | Keep runtime-compatible |
| `/api/execution/events` | Execution event list | Preserved | Present | Keep runtime-compatible |
| `/api/execution/verification` | Verification read preview | Preserved | Present | Keep runtime-compatible |
| `/api/execution/rollback` | Rollback read preview | Preserved | Present | Keep runtime-compatible |
| `/api/execution/explain` | Explanation read preview | Preserved | Present | Keep runtime-compatible |

## Deferred Local APIs

Local-only APIs are excluded from Wave 1 and must be reviewed as separate convergence candidates.

Primary deferred families:

- Candidate workflow.
- Approval/governance previews.
- Draft contracts.
- Gates and readiness.
- Validation and verification preview expansions.
- Rollback impact and service impact previews.
- Outcome preview.

## Compatibility Rule

Wave 1 must not reduce runtime read compatibility and must not add execution capability.

## Verdict

api_convergence_map_complete=true

Safety:

- runtime_mutation_performed=false
- routing_changed=false
- users_moved=false
- autoswitch_apply_run=false
- deploy_performed=false
- git_push_performed=false
- systemd_changed=false
