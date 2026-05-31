# P1.2 Release Trust UI Implementation

release_ui_implementation_defined=true

## Reality-First Mapping

```text
Product Capability: show current release, certification and rollback availability
Operator Meaning: release certified, rollback available, matches runtime, or attention required
Admin Surface: Главная, Проверки, Безопасность
Runtime Service: Release Trust API read calls
Storage: Release Trust Store
API: GET /api/release/*
UI Component: ReleaseTrustStatus, ReleaseDrawer, ReleaseHistory, RollbackAvailability
```

## Components

### ReleaseTrustStatus

Compact status component.

Shows:

- release label;
- release status pill;
- certified flag;
- runtime match;
- rollback availability;
- verification age.

### ReleaseDrawer

Shared drawer.

Sections:

- current release;
- status;
- certification;
- rollback availability;
- verification history;
- runtime convergence link;
- evidence link;
- recommended action;
- advanced details.

### ReleaseHistory

Timeline/table component.

Shows:

- release id/label;
- event type;
- timestamp;
- verification result;
- rollback target;
- evidence link.

### RollbackAvailability

Small component for security/release surfaces.

Shows:

- available/unknown/blocked/expired;
- rollback target;
- backup/restore ref;
- verification state.

## Exact Admin Placement

| Section | Placement |
| --- | --- |
| `Главная` | System status strip near runtime trust. |
| `Проверки` | Release verification check rows and detail drawer. |
| `Безопасность` | Release/rollback panel near backups and rollback controls. |

## UI Data Flow

```text
render section
-> GET /api/release/current?include_runtime=1&include_rollback=1
-> render ReleaseTrustStatus
-> open ReleaseDrawer
-> GET /api/release/{release_id}
-> optionally open RuntimeTrustDrawer or EvidenceDrawer
```

## Visual Rules

- `RELEASE_OK` uses ok.
- `RELEASE_WARNING` uses warn.
- `RELEASE_UNKNOWN` uses muted/warn.
- `RELEASE_DRIFT` uses warn/bad depending impact.
- `RELEASE_BLOCKING` uses bad.
- Raw hashes/manifests/signatures only in advanced details.

## Implementation Completeness

Release UI implementation is defined for current `/admin-v2`.
