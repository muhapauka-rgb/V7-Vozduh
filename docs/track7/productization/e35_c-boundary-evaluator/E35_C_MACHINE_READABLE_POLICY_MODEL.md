# E35.C Machine-Readable Policy Model

## Purpose

Future runtime components must evaluate the same constitutional rules consistently.

Policy must be both:

- human-readable;
- machine-readable.

## Policy Shape

```json
{
  "schema_version": "e35c.boundary-policy.v1",
  "priority": [
    "SAFETY",
    "CONTAINMENT",
    "GOVERNANCE",
    "OPERATOR",
    "GROUP",
    "USER_INTENT",
    "AUTOSWITCH",
    "SCHEDULER",
    "SCORE_SPEED",
    "PROPOSAL"
  ],
  "rules": [
    {
      "rule_id": "operator_pin_blocks_autoswitch",
      "category": "AUTHORITY",
      "priority": 400,
      "when": {
        "actor": "AUTOSWITCH",
        "routing_mode": "OPERATOR_PINNED",
        "action_type": "FORWARD_MOVE"
      },
      "outcome": "DENY",
      "reason": "operator_pinned",
      "admin_message": "Пользователь закреплён оператором"
    }
  ],
  "conflicts": [],
  "review_categories": [],
  "emergency_categories": []
}
```

## Rule Categories

- `SAFETY`
- `CONTAINMENT`
- `GOVERNANCE`
- `OPERATOR`
- `GROUP`
- `USER_INTENT`
- `AUTOSWITCH`
- `SCHEDULER`
- `SCORE_SPEED`
- `PROPOSAL`

## Rule Outcomes

- `ALLOW`
- `DENY`
- `REVIEW_REQUIRED`
- `EMERGENCY_ONLY`

## Conflict Categories

- `OPERATOR_PIN_VS_GROUP`
- `OPERATOR_PIN_VS_REQUIRED_SERVICES`
- `OPERATOR_PIN_VS_SAFETY`
- `AUTOSWITCH_VS_GOVERNANCE`
- `GROUP_VS_USER_INTENT`
- `SCHEDULER_VS_OPERATOR`
- `PROPOSAL_VS_AUTHORITY`

## Escalation Categories

- `OPERATOR_REVIEW`
- `GOVERNANCE_PACKET_REQUIRED`
- `CONTAINMENT_REQUIRED`
- `SAFETY_RECHECK_REQUIRED`
- `POLICY_CLARIFICATION_REQUIRED`

## Review Categories

- group conflict;
- authority conflict;
- stale trust;
- unknown suitability;
- expired authority;
- policy ambiguity;
- operator override request.

## Emergency Categories

- current channel dead;
- required service hard down on current channel;
- target quarantined;
- runtime trust broken;
- rollback required.

## Tests

- policy loads with schema version;
- priorities are unique/stable;
- unknown category fails closed;
- rule output is deterministic.

## Verdict

```text
machine_readable_policy_model_defined=true
```
