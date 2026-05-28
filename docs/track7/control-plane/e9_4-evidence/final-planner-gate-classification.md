# E9.4 Final Planner Gate Classification

```text
parsed_latest_selected_moves=true
final_planner_selected_moves=3
selected_move=10.7.0.5:1->vless reason=user_frozen_until_2026-05-26T01:00:19.598532+00:00 current_egress_not_eligible
selected_move=10.0.0.2:1->vless reason=user_frozen_until_2026-05-26T01:07:39.350594+00:00 current_egress_not_eligible
selected_move=10.0.0.3:1->vless reason=user_frozen_until_2026-05-26T01:07:39.350692+00:00 current_egress_not_eligible
```

Verdict: ABORT. Apply timer restore is not allowed because final planner-only gate did not return `selected_moves=0`.
