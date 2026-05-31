# E35.A Execution Authority Model

## Definition

Routing Authority means:

```text
The right to change a user's channel.
```

Russian meaning:

```text
Право изменить маршрут пользователя.
```

Authority is independent from:

- score;
- speed;
- suitability;
- capacity;
- service matrix ranking.

Those systems answer:

```text
Where would be good?
```

Authority answers:

```text
Is this actor allowed to move this user now?
```

## Authority Outcomes

| Outcome | Meaning |
|---|---|
| `ALLOW` | Movement may proceed to downstream gates and execution-time recheck. |
| `DENY` | Movement must not proceed. |
| `REVIEW_REQUIRED` | Operator/governance confirmation required before movement. |
| `EMERGENCY_ONLY` | Only containment/rollback style movement may proceed. |

## Authority Owners

### AUTOSWITCH

Product meaning:

System-managed routing for users in `AUTO`.

Operator meaning:

The operator delegates normal forward routing to V7.

Runtime mapping:

- `tools/v7-users-autoswitch`;
- selected moves;
- service, capacity, quality and safety gates.

Storage mapping:

- future routing authority store: `routing_owner=AUTOSWITCH`;
- `routing_mode=AUTO`.

Admin visibility:

- Users drawer: "Режим: Авто";
- Logs: autoswitch authority decision;
- Evidence/Proposal: why movement was allowed or denied.

Scope:

- forward movement for `AUTO` users only;
- target must pass suitability and capacity;
- cannot override `OPERATOR_PINNED` or `MANUAL`.

Expiration:

- no per-user authority lease; uses current policy freshness and gates.

Override rules:

- blocked by Safety, Governance, Operator Pin, Manual mode, group hard constraints and runtime trust.

### OPERATOR

Product meaning:

Human operator owns a user routing decision.

Operator meaning:

The user stays where the operator put them until removed, expired, or emergency containment moves them.

Runtime mapping:

- admin manual switch;
- future pin create/remove actions;
- no autonomous forward movement away from pinned/manual target.

Storage mapping:

- `routing_owner=OPERATOR`;
- `routing_mode=OPERATOR_PINNED` or `MANUAL`;
- `preferred_egress` or `pinned_egress`;
- actor/reason/timestamps.

Admin visibility:

- Users drawer: owner, reason, target, age, expiry;
- Channels drawer: pinned users;
- Logs: pin created/removed/overridden.

Scope:

- exact user and explicit target.

Expiration:

- optional. If absent, persists until explicit removal or emergency override.

Override rules:

- can override autoswitch;
- cannot override Safety/Governance hard blocks;
- can be emergency-overridden by CONTAINMENT.

### GOVERNANCE

Product meaning:

Packet-bound, evidence-bound movement authority.

Operator meaning:

Movement only happens when approval, scope and execution-time recheck match.

Runtime mapping:

- approval packet;
- execution-time recheck;
- replay protection;
- rollback manifest.

Storage mapping:

- approval packet store;
- audit records;
- future authority decision record.

Admin visibility:

- Proposal/Governance path;
- Evidence timeline;
- Logs.

Scope:

- exact allowed users;
- exact allowed targets;
- bounded budget/blast radius.

Expiration:

- packet expiry.

Override rules:

- can move `AUTO`;
- can move `OPERATOR_PINNED` only if packet explicitly includes operator-pin override reason or emergency path;
- cannot bypass Safety.

### SCHEDULER

Product meaning:

Future scheduled execution admission.

Operator meaning:

Scheduler may queue, reserve and launch only previously authorized batches.

Runtime mapping:

- future scheduler;
- batch/concurrency/reservation system.

Storage mapping:

- future scheduler state;
- authority decision references.

Admin visibility:

- Settings defaults;
- Home summary;
- Logs.

Scope:

- no direct user movement;
- may initiate execution-time recheck for approved batches.

Expiration:

- schedule window and packet expiry.

Override rules:

- cannot override operator pins, manual mode, governance denial or safety.

### CONTAINMENT

Product meaning:

Emergency authority to reduce harm.

Operator meaning:

V7 may move a user away from a dangerous channel even when normal forward authority is blocked.

Runtime mapping:

- rollback;
- failover away from failed/quarantined target;
- restore to known safe target.

Storage mapping:

- emergency authority event;
- previous target;
- temporary target;
- return plan.

Admin visibility:

- Home: emergency pins/containment actions;
- Users drawer: emergency state;
- Logs: containment action and return state.

Scope:

- only away from unsafe state or back to known rollback target;
- never for speed or score.

Expiration:

- short emergency lease with return/review requirement.

Override rules:

- may override OPERATOR_PINNED and MANUAL only for safety/containment;
- must not override kill-switch or governance hard denial.

## Product Capability Mapping

Product capability:

```text
Authority gate before channel movement.
```

Admin surface:

- Users drawer authority card;
- Channels drawer locks/pins card;
- Settings defaults;
- Logs authority history;
- Home summary.

Runtime service:

- authority evaluator called before autoswitch apply, manual switch confirmation, scheduler launch and governance execution.

Storage:

- authority state store;
- append-only authority event log;
- existing users/egress registries remain runtime truth.

API:

- read effective authority;
- create/remove pins in later implementation;
- preview authority decision;
- list authority events.

UI component:

- AuthorityStatus;
- AuthorityDrawerSection;
- AuthorityTimeline;
- AuthorityConflictBanner.

## Verdict

```text
authority_model_defined=true
authority_owner_model_defined=true
```
