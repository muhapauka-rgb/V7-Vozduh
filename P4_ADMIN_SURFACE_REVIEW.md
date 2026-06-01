# P4 Admin Surface Review

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Existing Surfaces

P4 reviewed existing surfaces:

- Approval Center
- Execution Drawer
- Checks
- Logs
- Operator
- Dry-Run Summary
- Dry-Run Verification
- Candidate Workflow

## Placement Decision

No new top-level admin section is required.

P4 Action Packet should appear inside existing `/admin-v2` areas:

| P4 Object | Existing surface |
| --- | --- |
| Action Packet | Execution Drawer / Operator operation detail |
| Approval | Approval Center / Operator approval preview |
| Verification | Execution Verification / Dry-Run Verification |
| Rollback | Rollback Preview / Operator rollback preview |
| Observation | Logs / Checks / Operator timeline |
| Runtime Recheck | Checks / Execution Readiness |

## Forbidden UI Controls

P4 must not add:

- Execute
- Apply
- Move user
- Route apply
- Autoswitch apply
- Rollback execute
- Deploy

## Verdict

`admin_surface_review_complete=true`

