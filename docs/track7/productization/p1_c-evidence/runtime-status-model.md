# P1.C Runtime Status Model

runtime_status_model_defined=true

## Statuses

| Status | Meaning | Operator action | Visibility |
| --- | --- | --- | --- |
| `RUNTIME_OK` | Runtime matches expected release and verification is fresh. | Continue normal review and governed actions. | Green/ok status on `Главная`, `Проверки`, `Безопасность`. |
| `RUNTIME_WARNING` | Minor or non-blocking concern exists, such as soon-stale validation or low-severity drift. | Inspect drawer and refresh verification if needed. | Warn status with next safe action. |
| `RUNTIME_DRIFT` | Runtime differs from expected release or lineage. Impact must be assessed. | Inspect drift, run verification, avoid forward movement until classified. | Warn or bad depending on severity. |
| `RUNTIME_UNKNOWN` | Runtime trust cannot be determined because evidence is missing or stale. | Refresh checks or collect evidence. | Muted/warn; forward movement denied. |
| `RUNTIME_BLOCKING` | Drift or inconsistency is safety-critical. | Stop forward actions, use containment/rollback/recovery path. | Bad status and blocking banner. |

## Status Rules

`RUNTIME_OK` requires:

- release match;
- fresh convergence verification;
- no blocking drift;
- runtime checkers OK;
- evidence available.

`RUNTIME_UNKNOWN`, `RUNTIME_DRIFT` and `RUNTIME_BLOCKING` must fail closed for forward governed movement.

Rollback and containment remain allowed when they reduce risk.

## Operator Copy

Use simple status language:

- "System matches release";
- "Runtime verification is getting stale";
- "System drift detected";
- "Runtime trust unknown";
- "Runtime blocked: inspect before action".

## Status Verdict

Runtime status model converts fingerprint and lineage facts into operator-safe trust states.
