# E33.B Flapping Protection

flapping_protection_defined=true

## Purpose

Flapping protection prevents repeated proposal loops such as:

```text
A -> B -> A -> B
```

Routing Intelligence must suppress unstable recommendations before they enter Governance Control Plane.

## Protection Mechanisms

| Mechanism | Purpose | Effect |
| --- | --- | --- |
| Cooldown | Prevent immediate reverse proposal. | Suppress proposal or require review. |
| Minimum observation window | Require persistence before proposing movement. | OBSERVE until enough samples exist. |
| Pair reversal memory | Detect recent A/B reversal. | Penalize confidence or block proposal. |
| Duplicate proposal coalescing | Prevent repeated identical proposals. | Update existing proposal evidence instead of creating new execution candidate. |
| Confidence penalty | Reflect instability. | LOW/MEDIUM instead of HIGH. |
| Operator override marker | Allow reviewed exception. | Still must pass governance. |

## Proposal Suppression Rules

Suppress or downgrade when:

- same user-target pair reversed within cooldown;
- proposed target recently failed for same required_services;
- current target recovered but evidence is not stable;
- candidate target quality oscillates;
- repeated proposals were denied for same reason.

## Required Fields

Each proposal must carry:

```text
flapping_state
last_user_target_changes
pair_reversal_detected
cooldown_remaining
duplicate_proposal_id
confidence_penalty
```

## Fail-Closed Behavior

- Flapping risk never authorizes faster execution.
- If flapping state is unknown, output OBSERVE or REVIEW_REQUIRED.
- Operator-approved exception still enters Governance Control Plane.

flapping_protection_defined=true
