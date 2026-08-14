# Admin Registry Wrapper Consumer Mapping Report

**Discovery:** `ADMIN_REGISTRY_WRAPPER_CONSUMER_MAPPING_V1`  
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**Type / Layer:** `READ_ONLY_BOUNDARY_DISCOVERY / MANAGEMENT_PLANE`  
**Runtime / Production / Authority effects:** `NONE / NONE / NONE`

## 1. Scope and owner boundary

The mapped cluster is limited to six Admin-local functions in
`admin/v7-admin-api`:

```text
parse_registry
egress_registry_rows
egress_registry_map
egress_exists
default_egress_id
egress_interface
```

Their existing target owner is `admin_core.admin_registry_views`. No source,
Runtime, CPS, owner, action handler, routing or egress lifecycle was changed.

## 2. Consumer matrix

Static AST mapping found exactly `84` Admin-local call sites. Classification is
by actual caller role, not by wrapper size.

| Wrapper | Calls | Read-only | Diagnostic | Admin action | Needs clarification | State / effect |
| --- | ---:| ---:| ---:| ---:| ---:| --- |
| `parse_registry(path)` | 41 | 16 | 5 | 18 | 2 | reads the caller-provided registry; returns redacted rows; no write itself |
| `egress_registry_rows()` | 5 | 3 | 0 | 2 | 0 | reads `STATE_DIR/egress.registry`; list output |
| `egress_registry_map()` | 17 | 6 | 0 | 9 | 2 | reads same registry; id-to-row map output |
| `egress_exists()` | 13 | 1 | 0 | 12 | 0 | validation predicate used by guarded POST flows |
| `default_egress_id()` | 7 | 2 | 0 | 5 | 0 | enabled-egress selection used by identity/POST flows |
| `egress_interface()` | 1 | 1 | 0 | 0 | 0 | route-status expected-device lookup |
| **Total** | **84** | **29** | **5** | **46** | **4** | no wrapper writes state |

`ADMIN_ACTION` means the caller can lead to an Admin operation; it does not
mean that the wrapper itself mutates state. `READ_ONLY` and `DIAGNOSTIC` mean
the caller’s observed path is read-only. The four unclassified call sites are
`egress_config_path`, `egress_runtime_profile_candidates`,
`generated_evidence_bundles`, and `generated_proposals`; their callers need a
separate behavior trace before any consumer migration is considered.

## 3. Responsibility matrix

| Wrapper | Actual responsibility | Target owner | Duplicate layer? | Wrapper value | Removal safety |
| --- | --- | --- | --- | --- | --- |
| `parse_registry` | transparent redacted parsing of an explicit path | `registry_views.parse_registry(path)` | yes at function level | none beyond local naming | blocked by 41 mixed consumers |
| `egress_registry_rows` | injects Admin `STATE_DIR` and enabled filter | `registry_views.egress_registry_rows(state_dir, ...)` | not a pure duplicate | binds Admin state-root boundary | blocked by action consumers |
| `egress_registry_map` | injects Admin `STATE_DIR`; map adapter | `registry_views.egress_registry_map(state_dir, ...)` | not a pure duplicate | centralizes implicit state-root use | blocked by action/unknown consumers |
| `egress_exists` | injects `STATE_DIR` for validation predicate | `registry_views.egress_exists(state_dir, ...)` | not a pure duplicate | preserves existing validation boundary | keep pending guarded-action analysis |
| `default_egress_id` | injects `STATE_DIR` for default selection | `registry_views.default_egress_id(state_dir)` | not a pure duplicate | protects identity/POST defaults | keep pending action analysis |
| `egress_interface` | injects `STATE_DIR` for route expectation | `registry_views.egress_interface(state_dir, id)` | thin adapter | test seam and route-status boundary | needs exact test/route contract |

The prior assumption that all six are equivalent “duplicate wrappers” is not
supported. Only `parse_registry` is a transparent delegation; the five egress
wrappers bind the existing Admin state-root into an owner API that deliberately
requires an explicit `state_dir` parameter.

## 4. Consumer separation

Read-only consumers include overview, user/egress detail, traffic summary,
route diagnostics, service-aware dry-run/preview and trusted-RU readiness.
Diagnostic consumers produce evidence/proposal or drift outputs. Action-bound
consumers include identity/profile issuance, egress draft/provision/delete
flows and guarded `do_POST` handlers. These groups must not share a single
migration without distinct behavior and rollback proof.

## 5. `egress_interface` monkey-patch

`tests/unit/test_api5_runtime_route_diagnostic_views.py` monkey-patches
`admin.egress_interface` only in `test_route_status_and_direct_routing_parity`.
It supplies an expected device (`stable -> awg0`) while `run_readonly` supplies
route output. It is test-only, not a production dependency, but it is an
intentional seam in the route-status test. Replacing it would require a
separate existing-owner contract for injected state-root/expected interface;
no patch was changed here.

## 6. Future-candidate disposition

| Group | Members | Disposition | Reason |
| --- | --- | --- | --- |
| A — ready now | none | `NONE` | no wrapper has both isolated consumers and complete direct-owner migration proof |
| B — evidence required | `parse_registry`, `egress_interface` | `NEEDS_MORE_EVIDENCE` | split parse readers from mixed/action callers; baseline route-status monkey-patch contract |
| C — retain boundary | `egress_registry_rows`, `egress_registry_map`, `egress_exists`, `default_egress_id` | `KEEP_PENDING_ACTION_ANALYSIS` | each injects `STATE_DIR` and serves action or validation paths |

## 7. Exact next action

Do not create an implementation Mission. The smallest safe re-entry is a
read-only split of `parse_registry` consumers into independent read-only and
action-bound cohorts, including output/rollback contracts for one cohort only.
The global CPS successor remains:

```text
EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION
```
