# Program Z1.5 Safety Review

Date: 2026-06-01

## Which Model Is Safer?

Strict target approval is safest in isolation because it denies almost all drift.

## Which Model Is More Practical?

Policy approval is more practical for bounded autonomy because target ranking changes frequently.

## Which Model Scales?

Hybrid scales best:

- target approval for high-risk or unusual movements
- policy approval for one-user bounded autonomy inside a strict target class
- fail-closed when candidate, budget, route class, trust class, rollback, or safety status changes

## Safety Decision

Use HYBRID.

Policy approval should not mean broad autonomy. It should mean:

`one approved user, budget=1, route_class=GLOBAL_STABLE, target_class=BEST_HEALTHY, strict substitution gates, TTL, fresh recheck`

## Safety Verdict

The hybrid model is safer than pure policy approval and more practical than pure target approval.

