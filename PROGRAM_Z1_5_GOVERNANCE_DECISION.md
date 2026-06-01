# Program Z1.5 Governance Decision

Date: 2026-06-01

## Selected Model

HYBRID

## Why Not Pure Target Approval?

It is safe but too brittle. Recent evidence shows repeated stale denials before execution.

## Why Not Pure Policy Approval?

It is practical but too broad unless constrained. Without strict gates it could hide meaningful trust or route-class changes from the operator.

## Recommended Hybrid Contract

Use target approval for:

- high-risk moves
- execution-only targets
- manual-only targets
- trust class changes
- route class changes
- rollback-sensitive actions

Use policy approval for:

- one user
- budget `1`
- route class `GLOBAL_STABLE`
- target class `BEST_HEALTHY`
- same trust class
- same policy class
- short TTL
- fresh recheck
- replay protection

## Required Implementation Before Execution

- movement approval packet schema
- policy approval fingerprint
- target substitution validator
- runtime recheck validator
- replay/expiry/stale-hash denial tests
- read-only admin preview explaining allowed substitutions

## Verdicts

- governance_model_selected=true
- recommended_model=HYBRID
- safe_to_continue=true

