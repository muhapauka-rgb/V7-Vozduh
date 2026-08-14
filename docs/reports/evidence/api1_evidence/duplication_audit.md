# API.1 Duplication Audit

Search terms covered the prompt-required areas: duplicate APIs, endpoint ownership, truth sources, registry readers, execution paths, rollback paths, governance paths, audit writers, closure writers, service readers, and routing intelligence readers.

## Duplicate Or Overlapping Registry Readers

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin_core/registry_readers.py` | Canonical `parse_registry_lines` and key/value parsing | REUSE | This should remain the shared parser contract. |
| `admin/v7-admin-api:1257` | `parse_registry(path)` wrapper over `parse_registry_lines`, with redaction | EXTEND | Safe early candidate only as a read-only admin view wrapper. |
| `admin_core/operator_observability.py` | Uses `parse_registry_lines` for observability snapshots | REUSE | Keep as read-only observability owner. |
| `tools/v7-users-autoswitch` | Local registry parser inside planner/runtime tool | DO NOT TOUCH | Runtime planner semantics should not be changed in API.1/API.2 extraction. |
| `tools/v7-route-movement-preview` | Local dry-run registry parser | DO NOT TOUCH | Tool-local parser may be consolidated later under separate runtime-tool certification. |
| `tools/v7-service-matrix-refresh-all` | Local egress parser | DO NOT TOUCH | Background/refresh tool ownership, not admin API extraction. |
| `tools/runtime-support/v7-proxy-*` | Local runtime-support parsers | DO NOT TOUCH | Runtime-support tools must not be modified as part of admin decomposition. |

Decision: registry parsing is duplicated, but not dangerously parallel inside the admin API. The first safe move is to centralize read-only admin registry view construction around `admin_core.registry_readers`, without changing runtime tools.

## Audit Writer Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin/v7-admin-api:10565` | `audit_admin` writes admin action audit records | DO NOT TOUCH | Mutation/audit authority; not a first extraction target. |
| `tools/runtime-support/v7-audit-log` | Runtime audit writer | REUSE | Runtime audit authority remains separate. |
| `tools/v7-users-autoswitch` | Emits runtime audit references and closure target metadata | DO NOT TOUCH | Planner/runtime output contract should stay fixed. |
| `admin_core/operator_observability.py` | Read-only audit search/export/detail surfaces | EXTEND | Good candidate for read-only API view extraction. |

Decision: there are multiple audit actors, but they represent different layers. Do not merge writers first. Extract only read-only audit/search serializers.

## Closure Writer Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin/v7-admin-api:11599` | `closure_records` read path | EXTEND | Read-only closure list/detail builder can move later. |
| `admin/v7-admin-api:11771` | closure state append via `append_jsonl` | DO NOT TOUCH | Writer is authority-bearing; keep in monolith until contracts are frozen. |
| `tools/v7-users-autoswitch` | emits `closure_owner=admin/v7-admin-api` target metadata | REUSE | Tool confirms admin API remains closure owner. |
| `admin_core/operator_observability.py` | correlates audit/evidence/operations for operator timeline | EXTEND | Read-only closure correlation can be extended here. |

Decision: closure ownership is split between admin write authority and runtime result metadata. This is intentional; do not merge in API.1/API.2.

## Execution Path Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin/v7-admin-api:9595` | `run_action` command executor for admin actions | DO NOT TOUCH | High-risk runtime mutation boundary. |
| `admin/v7-admin-api:9563` | `run_readonly` command executor for safe command reads | DO NOT TOUCH FIRST | Can be wrapped only after command contract fixtures exist. |
| `admin_core/operator_execution.py` | Execution packet/event model | REUSE | This is the canonical operator execution packet model. |
| `tools/v7-users-autoswitch` | Runtime planner/apply/dry-run engine | REUSE | Planner remains execution-adjacent authority; admin API should not duplicate it. |

Decision: execution is already separated conceptually but still invoked through admin action endpoints. Decomposition must not create a second executor.

## Rollback Path Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin/v7-admin-api` rollback endpoints/actions | Operator-triggered rollback wrappers and previews | DO NOT TOUCH | Rollback must stay in monolith until action contracts are complete. |
| Runtime support rollback tools | Actual runtime rollback mechanics | REUSE | Runtime support remains authority. |
| `admin_core/operator_execution.py` | Packet rollback preview/lineage data | EXTEND | Read-only rollback preview views may be extracted later. |

Decision: rollback authority is sensitive. Start with previews and lineage only, never apply handlers.

## Governance Path Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin/v7-admin-api` governance/approval/rehearsal endpoints | Admin presentation and selected action wrappers | DO NOT TOUCH FIRST | Keep routing and action dispatch fixed. |
| `admin_core/operator_execution.py` | Contract/packet/event foundation | REUSE | Canonical governance packet source. |
| `admin_core/operator_observability.py` | Read-only governance evidence views | EXTEND | Good read-only extraction target. |

Decision: no parallel governance system should be introduced. API decomposition should move serializers and view builders around the existing packet model only.

## Service Reader Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin/v7-admin-api` service matrix and route-class helpers | Overview, route fitness, recommendations, actions | EXTEND | Read-only service summary builders are valid extraction targets. |
| `tools/v7-service-matrix-refresh-all` | Refresh/cache producer | REUSE | Background producer remains outside admin API decomposition. |
| `tools/v7-service-matrix-test` | Probe/test utility | REUSE | Keep tool behavior unchanged. |
| `tools/v7-users-autoswitch` | Planner consumes service signals | DO NOT TOUCH | Planner semantics certified separately. |

Decision: shared service read models are useful, but cache production and planner decisions must stay separate.

## Routing Intelligence Reader Overlap

| Location | Behavior | Classification | Decision |
|---|---|---|---|
| `admin_core/routing_intelligence.py` | Advisory scoring/read model | REUSE | Canonical RI advisory model. |
| `admin_core/routing_brain.py` | Candidate advisory score contract | REUSE | Planner advisory influence source. |
| `tools/v7-users-autoswitch` | Uses RI advisory score in planner ranking | DO NOT TOUCH | Certified RI.3 behavior should remain fixed. |
| `admin/v7-admin-api` | May display routing/planner surfaces | EXTEND | Extract display adapters only after RI.3 contract fixtures. |

Decision: routing intelligence already has an owner outside the monolith. Admin API should expose read-only views, not recompute or override RI authority.

## Overall Duplication Verdict

Dangerous duplicate systems were not found in the form of two independent admin API routers or two independent runtime executors inside `admin/v7-admin-api`.

Material overlap exists in:

- registry parsing;
- audit and closure read/write responsibilities;
- service matrix/service-aware read helpers;
- preview/governance presentation builders.

These overlaps are manageable if API.2 starts with read-only extraction and avoids auth, routing, action execution, audit writes, closure writes, rollback apply, governance apply, and UI separation.
