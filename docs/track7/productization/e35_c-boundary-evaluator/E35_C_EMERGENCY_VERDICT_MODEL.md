# E35.C Emergency Verdict Model

## Definition

`EMERGENCY_ONLY` means:

```text
Normal forward action is denied, but a bounded containment/rollback action may proceed.
```

## Who May Create It?

- Boundary Evaluator when emergency inputs are valid.
- Governance packet recheck when packet declares containment scope.
- Future containment service when hard trigger is detected.

## Who May Approve It?

- Operator for manual containment;
- Governance for packet-bound containment;
- Safety/containment policy for pre-approved emergency escape class.

## Who May Consume It?

- Containment action;
- rollback action;
- emergency return action.

Autoswitch may consume it only if running in explicitly labeled containment/failover mode, not planned movement.

## Expiration

Emergency verdicts are short-lived.

Recommended:

```text
emergency_verdict_ttl_seconds=300
emergency_placement_lease_seconds=3600
```

## Can Emergency Become Permanent?

No.

Emergency placement must become:

- returned;
- reviewed and converted to operator/governance authority;
- expired into REVIEW_REQUIRED.

## Can Emergency Bypass Governance?

No for normal execution.

It may use pre-approved containment policy only if:

- scope is bounded;
- trigger is hard;
- audit is mandatory;
- return plan exists.

## Can Emergency Bypass Safety?

No.

If safety says no mutation at all, final verdict is `DENY`.

## Can Emergency Bypass Containment?

No.

Emergency is containment; it cannot exceed containment rules.

## Required Evidence

- trigger reason;
- current target state;
- proposed emergency target;
- expected return target;
- expiry;
- actor;
- audit link.

## Verdict

```text
emergency_model_defined=true
```
