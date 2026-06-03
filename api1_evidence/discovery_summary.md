# API.1 Discovery Summary

Scope: `admin/v7-admin-api` on branch `Updatesystem`.

Mode: read-only audit. No runtime files, governance behavior, routing, systemd, deployment, or user movement were changed.

## Inventory Source

Generated artifacts:

- `api1_evidence/endpoint_inventory.json`
- `api1_evidence/complete_endpoint_inventory.md`
- `api1_evidence/admin_api_static_map.json`
- `api1_evidence/endpoint_boundary_map.json`
- `api1_evidence/truth_source_map.json`
- `api1_evidence/largest_functions.json`

Static parser:

- `tools/v7-admin-endpoint-inventory`

## Current Size

| Source | Value |
|---|---:|
| `admin/v7-admin-api` lines | 36,468 |
| functions/classes detected | 657 |
| endpoint branches detected | 264 |
| GET endpoints | 118 |
| HEAD endpoints | 8 |
| POST endpoints | 138 |

## Endpoint Classification

| Category | Count |
|---|---:|
| Public endpoints | 19 |
| Auth-required endpoints | 245 |
| CSRF-required endpoints | 133 |
| Safe-mode blocked actions | 86 |
| Low-risk endpoints | 118 |
| Medium-risk endpoints | 38 |
| High-risk endpoints | 95 |
| Critical-risk endpoints | 13 |

## Boundary Summary

The static boundary classifier is intentionally conservative. POST/action endpoints are treated as potentially mutating unless the source block clearly proves otherwise.

| Boundary | Count |
|---|---:|
| READ | 62 |
| UI | 19 |
| ACTION | 130 |
| WRITE | 2 |
| EXECUTION | 38 |
| GOVERNANCE | 7 |
| ROLLBACK | 6 |

Derived flags:

| Flag | Count |
|---|---:|
| read-only | 78 |
| runtime mutation possible | 183 |
| execution authority possible | 39 |
| governance mutation possible | 10 |
| rollback authority possible | 6 |

## Largest Runtime Couplings

| Symbol | Start line | Lines | Owner |
|---|---:|---:|---|
| `html_page_v2` | 20067 | 12,370 | UI builder and embedded admin runtime |
| `Handler` | 32453 | 4,005 | HTTP routing, auth, endpoint dispatch |
| `egress_draft_runtime_run` | 7944 | 329 | egress draft/runtime preparation |
| `egress_channel_add_pipeline` | 8908 | 318 | egress provisioning pipeline |
| `egress_parse_proxy_share` | 5478 | 316 | proxy/import parser |
| `egress_config_preview` | 6715 | 270 | egress preview builder |
| `pending_profile_create` | 3401 | 213 | identity/profile creation |
| `connect_onboard` | 4223 | 183 | public onboarding |
| `smart_profile_validation` | 3075 | 179 | profile validation |
| `generated_proposals` | 18334 | 173 | proposal/read model |

## Critical Endpoint Paths

| Method | Path | Line | Role |
|---|---|---:|---|
| POST | `/api/actions/autoswitch-apply-guarded` | 35458 | admin |
| POST | `/api/actions/direct-domain-add` | 35301 | admin |
| POST | `/api/actions/direct-domain-remove` | 35320 | admin |
| POST | `/api/actions/egress-draft-enable-apply` | 35209 | admin |
| POST | `/api/actions/egress-set-state-apply` | 35264 | admin |
| POST | `/api/actions/policy-systemd-apply` | 36394 | admin |
| POST | `/api/actions/proxy-runtime-guard-apply` | 35985 | owner |
| POST | `/api/actions/proxy-runtime-guard-apply-preview` | 35962 | viewer |
| POST | `/api/actions/trusted-ru-decision` | 36318 | viewer |
| POST | `/api/actions/trusted-ru-diagnostic` | 36408 | operator |
| POST | `/api/actions/trusted-ru-readiness` | 36342 | viewer |
| POST | `/api/actions/trusted-ru-refresh-missing` | 36352 | operator |
| POST | `/api/actions/user-switch` | 34338 | operator |

## Key Finding

The admin API is not just a web API file. It is a combined operator console, embedded UI, auth/RBAC gate, preview builder set, state reader, state writer, runtime command launcher, governance surface, rollback surface, audit writer, closure writer, and public profile/onboarding delivery path.

Therefore the safe decomposition path must start with read-only, deterministic helpers and report/builders. Runtime action dispatch, auth/session gates, audit writers, closure writers, and handler routing must remain in place until contract tests and ownership boundaries are stronger.
