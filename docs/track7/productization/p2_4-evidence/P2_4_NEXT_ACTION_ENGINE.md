# P2.4 Next Action Engine

## Result

next_action_engine_implemented=true

## Actions

The next action engine emits recommendations only:

- Wait
- Review
- Investigate
- Re-certify
- Collect Evidence
- Resolve Trust
- Review Group Policy
- Review Channel
- Review Capacity

## API

`GET /api/execution/readiness/actions` returns all non-PASS gate workflow items plus action grouping.

## Boundary

No action can remediate automatically. The output is operator guidance, not an apply path.
