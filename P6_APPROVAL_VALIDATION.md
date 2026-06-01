# P6 Approval Validation

Project: V7 Vozduh

Block: P6

## Validation Result

Approval validation result:

```json
{
  "approval_valid": true,
  "errors": []
}
```

## Checks

- approval author present: true
- approval reviewer present: true
- author and reviewer distinct: true
- approval TTL valid at movement time: true
- movement budget exactly `1`: true
- allowed user exactly `10.7.0.11`: true
- allowed target exactly `amneziawg-exec-20260528-10-8-1-14`: true
- rollback target exactly `1`: true
- route table exactly `1009`: true
- runtime hashes match packet: true

## Verdict

- approval_valid=true
