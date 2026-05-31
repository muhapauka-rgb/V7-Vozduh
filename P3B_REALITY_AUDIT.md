# P3.B Reality Audit

Project: V7 Vozduh
Program: P3
Block: P3.B Runtime Hook Dry-Run Foundation
Mode: Architecture / Discovery / Hook Design / Certification

## Baseline

- Current branch: `v7-next`
- Local HEAD: `afcdd9cc61b7a1302c8785489991b0eac217b395`
- P3.A status: complete
- P3.A continuation verdict: `safe_to_continue_to_runtime_hook_dryrun=true`
- Runtime actions during this audit: none

## Repository Reality

The repository already has runtime observers, dry-run evaluators, execution preview models, candidate workflow, readiness, simulation, verification, rollback previews, and operator observability. P3.B must design passive hook foundations around those existing sources. It must not create a second autoswitch engine, execution engine, runtime event bus, routing hook, or decision state writer.

## Existing Runtime Observers

| Existing location | Behavior | P3.B decision |
| --- | --- | --- |
| `tools/v7-observability-summary` | Read-only summary; states it does not run probes, write state, change routing, trigger autoswitch, or mutate runtime. | Reuse as observer summary model. |
| `tools/runtime-support/v7-state-json` | Builds runtime JSON from state, registry, policy, route-class and trust files. | Reuse as state snapshot input model. |
| `admin/v7-admin-api` runtime fingerprint/drift/convergence helpers | Read runtime files and expose runtime status. | Reuse as admin presentation/read model. |
| `tools/v7-telegram-sentinel` | Observes service state and writes sentinel/service evidence; also can call autoswitch. | Reuse only produced evidence; forbid hook action calls. |
| `tools/runtime-support/v7-trusted-ru-diagnostic` | Produces trusted RU diagnostic evidence. | Reuse as trust evidence input. |
| `tools/runtime-support/v7-trusted-ru-decision` | Read-only routing decision preview by default; optional `--write-state`. | Reuse read-only output only. |
| `tools/runtime-support/v7-proxy-service-aware-routing-dry-run` | Read-only service-aware route candidate; explicitly does not write, route, open ports or move users. | Reuse as simulation input. |
| `tools/runtime-support/v7-proxy-public-enable-guard-dry-run` | Read-only final gate before public proxy enable. | Reuse as safety evidence. |

## Existing Evaluators

| Existing location | Behavior | P3.B decision |
| --- | --- | --- |
| `tools/v7-users-autoswitch` | Guarded autoswitch planner; read-only by default, optional `--apply`. Contains candidate scoring, gates, route class/service logic and verification calls after apply. | Reuse non-apply evaluator semantics only. |
| `tools/v7-second-canary-target-readiness` | Read-only target readiness with `execution_allowed_now=false`. | Reuse readiness gate semantics. |
| `admin/v7-admin-api` execution preview functions | Validation, verification, rollback, readiness, outcome, blast radius, service impact, forecast and candidate workflow previews. | Reuse as canonical preview family. |
| `admin_core/operator_observability.py` | Operator governance/rehearsal/readiness aggregation with disabled action controls. | Reuse as observability presentation model. |

## Existing Candidate And Execution Surfaces

`admin/v7-admin-api` exposes viewer-only routes for:

- `/api/execution/summary`
- `/api/execution/contracts`
- `/api/execution/timeline`
- `/api/execution/events`
- `/api/execution/verification`
- `/api/execution/rollback`
- `/api/execution/validation-preview`
- `/api/execution/verification-preview`
- `/api/execution/rollback-preview`
- `/api/execution/readiness-preview`
- `/api/execution/gates`
- `/api/execution/readiness`
- `/api/execution/outcome-preview`
- `/api/execution/blast-radius`
- `/api/execution/service-impact`
- `/api/execution/readiness-forecast`
- `/api/execution/rollback-impact`
- `/api/execution/candidates`
- `/api/execution/candidate-approval`
- `/api/execution/candidate-governance`
- `/api/execution/candidate-rehearsal`
- `/api/execution/candidate-workflow`

Contract tests assert these routes remain read-only and that mutating execution endpoints such as `/api/execution/apply`, `/api/execution/execute`, `/api/execution/route-apply`, and `/api/execution/autoswitch-apply` are absent.

## Reuse / Extend / Do Not Touch

| Area | Classification | Reason |
| --- | --- | --- |
| Existing observer outputs | Reuse | They are already runtime truth/evidence sources. |
| Execution preview API family | Reuse | It already owns preview-only contract/readiness/simulation/verification/rollback vocabulary. |
| Candidate workflow | Reuse | It already bridges candidate, approval, governance and rehearsal previews. |
| Autoswitch planner/evaluator | Extend by reference only | Non-apply semantics are useful; apply authority is forbidden. |
| Sentinel | Extend by consumption only | Evidence is useful; autoswitch trigger is forbidden for hooks. |
| Trusted RU decision | Extend by read-only consumption only | `--write-state` must remain outside P3.B. |
| Operator execution | Do not use as hook engine | Execution-named and append-capable boundary. |
| New runtime hook daemon | Do not create | P3.B is architecture-only. |
| New event stream/store | Do not create | Existing event/audit stores remain canonical. |

## Reality Verdict

`reality_audit_complete=true`

