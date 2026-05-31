# E35.C Admin Integration Plan

## Rule

Use existing `/admin-v2`.

No new top-level navigation section.

## Users

Show:

- Authority Verdict;
- Conflict Status;
- Boundary Explanation;
- Review Requirement;
- Emergency Status;
- Why Movement Allowed;
- Why Movement Denied.

## Channels

Show:

- Boundary Violations;
- Conflicts;
- Emergency Usage;
- Containment State.

## Checks

Show:

- Evaluator Health;
- Conflict Statistics;
- Review Queue;
- Emergency Queue.

## Logs

Show:

- Verdicts;
- Conflicts;
- Reviews;
- Emergency Decisions.

## Home

Summary only:

- Pending Reviews;
- Emergency Actions;
- Denied Actions;
- Boundary Conflicts.

## Tests

- verdict visible in user drawer;
- conflict visible in user/channel drawer;
- review queue visible under Checks;
- logs filter evaluator events;
- Home shows counts only.

## Verdict

```text
admin_integration_defined=true
```
