# E32.1.5 Status Impact Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

status_impact_model_defined=true

## Runtime Behavior By Status

| Status | Forward | Rollback | Approval Packet | Target Eligibility | Scheduler Eligibility |
| --- | --- | --- | --- | --- | --- |
| CERTIFIED | Allowed if all gates pass | Allowed | Executable packet allowed up to effective cap | Eligible | Eligible only under policy cap |
| STALE | Denied | Allowed as containment | Non-executable draft or refresh required | Not forward-eligible | Not eligible |
| DEGRADED | Denied | Allowed as containment | Denied except rollback/remediation plan | Not forward-eligible | Not eligible |
| EXPIRED | Denied | Allowed if exact scope known | Denied | Not forward-eligible | Not eligible |
| REVOKED | Denied | Containment only after incident review | Denied | Not eligible | Not eligible |
| CANDIDATE | Denied | Not applicable unless rollback from prior execution | Draft only | Prep only | Not eligible |
| VALIDATING | Denied for new class | Allowed for containment | Draft only | Prep only | Not eligible |
| UNKNOWN | Denied | Only if exact rollback manifest exists | Denied | Not eligible | Not eligible |

## Status Overrides

No status can override:

- execution-time recheck;
- exact approved user set;
- rollback manifest;
- replay denial;
- audit append requirement.

## Degraded Target Rule

If a target becomes DEGRADED during forward observation:

- no further forward movement is allowed;
- rollback or containment may proceed;
- target enters recertification after root-cause review.

