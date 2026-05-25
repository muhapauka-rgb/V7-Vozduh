# V7 Track 5 - Endpoint Contract Freeze Plan

Purpose: freeze admin API behavior before any module extraction.

No endpoint schema was changed in Track 5.

## Observed Endpoint Surface

Static route scan found approximately:

```text
186 route branches
```

Major groups:

- public pages:
  - `/`
  - `/login`
  - `/connect`
  - `/health`
  - `/admin-v2`
- profile/public delivery:
  - `/profile-delivery/*`
  - `/profile-import/*`
  - `/speed-test/*`
  - `/api/public-speed-sample/*`
- read-only admin APIs:
  - `/api/session`
  - `/api/overview`
  - `/api/state`
  - `/api/users`
  - `/api/egress`
  - `/api/diagnostics`
  - `/api/killswitch`
  - `/api/direct-routing`
  - `/api/events`
  - `/api/policy`
  - `/api/org-egress-policy`
  - `/api/autoswitch-plan`
- identity/profile APIs:
  - `/api/identity`
  - `/api/profile-delivery-status`
  - `/api/client-artifact`
  - `/api/smart-client-profile`
  - `/api/client-profile-capabilities`
- action APIs:
  - `/api/actions/*`

## Contract Fields To Freeze

For every endpoint:

| Field | Must Capture |
|---|---|
| method | GET/POST/HEAD |
| path | exact path or prefix |
| auth required | public/viewer/operator/admin/owner |
| CSRF required | yes/no |
| safe mode behavior | allowed/blocked |
| request schema | required fields, optional fields, confirmation token |
| response schema | top-level keys and nested object names |
| error semantics | status code and `error` string |
| redaction | secret/token/config handling |
| state files read | paths/classes |
| state files written | paths/classes |
| shell commands | exact `v7-*` dependencies |
| audit event | actor/action/object/result |
| rollback context | required/not required |

## Compatibility Constraints

Extraction must not silently change:

- endpoint paths;
- HTTP methods;
- auth roles;
- CSRF requirement;
- confirmation tokens;
- status codes;
- top-level JSON keys;
- redaction behavior;
- audit behavior;
- shell command arguments;
- state file paths.

## Critical Endpoint Families

### Routing/User Mutation

Examples:

- `/api/actions/user-switch`
- `/api/actions/user-reconcile-apply`
- `/api/actions/user-disable`
- `/api/actions/user-enable`
- `/api/actions/user-rotate-key`

Freeze requirements:

- role;
- confirmation behavior;
- before/after user state;
- expected `overview` inclusion;
- route safety verification expectations.

### Autoswitch

Examples:

- `/api/autoswitch-plan`
- `/api/actions/autoswitch-dry-run`
- `/api/actions/autoswitch-apply-guarded`

Freeze requirements:

- dry-run never mutates;
- apply requires `AUTOSWITCH`;
- anti-flap and policy semantics stay authoritative;
- response includes explanation/summary.

### Provisioning/Egress Lifecycle

Examples:

- `/api/actions/egress-draft-preflight-run`
- `/api/actions/egress-draft-runtime-run`
- `/api/actions/egress-draft-quarantine-run`
- `/api/actions/egress-draft-enable-apply`
- `/api/actions/egress-set-state-apply`

Freeze requirements:

- confirm tokens;
- draft lifecycle state;
- no production enable without explicit apply;
- rollback/error shape.

### Policy/Direct/RU

Examples:

- `/api/actions/direct-domain-add`
- `/api/actions/direct-refresh`
- `/api/actions/policy-domain-add`
- `/api/actions/policy-sync-direct-excludes`
- `/api/actions/trusted-ru-diagnostic`

Freeze requirements:

- route class semantics;
- confirmation token;
- domain validation;
- no hidden fallback behavior.

### Identity/Profile Delivery

Examples:

- `/api/connect/start`
- `/api/actions/identity-device-issue`
- `/api/actions/profile-delivery-create`
- `/api/actions/profile-delivery-revoke`

Freeze requirements:

- token redaction;
- delivery TTL behavior;
- DB path;
- public URL shape;
- no stale/revoked profile exposure.

## Freeze Implementation Plan

1. Create endpoint inventory JSON from current monolith.
2. Add snapshot fixtures for selected critical endpoints.
3. Add schema assertions:
   - top-level keys;
   - error key;
   - confirmation error strings.
4. Add smoke tests against local admin API in read-only mode.
5. Only then extract a `SAFE_READ_ONLY` helper module.

## First Contract Test Targets

Low-risk:

- `/health`
- `/api/session`
- `/api/overview`
- `/api/events`
- `/api/diagnostics`

High-value safety:

- `/api/actions/autoswitch-dry-run`
- `/api/actions/egress-draft-enable-preview`
- `/api/actions/egress-set-state-preview`
- `/api/actions/policy-route-preview`

Do not test apply endpoints by mutating production. For apply endpoints, freeze request/confirmation/error schemas first.

