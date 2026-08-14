# API.1 Safe Extraction Candidates

This list is ordered from safest to most constrained. Every candidate assumes before/after contract tests, `py_compile`, endpoint inventory verification, and no runtime mutation.

## Stage 1 Candidates: Read-Only And Pure

| Candidate | Current location | Proposed home | Risk | Expected line reduction | Notes |
|---|---|---|---|---:|---|
| Redacted registry view builders | `parse_registry`, registry map/default helpers | `admin_core.admin_registry_views` or extended `admin_core.registry_readers` | LOW | 150-300 | Reuse `parse_registry_lines`; no writes. |
| Event list serializers | admin event wrappers | `admin_core.events` or observability adapter | LOW | 100-250 | Preserve pagination and redaction. |
| Audit search/export-preview serializers | admin API wrappers + `admin_core.operator_observability` | `admin_core.operator_observability` | LOW/MEDIUM | 150-400 | Do not move `audit_admin`. |
| Evidence/detail/timeline serializers | operator read-only endpoints | `admin_core.operator_observability` | LOW/MEDIUM | 200-500 | Good because the owner already exists. |
| Safe value parsers and request-independent validators | scattered helper functions | `admin_core.sanitize` or new `admin_core.validators` | LOW | 100-250 | Only pure functions; avoid auth-specific validators first. |

## Stage 2 Candidates: Heavy Read Builders

| Candidate | Current location | Proposed home | Risk | Expected line reduction | Notes |
|---|---|---|---|---:|---|
| Overview sub-summary builders | `overview`, `overview_for_session`, `overview_cached` dependencies | `admin_core.admin_overview` | MEDIUM | 500-1,500 | Needs snapshot tests for `/api/overview`. |
| Service matrix summaries | service matrix helpers | `admin_core.service_views` | MEDIUM | 300-800 | Cache/read model only; producer tools stay separate. |
| Route-class and policy read summaries | policy/route helpers | `admin_core.policy_views` | MEDIUM | 300-700 | Read-only first; no policy writes. |
| Trusted RU/direct read summaries | trusted/direct helpers | `admin_core.policy_views` | MEDIUM/HIGH | 200-600 | Read-only only due routing sensitivity. |
| Traffic SQLite summary readers | traffic helpers | `admin_core.traffic_views` | MEDIUM | 150-400 | Should be cached/background where possible. |

## Stage 3 Candidates: Preview-Only Parsers

| Candidate | Current location | Proposed home | Risk | Expected line reduction | Notes |
|---|---|---|---|---:|---|
| Egress import parsers | OpenVPN/Clash/Xray/Outline/share helpers | `admin_core.egress_preview` | MEDIUM | 800-1,800 | Pure parse/normalize only; no apply/provision. |
| Egress config preview serializers | `egress_config_preview` and siblings | `admin_core.egress_preview` | MEDIUM | 300-700 | Preview result shape must be fixture-tested. |
| Identity read summaries | identity state functions | `admin_core.identity_views` | MEDIUM | 300-800 | No create/update/revoke/profile issue. |
| Profile delivery read summaries | token state read helpers | `admin_core.profile_delivery_views` | MEDIUM/HIGH | 200-500 | Token mutation and public delivery remain. |

## Must Not Be Extracted First

| Area | Reason |
|---|---|
| `Handler.do_GET` / `Handler.do_POST` | Auth, routing, response semantics, and CSRF are all coupled here. |
| `require_auth` / session handling / RBAC | Security behavior cannot drift. |
| `run_action` | Runtime mutation boundary. |
| `run_readonly` | Less dangerous than `run_action`, but command contracts are not fully frozen. |
| `audit_admin` | Audit writer authority. |
| closure writes | Operator closure accountability. |
| user movement endpoints | Direct user movement risk. |
| autoswitch apply | Planner/runtime authority and user movement risk. |
| egress enable/apply/provision | Runtime egress state risk. |
| policy/direct/trusted RU apply | Routing behavior risk. |
| rollback apply | Recovery behavior risk. |
| whole `html_page_v2` UI | Large but tightly coupled to API contracts and action names. |

## First API.2 Recommendation

Start API.2 with one small read-only module:

`admin_core.admin_registry_views`

Scope:

- registry snapshot loading;
- redacted users/egress rows;
- egress map/default helpers;
- no writes;
- no `run_action`;
- no endpoint route changes except importing helper functions;
- before/after endpoint inventory and `/api/overview` fixture checks.

This is the cleanest path because `admin_core.registry_readers` already exists and the admin API currently wraps it locally.
