# BLOCK E35.B Operator Boundaries Report

## 1. Discovery Summary

E35.B completed as architecture/governance/admin-integration/implementation-planning only.

Discovery found many existing boundary-like systems:

- safety gates;
- runtime trust and restore-settle;
- approval packet scope, hash binding and replay protection;
- autoswitch basic/reservation/group/service/quality/load/safety gates;
- group allowed/excluded/preferred/isolation policy;
- channel `manual_only`, `reserve_only`, `canary_reserved`;
- required services;
- capacity hard limits;
- quality floors;
- quarantine and anti-flap controls;
- manual switch;
- rollback/containment-like paths.

These are real boundaries, but V7 still needs a deterministic constitutional layer for actor precedence and conflict resolution.

## 2. Authority Domains

Final domains:

1. Safety
2. Containment
3. Governance
4. Operator
5. Group
6. User
7. Autoswitch
8. Scheduler

## 3. Boundary Matrix

The full boundary matrix is in:

```text
docs/track7/productization/e35_b-operator-boundaries/E35_B_BOUNDARY_MATRIX.md
```

Core rule:

```text
Safety can block everyone.
Containment can override only to reduce harm.
Governance defines exact execution scope.
Operator owns explicit user intent.
Group constrains policy boundaries.
User influences, but does not authorize.
Autoswitch acts only inside boundaries.
Scheduler only times already-authorized work.
```

## 4. Group Boundaries

Groups may:

- restrict channels;
- require services;
- define default routing mode;
- define operator override requirements;
- constrain autoswitch.

Groups may not:

- move users directly;
- bypass safety;
- bypass governance;
- silently override containment;
- hide hard restrictions from admin.

## 5. Operator Boundaries

Operator may:

- pin user;
- unpin user;
- set MANUAL;
- bypass autoswitch;
- request explicit movement.

Operator may never:

- bypass safety;
- bypass kill switch;
- bypass stale runtime trust;
- bypass replay denial;
- force unsafe movement.

## 6. Autoswitch Boundaries

Autoswitch may:

- move AUTO users only when all hard gates pass and apply authority exists.

Autoswitch may never:

- move pinned users;
- move manual users;
- break group restrictions;
- ignore required services;
- ignore capacity;
- ignore safety;
- ignore governance;
- use speed/score to defeat boundaries.

## 7. Containment Boundaries

Containment exists only to reduce harm.

It may temporarily override pin/manual/group/autoswitch boundaries when current state is unsafe.

It may never be used for:

- speed improvement;
- score improvement;
- convenience;
- normal rebalance;
- unbounded movement.

## 8. User Rights Model

Users do not have direct routing rights.

Users may influence routing through:

- required service needs;
- future request/feedback flow;
- evidence/proposal input.

Users cannot:

- move themselves;
- pin themselves;
- override operator/group/safety/governance.

## 9. Conflict Resolution Model

Conflict resolution is deterministic.

Examples:

- Group AUTO vs Operator MANUAL: MANUAL wins if operator override allowed, otherwise REVIEW_REQUIRED.
- Group allows A vs Operator pins B: DENY/REVIEW_REQUIRED unless B is group-allowed or explicit group override exists.
- Operator pin vs Safety: Safety wins.
- Operator pin vs Required Services: Containment may be EMERGENCY_ONLY if required service hard-fails.
- Proposal vs Authority: Authority wins.

## 10. Priority Chain

Final constitutional hierarchy:

```text
Safety
-> Containment
-> Governance
-> Operator
-> Group
-> User Intent
-> Autoswitch
-> Scheduler
-> Scoring / Speed / Preference
-> Proposal Explanation
```

## 11. Admin Integration

No new top-level admin section.

Use:

- `Главная`: summaries only;
- `Пользователи`: boundary state, authority chain, conflict explanations;
- `Каналы`: group restrictions, containment state, pinned users;
- `Настройки`: boundary defaults and group boundary rules;
- `Логи`: violations, overrides, containment, conflict resolution.

## 12. Implementation Readiness

E35.C should define implementation contracts for:

- boundary evaluator;
- conflict resolver;
- authority chain output;
- boundary event schema;
- admin read APIs;
- autoswitch/governance integration points.

P2 should implement read-only boundary surfaces first, then preview APIs and later controlled write paths.

## 13. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Operator override bypasses group accidentally | High | Explicit group override policy and audit. |
| Containment becomes normal bypass | High | Emergency triggers only, lease expiry, audit. |
| Autoswitch moves pinned/manual users | High | Boundary evaluator before selected moves. |
| Speed outranks safety/service/capacity | High | Constitutional chain keeps score low priority. |
| User requests mistaken for authority | Medium | User input remains proposal/evidence only. |
| Admin hides conflict reason | Medium | Mandatory boundary explanation UI. |

## 14. Recommendations For E35.C

Recommended next block:

```text
E35.C_BOUNDARY_EVALUATOR_AND_CONFLICT_RESOLUTION_CONTRACT
```

It should specify:

- evaluator input/output;
- conflict resolver table as machine-readable policy;
- event schema;
- read APIs;
- admin integration contract;
- integration points for autoswitch/governance/manual switch.

## Required Verdicts

```text
boundary_model_defined=true
authority_domains_defined=true
group_boundaries_defined=true
operator_boundaries_defined=true
autoswitch_boundaries_defined=true
containment_boundaries_defined=true
conflict_resolution_defined=true
priority_chain_defined=true
admin_integration_defined=true
implementation_ready=true
e35_c_ready=true
```

## Safety Verdict

```text
runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_changed=false
```
