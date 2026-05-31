# P3.A Runtime Audit

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Scope

This is a repository architecture audit. No live runtime mutation, deployment, routing change, systemd change, user movement or autoswitch apply was performed.

## Runtime Inputs Already Present

| Input | Role in runtime dry-run |
| --- | --- |
| `service-matrix.json` | Required-service health and degradation evidence. |
| `telegram-sentinel.json` and sentinel JSONL | Telegram availability and service observer events. |
| `egress-quality-summary.json` | Egress quality and routing readiness evidence. |
| `egress-load-summary.json` | Load and capacity pressure evidence. |
| `autoswitch-safety.json` | Autoswitch safety gate evidence. |
| `client-reconnect-state.json` | Client reconnect and user-impact evidence. |
| Trusted RU diagnostic state | RU trust and diagnostic evidence. |
| Trusted RU decision state | Read-only routing decision evidence. |
| `user-flow-trace` state | User-flow and routing truth evidence. |
| Selected moves state | Existing selected movement evidence. |
| Restore barrier state | Rollback/restore safety evidence. |
| Registries | Authority, service ownership and policy references. |

## Runtime Observability Surfaces

| Surface | Current behavior |
| --- | --- |
| Admin runtime fingerprint | Shows runtime identity and drift facts. |
| Admin runtime convergence | Shows convergence state and mismatches. |
| Admin runtime drift | Shows runtime drift records. |
| Admin execution readiness | Shows readiness gates, blockers, owners and reviews. |
| Operator observability | Aggregates governance, rehearsal, selected moves and barriers. |
| Observability summary tool | Produces read-only summaries without probes or mutations. |

## Runtime Action Surfaces To Exclude

| Surface | Reason excluded from P3.A |
| --- | --- |
| Autoswitch apply | User movement/routing effect possible. |
| Sentinel autoswitch trigger | Action-adjacent runtime hook behavior. |
| Trusted RU `--write-state` mode | Writes runtime decision state. |
| Operator execution append/execute modes | Execution-named and audit-writing boundary. |
| Any service/systemd control | Forbidden. |
| Any deploy or route apply | Forbidden. |

## Dry-Run Runtime Boundary

Runtime dry-run may:

- Read existing state.
- Normalize existing events.
- Evaluate what the system would decide.
- Produce non-authoritative reports.
- Compare predictions with later observed evidence.

Runtime dry-run may not:

- Write runtime state.
- Start, stop or reload services.
- Change routing.
- Move users.
- Execute approvals.
- Call autoswitch apply.
- Register runtime hooks with action authority.

## Runtime Verdict

`runtime_audit_complete=true`

