# E35.B Containment Boundaries

## Product Meaning

Containment exists to reduce harm.

It is emergency authority, not normal routing authority.

## What Containment May Override

Containment may temporarily override:

- OPERATOR_PINNED;
- MANUAL;
- group restrictions;
- autoswitch denial;
- normal governance scheduling;
- current sticky placement.

Only when:

- current channel is dead;
- required services are unavailable in hard state;
- target is quarantined;
- runtime trust is broken;
- rollback is required;
- safety violation exists.

## What Containment May Never Override

Containment cannot:

- bypass kill switch if kill switch blocks all mutation;
- perform convenience movement;
- move for speed/score/rebalance;
- exceed emergency scope;
- leave user in emergency state without expiry/review;
- hide action from operator.

## Lifetime

Containment overrides are temporary.

Recommended:

```text
default_emergency_lease_seconds=3600
```

Expiry outcome:

- `REVIEW_REQUIRED` if original target not healthy;
- return available if original target recovered and restore-settle GO.

## Operator Notification

Admin must show:

- emergency state on Home;
- user emergency banner;
- original target;
- emergency target;
- trigger reason;
- expiry;
- return plan.

## Recovery

Recovery requires:

- target recovered;
- restore-settle GO;
- runtime checkers OK;
- required services OK;
- no selected moves/hidden movers;
- operator/governance confirmation when required.

## Runtime Mapping

Containment maps to:

- rollback paths;
- emergency authority event;
- authority state emergency fields;
- future containment evaluator.

## Tests

- containment override allowed for pinned dead channel;
- containment denied for faster channel;
- emergency lease expires;
- operator sees emergency state;
- return blocked until target recovers.

## Verdict

```text
containment_boundaries_defined=true
```
