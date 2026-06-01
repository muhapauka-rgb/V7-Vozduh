# Block A Single User Certification

Project: V7 Vozduh

Block: A - Single User Completion Program

## Lifecycle

Certified lifecycle:

```text
egress 1 -> execution egress -> egress 1
```

User:

- `10.7.0.11`

Execution egress:

- `amneziawg-exec-20260528-10-8-1-14`

Rollback egress:

- `1`

## Certification Criteria

- Single user only: passed
- No second user touched: passed
- No batch movement: passed
- No autoswitch apply: passed
- No rebalance: passed
- No deploy: passed
- No systemd changes: passed
- No routing outside table `1009`: passed
- Existing runtime movement implementation reused: passed
- Rollback observed and certified: passed

## Verdict

`single_user_movement_certified=true`

