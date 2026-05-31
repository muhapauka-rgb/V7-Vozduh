# E35.A Routing Modes Model

## Final Routing Modes

E35.A finalizes three routing modes:

```text
AUTO
OPERATOR_PINNED
MANUAL
```

## AUTO

Product meaning:

System manages routing.

Operator meaning:

The operator delegates routing authority to V7.

Allowed movement:

- autoswitch may recommend and move when apply authority exists;
- governance may move under packet scope;
- scheduler may later launch approved batches;
- containment may move for safety.

Required gates:

- required services pass;
- suitability pass;
- capacity pass;
- runtime trust pass;
- restore-settle pass;
- execution authority pass.

Admin surface:

- Users drawer shows `Режим: Авто`;
- "Почему пользователь здесь" explains current route and relevant gates.

Storage:

```json
{
  "routing_mode": "AUTO",
  "routing_owner": "AUTOSWITCH",
  "preferred_egress": "",
  "authority_expires_at": ""
}
```

Tests:

- AUTO user can be selected when gates pass;
- AUTO user is denied when service/capacity/safety/gate fails.

## OPERATOR_PINNED

Product meaning:

Operator owns routing decision. User should remain on chosen channel.

Operator meaning:

V7 must not move the user merely because another channel is faster, scores higher, or is group-preferred.

Normal movement rules:

- autoswitch forward movement away from pinned target: `DENY`;
- speed/scoring/preference cannot override pin;
- governance movement requires explicit pin override or operator confirmation;
- operator can remove or change pin.

Emergency exceptions:

System may move pinned user only if:

- pinned channel fails;
- pinned channel becomes unhealthy/quarantined;
- required services are unavailable;
- runtime safety violation appears;
- containment/rollback is required.

Emergency escape model:

1. Detect hard safety/service/runtime failure on pinned target.
2. Authority outcome becomes `EMERGENCY_ONLY`.
3. Candidate target must be known safe, suitable and within containment scope.
4. Event is logged as emergency override, not normal autoswitch.
5. Operator sees emergency state.

Emergency return model:

1. Continue monitoring pinned target.
2. When target recovers and restore-settle is GO, present return action or governed return.
3. Do not silently return if return would violate current gates.

Pin persistence rules:

- default: persistent until removed;
- optional expiry allowed;
- expired pin becomes `AUTO` or `REVIEW_REQUIRED` according to group defaults;
- pin history remains in audit.

Admin surface:

- Users drawer: pinned target, owner, reason, age, expiry, emergency state;
- Channels drawer: pinned users;
- Logs: pin creation/removal/emergency override.

Storage:

```json
{
  "routing_mode": "OPERATOR_PINNED",
  "routing_owner": "OPERATOR",
  "preferred_egress": "1",
  "pin_created_by": "admin",
  "pin_created_at": "ISO-8601",
  "pin_evidence_bundle": "",
  "pin_proposal_id": "",
  "pin_comment": "",
  "authority_expires_at": ""
}
```

Tests:

- pinned user does not move for higher score;
- pinned user does not move for faster channel;
- pinned user emergency-moves when pinned target hard-fails;
- pinned user return is visible and auditable.

## MANUAL

Product meaning:

Human owns routing; system does not perform autonomous forward movement.

Evidence-based verdict:

`MANUAL` should exist in the model now, but implementation can remain limited until UI/product policy is ready.

Reason:

- admin manual switch already exists;
- channel `manual_only` exists;
- current system lacks durable user-level manual intent;
- without a `MANUAL` mode, admin manual movement can be misread as `AUTO`.

Rules:

- autoswitch forward movement: `DENY`;
- scheduler forward movement: `DENY` unless operator converts mode or approves explicit governed packet;
- governance packet: `REVIEW_REQUIRED` unless packet includes explicit manual override;
- containment/rollback: allowed under emergency rules.

Admin surface:

- Users drawer: `Режим: Ручной`;
- operator sees that V7 will not autonomously move user.

Storage:

```json
{
  "routing_mode": "MANUAL",
  "routing_owner": "OPERATOR",
  "authority_reason": "manual_assignment",
  "authority_created_at": "ISO-8601",
  "authority_expires_at": "optional"
}
```

Tests:

- MANUAL user blocks autoswitch;
- rollback/containment remains possible;
- expiry transitions to review or default group mode.

## Verdict

```text
routing_modes_finalized=true
manual_mode_should_exist_now=true
manual_mode_initial_implementation_may_be_operator_visible_read_write_without_autonomous_execution=true
```
