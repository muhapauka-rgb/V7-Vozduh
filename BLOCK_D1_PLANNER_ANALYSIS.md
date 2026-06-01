# Block D1 Planner Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Observed Planner Output

Shadow summary:

- `candidate_moves=12`
- `selected_moves=0`
- `keep=6`
- `switch=12`
- `failover=12`

## Why Exactly 12

The planner produced failover recommendations for:

- Ten users on `amneziawg-exec-20260528-10-8-1-14`
- Two enabled users on `vless`

It kept users already on `awg3` and `awg0`.

## Rules

The repeated reason was:

- `current_egress_not_eligible`

For the execution cohort this is expected at the raw planner level because the execution target is:

- `role=EXECUTION_ONLY`
- `manual_only=1`
- `reserve_only=1`
- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`

## Classification

Expected but overly broad.

The raw planner is correct that execution-only is not a normal autoswitch target, but it lacks a governance hold concept for certified execution cohorts.

## Verdict

`planner_behavior_understood=true`

