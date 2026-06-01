# Block D1 Planner Cap Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Question

Can planner operate under budget `1`, `2`, `5`, `10` without changing core decision logic?

## Answer

Yes, with a packet-oriented post-planner cap.

Do not change scoring first. Keep raw decisions, then filter into a bounded proposal:

- Raw planner output remains advisory.
- Proposal builder sorts and caps candidates.
- Operator packet owns allowed users, target, TTL, hashes, rollback manifest, and replay protection.

## Budget Behavior

Budget `1`:

- Select highest confidence single candidate.
- Best for first operator-approved autoswitch retry.

Budget `2`:

- Matches Block B proven batch size.

Budget `5`:

- Matches Block C intermediate proof.

Budget `10`:

- Maximum proven blast radius, but not recommended until safety review and second target are fixed.

## Required Addition

Add an autoswitch proposal builder that accepts:

- `max_proposal_moves`
- `allowed_target_classes`
- `excluded_current_roles`
- `hold_cohort_labels`
- `require_safety_status=ok`

## Verdict

`planner_cap_possible=true`

