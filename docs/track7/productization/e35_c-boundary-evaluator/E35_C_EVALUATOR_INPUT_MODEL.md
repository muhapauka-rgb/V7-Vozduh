# E35.C Evaluator Input Model

## Proposed Action

Required:

```json
{
  "action_id": "act_<id>",
  "action_type": "FORWARD_MOVE",
  "actor": "AUTOSWITCH",
  "user_ip": "10.7.0.11",
  "current_channel": "1",
  "target_channel": "awg2",
  "requested_at": "ISO-8601",
  "reason": "candidate_score_beats_current"
}
```

Supported action types:

- `FORWARD_MOVE`
- `ROLLBACK`
- `EMERGENCY_ESCAPE`
- `EMERGENCY_RETURN`
- `AUTHORITY_STATE_CHANGE`
- `SCHEDULED_EXECUTION_START`
- `GOVERNED_EXECUTION_START`

## Full Input Envelope

```json
{
  "proposed_action": {},
  "user": {},
  "current_channel": {},
  "target_channel": {},
  "routing_authority": {},
  "group_boundary": {},
  "required_services": {},
  "suitability": {},
  "capacity": {},
  "governance": {},
  "runtime_trust": {},
  "release_trust": {},
  "restore_settle": {},
  "selected_moves": {},
  "hidden_movers": {},
  "proposal_context": {},
  "containment_context": {},
  "emergency_context": {},
  "audit_context": {}
}
```

## Input Categories

| Category | Meaning | Missing Behavior |
|---|---|---|
| User | identity, current route, group | `DENY` for movement |
| Current Channel | current target health/status | `REVIEW_REQUIRED` or emergency if known failed |
| Target Channel | target status/eligibility | `DENY` |
| Routing Authority | mode/owner/pin/manual | `REVIEW_REQUIRED` |
| Group Boundary | allow/exclude/required services | `REVIEW_REQUIRED` |
| Required Services | effective services and pass/fail | `REVIEW_REQUIRED` or `DENY` in strict mode |
| Suitability | current/candidate hard blocks | `REVIEW_REQUIRED` |
| Capacity | hard limit and availability | `DENY` for forward |
| Governance | packet/scope/replay/hash | `DENY` if required and missing/stale |
| Runtime Trust | runtime OK/drift/blocking | `DENY` for forward |
| Release Trust | release/runtime match | `REVIEW_REQUIRED` or `DENY` if policy strict |
| Restore-Settle | GO/NO-GO | `DENY` forward |
| Selected Moves | count/hash | `DENY` if unexpected non-zero |
| Hidden Movers | scan result | `DENY` |
| Proposal Context | explanatory only | no authority |
| Containment Context | emergency scope | `DENY` if missing for emergency |
| Emergency Context | trigger/lease/return | `DENY` if invalid |
| Audit Context | lineage/event target | `REVIEW_REQUIRED` if unavailable |

## Output Linkage

Every input source used should be reflected in output:

- `input_hash`;
- `source`;
- `freshness`;
- `decision_reasons`.

## Verdict

```text
evaluator_input_model_defined=true
```
