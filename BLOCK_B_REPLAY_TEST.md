# Block B Replay Test

Project: V7 Vozduh

Block: B - Small Batch Program

Replay test source:

- `/tmp/block-b-small-batch-20260601T105928Z/replay_test.json`

## Results

```json
{
  "duplicate_packet": "duplicate_packet",
  "expired_packet": "expired_packet",
  "invalid_scope": "invalid_users",
  "valid_packet": "ok"
}
```

## Verdict

- Duplicate packet denied: true
- Expired packet denied: true
- Invalid scope denied: true
- Valid packet accepted before execution: true

`replay_protection_verified=true`

