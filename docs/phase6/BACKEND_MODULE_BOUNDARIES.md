# V7 Phase 6 Backend Module Boundaries

## Purpose

Backend modularization must reduce coupling without creating runtime risk.

## Recommended Extraction Order

1. Pure state helpers:
   - redaction;
   - atomic read/write;
   - registry parsing;
   - path validation.
2. Audit/event normalization.
3. Read-only state builders.
4. Auth and RBAC.
5. Identity DB layer.
6. Egress parser and draft helpers.
7. Egress lifecycle actions.
8. Autoswitch API wrappers.
9. Embedded UI extraction.
10. Handler route table split.

## Module Contracts

auth:

- owns admin accounts, sessions, CSRF, role checks.

state:

- owns safe file/JSON/registry IO and redaction.

identity:

- owns SQLite schema, organizations, users, devices, onboarding, pending profiles.

provisioning:

- owns draft import, preflight, runtime provision, quarantine, staged enable.

routing:

- owns route status, route classes, direct/RU checks, user route readiness.

diagnostics:

- owns service matrix, health summaries, incident diagnostics.

autoswitch:

- owns plan/dry-run/apply wrappers and explanation shaping.

policy:

- owns platform policy, org policy, route-class policy, service preferences.

audit:

- owns admin events, switch history adapters, security audit export.

profile delivery:

- owns one-time delivery tokens, public QR/import/download views.

## Guardrails

Do not extract a writer before:

- its state contract is documented;
- existing endpoint response shape is covered;
- rollback/fallback exists;
- dangerous actions remain role-checked and audited.

