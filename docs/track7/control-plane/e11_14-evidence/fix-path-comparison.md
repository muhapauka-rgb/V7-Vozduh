# BLOCK E11.14 Fix Path Comparison

fix_path_review_completed=true

| Fix path | Operational simplicity | Blast radius | Rollback clarity | Regression risk | Production viability | Cohort scalability | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Longer restore-settle | Simple | Low | Easy | Medium | Weak | Weak | REJECTED: does not bind future apply cycles. |
| Apply warmup delay | Simple | Low | Easy | Medium | Weak | Weak | REJECTED: delays but does not prevent transient after delay. |
| selected_moves invalidation | Medium | Low | Easy | Low | Weak | Weak | REJECTED: incident was not stale selected_moves. |
| planner cache flush | Medium | Low | Easy | Low | Weak | Weak | REJECTED: apply recomputed fresh. |
| delayed apply suppression window | Medium | Low | Easy | Low | Strong | Strong | SELECTED as restore barrier. |
| explicit clean apply cycle count | Medium | Medium | Medium | Medium | Conditional | Conditional | DEFER: would require carefully bounded live apply rehearsal. |
| planner/apply generation ID | High | Medium | Medium | Medium | Strong | Strong | DEFER: useful later, broader implementation. |
| restore barrier token | Medium | Low | Easy | Low | Strong | Strong | SELECTED. |
| apply timer quarantine window | Medium | Low | Easy | Low | Strong | Strong | SELECTED via barrier + apply hold. |
| non-cohort protection | High | Medium | Medium | Medium | Strong | Strong | DEFER: requires movement authorization model. |
| apply generation mismatch rejection | High | Medium | Medium | Medium | Strong | Strong | DEFER: broader planner/apply protocol change. |

## Selected Fix

fix_path_selected=RESTORE_BARRIER_FAILOVER_QUARANTINE

The selected bounded fix:

- Adds `--restore-barrier-file`, defaulting to `/opt/v7/egress/state/autoswitch-restore-barrier.json`.
- Adds active barrier metadata into plan safety output.
- Suppresses failover selection while restore barrier is active.
- Extends service-signal-only classification to include `telegram_required_*`.
- v2 correction was required because final live dry-run showed non-service failover pressure (`awg0` stability below floor) after the original service-signal-only barrier.
- Leaves non-service failures eligible.
- Does not run manual autoswitch apply.
- Does not move users.

Rollback:

- Restore `/usr/local/bin/v7-users-autoswitch` from backup `/usr/local/bin/v7-users-autoswitch.e11_14_backup_20260527T105151Z`.
- Disable or remove `/opt/v7/egress/state/autoswitch-restore-barrier.json`.
- Keep apply timer held unless a separate apply-restore approval block authorizes restoration.
