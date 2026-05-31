# E35.A Admin Integration Plan

## Rule

Use existing `/admin-v2`.

Do not create a new top-level section.

## Home

Show summaries only:

- pinned users count;
- manual users count;
- emergency authority count;
- authority conflicts count;
- containment actions count.

Components:

- `AuthoritySummaryStrip`
- `AuthorityConflictBadge`

## Users

User Drawer additions:

- Routing Mode;
- Authority Owner;
- Preferred/Pinned Channel;
- Authority Reason;
- Pin Created By;
- Pin Age;
- Expiry;
- Emergency State;
- Authority Timeline;
- "Why This User Is Here".

Operator actions for later implementation:

- Set AUTO;
- Pin to current channel;
- Pin to selected channel;
- Set MANUAL;
- Remove pin;
- View authority history.

No movement should happen from changing authority state alone.

## Channels

Channel Drawer additions:

- pinned users;
- manual users assigned here;
- authority locks;
- emergency evacuations;
- blocked moves;
- users protected from autoswitch.

## Settings

Authority defaults:

- default group routing mode;
- pin expiry defaults;
- emergency lease defaults;
- scheduler defaults (future);
- manual mode policy.

## Logs

Authority event filters:

- authority changes;
- pin creation;
- pin removal;
- manual mode set;
- emergency override;
- containment action;
- expiry;
- denied override.

## Evidence / Proposal / Trust Links

Authority UI must link to:

- Evidence bundle;
- Proposal;
- Runtime Trust;
- Release Trust;
- execution/governance audit when relevant.

## Operator Copy

Preferred Russian labels:

| Internal | Operator Label |
|---|---|
| `AUTO` | Авто |
| `OPERATOR_PINNED` | Закреплено оператором |
| `MANUAL` | Ручной режим |
| `AUTOSWITCH` | Система |
| `OPERATOR` | Оператор |
| `GOVERNANCE` | Governance |
| `CONTAINMENT` | Защитный перевод |
| `EMERGENCY_ONLY` | Только аварийное действие |

## Product Mapping

Product capability:

```text
Operator can see and control who is allowed to change a user's channel.
```

Admin surface:

- Home;
- Users;
- Channels;
- Settings;
- Logs.

Runtime service:

- authority evaluator read results shown in drawers.

Storage:

- routing authority store and events.

API:

- read authority;
- preview authority decision;
- future write actions.

Tests:

- authority visible in user drawer;
- channel drawer shows pinned users;
- logs filter authority events;
- changing authority does not move user.

## Verdict

```text
admin_integration_defined=true
```
