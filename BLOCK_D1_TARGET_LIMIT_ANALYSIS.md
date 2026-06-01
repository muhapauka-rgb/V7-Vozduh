# Block D1 Target Limit Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Current Limit

Defined in `/opt/v7/egress/state/egress.registry`:

- `soft_limit=10`
- `hard_limit=10`

For target:

- `amneziawg-exec-20260528-10-8-1-14`

## Limit Type

Primary classification:

- governance/certification guardrail
- registry limit

Not proven to be a hard technical interface limit.

## Related Policy

Autoswitch load policy includes:

- `max_hard_limit=80`
- dynamic hard limits can be larger than per-target registry limits

This means increasing the registry limit is technically possible as a configuration concept, but not approved by certification evidence.

## What If Limit Becomes 20

Likely technically feasible, but requires:

- capacity certification
- observation window
- trust review
- rollback impact review

## What If Limit Becomes 50

High blast-radius risk.

Requires broader performance and failure-domain proof.

## What If Limit Becomes 100

Exceeds current autoswitch policy `max_hard_limit=80`.

Not appropriate without policy redesign.

## Verdict

`target_limit_source_known=true`

