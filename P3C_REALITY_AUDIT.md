# P3.C Reality Audit

Project: V7 Vozduh
Program: P3
Block: P3.C First Runtime Dry-Run

## Baseline

- Current branch: `v7-next`
- Local HEAD: `afcdd9cc61b7a1302c8785489991b0eac217b395`
- P3.A complete: yes
- P3.B complete: yes
- P3.B continuation verdicts present: `safe_to_continue_to_first_runtime_dry_run=true`, `hook_certified_non_executable=true`

## Existing Paths Found

| Searched area | Existing path | Decision |
| --- | --- | --- |
| Runtime observers | `tools/v7-observability-summary`, runtime fingerprint/drift/convergence helpers | Reuse read-only evidence vocabulary. |
| Autoswitch non-apply evaluator | `tools/v7-users-autoswitch` default dry-run planner | Do not call from P3.C; reuse output vocabulary only. |
| Sentinel observer output | `tools/v7-telegram-sentinel` | Consume state only in future; do not invoke action path. |
| Trusted RU preview | `tools/runtime-support/v7-trusted-ru-decision`, `trusted_ru_decision_state()` | Reuse read-only state reader; no `--write-state`. |
| State JSON tools | `tools/runtime-support/v7-state-json` | Reuse source model; P3.C reads files directly inside admin API. |
| Observability summary | `tools/v7-observability-summary` | Reuse model as report-only reference. |
| Execution preview | `/api/execution/*` preview/read family | Reuse contracts/events/candidate preview helpers. |
| Candidate workflow | `/api/execution/candidate-workflow` and `execution_candidates_from_query()` | Reuse derived candidate state. |
| Readiness/simulation/verification/rollback | Existing execution preview helpers | Reuse as derived evidence and report references. |

## Implementation Decision

P3.C implements the smallest safe path:

- `GET /api/runtime/dry-run/summary`
- Derived-on-demand report object.
- Read-only input adapters over existing files and preview helpers.
- Evaluator restricted to allowed `NO_ACTION` / `WOULD_*` outputs.
- Existing `/admin-v2` surfaces only: Trust overview and Operator preview.

## Reality Verdict

`reality_audit_complete=true`

