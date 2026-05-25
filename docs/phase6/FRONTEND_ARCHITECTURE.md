# V7 Phase 6 Frontend Architecture

## Purpose

The new frontend architecture must support a calm operator platform without forcing an immediate production migration.

## Scaffold

Initial structure:

```text
web/
  src/
    app/
    pages/
    components/
    layouts/
    api/
    hooks/
    stores/
    styles/
    utils/
```

## Responsibilities

app:

- app shell;
- route registration;
- bootstrap and feature flags.

pages:

- workflow-oriented screens.

components:

- reusable operator components.

layouts:

- app frame, detail drawer, workspace layout.

api:

- typed wrappers around existing backend endpoints.

hooks:

- polling, refresh, command state.

stores:

- UI state and cached overview data.

styles:

- design tokens and semantic status classes.

utils:

- formatting, severity mapping, endpoint helpers.

## Runtime Rule

The frontend must not directly mutate routing state.

All critical actions must go through existing backend validation, RBAC, CSRF, audit, preview, and confirmation flows.

## Compatibility Rule

The scaffold is not production-connected until explicitly wired behind a separate feature flag or path.

Existing `/admin-v2` remains the operational fallback.

