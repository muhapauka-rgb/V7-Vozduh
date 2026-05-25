# V7 Phase 6 Report

## Scope

Phase 6 inspected the current admin platform and added a safe migration foundation.

No runtime behavior, routing behavior, nftables behavior, provisioning behavior, systemd units, admin endpoint behavior, or embedded admin rendering was changed.

## Current Strengths

The current admin already contains important platform-grade foundations:

- `/admin-v2` operator UI;
- `/connect` user onboarding surface;
- public gateway allowlist;
- RBAC via `ACTION_MIN_ROLE` and `GET_MIN_ROLE`;
- CSRF checks for mutating actions;
- safe-mode blocked actions;
- explicit confirm tokens;
- overview cache and live refresh;
- drawers and workspace tabs for progressive disclosure;
- user readiness, identity, routing, diagnostics, security, settings, logs.

## Main Bottlenecks

### Embedded monolith

`admin/v7-admin-api` contains backend, API routing, HTML, CSS, and JavaScript in one runtime-critical file.

### Frontend coupling

Frontend rendering depends directly on backend JSON shapes and global `overview` state.

### Dense UI growth risk

The admin already tries to preserve calm UX, but large tables, many workspace tabs, and long embedded render functions can become harder to reason about as users/egress/incidents grow.

### Extraction risk

Moving code directly out of the monolith without contracts would risk breaking endpoint compatibility.

## Added Artifacts

- `ADMIN_PLATFORM_ARCHITECTURE.md`
- `BACKEND_MODULE_BOUNDARIES.md`
- `FRONTEND_ARCHITECTURE.md`
- `CALM_OPERATOR_UX.md`
- `OVERVIEW_FIRST_UX.md`
- `WORKFLOW_NAVIGATION.md`
- `PROGRESSIVE_DISCLOSURE.md`
- `SAFE_ACTION_UX.md`
- `DIAGNOSTICS_INCIDENT_UX.md`
- `ROUTING_VISUALIZATION.md`
- `OPERATOR_USER_UX_SEPARATION.md`
- `MOBILE_OPERATOR_UX.md`
- `DESIGN_SYSTEM_FOUNDATION.md`
- `LEGACY_MIGRATION_STRATEGY.md`
- `PERFORMANCE_SCALABILITY_UX.md`
- `FUTURE_OPERATOR_FOUNDATION.md`

## Added Frontend Scaffold

`web/src` now contains a non-production modular scaffold:

- `app`;
- `pages`;
- `components`;
- `layouts`;
- `api`;
- `hooks`;
- `stores`;
- `styles`;
- `utils`.

This scaffold is not wired into runtime.

## Added Tool

`tools/v7-admin-platform-review` is a read-only static review helper.

It reports:

- admin monolith size;
- embedded UI markers;
- endpoint/action counts;
- safe-mode and RBAC coverage;
- frontend scaffold presence;
- extraction risk notes.

## Static Review Result

Local static review reported:

- monolith size: `30067` lines;
- action handlers: `132`;
- `ACTION_MIN_ROLE` entries: `132`;
- action handlers missing role mapping: `0`;
- likely preview/read-only safe-mode exceptions: `43`;
- action handlers needing safe-mode classification review: `3`.

The three endpoints flagged for future review are:

- `/api/actions/egress-draft-clash-create-proxy-draft`;
- `/api/actions/egress-draft-endpoint-create-managed-draft`;
- `/api/actions/egress-draft-post-enable-validation`.

No endpoint behavior was changed in Phase 6.

## Phase Boundary

Phase 6 did not start Phase 7.

Scaling, disaster recovery, infrastructure reliability, and production frontend replacement remain out of scope until a separate command.
