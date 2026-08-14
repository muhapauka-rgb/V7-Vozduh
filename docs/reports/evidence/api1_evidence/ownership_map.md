# API.1 Ownership Map

## Responsibility Owners

| Responsibility | Current owner | Truth source | Extraction class | Decision |
|---|---|---|---|---|
| HTTP router | `admin/v7-admin-api` `Handler` | endpoint branch logic | critical control plane | DO NOT TOUCH FIRST |
| Auth/session/RBAC | `admin/v7-admin-api` | `/etc/v7/admin/auth.json`, cookies, role maps | security boundary | DO NOT TOUCH FIRST |
| Safe mode | `admin/v7-admin-api` | `/etc/v7/admin/safe-mode.json` | safety boundary | DO NOT TOUCH FIRST |
| Admin UI | `html_page_v2` in `admin/v7-admin-api` | embedded HTML/CSS/JS | presentation/control coupling | REFRACTOR LATE |
| Runtime action execution | `run_action` in `admin/v7-admin-api` plus runtime tools | runtime-support tools and `/opt`/`/etc` state | mutation boundary | DO NOT TOUCH FIRST |
| Read-only commands | `run_readonly` in `admin/v7-admin-api` | system/runtime diagnostics | diagnostic boundary | WRAP LATER |
| Audit writing | `audit_admin` in `admin/v7-admin-api` and runtime audit tool | `/opt/v7/audit/audit.jsonl` | accountability boundary | DO NOT TOUCH FIRST |
| Audit reading/search | `admin_core/operator_observability.py` plus admin wrappers | audit/events/evidence files | read-only view | EXTEND |
| Closure writing | `admin/v7-admin-api` closure functions | closure store file | governance/accountability boundary | DO NOT TOUCH FIRST |
| Closure reading | admin closure helpers and observability views | closure store file | read-only view | EXTEND |
| Operator execution packet model | `admin_core/operator_execution.py` | packet/event stores | canonical governance model | REUSE |
| Governance preview | admin API + `admin_core/operator_execution.py`/observability | packet/event/audit stores | preview-only view | EXTEND READ-ONLY |
| Rollback preview | admin API + runtime-support tools | rollback plan/output stores | preview/action mixed | PREVIEW ONLY FIRST |
| Rollback apply | admin action endpoints and runtime tools | runtime backups/state | mutation boundary | DO NOT TOUCH FIRST |
| Registry readers | `admin_core/registry_readers.py` and admin wrapper | users/egress registries | parser/view | EXTEND |
| Overview summary | `overview`, `overview_cached`, `overview_for_session` | many runtime/admin stores | heavy read model | EXTRACT CAREFULLY |
| Service matrix | admin helpers + service matrix tools | `/opt/v7/egress/state/service-matrix.json` | read/cache model | EXTEND READ-ONLY |
| Routing intelligence | `admin_core/routing_brain.py`, `admin_core/routing_intelligence.py`, planner tool | RI snapshots/planner evidence | advisory model | REUSE |
| Planner/autoswitch | `tools/v7-users-autoswitch` | runtime registries, policy, RI advisory | planner authority | DO NOT TOUCH IN API.2 |
| Identity/onboarding | admin API identity helpers | identity DB, profile tokens, registries | access lifecycle | READ-ONLY FIRST ONLY |
| Egress draft/import | admin API egress helpers | drafts, tests, runtime config dirs | preview/apply mixed | PARSERS FIRST ONLY |
| Policy/direct/trusted RU | admin API policy helpers/actions | policy files, direct domains, trusted RU states | route policy authority | READ-ONLY FIRST ONLY |

## Owner Groups In Generated Boundary Map

| Purpose owner | Endpoint count |
|---|---:|
| `admin_api_misc` | 57 |
| `admin_ui_public_delivery` | 13 |
| `audit_events_logs` | 5 |
| `auth_admin_settings` | 11 |
| `egress_draft_and_pool` | 25 |
| `identity_onboarding` | 25 |
| `operator_governance_execution` | 36 |
| `overview_diagnostics` | 6 |
| `planner_autoswitch_candidate_workflow` | 13 |
| `policy_routing_direct_trusted_ru` | 24 |
| `proxy_runtime_preview` | 20 |
| `runtime_tool_action` | 29 |

## Ownership Rule For API.2

API.2 should create modules only where ownership is already clear and read-only:

- `admin_core` read models;
- deterministic serializers;
- pure parser adapters;
- no new stores;
- no runtime command execution;
- no action routing changes.

The monolith remains the owning shell for auth, routing, mutation, audit writes, closure writes, and UI until those contracts are separately frozen.
