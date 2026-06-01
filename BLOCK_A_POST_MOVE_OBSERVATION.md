# Block A Post-Move Observation

Project: V7 Vozduh

Block: A - Single User Completion Program

Observation target: post P6 move, before Block A rollback

## Observed State

The single approved user was still on the execution egress before rollback:

- User: `10.7.0.11`
- Current egress: `amneziawg-exec-20260528-10-8-1-14`
- Route table: `1009`
- Route table default: `default dev v7execwg0 scope link`

Counts:

- Source egress `1`: `9`
- Execution egress `amneziawg-exec-20260528-10-8-1-14`: `1`

## Stability Signals

- Selected move queue count: `0`
- Autoswitch timer: `inactive`
- Outside user hash stable through rollback recheck
- Egress registry hash stable through rollback recheck
- Rules hash stable through rollback recheck
- Routes outside table `1009` hash stable through rollback recheck

## Observation Verdict

- Post-move observation passed: true
- Move was observable and bounded: true
- Ready for move certification: true

