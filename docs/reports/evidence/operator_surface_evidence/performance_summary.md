# Operator Surface Performance Summary

Micro-check:

```text
{'iterations': 100, 'users': 50, 'elapsed_sec': 0.081365, 'avg_ms': 0.814, 'mode': 'missing_snapshot_fail_closed'}
```

Result:

- The read-only decision surface helper loads the request snapshot once per API request.
- Missing snapshots fail closed without runtime mutation.
- UI rendering is incremental: first overview renders normally, then operator decision surface enriches user/channel tables.
- No network probes, planner execution, autoswitch apply, user movement, or runtime execution are triggered by the decision surface.

