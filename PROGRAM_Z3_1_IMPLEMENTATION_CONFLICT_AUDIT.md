# Program Z3.1 Implementation Conflict Audit

Date: 2026-06-01

## Verdict

implementation_conflict_audit_complete=true
duplicate_system_created=false

## Existing Implementations Reused

| Area | Existing implementation | Z3.1 decision |
| --- | --- | --- |
| Restore barrier | `/opt/v7/egress/state/autoswitch-restore-barrier.json` | Reuse and refresh governance fields. |
| Barrier rule | `tools/v7-users-autoswitch` restore barrier logic | Reuse exactly. |
| Restore settle gate | live `v7-restore-settle-gate` | Reuse for read-only readiness evidence. |
| Planner | live `v7-users-autoswitch` | Reuse as canonical proposal/selection source. |
| Proposal cap | repo `tools/v7-autoswitch-proposal-cap` | No duplicate; Z3.1 relies on live planner for barrier truth. |
| Runtime recheck | planner generation and selected-move hash check | Reuse existing generation-bound clearance check. |
| Movement authority | live `v7-user-switch` | Not invoked. |
| Rollback authority | live `v7-user-switch` | Not invoked. |

## Conflict Finding

No new clearance engine was created. Z3.1 refreshed the existing barrier file using fields already supported by `v7-users-autoswitch`:

- `clearance_max_selected_moves`
- `generation_token`
- `clearance_generation_id`
- `approved_selected_moves_hash`
- `clearance_expected_selected_moves`
- `clearance_expires_at`

## Safety

- movement_engine_duplicated=false
- direct_v7_user_switch_outside_approved_path=false
- deploy_performed=false
- systemd_changed=false

