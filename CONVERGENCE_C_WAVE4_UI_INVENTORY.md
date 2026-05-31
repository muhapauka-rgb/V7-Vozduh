# Convergence C Wave 4 UI Inventory

| Surface | Purpose | Owner | Truth Source | Displayed Data | Dependencies |
| --- | --- | --- | --- | --- | --- |
| Execution Drawer | Primary execution/candidate drill-down | Admin UI | Execution APIs | Summary, candidates, readiness, gates, contracts | Wave 1-3 APIs |
| Candidate Drawer | Not a separate drawer; candidate uses Execution Drawer | Admin UI | Candidate APIs | Candidate detail and workflow mapping | Wave 3 APIs |
| Approval Center | Approval summary and disabled actions | Operator UI | `operator_approval_preview` | Preview contracts, disabled controls | Runtime/operator API |
| Operator Tab | Summary and operator workflow bridge | Operator UI | Operator overview + candidate workflow | Candidate bridge, governance, rehearsal | Wave 3 API |
| Checks | Existing checks surface | Admin UI | diagnostics/check APIs | Readiness and checks | Unchanged |
| Logs | Existing logs surface | Admin UI | events/audit APIs | Timeline and audit | Unchanged |
| Home | Summary surface | Admin UI | runtime/release/execution summary | Trust cards | Wave 4 execution card |
| Users | Existing user surface | Admin UI | users registry | User state | Unchanged |
| Channels | Existing channel surface | Admin UI | egress registry | Channel state | Unchanged |
| Routes | Existing routing surface | Admin UI | route state | Route reality | Unchanged |

## Verdict

ui_inventory_complete=true
