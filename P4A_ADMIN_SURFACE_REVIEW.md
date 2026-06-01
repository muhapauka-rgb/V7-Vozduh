# P4.A Admin Surface Review

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Existing Surfaces

Reviewed:

- Execution Drawer
- Approval Center
- Checks
- Logs
- Operator
- Dry-Run Summary
- Dry-Run Verification

## Placement

| P4.A Object | Existing surface |
| --- | --- |
| First action packet | Execution Drawer / Operator operation detail |
| Approval | Approval Center / Operator approval preview |
| Pre-action recheck | Checks / Execution readiness |
| Abort | Checks / Operator timeline |
| Rollback preview | Rollback Preview / Operator rollback |
| Observation | Logs / Operator timeline / Audit search |

## No New Top-Level Section

P4.A requires no new top-level admin section.

## Forbidden Controls

Do not add execute, apply, move, route, autoswitch, rollback execute, deploy or systemd controls.

## Verdict

`admin_surface_review_complete=true`

