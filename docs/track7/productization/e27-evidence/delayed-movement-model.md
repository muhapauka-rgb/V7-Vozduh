# E27 Delayed Movement Model

## Inputs Reviewed

Fresh E27 restore-settle samples:

```text
gate_status=GO
sample_count=3
samples_span_seconds=56
apply_timer_intervals_covered=2.8
selected_moves_by_sample=[0, 0, 0]
hidden_movers_observed=false
checkers_ok=true
registry_stable=true
egress_registry_stable=true
```

## Scaling Model

Delayed movement protection can scale to two users if:

- selected_moves remains 0 before movement;
- hidden movers remain absent before, during, and after movement;
- post-forward observation checks both users and all out-of-scope users;
- rollback verification checks both users;
- post-rollback restore-settle samples verify `movement_count=0`;
- delayed monitoring explicitly checks no third user moved.

## Verdict

`delayed_movement_protection_scales=true`

This is a model verdict based on E25.15 and fresh E27 restore-settle evidence. It is not a two-user execution proof.

