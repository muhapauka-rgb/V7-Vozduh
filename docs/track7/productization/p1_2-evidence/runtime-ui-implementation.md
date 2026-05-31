# P1.2 Runtime Trust UI Implementation

runtime_ui_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: show whether runtime is trustworthy
Operator Meaning: system matches release, drift, unknown, blocking
Admin Surface: Главная, Проверки, Безопасность
Runtime Service: Runtime Trust API read calls
Storage: Runtime Convergence Store
API: GET /api/runtime/*
UI Component: RuntimeTrustStatus, RuntimeTrustDrawer, DriftComponent, VerificationHistoryView
```

## Components

### RuntimeTrustStatus

Compact status component for page summaries.

Shows:

- status pill;
- release match;
- drift count;
- verification age;
- recommended action label.

### RuntimeTrustDrawer

Shared drawer.

Sections:

- status;
- summary;
- drift;
- verification history;
- evidence link;
- recommended action;
- advanced details.

### DriftComponent

Reusable drift list/summary.

Shows:

- drift type;
- severity;
- impact;
- detected time;
- action.

### VerificationHistoryView

Timeline/table for convergence checks.

Shows:

- timestamp;
- source;
- result;
- release ref;
- evidence link.

## Exact Admin Placement

| Section | Placement |
| --- | --- |
| `Главная` | Top system/status strip and alert list. |
| `Проверки` | Runtime convergence check result row and readiness map detail. |
| `Безопасность` | Security overview trust panel near backup/rollback/safe mode. |

## UI Data Flow

```text
render section
-> GET /api/runtime/convergence
-> render RuntimeTrustStatus
-> open RuntimeTrustDrawer
-> GET /api/runtime/convergence?include_history=1&include_drift=1
-> GET /api/runtime/drift if drawer needs full list
```

## Visual Rules

- Use existing `pill` semantics.
- `RUNTIME_OK` uses ok.
- `RUNTIME_WARNING` uses warn.
- `RUNTIME_DRIFT` uses warn/bad depending severity.
- `RUNTIME_UNKNOWN` uses muted/warn.
- `RUNTIME_BLOCKING` uses bad.
- Raw fingerprint details only in advanced section.

## Implementation Completeness

Runtime UI implementation is defined for current `/admin-v2`.
