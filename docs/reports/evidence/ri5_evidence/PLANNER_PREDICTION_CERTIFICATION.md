# PLANNER_PREDICTION_CERTIFICATION

Planner owner remains:

`tools/v7-users-autoswitch`

Planner may read:

- `prediction-summaries`;
- forecast advice;
- future degradation advice;
- future recovery advice.

Planner may not:

- delegate authority;
- change governance;
- change execution;
- change selected moves ownership;
- execute prediction.

## Snapshot Behavior

`prediction-summaries` is advisory-only.

Low confidence: `IGNORE`

Stale: `IGNORE`

Expired/unknown: stop behavior is handled by generic snapshot reader, but prediction remains non-required and cannot create selected moves.

## Verdict

```text
planner_authority_changed=false
governance_changed=false
execution_changed=false
selected_move_ownership_changed=false
```

