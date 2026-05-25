# V7 Web Scaffold

This is a Phase 6 non-production frontend scaffold.

It is not wired into the running admin platform yet.

Runtime admin remains:

- `admin/v7-admin-api`;
- `/admin-v2`;
- existing backend endpoints.

## Purpose

Prepare modular frontend structure without breaking the embedded admin.

## Safety Rules

- Do not bypass backend validation.
- Do not call dangerous actions without preview/confirm UX.
- Do not change endpoint contracts without migration notes.
- Keep `/admin-v2` as fallback until explicit migration.

