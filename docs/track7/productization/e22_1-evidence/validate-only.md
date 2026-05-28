# E22.1 Validate-Only Result

The fresh VPS packet was validated with the same E22 packet-consumer semantics.

```json
{
  "errors": [],
  "ok": true,
  "verdict": "PACKET_VALID"
}
```

Validated constraints:

```text
selected_move_budget=0
allowed_users=[]
allowed_targets=[]
user_movement_allowed=false
routing_mutation_allowed=false
runtime_action=RECHECK_AND_RECORD_ONLY
dual_confirmations=present
approval_expiry=fresh
```
