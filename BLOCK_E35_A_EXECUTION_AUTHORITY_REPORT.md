# BLOCK E35.A Execution Authority Report

## 1. Discovery Summary

E35.A completed as an architecture, governance, admin integration and implementation planning block.

No runtime mutation was performed.

Discovery confirmed:

- current assignment truth is `users.registry`;
- autoswitch can recommend/apply selected moves when allowed;
- admin manual switch can directly request `v7-user-switch`;
- approval packets provide packet-bound governance authority;
- execution-only targets are isolated from autoswitch;
- channel/group/service/capacity/safety gates already block movement candidates;
- sticky and preferred egress are soft preferences, not authority.

Missing today:

- explicit routing authority model;
- explicit per-user ownership;
- explicit `AUTO`;
- explicit `OPERATOR_PINNED`;
- explicit user-level `MANUAL`;
- pin lifecycle.

## 2. Authority Model

Routing Authority is:

```text
The right to change a user's channel.
```

Outcomes:

```text
ALLOW
DENY
REVIEW_REQUIRED
EMERGENCY_ONLY
```

Owners:

| Owner | Role |
|---|---|
| AUTOSWITCH | May move AUTO users when all gates pass. |
| OPERATOR | May create manual/pinned intent and direct manual movement. |
| GOVERNANCE | May authorize bounded packet-scoped movement. |
| SCHEDULER | Future launcher only; no direct override. |
| CONTAINMENT | Emergency/rollback authority only. |

## 3. Routing Modes Verdict

Final routing modes:

```text
AUTO
OPERATOR_PINNED
MANUAL
```

Verdict:

- `AUTO` should be active/default.
- `OPERATOR_PINNED` should be implemented as a hard authority lock against normal autonomous movement.
- `MANUAL` should exist now in the model because admin manual movement already exists, but rollout can be staged.

## 4. Override Matrix

Summary:

- Autoswitch cannot override operator pin or manual mode.
- Operator can override autoswitch, but not safety/governance hard denial.
- Governance can override pins/manual only with explicit protected-user override.
- Containment can emergency-override pin/manual only to reduce harm.
- Safety blocks everyone for forward movement.
- Scheduler cannot override anyone.

Full matrix:

```text
docs/track7/productization/e35_a-execution-authority/E35_A_OVERRIDE_MATRIX.md
```

## 5. Emergency Model

Emergency authority is for containment only.

It is allowed when current target hard-fails, is quarantined, loses required services, violates runtime trust or requires rollback/containment.

It is not allowed for:

- better speed;
- better score;
- normal rebalancing;
- group preference.

Emergency placement must be temporary and must expose return state in admin.

## 6. Admin Integration

No new top-level admin section.

Integrate into:

- `Главная`: summaries only;
- `Пользователи`: routing mode, owner, pin, reason, emergency state, timeline;
- `Каналы`: pinned users, authority locks, emergency evacuations;
- `Настройки`: defaults and future scheduler defaults;
- `Логи`: authority changes and overrides.

## 7. Runtime Mapping

Runtime truth remains:

```text
users.registry.current
users.registry.table
```

Authority truth should be separate:

```text
routing-authority.json
routing-authority-events.jsonl
```

Authority evaluator should run before:

- autoswitch apply;
- admin manual switch confirmation;
- governed execution;
- future scheduler launch.

## 8. Implementation Readiness

Recommended first implementation:

1. Authority store and event log.
2. Read/preview APIs.
3. Admin visibility.
4. Autoswitch authority gate.
5. Governance authority hash/override integration.
6. Later write APIs for pin/manual/auto.

Implementation-ready verdict:

```text
implementation_ready=true
e35_b_ready=true
```

## 9. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Manual switch mistaken for persistent pin | High | Add explicit authority state. |
| Sticky score mistaken for authority | High | Keep sticky as soft preference only. |
| Autoswitch moves pinned user | High | Add authority gate before selection/apply. |
| Governance packet ignores authority drift | High | Include authority hash in packet/recheck. |
| Emergency escape becomes normal bypass | High | Restrict to hard failure/containment triggers. |
| Admin UI hides authority | Medium | Add visible Users/Channels/Logs surfaces. |

## 10. Recommendations For E35.B/C

Recommended E35.B:

```text
E35.B_ROUTING_AUTHORITY_STORAGE_AND_API_CONTRACT
```

Scope:

- authority store schema;
- event log schema;
- effective authority resolver;
- read/preview API contracts;
- authority hash contract for governance packets.

Recommended E35.C:

```text
E35.C_ROUTING_AUTHORITY_ADMIN_AND_RUNTIME_GATE_IMPLEMENTATION_PLAN
```

Scope:

- admin integration detail;
- autoswitch gate integration;
- manual switch authority check;
- governance authority recheck;
- implementation test matrix.

## Required Verdicts

```text
authority_model_defined=true
authority_owner_model_defined=true
routing_modes_finalized=true
override_matrix_defined=true
emergency_authority_defined=true
runtime_mapping_defined=true
admin_integration_defined=true
implementation_ready=true
e35_b_ready=true
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
