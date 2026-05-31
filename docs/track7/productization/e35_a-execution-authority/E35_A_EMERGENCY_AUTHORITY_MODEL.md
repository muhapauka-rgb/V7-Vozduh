# E35.A Emergency Authority Model

## Purpose

Emergency authority exists to reduce harm without weakening normal governance.

It is not a shortcut for speed, preference, rebalancing or convenience.

## Emergency Triggers

Emergency authority may activate when current user target has:

- channel failed;
- health/severity hard failure;
- quarantine;
- required service hard down;
- Telegram hard-blocked for Telegram-required user;
- runtime trust blocking current route;
- safety violation;
- failed verification threshold;
- containment requested by governance.

## Emergency Outcomes

| Condition | Outcome |
|---|---|
| pinned target hard-fails | `EMERGENCY_ONLY` escape allowed |
| manual target hard-fails | `EMERGENCY_ONLY` escape allowed |
| target only slower | `DENY` emergency |
| target lower score | `DENY` emergency |
| group preferred elsewhere | `DENY` emergency |
| capacity conflict but current still safe | `REVIEW_REQUIRED` |

## Who May Move?

| Owner | Emergency Move Allowed? | Notes |
|---|---:|---|
| CONTAINMENT | Yes | Primary emergency authority. |
| GOVERNANCE | Yes | If packet explicitly includes containment scope. |
| OPERATOR | Yes | Manual emergency action with audit. |
| AUTOSWITCH | Only if configured as containment/failover, not normal planned move. |
| SCHEDULER | No direct authority. |

## Where May User Move?

Emergency target must be:

- not the failed target;
- enabled;
- not quarantined;
- compatible with group hard constraints unless no safe group target exists and operator review is required;
- required-services suitable or least-risk target;
- capacity-safe or explicitly marked emergency overflow;
- rollback/return plan recorded.

## Duration

Emergency placement must be temporary.

Recommended defaults:

- `emergency_lease_seconds=3600`;
- extend only by operator/governance review;
- after expiry, state becomes `REVIEW_REQUIRED`.

## Operator Notification

Admin must show:

- emergency state on Home;
- emergency banner in User drawer;
- original pinned/manual target;
- temporary target;
- trigger reason;
- return status;
- next safe action.

## Return Model

Return is allowed only when:

- original target is healthy;
- required services pass;
- restore-settle GO;
- runtime checkers OK;
- no selected moves/hidden movers;
- authority still expects return.

Return may be:

- operator-confirmed;
- governance packet;
- future scheduler action with explicit authority.

## Audit

Every emergency action records:

- trigger;
- actor/owner;
- source target;
- emergency target;
- evidence bundle;
- created_at;
- expires_at;
- return target;
- return outcome.

## Tests

- pinned user emergency escape;
- manual user emergency escape;
- no emergency for speed-only improvement;
- emergency lease expiry;
- return blocked when target remains unhealthy;
- return allowed after recovery and restore-settle.

## Verdict

```text
emergency_authority_defined=true
```
