# P1.1 Evidence UI Implementation

evidence_ui_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: make proof visible in context
Admin Surface: existing Главная, Пользователи, Каналы, Маршруты, Проверки, Безопасность, Логи
Runtime Service: Evidence API read calls
Storage: Evidence Store
API: GET /api/evidence*
UI Component: EvidenceChip, EvidenceDrawer, EvidenceTimeline, EvidenceSummary
```

## Components

### EvidenceChip

Compact row/table indicator.

Props:

- `bundleId`;
- `status`;
- `severity`;
- `label`;
- `count`;
- `objectType`;
- `objectId`.

Behavior:

- click opens Evidence Drawer;
- uses existing `.pill.ok/.warn/.bad/.info/.muted`;
- no mutation actions.

### EvidenceSummary

Small panel/card inside section summaries.

Shows:

- title;
- severity;
- operator meaning;
- diagnosis;
- updated time;
- next safe action label.

### EvidenceTimeline

Drawer section.

Shows:

- detected;
- checked;
- diagnosed;
- recommended;
- verified;
- closed.

### EvidenceDrawer

Shared drawer using existing `/admin-v2` drawer patterns.

Sections:

- summary;
- timeline;
- evidence items;
- recommendation;
- verification;
- closure;
- advanced details.

## Exact Admin Placement

| Section | Placement |
| --- | --- |
| `Главная` | Alert rows and status cards show EvidenceChip; drawer opens from alert/status detail. |
| `Пользователи` | User row issue/next-action column and user drawer show evidence chips by user IP. |
| `Каналы` | Channel table status/readiness/service cells show evidence by channel id. |
| `Маршруты` | Route check and service-aware preview panels show route evidence. |
| `Проверки` | Check result rows use evidence as primary detail drawer. |
| `Безопасность` | Backup/restore/safe-mode panels link to evidence. |
| `Логи` | Log event drawer links related evidence bundles. |

## UI Data Flow

```text
render table/card
-> call /api/evidence/by-object/{type}/{id} lazily
-> show chip count/status
-> open drawer
-> call /api/evidence/{bundle_id}
```

## Visual Rules

- Use existing drawer, pill, panel and table-shell styling.
- Do not create a new top-level page.
- Raw JSON only in advanced details.
- Secrets remain redacted.

## Implementation Completeness

UI plan is implementation-ready for the embedded `/admin-v2` admin. The future `web/` scaffold can reuse the component contract later.
