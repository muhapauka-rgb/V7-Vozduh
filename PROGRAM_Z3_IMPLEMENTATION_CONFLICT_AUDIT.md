# Program Z3 Implementation Conflict Audit

Date: 2026-06-01

## Verdict

implementation_conflict_audit_complete=true
duplicate_runtime_system_created=false

## Existing Implementations

| Area | Existing implementation | Z3 decision |
| --- | --- | --- |
| Planner | live `/usr/local/bin/v7-users-autoswitch` | Reuse. |
| Proposal cap | repo `tools/v7-autoswitch-proposal-cap` | Reuse for bounded proposal semantics; live planner remains truth. |
| Hybrid approval | repo `admin_core/hybrid_approval.py`, `tools/v7-hybrid-approval-contract` | Reuse. |
| Runtime recheck | Z2 hybrid validator plus live registry/planner hashes | Reuse/extend by evidence. |
| Movement authority | live `/usr/local/bin/v7-user-switch` | Reuse only after valid live packet. Not invoked in Z3 because recheck failed. |
| Rollback authority | live `/usr/local/bin/v7-user-switch` rollback to prior egress | Reuse conceptually, not executed. |
| Verification | live `v7-user-route-check`, `v7-reconcile-check`, `v7-killswitch-check`, `v7-restore-settle-gate` | Reuse. |

## Runtime Tools Present

The following live tools exist:

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-user-switch`
- `/usr/local/bin/v7-second-canary-target-readiness`
- `/usr/local/bin/v7-restore-settle-gate`
- `/usr/local/bin/v7-user-route-check`
- `/usr/local/bin/v7-reconcile-check`
- `/usr/local/bin/v7-killswitch-check`

## Conflict Finding

No new executor was required or created. The live planner has an existing governance guard that prevents selected movement:

`restore_barrier_clearance_selected_moves_exceed_budget`

Z3 must not bypass that guard by directly invoking `v7-user-switch`.

## Safety

- movement_authority_duplicated=false
- autoswitch_apply_run=false
- v7_user_switch_invoked=false
- systemd_changed=false
- deploy_performed=false

