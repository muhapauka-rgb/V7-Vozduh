# P1.D/E Release Status Model

release_status_model_defined=true

## Statuses

| Status | Meaning | Operator action | Visibility |
| --- | --- | --- | --- |
| `RELEASE_OK` | Current release is known, certified, rollback-aware and runtime matches it. | Continue normal governed workflow. | OK status on `Главная`, `Проверки`, `Безопасность`. |
| `RELEASE_WARNING` | Release is known but verification is near-stale or has non-blocking concerns. | Inspect drawer and refresh verification if needed. | Warn status. |
| `RELEASE_UNKNOWN` | Release identity, certification or rollback lineage is missing. | Inspect, verify release, avoid risky forward action. | Muted/warn with blocker reason. |
| `RELEASE_DRIFT` | Runtime or expected state does not match the release/provenance chain. | Inspect runtime convergence and release lineage. | Warn/bad depending on impact. |
| `RELEASE_BLOCKING` | Release trust failure blocks forward governance. | Stop forward action; use containment/recovery path. | Bad blocking banner. |

## Status Rules

`RELEASE_OK` requires:

- current release known;
- release certification valid;
- rollback lineage known or explicitly not required for this context;
- runtime convergence acceptable;
- verification fresh;
- evidence available.

`RELEASE_UNKNOWN`, `RELEASE_DRIFT` and `RELEASE_BLOCKING` must fail closed for forward movement when release trust is required.

Rollback and containment remain allowed when they reduce risk.

## Operator Copy

Use simple phrases:

- "Current release certified";
- "Rollback available";
- "Release matches runtime";
- "Release trust unknown";
- "Release drift detected";
- "Release blocked: inspect before action".

## Status Verdict

Release status model converts provenance and rollback details into operator-safe trust states.
