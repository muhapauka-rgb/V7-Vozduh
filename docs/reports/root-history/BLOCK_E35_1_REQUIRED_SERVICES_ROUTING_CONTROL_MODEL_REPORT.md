# BLOCK E35.1 - Required Services & Routing Control Model Report

## 1. Scope

E35.1 defined the Required Services & Routing Control Model for V7.

The block covered:

- existing implementation discovery;
- required services model;
- channel suitability model;
- hard block vs soft preference semantics;
- group model and Organizations -> Groups evolution;
- routing mode semantics;
- admin integration plan for `/admin-v2`;
- storage/API contract;
- test plan;
- runtime boundary.

No implementation that mutates runtime was performed.

## 2. Runtime Mutation Statement

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false

No live users, routes, channels, runtime services, policy apply paths, Direct/Trusted RU refresh paths, kill switch controls or autoswitch apply paths were executed or changed.

## 3. Existing Implementation Discovery Summary

Discovery report:

```text
docs/track7/productization/e35_1-required-services-routing-control/E35_1_EXISTING_IMPLEMENTATION_DISCOVERY.md
```

Key findings:

- Required services already exist through `SERVICE_CATALOG`, `DEFAULT_USER_PRIORITY_SERVICES`, `SERVICE_PREFS_FILE`, `/api/actions/service-preferences-update`, service matrix and service recommendations.
- Channel suitability already exists partially through service matrix route fitness, service-aware dry run and autoswitch gates.
- Organizations and Groups already exist in identity DB; `org-egress-policy.json` already supports group/egress policy concepts.
- Autoswitch already has real group gates, quality gates, service gates, load gates and safety gates.
- Admin already has Users, Channels, Routing, Settings, Evidence, Proposals, Runtime Trust and Release Trust surfaces.
- Missing product piece is one unified effective routing-control model and admin explanation layer.

## 4. Reuse / Extend / Refactor / Replace / Do Not Touch

| Area | Decision | Reason |
|---|---|---|
| Service catalog | Reuse | Already authoritative for known service IDs. |
| Per-user service preferences | Extend | Existing store works, but needs effective merge with group baseline. |
| Service matrix | Reuse | Already computes service status and route-class fitness. |
| Service recommendations | Extend | Already produces manual-review recommendations; needs explicit hard/soft semantics. |
| Identity groups | Extend | Existing group table can become the identity half of the Group model. |
| Organizations | Reuse | Keep as identity/admin metadata linked to groups. |
| Org-egress policy | Extend | Existing JSON already models group constraints, but needs formal contract and admin UX. |
| Autoswitch group gates | Reuse | Already implements allowed/excluded/preferred/exclusive/isolation gates. |
| Autoswitch service/quality/load/safety gates | Reuse | Already match E35.1 priority chain. |
| Per-user pinned channel | Extend | Not currently explicit. Add future `routing_mode` and `preferred_channel`. |
| Proposal/Evidence/Trust | Do Not Touch | Already certified non-authoritative operator chain. |
| Approval packet/operator execution | Do Not Touch | Safety-critical governance path. |
| Execution-only targets | Do Not Touch | Certified governance target model. |

## 5. Final Model Summary

Model document:

```text
docs/track7/productization/e35_1-required-services-routing-control/E35_1_REQUIRED_SERVICES_ROUTING_CONTROL_MODEL.md
```

Defined:

- Required Services as first-class suitability/admission inputs.
- Group baseline required services.
- User-added required services.
- No silent removal of group-required services.
- Effective required services merge rule.
- Channel suitability gates.
- Hard Block and Soft Preference semantics.
- Groups as routing/policy containers.
- Priority chain.
- Routing modes: `AUTO`, `OPERATOR_PINNED`, future-reserved `MANUAL`.

Final priority chain:

```text
Safety / runtime trust
-> group allowed channels
-> user/group required services
-> route-class compatibility
-> capacity hard gates
-> operator routing mode constraints
-> stability
-> sticky preference
-> speed/score
-> proposal/governance admission
-> execution-time recheck later in E35.D/P2
```

## 6. Admin Integration Summary

Admin plan:

```text
docs/track7/productization/e35_1-required-services-routing-control/E35_1_ADMIN_INTEGRATION_PLAN.md
```

Existing admin `/admin-v2` remains the only admin surface.

Planned integration:

- `Пользователи` -> User Drawer: routing mode, preferred channel, group, effective required services, current suitability, "why this user is here".
- `Каналы` -> Channel Drawer: group allow/exclude status, service suitability, capacity, users blocked from channel and why.
- `Настройки` -> Groups routing control: group list, allowed channels, required services, default routing mode, audit link.
- `Маршруты`: service-aware preview and hard-block reasons.
- `Главная`: summary indicators only.
- `Проверки`: diagnostics for service matrix, group policy and pinned users.
- `Логи`: filters/history for future routing-control changes.

No new top-level admin section is required.

## 7. Storage/API Contract Summary

Contract:

```text
docs/track7/productization/e35_1-required-services-routing-control/E35_1_STORAGE_API_CONTRACT.md
```

Storage strategy:

- Reuse service preferences.
- Reuse identity DB groups/organizations.
- Reuse org-egress policy.
- Reuse users/egress registries.
- Do not introduce duplicate truth source.

Read API design:

- `GET /api/routing-control/users`
- `GET /api/routing-control/users/{ip}`
- `GET /api/routing-control/groups`
- `GET /api/routing-control/groups/{group_id}`
- `GET /api/routing-control/suitability`
- `GET /api/routing-control/services/summary`

Future mutation APIs are deferred to later blocks and must not move users directly.

## 8. Tests Run And Results

Checks file:

```text
docs/track7/productization/e35_1-required-services-routing-control/E35_1_CHECKS.md
```

Commands run:

```text
git diff --check
```

Result:

```text
PASS
```

Marker scan:

```text
PASS
```

Dangerous-call scan:

```text
PASS_WITH_DOCUMENTATION_ONLY_MENTIONS
```

Notes:

- Matches were safety/test documentation references only.
- No executable code was added.
- No runtime mutation command was executed.

tests_passed=true

## 9. Files Changed

Created:

- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_EXISTING_IMPLEMENTATION_DISCOVERY.md`
- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_REQUIRED_SERVICES_ROUTING_CONTROL_MODEL.md`
- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_ADMIN_INTEGRATION_PLAN.md`
- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_STORAGE_API_CONTRACT.md`
- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_TEST_PLAN.md`
- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_RUNTIME_BOUNDARY.md`
- `docs/track7/productization/e35_1-required-services-routing-control/E35_1_CHECKS.md`
- `BLOCK_E35_1_REQUIRED_SERVICES_ROUTING_CONTROL_MODEL_REPORT.md`

## 10. Safety Verdict

Safety verdict:

```text
SAFE_READ_ONLY_ARCHITECTURE_BLOCK_COMPLETE
```

E35.1 created the model and implementation contract needed before E35.A/P2 work. It did not create runtime authority, movement authority or autoswitch authority.

## Final Verdict

required_services_model_defined=true
group_model_defined=true
routing_modes_semantics_defined=true
admin_integration_defined=true
storage_api_contract_defined=true
test_plan_defined=true
tests_passed=true
e35_1_ready_for_e35_A=true

## Final Mutation Statement

Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
Cohort performed: NO
