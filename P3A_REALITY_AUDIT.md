# P3.A Reality Audit

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation
Mode: Architecture / Discovery / Dry-Run Preparation

## Branch And Baseline

- Current branch: `v7-next`
- Local HEAD: `afcdd9cc61b7a1302c8785489991b0eac217b395`
- Prior certification signal: P2.9 reported `safe_to_continue_to_runtime_dry_run=true`
- Runtime actions performed during this audit: none

## Existing Runtime And Dry-Run Reality

The repository already contains a substantial preview and observability surface. P3.A must not create a parallel runtime engine. It must define a foundation that reuses existing read-only truth sources and preview adapters.

## Existing Observers

| Area | Existing location | Behavior | P3.A decision |
| --- | --- | --- | --- |
| Runtime state summary | `tools/runtime-support/v7-state-json` | Produces runtime JSON from state files and policy previews. | Reuse as read-only input adapter. |
| Operator observability | `admin_core/operator_observability.py` | Aggregates barriers, selected moves, approvals, audit, governance and rehearsal previews. | Reuse as operator-facing aggregation source. |
| Admin runtime views | `admin/v7-admin-api` | Exposes runtime fingerprint, drift, convergence, health and diagnostics responses. | Extend conceptually through preview-only dry-run views. |
| Service matrix | `service-matrix.json` readers in tools/admin | Provides service health and required-service evidence. | Reuse as canonical service health input. |
| Telegram sentinel | `tools/v7-telegram-sentinel` | Observes Telegram availability and writes sentinel/service evidence; also has an autoswitch action path. | Reuse only produced state; never call action authority. |
| Trusted RU diagnostic | `tools/runtime-support/v7-trusted-ru-diagnostic` and admin readers | Captures RU trust and diagnostic evidence. | Reuse as trust evidence input. |
| Trusted RU decision | `tools/runtime-support/v7-trusted-ru-decision` | Computes routing decision preview; optional state write exists. | Reuse read-only decision preview only; no write mode. |
| Proxy routing dry-run | `tools/runtime-support/v7-proxy-service-aware-routing-dry-run` | Evaluates route candidates without writing, routing, nft, ports or user movement. | Reuse as route simulation evidence. |
| Proxy enable guard dry-run | `tools/runtime-support/v7-proxy-public-enable-guard-dry-run` | Final read-only public-enable guard. | Reuse as safety gate evidence. |

## Existing Events And Logs

| Store | Existing role | P3.A interpretation |
| --- | --- | --- |
| `AUDIT_FILE` | Admin/operator audit log. | Canonical audit event source. |
| `EVENT_DIR` / `switch-history.jsonl` | Autoswitch and movement-adjacent history. | Canonical runtime movement-event history; read-only. |
| `EXECUTION_EVENTS_FILE` | Execution preview and contract event timeline. | Canonical execution-preview event source. |
| Telegram sentinel daily JSONL | Service observer evidence. | Canonical service observer event evidence. |
| `USER_FLOW_TRACE_FILE` | User-flow trace and routing truth evidence. | Read-only routing/user-flow evidence. |

## Existing Evaluators And Preview Engines

| Area | Existing behavior | P3.A decision |
| --- | --- | --- |
| Autoswitch evaluator | `tools/v7-users-autoswitch` contains candidate selection, gates, scoring and explanations. | Reuse evaluator semantics only in non-apply mode. |
| Execution readiness | `admin/v7-admin-api` exposes readiness previews, gates, blockers, owners, reviews and explanations. | Reuse as dry-run readiness source. |
| Execution candidate workflow | `admin/v7-admin-api` exposes candidate queue/detail/workflow and P2.7 approval states. | Reuse candidate/review semantics. |
| Simulation previews | Admin API exposes service impact, blast radius, rollback impact, readiness forecast and outcome preview. | Reuse as dry-run simulation vocabulary. |
| Verification previews | Admin API exposes validation, verification, rollback and explain previews. | Reuse for P3.A verification model. |
| Governance and rehearsal previews | `admin_core/operator_observability.py` and admin API expose governance/rehearsal previews. | Reuse as dry-run governance evidence. |

## Existing Runtime Guardrails

The existing preview family already uses safety flags such as:

- `read_only`
- `derived_only`
- `preview_only`
- `non_authoritative`
- `execution_allowed_now=false`
- `runtime_mutation_performed=false`
- `routing_changed=false`
- `users_moved=false`
- `autoswitch_apply_run=false`
- `execution_engine_implemented=false`
- `runtime_hooks_implemented=false`

P3.A keeps this pattern and makes the dry-run foundation explicitly non-authoritative.

## Classification

| Component family | Classification | Reason |
| --- | --- | --- |
| Admin execution preview APIs | Reuse | They already model contracts, readiness, simulation, verification and rollback as previews. |
| Operator observability | Reuse | It already aggregates operator-facing truth without movement. |
| Autoswitch evaluator | Extend carefully | Reuse scoring and gate semantics, but not apply mode. |
| Telegram sentinel | Extend carefully | Reuse observer output only; action leg is out of scope. |
| Trusted RU decision | Extend carefully | Reuse read-only preview only; state write mode is out of scope. |
| `admin_core/operator_execution.py` | Do Not Touch for P3.A | It has audit append and execution-named entry points; not part of dry-run foundation. |
| New runtime executor | Do Not Create | Forbidden by P3.A. |
| New routing hook | Do Not Create | Forbidden by P3.A. |

## Reality Verdict

`reality_audit_complete=true`

