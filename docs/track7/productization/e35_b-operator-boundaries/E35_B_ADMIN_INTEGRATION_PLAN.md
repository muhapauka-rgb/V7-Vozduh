# E35.B Admin Integration Plan

## Rule

Use existing `/admin-v2`.

No new top-level sections.

## Users

Show:

- Routing Mode;
- Authority Owner;
- Boundary State;
- Why Movement Allowed;
- Why Movement Blocked;
- Authority Chain;
- Conflict Explanations;
- Next Safe Action.

Operator value:

The operator can understand why a user can or cannot move.

## Channels

Show:

- Group Restrictions;
- Boundary Violations;
- Containment State;
- Pinned Users;
- Manual Users;
- Autoswitch blocked reasons.

Operator value:

The operator can understand why a channel is not available for a user or group.

## Settings

Show/edit later:

- Boundary Defaults;
- Group Boundary Rules;
- Operator override policy;
- Future Scheduler Policies.

Operator value:

The operator configures policy boundaries without changing runtime routing directly.

## Logs

Show filters:

- Boundary Violations;
- Authority Overrides;
- Containment Actions;
- Conflict Resolutions;
- Denied movement attempts.

Operator value:

Audit chain explains every denied/overridden movement.

## Home

Summary only:

- Boundary Violations;
- Pinned Users;
- Containment Events;
- Authority Conflicts.

## Runtime Mapping

Admin reads boundary state from:

- authority evaluator;
- org policy;
- users registry;
- egress registry;
- Evidence/Proposal/Trust surfaces.

## Storage Impact

Admin displays effective state and event history.

It should not store duplicate truth in UI.

## API Impact

Future APIs:

- boundary summary;
- user boundary detail;
- channel boundary detail;
- conflict preview;
- events list.

## Tests

- User drawer shows boundary state.
- Channel drawer shows group restrictions.
- Logs filter boundary events.
- Home summary counts conflicts.
- Admin boundary views do not mutate runtime.

## Verdict

```text
admin_integration_defined=true
```
