# Program F Rollback Reliability

Date: 2026-06-01
Status: PREVIEW_READY_EXECUTION_NOT_PERFORMED

## Rollback Preview

For the proposed movement:

- user: `10.7.0.16`
- proposed movement: `vless -> awg3`
- rollback target: `vless`
- rollback command: `v7-user-switch 10.7.0.16 vless`

## Certification

Rollback path is preview-ready, but rollback reliability cannot be fully certified without:

1. approved forward movement
2. post-movement verification
3. rollback packet execution or rollback rehearsal
4. rollback observation

rollback_reliable=false

