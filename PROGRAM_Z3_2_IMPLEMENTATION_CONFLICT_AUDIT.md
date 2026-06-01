# PROGRAM Z3.2 Implementation Conflict Audit

Purpose: verify that Z3.2 reused existing authority and did not create a parallel autonomy system.

## Inspected Implementations

| Area | Existing implementation | Z3.2 decision |
| --- | --- | --- |
| Autoswitch planner/apply | live `/usr/local/bin/v7-users-autoswitch`, repo `tools/v7-users-autoswitch` | Reuse |
| Proposal cap | repo `tools/v7-autoswitch-proposal-cap` | Reuse for bounded proposal semantics |
| Hybrid approval | repo `admin_core/hybrid_approval.py`, `tools/v7-hybrid-approval-contract` | Reuse as governance contract |
| Runtime recheck | live filtered planner recheck plus generation-bound restore barrier | Reuse |
| Movement authority | live `/usr/local/bin/v7-users-autoswitch --apply` and `v7-user-switch` | Reuse |
| Rollback authority | live `/usr/local/bin/v7-user-switch` | Reuse |
| Verification | live `v7-user-route-check`, `v7-reconcile-check`, `v7-killswitch-check`, `v7-restore-settle-gate` | Reuse |

## Conflict Findings

No parallel execution engine was added.

Z3.2 did not add a second movement authority, second planner, second rollback command, or second runtime checker. The live movement used the existing autoswitch engine and the live rollback used the existing user-switch authority.

The new work in this turn is report-only. It records evidence from the live Z3.2 run.

## Important Boundary

The live execution path used a generation-bound clearance packet in `autoswitch-restore-barrier.json` plus a fresh filtered planner/apply command. The hybrid approval contract remains the repo governance validator, but no new direct runtime integration was implemented in Z3.2.

## Classification

- Reuse: autoswitch planner/apply, proposal cap, hybrid approval contract, runtime checks, rollback authority.
- Extend: documentation evidence only.
- Refactor: none.
- Replace: none.
- Do Not Touch: deploy, systemd, routing outside selected user, top-level runtime architecture.

## Safety

- duplicate_autonomy_system_created=false
- duplicate_movement_authority_created=false
- duplicate_rollback_authority_created=false
- execution_engine_implemented=false
- systemd_changed=false
- deploy_performed=false

