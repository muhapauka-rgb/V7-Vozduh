# E35.C Authority Verdict Engine

## Verdicts

### ALLOW

Meaning:

Action may proceed to the next runtime gate or execution-time recheck.

Operator visibility:

Show "Разрешено" plus authority chain.

Runtime meaning:

Consumer may continue. It still must not skip execution-time recheck.

Audit requirement:

Record verdict event.

Escalation path:

None.

Rollback requirement:

If action mutates routing later, rollback manifest must exist.

### DENY

Meaning:

Action must not proceed.

Operator visibility:

Show hard block reason and next safe action.

Runtime meaning:

Consumer must fail closed.

Audit requirement:

Record denial event.

Escalation path:

Only explicit review/new proposal/new governance packet can change outcome.

Rollback requirement:

No forward rollback because no movement happened.

### REVIEW_REQUIRED

Meaning:

Machine cannot safely decide without human/governance review.

Operator visibility:

Show review queue item with conflict/input details.

Runtime meaning:

No forward movement.

Audit requirement:

Create review event.

Escalation path:

Operator/governance must decide.

Rollback requirement:

None unless later approved action moves user.

### EMERGENCY_ONLY

Meaning:

Normal forward movement is denied, but containment/rollback action may proceed if scoped.

Operator visibility:

Show emergency state and temporary nature.

Runtime meaning:

Only emergency consumer may use this verdict.

Audit requirement:

Emergency event required.

Escalation path:

Containment or governance.

Rollback requirement:

Return/rollback plan required.

## Verdict Priority

If multiple verdicts apply:

```text
DENY > EMERGENCY_ONLY > REVIEW_REQUIRED > ALLOW
```

Exception:

If Safety says no mutation at all, final verdict is `DENY`, not `EMERGENCY_ONLY`.

## Verdict Output Shape

```json
{
  "verdict": "DENY",
  "verdict_reason": "operator_pinned",
  "authority_chain": ["Safety:PASS", "Governance:PASS", "Operator:DENY"],
  "conflicts": [],
  "allowed_actions": [],
  "review_required": false,
  "emergency": false,
  "admin_message": "Пользователь закреплён оператором",
  "audit_required": true
}
```

## Verdict

```text
verdict_engine_defined=true
```
