# E25.14 Post-Abort Restore-Settle

## Result

`restore_settle_gate_status=GO`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

## Context

No forward movement was executed, so this is a post-abort restore-settle validation rather than a post-rollback settle.

Fresh settle evidence:

```text
gate_status=GO
sample_count=3
checkers_ok=True
hidden_movers_observed=False
execution_allowed_now=False
```

See:

- `docs/track7/productization/e25_14-evidence/recheck-restore-settle.pretty`
- `docs/track7/productization/e25_14-evidence/post-abort-safety-check.md`
