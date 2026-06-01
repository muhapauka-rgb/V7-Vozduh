# P4.B Admin Surface Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Existing Surfaces

Use existing:

- Execution Drawer
- Approval Center
- Checks
- Logs
- Operator
- Dry-Run Verification
- Rollback Preview

## Visibility

| Item | Surface |
| --- | --- |
| Packet | Execution Drawer / Operator detail |
| Approval | Approval Center |
| Abort | Checks / Operator timeline |
| Verification | Dry-Run Verification / Execution Verification |
| Rollback preview | Rollback Preview / Operator rollback |
| Replay protection | Audit search / Operator timeline |
| Observation | Logs / Checks / Operator timeline |

## No New Top-Level Section

No new top-level admin section is required.

## Forbidden Controls

Do not expose:

- Execute
- Apply
- Move user
- Route apply
- Autoswitch apply
- Rollback execute
- Deploy
- Systemd change

## Verdict

`admin_surface_spec_complete=true`

