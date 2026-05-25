# V7 Phase 0 Admin API Split Plan

Purpose: describe future module boundaries for `admin/v7-admin-api` without splitting it now.

## Current State

`admin/v7-admin-api` is a single Python executable of about 30067 lines. It contains configuration, auth, state helpers, identity DB, egress lifecycle, routing policy, diagnostics, embedded UI, and HTTP routing.

Phase 0 must not split it. The current file is runtime-critical.

## Proposed Future Modules

### `auth`

Would own:

- admin accounts;
- password hashing;
- sessions;
- login throttling;
- CSRF;
- RBAC.

Current approximate range: helpers and auth around lines 722-1206 plus route guards in `Handler`.

### `state`

Would own:

- atomic JSON/text IO;
- registry parsing;
- safe validators;
- path helpers;
- redaction.

Current approximate range: lines 722-1756 and scattered helper use.

### `identity`

Would own:

- `IDENTITY_SCHEMA`;
- SQLite migrations;
- users/groups/organizations/devices;
- allowed phone flows;
- connect sessions;
- pending profiles.

Current approximate range: lines 1757-4389.

### `egress`

Would own:

- config preview/parsing;
- OpenVPN/Clash/Xray/Outline/subscription parsers;
- draft lifecycle;
- preflight/runtime/provision;
- egress deletion/pause/migration.

Current approximate ranges: lines 4392-9360 and 13984-14535.

### `policy`

Would own:

- platform policy;
- org egress policy;
- route classes;
- service-aware routing;
- direct/RU domain policy;
- trusted RU state.

Current approximate ranges: lines 11146-12142 and 14538-15032.

### `diagnostics`

Would own:

- system checks;
- route checks;
- killswitch summaries;
- service matrix views;
- traffic/speed states;
- readiness maps.

Current approximate ranges: lines 9363-11397 and 12145-13981.

### `autoswitch`

Would own:

- autoswitch plan/dry-run/apply API wrappers;
- autoswitch explanation adaptation for UI;
- safety summaries.

Current approximate range: lines 11235-11272 plus UI render sections.

### `audit`

Would own:

- admin audit;
- normalized events;
- security audit;
- CSV export.

Current approximate range: lines 10533-10791.

### `ui`

Would own:

- login/connect pages;
- admin v2 HTML/CSS/JS;
- UI data transformation.

Current approximate range: lines 15253-26475.

### `routing`

Would own:

- route status;
- direct routing checks;
- user route readiness;
- route-class decisions.

This must remain deterministic and policy-driven.

## Extraction Order

Recommended order, once Phase 0 is complete:

1. Pure helpers: redaction, IO, registry parsing, validators.
2. Audit/event normalization.
3. Read-only state builders.
4. Auth/RBAC with compatibility tests.
5. Identity DB layer.
6. Egress parser functions with regression tests.
7. Egress lifecycle actions.
8. Embedded UI extraction.
9. Handler route table split.

## Coupling Risks

- Many functions rely on globals such as `STATE_DIR`, `POLICY_FILE`, `SERVICE_MATRIX_FILE`.
- Handler directly calls functions instead of a route registry.
- UI JavaScript expects specific JSON shapes.
- External `/usr/local/bin/v7-*` commands are not fully represented in repo.
- State defaults can mask missing contracts.

## Split Guardrails

- No behavior change during extraction.
- Keep executable compatibility path.
- Add contract tests before moving state writers.
- Maintain all endpoint paths.
- Keep redaction behavior identical.
- Never alter datapath as part of code organization.

