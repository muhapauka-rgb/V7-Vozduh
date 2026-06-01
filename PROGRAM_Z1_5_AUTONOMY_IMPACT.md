# Program Z1.5 Autonomy Impact

Date: 2026-06-01

## Target Approval Impact

Bounded autonomy impact:

- very safe
- very brittle
- high stale-denial rate
- poor fit for rapidly changing health

Rollback impact:

- simple and exact

Replay impact:

- easy to fingerprint

Fail-closed impact:

- strong and already demonstrated

Operator understanding:

- excellent

## Policy Approval Impact

Bounded autonomy impact:

- better fit for live planner
- fewer harmless stale target denials
- still bounded if budget/candidate/scope are fixed

Rollback impact:

- must bind rollback to current egress, not target egress

Replay impact:

- more complex; must include policy and runtime fingerprints

Fail-closed impact:

- strong only if substitution gates are strict

Operator understanding:

- needs explicit UI wording and explanation of allowed substitutions

## Verdict

autonomy_impact_understood=true

