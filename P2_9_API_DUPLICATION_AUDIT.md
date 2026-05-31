# P2.9 API Duplication Audit

Project: V7 Vozduh
Branch: `v7-next`
Mode: Read-only audit
Date: 2026-06-01

## Scope

Audited route maps, role maps, GET handlers, POST action boundaries, execution preview APIs,
operator APIs, and contract tests.

## Canonical API Families

The admin API keeps one public execution read/preview family under `/api/execution/*`:

- stored execution reads: `summary`, `contracts`, `timeline`, `events`, `verification`, `rollback`, `explain`
- draft/preview reads: `contracts/draft`, `validation-preview`, `verification-preview`, `rollback-preview`, `readiness-preview`
- readiness reads: `gates`, `readiness`, `readiness/detail`, `readiness/explain`, `readiness/owners`, `readiness/actions`, `readiness/blockers`, `readiness/reviews`, `validation-evidence`
- simulation/impact previews: `outcome-preview`, `blast-radius`, `service-impact`, `readiness-forecast`, `rollback-impact`
- candidate bridge reads: `candidates`, `candidates/readiness`, `candidates/risks`, `candidates/explain`, `candidates/timeline`, `candidate-approval`, `candidate-governance`, `candidate-rehearsal`, `candidate-workflow`

Operator governance APIs remain under `/api/operator/*` and are preview/read-only surfaces.

## Duplication Findings

The previously deferred simulation routes are now present in the canonical execution preview family,
not as a separate simulation engine. Approval, governance, and rehearsal APIs are bridge read models
that reuse existing operator preview helpers. No duplicate approval API family, governance engine API,
rehearsal engine API, or dry-run executor API was found.

Existing mutating `/api/actions/*` routes are legacy/admin operational actions. P2.9 did not inspect
or execute them as runtime actions; they are not duplicated by the convergence preview APIs.

## Risk

API duplication risk is LOW. The surface is broad, but it is organized under one execution preview
family and contract tests assert the public preview endpoints and single UI integration points.

api_duplication_risk=LOW
dangerous_parallel_api_systems_found=false
execution_engine_implemented=false
runtime_hooks_implemented=false
