# E35.D Admin View Models

## Home

Read models:

- Authority Summary;
- Pending Reviews;
- Emergency States;
- Authority Drift.

Operator value:

Know whether authority needs attention without opening technical details.

## Users

Read models:

- Routing Mode;
- Authority Owner;
- Pin State;
- Conflict State;
- Authority Timeline;
- Authority Explanation.

Operator value:

Understand why this user is here and whether movement is allowed.

## Channels

Read models:

- Pinned Users;
- Boundary Conflicts;
- Emergency Usage.

Operator value:

Understand who is locked to a channel and which users cannot move there.

## Checks

Read models:

- Authority Health;
- Evaluator Health;
- Conflict Statistics.

Operator value:

Validate that authority/evaluator storage is trustworthy.

## Logs

Read models:

- Authority Events;
- Reviews;
- Conflicts;
- Emergency Actions.

Operator value:

Follow audit lineage.

## Tests

- every view model can render with empty state;
- every view model can link to source events;
- no admin view mutates authority or routing;
- raw storage hidden by default.

## Verdict

```text
admin_view_models_defined=true
```
