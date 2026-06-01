# Program Z1.5 Policy Approval Analysis

Date: 2026-06-01

## Model

Approval for:

- `user=X`
- `target_class=BEST_HEALTHY`
- `budget=1`
- `route_class=GLOBAL_STABLE`

## Advantages

- Reduces stale-denial caused by harmless target substitution.
- Keeps autonomy bounded to one user.
- Lets runtime choose the best eligible target at execution time.
- Better matches the planner's actual decision model.
- Can preserve safety if fingerprints and substitution constraints are strict.

## Risks

- Harder for operators to understand than target approval.
- Requires a precise target-class contract.
- Bad substitution rules could move traffic to an unintended trust/route/capacity class.
- Replay protection must include policy fingerprint, proposal generation, and runtime snapshot tolerance.

## Failure Modes

- policy class too broad
- trust class mismatch
- route class mismatch
- capacity class mismatch
- target only barely healthy
- candidate changed when approval only intended one user
- target changes after approval but outside allowed class

## Operational Cost

Medium. It needs better packet text and UI explanation, but reduces repeated stale target approvals.

## Verdict

policy_approval_understood=true

