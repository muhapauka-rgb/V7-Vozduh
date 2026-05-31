# P3.B Runtime Audit

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Scope

This audit inspects repository runtime evidence sources and action boundaries. It does not inspect or mutate a live runtime.

## Runtime Evidence Sources

| Evidence | Source family | Hook use |
| --- | --- | --- |
| Health | Service matrix, sentinel state, system checks, admin runtime health | Observe freshness and health status. |
| Capacity | `egress-load-summary.json`, capacity readiness/check helpers | Evaluate capacity gates. |
| Required services | Service matrix route-class/service fitness | Evaluate required-service gates. |
| Runtime trust | Trusted RU diagnostic/decision, runtime trust store | Evaluate trust gates. |
| Release trust | Release trust store | Evaluate release/risk gates. |
| Candidate state | Proposal records, evidence bundles, execution candidate models | Evaluate candidate eligibility. |
| Execution state | Execution contracts/events and preview APIs | Evaluate contract and event context. |
| Audit state | Admin/operator audit logs | Explain operator history and governance state. |
| Sentinel state | Telegram sentinel state and daily observer JSONL | Observe service-specific degradation. |
| Autoswitch inputs | Users/egress registries, switch policy, safety file, service matrix, restore barrier | Evaluate what autoswitch would recommend without apply. |
| Rollback state | Restore barrier, rollback manifest, rollback impact preview | Evaluate rollback feasibility. |

## Existing Hook-Like Behaviors

| Behavior | Existing implementation | P3.B status |
| --- | --- | --- |
| Periodic service observation | Sentinel and observability summaries | Evidence source only. |
| Runtime summary production | `v7-state-json`, admin runtime views | Input adapter only. |
| Candidate scoring | Autoswitch planner | Non-apply evaluation only. |
| Runtime governance/rehearsal | Operator observability | Presentation/reuse. |
| Verification | Execution preview and route checker references | Report-only; no checker execution from hook. |

## Runtime Mutating Boundaries

The hook foundation must stay outside:

- Autoswitch apply.
- Policy apply.
- Routing apply.
- User switch/movement commands.
- Runtime decision state writes.
- Systemd/service commands.
- Deployment commands.
- Operator execution append/execute modes.

## Runtime Audit Verdict

`runtime_audit_complete=true`

