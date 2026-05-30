# P1.A Admin Surface

evidence_admin_surface_defined=true

## Placement Rule

Evidence integrates into the existing V7 Admin navigation. No new top-level navigation item is introduced.

Evidence appears through:

- inline evidence chips;
- "Open evidence" drawer actions;
- timeline summaries;
- linked log/check/proposal/recovery records;
- advanced detail sections.

## Existing Navigation Mapping

| Admin section | Evidence operator meaning | Visible surface | Drawer entry |
| --- | --- | --- | --- |
| `Главная` | What needs attention first and why. | Alert rows, status cards, topology issues. | Open bundle from alert/status item. |
| `Проверки` | What was checked and whether it passed. | Check result rows, readiness map, blocked gates. | Evidence timeline for check run. |
| `Логи` | What happened and how it links to proof. | Event rows with bundle links. | Evidence bundle for event chain. |
| `Пользователи` | Why a user has an issue or recommendation. | User row issue/next-action, required-service mismatch. | User evidence bundle drawer. |
| `Каналы` | Why a channel is suitable, degraded or blocked. | Channel readiness, service matrix, speed/quality. | Channel evidence bundle drawer. |
| `Маршруты` | Why traffic should or should not move. | Route checks, service-aware routing, route reality. | Route/proposal evidence bundle drawer. |

## What Operator Sees

The operator sees:

- concise bundle summary;
- status and severity;
- affected object;
- current diagnosis;
- recommended next safe action;
- verification state;
- closure state;
- link to full evidence drawer.

## What Stays Hidden By Default

The first view hides:

- raw command output;
- raw JSON;
- secrets and credentials;
- verbose probe logs;
- low-level stack traces.

These remain available only in advanced details when role and redaction rules allow it.

## Drawer Behavior

Evidence opens in a right-side drawer from the existing workflow. The drawer should not force the operator into a separate page during normal investigation.

The drawer must support:

- summary;
- timeline;
- evidence item list;
- recommendation;
- verification;
- closure;
- advanced details.

## Admin Surface Verdict

Evidence is a cross-cutting detail and proof layer inside existing admin sections, not a new workspace or top-level section.

