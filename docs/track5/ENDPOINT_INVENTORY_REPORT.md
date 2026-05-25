# V7 Track 5.1 - Endpoint Inventory Report

Generated: 2026-05-23

Scope: freeze the current admin API endpoint surface before any monolith extraction.

No admin endpoint logic was changed.

## Files Created

- `docs/track5/endpoint-inventory.json`
- `docs/track5/ENDPOINT_INVENTORY_REPORT.md`
- `tools/v7-admin-endpoint-inventory`
- `tests/contracts/endpoint_inventory_test.py`
- `tests/contracts/fixtures/health.json`
- `tests/contracts/fixtures/session_unauthenticated.json`
- `tests/contracts/fixtures/overview_schema.json`
- `tests/contracts/fixtures/events_schema.json`
- `tests/contracts/fixtures/diagnostics_schema.json`

## Inventory Summary

Static inventory source:

```text
admin/v7-admin-api
```

Source line count:

```text
30067
```

Endpoint branches detected:

```text
192
```

This count is slightly higher than the Track 5 rough count because Track 5.1 includes HEAD routes, tuple branches, prefix routes, and public delivery/API prefixes in one machine-readable inventory.

## Counts By Method

| Method | Count |
|---|---:|
| GET | 47 |
| HEAD | 8 |
| POST | 137 |

## Counts By Auth

| Auth | Count |
|---|---:|
| public | 19 |
| required | 173 |

## Counts By Risk

| Risk | Count |
|---|---:|
| low | 47 |
| medium | 37 |
| high | 95 |
| critical | 13 |

## Counts By Family

| Family | Count |
|---|---:|
| action | 132 |
| read_api | 38 |
| page | 14 |
| public_delivery | 5 |
| public_api | 3 |

## Guard Counts

| Guard | Count |
|---|---:|
| CSRF-required endpoints | 132 |
| Safe-mode blocked actions | 86 |

## Read-Only Contract Foundation

Initial contract fixtures cover:

| Endpoint | Auth | Expected Unauthenticated Behavior | Authenticated Shape |
|---|---|---|---|
| `/health` | public | `200` JSON | `status`, `updated`, `local_only`, `auth_configured` |
| `/api/session` | required | `401 {"error":"unauthorized"}` | `user`, `role`, `csrf`, `expires_at`, `access` |
| `/api/overview` | required | `401 {"error":"unauthorized"}` | broad overview keys including `summary`, `registries`, `service_matrix`, `checks`, `events` |
| `/api/events` | required | `401 {"error":"unauthorized"}` | `items`, `filters`, `source` |
| `/api/diagnostics` | required | `401 {"error":"unauthorized"}` | `system_check`, `route_check`, `killswitch`, `direct_routing`, `stale` |

The fixtures are schema/contract specs. They do not bypass auth or store live credentials.

## Auth Behavior Captured

Captured in inventory:

- public vs required auth;
- role requirement for action endpoints;
- GET role overrides from `GET_MIN_ROLE`;
- CSRF requirement for action endpoints;
- safe-mode blocking status;
- unauthenticated behavior for initial read-only fixture set.

Important:

Authenticated live snapshot tests are still needed before extracting anything beyond pure helpers.

## Response-Shape Freeze Status

Frozen now:

- top-level keys for the first read-only contract set;
- unauthenticated status expectations;
- content/response type expectations;
- dangerous action guard expectations for selected critical POST endpoints.

Not yet frozen:

- full nested schemas;
- every `/api/actions/*` response shape;
- authenticated live payload samples;
- redaction snapshots;
- binary/file endpoint contracts;
- profile delivery token behavior.

## Contract Test Coverage

Created:

```text
tests/contracts/endpoint_inventory_test.py
```

Current tests:

1. `admin/v7-admin-api` compiles.
2. `endpoint-inventory.json` has expected shape and counts.
3. Mandatory read-only endpoints are present and classified.
4. Fixture specs match inventory.
5. Selected dangerous POST endpoints require auth + CSRF + role.

Selected dangerous POST endpoints checked:

- `/api/actions/user-switch`
- `/api/actions/autoswitch-apply-guarded`
- `/api/actions/egress-draft-enable-apply`
- `/api/actions/policy-domain-add`

## Verification

Local verification:

```text
python3 tools/v7-admin-endpoint-inventory --admin admin/v7-admin-api --out docs/track5/endpoint-inventory.json
python3 -m unittest tests.contracts.endpoint_inventory_test
```

Result:

```text
Ran 5 tests in 0.133s
OK
```

Runtime verification:

No production runtime files were changed in Track 5.1. Live VPS safety checks were not required for this local-only contract/test foundation. The mandatory runtime check set remains the deployment gate before any future extraction is deployed.

## Gaps Before Extraction

Before extracting anything state-coupled:

- add live or local server smoke tests for authenticated read-only endpoints;
- capture nested schemas for `/api/overview`;
- add redaction assertions for token/config-bearing responses;
- add fixtures for preview endpoints:
  - `/api/actions/autoswitch-dry-run`;
  - `/api/actions/egress-draft-enable-preview`;
  - `/api/actions/egress-set-state-preview`;
  - `/api/actions/policy-route-preview`;
- add no-mutation contract tests for preview endpoints;
- map shell commands per endpoint more strictly than static best-effort.

## Extraction Readiness Gate

`admin_core.sanitize` and `admin_core.time`:

```text
conditionally ready for first tiny extraction
```

Conditions:

- keep old imports compatible;
- move only pure helpers;
- run contract tests before/after;
- run `py_compile`;
- do not move state IO, registry parsing, shell wrappers, auth, Handler, routing, direct/RU, autoswitch, provisioning, or profile delivery.

Everything beyond pure helpers:

```text
not ready
```

Reason:

Endpoint contracts are now started, not complete.

